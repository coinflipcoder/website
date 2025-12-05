source ".venv/bin/activate"

# development inotify
# gunicorn app:app --workers 1 --threads 1 --reload --reload-engine="inotify" $(find ./pages ./assets -type f -printf '--reload-extra-file %p ')

# development polling
gunicorn app:app --workers 1 --threads 1 --reload --reload-engine="poll" $(find ./pages ./assets -type f -printf '--reload-extra-file %p ')

# would love to use inotify, but it automatically tracks all files in the directory tree without letting me exclude files... like a .db file...
