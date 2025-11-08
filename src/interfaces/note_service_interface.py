from abc import ABC, abstractmethod

class NoteServiceInterface(ABC):

    @staticmethod
    @abstractmethod
    def create_note() -> None:
        pass
    
    
    @staticmethod
    @abstractmethod
    def update_note() -> None:
        pass 
    
    @staticmethod
    @abstractmethod
    def get_user_notes() -> None:
        pass
    
    @staticmethod
    @abstractmethod
    def delete_user_note() -> None:
        pass
