FROM python:3.11

# Set work directory
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gosu \
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

# Make scripts executable
RUN chmod +x /app/check_connections.py
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Create the logs directory with appropriate permissions
RUN touch /app/django-error.log && chmod 666 /app/django-error.log 

# Run as non-root user for better security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
# Don't change to appuser yet so the entrypoint script can set permissions
# USER appuser

# Set entrypoint to handle permissions
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command is now in docker-compose.yaml