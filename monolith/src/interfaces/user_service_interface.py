from abc import abstractmethod, ABC
from src.models.task_model import Task
from src.models.user_model import User

class UserServiceInterface(ABC):

    @staticmethod
    @abstractmethod
    def create_user(data) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_all_users() -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def update_user(user, data) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def delete_user(data) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def exists(user: User) -> bool:
        raise NotImplementedError()
