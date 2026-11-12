#!/bin/sh
set -u  # errors on undefined env variables (i think)
python3 -u /app/scripts/txtgenerator.py --file-dir /data --data-dir /app/pages/content

# Environment variables
WORKERS="${GUNICORN_WORKERS:-1}"
THREADS="${GUNICORN_THREADS:-8}"
BIND="${GUNICORN_BIND:-0.0.0.0}"
PORT="${GUNICORN_PORT:-8000}"

exec gunicorn -c /app/scripts/gunicorn_config.py app:app --no-control-socket --workers "$WORKERS" --threads "$THREADS" --bind "$BIND":"$PORT"
