from flask import request
from typing import List
from flask_restx import Namespace, Resource, fields
from ..models.task_model import Task
from ..services.user_service import UserService
from ..services.task_service import TaskService
from ..repositories.task_repository import TaskRepository
from ..utils.api import single_task_serializer, task_serializer
from .api_models import task_model, task_model_creation

bp = Namespace("todo", description="Endpoint to manage the tasks")


task_entity = bp.model("Task", task_model)
task_entity_creation = bp.model("TaskCreation", task_model_creation)
 
@bp.route("/")
@bp.response(404, "tasks not found")
@bp.response(201, "Task Created")
@bp.response(200, "Tasks finded")
class TasksList(Resource):
    def get(self) -> List[Task]:
        """Pegar todas as tasks da base de dados"""
        tasks = TaskService.get_all()
        tasks_serialized = task_serializer(tasks)
        return tasks_serialized

    @bp.expect(task_entity_creation)
    def post(self) -> None:
        """Criar uma task com base no body do request"""
        payload = request.json
        user = UserService.get_user_by_uuid(payload["user_id"])
        if not user:
            return {"message": "User not found"}, 404

        task = TaskService.create(payload, payload["user_id"])

        return single_task_serializer(task)


@bp.route("/<uuid:uuid>")
@bp.response(404, "Task not found")
@bp.response(200, "Task finded")
class Tasks(Resource):
    """Manejar as tasks"""
    def get(self, uuid) -> List[Task]:
        """Pegar uma determinada task"""
        str_uuid = str(uuid)
        tasks = TaskService.get_one_by_uuid(str_uuid)

        tasks_serialized = single_task_serializer(tasks)
        return tasks_serialized

    @bp.expect(task_entity)
    def put(self) -> None:
        """NAO IMPLEMENTADO"""
        payload = request.json
        task = TaskService.get_one_by_uuid(payload["uuid"])
        
        if not task:
            return {"message": "Task not found"}, 404

        task = Task(
            task=payload["task"],
            task_description=payload["task_description"],
            task_conclusion=False,
            user_id=payload["user_id"]
        )
        # TaskRepository.create(task)

        return single_task_serializer(task)
    
    
    
