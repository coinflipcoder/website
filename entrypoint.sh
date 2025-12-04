#!/bin/sh

cp -r /app/assets/* /static/

exec gunicorn app:app --workers 1 --threads 8 --bind 0.0.0.0:8000