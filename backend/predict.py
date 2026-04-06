import torch
import timm
import json
import os
import numpy as np
import cv2

from PIL import Image
import torchvision.transforms as transforms

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# load classes
classes_path = os.path.join(BASE_DIR, "classes.json")

with open(classes_path) as f:
    classes = json.load(f)

# load disease database
database_path = os.path.join(BASE_DIR, "data", "disease_database.json")

with open(database_path) as f:
    disease_db = json.load(f)

# image preprocessing
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485,0.456,0.406],
        [0.229,0.224,0.225]
    )
])

# load model
model_path = os.path.join(BASE_DIR,"model","final_plant_disease_model.pth")

model = timm.create_model(
    "efficientnet_b0",
    pretrained=False,
    num_classes=len(classes)
)

model.load_state_dict(torch.load(model_path,map_location=device))
model.to(device)
model.eval()


# severity detection
def estimate_severity(image_path):

    img = cv2.imread(image_path)
    img = cv2.resize(img,(256,256))

    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower = np.array([10,40,40])
    upper = np.array([35,255,255])

    mask = cv2.inRange(hsv,lower,upper)

    infected_ratio = np.sum(mask>0)/(256*256)

    if infected_ratio < 0.05:
        return "Mild"

    elif infected_ratio < 0.20:
        return "Moderate"

    else:
        return "Severe"


def predict_disease(image_path):

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():

        outputs = model(image)
        _,pred = torch.max(outputs,1)

    disease_name = classes[pred.item()]

    severity = estimate_severity(image_path)

    return {

        "prediction": disease_name,
        "severity": severity,
        "details": disease_db.get(disease_name,{})

    }