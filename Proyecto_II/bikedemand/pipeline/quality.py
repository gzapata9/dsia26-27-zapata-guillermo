# Validación y calidad
# `validate` es una función pura: no escribe ficheros. Devuelve las filas limpias,
# las rechazadas con el motivo y un informe con `error_rate` para el gate.

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

logger = logging.getLogger("bikedemand.quality")

# (columna, mínimo, máximo) — rangos del diccionario de datos de UCI
RANGE_RULES = [
    ("season", 1, 4), ("yr", 0, 1), ("mnth", 1, 12), ("hr", 0, 23), ("holiday", 0, 1),
    ("weekday", 0, 6), ("workingday", 0, 1), ("weathersit", 1, 4),
    ("temp", 0, 1), ("atemp", 0, 1), ("hum", 0, 1), ("windspeed", 0, 1),
    ("casual", 0, None), ("registered", 0, None), ("cnt", 0, None),
]


@dataclass
class QualityResult:
    clean: pd.DataFrame
    rejected: pd.DataFrame
    report: dict


def validate(frame: pd.DataFrame) -> QualityResult:
    work = frame.copy()
    reasons = pd.Series("", index=work.index, dtype=object)

    def flag(mask: pd.Series, reason: str) -> None:
        mask = mask.fillna(True)
        reasons[mask & (reasons == "")] = reason

    work["dteday"] = pd.to_datetime(work["dteday"], errors="coerce")
    flag(work["dteday"].isna(), "fecha_invalida")

    for col, lo, hi in RANGE_RULES:
        values = pd.to_numeric(work[col], errors="coerce")
        bad = values.isna() | (values < lo)
        if hi is not None:
            bad |= values > hi
        flag(bad, f"{col}_fuera_de_rango")
        work[col] = values

    total = work["casual"] + work["registered"]
    flag(work["cnt"] != total, "cnt_distinto_de_casual_mas_registered")
    flag(work.duplicated(subset=["dteday", "hr"], keep="first"), "duplicado_fecha_hora")

    rejected_mask = reasons != ""
    clean = work.loc[~rejected_mask].copy()
    int_cols = [c for c, _, _ in RANGE_RULES if c not in ("temp", "atemp", "hum", "windspeed")]
    clean[int_cols] = clean[int_cols].astype(int)
    rejected = frame.loc[rejected_mask].copy()
    rejected["reject_reason"] = reasons[rejected_mask]

    rows_in = len(frame)
    report = {
        "rows_in": rows_in,
        "rows_out": len(clean),
        "rows_rejected": int(rejected_mask.sum()),
        "error_rate": round(float(rejected_mask.sum()) / rows_in, 4) if rows_in else 0.0,
        "reject_reasons": rejected["reject_reason"].value_counts().to_dict(),
        "date_min": str(clean["dteday"].min().date()) if len(clean) else None,
        "date_max": str(clean["dteday"].max().date()) if len(clean) else None,
    }
    logger.info("quality_done rows_in=%d rows_out=%d rejected=%d error_rate=%.4f",
                rows_in, report["rows_out"], report["rows_rejected"], report["error_rate"])
    return QualityResult(clean=clean, rejected=rejected, report=report)


def save_layers(result: QualityResult, silver_path: Path, quarantine_path: Path) -> None:
    """Sobrescribe siempre idempotente"""
    silver_path.parent.mkdir(parents=True, exist_ok=True)
    quarantine_path.parent.mkdir(parents=True, exist_ok=True)
    out = result.clean.copy()
    out["dteday"] = out["dteday"].dt.strftime("%Y-%m-%d")
    out.to_csv(silver_path, index=False)
    result.rejected.to_csv(quarantine_path, index=False)
    logger.info("layers_saved silver=%s quarantine=%s", silver_path, quarantine_path)
