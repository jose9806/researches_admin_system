FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

COPY pyproject.toml poetry.lock* ./
# Install dependencies
RUN pip install --no-cache-dir "poetry==1.8.4" && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy project
COPY . /app/

# Ensure manage.py is executable
RUN chmod +x /app/manage.py

# Run as non-root user for better security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "research_admin.wsgi:application"]