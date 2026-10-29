---
name: gcp-install-cli
description: Instala la CLI de Google Cloud (gcloud, Google Cloud SDK) detectando automáticamente el sistema operativo — macOS (Intel o Apple Silicon), Linux (Debian/Ubuntu, Fedora/RHEL u otra distro), WSL o Windows — y la deja lista para usar con gcloud init, gcloud auth login y Application Default Credentials. Úsala cuando el usuario pida instalar gcloud, la CLI de GCP, el SDK de Google Cloud, cuando un comando falle con "gcloud: command not found" / "gcloud no se reconoce", o cuando mencione "instalar gcloud", "no tengo gcloud", "configurar GCP en mi máquina", "/gcp-install-cli".
---

Instala la **Google Cloud CLI** (`gcloud`, `gsutil`, `bq`) en la máquina del usuario y déjala autenticada. Sigue los pasos **en orden** y no los saltes.

> Reglas generales
> - Explica cada paso en español y en lenguaje simple: quien usa esta skill es un alumno.
> - Los comandos **interactivos** (abren el navegador o hacen preguntas: `gcloud init`, `gcloud auth login`, `gcloud auth application-default login`, el instalador `.exe` de Windows) **no los ejecutes tú**: pídele al alumno que los escriba con el prefijo `!` en el prompt (ej. `! gcloud auth login`) o en su propia terminal.
> - Si un comando necesita `sudo` y falla por contraseña, pídele al alumno que lo ejecute con `!`.

## Paso 1 — ¿Ya está instalada?

```bash
gcloud --version
```

- **Si responde con una versión** (ej. `Google Cloud SDK 5xx.0.0`): ya está instalada. Muestra la versión y la ruta (`which gcloud`, o `where gcloud` en Windows CMD). Ofrece actualizar con `gcloud components update` (si se instaló con brew/apt/dnf, se actualiza con ese gestor). **Salta al Paso 5.**
- **Si dice `command not found` / `no se reconoce`**: continúa al Paso 2.

## Paso 2 — Detectar el sistema operativo y la arquitectura

```bash
uname -s; uname -m
```

| `uname -s` | Sistema | Sección del Paso 3 |
|---|---|---|
| `Darwin` | macOS | 3A |
| `Linux` (y `/proc/version` contiene `microsoft`) | WSL | 3B (se instala como Linux) |
| `Linux` | Linux | 3B |
| `MINGW*`, `MSYS*`, `CYGWIN*` | Windows (Git Bash) | 3C |
| el comando falla | Windows (PowerShell/CMD) | 3C |

| `uname -m` | Arquitectura | Sufijo del archivo |
|---|---|---|
| `arm64` (Mac M1/M2/M3/M4) | ARM | `darwin-arm` |
| `x86_64` en Mac | Intel | `darwin-x86_64` |
| `x86_64` en Linux | Intel/AMD | `linux-x86_64` |
| `aarch64` en Linux | ARM | `linux-arm` |

En Linux, identifica la distribución:

```bash
cat /etc/os-release | grep -E '^(ID|ID_LIKE)='
```

## Paso 3 — Instalar

### 3A — macOS

**Opción 1 (recomendada si el alumno tiene Homebrew):** comprueba con `brew --version`.

```bash
brew install --cask gcloud-cli
```

> Si brew dice que no encuentra `gcloud-cli`, prueba con el nombre antiguo: `brew install --cask google-cloud-sdk`.

**Opción 2 (sin Homebrew): instalador oficial.** Usa el sufijo de arquitectura del Paso 2 (`darwin-arm` o `darwin-x86_64`):

```bash
cd ~
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz
tar -xf google-cloud-cli-darwin-arm.tar.gz
./google-cloud-sdk/install.sh --quiet --path-update true --command-completion true --usage-reporting false
rm google-cloud-cli-darwin-arm.tar.gz
```

El instalador agrega `gcloud` al PATH editando `~/.zshrc` (o `~/.bash_profile`). Si pregunta por instalar Python, acepta: trae su propio Python y no interfiere con el de uv ni con el del sistema.

### 3B — Linux y WSL

**Debian / Ubuntu / WSL con Ubuntu (`ID=ubuntu` o `ID_LIKE` contiene `debian`):** repositorio oficial con apt.

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates gnupg curl
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install -y google-cloud-cli
```

**Fedora / RHEL / Rocky / Alma (`ID_LIKE` contiene `rhel` o `fedora`):** repositorio oficial con dnf. Cambia `x86_64` por `aarch64` si la arquitectura es ARM.

```bash
sudo tee /etc/yum.repos.d/google-cloud-sdk.repo << 'EOM'
[google-cloud-cli]
name=Google Cloud CLI
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el9-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOM
sudo dnf install -y google-cloud-cli
```

**Cualquier otra distro, o si el alumno no tiene `sudo`:** instalador oficial en su carpeta de usuario (usa `linux-x86_64` o `linux-arm` según el Paso 2):

```bash
cd ~
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh --quiet --path-update true --command-completion true --usage-reporting false
rm google-cloud-cli-linux-x86_64.tar.gz
```

> En WSL instala gcloud **dentro de Linux** (no uses el gcloud de Windows desde WSL). Para `gcloud auth login`, si no se abre el navegador, usa `gcloud auth login --no-launch-browser` y copia el enlace en el navegador de Windows.

### 3C — Windows

**Opción 1 (recomendada): winget**, viene incluido en Windows 10/11. Funciona desde PowerShell o Git Bash:

```bash
winget install --id Google.CloudSDK -e --accept-source-agreements --accept-package-agreements
```

**Opción 2: instalador oficial (.exe).** Pídele al alumno que lo ejecute en **PowerShell** (abre un asistente gráfico; deja marcadas las opciones por defecto, incluida "Bundled Python"):

```powershell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

