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
from src.views.admin import admin_add_views
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

            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            required_tables = list(db.metadata.tables.keys())
            missing = [t for t in required_tables if t not in existing_tables]
            if missing:
                app.logger.info("Missing tables detected: %s. Creating...", missing)
                db.create_all()
            else:
                app.logger.info("All tables already exist. Skipping create_all().")
        except Exception:
            # If inspection fails for any reason, fall back to create_all to avoid startup failure.
            app.logger.exception("Table inspection failed; falling back to db.create_all().")
            db.create_all()
    
    admin = Admin()
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

# Force production environment no Docker
config_name = os.getenv('FLASK_ENV', 'production')
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)