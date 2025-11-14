FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/logs && chmod 755 /app/logs

EXPOSE 5000

ENV FLASK_ENV=production \
    FLASK_APP=wsgi.py

# HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    # CMD curl -f http://localhost:5000/health || exit 1

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