O que lo descargue desde el navegador: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe

## Paso 4 — Verificar la instalación

La terminal actual **todavía no ve el PATH nuevo**. Verifica con la ruta completa según cómo se instaló:

| Instalación | Comando de verificación |
|---|---|
| Instalador oficial (macOS/Linux) | `~/google-cloud-sdk/bin/gcloud --version` |
| Homebrew (Apple Silicon) | `/opt/homebrew/bin/gcloud --version` |
| Homebrew (Intel) | `/usr/local/bin/gcloud --version` |
| apt / dnf | `gcloud --version` (ya queda en `/usr/bin`) |
| Windows | `"$LOCALAPPDATA/Google/Cloud SDK/google-cloud-sdk/bin/gcloud" --version` o, si se instaló para todos los usuarios, `"/c/Program Files (x86)/Google/Cloud SDK/google-cloud-sdk/bin/gcloud" --version` |

Si responde con una versión, la instalación fue exitosa. Explícale al alumno que para poder escribir solo `gcloud` debe:

- **macOS / Linux:** cerrar y volver a abrir la terminal, **o** ejecutar `source ~/.zshrc` (zsh) / `source ~/.bashrc` (bash).
- **Windows:** cerrar y volver a abrir la terminal (PowerShell, CMD o Git Bash). Si usa VS Code, cerrar VS Code completo.

Después de reabrir la terminal, que confirme:

```bash
gcloud --version
```

## Paso 5 — Iniciar sesión y elegir proyecto

Estos comandos abren el navegador. Pídele al alumno que los ejecute él (con `!` o en su terminal), uno por uno:

1. **Login de la CLI** (para usar `gcloud`, `gsutil`, `bq`):
   ```bash
   gcloud auth login
   ```
2. **Credenciales para el código** (Application Default Credentials: las usan las librerías de Python como `google-cloud-storage`, `vertexai`, etc.):
   ```bash
   gcloud auth application-default login
   ```
3. **Proyecto por defecto.** Lista los proyectos y fija el de la clase:
   ```bash
   gcloud projects list
   gcloud config set project <PROJECT_ID>
   gcloud auth application-default set-quota-project <PROJECT_ID>
   ```
   Si el alumno aún no tiene proyecto, que lo cree en https://console.cloud.google.com/projectcreate (o con `gcloud projects create <PROJECT_ID>`) y que vincule una cuenta de facturación en https://console.cloud.google.com/billing.
4. **Región por defecto (opcional, recomendado):**
   ```bash
   gcloud config set run/region us-central1
   gcloud config set compute/region us-central1
   ```

> Alternativa todo-en-uno: `gcloud init` hace login + proyecto + región en un asistente interactivo. Igual hace falta el `application-default login` aparte.

## Paso 6 — Comprobación final

Ejecuta tú estos comandos (no son interactivos) y muéstrale el resultado al alumno:

```bash
gcloud --version
gcloud auth list
gcloud config list
```

Debe verse: la versión, la cuenta con un `*` (cuenta activa) y `project = <PROJECT_ID>`. Si todo está, dile que gcloud quedó listo.

## Solución de problemas

| Síntoma | Causa | Solución |
|---|---|---|
| `gcloud: command not found` justo después de instalar | La terminal no recargó el PATH | Cerrar y abrir la terminal (Paso 4) |
| `zsh: command not found` aunque `~/google-cloud-sdk/bin/gcloud` funciona | `install.sh` editó otro archivo rc | `echo 'source ~/google-cloud-sdk/path.zsh.inc' >> ~/.zshrc && source ~/.zshrc` (en bash: `path.bash.inc` en `~/.bashrc`) |
| En Windows: `"gcloud" no se reconoce...` tras reabrir | Instalación sin agregar al PATH | Reinstalar con el `.exe` dejando marcada la opción de PATH, o agregar `...\google-cloud-sdk\bin` a las variables de entorno |
| PowerShell: `la ejecución de scripts está deshabilitada` | Política de ejecución | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `gcloud auth login` no abre el navegador (WSL, SSH, contenedor) | No hay navegador en esa terminal | `gcloud auth login --no-launch-browser` y pegar el código |
| `ERROR: (gcloud.components.update) You cannot perform this action because the Google Cloud CLI component manager is disabled` | Se instaló con apt/dnf | Actualizar con `sudo apt-get install --only-upgrade google-cloud-cli` / `sudo dnf upgrade google-cloud-cli` |
| `Your default credentials were not found` al correr código Python | Falta ADC | `gcloud auth application-default login` (Paso 5.2) |
| `Billing account ... is not found` / `billing not enabled` | El proyecto no tiene facturación | Vincular facturación en la consola |

## Notas

- **No uses `pip install gcloud`** ni `pip install google-cloud-sdk`: esos paquetes no son la CLI oficial.
- **No hace falta instalar Python antes:** los instaladores de macOS y Windows traen su propio Python, y los paquetes de apt/dnf también lo resuelven.
- `gsutil` y `bq` vienen incluidos. Para componentes extra (ej. `kubectl`): `gcloud components install kubectl` (o `sudo apt-get install kubectl` si se instaló con apt).
- La CLI se instala **una sola vez por computadora**, no por proyecto.
