import os
import json
import torch
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from torchvision import transforms
from model import load_model
from rag import rag_agent

app = FastAPI()

# ---------------------------
# CORS (IMPORTANT)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# BASE PATH
# ---------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ---------------------------
# LOAD MODEL
# ---------------------------
model = load_model()

# ---------------------------
# LOAD CLASSES
# ---------------------------
classes_path = os.path.join(BASE_DIR, "classes.json")

with open(classes_path, "r") as f:
    class_labels = json.load(f)

# ---------------------------
# TRANSFORM
# ---------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# ---------------------------
# API ROUTE
# ---------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        print("📸 Image received")

        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        img_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(img_tensor)
            probs = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)

        class_name = class_labels[predicted.item()]

        print("✅ Prediction:", class_name)

        rag_output = rag_agent(class_name, float(confidence.item()))

        return {
            "prediction": class_name,
            "confidence": float(confidence.item()),
            "rag_analysis": rag_output
        }

    except Exception as e:
        print("🔥 BACKEND ERROR:", e)
        return {"error": str(e)}