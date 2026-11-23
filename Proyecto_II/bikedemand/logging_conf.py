# Logging: consola + fichero `run.log`, formato `clave=valor` para poder hacer grep

from __future__ import annotations

import logging
import sys
import uuid
from pathlib import Path

FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def setup_logging(level: str = "INFO", log_file: Path | None = None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(level=level, format=FORMAT, handlers=handlers, force=True)


def new_run_id() -> str:
    """Identificador corto para unir todas las líneas de log de una ejecución."""
    return uuid.uuid4().hex[:8]
