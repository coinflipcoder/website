FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

COPY . .



RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app", "--workers", "1", "--threads", "8", "--bind", "0.0.0.0:8000"]