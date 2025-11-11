FROM python:3.12-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copiar aplicação
COPY . .

# Criar diretório para logs (se necessário)
RUN mkdir -p /app/logs && chmod 755 /app/logs

EXPOSE 5000

# Variáveis padrão
ENV FLASK_ENV=development \
    FLASK_APP=wsgi.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

