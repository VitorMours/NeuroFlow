from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from pathlib import Path
import os
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

dotenv_file = Path(".env")
load_dotenv(dotenv_path=dotenv_file)

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

    # Create only missing tables: if all tables already exist, skip creating.
    with app.app_context():
        try:
            from sqlalchemy import inspect
            
            # Tenta conectar e inspecionar
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            app.logger.info(f"Existing tables: {existing_tables}")
            
            required_tables = list(db.metadata.tables.keys())
            app.logger.info(f"Required tables: {required_tables}")
            
            missing = [t for t in required_tables if t not in existing_tables]
            
            if missing:
                app.logger.info(f"Missing tables detected: {missing}. Creating...")
                try:
                    db.create_all()
                    app.logger.info("Missing tables created successfully.")
                except Exception as create_error:
                    app.logger.error(f"Failed to create tables: {create_error}")
                    # Não levante o erro - apenas registre
            else:
                app.logger.info("All tables already exist. Skipping create_all().")
                
        except Exception as e:
            # Se a inspeção falhar, apenas registre o erro mas NÃO tente criar tabelas
            app.logger.warning(f"Table inspection failed: {e}")
            app.logger.info("Assuming tables already exist or will be created via migrations.")
            # NÃO chame db.create_all() aqui!
    
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