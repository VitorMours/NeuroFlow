import os
from pathlib import Path
from dotenv import load_dotenv

dotenv = Path(".env")
load_dotenv(dotenv_path=dotenv)

class Config:
    """Configurações base da aplicação."""
    SECRET_KEY = os.getenv("SECRET_KEY") or "uma_chave_padrao_fortissima"
    SESSION_PERMANENT = os.getenv("SESSION_PERMANENT") == "True"
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE") or "Strict"
    SESSION_COOKIE_HTTPONLY = os.getenv("SESSION_COOKIE_HTTPONLY") == "True"
    MONGO_URI = os.getenv("MONGO_URI") or "CHANGE-ME"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #FLASK_ADMIN_SWATCH = 'minty'
    FLASK_ADMIN = 'jvrezendemoura@gmail.com'

    @staticmethod
    def init_app(app):
        """Método de inicialização para extensões de aplicação."""
        pass


class DevelopmentConfig(Config):
    """Configurações para o ambiente de desenvolvimento."""
    # Use MySQL em desenvolvimento também
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or \
        "mysql+pymysql://neuroflow_user:neuroflow_password_dev@db:3306/neuroflow_db"


class TestConfig(Config):
    TESTING=True
    """Configurações para o ambiente de produção."""
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"



class ProductionConfig(Config):
    """Configurações para o ambiente de produção."""
    # Force MySQL em produção com fallback explícito
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or \
        "mysql+pymysql://neuroflow_user:neuroflow_password_dev@db:3306/neuroflow_db"


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': ProductionConfig  # Mude para Production como padrão
}