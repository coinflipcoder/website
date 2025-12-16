FROM python:3.10-alpine

# Create non-root user
RUN addgroup -S 985 && adduser -S 985 -G 985

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure appuser owns the app directory
RUN chown -R 985:985 /app

# Make scripts executable
RUN chmod +x /app/entrypoint.sh /app/minifyfont.py

# Switch to non-root user
USER appuser

CMD ["/app/entrypoint.sh"]
