FROM python:3.12-slim

# Minimal image to run the Flask app using the bundled sqlite DB
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       libffi-dev \
       libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Ensure files are readable
RUN chmod -R a+rX /app || true

EXPOSE 5000

# Default environment
ENV FLASK_ENV=development \
    FLASK_APP=wsgi.py

# Start the app directly (wsgi.py runs app.run when executed)
CMD ["python", "wsgi.py"]

