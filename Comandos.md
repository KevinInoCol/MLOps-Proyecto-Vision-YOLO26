# ================================= Instalamos UV ================================
# Paso 1: Instalamos UV en Mac:
brew install uv

# Paso 1: Instalamos UV en Linux / Mac sin brew:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Paso 1: Instalamos UV en Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# =========================== Clonamos el Repositorio ============================
# Paso 2: Clonamos el repositorio
git clone https://github.com/KevinInoCol/MLOps-Proyecto-Vision-YOLO26.git

# Paso 3: Entramos a la carpeta del proyecto  <-- IMPORTANTE
# El repositorio tiene DOS carpetas y cada una tiene su propio pyproject.toml.
# La raiz no tiene ninguno, asi que si te quedas ahi "uv sync" falla con:
#     error: No `pyproject.toml` found in current directory or any parent directory
cd MLOps-Proyecto-Vision-YOLO26/Proyecto-Vision-YOLO26

# ============================== Entorno Virtual =================================
# Paso 4: Creamos el Entorno Virtual
uv venv --python 3.12

# Paso 5: Activamos el Entorno Virtual
source .venv/bin/activate       # Mac / Linux
.venv\Scripts\activate          # Windows

# Paso 6: Instalamos las dependencias en el Entorno Virtual
uv sync

# Paso 7: Ejecutamos el Jupyter
uv run jupyter notebook server.ipynb


# ==================================== NOTAS =====================================
#
# NOTA 1 — Los pasos 4 y 5 son opcionales.
#   "uv sync" ya crea el entorno con la version correcta: la lee de
#   requires-python (pyproject.toml) y de .python-version. Y "uv run" usa ese
#   entorno sin necesidad de activarlo. Con 3 comandos alcanza:
#
#       git clone https://github.com/KevinInoCol/MLOps-Proyecto-Vision-YOLO26.git
#       cd MLOps-Proyecto-Vision-YOLO26/Proyecto-Vision-YOLO26
#       uv sync
#       uv run jupyter notebook server.ipynb
#
# NOTA 2 — Si usas VS Code, abre la carpeta "Proyecto-Vision-YOLO26",
#   NO la raiz del repositorio.
#   VS Code solo detecta el .venv en la raiz del workspace. Si abres la raiz del
#   repo, el entorno queda una carpeta mas abajo y no aparece en "Select Kernel".
#   (Con conda no pasaba: sus entornos son globales; los de uv viven en el proyecto.)
#
# NOTA 3 — La primera vez tarda.
#   "uv sync" descarga PyTorch (~250 MB) y el notebook descarga yolo26n.pt
#   (~5 MB) al cargar el modelo. Despues queda en cache.
#
# NOTA 4 — Para la carpeta de despliegue, el flujo es el mismo cambiando el cd:
#       cd MLOps-Proyecto-Vision-YOLO26/Proyecto-Vision-YOLO26-Deploy
#       uv sync
#       uv run uvicorn application.main:app --reload --port 8080
