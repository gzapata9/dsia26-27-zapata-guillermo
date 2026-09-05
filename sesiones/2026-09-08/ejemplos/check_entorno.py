"""Comprueba que el entorno del curso está activo y usable."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    print("Python:", sys.version.split()[0])
    print("Executable:", sys.executable)

    if ".venv" not in sys.executable.replace("\\", "/"):
        print("AVISO: parece que no estás usando .venv (continúo igual).")

    try:
        import pandas as pd
        import pytest
    except ImportError as exc:
        print("FALLO: falta dependencia —", exc)
        print("Ejecuta: pip install -r requirements.txt")
        return 1

    root = Path(__file__).resolve().parents[3]
    req = root / "requirements.txt"
    if not req.exists():
        print("FALLO: no encuentro requirements.txt en", root)
        return 1

    print(f"pandas={pd.__version__} | pytest={pytest.__version__}")
    print("ENTORNO OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
