// Your deployed Python backend on Render
const API_URL = "https://emotion-detection-i90e.onrender.com";

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusText = document.getElementById("status");
const emotionText = document.getElementById("emotion");

let stream = null;
let timer = null;
let busy = false;

startBtn.addEventListener("click", startCamera);
stopBtn.addEventListener("click", stopCamera);

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 }
      },
      audio: false
    });

    video.srcObject = stream;

    statusText.textContent = "Camera is running";
    startBtn.disabled = true;
    stopBtn.disabled = false;

    timer = setInterval(analyzeFrame, 1200);

  } catch (error) {
    console.error(error);
    statusText.textContent =
      "Camera permission was denied or unavailable.";
  }
}

function stopCamera() {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }

  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }

  video.srcObject = null;

  statusText.textContent = "Camera is off";
  emotionText.textContent = "Waiting...";

  startBtn.disabled = false;
  stopBtn.disabled = true;
}

async function analyzeFrame() {
  if (busy || !stream || video.readyState < 2) {
    return;
  }

  busy = true;

  try {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );

    const blob = await new Promise(resolve => {
      canvas.toBlob(resolve, "image/jpeg", 0.8);
    });

    if (!blob) {
      throw new Error("Could not create image");
    }

    const formData = new FormData();

    formData.append(
      "image",
      blob,
      "frame.jpg"
    );

    const response = await fetch(
      `${API_URL}/analyze`,
      {
        method: "POST",
        body: formData
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.error || "Server error"
      );
    }

    if (
      data.emotions &&
      data.emotions.length > 0
    ) {
      emotionText.textContent =
        data.emotions
          .map(item => item.emotion)
          .join(", ");
    } else {
      emotionText.textContent =
        "No face detected";
    }

    statusText.textContent =
      "Emotion updated";

  } catch (error) {

    console.error(error);

    statusText.textContent =
      "Could not connect to Python backend";

  } finally {

    busy = false;
  }
}