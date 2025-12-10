from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import insightface
from insightface.app import FaceAnalysis
import base64
import io

app = FastAPI()

# CORS for Render & Node backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize InsightFace
model = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
model.prepare(ctx_id=0, det_size=(640, 640))


@app.post("/encode")
async def encode_face(file: UploadFile = File(...)):
    try:
        # Read image bytes
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = np.array(image)

        # Detect faces
        faces = model.get(img)

        if len(faces) == 0:
            return {"error": "No face detected"}

        # Extract original 512-dim embedding
        emb512 = faces[0].embedding.tolist()

        # Convert to 128-dim (for compatibility with your old system)
        emb128 = emb512[:128]

        return {"embedding": emb128}

    except Exception as e:
        return {"error": str(e)}
