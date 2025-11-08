import pytest
import importlib

from flask import session

from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.utils.erros import IncorrectCredentialsToLoginError

class TestAuthService:
    def test_is_running(self) -> None:
        assert True

    def test_service_have_check_session_method(self) -> None:
        module = importlib.import_module("src.services.auth_service")
        assert hasattr(module.AuthService, "check_session")
        assert callable(module.AuthService.check_session)

    def test_service_check_session_method_implementation(self, app, create_random_user) -> None:
        with app.app_context():
            with app.test_request_context():
                module = importlib.import_module("src.services.auth_service")
                assert module.AuthService.check_session

    def test_service_have_create_session_method(self) -> None:
        module = importlib.import_module("src.services.auth_service")
        assert hasattr(module.AuthService, "create_session")
        assert callable(module.AuthService.create_session)

    def test_service_create_session_method_implementation(self, app, create_random_user) -> None:
        with app.app_context():
            with app.test_request_context():
                module = importlib.import_module("src.services.auth_service")
                assert module.AuthService.create_session(create_random_user)

    def test_service_destroy_session_method(self) -> None:
        module = importlib.import_module("src.services.auth_service")
        assert hasattr(module.AuthService, "destroy_session")

    def test_service_destroy_session_method_implementation(self, app, create_random_user) -> None:
        with app.app_context():
            with app.test_request_context():
                module = importlib.import_module("src.services.auth_service")
                assert module.AuthService.destroy_session(create_random_user)

    def test_service_login_user_method(self) -> None:
        module = importlib.import_module("src.services.auth_service")
        assert hasattr(module.AuthService, "login_user")
    #
    # def test_service_login_user_method_implementation(self, app, create_random_user_dict) -> None:
    #     with app.app_context():
    #         with app.test_request_context():
    #             user = UserService.create_user(create_random_user_dict)
    #             module = importlib.import_module("src.services.auth_service")
    #             assert module.AuthService.login_user(user_data={"email":user.email})

    def test_service_logout_user_method(self) -> None:
        module = importlib.import_module("src.services.auth_service")
        assert hasattr(module.AuthService, "logout_user")

    def test_service_logout_user_method_implementation(self, app, create_random_user_dict) -> None:
        with app.app_context():
            with app.test_request_context():
                user = UserService.create_user(create_random_user_dict)
                module = importlib.import_module("src.services.auth_service")
                AuthService.login_user(create_random_user_dict)
                assert module.AuthService.logout_user()

    def test_service_logout_user_method_implementation_without_login(self, app, create_random_user_dict) -> None:
        with app.app_context():
            with app.test_request_context():
                UserService.create_user(create_random_user_dict)
                module = importlib.import_module("src.services.auth_service")
                #with pytest.raises(AssertionError):
                #    assert module.AuthService.logout_user()

    def test_service_authenticate_user_method(self) -> None:
        module = importlib.import_module("src.services.auth_service")
        assert hasattr(module.AuthService, "authenticate_user")

    def test_service_authenticate_user_method_implementation(self, app, create_random_user_dict, create_user_repository) -> None:
        with app.app_context():
            create_user_repository.create(create_random_user_dict)
            user_email = create_random_user_dict["email"]
            with app.test_request_context():
                module = importlib.import_module("src.services.auth_service")
                value = module.AuthService.authenticate_user({"email":user_email})
                print(value)
                assert True

    def test_service_check_password_user_method(self) -> None:
        module = importlib.import_module("src.services.auth_service")
        assert hasattr(module.AuthService, "check_password")

    def test_service_check_password_user_method_implementation(self, app) -> None:
        with app.app_context():
            module = importlib.import_module("src.services.auth_service")
            assert module.AuthService.check_password(password="123123123aA!", confirmation="123123123aA!")

    def test_service_check_password_raise_error_correctly(self) -> None:
        with pytest.raises(IncorrectCredentialsToLoginError):
            module = importlib.import_module("src.services.auth_service")
            assert module.AuthService.check_password(password="123123123aA!", confirmation="1231223123aA!")

    def test_if_can_create_user_session(self, app, create_random_user_dict) -> None:
        with app.app_context():
            with app.test_request_context():
                user_service = UserService()
                user_created = user_service.create_user(create_random_user_dict)
                if user_created:
                    user_entity = UserRepository.get_by_email(create_random_user_dict["email"])
                    AuthService.create_session(user_entity)

                    assert session["login"] == True

    def test_if_can_destroy_user_session(self, app, create_random_user_dict) -> None:
        with app.app_context():
            with app.test_request_context():
                user_service = UserService()
                user_created = user_service.create_user(create_random_user_dict)
                if user_created:
                    user_entity = UserRepository.get_by_email(create_random_user_dict["email"])
                    AuthService.create_session(user_entity)
                    assert session.get("login") is True

                    AuthService.destroy_session(user_entity)
                    assert session.get("login") is None
                        
                        
    def test_if_check_session_views_if_session_exists(self, app, create_random_user_dict) -> None:
        with app.app_context():
            with app.test_request_context():
                user_service = UserService()
                assert session.get("login") is None
                user_created = user_service.create_user(create_random_user_dict)
                #with pytest.raises(AssertionError):
                #    assert AuthService.check_session()
                if user_created:
                    user_entity = UserRepository.get_by_email(create_random_user_dict["email"])
                    AuthService.create_session(user_entity)
                    assert AuthService.check_session()
                    
