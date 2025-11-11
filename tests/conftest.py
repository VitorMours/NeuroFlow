import sys
import os
import pytest

# Configuração robusta do PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from faker import Faker
from src.models import db
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository
from src.models.user_model import User
from wsgi import create_app

@pytest.fixture()
def app():
    faker = Faker()
    
    try:
        app = create_app("testing")
    except Exception as e:
        pytest.fail(f"Erro ao criar app Flask: {e}")

    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            
            users = []
            for _ in range(25):
                user = User(
                    first_name=faker.first_name(), 
                    last_name=faker.last_name(),
                    email=faker.unique.email(),
                    password=faker.password(length=12)
                )
                users.append(user)
                db.session.add(user)
            
            db.session.commit()
            print(f"✓ Criados {len(users)} usuários de teste")
            
        except Exception as e:
            db.session.rollback()
            pytest.fail(f"Erro ao configurar banco de dados: {e}")

        yield app

        try:
            db.session.remove()
            db.drop_all()
        except Exception as e:
            print(f"Aviso no cleanup: {e}")

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def create_default_static_user():
    """Cria um usuário estático padrão para testes"""
    return User(
        first_name="Lucas",
        last_name="Moura",
        email="lucas.moura@email.com",
        password="32322916aA!",
    )

@pytest.fixture()
def create_second_user():
    """Cria um segundo usuário estático para testes"""
    return User(
        first_name="John",
        last_name="Doe",
        email="john.doe@email.com",
        password="32322916aA!",
    )

@pytest.fixture()
def create_random_user():
    """Cria um usuário com dados aleatórios"""
    faker = Faker()
    return User(
        first_name=faker.first_name(),  # Corrigido: name() -> first_name()
        last_name=faker.last_name(),
        email=faker.unique.email(),
        password=faker.password(length=12)
    )

@pytest.fixture()
def create_random_user_dict():
    """Cria um dicionário com dados de usuário aleatórios"""
    faker = Faker()
    return {
        "first_name": faker.first_name(),  # Corrigido: name() -> first_name()
        "last_name": faker.last_name(),
        "email": faker.unique.email(),
        "password": faker.password(length=12)
    }

@pytest.fixture()
def create_auth_service():
    """Cria uma instância do AuthService"""
    return AuthService()

@pytest.fixture()
def create_random_task_dict():
    """Cria um dicionário com dados de tarefa aleatórios"""
    faker = Faker()
    
    # Criar um usuário temporário para associar à tarefa
    temp_user = User(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.unique.email(),
        password=faker.password(length=12)
    )
    
    return {
        "task": faker.sentence(nb_words=3),  # Nome mais realista para tarefa
        "task_description": faker.text(max_nb_chars=200),
        "task_conclusion": faker.boolean(),
        "user": temp_user
    }
    
@pytest.fixture()
def create_random_note_dict():
    faker = Faker() 
    temp_user = User(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.unique.email(),
        password=faker.password(length=12)
    )
    return {
        "title":faker.sentence(nb_words=3),        
        "content":faker.text(),        
        "owner":temp_user,        
    }

@pytest.fixture()
def create_user_repository():
    """Cria uma instância do UserRepository"""
    return UserRepository()

@pytest.fixture()
def authenticated_client(client, create_default_static_user):
    """Client autenticado para testes que requerem login"""
    # Adiciona o usuário padrão ao banco
    try:
        db.session.add(create_default_static_user)
        db.session.commit()
        
        # Aqui você pode adicionar lógica de autenticação se necessário
        # Por exemplo, obter um token JWT e configurar no client
        
        return client
    except Exception as e:
        db.session.rollback()
        pytest.fail(f"Erro ao configurar client autenticado: {e}")

@pytest.fixture()
def database_session(app):
    """Fornece uma sessão de banco de dados para testes"""
    with app.app_context():
        yield db.session
        
        # Cleanup após cada teste que usar esta fixture
        db.session.rollback()