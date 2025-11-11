from abc import ABC, abstractmethod
import json
from flask import session
from ..interfaces.task_service_interface import TaskServiceInterface
from ..services.user_service import UserService
from src.repositories.task_repository import TaskRepository
from src.models.task_model import Task

class TaskService(TaskServiceInterface):
    
    @staticmethod
    def get_all(as_json = False) -> Task | list[dict[str, str | bool]]:
        user_id = session.get("user_id")
        tasks = TaskRepository.get_all()
        if as_json:
            tasks_list = list()
            if not isinstance(tasks, dict):
                for task in tasks:
                    task_dict = task.to_json()
                    tasks_list.append(task_dict)
            return tasks_list
        return tasks

    @staticmethod
    def get_user_tasks(email: str) -> None:
        user = UserService.get_user_by_email(email)
        if not user:
            raise Exception("User not Found")

        all_tasks = TaskRepository.get_by_email(email)
        return all_tasks

    @staticmethod 
    def get_one_by_uuid(uuid: str) -> None:
        return TaskRepository.get_by_uuid(uuid) 


    @staticmethod
    def create(data: dict[str, str], user_id=None) -> None:
        
        if user_id is None:
            user = UserService.get_user_by_email(session.get("email"))
            if not user:
                raise Exception("User not found.")
                
            created_task = TaskRepository.create(
                task_data={
                    "task": data.get("task"),
                    "task_description": data.get("task_description"),
                    "task_conclusion": data.get("task_conclusion")
                },
                user_id=user.id  # O objeto User
            )
        else:
            created_task = TaskRepository.create(
                task_data={
                    "task": data.get("task"),
                    "task_description": data.get("task_description"),
                    "task_conclusion": data.get("task_conclusion")
                },
                user_id=user_id  # Apenas o ID, não o objeto User
            )
            
        return created_task
    
    @staticmethod
    def delete() -> None:
        pass

    @staticmethod
    def update(task_id: int, update_data: dict) -> None:
        try:
            if not task_id or not isinstance(task_id, str):
                raise ValueError("Invalid task ID")
            
            if not update_data or not isinstance(update_data, dict):
                raise ValueError("Invalid update data")
            
            filtered_data = {k: v for k, v in update_data.items() if v is not None}
            
            if not filtered_data:
                return False
            
            success = TaskRepository.update(task_id, filtered_data)
            
            return success
            
        except Exception as e:
            print(f"Error in TaskService.update: {str(e)}")
            return False

    @staticmethod
    def toggle_status() -> None:
        pass

    @staticmethod
    def check_owner() -> None:
        pass

    def __str__(self) -> None:
        return "<TaskService>"

    def __repr__(self) -> None:
        return "<TaskService>"
