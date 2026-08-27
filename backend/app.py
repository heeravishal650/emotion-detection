from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


@app.get("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Emotion Detection API is running"
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.post("/analyze")
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image was uploaded"}), 400

    try:
        image_bytes = request.files["image"].read()
        np_array = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Invalid image"}), 400

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.2,
            minNeighbors=6,
            minSize=(30, 30)
        )

        emotions = []

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]

            try:
                result = DeepFace.analyze(
                    face_roi,
                    actions=["emotion"],
                    enforce_detection=False
                )

                if isinstance(result, list):
                    emotion = result[0]["dominant_emotion"]
                else:
                    emotion = result["dominant_emotion"]

            except Exception:
                emotion = "Unknown"

            emotions.append({
                "emotion": emotion,
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h)
            })

        return jsonify({"emotions": emotions})

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
