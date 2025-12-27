from flask import Blueprint, render_template, flash, redirect
from flask.views import MethodView
from .auth import bp as auth
from .home import bp as home
from ..models.user_model import User

from src.repositories.user_repository import UserRepository
bp = Blueprint("views", __name__)

class IndexView(MethodView):
    def get(self):
        return render_template("index.html")


bp.add_url_rule("/", view_func=IndexView.as_view("index"))
bp.register_blueprint(auth)
bp.register_blueprint(home)

