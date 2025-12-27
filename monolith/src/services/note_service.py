from flask import session
from src.interfaces.note_service_interface import NoteServiceInterface
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.utils.erros import AuthenticationError
from src.repositories.note_repository import NoteRepository
from src.repositories.user_repository import UserRepository
from src.models.note_model import Note
from uuid import uuid4

class NoteService(NoteServiceInterface):
    
    @staticmethod
    def create_note(note_data: dict[str, str], user_id: str | None =None) -> Note:
        if user_id is None:
            if not AuthService.check_session():
                raise AuthenticationError("User not authenticated")
            user_email = session.get("email")
            user = UserRepository.get_by_email(user_email)            
        else:
            user = UserRepository.get_by_uuid(user_id)
                        
        return NoteRepository.create(note_data, user)

    @staticmethod
    def update_note() -> None:
        pass

    @staticmethod
    def get_user_notes(as_json: bool = False, user_id: str = None, user_email: str = None) -> None:
        notes = None
        try: 
            if not (user_id is None):
                notes = NoteRepository.get_by_user_uuid(user_uuid=user_id)
            elif not (user_email is None):
                user = UserRepository.get_by_email(user_email)
                if user is None:
                    raise AuthenticationError("User not found")
                notes = NoteRepository.get_by_user_uuid(user_uuid=user.id)
            
            return notes
        except Exception as e:
            return e

    @staticmethod
    def update_user_note() -> None:
        pass

    @staticmethod
    def delete_user_note() -> None:
        pass


    def __str__(self) -> None:
        return "<NoteService>"
