# Emotion Detection Web App

This project is split into two parts:

- `frontend/` -> deploy this folder to Netlify.
- `backend/` -> deploy this folder to Render (or another Python-compatible host).

The original desktop webcam code used `cv2.VideoCapture(0)`. The web version
uses the browser's webcam API and sends frames to the Python backend, where
OpenCV + DeepFace perform emotion detection.

## 1. Deploy backend

Create a new Web Service on Render and use the `backend` folder.

Build command:
pip install -r requirements.txt

Start command:
gunicorn app:app

After deployment, copy the backend URL.

## 2. Connect frontend

Open `frontend/script.js` and change:

const API_URL = "YOUR_RENDER_BACKEND_URL";

to your real backend URL, for example:

const API_URL = "https://your-service.onrender.com";

## 3. Deploy frontend to Netlify

Upload/deploy the `frontend` folder to Netlify.

No build command is required.

Publish directory:
.

The Netlify URL uses HTTPS, so browser camera permissions can work.

## Important

Do not upload only `emotion.py` to Netlify. Netlify needs the frontend files,
while the Python/DeepFace code needs a Python server.
