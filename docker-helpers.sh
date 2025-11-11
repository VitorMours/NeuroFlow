#!/bin/bash

# Script auxiliar para gerenciar Docker Compose do VTasks
# Uso: ./docker-helpers.sh [comando]

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_NAME="vtasks"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} VTasks Docker Compose Helper"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
}

print_help() {
    cat << EOF
${GREEN}Comandos disponíveis:${NC}

  ${YELLOW}up${NC}              - Iniciar os serviços
  ${YELLOW}down${NC}            - Parar os serviços
  ${YELLOW}logs${NC}            - Ver logs em tempo real
  ${YELLOW}build${NC}           - Reconstruir imagens
  ${YELLOW}clean${NC}           - Limpar containers, volumes e imagens
  ${YELLOW}shell-web${NC}       - Acessar shell da aplicação
  ${YELLOW}shell-db${NC}        - Acessar psql do PostgreSQL
  ${YELLOW}migrate${NC}         - Executar migrations
  ${YELLOW}test${NC}            - Executar testes
  ${YELLOW}seed${NC}            - Popular banco de dados
  ${YELLOW}install-deps${NC}    - Instalar/atualizar dependências
  ${YELLOW}ps${NC}              - Ver status dos containers
  ${YELLOW}restart${NC}         - Reiniciar serviços
  ${YELLOW}help${NC}            - Mostrar esta ajuda

${GREEN}Exemplos de uso:${NC}

  ./docker-helpers.sh up
  ./docker-helpers.sh logs
  ./docker-helpers.sh shell-web
  ./docker-helpers.sh migrate
  ./docker-helpers.sh test

EOF
}

up() {
    echo -e "${YELLOW}Iniciando serviços...${NC}"
    docker-compose up -d
    sleep 2
    ps
}

down() {
    echo -e "${YELLOW}Parando serviços...${NC}"
    docker-compose down
}

logs() {
    docker-compose logs -f "$@"
}

build() {
    echo -e "${YELLOW}Reconstruindo imagens...${NC}"
    docker-compose build --no-cache
}

clean() {
    echo -e "${RED}ATENÇÃO: Isso removerá containers, volumes e imagens!${NC}"
    read -p "Tem certeza? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        docker-compose down -v
        docker system prune -f
        echo -e "${GREEN}Limpeza concluída!${NC}"
    else
        echo "Operação cancelada"
    fi
}

shell_web() {
    echo -e "${YELLOW}Acessando shell da aplicação...${NC}"
    docker-compose exec web bash
}

shell_db() {
    echo -e "${YELLOW}Acessando PostgreSQL...${NC}"
    echo "Acessando MySQL (cliente mysql) dentro do container db..."
    # Usa variáveis de ambiente se estiverem definidas
    DB_USER=${DB_USER:-vtasks_user}
    DB_PASSWORD=${DB_PASSWORD:-vtasks_password_dev}
    DB_NAME=${DB_NAME:-vtasks_db}
    docker-compose exec db mysql -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME"
}

migrate() {
    echo -e "${YELLOW}Executando migrations...${NC}"
    docker-compose exec web flask db upgrade
}

test() {
    echo -e "${YELLOW}Executando testes...${NC}"
    docker-compose exec web pytest -v --tb=short
}

seed() {
    echo -e "${YELLOW}Populando banco de dados...${NC}"
    docker-compose exec web python -c "
from wsgi import create_app
from src.models import db
app = create_app('development')
with app.app_context():
    print('Banco de dados já existente!')
"
}

install_deps() {
    echo -e "${YELLOW}Atualizando dependências...${NC}"
    docker-compose exec web pip install -r requirements.txt
}

ps_status() {
    docker-compose ps
}

restart() {
    echo -e "${YELLOW}Reiniciando serviços...${NC}"
    down
    sleep 1
    up
}

# Main
print_header
echo

case "${1:-help}" in
    up)
        up
        ;;
    down)
        down
        ;;
    logs)
        shift
        logs "$@"
        ;;
    build)
        build
        ;;
    clean)
        clean
        ;;
    shell-web)
        shell_web
        ;;
    shell-db)
        shell_db
        ;;
    migrate)
        migrate
        ;;
    test)
        test
        ;;
    seed)
        seed
        ;;
    install-deps)
        install_deps
        ;;
    ps)
        ps_status
        ;;
    restart)
        restart
        ;;
    help)
        print_help
        ;;
    *)
        echo -e "${RED}Comando desconhecido: ${1}${NC}"
        echo
        print_help
        exit 1
        ;;
esac
