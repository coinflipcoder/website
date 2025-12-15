FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/minifyfont.py

CMD ["/app/entrypoint.sh"]