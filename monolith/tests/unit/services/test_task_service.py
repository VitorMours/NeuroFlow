import inspect 
import importlib 
import pytest

class TestTaskService:  
    def test_if_is_running(self) -> None:
        assert True

    def test_if_task_service_can_be_imported(self) -> None:
        module = importlib.import_module("src.services.task_service")
        print(module)
        assert hasattr(module, "TaskService")
    
    @pytest.mark.skip()
    def test_if_can_string_representation_of_the_service(self) -> None:
        module = importlib.import_module("src.services.task_service")
        class_ = module.TaskService()    
        assert str(class_) == "<TaskService>"

    def test_if_service_can_create_task(self, app, create_user_repository, 
                                        create_random_user_dict, 
                                        create_auth_service, 
                                        create_random_task_dict
                                        ) -> None:
        with app.test_request_context(): 
            module = importlib.import_module("src.services.task_service")
            entity = importlib.import_module("src.models.task_model")
            class_ = module.TaskService    
            user = create_user_repository.create(create_random_user_dict)
            create_auth_service.create_session(user)
            task = class_.create(create_random_task_dict)
            assert type(task) is entity.Task

    def test_if_service_can_get_all_tasks_with_empty_database(self, app) -> None:
        with app.test_request_context():
            module = importlib.import_module("src.services.task_service")
            class_ = module.TaskService 
            tasks = class_.get_all()
            assert len(tasks) == 0

    def test_if_service_can_get_all_tasks_with_tasks_in_database(self, app, create_random_user_dict, 
                                                                 create_user_repository, 
                                                                 create_random_task_dict,
                                                                 create_auth_service
                                                                 ) -> None:
        with app.test_request_context():
            module = importlib.import_module("src.services.task_service")
            entity = importlib.import_module("src.models.task_model")
            class_ = module.TaskService
            user = create_user_repository.create(create_random_user_dict)
            create_auth_service.create_session(user)
            for _ in range(3):
                class_.create(create_random_task_dict)
            tasks = class_.get_all()
            for task in tasks: 
                assert type(task) is entity.Task

    def test_if_service_can_get_all_user_tasks_in_the_database(self, app, create_random_user_dict, 
                                                               create_user_repository, 
                                                               create_random_task_dict,
                                                               create_auth_service
                                                               ) -> None:
        with app.test_request_context():
            module = importlib.import_module("src.services.task_service")
            entity = importlib.import_module("src.models.task_model")
            class_ = module.TaskService 
            user = create_user_repository.create(create_random_user_dict)
            create_auth_service.create_session(user)
            for _ in range(4):
                class_.create(create_random_task_dict)
            tasks = class_.get_user_tasks(user.email)
            for task in tasks:
                assert task.user_id == user.id



