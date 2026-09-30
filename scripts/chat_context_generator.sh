#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_FILE="$ROOT_DIR/CHAT_CONTEXT.md"

cd "$ROOT_DIR"

{
  echo "# RadConductor Chat Context"
  echo
  echo "## Project tree"
  echo
  echo '```text'
  find . \
    -path './.git' -prune -o \
    -path './.venv' -prune -o \
    -path './.vscode' -prune -o \
    -path './data' -prune -o \
    -path './outputs' -prune -o \
    -path './logs' -prune -o \
    -path './build' -prune -o \
    -path './dist' -prune -o \
    -name '__pycache__' -prune -o \
    -name '*.egg-info' -prune -o \
    -name '.pytest_cache' -prune -o \
    -name '.ruff_cache' -prune -o \
    -name '.mypy_cache' -prune -o \
    -name '.DS_Store' -prune -o \
    -name '*.pyc' -prune -o \
    -name 'CHAT_CONTEXT.md' -prune -o \
    -print |
    sed 's|^\./||' |
    sort
  echo '```'

  for file in \
    HANDOFF.md \
    PROJECT_STATE.md \
    ARCHITECTURE.md \
    ENGINEERING_GUIDELINES.md
  do
    if [[ -f "$file" ]]; then
      echo
      echo "## $file"
      echo
      cat "$file"
    fi
  done
} > "$OUTPUT_FILE"

echo "Created: $OUTPUT_FILE"
