from abc import ABC, abstractmethod
from src.models.user_model import User
class AuthServiceInterface(ABC):

    @staticmethod
    @abstractmethod
    def create_session(user: User) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def destroy_session():
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def check_session():
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def logout_user() -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def login_user(user_data: dict) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def authenticate_user(user_data: dict) -> None:
        raise NotImplementedError()
