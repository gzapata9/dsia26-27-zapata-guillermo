from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/analyze")
def analyze():
    text = (request.get_json(silent=True) or {}).get("text", "")
    if not str(text).strip():
        return jsonify({"error": "text required"}), 400
    return jsonify({"summary": str(text)[:80], "provider": "mock"})


if __name__ == "__main__":
    app.run(debug=True, port=8012)
