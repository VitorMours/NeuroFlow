import pytest
from src.models.user_model import User
from src.models.task_model import Task

class TestTaskModel:
    def test_create_task(self, create_default_static_user) -> None:
        task_instance = Task(
                task = "Estudar Flask",
                task_description = "Estudar o framework Flask para desenvolver aplicações web",
                task_conclusion = False, 
                user = create_default_static_user
        )
        assert isinstance(task_instance, Task)
        
    def test_task_string_representation(self, create_default_static_user) -> None:
        task_instance = Task(
                task = "Estudar Flask",
                task_description = "Estudar o framework Flask para desenvolver aplicações web",
                task_conclusion = False,
                user = create_default_static_user
        )
        
        assert str(task_instance) == f"<{task_instance.user_id} -> {task_instance.task} {task_instance.task_conclusion}>"
        
    def test_get_task_name_and_description(self, create_default_static_user) -> None:
        task_instance = Task(
            task = "asd",
            task_description = "asd",
            task_conclusion = False,
            user = create_default_static_user
        )
        task_name = task_instance.task
        task_description = task_instance.task_description
        assert task_name == "asd"
        assert task_description == "asd"
        
        
    def test_modify_task_name_and_description(self, create_default_static_user) -> None:
        task_instance = Task(
            task = "Estudar Flask",
            task_description = "Estudar o framework Flask para desenvolver aplicações web",
            task_conclusion = False,
            user = create_default_static_user
        )
        task_instance.task = "Estudar FastAPI"
        task_instance.task_description = "Estudar o framework FastAPI para desenvolver APIs"
        assert task_instance.task == "Estudar FastAPI"
        assert task_instance.task_description == "Estudar o framework FastAPI para desenvolver APIs"
        
    def test_toggle_task_conclusion_status(self, create_default_static_user) -> None:
        task_instance = Task(
            task = "Estudar Flask",
            task_description = "Estudar o framework Flask para desenvolver aplicações web",
            task_conclusion = False,
            user = create_default_static_user
        )
        assert task_instance.task_conclusion == False
        task_instance.task_conclusion = True
        assert task_instance.task_conclusion == True
        task_instance.toggle_conclusion()
        assert task_instance.task_conclusion == False
        
    def test_get_task_owner(self, create_default_static_user) -> None:
        task_instance = Task(
            task = "Estudar Flask",
            task_description = "Estudar o framework Flask para desenvolver aplicações web",
            task_conclusion = False,
            user = create_default_static_user
        )
        assert task_instance.user == create_default_static_user
        assert isinstance(task_instance.user, User)
        
    def test_get_task_owner_id(self, create_default_static_user) -> None:
        task_instance = Task(
            task = "Estudar Flask",
            task_description = "Estudar o framework Flask para desenvolver aplicações web",
            task_conclusion = False,
            user = create_default_static_user
        )
        assert task_instance.user_id == create_default_static_user.id

    def test_modify_task_owner(self, create_default_static_user, create_second_user) -> None:
        task_instance = Task(
            task = "Estudar Flask",
            task_description = "Estudar o framework Flask para desenvolver aplicações web",
            task_conclusion = False,
            user = create_default_static_user
        )
        assert task_instance.user == create_default_static_user
    
    def test_get_task_description_content_type(self, create_default_static_user) -> None:
        task_instance = Task(
            task = "Estudar Flask",
            task_description = "Estudar o framework Flask para desenvolver aplicações web",
            task_conclusion = False,
            user = create_default_static_user
        )
        assert isinstance(task_instance.task_description, str)
        
    def test_get_task_description_content(self, create_default_static_user) -> None:
        task_instance = Task(
            task = "Estudar Flask",
            task_description = "Estudar o framework Flask para desenvolver aplicações web",
            task_conclusion = False,
            user = create_default_static_user
        )
        assert task_instance.task_description == "Estudar o framework Flask para desenvolver aplicações web"

