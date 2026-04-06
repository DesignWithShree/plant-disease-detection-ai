from fastapi import FastAPI, UploadFile, File
import shutil
import os

from predict import predict_disease
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER,exist_ok=True)


@app.get("/")
def home():

    return {"message":"Plant Disease Detection API Running"}


@app.post("/predict")
async def predict(file:UploadFile=File(...)):

    file_path = os.path.join(UPLOAD_FOLDER,file.filename)

    with open(file_path,"wb") as buffer:

        shutil.copyfileobj(file.file,buffer)

    result = predict_disease(file_path)

    return result