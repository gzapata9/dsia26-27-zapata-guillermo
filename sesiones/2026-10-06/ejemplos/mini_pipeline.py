"""Mini pipeline didáctico — sesión 6 oct 2026."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd

REQUIRED = {"fecha", "region", "producto", "unidades", "precio_unitario", "cliente_id"}


def get_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("mini_pipeline")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(levelname)s | %(message)s")
    for handler in (logging.StreamHandler(), logging.FileHandler(log_path, encoding="utf-8")):
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger


def transform(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
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
        "error_rate": float((~ok).sum() / len(work)) if len(work) else 0.0,
        "importe_total": float(clean["importe"].sum()) if len(clean) else 0.0,
    }
    return clean, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-error-rate", type=float, default=0.5)
    args = parser.parse_args(argv)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    logger = get_logger(args.output_dir / "run.log")
    if not args.input.exists():
        logger.error("input not found")
        return 2
    try:
        clean, report = transform(pd.read_csv(args.input))
    except ValueError as exc:
        logger.error("%s", exc)
        return 2

    logger.info("report=%s", report)
    if report["error_rate"] > args.max_error_rate:
        logger.error("quality gate failed")
        return 1

    clean.to_csv(args.output_dir / "ventas_limpias.csv", index=False)
    (args.output_dir / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
