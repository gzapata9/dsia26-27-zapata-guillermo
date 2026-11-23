"""Tests de los bordes externos sin red: HTTP simulado y proveedores de IA falsos."""
from types import SimpleNamespace

import pytest
import requests

from bikedemand.integrations import ai_client as ai
from bikedemand.integrations import open_data_client as od
from bikedemand.integrations.prompts import build_briefing_prompt


# ------------------------------------------------------------------ open data
class _R:
    def __init__(self, status=200, payload=None, bad_json=False):
        self.status_code, self._payload, self._bad = status, payload, bad_json

    def json(self):
        if self._bad:
            raise ValueError("bad json")
        return self._payload


HOURLY_OK = {"hourly": {"time": ["2026-11-26T00:00", "2026-11-26T01:00"],
                        "temperature_2m": [5, 4], "apparent_temperature": [3, 2],
                        "relative_humidity_2m": [70, 72], "wind_speed_10m": [8, 9], "weather_code": [0, 61]}}


def _patch_get(monkeypatch, responses):
    it = iter(responses)

    def fake_get(url, params=None, timeout=None, headers=None):
        r = next(it)
        if isinstance(r, Exception):
            raise r
        return r
    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(od.time, "sleep", lambda s: None)


def test_weather_ok(monkeypatch):
    _patch_get(monkeypatch, [_R(payload=HOURLY_OK)])
    res = od.hourly_weather_forecast(38.9, -77.0, hours=2)
    assert res.source == "open-meteo" and res.data["weather_code"] == [0, 61]


def test_weather_retries_transient_then_ok(monkeypatch):
    _patch_get(monkeypatch, [requests.Timeout(), _R(payload=HOURLY_OK)])
    assert len(od.hourly_weather_forecast(0, 0).data["time"]) == 2


def test_weather_4xx_not_retried(monkeypatch):
    _patch_get(monkeypatch, [_R(status=400)])
    with pytest.raises(od.OpenAPIError) as exc:
        od.hourly_weather_forecast(0, 0)
    assert exc.value.status == 400 and not exc.value.transient


@pytest.mark.parametrize("payload", [{"hourly": {"time": []}}, {"foo": 1},
                                      {"hourly": {**HOURLY_OK["hourly"], "weather_code": [0]}}])
def test_weather_invalid_payload(monkeypatch, payload):
    _patch_get(monkeypatch, [_R(payload=payload)])
    with pytest.raises(od.OpenAPIError):
        od.hourly_weather_forecast(0, 0)


def test_weather_5xx_exhausts_retries(monkeypatch):
    _patch_get(monkeypatch, [_R(status=503), _R(status=503)])
    with pytest.raises(od.OpenAPIError) as exc:
        od.hourly_weather_forecast(0, 0)
    assert exc.value.transient


def test_bad_json(monkeypatch):
    _patch_get(monkeypatch, [_R(bad_json=True)])
    with pytest.raises(od.OpenAPIError):
        od.public_holidays("US", 2026)


def test_holidays_filters_subdivision(monkeypatch):
    payload = [{"date": "2026-11-26", "name": "Thanksgiving Day", "global": True},
               {"date": "2026-04-16", "name": "DC Emancipation Day", "global": False, "counties": ["US-DC"]},
               {"date": "2026-03-02", "name": "Texas Independence", "global": False, "counties": ["US-TX"]}]
    _patch_get(monkeypatch, [_R(payload=payload)])
    res = od.public_holidays("us", 2026, subdivision="US-DC")
    assert [h["name"] for h in res.data["holidays"]] == ["Thanksgiving Day", "DC Emancipation Day"]
    assert len(od.holiday_dates(res)) == 2


# ------------------------------------------------------------------ IA
def test_mock_contract():
    resp = ai.complete("mock", "Hola DSIA")
    assert isinstance(resp, ai.AIResponse) and resp.provider == "mock" and "Hola DSIA" in resp.text


def test_unknown_provider():
    with pytest.raises(ai.AIClientError):
        ai.complete("openai-pirata", "hola")


def test_missing_keys():
    with pytest.raises(ai.AIClientError, match="HF_TOKEN"):
        ai.complete("hf", "hola", config=ai.AIConfig())
    with pytest.raises(ai.AIClientError, match="NVIDIA_API_KEY"):
        ai.complete("nvidia", "hola", config=ai.AIConfig())


