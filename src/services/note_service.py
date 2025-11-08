from src.interfaces.note_service_interface import NoteServiceInterface
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.utils.erros import AuthenticationError
from uuid import uuid4

class NoteService(NoteServiceInterface):
    
    @staticmethod
    def create_note(note_data: dict[str, str], user_id: str) -> None:
        if AuthService.check_session():
             # if UserRepository.get_ gettar user by id
            pass
        else:
            raise AuthenticationError("User need to be authenticated")

    @staticmethod
    def update_note() -> None:
        pass

    @staticmethod
    def get_user_notes() -> None:
        pass

    @staticmethod
    def update_user_note() -> None:
        pass

    @staticmethod
    def delete_user_note() -> None:
        pass


    def __str__(self) -> None:
        return "<NoteService>"
