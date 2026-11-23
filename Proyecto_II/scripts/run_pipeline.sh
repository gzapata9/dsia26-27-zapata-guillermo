# Script que puede reentrenar el modelo para poder programarlo con el
# programador de tareas de windows u otra plataforma
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

if [ -f "$REPO/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "$REPO/.venv/bin/activate"
fi

OUT="${OUTPUT_DIR:-$REPO/outputs}"

python -m bikedemand --output-dir "$OUT" prepare \
  && python -m bikedemand --output-dir "$OUT" train \
  && python -m bikedemand --output-dir "$OUT" forecast \
  && echo "$(date -u +%FT%TZ) pipeline OK -> $OUT/briefing.md"
