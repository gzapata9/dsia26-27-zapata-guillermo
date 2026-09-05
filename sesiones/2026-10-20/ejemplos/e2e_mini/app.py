"""API mínima E2E — puerto 8010 para no chocar con otras demos."""

from __future__ import annotations

from flask import Flask, jsonify, request

app = Flask(__name__)


def summarize(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("text must be non-empty")
    words = text.split()
    return text if len(words) <= 12 else " ".join(words[:12]) + "…"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "field 'text' is required"}), 400
    try:
        summary = summarize(text)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"summary": summary, "provider": "mock"})


if __name__ == "__main__":
    app.run(debug=True, port=8010)
