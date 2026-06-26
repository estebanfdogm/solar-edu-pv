"""Lanzador de escritorio para SolarEdu PV.

En desarrollo inicia Streamlit con el intérprete activo. Dentro del ejecutable
usa la CLI incluida por PyInstaller, porque un .exe congelado no puede actuar
como intérprete para ejecutar ``-m streamlit``.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

from streamlit.web import cli as streamlit_cli


PORT = 8501
URL = f"http://localhost:{PORT}"
SERVER_WAIT_SECONDS = 30


def project_root() -> Path:
    """Encuentra los archivos de la app en desarrollo y en PyInstaller."""
    if getattr(sys, "frozen", False):
        # PyInstaller define _MEIPASS tanto en --onedir como en --onefile.
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parent


def streamlit_arguments(base_dir: Path) -> list[str]:
    """Construye los argumentos comunes para el servidor local de Streamlit."""
    return [
        "run",
        str(base_dir / "app.py"),
        "--server.port",
        str(PORT),
        "--server.headless",
        "true",
        "--global.developmentMode",
        "false",
        "--browser.gatherUsageStats",
        "false",
    ]


def open_browser_when_ready() -> None:
    """Espera una respuesta HTTP antes de abrir la aplicación en el navegador."""
    deadline = time.monotonic() + SERVER_WAIT_SECONDS
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(URL, timeout=1):
                webbrowser.open(URL, new=2)
                return
        except (OSError, urllib.error.URLError):
            time.sleep(0.4)

    print(f"No fue posible abrir el navegador automáticamente. Visite {URL}.", flush=True)


def prepare_runtime(base_dir: Path) -> None:
    """Asegura que app.py encuentre sus módulos y recursos empaquetados."""
    os.chdir(base_dir)
    if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))


def run_development(arguments: list[str]) -> int:
    """Inicia Streamlit como un subproceso cuando se ejecuta launcher.py."""
    process = subprocess.Popen([sys.executable, "-m", "streamlit", *arguments])
    try:
        return process.wait()
    except KeyboardInterrupt:
        process.terminate()
        return process.wait()


def run_packaged(arguments: list[str]) -> int:
    """Inicia la CLI de Streamlit incluida dentro de SolarEduPV.exe."""
    original_argv = sys.argv[:]
    sys.argv = [sys.executable, *arguments]
    try:
        streamlit_cli.main()
    finally:
        sys.argv = original_argv
    return 0


def main() -> int:
    """Prepara el entorno, muestra instrucciones e inicia el servidor local."""
    base_dir = project_root()
    app_file = base_dir / "app.py"
    if not app_file.is_file():
        print(f"No se encontró app.py en: {base_dir}", flush=True)
        return 1

    prepare_runtime(base_dir)
    print("Iniciando SolarEdu PV...", flush=True)
    print("Abriendo navegador...", flush=True)
    print("Para cerrar la aplicación, cierre esta ventana.", flush=True)

    threading.Thread(target=open_browser_when_ready, daemon=True).start()
    arguments = streamlit_arguments(base_dir)
    if getattr(sys, "frozen", False):
        return run_packaged(arguments)
    return run_development(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
