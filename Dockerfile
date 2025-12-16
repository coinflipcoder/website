FROM python:3.10-alpine

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure appuser owns the app directory
RUN chown -R appuser:appgroup /app

# Make scripts executable
RUN chmod +x /app/entrypoint.sh /app/minifyfont.py

# Switch to non-root user
USER appuser

CMD ["/app/entrypoint.sh"]
