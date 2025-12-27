import pytest
import importlib
from abc import ABC
from src.interfaces.user_service_interface import UserServiceInterface

class TestUserServiceInterface:
    def test_user_service_interface_import(self) -> None:
        module = importlib.import_module("src.interfaces.user_service_interface")
        assert module is not None
        assert hasattr(module, "UserServiceInterface")

    def test_user_service_interface_is_abstract_class(self) -> None:
        assert issubclass(UserServiceInterface, ABC)

    def test_if_user_service_interface_have_abstract_methods(self) -> None:
        methods_list = ["create_user","get_all_users","update_user","delete_user"]
        interface = UserServiceInterface
        for method in methods_list:
            assert hasattr(interface, method)

    def test_if_service_interface_have_abstract_methods(self) -> None:
        interface = UserServiceInterface
        for method in interface.__abstractmethods__:
            assert hasattr(interface, method)

    def test_if_calling_method_raises_error(self) -> None:
        class UserService(UserServiceInterface):
            pass

        service = UserService
        user_data = {"name": "John", "email": "john@example.com"}
        user_id = 123

        with pytest.raises(NotImplementedError):
            service.create_user(data=user_data)

        with pytest.raises(NotImplementedError):
            service.get_all_users()


        with pytest.raises(NotImplementedError):
            service.update_user(user=user_id, data=user_data)

        with pytest.raises(NotImplementedError):
            service.delete_user(data={"user_id": user_id})