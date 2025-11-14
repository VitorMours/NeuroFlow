from flask import Flask, render_template
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
load_dotenv(dotenv_path = dotenv_file)

def create_app(config_name: str) -> Flask:
    app = Flask(__name__, template_folder="src/templates/pages")
    app.config.from_object(config[config_name])

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
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()
    admin = Admin()
    admin_add_views(admin, [User, Task, Note])
    admin.init_app(app)
    app.register_blueprint(bp)
    app.register_blueprint(api_bp)

    return app


config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)
app.run()
