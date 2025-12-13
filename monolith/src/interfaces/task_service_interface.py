from abc import ABC, abstractmethod
from typing import List 
from src.models.task_model import Task
from src.repositories.task_repository import TaskRepository
from flask import session

class TaskServiceInterface(ABC):

    @abstractmethod
    def get_all_user_tasks() -> List[Task]:
        pass
    
    @abstractmethod
    def delete() -> None:
        pass

    @abstractmethod
    def update() -> None:
        pass

    @abstractmethod
    def toggle_status() -> None:
        pass

    @abstractmethod
    def check_owner() -> None:
        pass

    @abstractmethod
    def get_one_by_id() -> None:
        pass

    @abstractmethod
    def create() -> None:
        pass


