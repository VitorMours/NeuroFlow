from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from pathlib import Path
import os
import time
import logging
from flask_admin import Admin
from flask_pagedown import PageDown
from src.models import db
from flask_migrate import Migrate
from src.models.user_model import User
from src.models.task_model import Task
from src.models.note_model import Note
from src.views.admin import AdminView, admin_add_views
from src.views import bp
from src.resources import api_bp
from config import config

logger = logging.getLogger(__name__)

dotenv_file = Path(".env")
load_dotenv(dotenv_path=dotenv_file)

def initialize_database(app, max_retries=10, retry_delay=2):
    """
    Tenta conectar ao banco de dados e criar as tabelas que não existem.
    Faz retry até conseguir ou alcançar o máximo de tentativas.
    
    Args:
        app: A aplicação Flask
        max_retries: Número máximo de tentativas
        retry_delay: Delay em segundos entre tentativas
    """
    attempt = 0
    
    while attempt < max_retries:
        try:
            attempt += 1
            app.logger.info(f"Tentativa {attempt}/{max_retries} de conectar ao banco de dados...")
            
            with app.app_context():
                from sqlalchemy import inspect, text
                
                # Testa conexão com o banco
                db.session.execute(text('SELECT 1'))
                app.logger.info("✅ Conexão com banco de dados estabelecida!")
                
                # Inspeciona tabelas existentes
                inspector = inspect(db.engine)
                existing_tables = inspector.get_table_names()
                app.logger.info(f"📋 Tabelas existentes: {existing_tables}")
                
                required_tables = list(db.metadata.tables.keys())
                app.logger.info(f"📋 Tabelas requeridas: {required_tables}")
                
                missing = [t for t in required_tables if t not in existing_tables]
                
                if missing:
                    app.logger.info(f"⚠️  Tabelas faltando: {missing}. Criando...")
                    db.create_all()
                    app.logger.info("✅ Tabelas criadas com sucesso!")
                else:
                    app.logger.info("✅ Todas as tabelas já existem!")
                
                return True
                
        except Exception as e:
            app.logger.warning(f"❌ Tentativa {attempt} falhou: {type(e).__name__}: {str(e)}")
            
            if attempt < max_retries:
                app.logger.info(f"⏳ Aguardando {retry_delay}s antes de tentar novamente...")
                time.sleep(retry_delay)
            else:
                app.logger.error(f"❌ Falha ao conectar após {max_retries} tentativas!")
                raise RuntimeError(f"Não foi possível inicializar o banco de dados após {max_retries} tentativas: {str(e)}")
    
    return False

def create_app(config_name: str) -> Flask:
    app = Flask(__name__, template_folder="src/templates/pages")
    app.config.from_object(config[config_name])

    print(f"✅ Using database: {app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0]}")  # Debug

    pagedown = PageDown()
    pagedown.init_app(app)

    @app.context_processor
    def inject_pagedown():
        return dict(pagedown=pagedown)

    def render_http_error(error):
        code = getattr(error, 'code', 500)
        return render_template("error.html", error=error, code=code), code

    for err_code in [404, 405, 500]:
        app.register_error_handler(err_code, render_http_error)

    # Adding template extensions
    app.jinja_env.add_extension('jinja2.ext.do')
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Inicializa o banco de dados com retry
    initialize_database(app)
    
    admin = Admin(index_view=AdminView())
    admin_add_views(admin, [User, Task, Note])
    admin.init_app(app)
    app.register_blueprint(bp)
    app.register_blueprint(api_bp)

    # Health check route
    @app.route('/health')
    def health_check():
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            return jsonify({
                'status': 'healthy', 
                'database': 'connected',
                'environment': config_name
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy', 
                'error': str(e),
                'environment': config_name
            }), 500

    return app

try:
    app = create_app(os.getenv("FLASK_ENV", "production"))
except Exception:
    # If creating the app at import time fails, log and re-raise to ensure
    # the container / process exits with a clear error message.
    import logging
    logging.exception("Failed to create application during import")
    raise


if __name__ == "__main__":

    config_name = os.getenv("FLASK_ENV", "development")
    app = create_app(config_name)
    app.run(host="0.0.0.0", port=5000)