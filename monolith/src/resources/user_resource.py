from typing import List
from flask import request
from flask_restx import Namespace, Resource

from src.models.task_model import Task
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService
from ..services.user_service import UserService
from ..utils.api import single_task_serializer, task_serializer, user_serializer, single_user_serializer
from .api_models import user_model, user_model_creation, user_model, task_model, task_model_creation
from src.models.user_model import User as Q
bp = Namespace("user", description="Api resource to access the users data")

user_entity = bp.model("User", user_model)
user_entity_creation = bp.model("UserCreation", user_model_creation)
user_entity_updating = bp.model("UserUpdating", user_model_creation)
task_entity = bp.model("Task", task_model)
task_entity_creation = bp.model("TaskCreation", task_model_creation)
 


@bp.route("/")
@bp.response(404, "User not found")
@bp.response(405, "HTTP Method not allowed")
class UserList(Resource):
    """Resource to get the data based on the user and the user uuid"""
    @bp.doc("Get all the users data")
    @bp.marshal_list_with(user_entity)
    def get(self):
        """Get all the users in database"""
        users = UserService.get_all_users()
        return user_serializer(users)

    @bp.doc("Create a new user with body data")
    @bp.expect(user_entity_creation)
    def post(self):
        """Creating user with json in the database"""
        payload = request.json
        user = UserService.create_user(payload)
        if isinstance(user, Exception):
            return {"message": str(user)}, 400
        if not user:
            return {"message": "Erro ao criar usuário"}, 400
        user_serialized = single_user_serializer(user)
        return {"new_user": user_serialized}, 201
    
    
@bp.route("/<uuid:uuid>")
@bp.param("uuid", "The user identifier")
@bp.response(404, "User not found")
@bp.response(200, "OK")
@bp.response(204, "No content in the request")
class User(Resource):
    
    @bp.doc("Get a specific user by the id")
    def get(self, uuid):
        """Get user by uuid"""
        user_id_str = str(uuid)

        user = UserService.get_user_by_uuid(user_id_str)
        if not user:
            return {"message": "User not found"}, 404

        user_serialized = single_user_serializer(user)
        return {"user": user_serialized}, 200

    @bp.doc("Updating user with new data based on the id")
    @bp.expect(user_entity_updating)
    def patch(self, uuid):
        payload = request.json
        user = UserService.get_user_by_uuid(str(uuid))
        
        if isinstance(user, Exception):
            return {"message": str(user)}, 400
        if not user:
            return {"message": "This user does not have been registered"}, 404
        
        new_user = UserService.update_user(user, payload)
        user_serialized = single_user_serializer(new_user)
        return {"updated_user": user_serialized}, 200

    
    
    


    
@bp.route("/<uuid:user_id>/todo")
@bp.response(404, "tasks not found")
@bp.response(200, "Tasks finded")
class UserTasksList(Resource):
    """Manejar as tasks de um determinado usuario por meio do id de identificacao dele"""
    def get(self, user_id) -> List[Task]:
        """Pegar as tasks que sao de um determinado usuario"""
        user = UserService.get_user_by_uuid(str(user_id))
        if not user:
            return {"message": "User not found"}, 404

        tasks = TaskService.get_user_tasks(user.email)
        tasks_serialized = task_serializer(tasks)
        return tasks_serialized

    @bp.expect(task_entity)
    def put(self) -> None:
        """NAO IMPLEMENTADO"""
        
        user = UserService.get_user_by_uuid(bp.payload["user_id"])
        if not user:
            return {"message": "User not found"}, 404

        task = Task(
            task=bp.payload["task"],
            task_description=bp.payload["task_description"],
            task_conclusion=False,
            user_id=bp.payload["user_id"]
        )
        TaskRepository.create(task)

        return single_task_serializer(task)
    
    
    