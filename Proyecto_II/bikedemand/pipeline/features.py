# Transformaciones y construcción de features para inferencia.

from __future__ import annotations

from datetime import date

import pandas as pd

FEATURES = [
    "system_year",
    "season", "mnth", "hr", "holiday", "weekday", "workingday", "weathersit",
    "temp_c", "feels_like_c", "humidity_pct", "wind_kmh",
]
TARGET = "cnt"

# Factores de des-normalización
TEMP_MAX_C, ATEMP_MAX_C, HUM_MAX, WIND_MAX_KMH = 41.0, 50.0, 100.0, 67.0

# Códigos WMO de Open-Meteo
# 1 despejado / poco nuboso, 2 nublado o niebla, 3 lluvia o nieve débil, tormenta, 4 intensa
_WMO_TO_WEATHERSIT = {
    **dict.fromkeys([0, 1, 2], 1),
    **dict.fromkeys([3, 45, 48], 2),
    **dict.fromkeys([51, 53, 55, 56, 57, 61, 63, 66, 71, 73, 77, 80, 81, 85, 95], 3),
    **dict.fromkeys([65, 67, 75, 82, 86, 96, 99], 4),
}


def wmo_to_weathersit(code: int) -> int:
    return _WMO_TO_WEATHERSIT.get(int(code), 2)


def season_from_date(d: date) -> int:
    """Estación astronómica tal como la codifica UCI: 1 invierno, 2 primavera, 3 verano, 4 otoño."""
    md = (d.month, d.day)
    if md >= (12, 21) or md < (3, 21):
        return 1
    if md < (6, 21):
        return 2
    if md < (9, 23):
        return 3
    return 4


def build_training_table(clean: pd.DataFrame) -> pd.DataFrame:
    """UCI limpio, features en unidades físicas y objetivo"""
    gold = pd.DataFrame({
        "timestamp": pd.to_datetime(clean["dteday"]) + pd.to_timedelta(clean["hr"], unit="h"),
        "system_year": clean["yr"],
        "season": clean["season"],
        "mnth": clean["mnth"],
        "hr": clean["hr"],
        "holiday": clean["holiday"],
        "weekday": clean["weekday"],
        "workingday": clean["workingday"],
        "weathersit": clean["weathersit"],
        "temp_c": (clean["temp"] * TEMP_MAX_C).round(2),
        "feels_like_c": (clean["atemp"] * ATEMP_MAX_C).round(2),
        "humidity_pct": (clean["hum"] * HUM_MAX).round(1),
        "wind_kmh": (clean["windspeed"] * WIND_MAX_KMH).round(2),
        TARGET: clean["cnt"],
    })
    return gold.reset_index(drop=True)


def build_forecast_features(weather: pd.DataFrame, holidays: set[date], system_year: int = 1) -> pd.DataFrame:
    """Previsión horaria (Open-Meteo) y festivos """
    ts = pd.to_datetime(weather["time"])
    days = ts.dt.date
    # UCI: 0 = domingo,..., 6 = sábado
    weekday = (ts.dt.dayofweek + 1) % 7
    holiday = days.map(lambda d: int(d in holidays))
    workingday = ((weekday.between(1, 5)) & (holiday == 0)).astype(int)
    return pd.DataFrame({
        "timestamp": ts,
        "system_year": system_year,
        "season": days.map(season_from_date),
        "mnth": ts.dt.month,
        "hr": ts.dt.hour,
        "holiday": holiday,
        "weekday": weekday,
        "workingday": workingday,
        "weathersit": weather["weather_code"].map(wmo_to_weathersit),
        "temp_c": weather["temperature_2m"].astype(float),
        "feels_like_c": weather["apparent_temperature"].astype(float),
        "humidity_pct": weather["relative_humidity_2m"].astype(float),
        "wind_kmh": weather["wind_speed_10m"].astype(float),
    })
