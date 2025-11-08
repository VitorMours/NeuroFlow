from abc import ABC
from typing import List, Optional
from ..utils.erros import IncorrectUserDataError
from ..interfaces.user_service_interface import UserServiceInterface
from src.models.user_model import User
from src.utils.security import check_password, encrypt_password
from src.repositories.user_repository import UserRepository
from collections.abc import Hashable
from flask import session
from src.utils.security import email_validator

class UserService(UserServiceInterface):

    @staticmethod
    def create_user(data) -> bool | IncorrectUserDataError:
        """
        Função que verifica os dados do dicionario que é passado,
        e caso estejam corretos usa para criar um usuário por meio do
        UserRepository
        """


        if 'password' in data:
            senha_plana = data['password']
            senha_hash = encrypt_password(senha_plana)  # Usando sua função de segurança
            data['password'] = senha_hash  # Substitui a senha plana pelo hash

        user = UserRepository.create(data)

        return user


    @staticmethod
    def get_all_users() -> None:
        all_users = UserRepository.get_all()
        return all_users

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """
        Busca um usuário pelo ID
        
        Args:
            user_id (str): ID do usuário a ser buscado
        
        Returns:
            User | None: Retorna o objeto User se encontrado, None caso contrário
        """
        user = UserRepository.get_by_email(email) 
        return user

    @staticmethod
    def update_user(user, data) -> None:
        pass

    @staticmethod
    def delete_user(data) -> None:
        pass
    


    @staticmethod
    def get_user_by_uuid(uuid: str) -> User | None:
        return UserRepository.get_by_uuid(uuid)
    
    @staticmethod
    def exists(user: User | str) -> bool | None:
        """
        Check if user exists
        """
        try:
            if type(user) == User:
                email = user.email
                if UserRepository.get_by_email(email): #type: ignore
                    return True

            elif type(user) == str and email_validator(user):
                if UserRepository.get_by_email(user):
                    return True
            else:
                raise TypeError
        except Exception as e:
            raise e

    def __str__(self) -> str:
        return "<UserService>"
