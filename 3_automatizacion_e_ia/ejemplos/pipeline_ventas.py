"""Pipeline de ejemplo: ventas CSV → limpieza → métricas JSON."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("pipeline_ventas")


def load(path: Path) -> pd.DataFrame:
    logger.info("Cargando %s", path)
    return pd.read_csv(path)


def transform(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    work = frame.copy()
    work["unidades"] = pd.to_numeric(work["unidades"], errors="coerce")
    work["precio_unitario"] = pd.to_numeric(work["precio_unitario"], errors="coerce")
    ok = work["unidades"].notna() & (work["unidades"] > 0) & (work["precio_unitario"] > 0)
    clean = work.loc[ok].copy()
    clean["importe"] = clean["unidades"] * clean["precio_unitario"]
    report = {
        "rows_in": int(len(work)),
        "rows_out": int(len(clean)),
        "rows_dropped": int((~ok).sum()),
        "importe_total": float(clean["importe"].sum()),
    }
    logger.info("Transformación: %s", report)
    return clean, report


def save(clean: pd.DataFrame, report: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    clean_path = out_dir / "ventas_limpias.csv"
    report_path = out_dir / "metrics.json"
    clean.to_csv(clean_path, index=False)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Escrito %s y %s", clean_path, report_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline de ventas")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    frame = load(args.input)
    clean, report = transform(frame)
    save(clean, report, args.output_dir)


if __name__ == "__main__":
    main()
