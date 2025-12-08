#!/bin/sh

echo "Minifying fonts..."
python3 /app/minifyfont.py --site-dir /app/pages --fonts-dir /app/assets/fonts --output-dir /app/assets/fonts
echo "Finished minifying fonts."

cp -r /app/assets/* /static/

# Environment variables
WORKERS="${GUNICORN_WORKERS:-1}"
THREADS="${GUNICORN_THREADS:-8}"
BIND="${GUNICORN_BIND:-0.0.0.0}"
PORT="${GUNICORN_PORT:-8000}"

exec gunicorn app:app --workers "$WORKERS" --threads "$THREADS" --bind "$BIND":"$PORT"