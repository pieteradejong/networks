#!/usr/bin/env bash
# test.sh — every check in one place. Exit 0 = all green = safe to commit.
# Mirrors CI (black, ruff, pytest) over the tracked Python files; also checks the venv matches
# requirements.txt, shell syntax and shellcheck, and that no .env is tracked.
# `./run.sh test` runs this script.
#   ./test.sh            all checks
#   ./test.sh --help     this text
set -euo pipefail
cd "$(dirname "$0")"

case "${1:-}" in -h|--help|help) sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;; esac

VENV=venv
PY="$VENV/bin/python"
[ -x "$PY" ] || { echo "No $VENV: run ./init.sh first" >&2; exit 1; }

echo "== python: $("$PY" --version)"

echo "== deps: venv matches requirements.txt"
"$PY" -m pip check
"$PY" -m pip install --quiet --disable-pip-version-check --dry-run --no-deps -r requirements.txt 2>&1 \
  | grep -q 'Would install' && { echo "venv is missing pinned packages; run ./init.sh" >&2; exit 1; } || true

echo "== secrets: no tracked .env"
tracked="$(git ls-files | grep -E '(^|/)\.env(\..+)?$' | grep -vE '\.env\.(example|template)$' || true)"
[ -z "$tracked" ] || { echo "env files must never be tracked:"; echo "$tracked"; exit 1; }

echo "== shell: syntax (bash, /bin/bash 3.2) and shellcheck"
for f in ./*.sh; do bash -n "$f"; /bin/bash -n "$f"; done
if command -v shellcheck >/dev/null 2>&1; then shellcheck -S warning ./*.sh; else echo "   shellcheck not installed; syntax-checked only (brew install shellcheck)"; fi

# Tracked files only: what CI sees. An untracked scratch file is not a failing build.
echo "== format: black --check (tracked .py)"
git ls-files -z -- '*.py' | xargs -0 "$PY" -m black --check --quiet

echo "== lint: ruff check (tracked .py)"
git ls-files -z -- '*.py' | xargs -0 "$PY" -m ruff check

echo "== compile: every tracked module"
git ls-files -z -- '*.py' | xargs -0 "$PY" -m compileall -q

echo "== unit: pytest"
# pytest exits 5 when no tests are collected; an empty tests/ is not a failure here.
"$PY" -m pytest -q || { rc=$?; [ "$rc" -eq 5 ] && echo "   no tests collected" || exit "$rc"; }

echo "== all green"
