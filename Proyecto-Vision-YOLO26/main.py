import os
import tempfile

# Ultralytics escribe un settings.yaml al importarse. Usamos el temporal del
# sistema (no "/tmp" a secas) para que funcione igual en macOS, Linux y Windows.
os.environ.setdefault(
    "YOLO_CONFIG_DIR", os.path.join(tempfile.gettempdir(), "ultralytics")
)

import io
import cv2
import numpy as np
from enum import Enum
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

app = FastAPI(title='Deploying un Modelo ML con FastAPI - YOLO26')


class Model(str, Enum):
    yolo26n = "yolo26n"
    yolo26s = "yolo26s"


# Cache de modelos: se carga una sola vez, no en cada request.
_models = {}


def get_model(name: str) -> YOLO:
    if name not in _models:
        _models[name] = YOLO(f"{name}.pt")
    return _models[name]


@app.get("/")
def home():
    return "Congratulations! Your API is working as expected."


@app.post("/predict")
def prediction(model: Model, file: UploadFile = File(...)):

    # 1. VALIDATE INPUT FILE
    filename = file.filename
    fileExtension = filename.split(".")[-1].lower() in ("jpg", "jpeg", "png")
    if not fileExtension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")

    # 2. TRANSFORM RAW IMAGE INTO CV2 image
    image_stream = io.BytesIO(file.file.read())
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # 3. RUN OBJECT DETECTION MODEL
    results = get_model(model.value).predict(image, conf=0.1, verbose=False)
    output_image = results[0].plot()  # BGR con las cajas ya dibujadas

    # 4. ENCODE AND RETURN IMAGE
    _, img_encoded = cv2.imencode('.jpg', output_image)
    return StreamingResponse(
        io.BytesIO(img_encoded.tobytes()),
        media_type="image/jpeg"
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