class FakeHF:
    def __init__(self, errors=(), content="Briefing HF"):
        self.errors, self.content, self.calls = list(errors), content, 0

    def chat_completion(self, **kw):
        self.calls += 1
        assert kw["messages"][0]["role"] == "system" and kw["model"] == "owner/model"
        if self.errors:
            raise self.errors.pop(0)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))])


def _http_error(status):
    exc = Exception(f"HTTP {status}")
    exc.response = SimpleNamespace(status_code=status)
    return exc


CFG = ai.AIConfig(hf_token="t", hf_model="owner/model", nvidia_api_key="k")


def test_hf_ok():
    resp = ai.complete("hf", "p", system="s", config=CFG, client=FakeHF())
    assert resp.text == "Briefing HF" and resp.model == "owner/model"


def test_hf_retries_on_503_then_ok():
    fake = FakeHF(errors=[_http_error(503)])
    resp = ai.complete_with_retries("hf", "p", system="s", config=CFG, client=fake, sleep=lambda s: None)
    assert resp.text == "Briefing HF" and fake.calls == 2


def test_hf_401_is_not_retried():
    fake = FakeHF(errors=[_http_error(401), _http_error(401)])
    with pytest.raises(ai.AIClientError, match="credenciales"):
        ai.complete_with_retries("hf", "p", system="s", config=CFG, client=fake, sleep=lambda s: None)
    assert fake.calls == 1


def test_hf_empty_answer():
    with pytest.raises(ai.AIClientError, match="vacía"):
        ai.complete("hf", "p", system="s", config=CFG, client=FakeHF(content=""))


class _Post:
    def __init__(self, responses):
        self.responses, self.calls = list(responses), []

    def __call__(self, url, **kw):
        self.calls.append((url, kw))
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


class _NR:
    def __init__(self, status=200, payload=None, text=""):
        self.status_code, self._p, self.text = status, payload, text

    def json(self):
        return self._p


def test_nvidia_ok_sends_openai_compatible_request():
    post = _Post([_NR(payload={"choices": [{"message": {"content": "Briefing NVIDIA"}}]})])
    resp = ai.complete("nvidia", "p", config=CFG, post=post)
    url, kw = post.calls[0]
    assert url.endswith("/chat/completions") and kw["headers"]["Authorization"] == "Bearer k"
    assert kw["json"]["model"] == "nvidia/nemotron-3.5-bolt-e4b" and resp.text == "Briefing NVIDIA"
    assert kw["json"]["chat_template_kwargs"] == {"enable_thinking": False} and kw["json"]["stream"] is False


def test_reasoning_block_is_stripped():
    post = _Post([_NR(payload={"choices": [{"message": {"content": "<think>9.8 > 9.11…</think>\n- Pico a las 8 h"}}]})])
    assert ai.complete("nvidia", "p", config=CFG, post=post).text == "- Pico a las 8 h"


def test_nvidia_429_then_timeout_exhausts():
    post = _Post([_NR(status=429), requests.Timeout()])
    with pytest.raises(ai.AIClientError) as exc:
        ai.complete_with_retries("nvidia", "p", attempts=2, config=CFG, post=post, sleep=lambda s: None)
    assert exc.value.transient and len(post.calls) == 2


def test_nvidia_bad_payload():
    post = _Post([_NR(payload={"unexpected": True})])
    with pytest.raises(ai.AIClientError, match="formato"):
        ai.complete("nvidia", "p", config=CFG, post=post)


def test_prompt_contains_summary_fields():
    summary = {"city": "DC", "start": "a", "end": "b", "hours": 2, "total_pred": 100, "avg_per_hour": 50.0,
               "peak_hours": [{"timestamp": "26/11 08:00", "pred_cnt": 70, "weather": "despejado", "temp_c": 9.0}],
               "maintenance_windows": [{"start": "x", "end": "y", "avg_cnt": 3.0}],
               "bad_weather_hours": [], "holidays": ["Thanksgiving Day (26/11)"]}
    prompt = build_briefing_prompt(summary)
    assert "26/11 08:00" in prompt and "Thanksgiving" in prompt and "ninguna" in prompt
