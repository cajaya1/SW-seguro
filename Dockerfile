FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application structure
COPY src/ ./src/
COPY data/modelo_seguridad_final.pkl ./data/

# Expose port
EXPOSE 5000

# Set environment variable
ENV ENVIRONMENT=production
ENV PYTHONPATH=/app

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app.app:app"]
