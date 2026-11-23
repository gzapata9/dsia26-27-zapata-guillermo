# Cliente unificado de IA (borde de modelos vía API).

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass
from typing import Callable

import requests

logger = logging.getLogger("bikedemand.ai")


class AIClientError(RuntimeError):
    """Error del borde de IA. `transient=True` → tiene sentido reintentar."""

    def __init__(self, message: str, *, transient: bool = False, status: int | None = None):
        super().__init__(message)
        self.transient = transient
        self.status = status


@dataclass(frozen=True)
class AIResponse:
    provider: str
    text: str
    model: str = "mock"
    latency_ms: float = 0.0


@dataclass(frozen=True)
class AIConfig:
    hf_token: str | None = None
    hf_model: str = "meta-llama/Llama-3.1-8B-Instruct"
    nvidia_api_key: str | None = None
    nvidia_model: str = "nvidia/nemotron-3.5-bolt-e4b"
    nvidia_enable_thinking: bool = False
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    timeout: float = 30.0
    max_tokens: int = 400
    temperature: float = 0.3


def _classify_status(status: int | None, provider: str, detail: str) -> AIClientError:
    if status in (401, 403):
        return AIClientError(f"{provider}: credenciales inválidas o sin permiso ({status})", status=status)
    if status == 429:
        return AIClientError(f"{provider}: límite de peticiones/cuota (429)", status=status, transient=True)
    if status is not None and status >= 500:
        return AIClientError(f"{provider}: error del proveedor ({status})", status=status, transient=True)
    return AIClientError(f"{provider}: petición rechazada ({status}): {detail[:200]}", status=status)


_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def _strip_reasoning(text: str) -> str:
    """Quita el bloque de razonamiento (<think>…</think>) si el modelo lo devuelve en el texto."""
    return _THINK_RE.sub("", text or "").strip()


def _messages(prompt: str, system: str | None) -> list[dict]:
    msgs = [{"role": "system", "content": system}] if system else []
    return msgs + [{"role": "user", "content": prompt}]


def _mock(prompt: str, system: str | None, cfg: AIConfig) -> tuple[str, str]:
    first_line = prompt.strip().splitlines()[0] if prompt.strip() else ""
    return f"[mock] Recibido prompt de {len(prompt)} caracteres. {first_line[:160]}", "mock"


def _hf(prompt: str, system: str | None, cfg: AIConfig, client=None) -> tuple[str, str]:
    if not cfg.hf_token and client is None:
        raise AIClientError("Falta HF_TOKEN en el entorno")
    if client is None:
        try:
            from huggingface_hub import InferenceClient
        except ImportError as exc:
            raise AIClientError("Instala: pip install huggingface_hub") from exc
        client = InferenceClient(api_key=cfg.hf_token, provider="auto", timeout=cfg.timeout)
    try:
        out = client.chat_completion(messages=_messages(prompt, system), model=cfg.hf_model,
                                     max_tokens=cfg.max_tokens, temperature=cfg.temperature)
    except Exception as exc:  # el SDK lanza HfHubHTTPError, timeouts de requests/httpx, etc.
        status = getattr(getattr(exc, "response", None), "status_code", None)
        if status is None and "timeout" in type(exc).__name__.lower():
            raise AIClientError("hf: timeout", transient=True) from exc
        raise _classify_status(status, "hf", str(exc)) from exc
    return _strip_reasoning(out.choices[0].message.content), cfg.hf_model


def _nvidia(prompt: str, system: str | None, cfg: AIConfig, post: Callable = requests.post) -> tuple[str, str]:
    if not cfg.nvidia_api_key:
        raise AIClientError("Falta NVIDIA_API_KEY en el entorno")
    try:
        r = post(f"{cfg.nvidia_base_url}/chat/completions", timeout=cfg.timeout,
                 headers={"Authorization": f"Bearer {cfg.nvidia_api_key}", "Accept": "application/json"},
                 json={"model": cfg.nvidia_model, "messages": _messages(prompt, system),
                       "max_tokens": cfg.max_tokens, "temperature": cfg.temperature, "stream": False,
                       "chat_template_kwargs": {"enable_thinking": cfg.nvidia_enable_thinking}})
    except requests.Timeout as exc:
        raise AIClientError("nvidia: timeout", transient=True) from exc
    except requests.RequestException as exc:
        raise AIClientError(f"nvidia: error de red: {exc}", transient=True) from exc
    if r.status_code >= 400:
        raise _classify_status(r.status_code, "nvidia", r.text)
    try:
        text = r.json()["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise AIClientError("nvidia: respuesta con formato inesperado") from exc
    return _strip_reasoning(text), cfg.nvidia_model


_PROVIDERS: dict[str, Callable] = {"mock": _mock, "hf": _hf, "nvidia": _nvidia}


def complete(provider: str, prompt: str, *, system: str | None = None, config: AIConfig | None = None,
             **provider_kwargs) -> AIResponse:
    """Una llamada (sin reintentos) al proveedor elegido."""
    provider = provider.lower().strip()
    if provider not in _PROVIDERS:
        raise AIClientError(f"Proveedor no soportado: {provider}")
    cfg = config or AIConfig()
    t0 = time.perf_counter()
    text, model = _PROVIDERS[provider](prompt, system, cfg, **provider_kwargs)
    if not text:
        raise AIClientError(f"{provider}: respuesta vacía", transient=False)
    return AIResponse(provider=provider, text=text, model=model,
                      latency_ms=round((time.perf_counter() - t0) * 1000, 1))


def complete_with_retries(provider: str, prompt: str, *, attempts: int = 3, base_delay: float = 0.5,
                          sleep: Callable[[float], None] = time.sleep, **kwargs) -> AIResponse:
    """`complete` + reintentos con backoff exponencial SOLO para errores transitorios."""
    for attempt in range(1, attempts + 1):
        try:
            resp = complete(provider, prompt, **kwargs)
            logger.info("ai_ok provider=%s model=%s latency_ms=%.1f n_chars_prompt=%d attempt=%d",
                        resp.provider, resp.model, resp.latency_ms, len(prompt), attempt)
            return resp
        except AIClientError as exc:
            if not exc.transient or attempt == attempts:
                logger.error("ai_failed provider=%s attempt=%d/%d transient=%s cause=%s",
                             provider, attempt, attempts, exc.transient, exc)
                raise
            logger.warning("ai_retry provider=%s attempt=%d/%d cause=%s", provider, attempt, attempts, exc)
            sleep(base_delay * 2 ** (attempt - 1))
    raise AIClientError("Reintentos agotados")  # pragma: no cover
