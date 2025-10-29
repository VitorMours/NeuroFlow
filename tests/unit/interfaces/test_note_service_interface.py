import pytest 
from abc import ABC 
import inspect 
import importlib 

# TODO: Tenho que corrigit pelo fato de serem atributos de uma classe abstrata
# nao sei omo vou corrigir isso, mas preciso corrigir para o funcionamento pleno
class TestNoteServiceInterface:
    
    def test_if_can_import_note_service_interface(self) -> None: 
        module = importlib.import_module("src.interfaces.note_service_interface")
        assert hasattr(module, "NoteServiceInterface")
        
    def test_if_note_service_interface_have_correct_superclass(self) -> None: 
        module = importlib.import_module("src.interfaces.note_service_interface")
        class_ = module.Note 
        assert issubclass(class_, ABC)
        
    def test_if_note_service_interface_have_correct_methods(self) -> None:
        module = importlib.import_module("src.interfaces.note_service_interface")
        class_ = module.Note 
        assert hasattr(class_, "create_note")
    
    
    
    