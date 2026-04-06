import torch
import torch.nn as nn
import timm
import os

NUM_CLASSES = 38

def load_model():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    model_path = os.path.join(BASE_DIR, "model", "final_plant_disease_model.pth")

    print("Loading model from:", model_path)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model NOT found at {model_path}")

    model = timm.create_model('efficientnet_b0', pretrained=False)
    model.classifier = nn.Linear(model.classifier.in_features, NUM_CLASSES)

    model.load_state_dict(
        torch.load(model_path, map_location="cpu")
    )

    model.eval()
    return model