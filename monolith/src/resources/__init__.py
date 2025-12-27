from flask import Blueprint
from flask_restx import Api, fields
from .user_resource import bp as user
from .todo_resource import bp as todo

api_bp = Blueprint("api", __name__, url_prefix="/api")



api = Api(api_bp, title='neuroflows API', version='1.0', docs="/docs")

api.add_namespace(user)
api.add_namespace(todo)
