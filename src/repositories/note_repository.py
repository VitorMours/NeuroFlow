from ..models.note_model import Note 
from ..models.user_model import User
from ..models import db
from typing import List, Optional 

class NoteRepository:
    
    @staticmethod 
    def create(note_data: dict[str, str], user: User) -> Note: 
        """ 
        metodo designado para criar a nota de um usuario dentro do
        banco de dados, e ter seu id como chave estrangeira de procura
        """
        try:
            new_note = Note(
                title= note_data["title"],
                link = "",
                content=note_data["content"],
                user_id = user.id
            )
            db.session.add(new_note)
            db.session.commit()
            
            return new_note        
        except Exception as e:
            return e    
        
        
    @staticmethod 
    def update() -> None:
        pass 
    
    @staticmethod 
    def get_by_uuid() -> None: 
        pass
    
    @staticmethod
    def get_all() -> None:
        all_notes = Note.query.all()
        return all_notes         
    
    def __repr__(self) -> str:
        return "<NoteRepository>"
    
    def __str__(self) -> str:
        return "<NoteRepository>"