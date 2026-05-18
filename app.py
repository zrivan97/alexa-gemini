from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# =========================
# CONFIG GEMINI API KEY
# =========================
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/", methods=["POST"])
def alexa():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "No llegó JSON al servidor"
                },
                "shouldEndSession": False
            }
        })

    request_type = data.get("request", {}).get("type", "")

    # =========================
    # LaunchRequest
    # =========================
    if request_type == "LaunchRequest":
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Hola Iván, listo para ayudarte."
                },
                "shouldEndSession": False
            }
        })

    # =========================
    # IntentRequest
    # =========================
    if request_type == "IntentRequest":

        user_text = data.get("request", {}) \
                        .get("intent", {}) \
                        .get("slots", {}) \
                        .get("text", {}) \
                        .get("value", "hola")

        try:
            response = model.generate_content(str(user_text))
            ai_text = response.text

        except Exception as e:
            print("🔥 ERROR GEMINI REAL:", str(e))
            ai_text = "Error en Gemini (revisar logs)"

        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": ai_text
                },
                "shouldEndSession": False
            }
        })

    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Tipo de request no soportado"
            },
            "shouldEndSession": False
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)