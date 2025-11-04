import importlib 
import inspect 
import pytest 
from src.models.user_model import User
from src.models.note_model import Note
from src.repositories.user_repository import UserRepository
from src.repositories.note_repository import NoteRepository
class TestNoteRepository:
    def verify_test_note_repository_is_running(self) -> None:
        assert True
        
    def test_if_can_import_the_repository_class(self) -> None:
        module = importlib.import_module("src.repositories.note_repository")   
        assert hasattr(module, "NoteRepository")
        
    def test_if_repository_is_callable(self) -> None:
        module = importlib.import_module("src.repositories.note_repository")
        assert module is not None
        assert callable(module.NoteRepository) 
                
    def test_if_can_print_repository(self) -> None:
        module = importlib.import_module("src.repositories.note_repository")
        class_ = module.NoteRepository()
        assert "<NoteRepository>" == str(class_)

    def test_if_can_represent_the_repository(self) -> None:
        module = importlib.import_module("src.repositories.note_repository")
        class_ = module.NoteRepository()
        assert "<NoteRepository>" == repr(class_)
        
    def test_if_can_create_note(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            new_note = NoteRepository.create(create_random_note_dict, new_user)
            assert isinstance(new_note, Note)
            
            
    def test_if_can_print_note(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            new_note = NoteRepository.create(create_random_note_dict, new_user)
            assert str(new_note) == f"{new_note.title}: {new_user.id}"
            
    def test_if_can_get_all_notes_with_empty_database(self, app) -> None:
        with app.app_context():
            notes = NoteRepository.get_all()
            print(notes)
            assert notes == []
            
    def test_if_can_get_all_notes_with_full_database(self, app, create_random_note_dict, create_random_user_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            
            NoteRepository.create(create_random_note_dict, new_user)
            NoteRepository.create(create_random_note_dict, new_user)
            NoteRepository.create(create_random_note_dict, new_user)
            
            notes_count = NoteRepository.get_all()  # If this returns count instead of list
            
            assert len(notes_count) == 3  # Should be 3, not 1
            for note in notes_count:
                assert isinstance(note, Note)