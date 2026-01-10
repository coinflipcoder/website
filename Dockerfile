FROM python:3.10-alpine

# Add user/group with the same id that the container will run as
RUN addgroup -S 985 && adduser -S 985 -G 985

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# app files need to be owned by the user running the app
RUN chown -R 985:985 /app

# the folders need execute (and write, because of sqlite)
RUN chmod -R 770 /app

# the files dont
RUN find /app -type f -print0 | xargs -0 chmod 440

# and the entrypoint / minify script, as those need to be executed
RUN chmod +x /app/scripts/entrypoint.sh /app/scripts/minifyfont.py

USER 985:985

CMD ["/app/scripts/entrypoint.sh"]
