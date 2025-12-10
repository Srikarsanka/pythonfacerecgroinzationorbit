from fastapi import FastAPI, UploadFile, File
import face_recognition
import numpy as np
from PIL import Image
import io

app = FastAPI()

@app.post("/encode")
async def encode_face(file: UploadFile = File(...)):
    try:
        img_bytes = await file.read()

        # Convert bytes → image
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img_array = np.array(img)

        # Generate encoding
        encodings = face_recognition.face_encodings(img_array)

        if len(encodings) == 0:
            return {"error": "No face detected"}

        return {"embedding": encodings[0].tolist()}

    except Exception as e:
        return {"error": str(e)}
