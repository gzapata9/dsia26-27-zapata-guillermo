"""CLI del pipeline.

    python -m bikedemand fetch                      
    python -m bikedemand prepare [--max-error-rate 0.05]
    python -m bikedemand train   [--min-r2 0.80]
    python -m bikedemand forecast [--provider mock|hf|nvidia] [--hours 48]
    python -m bikedemand run-all                     # prepare → train → forecast

Exit codes: 0 OK, 1 gate de calidad, 2 entrada/config inválida, 3 dependencia externa caída
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from . import jobs
from .config import PROJECT_ROOT, Settings
from .errors import BikeDemandError
from .logging_conf import new_run_id, setup_logging
from .pipeline import ingest

logger = logging.getLogger("bikedemand.cli")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bikedemand", description="Previsión de demanda de bicicleta compartida")
    p.add_argument("--env-file", default=str(PROJECT_ROOT / ".env"))
    p.add_argument("--output-dir", type=Path, help="Carpeta de métricas, informe y run.log")
    p.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    sub = p.add_subparsers(dest="command", required=True)

    f = sub.add_parser("fetch", help="Descargar el dataset UCI a data/raw")
    f.add_argument("--force", action="store_true")

    pr = sub.add_parser("prepare", help="raw → validación → silver/cuarentena → gold")
    pr.add_argument("--input", type=Path, dest="raw_path")
    pr.add_argument("--max-error-rate", type=float)

    t = sub.add_parser("train", help="Entrenar y evaluar el modelo sklearn")
    t.add_argument("--min-r2", type=float)
    t.add_argument("--test-from", help="Fecha de corte del split temporal (YYYY-MM-DD)")

    fc = sub.add_parser("forecast", help="Previsión de las próximas horas + briefing IA")
    fc.add_argument("--provider", dest="ai_provider", choices=["mock", "hf", "nvidia"])
    fc.add_argument("--hours", type=int, dest="horizon_hours")

    sub.add_parser("run-all", help="prepare → train → forecast")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    overrides = {k: v for k, v in vars(args).items()
                 if k in {"output_dir", "log_level", "raw_path", "max_error_rate", "min_r2",
                          "test_from", "ai_provider", "horizon_hours"}}
    try:
        settings = Settings.from_env(args.env_file).with_overrides(**overrides)
    except BikeDemandError as exc:
        print(f"ERROR de configuración: {exc}", file=sys.stderr)
        return 2

    setup_logging(settings.log_level, settings.output_dir / "run.log")
    run_id = new_run_id()
    logger.info("job_start run_id=%s command=%s provider=%s", run_id, args.command, settings.ai_provider)
    try:
        if args.command == "fetch":
            ingest.fetch_dataset(settings.raw_path, force=args.force)
            return 0
        if args.command in ("prepare", "run-all"):
            rep = jobs.prepare(settings, run_id)
            print(f"prepare OK · {rep['rows_out']}/{rep['rows_in']} filas válidas · error_rate={rep['error_rate']}")
        if args.command in ("train", "run-all"):
            rep = jobs.train(settings, run_id)
            m, b = rep["metrics_test"], rep["metrics_baseline"]
            print(f"train OK · MAE={m['mae']} RMSE={m['rmse']} R²={m['r2']} (baseline R²={b['r2']})")
        if args.command in ("forecast", "run-all"):
            rep = jobs.forecast(settings, run_id)
            print(f"forecast {rep['status'].upper()} · {rep['hours']} h · total={rep['total_pred']} · "
                  f"informe: {settings.output_dir / 'briefing.md'}")
            print(json.dumps(rep["dependencies"], ensure_ascii=False))
        logger.info("job_end run_id=%s status=ok", run_id)
        return 0
    except BikeDemandError as exc:
        logger.error("job_failed run_id=%s type=%s exit=%d cause=%s",
                     run_id, type(exc).__name__, exc.exit_code, exc)
        return exc.exit_code
    except Exception:  # bug propio: traza completa solo en el log
        logger.exception("job_bug run_id=%s", run_id)
        return 1
