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
        standard_methods = ["create","update","delete","get_all","get_by_email"]
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
            tasks = TaskRepository.get_by_email(new_user.email)
            assert isinstance(tasks, list)

    def test_if_can_return_all_tasks(self, app) -> None:
        with app.app_context(): 
            tasks = TaskRepository.get_all()
            assert isinstance(tasks, list)
        
    def test_if_get_all_return_empty_list_when_no_tasks(self, app) -> None:
        with app.app_context():
            tasks = TaskRepository.get_all()
            assert isinstance(tasks, list)
            assert len(tasks) == 0

    def test_if_return_list_when_task_exists(self, app, create_user_repository, create_random_user_dict) -> None:
        with app.app_context():
            user_repository = UserRepository.create(create_random_user_dict)
            created_task = TaskRepository.create({
                "task": "Test Task",
                "task_description": "This is a test task",
                "task_conclusion": True
            }, user_repository.id)
            tasks = TaskRepository.get_all()
            assert isinstance(tasks, list)
            assert len(tasks) > 0
            assert isinstance(tasks[0], Task)            
            
    def test_if_can_get_task_by_user_email(self, app, create_random_user_dict) -> None:
        with app.app_context():
            user_repository = UserRepository.create(create_random_user_dict)
            created_task = TaskRepository.create({
                "task": "Test Task",
                "task_description": "This is a test task",
                "task_conclusion": True
            }, user_repository.id)
            user_task = TaskRepository.get_by_email(user_repository.email)
            assert isinstance(user_task[0], Task)
            assert user_task[0] == created_task
            
    def test_can_delete_task_that_exists_in_the_database(self, app, create_user_repository, create_random_user_dict) -> None:
        with app.app_context():
            user_repository = UserRepository.create(create_random_user_dict)
            created_task = TaskRepository.create({
                "task": "Test Task",
                "task_description": "This is a test task",
                "task_conclusion": True
            }, user_repository.id)
            user_task = TaskRepository.get_by_email(user_repository.email)
            assert TaskRepository.delete(user_task[0].id)

    