
---
# ✍️ Signature Verification API

This project is a web-based signature verification system using:

- 🔍 **Siamese Neural Network** for comparing signatures  
- ⚡ **FastAPI** for serving a RESTful backend  
- 🧠 **TensorFlow** for the trained model  
- 🔎 **FAISS** for fast similarity search  
- 🖼️ **OpenCV** for detecting signature regions  
- 🌐 A clean frontend to upload and verify signatures

---

## 🚀 Features

- Upload an image of a signature
- System crops the signature automatically
- Returns:
  - ✅ Whether it's genuine or forged
  - 📊 Similarity score
  - ⏱ Processing time
- Mobile-responsive UI

---

## 🛠 Setup Instructions (macOS/Windows)

### 1. Clone the Repository

```bash
git clone https://github.com/1202DREAMSCAPE/Thesis_Signature_Verification_FASTAPI
cd signature_verification_fastapi
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

(If `requirements.txt` doesn’t exist yet, ask [Raffy] to export it using `pip freeze > requirements.txt`)

### 4. Ensure Files Are in Place

Ensure you have:
- ✅ `model/triplet_model.keras`  → trained TensorFlow model
- ✅ `model/signature_index.faiss` → saved FAISS index
- ✅ `utils/detector.py`           → contains `detect_signature()` logic
- ✅ `main.py`                     → FastAPI app
- ✅ `templates/index.html`        → Web UI
- ✅ `static/style.css` (optional) → Styling

Create folders if needed:
```bash
mkdir -p model static templates
```

---

## ▶️ Run the App

```bash
uvicorn main:app --reload
```

You’ll see:
```
Uvicorn running on http://127.0.0.1:8000
```

---

## 🌐 Access the App

- UI: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Test with Postman

**POST** to `/verify`  
- Body: `form-data`
- Key: `signature` (File) → Upload an image

📥 Response:
```json
{
  "is_genuine": true,
  "similarity_score": 0.873,
  "processing_time": 0.043
}
```

---

## 📁 Project Structure

```
signature_verification_fastapi/
│
├── main.py
├── model/
│   ├── triplet_model.keras
│   └── signature_index.faiss
├── utils/
│   └── detector.py
├── templates/
│   └── index.html
├── static/
│   └── style.css 
├── README.md
└── requirements.txt
```

---

## 🧠 Notes

- Signature cropping uses OpenCV to locate contours
- FAISS compares input signature to genuine reference signatures
- Model uses a Triplet Network trained with adaptive margin and SMOTE-balanced data

---

```