# MLOps-Proyecto-Vision-YOLO26

Deteccion de objetos con **YOLO26** (Ultralytics), servida con FastAPI y
desplegada en Google Cloud Run. Material del modulo de MLOps.

Version anterior del curso: YOLOv3 via `cvlib` (motor OpenCV DNN, 237 MB de
pesos). Version actual: YOLO26 via `ultralytics` (motor PyTorch, 5 MB de pesos
y mejor precision).

## Las dos carpetas

| Carpeta | Rol |
|---|---|
| [`Proyecto-Vision-YOLO26/`](Proyecto-Vision-YOLO26/) | Demo local: notebook + API con FastAPI |
| [`Proyecto-Vision-YOLO26-Deploy/`](Proyecto-Vision-YOLO26-Deploy/) | Contenedor y despliegue a Cloud Run |

## Requisitos

Solo [uv](https://docs.astral.sh/uv/). No hace falta instalar Python aparte:
uv descarga el 3.12 que el proyecto declara.

```bash
# macOS
brew install uv

# Linux / Windows (o si no usas brew)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Demo local

Paso a paso completo en [`Comandos.md`](Comandos.md).

```bash
git clone https://github.com/KevinInoCol/MLOps-Proyecto-Vision-YOLO26.git
cd MLOps-Proyecto-Vision-YOLO26/Proyecto-Vision-YOLO26
uv sync
uv run jupyter notebook server.ipynb
```

> **Importante:** el `cd` no es opcional. Cada carpeta tiene su propio
> `pyproject.toml` y la raiz del repo no tiene ninguno, asi que `uv sync` ahi
> falla con `No pyproject.toml found`.
>
> Y si usas VS Code, abre la carpeta `Proyecto-Vision-YOLO26`, **no la raiz del
> repositorio**: VS Code solo detecta el `.venv` en la raiz del workspace, asi
> que de lo contrario el entorno no aparece en "Select Kernel".

`uv sync` crea el entorno con Python 3.12 e instala las versiones exactas de
`uv.lock` — identicas en macOS, Linux y Windows.

Para levantar solo la API:

```bash
uv run uvicorn main:app --reload --port 8080
# http://localhost:8080/docs
```

## Despliegue

Ver [`Proyecto-Vision-YOLO26-Deploy/COMANDOS.md`](Proyecto-Vision-YOLO26-Deploy/COMANDOS.md).
Requiere un proyecto de GCP propio: los IDs que aparecen en `service.yaml` y
`cloudbuild.yaml` hay que reemplazarlos por los tuyos.

## Notas para quien clone esto

- **Los pesos no estan versionados.** `ultralytics` descarga `yolo26n.pt`
  (~5 MB) la primera vez que corres el notebook.
- **El entorno tampoco.** `.venv` pesa ~1.2 GB; se reconstruye con `uv sync`.
- **`pyproject.toml` + `uv.lock` se editan distinto:** el primero a mano, el
  segundo se regenera con `uv lock`. Los dos se commitean juntos.
- **Aceleradores:** el notebook detecta MPS (Apple), CUDA (NVIDIA) o CPU segun
  tu maquina. Cloud Run solo tiene CPU, y esa es la cifra que importa para
  dimensionar produccion.

## Licencia

El codigo de este repositorio es material educativo. Ojo con la dependencia:
**`ultralytics` es AGPL-3.0**. Para uso educativo o proyectos open source no hay
problema, pero un producto comercial de codigo cerrado requiere una Enterprise
License de Ultralytics, o migrar a alternativas permisivas como RF-DETR o YOLOX.
