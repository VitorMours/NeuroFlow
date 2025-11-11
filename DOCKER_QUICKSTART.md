# 🐳 Docker Compose Setup - VTasks

## Quick Start

### 1️⃣ Preparação inicial
```bash
# Copiar arquivo de ambiente
cp .env.example .env

# Editar variáveis (opcional)
nano .env
```

### 2️⃣ Iniciar serviços
```bash
# Opção 1: Usar docker-compose diretamente
docker-compose up -d

# Opção 2: Usar script auxiliar (mais fácil)
chmod +x docker-helpers.sh
./docker-helpers.sh up
```

### 3️⃣ Verificar status
```bash
docker-compose ps

# Ou com script
./docker-helpers.sh ps
```

### 4️⃣ Acessar a aplicação
- URL: **http://localhost:5000**
- Admin: **http://localhost:5000/admin** (se configurado)

---

## 📝 Arquivos criados/modificados

| Arquivo | Descrição |
|---------|-----------|
| `compose.yaml` | Configuração completa do Docker Compose com PostgreSQL e Flask |
| `Dockerfile` | Image otimizada com health check e variáveis de ambiente |
| `.env.example` | Template de variáveis de ambiente |
| `.dockerignore` | Otimização do build (ignora arquivos desnecessários) |
| `DOCKER_COMPOSE.md` | Documentação detalhada |
| `docker-helpers.sh` | Script auxiliar com comandos úteis |
| `docker-entrypoint.sh` | Script de inicialização do container |

---

## 🛠️ Comandos úteis

### Com script auxiliar (recomendado)
```bash
./docker-helpers.sh up              # Iniciar
./docker-helpers.sh down            # Parar
./docker-helpers.sh logs            # Ver logs
./docker-helpers.sh shell-web       # Acessar shell da app
./docker-helpers.sh shell-db        # Acessar PostgreSQL
./docker-helpers.sh test            # Rodar testes
./docker-helpers.sh migrate         # Executar migrations
./docker-helpers.sh restart         # Reiniciar tudo
./docker-helpers.sh clean           # Limpar containers/volumes
```

### Com docker-compose diretamente
```bash
docker-compose up -d                           # Iniciar
docker-compose down                            # Parar
docker-compose logs -f web                     # Ver logs
docker-compose exec web bash                   # Shell da app
docker-compose exec db psql -U vtasks_user     # Shell do DB
docker-compose exec web pytest -v              # Testes
docker-compose exec web flask db upgrade       # Migrations
```

---

## 🗄️ Serviços

### PostgreSQL (db)
- **Porta**: 5432
- **Usuário**: vtasks_user
- **Senha**: vtasks_password_dev
- **Database**: vtasks_db
- **Status**: Verificação de saúde a cada 10s

### Flask (web)
- **Porta**: 5000
- **Volume**: Código sincronizado para desenvolvimento
- **Depende de**: PostgreSQL saudável
- **Auto-init**: Executa migrations ao iniciar

---

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# Banco de dados
SQLALCHEMY_DATABASE_URI=postgresql://vtasks_user:vtasks_password_dev@db:5432/vtasks_db

# Segurança (MUDE EM PRODUÇÃO!)
SECRET_KEY=sua_chave_muito_forte_aqui

# Flask
FLASK_ENV=development
FLASK_APP=wsgi.py

# Cookies/Sessão
SESSION_PERMANENT=False
SESSION_COOKIE_SAMESITE=Strict
SESSION_COOKIE_HTTPONLY=True
```

---

## 📊 Status dos Serviços

```bash
# Ver containers em execução
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f web
docker-compose logs -f db
```

---

## 🐛 Troubleshooting

### PostgreSQL não conecta
```bash
# Verificar logs do DB
docker-compose logs db

# Verificar saúde
docker-compose exec db pg_isready -U vtasks_user -d vtasks_db
```

### Porta 5000 já em uso
Edite `compose.yaml`:
```yaml
ports:
  - "5001:5000"  # Use 5001 localmente
```

### Remover tudo e começar do zero
```bash
./docker-helpers.sh clean
# Ou manualmente:
docker-compose down -v
docker system prune -f
```

---

## 📚 Documentação Completa

Para mais detalhes, veja: **[DOCKER_COMPOSE.md](DOCKER_COMPOSE.md)**

---

## ✨ Recursos Implementados

✅ PostgreSQL com health check  
✅ Flask com hot-reload em desenvolvimento  
✅ Migrations automáticas  
✅ Volumes persistentes  
✅ Network isolada entre containers  
✅ Variáveis de ambiente configuráveis  
✅ Script auxiliar para operações comuns  
✅ Otimizações de build (`.dockerignore`)  
✅ Dockerfile otimizado (slim, cache)  
✅ Health checks em ambos serviços  
✅ Perfil de testes (opcional)  

---

## 🚀 Próximos passos

1. ✅ Configure suas variáveis em `.env`
2. ✅ Execute `./docker-helpers.sh up`
3. ✅ Acesse http://localhost:5000
4. ✅ Comece a desenvolver!

Boa sorte! 🎉
