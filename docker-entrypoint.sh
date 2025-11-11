#!/bin/bash

# Script de inicialização do container VTasks

set -e

echo "════════════════════════════════════════"
echo "VTasks - Inicializando aplicação"
echo "════════════════════════════════════════"

# Aguardar MySQL estar pronto
echo "Aguardando MySQL inicializar..."
DB_USER=${DB_USER:-$MYSQL_USER}
DB_PASSWORD=${DB_PASSWORD:-$MYSQL_PASSWORD}
DB_NAME=${DB_NAME:-$MYSQL_DATABASE}
until mysqladmin ping -h db -u "$DB_USER" -p"$DB_PASSWORD" --silent; do
  >&2 echo "MySQL ainda não está pronto - aguardando..."
  sleep 1
done

echo "MySQL está pronto!"

# Executar migrations
echo "Executando migrations do banco de dados..."
cd /app
flask db upgrade || {
  echo "Migrations falharam, tentando novamente..."
  sleep 2
  flask db upgrade
}

echo "Migrations concluídas!"

# Iniciar aplicação
echo "Iniciando Flask..."
exec "$@"
