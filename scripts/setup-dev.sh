#!/usr/bin/env bash
set -euo pipefail

# Helper script to create and populate a repository-local virtual environment named .venv
# Usage: ./scripts/setup-dev.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "Creating virtual environment at .venv (if missing)..."
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

echo "Activating .venv and upgrading pip..."
# shellcheck source=/dev/null
source .venv/bin/activate
python -m pip install --upgrade pip

echo "Installing runtime requirements..."
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  echo "WARNING: requirements.txt not found; skipping runtime deps"
fi

echo "Installing dev requirements (if present)..."
if [ -f requirements-dev.txt ]; then
  pip install -r requirements-dev.txt
else
  echo "No requirements-dev.txt found; skipping dev deps"
fi

echo "Setup complete. Activate the venv with: source .venv/bin/activate"
