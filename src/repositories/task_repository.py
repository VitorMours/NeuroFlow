from ..models import db
from typing import List 
from src.models.task_model import Task
from src.models.user_model import User

class TaskRepository:
    
    @staticmethod 
    def create(task_data: dict, user_id: User) -> None:
        """
        Create a new task in the database based on the user as the foreign key.
        """
        needed_fields = ["task","task_description","task_conclusion"]
        
        for field in needed_fields:
            if field not in task_data.keys():
                return False

        new_task = Task(
                task = task_data["task"],
                task_description = task_data["task_description"],
                task_conclusion = task_data["task_conclusion"],
                user_id = user_id
                )
        return new_task
    
    @staticmethod   
    def update() -> None:
        pass
    @staticmethod
    def delete() -> None:
        pass
    
    @staticmethod
    def get_all(user: User) -> None:
        pass
    
    @staticmethod
    def get_by_email() -> None:
        pass
    
    @staticmethod 
    def get_by_owner_id(id: str) -> None:
        tasks = Task.query.filter_by(user_id=id).all()
        return tasks

    def __repr__(self) -> str:
        return "<TaskRepository>"

    def __str__(self) -> str:
        return "<TaskRepository>"
