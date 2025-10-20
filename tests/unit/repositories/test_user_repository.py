import pytest
import importlib
from src.models.user_model import User
from src.repositories.user_repository import UserRepository
from src.utils.erros import UserDoesNotExistsError, IncorrectUserDataError
from faker import Faker

class TestUserRepository:
    def test_if_is_running(self) -> None:
        assert True

    def test_if_user_repository_can_be_imported(self):
        module = importlib.import_module("src.repositories.user_repository")
        assert module is not None
        assert hasattr(module, "UserRepository")

    def test_instantiate_user_repository(self) -> None:
        user_repository = UserRepository()
        assert user_repository is not None

    def test_user_repository_primitive_type(self) -> None:
        user_repository = UserRepository()
        assert isinstance(user_repository, UserRepository)

    def test_user_repository_str(self) -> None:
        user_repository = UserRepository()
        assert str(user_repository) == "<UserRepository>"


    def test_if_repository_have_only_the_correct_methods(self, create_user_repository) -> None:
        required_methods = [
            "create", "update", "delete",
            "get_all", "get_by_email", "get_by_uuid"
        ]
        for method_name in dir(create_user_repository):
            if method_name.startswith("__"):
                continue
            assert method_name in required_methods

    def test_if_repository_can_call_the_methods(self, create_user_repository) -> None:
        repository = create_user_repository
        required_methods = [
            "create", "update", "delete",
            "get_all", "get_by_email",
            "__str__"
        ]
        for method_name in required_methods:
            assert hasattr(repository, method_name), f"Missing method: {method_name}"
            assert callable(getattr(repository, method_name)), f"{method_name} is not a callable method"

    def test_if_get_all_return_only_users(self, app, create_user_repository) -> None:
        with app.app_context():
            query = create_user_repository.get_all()
            for user in query:
                assert isinstance(user, User)

    def test_if_can_create_user_with_repository(self, app, create_user_repository, create_random_user_dict) -> None:
        with app.app_context():
            create_user_repository.create(create_random_user_dict)
            searched_user = create_user_repository.get_by_email(create_random_user_dict["email"])
            assert create_random_user_dict["email"] == searched_user.email

    def test_if_can_find_user_in_database_by_email(self, app, create_user_repository, create_random_user_dict) -> None:
        with app.app_context():
            create_user_repository.create(create_random_user_dict)
            searched_user = create_user_repository.get_by_email(create_random_user_dict["email"])
            assert isinstance(searched_user, User)
            assert searched_user.email == create_random_user_dict["email"]

    def test_raising_error_when_not_finding_user(self, app, create_user_repository, create_random_user) -> None:
        with app.app_context():
            result = create_user_repository.get_by_email("never.exists@gmail.com")
            assert result == None

    def test_if_can_update_a_user_that_exists(self, app, create_user_repository, create_random_user_dict) -> None:

        faker = Faker()
        with app.app_context():
            create_user_repository.create(create_random_user_dict)
            searched_user = create_user_repository.get_by_email(create_random_user_dict["email"])
            new_email = faker.email()
            data = {"email":new_email}
            create_user_repository.update(searched_user, data=data)
            modified_user = create_user_repository.get_by_email(searched_user.email)
            assert modified_user.email == data["email"]

    def test_if_raise_error_with_wrong_key(self, app, create_user_repository, create_random_user_dict) -> None:
        with app.app_context():
            create_user_repository.create(create_random_user_dict)
            with pytest.raises(IncorrectUserDataError):
                searched_user = create_user_repository.get_by_email(create_random_user_dict["email"])
                create_user_repository.update(searched_user, {"dando":"errado"})


    def test_if_get_all_return_list_when_more_than_one(self, app, create_user_repository) -> None:
        with app.app_context():
            query = create_user_repository.get_all()
            assert len(query) >= 1
