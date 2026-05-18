from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/", methods=["POST"])
def alexa():

    data = request.get_json(silent=True) or {}

    request_type = data.get("request", {}).get("type", "")

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

    if request_type == "IntentRequest":

        user_text = data.get("request", {}) \
                        .get("intent", {}) \
                        .get("slots", {}) \
                        .get("text", {}) \
                        .get("value", "hola")

        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=user_text
            )
            ai_text = response.text

        except Exception as e:
            print("🔥 ERROR GEMINI REAL:", str(e))
            ai_text = "Error en Gemini: revisar logs"

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
                "text": "Request no válido"
            },
            "shouldEndSession": False
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)