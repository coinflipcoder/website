FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

COPY . .



RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app", "--workers", "2", "--threads", "4", "--bind", "0.0.0.0:8000"]