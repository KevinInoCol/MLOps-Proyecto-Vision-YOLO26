import os
import tempfile

# Ultralytics escribe un settings.yaml al importarse. El HOME del contenedor
# puede no ser escribible, asi que lo mandamos al temporal del sistema.
# gettempdir() devuelve /tmp en el contenedor y lo correcto en Windows/macOS,
# para que este archivo sirva igual en local y en Cloud Run.
os.environ.setdefault(
    "YOLO_CONFIG_DIR", os.path.join(tempfile.gettempdir(), "ultralytics")
)

import io
import cv2
import numpy as np
from enum import Enum
from contextlib import asynccontextmanager
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse


class Model(str, Enum):
    yolo26n = "yolo26n"
    yolo26s = "yolo26s"


# Cache de modelos. Sin esto cada request reconstruiria la red desde disco,
# que era justamente el defecto de la version con cvlib.
_models: dict[str, YOLO] = {}


def get_model(name: str) -> YOLO:
    if name not in _models:
        _models[name] = YOLO(f"{name}.pt")
    return _models[name]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-carga el modelo por defecto para que el primer request real
    # no pague la inicializacion de torch.
    get_model(Model.yolo26n.value)
    yield
    _models.clear()


app = FastAPI(title="Deploying un Modelo ML con FastAPI - YOLO26", lifespan=lifespan)


@app.get("/")
def home():
    return {
        "status": "Congratulations! Your API is working as expected.",
        "backend": "ultralytics YOLO26 (PyTorch CPU)",
        "available_models": [m.value for m in Model],
        "loaded_models": sorted(_models.keys()),
    }


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
    output_image = results[0].plot()  # devuelve BGR con las cajas dibujadas

    # 4. ENCODE AND RETURN IMAGE
    _, img_encoded = cv2.imencode(".jpg", output_image)
    return StreamingResponse(
        io.BytesIO(img_encoded.tobytes()),
        media_type="image/jpeg"
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
