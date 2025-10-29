from abc import ABC, abstractmethod

class NoteServiceInterface(ABC):
    
    @abstractmethod
    @staticmethod
    def create_note() -> None:
        pass
    
    
    @abstractmethod
    @staticmethod
    def update_note() -> None:
        pass 
    
    @abstractmethod
    @staticmethod 
    def get_user_notes() -> None:
        pass
    
    @abstractmethod 
    @staticmethod 
    def delete_user_note() -> None:
        pass