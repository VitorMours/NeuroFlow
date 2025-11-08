from ..models.note_model import Note 
from ..models.user_model import User
from ..models import db
from typing import List, Optional 
import uuid

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
    def update(old_data: Note, new_data: dict[str, str | bool]) -> None:
        fields = [field for field in dir(Note) if not field.startswith("_")]
        try:
            for key, value in new_data.items():
                if key not in fields:
                    raise KeyError("This type of value does not can be assigned")
                setattr(old_data, key, value)

            db.session.commit()
            return True

        except Exception as e:
            return e
    
    @staticmethod 
    def get_by_uuid(uuid: uuid.uuid4) -> None | Note:
        return Note.query.filter_by(id=uuid).first()
    
    @staticmethod
    def get_all() -> None:
        all_notes = Note.query.all()
        return all_notes         
    
    @staticmethod
    def get_by_user_uuid(user_uuid: uuid) -> None | List[Note]:
        return Note.query.filter_by(user_id=user_uuid).all()

    def __repr__(self) -> str:
        return "<NoteRepository>"
    
    def __str__(self) -> str:
        return "<NoteRepository>"
