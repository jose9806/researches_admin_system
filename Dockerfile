FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./
# Install dependencies
RUN pip install --no-cache-dir "poetry==1.8.4" && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy project
COPY . /app/

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Make check_connections.py executable
RUN chmod +x /app/check_connections.py

# Run as non-root user for better security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Default command is now in docker-compose.yaml