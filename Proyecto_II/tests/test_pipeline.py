"""Tests de integración: jobs completos y CLI (exit codes, gates, degradación, idempotencia)."""
import json

import pytest

from bikedemand import cli, jobs
from bikedemand.errors import DataContractError, ModelNotFoundError, QualityGateError, UpstreamError
from bikedemand.integrations import open_data_client as od
from bikedemand.integrations.ai_client import AIClientError
from conftest import fake_holidays, fake_weather


@pytest.mark.integration
def test_prepare_train_forecast_end_to_end(settings, weather_fn, holidays_fn):
    prep = jobs.prepare(settings, "t")
    assert prep["status"] == "ok" and settings.gold_path.exists() and settings.quarantine_path.exists()

    tr = jobs.train(settings, "t", max_iter=60)
    assert tr["status"] == "ok" and settings.model_path.exists() and settings.model_card_path.exists()

    fc = jobs.forecast(settings, "t", weather_fn=weather_fn, holidays_fn=holidays_fn)
    assert fc["status"] == "ok" and fc["hours"] == 48 and fc["ai"]["provider"] == "mock"
    report = (settings.output_dir / "briefing.md").read_text(encoding="utf-8")
    assert "Thanksgiving" in report and "Resumen por reglas" in report and "[mock]" in report
    metrics = json.loads((settings.output_dir / "forecast_metrics.json").read_text())
    assert metrics["dependencies"] == {"weather": "ok", "holidays": "ok", "ai": "ok"}


def test_prepare_gate_blocks_publication(settings, raw_df):
    raw_df.loc[:200, "hr"] = 99  # ~14 % de filas inválidas
    raw_df.to_csv(settings.raw_path, index=False)
    with pytest.raises(QualityGateError):
        jobs.prepare(settings, "t")
    assert not settings.gold_path.exists()
    assert json.loads((settings.output_dir / "prepare_metrics.json").read_text())["status"] == "gate_failed"


def test_train_gate_does_not_overwrite_model(settings):
    jobs.prepare(settings, "t")
    strict = settings.with_overrides(min_r2=0.999)
    with pytest.raises(QualityGateError):
        jobs.train(strict, "t", max_iter=20)
    assert not settings.model_path.exists()


def test_train_without_gold(settings):
    with pytest.raises(DataContractError):
        jobs.train(settings, "t")


def test_forecast_without_model(settings, weather_fn, holidays_fn):
    with pytest.raises(ModelNotFoundError):
        jobs.forecast(settings, "t", weather_fn=weather_fn, holidays_fn=holidays_fn)


@pytest.fixture
def trained(settings):
    jobs.prepare(settings, "t")
    jobs.train(settings, "t", max_iter=40)
    return settings


def test_forecast_weather_down_is_upstream_error(trained, holidays_fn):
    def down(*a, **k):
        raise od.OpenAPIError("caído", transient=True)
    with pytest.raises(UpstreamError):
        jobs.forecast(trained, "t", weather_fn=down, holidays_fn=holidays_fn)


def test_forecast_degrades_when_holidays_and_ai_fail(trained, weather_fn):
    def no_holidays(*a, **k):
        raise od.OpenAPIError("caído")

    def broken_ai(*a, **k):
        raise AIClientError("401", status=401)

    rep = jobs.forecast(trained, "t", weather_fn=weather_fn, holidays_fn=no_holidays, ai_fn=broken_ai)
    assert rep["status"] == "degraded"
    assert rep["dependencies"] == {"weather": "ok", "holidays": "degraded", "ai": "degraded"}
    report = (trained.output_dir / "briefing.md").read_text(encoding="utf-8")
    assert "modo degradado" in report and "Pico principal" in report


def test_forecast_is_idempotent(trained, weather_fn, holidays_fn):
    jobs.forecast(trained, "a", weather_fn=weather_fn, holidays_fn=holidays_fn)
    first = (trained.output_dir / "forecast.csv").read_text()
    jobs.forecast(trained, "b", weather_fn=weather_fn, holidays_fn=holidays_fn)
    assert (trained.output_dir / "forecast.csv").read_text() == first
    assert sorted(p.name for p in trained.output_dir.iterdir()) == sorted(
        ["forecast.csv", "briefing.md", "forecast_metrics.json", "prepare_metrics.json", "train_metrics.json"])


def test_summarize_forecast_windows_do_not_overlap(trained, weather_fn, holidays_fn):
    jobs.forecast(trained, "t", weather_fn=weather_fn, holidays_fn=holidays_fn)
    import pandas as pd
    df = pd.read_csv(trained.output_dir / "forecast.csv", parse_dates=["timestamp"])
    s = jobs.summarize_forecast(df, "DC", [])
    assert len(s["peak_hours"]) == 3 and len(s["maintenance_windows"]) == 2
    assert s["peak_hours"][0]["pred_cnt"] >= s["peak_hours"][1]["pred_cnt"]
    assert len(s["bad_weather_hours"]) == 6


# ------------------------------------------------------------------ CLI
def _cli(settings, *args):
    return cli.main(["--env-file", "", "--output-dir", str(settings.output_dir), *args])


@pytest.fixture
def cli_env(settings, monkeypatch):
    for var in ("AI_PROVIDER", "HF_TOKEN", "NVIDIA_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("RAW_PATH", str(settings.raw_path))
    monkeypatch.setenv("DATA_DIR", str(settings.data_dir))
    monkeypatch.setenv("MODEL_DIR", str(settings.model_dir))
    monkeypatch.setenv("MIN_R2", "0.5")
    monkeypatch.setattr(od, "hourly_weather_forecast", fake_weather())
    monkeypatch.setattr(od, "public_holidays", fake_holidays)
    return settings


@pytest.mark.integration
def test_cli_prepare_train_forecast_exit_0(cli_env, capsys):
    assert _cli(cli_env, "prepare") == 0
    assert _cli(cli_env, "train", "--test-from", "2012-09-20") == 0
    out = capsys.readouterr().out
    assert "prepare OK" in out and "train OK" in out
    assert _cli(cli_env, "forecast", "--provider", "mock", "--hours", "48") == 0
    assert "forecast OK" in capsys.readouterr().out
    assert (cli_env.output_dir / "run.log").exists()


def test_cli_exit_codes(cli_env, monkeypatch, tmp_path):
    assert _cli(cli_env, "forecast") == 2                        # sin modelo
    assert _cli(cli_env, "prepare", "--max-error-rate", "1.5") == 2  # config inválida
    monkeypatch.setenv("AI_PROVIDER", "nvidia")                 # proveedor real sin clave
    assert _cli(cli_env, "train") == 2
    monkeypatch.setenv("AI_PROVIDER", "mock")
    assert _cli(cli_env, "prepare", "--input", str(tmp_path / "x.csv")) == 2


def test_cli_fetch_skips_existing_file(cli_env):
    assert _cli(cli_env, "fetch") == 0
