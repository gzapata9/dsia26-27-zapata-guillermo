#!/usr/bin/env bash
# Demo guiada del flujo venv (macOS/Linux). No hace push a GitHub.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

if [[ "${1:-}" == "--help" ]]; then
  cat <<EOF
Uso: bash sesiones/2026-09-08/ejemplos/demo_flujo.sh

Pasos:
  1) Crea .venv si no existe
  2) Activa e instala requirements.txt
  3) Ejecuta check_entorno.py --strict
EOF
  exit 0
fi

echo "==> Repo: $ROOT"
if [[ ! -d .venv ]]; then
  echo "==> Creando .venv"
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null
pip install -r requirements.txt
python sesiones/2026-09-08/ejemplos/check_entorno.py --strict
echo "==> Demo venv completada"
echo "Siguiente (manual): crea rama, commit y PR en tu repo personal"
