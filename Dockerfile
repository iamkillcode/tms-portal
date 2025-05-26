FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    zstd \
    gettext \
    && apt-get clean

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=tender.settings
ENV DEBUG=False

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

# Change ownership of the workdir
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Port for Gunicorn
EXPOSE 8000

# Start the Django app with Gunicorn
CMD ["gunicorn", "tender.wsgi:application", "--bind", "0.0.0.0:8000"]

# Add a health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1
