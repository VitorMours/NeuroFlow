import pytest
import importlib
import inspect
from src.models.note_model import Note
from src.models.user_model import User
from src.interfaces.note_service_interface import NoteServiceInterface
from src.repositories.user_repository import UserRepository
from src.services.note_service import NoteService

class TestNoteService:
    def test_if_is_running(self) -> None:
        assert True

    def test_if_can_import_note_service(self) -> None:
        module = importlib.import_module("src.services.note_service")
        assert hasattr(module, "NoteService")

    def test_if_note_service_class_has_note_service_interface(self) -> None:
        module = importlib.import_module("src.services.note_service")
        class_ = module.NoteService
        assert issubclass(class_, NoteServiceInterface)


    def test_if_note_service_create_note_have_correct_parameters(self, app, create_random_user_dict, create_random_note_dict) -> None:
        needed_fields = ["note_data","user_id"]
        module = importlib.import_module("src.services.note_service")
        class_ = module.NoteService
        signature = inspect.signature(class_.create_note)

        for field in needed_fields:
            assert field in signature.parameters.keys()


    def test_if_can_create_note_with_note_service(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.test_request_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            new_note = NoteService.create_note(create_random_note_dict, new_user.id)
            assert new_note

    def test_if_can_call_note_service(self) -> None:
        module = importlib.import_module("src.services.note_service")
        class_ = module.NoteService
        instance = class_()
        assert str(instance) == "<NoteService>"  # Se tiver __str__ definido


    def test_if_get_user_notes_method_is_defined(self) -> None:
        module = importlib.import_module("src.services.note_service")
        class_ = module.NoteService 
        assert hasattr(class_, "get_user_notes")
        method = getattr(class_, "get_user_notes")
        assert callable(method)
    
    def test_if_get_user_notes_method_has_correct_parameters(self) -> None:
        needed_fields = ["as_json", "user_id", "user_email"]
        module = importlib.import_module("src.services.note_service")
        class_ = module.NoteService 
        method = getattr(class_, "get_user_notes")
        signature = inspect.signature(method)
        
        for field in needed_fields:
            assert field in signature.parameters.keys()
            
            
    def test_if_get_user_notes_method_returns_none_if_none_parameter(self) -> None:
        module = importlib.import_module("src.services.note_service")
        class_ = module.NoteService 
        method = getattr(class_, "get_user_notes")
        result = method()
        assert result is None
        
    def test_if_can_get_user_notes_with_email(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.test_request_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            new_note = NoteService.create_note(create_random_note_dict, new_user.id)
            assert isinstance(new_note, Note)
            notes = NoteService.get_user_notes(user_email=new_user.email)
            assert isinstance(notes, list)
    
    
    def test_if_can_get_multiple_user_notes_with_email(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.test_request_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            new_note = NoteService.create_note(create_random_note_dict, new_user.id)
            new_note = NoteService.create_note(create_random_note_dict, new_user.id)
            new_note = NoteService.create_note(create_random_note_dict, new_user.id)
            assert isinstance(new_note, Note)
            notes = NoteService.get_user_notes(user_email=new_user.email)
            assert isinstance(notes, list)
            assert len(notes) == 3 
            
            for note in notes:
                assert isinstance(note, Note)
        