# Docker Compose - VTasks

Este arquivo `compose.yaml` configura o ambiente completo para executar a aplicação VTasks em containers Docker.

## Serviços inclusos

### 1. **db** (PostgreSQL)
- Banco de dados PostgreSQL 16 Alpine
- Porta: `5432`
- Usuário: `vtasks_user`
- Senha: `vtasks_password_dev`
- Database: `vtasks_db`
- Verificação de saúde automática

### 2. **web** (Flask Application)
- Aplicação Flask Python
- Porta: `5000`
- Volume montado localmente para desenvolvimento (hot-reload)
- Depende do serviço `db`
- Executa automáticamente migrations no iniciar

### 3. **tests** (Pytest)
- Serviço opcional para execução de testes
- Profile: `tests`
- Executa testes automaticamente

## Pré-requisitos

- Docker
- Docker Compose (v3.8+)
- Git

## Como usar

### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
cd VTasks
```

### 2. Copiar arquivo de ambiente
```bash
cp .env.example .env
```

### 3. Editar variáveis de ambiente (opcional)
```bash
nano .env
```

### 4. Iniciar os serviços
```bash
# Iniciar todos os serviços
docker-compose up -d

# Ou com logs em tempo real
docker-compose up
```

### 5. Verificar logs
```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f web
docker-compose logs -f db
```

### 6. Acessar a aplicação
- URL: `http://localhost:5000`
- Banco de dados: `localhost:5432`

## Comandos úteis

### Parar os serviços
```bash
docker-compose down
```

### Remover volumes (limpar dados)
```bash
docker-compose down -v
```

### Executar testes
```bash
# Com profile
docker-compose run --rm tests

# Ou diretamente no container web
docker-compose exec web pytest -v
```

### Acessar shell da aplicação
```bash
docker-compose exec web bash
```

### Acessar shell do PostgreSQL
```bash
docker-compose exec db psql -U vtasks_user -d vtasks_db
```

### Executar migrations do banco de dados
```bash
# Upgrade
docker-compose exec web flask db upgrade

# Downgrade
docker-compose exec web flask db downgrade
```

### Reconstruir imagens
```bash
docker-compose build --no-cache
```

## Estrutura de Volume

```
PostgreSQL Data:
├── postgres_data/          # Dados persistentes do PostgreSQL

Aplicação (bindmount):
├── .                       # Diretório do projeto (sincronizado)
├── /app/__pycache__       # Cache Python (volume isolado)
```

## Variáveis de Ambiente

As seguintes variáveis podem ser configuradas no arquivo `.env`:

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `FLASK_ENV` | `development` | Ambiente da aplicação |
| `SECRET_KEY` | `sua_chave_secreta...` | Chave secreta da aplicação |
| `SQLALCHEMY_DATABASE_URI` | `postgresql://...` | String de conexão do banco |
| `SESSION_PERMANENT` | `False` | Manter sessão permanente |
| `SESSION_COOKIE_SAMESITE` | `Strict` | Política SAMESITE do cookie |
| `SESSION_COOKIE_HTTPONLY` | `True` | Cookie somente HTTP |

## Health Check

O serviço PostgreSQL possui verificação de saúde automática que:
- Verifica a cada 10 segundos
- Timeout de 5 segundos
- Retenta 5 vezes antes de falhar
- A aplicação Flask aguarda o banco estar saudável antes de iniciar

## Desenvolvimento

Durante o desenvolvimento:
1. O código local é montado como volume
2. Alterações no código são refletidas imediatamente (se usar Flask em modo debug)
3. O banco de dados persiste entre reinicializações
4. Logs são exibidos em tempo real

## Produção

Para ambiente de produção:
1. Alterar as variáveis de ambiente (especialmente `SECRET_KEY`)
2. Usar um reverse proxy (nginx/traefik)
3. Remover `volumes` de código-fonte
4. Usar WSGI server (gunicorn, uwsgi)
5. Configurar SSL/TLS
6. Usar variáveis secretas do Docker Secrets ou Vault

## Troubleshooting

### Porta já em uso
```bash
# Mudar porta no compose.yaml
# Exemplo: "5001:5000" para usar porta 5001 localmente
```

### Permissão negada ao criar volumes
```bash
# No Linux, adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
```

### Banco de dados não conecta
```bash
# Verificar se o container db está saudável
docker-compose ps

# Ver logs do PostgreSQL
docker-compose logs db
```

### Aplicação não encontra o banco
```bash
# Verificar conectividade entre containers
docker-compose exec web ping db

# Verificar variáveis de ambiente
docker-compose exec web env | grep DATABASE
```

## Referências

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
