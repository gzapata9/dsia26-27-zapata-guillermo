#!/usr/bin/env bash
set -euo pipefail
BASE=${1:-http://127.0.0.1:8012}
curl -sf "$BASE/health" | grep -q status
curl -sf -X POST "$BASE/analyze" -H 'Content-Type: application/json' \
  -d '{"text":"smoke test DSIA"}' | grep -q summary
echo OK
