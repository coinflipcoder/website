#!/bin/sh
# -u stops python from buffering prints until the script is done
python3 -u /app/minifyfont.py --fonts-dir /app/assets/fonts --output-dir /app/assets/fonts

# Environment variables
WORKERS="${GUNICORN_WORKERS:-1}"
THREADS="${GUNICORN_THREADS:-8}"
BIND="${GUNICORN_BIND:-0.0.0.0}"
PORT="${GUNICORN_PORT:-8000}"

exec gunicorn -c /app/gunicorn_config.py app:app --workers "$WORKERS" --threads "$THREADS" --bind "$BIND":"$PORT"