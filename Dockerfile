FROM python:3.10-alpine

# Add user/group with the same id that the container will run as
RUN addgroup -S 985 && adduser -S 985 -G 985

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# app files need to be owned by the user running the app
RUN chown -R 985:985 /app

# app only needs read access
RUN chmod -R 440 /app

# except for the fonts dir, as the user needs to generate the minified fonts there
RUN chmod 770 /app/assets/fonts

# and needs to be able to execute the entrypoint ig
RUN chmod 550 /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh /app/minifyfont.py

USER appuser

CMD ["/app/entrypoint.sh"]
