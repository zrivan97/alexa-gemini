from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# API KEY GEMINI
genai.configure(
    api_key="AIzaSyA7v84GquxcvY-zNVTUMd1S65xevArX8Nk"
)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["POST"])
def alexa():

    data = request.json

    request_type = data["request"]["type"]

    # Cuando Alexa abre la skill
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

    # Cuando el usuario pregunta
    if request_type == "IntentRequest":

        user_text = data["request"]["intent"]["slots"]["text"]["value"]

        response = model.generate_content(user_text)

        ai_text = response.text

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)