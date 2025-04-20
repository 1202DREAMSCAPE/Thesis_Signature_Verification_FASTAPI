from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time
import os
import random

# Uncomment these when you're ready to load real model and FAISS
# import tensorflow as tf
# import faiss
# import numpy as np
# import cv2

# 🔐 Optional: Uncomment if your model uses Lambda layers
# from keras import config
# config.enable_unsafe_deserialization()

app = FastAPI()

# Serve static files (like uploaded image preview)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 🔄 Load model and FAISS index when you're ready
# model = tf.keras.models.load_model("model/CEDAR_triplet_model.keras")
# index = faiss.read_index("model/CEDAR_signature_index.faiss")

# def get_embedding(image):
#     emb = model.predict(image, verbose=0)
#     return emb / np.linalg.norm(emb)

# def preprocess_image(image):
#     image = cv2.resize(image, (220, 155))
#     image = image / 255.0
#     return np.expand_dims(image, axis=0)

# =======================
# Home UI
# =======================
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# =======================
# Dummy /verify Endpoint
# =======================
@app.post("/verify")
async def verify_signature(signature: UploadFile = File(...)):
    try:
        # Save uploaded file so it can be previewed
        path = "static/uploaded.png"
        with open(path, "wb") as f:
            f.write(await signature.read())

        # Simulate loading + processing time
        time.sleep(1)

        # Simulate realistic random result
        random_value = random.random()
        is_genuine = random_value > 0.4  # 60% chance of being genuine
        similarity_score = round(random.uniform(0.4, 0.95), 4)
        processing_time = round(random.uniform(0.1, 0.3), 4)

        # Simulate an error case (e.g., blurry image) ~10% chance
        if random_value < 0.1:
            raise ValueError("Signature too blurry or unclear to verify.")

        return {
            "is_genuine": is_genuine,
            "similarity_score": similarity_score,
            "processing_time": processing_time
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
