"""Fixtures compartidas. Ningún test usa la red: las APIs se simulan y la IA va en mock."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from bikedemand.config import Settings
from bikedemand.integrations.open_data_client import APIResult

PROJECT = Path(__file__).resolve().parent.parent


def make_raw(days: int = 60, start: str = "2012-08-01") -> pd.DataFrame:
    """Dataset con el esquema UCI y un patrón aprendible (picos 8 h y 17-18 h en laborables)."""
    rng = np.random.default_rng(0)
    rows = []
    for d in pd.date_range(start, periods=days, freq="D"):
        weekday = (d.dayofweek + 1) % 7
        working = int(1 <= weekday <= 5)
        for hr in range(24):
            base = 20 + (200 if working and hr in (8, 17, 18) else 60 if 9 <= hr <= 20 else 0)
            weathersit = 3 if rng.random() < 0.1 else 1
            cnt = max(0, int(base * (0.4 if weathersit == 3 else 1) + rng.normal(0, 5)))
            casual = cnt // 4
            rows.append({
                "instant": len(rows) + 1, "dteday": d.strftime("%Y-%m-%d"), "season": 3, "yr": 1,
                "mnth": d.month, "hr": hr, "holiday": 0, "weekday": weekday, "workingday": working,
                "weathersit": weathersit, "temp": 0.6, "atemp": 0.55, "hum": 0.6, "windspeed": 0.2,
                "casual": casual, "registered": cnt - casual, "cnt": cnt,
            })
    return pd.DataFrame(rows)


@pytest.fixture
def raw_df() -> pd.DataFrame:
    return make_raw()


@pytest.fixture
def settings(tmp_path, raw_df) -> Settings:
    raw_path = tmp_path / "raw" / "hour.csv"
    raw_path.parent.mkdir()
    raw_df.to_csv(raw_path, index=False)
    return Settings(raw_path=raw_path, data_dir=tmp_path / "data", model_dir=tmp_path / "models",
                    output_dir=tmp_path / "out", test_from="2012-09-20", min_r2=0.5, ai_max_attempts=1)


def fake_weather(hours: int = 48, start: str = "2026-11-26 00:00", rain_hours: int = 6):
    times = pd.date_range(start, periods=hours, freq="h")
    codes = [0] * (hours - rain_hours) + [61] * rain_hours

    def _fn(lat, lon, n, tz, timeout=15.0):
        return APIResult("open-meteo", {
            "time": [t.strftime("%Y-%m-%dT%H:%M") for t in times],
            "temperature_2m": [15.0] * hours, "apparent_temperature": [14.0] * hours,
            "relative_humidity_2m": [60] * hours, "wind_speed_10m": [10.0] * hours, "weather_code": codes,
        })
    return _fn


def fake_holidays(country, year, subdivision=None, timeout=15.0):
    return APIResult("nager.date", {"holidays": [{"date": "2026-11-26", "name": "Thanksgiving Day"}]})


@pytest.fixture
def weather_fn():
    return fake_weather()


@pytest.fixture
def holidays_fn():
    return fake_holidays
