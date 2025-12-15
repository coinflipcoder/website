#!/bin/sh

# Environment variables
WORKERS="${GUNICORN_WORKERS:-1}"
THREADS="${GUNICORN_THREADS:-8}"
BIND="${GUNICORN_BIND:-0.0.0.0}"
PORT="${GUNICORN_PORT:-8000}"

exec gunicorn app:app --workers "$WORKERS" --threads "$THREADS" --bind "$BIND":"$PORT"