# Borde HTTP de datos abiertos con Open-Meteo (previsión) y Nager.Date (festivos).

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import date
from typing import Any

import requests

logger = logging.getLogger("bikedemand.open_data")

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
NAGER_URL = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"
HOURLY_VARS = ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "wind_speed_10m", "weather_code"]


class OpenAPIError(RuntimeError):
    """Fallo del borde de datos abiertos. `transient=True` se vuelve a intentar"""

    def __init__(self, message: str, *, status: int | None = None, transient: bool = False):
        super().__init__(message)
        self.status = status
        self.transient = transient


@dataclass
class APIResult:
    source: str
    data: dict[str, Any]


def _get_json(url: str, *, params: dict | None = None, timeout: float = 15.0, attempts: int = 2,
              sleep=time.sleep) -> Any:
    last: OpenAPIError | None = None
    for attempt in range(1, attempts + 1):
        try:
            r = requests.get(url, params=params, timeout=timeout,
                             headers={"User-Agent": "bikedemand-dsia/0.2 (proyecto academico)"})
        except requests.Timeout as exc:
            last = OpenAPIError(f"Timeout al llamar {url}", transient=True)
        except requests.RequestException as exc:
            last = OpenAPIError(f"Error de red al llamar {url}: {exc}", transient=True)
        else:
            if r.status_code == 429 or r.status_code >= 500:
                last = OpenAPIError(f"{url} devolvió {r.status_code}", status=r.status_code, transient=True)
            elif r.status_code >= 400:  # 4xx: error de petición/configuración, no se reintenta
                raise OpenAPIError(f"{url} devolvió {r.status_code}", status=r.status_code)
            else:
                try:
                    return r.json()
                except ValueError as exc:
                    raise OpenAPIError(f"JSON inválido en {url}") from exc
        if attempt < attempts:
            logger.warning("open_data_retry attempt=%d/%d cause=%s", attempt, attempts, last)
            sleep(0.5 * 2 ** (attempt - 1))
    raise last  # type: ignore[misc]


def hourly_weather_forecast(lat: float, lon: float, hours: int = 48, tz: str = "America/New_York",
                            timeout: float = 15.0) -> APIResult:
    """Open-Meteo devuelve listas alineadas por hora (unidades: °C, %, km/h, WMO)."""
    payload = _get_json(OPEN_METEO_URL, timeout=timeout, params={
        "latitude": lat, "longitude": lon, "hourly": ",".join(HOURLY_VARS),
        "forecast_hours": hours, "timezone": tz, "wind_speed_unit": "kmh",
    })
    hourly = payload.get("hourly") if isinstance(payload, dict) else None
    if not hourly or "time" not in hourly or any(v not in hourly for v in HOURLY_VARS):
        raise OpenAPIError("Respuesta de Open-Meteo sin las variables horarias esperadas")
    n = len(hourly["time"])
    if n == 0 or any(len(hourly[v]) != n for v in HOURLY_VARS):
        raise OpenAPIError("Open-Meteo devolvió series horarias vacías o desalineadas")
    if any(x is None for v in HOURLY_VARS for x in hourly[v]):
        raise OpenAPIError("Open-Meteo devolvió valores nulos en la previsión")
    data = {"time": hourly["time"], **{v: hourly[v] for v in HOURLY_VARS}}
    logger.info("weather_ok source=open-meteo hours=%d first=%s", n, hourly["time"][0])
    return APIResult(source="open-meteo", data=data)


def public_holidays(country: str, year: int, subdivision: str | None = None,
                    timeout: float = 15.0) -> APIResult:
    """Nager.Datedevuelve los festivos nacionales"""
    payload = _get_json(NAGER_URL.format(year=year, country=country.upper()), timeout=timeout)
    if not isinstance(payload, list):
        raise OpenAPIError(f"Respuesta inesperada de festivos para {country}/{year}")
    days = []
    for h in payload:
        counties = h.get("counties") or []
        if h.get("global") or (subdivision and subdivision in counties):
            days.append({"date": h.get("date"), "name": h.get("name")})
    logger.info("holidays_ok source=nager.date country=%s year=%d n=%d", country, year, len(days))
    return APIResult(source="nager.date", data={"holidays": days})


def holiday_dates(result: APIResult) -> set[date]:
    return {date.fromisoformat(h["date"]) for h in result.data["holidays"]}
