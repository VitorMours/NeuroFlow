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
        
    def test_if_repository_have_create_note_method(self) -> None:
        parameters_list = ["note_data","user"]
        module = importlib.import_module("src.repositories.note_repository")
        class_ = module.NoteRepository 
        signature = inspect.signature(class_.create)
        for parameter in parameters_list:
            assert parameter in signature.parameters.keys()

    def test_if_can_create_note(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            new_note = NoteRepository.create(create_random_note_dict, new_user)
            assert isinstance(new_note, Note)

    def test_if_repository_have_update_note_method(self) -> None:
        module = importlib.import_module("src.repositories.note_repository")
        class_ = module.NoteRepository
        assert hasattr(class_, "update")

    def test_if_repository_update_method_have_correct_parameters(self) -> None:
        required_parameters = ["old_data", "new_data"]
        module = importlib.import_module("src.repositories.note_repository")
        class_ = module.NoteRepository
        signature = inspect.signature(class_.update)

        for parameter in required_parameters:
            assert parameter in signature.parameters.keys()

    def test_if_can_update_a_note(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            new_note = NoteRepository.create(create_random_note_dict, new_user)
            assert isinstance(new_note, Note)

            new_data = {"title":"modificando o titulo"}
            result = NoteRepository.update(new_note, new_data)

            assert result

    # def test_if_when_update_note_the_data_update_in_database(self, app, create_random_user_dict, create_random_note_dict) -> None:
    #     with app.app_context():
    #         new_user = UserRepository.create(create_random_user_dict)
    #         assert isinstance(new_user, User)
    #         new_note = NoteRepository.create(create_random_note_dict, new_user)
    #         assert isinstance(new_note, Note)
    #
    #         new_data = {"title":"modificando o titulo"}
    #         result = NoteRepository.update(new_note, new_data)
    #         NoteRepository.

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

    def test_if_can_get_note_by_uuid_method_exists(self) -> None:
        module = importlib.import_module("src.repositories.note_repository")
        class_ = module.NoteRepository
        assert hasattr(class_, "get_by_uuid")


    def test_if_get_by_uuid_method_have_correct_parameters(self) -> None:
        needed_fields = ["uuid"]
        module = importlib.import_module("src.repositories.note_repository")
        class_ = module.NoteRepository
        signature = inspect.signature(class_.get_by_uuid)
        for field in needed_fields:
            assert field in signature.parameters.keys()

    def test_if_can_get_a_note_by_uuid(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.app_context():
            module = importlib.import_module("src.repositories.note_repository")
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)
            new_note = NoteRepository.create(create_random_note_dict, new_user)
            new_note_uuid = new_note.id
            assert isinstance(new_note, Note)
            result = NoteRepository.get_by_uuid(new_note_uuid)

            assert isinstance(result, Note)

    def test_if_can_get_user_notes_by_user_uuid_method_exists(self) -> None:
        module = importlib.import_module("src.repositories.note_repository")
        class_ = module.NoteRepository
        assert hasattr(class_, "get_by_user_uuid")

    def test_if_can_get_user_notes_by_user_uuid(self, app, create_random_user_dict, create_random_note_dict) -> None:
        with app.app_context():
            new_user = UserRepository.create(create_random_user_dict)
            assert isinstance(new_user, User)

            NoteRepository.create(create_random_note_dict, new_user)
            NoteRepository.create(create_random_note_dict, new_user)
            NoteRepository.create(create_random_note_dict, new_user)

            notes_count = NoteRepository.get_all()

            assert len(notes_count) == 3
            for note in notes_count:
                assert isinstance(note, Note)

            notes = NoteRepository.get_by_user_uuid(new_user.id)

            for note in notes:
                assert isinstance(note, Note)
                assert note.user_id == new_user.id
