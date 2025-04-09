from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import tensorflow as tf
import faiss
import numpy as np
import time
import cv2
import os
from utils.detector import detect_signature

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load model + FAISS index once
model = tf.keras.models.load_model("model/triplet_model.keras")
index = faiss.read_index("model/signature_index.faiss")

# Preprocess image
def preprocess_image(image):
    image = cv2.resize(image, (220, 155))
    image = image / 255.0
    return np.expand_dims(image, axis=0)

# Normalize embedding
def get_embedding(image):
    emb = model.predict(image, verbose=0)
    return emb / np.linalg.norm(emb)

# Homepage (UI)
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API Endpoint
@app.post("/verify")
async def verify_signature(signature: UploadFile = File(...)):
    try:
        # Save uploaded file
        path = "static/uploaded.png"
        with open(path, "wb") as f:
            f.write(await signature.read())

        # Detect signature region
        cropped_path = detect_signature(path)

        # Read and preprocess
        image = cv2.imread(cropped_path)
        image = preprocess_image(image)
        embedding = get_embedding(image)

        # Search in FAISS
        start = time.time()
        distances, _ = index.search(embedding, 1)
        duration = round(time.time() - start, 4)
        score = round(1 / (1 + distances[0][0]), 4)
        is_genuine = score > 0.5

        return {
            "is_genuine": is_genuine,
            "similarity_score": score,
            "processing_time": duration
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
