#!/usr/bin/env bash
# Simple wrapper to set up a virtualenv and run Scanlytic CLI or example script
# Usage:
#   ./scripts/run_scanlytic.sh setup      # create venv and install deps
#   ./scripts/run_scanlytic.sh example    # run examples/basic_usage.py
#   ./scripts/run_scanlytic.sh analyze /path/to/target [--recursive] [-o out.json]

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"

print_help() {
  cat <<EOF
Usage: $0 <command> [args]

Commands:
  setup                Create virtualenv (at .venv) and install requirements
  example              Run examples/basic_usage.py
  analyze <path> [...] Run CLI analyze command (forwards args to python -m scanlytic analyze)
  shell                Open a subshell with the virtualenv activated
  help                 Show this help message

Examples:
  $0 setup
  $0 example
  $0 analyze /tmp/samples -r -o ./report.json -f json

EOF
}

ensure_venv() {
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "Creating virtualenv at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
  fi

  echo "Installing Python dependencies..."
  "$PIP_BIN" install --upgrade pip
  "$PIP_BIN" install -r "$ROOT_DIR/requirements.txt"
}

cmd="$1"
shift || true

case "$cmd" in
  setup)
    ensure_venv
    echo "Setup complete. Activate with: source $VENV_DIR/bin/activate";
    ;;

  example)
    ensure_venv
    echo "Running example script..."
    "$PYTHON_BIN" "$ROOT_DIR/examples/basic_usage.py" "$@"
    ;;

  analyze)
    ensure_venv
    if [ $# -lt 1 ]; then
      echo "analyze requires a path argument" >&2
      exit 2
    fi
    # Forward all args to CLI module
    "$PYTHON_BIN" -m scanlytic analyze "$@"
    ;;

  shell)
    ensure_venv
    echo "Launching subshell with virtualenv activated. Exit to return.";
    # shell with venv activated
    bash --rcfile <(cat <<'RC'
source "$VENV_DIR/bin/activate"
PS1="(scanlytic) $PS1"
RC
)
    ;;

  help|--help|-h|"")
    print_help
    ;;

  *)
    echo "Unknown command: $cmd" >&2
    print_help
    exit 2
    ;;
esac
