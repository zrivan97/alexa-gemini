from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# API KEY GEMINI (CORRECTO)
genai.configure(
    api_key=os.environ["AIzaSyA7v84GquxcvY-zNVTUMd1S65xevArX8Nk"]
)

model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/", methods=["POST"])
def alexa():

    data = request.get_json(silent=True) or {}

    request_type = data.get("request", {}).get("type", "")

    # LaunchRequest
    if request_type == "LaunchRequest":

        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Hola Iván, soy tu asistente inteligente."
                },
                "shouldEndSession": False
            }
        })

    # IntentRequest
    if request_type == "IntentRequest":

        user_text = (
            data.get("request", {})
                .get("intent", {})
                .get("slots", {})
                .get("text", {})
                .get("value", "hola")
        )

        try:
            response = model.generate_content(user_text)
            ai_text = response.text
        except Exception:
            ai_text = "Lo siento, hubo un error procesando tu pregunta."

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

    # fallback seguro
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Solicitud no válida"
            },
            "shouldEndSession": False
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)