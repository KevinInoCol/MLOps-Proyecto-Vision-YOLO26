# Proyecto Vision — YOLO26 (demo local)

Contraparte local de `../Proyecto-Vision-YOLO26-Deploy/`.
Misma relacion que `Proyecto-Vision` tiene con `Proyecto-Vision-Deploy`.

## Las cuatro carpetas del modulo

| Carpeta | Modelo | Rol en la clase |
|---|---|---|
| `Proyecto-Vision` | YOLOv3 | Demo local (version original del curso) |
| `Proyecto-Vision-Deploy` | YOLOv3 | Despliegue a Cloud Run |
| `Proyecto-Vision-YOLO26` | YOLO26 | Demo local (esta carpeta) |
| `Proyecto-Vision-YOLO26-Deploy` | YOLO26 | Despliegue a Cloud Run |

## Como correr la demo

Un solo comando crea el entorno con la version exacta de Python y de cada
dependencia, identicas para todos:

```bash
uv sync
```

Lee `pyproject.toml` + `uv.lock`, crea `.venv` con Python 3.12 e instala todo.
No hace falta `uv venv` ni `activate` por separado.

```bash
# Opcion A: el notebook (recomendado para clase)
uv run jupyter notebook server.ipynb

# Opcion B: la API suelta
uv run uvicorn main:app --reload --port 8080
# luego abrir http://localhost:8080/docs
```

`uv run` usa el `.venv` del proyecto sin necesidad de activarlo. Si prefieres
activarlo a mano para mostrarlo en clase: `source .venv/bin/activate`.

## Los archivos de entorno

| Archivo | Que hace |
|---|---|
| `pyproject.toml` | Lo que pedimos: dependencias directas y `requires-python` |
| `uv.lock` | Lo que se instala: 135 paquetes con version exacta y hash |
| `.python-version` | Fija 3.12, para que `uv venv` sin flags acierte |

Los tres se commitean. `uv.lock` no se edita a mano — se regenera con `uv lock`.

## Recorrido del notebook

1. Mostrar las imagenes de ejemplo
2. Cargar YOLO26 y ver el tamano real en disco (5 MB vs 237 MB de YOLOv3)
3. `detect_and_draw_box()` — misma firma que la version cvlib, para comparar
4. Efecto del umbral de confianza
5. **Bonus:** MPS, la GPU del chip M (YOLOv3 sobre OpenCV solo hacia CPU)
6. Tabla comparativa YOLOv3 vs YOLO26, incluida la licencia
7. Envolver en FastAPI y levantar el server con `nest_asyncio`
8. Cierre: que cambia al pasar a Cloud Run

## Nota sobre `programa-api.py`

No hay version YOLO26 de ese archivo a proposito: es la introduccion a FastAPI
(GET/POST, path params) y no depende del modelo. Se sigue usando el de
`Proyecto-Vision`.
