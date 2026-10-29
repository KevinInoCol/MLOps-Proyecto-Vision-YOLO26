# Despliegue YOLO26

Servicio independiente. No interfiere con `Proyecto-Vision-Deploy` (YOLOv3):
distinto nombre de imagen y distinto nombre de servicio, mismo Artifact Registry.

Los comandos son **los mismos** que en el proyecto YOLOv3. PyTorch se instala
dentro de Cloud Build, no en tu Mac.

## Paso 0: Vinculacion (si no lo hiciste ya)
gcloud init

## Paso 1: Repositorio (ya existe, se reutiliza — omitir)
gcloud artifacts repositories create repositorio-mlops-inofuente --repository-format docker --project datapath-mlops-kevin-inofuente --location us-central1

## Paso 2: Crear la imagen y subir al repositorio
gcloud builds submit --config=cloudbuild.yaml --project datapath-mlops-kevin-inofuente

## Paso 3: Despliegue de la imagen: Container
gcloud run services replace service.yaml --region us-central1 --project datapath-mlops-kevin-inofuente

## Paso 4: (OPCIONAL) Dar permisos de acceso publico (una sola vez)
gcloud run services set-iam-policy servicio-proyecto-vision-yolo26-kevin-inofuente gcr-service-policy.yaml --region us-central1 --project datapath-mlops-kevin-inofuente


# Prueba local (opcional, en tu Mac)

uv sync
uv run uvicorn application.main:app --reload --port 8080

Luego abre http://localhost:8080/docs


# Comparacion contra YOLOv3 (para el informe del modulo)

## Tamano de cada imagen en el registry
gcloud artifacts docker images list us-central1-docker.pkg.dev/datapath-mlops-kevin-inofuente/repositorio-mlops-inofuente --include-tags --project datapath-mlops-kevin-inofuente

## Cold start: forzar instancia nueva y medir el primer request
gcloud run services update servicio-proyecto-vision-yolo26-kevin-inofuente --region us-central1 --project datapath-mlops-kevin-inofuente --min-instances 0

curl -o /dev/null -s -w "total: %{time_total}s\n" \
  -X POST "<URL_DEL_SERVICIO>/predict?model=yolo26n" \
  -F "file=@imagen.jpg"

Corre el mismo curl dos veces: la primera incluye el cold start,
la segunda es el tiempo de inferencia puro.


# Notas

- El endpoint es identico al de YOLOv3: POST /predict?model=...&file=<imagen>
  Modelos disponibles: yolo26n (5 MB, mAP 40.9) y yolo26s (19 MB, mAP 48.6).
- Dependencias fijadas en uv.lock (51 paquetes). El Dockerfile usa
  "uv sync --frozen", que FALLA el build si uv.lock quedo desincronizado de
  pyproject.toml. Es lo que hace el build reproducible.
- Si agregas o cambias una dependencia: editar pyproject.toml, correr "uv lock",
  y commitear ambos archivos juntos.
- Si quieres abaratar: baja cpu a "1" en service.yaml y pon OMP_NUM_THREADS=1
  en el Dockerfile. Deben ir siempre en pareja.
- Licencia: ultralytics es AGPL-3.0. Uso educativo OK. Para uso comercial
  cerrado hace falta Enterprise License o migrar a RF-DETR / YOLOX.
