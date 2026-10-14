#!/usr/bin/env bash
# run.sh — entry points. Run ./init.sh once first.
#   ./run.sh [run]       python src/main.py (default)
#   ./run.sh test        every check (delegates to ./test.sh)
#   ./run.sh lint        black --check + ruff check
#   ./run.sh format      black + ruff check --fix
#   ./run.sh help        this text
set -euo pipefail
cd "$(dirname "$0")"

usage() { sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'; }
cmd="${1:-run}"
[ $# -gt 0 ] && shift
case "$cmd" in help|-h|--help) usage; exit 0 ;; esac

VENV=venv
PY="$VENV/bin/python"
[ -x "$PY" ] || { echo "No $VENV: run ./init.sh first" >&2; exit 1; }

case "$cmd" in
  run) exec "$PY" src/main.py "$@" ;;
  test) exec ./test.sh "$@" ;;
  lint) "$PY" -m black --check . && "$PY" -m ruff check . ;;
  format) "$PY" -m black . && "$PY" -m ruff check --fix . ;;
  *) echo "run.sh: unknown command: $cmd" >&2; usage >&2; exit 2 ;;
esac
