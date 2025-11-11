import pytest
import importlib 
import inspect

class TestNoteModel:
    def test_if_is_running(self) -> None:
        assert True 
        
    def test_if_can_get_note_model(self) -> None:
        module = importlib.import_module("src.models.note_model")
        assert hasattr(module, "Note")
        
    def test_if_note_model_is_a_class(self) -> None:
        module = importlib.import_module("src.models.note_model")
        class_ = module.Note 
        assert inspect.isclass(class_)
        
    def test_if_note_correct_subclass(self) -> None:
        module = importlib.import_module("src.models.note_model")
        class_ = module.Note 
        assert hasattr(class_, "__tablename__")
        assert hasattr(class_, "metadata")
    
    def test_if_note_model_have_correct_fields(self) -> None:
        module = importlib.import_module("src.models.note_model")
        class_ = module.Note
        assert hasattr(class_, "id")
        assert hasattr(class_, "title")
        assert hasattr(class_, "link")
        assert hasattr(class_, "content")
        assert hasattr(class_, "created_at")
        assert hasattr(class_, "user_id")
        
    def test_get_note_title_data(self) -> None:
        module = importlib.import_module("src.models.note_model")
        class_ = module.Note
        assert True