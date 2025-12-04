FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Server static files through nginx proxy manager directly
RUN mkdir -p /static

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]

CMD ["gunicorn", "app:app", "--workers", "1", "--threads", "8", "--bind", "0.0.0.0:8000"]