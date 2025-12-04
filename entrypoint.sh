#!/bin/sh

cp -r /app/assets/* /static/

exec gunicorn app:app --workers 4 --threads 4 --bind 0.0.0.0:8000