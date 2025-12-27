import pytest 
from abc import ABC 
import inspect 
import importlib 

# TODO: Tenho que corrigit pelo fato de serem atributos de uma classe abstrata
# nao sei omo vou corrigir isso, mas preciso corrigir para o funcionamento pleno
# class TestNoteServiceInterface:

#     def test_if_can_import_note_service_interface(self) -> None:
#         module = importlib.import_module("src.interfaces.note_service_interface")
#         assert hasattr(module, "NoteServiceInterface"), "Módulo não exporta NoteServiceInterface"

#     def test_if_note_service_interface_is_abstract_and_subclass_of_ABC(self) -> None:
#         module = importlib.import_module("src.interfaces.note_service_interface")
#         cls = getattr(module, "NoteServiceInterface")
#         assert inspect.isclass(cls), "NoteServiceInterface não é uma classe"
#         assert issubclass(cls, ABC), "NoteServiceInterface deve herdar de ABC"
#         assert inspect.isabstract(cls), "NoteServiceInterface deve ser abstrata"

#     def test_if_note_service_interface_has_create_note_abstract_method(self) -> None:
#         module = importlib.import_module("src.interfaces.note_service_interface")
#         cls = getattr(module, "NoteServiceInterface")
#         assert hasattr(cls, "create_note"), "Método create_note não encontrado na interface"
#         abstract_methods = getattr(cls, "__abstractmethods__", set())
#         assert "create_note" in abstract_methods, "create_note deve ser um método abstrato"
# ...existing code...
    
    