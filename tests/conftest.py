import sys
import os
import pytest
from faker import Faker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models import db
from src.repositories.user_repository import UserRepository
from src.models.user_model import User
from wsgi import create_app

@pytest.fixture()
def app():
    faker = Faker()
    app = create_app("testing")

    with app.app_context():
        db.drop_all()
        db.create_all()
        for _ in range(25):
            user = User(
                first_name = faker.name(),
                last_name = faker.last_name(),
                email = faker.unique.email(),
                password = faker.password()
            )
        
            db.session.add(user)
            db.session.commit()

        yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def create_default_static_user():
    return User(
        first_name="Lucas",
        last_name="Moura",
        email="lucas.moura@email.com",
        password="32322916aA!",
    )
    

@pytest.fixture
def create_second_user():
    return User(
        first_name="John",
        last_name="Doe",
        email="john.doe@email.com",
        password="32322916aA!",
    )

@pytest.fixture
def create_random_user():
    faker = Faker()
    return User(
        first_name = faker.name(),
        last_name = faker.name(),
        email = faker.unique.email(),
        password = faker.password()
    )

@pytest.fixture
def create_random_user_dict():
    faker = Faker()
    return {
        "first_name":faker.name(),
        "last_name":faker.name(),
        "email":faker.unique.email(),
        "password":faker.password()
    }
    
    
@pytest.fixture
def create_random_task_dict():
    faker = Faker()
    return {
        "task":faker.name(),
        "task_description":faker.text(),
        "task_conclusion":faker.boolean(),
        "user": User()
    }

@pytest.fixture
def create_user_repository():
    return UserRepository()