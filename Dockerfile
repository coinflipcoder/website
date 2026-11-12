FROM python:3.13-slim-trixie

ARG APP_UID=985
ARG APP_GID=985

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DATABASE_PATH=/data/database.db

# 985 is only of importance because my deployment server generated that for this containers uid/gid
RUN groupadd --system --gid ${APP_GID} app \
 && useradd  --system --uid ${APP_UID} --gid ${APP_GID} \
             --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python3 scripts/minifyfont.py --fonts-dir assets/fonts --output-dir assets/fonts

# /txt is served from pages/content/txtversion.txt, but the real file is
# generated at startup into the writable /data volume
RUN ln -sf /data/txtversion.txt pages/content/txtversion.txt \
 && chmod 755 scripts/entrypoint.sh \
 && install -d -o app -g app -m 750 /data

USER app
EXPOSE 8000
CMD ["/app/scripts/entrypoint.sh"]
