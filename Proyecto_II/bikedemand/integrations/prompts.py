# Prompts para generar los informes
from __future__ import annotations

PROMPT_VERSION = "briefing-v1"

SYSTEM_BRIEFING = (
    "Eres el analista de operaciones de un sistema de bicicleta compartida. "
    "Recibes la previsión horaria de alquileres calculada por un modelo de machine learning "
    "y el tiempo previsto. Escribe en español un briefing operativo de máximo 150 palabras con "
    "tres apartados en viñetas: 1) Picos de demanda y cuándo reforzar el reequilibrado de bicis, "
    "2) Ventanas valle recomendadas para mantenimiento, 3) Avisos por meteorología o festivos. "
    "Usa solo los datos proporcionados; no inventes cifras."
)


def build_briefing_prompt(summary: dict) -> str:
    peaks = "\n".join(f"  - {p['timestamp']}: {p['pred_cnt']} alquileres/h ({p['weather']}, {p['temp_c']} °C)"
                      for p in summary["peak_hours"])
    valleys = "\n".join(f"  - {v['start']} → {v['end']} (media {v['avg_cnt']} alquileres/h)"
                        for v in summary["maintenance_windows"])
    rain = ", ".join(summary["bad_weather_hours"]) or "ninguna"
    holidays = ", ".join(summary["holidays"]) or "ninguno"
    return (
        f"Previsión de demanda para {summary['city']} ({summary['start']} → {summary['end']}, "
        f"{summary['hours']} horas).\n"
        f"Total previsto: {summary['total_pred']} alquileres. Media: {summary['avg_per_hour']} por hora.\n"
        f"Horas punta:\n{peaks}\n"
        f"Ventanas valle (mantenimiento):\n{valleys}\n"
        f"Horas con lluvia/nieve/tormenta prevista: {rain}\n"
        f"Festivos en el periodo: {holidays}\n"
    )
