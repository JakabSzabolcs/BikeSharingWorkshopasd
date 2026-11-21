"""Helyi környezetet készít, majd elindítja a Streamlit-dashboardot."""

import os
from pathlib import Path
import subprocess
import sys
import venv

PROJECT_DIR = Path(__file__).resolve().parent
ENV_DIR = PROJECT_DIR / ".venv"
REQUIREMENTS = PROJECT_DIR / "requirements.txt"

CHECK_PACKAGES = """
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys

for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    name, required = line.strip().split("==", 1)
    try:
        installed = version(name)
    except PackageNotFoundError:
        sys.exit(1)
    if installed != required:
        sys.exit(1)
"""


def main() -> int:
    python = ENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    try:
        if not python.is_file():
            print("A helyi Python-környezet létrehozása…", flush=True)
            venv.create(ENV_DIR, with_pip=True)

        check = subprocess.run(
            [str(python), "-I", "-c", CHECK_PACKAGES, str(REQUIREMENTS)],
            cwd=PROJECT_DIR,
        )
        if check.returncode:
            print("A workshop csomagjainak telepítése…", flush=True)
            subprocess.run(
                [str(python), "-I", "-m", "pip", "--disable-pip-version-check",
                 "install", "-r", str(REQUIREMENTS)],
                cwd=PROJECT_DIR,
                check=True,
            )

        command = [str(python), "-I", "-m", "streamlit", "run", "app.py"]
        print("A workshop dashboard indítása…", flush=True)
        if os.name == "posix":
            os.chdir(PROJECT_DIR)
            os.execv(python, command)
        return subprocess.call(command, cwd=PROJECT_DIR)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Az indítás sikertelen. {error}", file=sys.stderr)
        print("Válassz Python 3.12-interpretert, és ellenőrizd az internetkapcsolatot.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
