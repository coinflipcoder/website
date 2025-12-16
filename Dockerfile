FROM python:3.10-alpine

# Add user/group with the same id that the container will run as
RUN addgroup -S 985 && adduser -S 985 -G 985

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# app files need to be owned by the user running the app
RUN chown -R 985:985 /app

# the folders need execute
RUN chmod -R 550 /app

# the files dont
RUN find /app -type f -print0 | xargs -0 chmod 440

# except for the fonts dir, as the user needs to generate the minified fonts there
RUN chmod 770 /app/assets/fonts

# and the entrypoint / minify script, as those need to be executed
RUN chmod +x /app/entrypoint.sh /app/minifyfont.py

USER 985:985

CMD ["/app/entrypoint.sh"]
