"""API con logging y fallo simulado — sesión 27 oct 2026."""

from __future__ import annotations

import logging
import os
import time
import uuid
from pathlib import Path

from flask import Flask, jsonify, request

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("dsia.robusta")

app = Flask(__name__)
DATA_PATH = Path(os.getenv("DATA_PATH", "."))


class AIProviderError(RuntimeError):
    pass


def call_ai(text: str) -> str:
    if os.getenv("FORCE_AI_FAIL") == "1":
        raise AIProviderError("provider unavailable")
    words = text.split()
    return text if len(words) <= 10 else " ".join(words[:10]) + "…"


@app.get("/health")
def health():
    checks = {
        "api": "ok",
        "data_path": "ok" if DATA_PATH.exists() else "fail",
        "ai": "fail" if os.getenv("FORCE_AI_FAIL") == "1" else "ok",
    }
    ok = all(v == "ok" for v in checks.values())
    return jsonify({"status": "ok" if ok else "degraded", "checks": checks}), (200 if ok else 503)


@app.post("/analyze")
def analyze():
    request_id = str(uuid.uuid4())
    payload = request.get_json(silent=True) or {}
    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        logger.warning("invalid_input request_id=%s", request_id)
        return jsonify({"error": "field 'text' is required", "request_id": request_id}), 400

    t0 = time.perf_counter()
    try:
        summary = call_ai(text.strip())
    except AIProviderError as exc:
        logger.error("ai_fail request_id=%s error=%s", request_id, exc)
        return jsonify({"error": str(exc), "request_id": request_id}), 503

    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info("analyze_ok request_id=%s latency_ms=%.1f", request_id, latency_ms)
    return jsonify({"summary": summary, "provider": "mock", "request_id": request_id, "latency_ms": latency_ms})


if __name__ == "__main__":
    app.run(debug=True, port=8011)
