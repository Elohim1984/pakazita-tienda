#!/usr/bin/env bash
set -e

# scripts/run_migrations.sh
# Helper script to run Flask-Migrate commands consistently.
# Usage:
#   ./scripts/run_migrations.sh init
#   ./scripts/run_migrations.sh migrate "message"
#   ./scripts/run_migrations.sh upgrade

CMD="$1"
MSG="$2"

# ensure we're in repo root
cd "$(dirname "$0")/.."

# Ensure FLASK_APP is set
if [ -z "$FLASK_APP" ]; then
  export FLASK_APP=app.py
fi

# Ensure DATABASE_URL is present
if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DATABASE_URL is not set. Export it before running migrations." >&2
  exit 1
fi

case "$CMD" in
  init)
    flask db init
    ;;
  migrate)
    if [ -z "$MSG" ]; then
      echo "Usage: $0 migrate \"message\"" >&2
      exit 1
    fi
    flask db migrate -m "$MSG"
    ;;
  upgrade)
    flask db upgrade
    ;;
  *)
    echo "Usage: $0 {init|migrate \"message\"|upgrade}" >&2
    exit 1
    ;;
esac
