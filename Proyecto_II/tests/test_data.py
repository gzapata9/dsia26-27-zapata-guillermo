"""Tests unitarios de ingesta, calidad y features (funciones puras)."""
import io
import zipfile
from datetime import date

import pandas as pd
import pytest
import requests

from bikedemand.errors import DataContractError, UpstreamError
from bikedemand.pipeline import features, ingest, quality


# ------------------------------------------------------------------ ingest
def test_load_raw_ok(settings):
    assert len(ingest.load_raw(settings.raw_path)) == 60 * 24


def test_load_raw_missing_file(tmp_path):
    with pytest.raises(DataContractError):
        ingest.load_raw(tmp_path / "nope.csv")


def test_load_raw_missing_columns(tmp_path, raw_df):
    path = tmp_path / "bad.csv"
    raw_df.drop(columns=["cnt"]).to_csv(path, index=False)
    with pytest.raises(DataContractError, match="cnt"):
        ingest.load_raw(path)


class _Resp:
    def __init__(self, content=b"", status=200):
        self.content, self.status_code = content, status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


def test_fetch_dataset_downloads_and_is_idempotent(tmp_path, monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("hour.csv", "a,b\n1,2\n")
    calls = []
    monkeypatch.setattr(requests, "get", lambda url, timeout: calls.append(url) or _Resp(buf.getvalue()))
    dest = tmp_path / "raw" / "hour.csv"
    ingest.fetch_dataset(dest)
    ingest.fetch_dataset(dest)  # segunda vez: no descarga
    assert dest.read_text() == "a,b\n1,2\n" and len(calls) == 1


def test_fetch_dataset_upstream_error(tmp_path, monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url, timeout: _Resp(status=503))
    with pytest.raises(UpstreamError):
        ingest.fetch_dataset(tmp_path / "hour.csv")


# ------------------------------------------------------------------ quality
def test_validate_clean_data(raw_df):
    res = quality.validate(raw_df)
    assert res.report["error_rate"] == 0 and len(res.rejected) == 0


def test_validate_sends_bad_rows_to_quarantine(raw_df):
    bad = raw_df.copy()
    bad.loc[0, "hr"] = 25                       # fuera de rango
    bad.loc[1, "cnt"] = bad.loc[1, "cnt"] + 7   # cnt != casual + registered
    bad.loc[2, "dteday"] = "no-es-fecha"
    bad = pd.concat([bad, bad.iloc[[10]]])      # duplicado fecha-hora
    res = quality.validate(bad)
    assert res.report["rows_rejected"] == 4
    assert set(res.rejected["reject_reason"]) == {
        "hr_fuera_de_rango", "cnt_distinto_de_casual_mas_registered", "fecha_invalida", "duplicado_fecha_hora"}
    assert len(res.clean) + len(res.rejected) == len(bad)


def test_save_layers_is_idempotent(tmp_path, raw_df):
    res = quality.validate(raw_df)
    silver, quar = tmp_path / "s.csv", tmp_path / "q.csv"
    quality.save_layers(res, silver, quar)
    first = silver.read_text()
    quality.save_layers(res, silver, quar)
    assert silver.read_text() == first


# ------------------------------------------------------------------ features
@pytest.mark.parametrize("d, season", [
    (date(2026, 1, 15), 1), (date(2026, 3, 21), 2), (date(2026, 7, 1), 3),
    (date(2026, 9, 23), 4), (date(2026, 12, 21), 1),
])
def test_season_from_date(d, season):
    assert features.season_from_date(d) == season


@pytest.mark.parametrize("code, sit", [(0, 1), (3, 2), (45, 2), (61, 3), (95, 3), (65, 4), (999, 2)])
def test_wmo_to_weathersit(code, sit):
    assert features.wmo_to_weathersit(code) == sit


def test_build_training_table_units(raw_df):
    gold = features.build_training_table(quality.validate(raw_df).clean)
    assert set(features.FEATURES) <= set(gold.columns)
    assert gold["temp_c"].iloc[0] == pytest.approx(0.6 * 41)
    assert gold["wind_kmh"].iloc[0] == pytest.approx(0.2 * 67)


def test_build_forecast_features_calendar(weather_fn):
    w = pd.DataFrame(weather_fn(0, 0, 48, "tz").data)
    feats = features.build_forecast_features(w, {date(2026, 11, 26)})
    thursday = feats[feats["timestamp"].dt.date == date(2026, 11, 26)].iloc[0]
    friday = feats[feats["timestamp"].dt.date == date(2026, 11, 27)].iloc[0]
    assert thursday["weekday"] == 4 and thursday["holiday"] == 1 and thursday["workingday"] == 0
    assert friday["workingday"] == 1 and friday["season"] == 4
    assert feats["weathersit"].iloc[-1] == 3  # lluvia en las últimas horas
