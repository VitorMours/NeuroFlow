from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.models.task_model import Task 
from src.models.user_model import User
import importlib

class TestTaskRepository:
    
    def test_if_its_running(self) -> None:
        assert True

    def test_if_task_repository_class_is_importable(self) -> None:    
        module = importlib.import_module("src.repositories.task_repository")
        assert module is not None
        assert hasattr(module, "TaskRepository")

    def test_if_task_repository_is_callable(self) -> None:
        module = importlib.import_module("src.repositories.task_repository")
        assert module is not None
        assert callable(module.TaskRepository)

    def test_if_task_repository_have_the_standard_methods(self) -> None: 
        standard_methods = ["create","update","delete","get_all","get_by_email", "get_by_owner_id"]
        repository = TaskRepository()
        for method in standard_methods:
            assert hasattr(repository, method)        

    def test_if_repository_has_str_and_repr_representation(self, app) -> None: 
        with app.app_context():
            repository = TaskRepository()
            assert str(repository) == "<TaskRepository>"
            assert repr(repository) == "<TaskRepository>"

    def test_creating_task(self, app, create_random_user_dict, create_random_task_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            created_task = TaskRepository.create(create_random_task_dict, new_user.id)
            assert created_task

    def test_if_creating_task_return_task(self, app, create_random_user_dict, create_random_task_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            created_task = TaskRepository.create(create_random_task_dict, new_user.id)
            assert isinstance(created_task, Task)

    def test_if_can_create_and_search_for_user_tasks(self, app, create_random_user_dict, create_random_task_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            created_task = TaskRepository.create(create_random_task_dict, new_user.id)
            assert isinstance(created_task, Task)
            tasks = TaskRepository.get_by_owner_id(new_user.id)
            assert isinstance(tasks, list)
