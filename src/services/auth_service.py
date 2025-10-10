from ..interfaces.auth_service_interface import AuthServiceInterface
from .user_service import UserService
from ..repositories.user_repository import UserRepository
from src.models.user_model import User
from src.utils import security
from src.utils.erros import (
    UserAlreadyExistsError,
    UserDoesNotExistsError,
    IncorrectCredentialsToLoginError,
)

from flask import session, redirect, url_for, flash


class AuthService(AuthServiceInterface):

    @staticmethod
    def check_session() -> bool:

        if session.get("login") is None:
            return False
        elif session.get("email") is None:
            return False
        return True

    @staticmethod
    def create_session(user: User) -> None:
        session["email"] = user.email
        session["username"] = f"{user.first_name} {user.last_name}"
        session["login"] = True
        return True

    @staticmethod
    def destroy_session() -> None:
        return True

    @staticmethod
    def login_user(user_data: dict) -> bool:
        user_email = user_data["email"]
        user = UserRepository.get_by_email(user_email)

        if user is None:
            return False

        AuthService.create_session(user)
        return True

    @staticmethod
    def logout_user() -> bool:
        if AuthService.check_session():
            AuthService.destroy_session()
            return True
        return False

    @staticmethod
    def authenticate_user(user_data: dict) -> bool:
        user_email = user_data["email"]
        if UserRepository.get_by_email(user_email) is not None:
            return True

    @staticmethod
    def check_password(
        password: str, confirmation: str
    ) -> bool | IncorrectCredentialsToLoginError:
        if password == confirmation:
            return True
        else:
            raise IncorrectCredentialsToLoginError(
                "A senha e a contrasenha possuem valores diferentes"
            )
