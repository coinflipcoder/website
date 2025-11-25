source ".venv/bin/activate.sh"

# deployment
# gunicorn app:app --workers 2 --threads 4

# development
gunicorn app:app --workers 1 --threads 1 \
 --reload --reload-engine="inotify" $(find ./pages ./assets -type f -printf '--reload-extra-file %p ')