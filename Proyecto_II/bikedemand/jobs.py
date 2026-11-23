"""Jobs del pipeline (orquestación). Cada job es una función sobre `Settings` que
devuelve un dict de métricas; la CLI solo traduce excepciones a exit codes.

    prepare  : raw (bronze) -> validación -> silver + cuarentena → gold           [batch, diario]
    train    : gold -> modelo sklearn (gate R²) -> models/*.joblib + model_card   [batch, bajo demanda]
    forecast : Open-Meteo + Nager.Date → features -> predicción -> briefing IA    [batch, cada hora/día]

"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable

import pandas as pd

from .config import Settings
from .errors import DataContractError, QualityGateError, UpstreamError
from .integrations import open_data_client as od
from .integrations.ai_client import AIClientError, AIConfig, AIResponse, complete_with_retries
from .integrations.prompts import PROMPT_VERSION, SYSTEM_BRIEFING, build_briefing_prompt
from .pipeline import features, ingest, model, quality

logger = logging.getLogger("bikedemand.jobs")

WEATHER_LABEL = {1: "despejado", 2: "nublado/niebla", 3: "lluvia o nieve débil", 4: "temporal"}


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")



def prepare(settings: Settings, run_id: str = "-") -> dict:
    raw = ingest.load_raw(settings.raw_path)
    result = quality.validate(raw)
    report = {"job": "prepare", "run_id": run_id, **result.report, "max_error_rate": settings.max_error_rate}

    if result.report["error_rate"] > settings.max_error_rate:
        report["status"] = "gate_failed"
        _write_json(settings.output_dir / "prepare_metrics.json", report)
        raise QualityGateError(
            f"error_rate {result.report['error_rate']:.3f} > max_error_rate {settings.max_error_rate:.3f}; "
            "no se publican silver/gold"
        )

    quality.save_layers(result, settings.silver_path, settings.quarantine_path)
    gold = features.build_training_table(result.clean)
    settings.gold_path.parent.mkdir(parents=True, exist_ok=True)
    gold.to_csv(settings.gold_path, index=False)
    report.update(status="ok", gold_rows=len(gold), gold_path=str(settings.gold_path))
    _write_json(settings.output_dir / "prepare_metrics.json", report)
    logger.info("prepare_ok run_id=%s gold_rows=%d", run_id, len(gold))
    return report


# Entrenamiento
def train(settings: Settings, run_id: str = "-", max_iter: int = 400) -> dict:
    if not settings.gold_path.exists():
        raise DataContractError(f"No existe {settings.gold_path}. Ejecuta antes: python -m bikedemand prepare")
    gold = pd.read_csv(settings.gold_path, parse_dates=["timestamp"])
    result = model.train_model(gold, settings.test_from, settings.random_state, max_iter)
    r2 = result.card["metrics_test"]["r2"]
    report = {"job": "train", "run_id": run_id, "min_r2": settings.min_r2, **result.card}

    if r2 < settings.min_r2:  # gate: un modelo peor no sustituye al de producción
        report["status"] = "gate_failed"
        _write_json(settings.output_dir / "train_metrics.json", report)
        raise QualityGateError(f"R² en test {r2:.3f} < MIN_R2 {settings.min_r2:.2f}; el modelo no se promociona")

    model.save_model(result, settings.model_path, settings.model_card_path)
    report["status"] = "ok"
    _write_json(settings.output_dir / "train_metrics.json", report)
    return report


# Prediccion
def summarize_forecast(pred: pd.DataFrame, city: str, holiday_names: list[str]) -> dict:
    """Agregados de la previsión que alimentan el briefing (función pura)."""
    df = pred.sort_values("timestamp").reset_index(drop=True)
    fmt = lambda ts: pd.Timestamp(ts).strftime("%d/%m %H:%M")  # noqa: E731
    peaks = df.nlargest(3, "pred_cnt")
    peak_hours = [{"timestamp": fmt(r.timestamp), "pred_cnt": int(r.pred_cnt),
                   "weather": WEATHER_LABEL.get(int(r.weathersit), "?"), "temp_c": round(float(r.temp_c), 1)}
                  for r in peaks.itertuples()]

    # Ventanas valle de 3 h que no se solapan
    windows, used = [], set()
    if len(df) >= 3:
        roll = df["pred_cnt"].rolling(3).mean().dropna().sort_values()
        for end_idx, avg in roll.items():
            span = set(range(end_idx - 2, end_idx + 1))
            if span & used:
                continue
            used |= span
            windows.append({"start": fmt(df.loc[end_idx - 2, "timestamp"]),
                            "end": fmt(df.loc[end_idx, "timestamp"] + pd.Timedelta(hours=1)),
                            "avg_cnt": round(float(avg), 1)})
            if len(windows) == 2:
                break

    return {
        "city": city,
        "start": fmt(df["timestamp"].iloc[0]),
        "end": fmt(df["timestamp"].iloc[-1]),
        "hours": int(len(df)),
        "total_pred": int(df["pred_cnt"].sum()),
        "avg_per_hour": round(float(df["pred_cnt"].mean()), 1),
        "peak_hours": peak_hours,
        "maintenance_windows": windows,
        "bad_weather_hours": [fmt(t) for t in df.loc[df["weathersit"] >= 3, "timestamp"]],
        "holidays": holiday_names,
    }


def rules_briefing(summary: dict) -> str:
    """Resumen determinista sin IA: siempre aparece en el informe y garantiza un resultado
    útil aunque el proveedor de IA falle"""
    p = summary["peak_hours"][0] if summary["peak_hours"] else None
    lines = [f"- Pico principal: {p['timestamp']} con ~{p['pred_cnt']} alquileres/h; "
             "reequilibrar estaciones céntricas 1 h antes." if p else "- Sin picos destacables."]
    for w in summary["maintenance_windows"]:
        lines.append(f"- Ventana de mantenimiento: {w['start']} → {w['end']} (~{w['avg_cnt']}/h).")
    if summary["bad_weather_hours"]:
        lines.append(f"- Precipitación prevista en {len(summary['bad_weather_hours'])} h "
                     f"(desde {summary['bad_weather_hours'][0]}): esperar menos demanda.")
    if summary["holidays"]:
        lines.append(f"- Festivo en el periodo: {', '.join(summary['holidays'])} (patrón de fin de semana).")
    return "\n".join(lines)


def _render_report(summary: dict, ai: AIResponse | None, briefing: str, statuses: dict) -> str:
    peaks = "\n".join(f"| {p['timestamp']} | {p['pred_cnt']} | {p['weather']} | {p['temp_c']} |"
                      for p in summary["peak_hours"])
    source = (f"_Generado por `{ai.provider}` · modelo `{ai.model}` · {ai.latency_ms} ms · prompt {PROMPT_VERSION}_"
              if ai else "_Proveedor de IA no disponible: se muestra solo el resumen por reglas (modo degradado)._")
    return (
        f"# Previsión de demanda — {summary['city']}\n\n"
        f"Periodo: **{summary['start']} → {summary['end']}** ({summary['hours']} h) · "
        f"Total previsto: **{summary['total_pred']}** alquileres · media **{summary['avg_per_hour']}**/h\n\n"
        f"## Horas punta\n\n| Hora | Alquileres previstos | Tiempo | °C |\n|---|---|---|---|\n{peaks}\n\n"
        f"## Resumen por reglas (determinista)\n\n{rules_briefing(summary)}\n\n"
        f"## Briefing operativo (IA)\n\n{briefing}\n\n{source}\n\n"
        f"## Estado de las dependencias\n\n" + "\n".join(f"- {k}: `{v}`" for k, v in statuses.items()) + "\n"
    )


def forecast(settings: Settings, run_id: str = "-",
             weather_fn: Callable | None = None, holidays_fn: Callable | None = None,
             ai_fn: Callable | None = None) -> dict:
    weather_fn = weather_fn or od.hourly_weather_forecast
    holidays_fn = holidays_fn or od.public_holidays
    ai_fn = ai_fn or complete_with_retries
    bundle = model.load_model(settings.model_path)
    statuses = {"weather": "ok", "holidays": "ok", "ai": "ok"}

    try:
        weather = weather_fn(settings.latitude, settings.longitude, settings.horizon_hours,
                             settings.timezone, timeout=settings.open_data_timeout)
    except od.OpenAPIError as exc:  # sin tiempo previsto no hay previsión: fallo de dependencia
        raise UpstreamError(f"Open-Meteo no disponible: {exc}") from exc
    wdf = pd.DataFrame(weather.data)

    years = sorted({pd.Timestamp(t).year for t in wdf["time"]})
    holidays: dict = {}  # fecha -> nombre
    try:
        for y in years:
            res = holidays_fn(settings.country_code, y, settings.subdivision, timeout=settings.open_data_timeout)
            holidays.update({date.fromisoformat(h["date"]): h["name"] for h in res.data["holidays"]})
    except od.OpenAPIError as exc:  # degradación: seguimos asumiendo que no hay festivos
        statuses["holidays"] = "degraded"
        holidays = {}
        logger.warning("holidays_degraded run_id=%s cause=%s", run_id, exc)

    feats = features.build_forecast_features(wdf, set(holidays))
    feats["pred_cnt"] = model.predict(bundle, feats)
    period_days = set(feats["timestamp"].dt.date)
    names_in_period = [f"{n} ({d:%d/%m})" for d, n in sorted(holidays.items()) if d in period_days]
    summary = summarize_forecast(feats, settings.city_name, names_in_period)

    ai_cfg = AIConfig(hf_token=settings.hf_token, hf_model=settings.hf_model,
                      nvidia_api_key=settings.nvidia_api_key, nvidia_model=settings.nvidia_model,
                      nvidia_base_url=settings.nvidia_base_url, timeout=settings.ai_timeout,
                      max_tokens=settings.ai_max_tokens)
    ai: AIResponse | None = None
    try:
        ai = ai_fn(settings.ai_provider, build_briefing_prompt(summary), system=SYSTEM_BRIEFING,
                   config=ai_cfg, attempts=settings.ai_max_attempts)
        briefing = ai.text
    except AIClientError as exc:
        statuses["ai"] = "degraded"
        briefing = "_No disponible en esta ejecución._"
        logger.error("briefing_degraded run_id=%s provider=%s cause=%s", run_id, settings.ai_provider, exc)

    out = settings.output_dir
    out.mkdir(parents=True, exist_ok=True)
    cols = ["timestamp", "pred_cnt", "weathersit", "temp_c", "feels_like_c", "humidity_pct",
            "wind_kmh", "holiday", "workingday"]
    feats[cols].round({c: 1 for c in cols[2:]}).to_csv(out / "forecast.csv", index=False)
    (out / "briefing.md").write_text(_render_report(summary, ai, briefing, statuses), encoding="utf-8")

    report = {
        "job": "forecast", "run_id": run_id, "status": "ok" if all(v == "ok" for v in statuses.values()) else "degraded",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "city": settings.city_name, "hours": summary["hours"], "total_pred": summary["total_pred"],
        "peak": summary["peak_hours"][0] if summary["peak_hours"] else None,
        "dependencies": statuses, "ai": asdict(ai) | {"text": None} if ai else None,
        "model_trained_at": bundle.get("trained_at"), "prompt_version": PROMPT_VERSION,
    }
    _write_json(out / "forecast_metrics.json", report)
    logger.info("forecast_ok run_id=%s hours=%d total=%d status=%s",
                run_id, summary["hours"], summary["total_pred"], report["status"])
    return report
