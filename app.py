from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(
    api_key=os.getenv("AIzaSyA7v84GquxcvY-zNVTUMd1S65xevArX8Nk")
)

model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/", methods=["POST"])
def alexa():

    data = request.get_json(silent=True)

    # DEBUG seguro
    if not data:
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "No llegó JSON"
                },
                "shouldEndSession": False
            }
        })

    request_type = data.get("request", {}).get("type")

    # LaunchRequest
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

    # IntentRequest
    if request_type == "IntentRequest":

        user_text = "hola"

        try:
            user_text = data["request"]["intent"]["slots"]["text"]["value"]
        except:
            pass

        try:
            response = model.generate_content(user_text)
            ai_text = response.text
        except Exception as e:
            print("ERROR GEMINI:", e)
            ai_text = f"Error en Gemini con: {user_text}"

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