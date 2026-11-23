# Ingesta 
# El fichero raw nunca se modifica ya que es la fuente de verdad para poder reprocesar

from __future__ import annotations

import io
import logging
import zipfile
from pathlib import Path

import pandas as pd
import requests

from ..errors import DataContractError, UpstreamError

logger = logging.getLogger("bikedemand.ingest")

UCI_URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"

REQUIRED_COLUMNS = [
    "dteday", "season", "yr", "mnth", "hr", "holiday", "weekday", "workingday",
    "weathersit", "temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt",
]


def fetch_dataset(dest: Path, url: str = UCI_URL, force: bool = False, timeout: float = 30.0) -> Path:
    """Descarga el zip de UCI y extrae `hour.csv` en `dest` y el Idempotente si ya existe, no hace nada"""
    if dest.exists() and not force:
        logger.info("fetch_skip path=%s reason=already_exists", dest)
        return dest
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            content = zf.read("hour.csv")
    except (requests.RequestException, zipfile.BadZipFile, KeyError) as exc:
        raise UpstreamError(f"No se pudo descargar el dataset de UCI: {exc}") from exc
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
    logger.info("fetch_ok path=%s bytes=%d", dest, len(content))
    return dest


def load_raw(path: Path) -> pd.DataFrame:
    """Lee el CSV raw y comprueba el contrato de columnas"""
    if not path.exists():
        raise DataContractError(f"No existe el fichero de entrada: {path}")
    try:
        frame = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as exc:
        raise DataContractError(f"No se pudo leer {path}: {exc}") from exc
    missing = [c for c in REQUIRED_COLUMNS if c not in frame.columns]
    if missing:
        raise DataContractError(f"Faltan columnas requeridas: {missing}")
    logger.info("load_raw_ok path=%s rows=%d", path, len(frame))
    return frame
