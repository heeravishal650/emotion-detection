from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Emotion Detection API is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    if "image" not in request.files:
        return jsonify({
            "error": "No image was uploaded"
        }), 400

    try:
        image_file = request.files["image"]
        image = Image.open(image_file).convert("RGB")

        frame = np.array(image)

        result = DeepFace.analyze(
            img_path=frame,
            actions=["emotion"],
            enforce_detection=False
        )

        if isinstance(result, list):
            result = result[0]

        emotion = result.get(
            "dominant_emotion",
            "Unknown"
        )

        return jsonify({
            "emotions": [
                {
                    "emotion": emotion
                }
            ]
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )