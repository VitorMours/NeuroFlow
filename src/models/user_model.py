from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import uuid
from . import db

class User(db.Model):
    """
    User:
        Modelo responsável por criar os modelos que são usados para definir usuários dentro do banco de dados, e para 
        estruturar os relacionamentos e funcionamentos dentro do banco de dados
    
    Args:
        first_name: Primeiro nome do usuário
        last_name: Ultimo nome do usuário
        email: Email para fazer cadastro e receber comunicados por meios oficiais
        password: Senha do usuário para fazer login dentro do sistema
    
    Returns:
        Retorna a instância de um usuário
    """
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    tasks: Mapped[List["Task"]] = relationship(back_populates="user") # type:ignore
    notes: Mapped[List["Note"]] = relationship(back_populates="user") # type:ignore
    
    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        if self.first_name:
            return self.first_name
        return "O usuário ainda não possui nome cadastrado"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}: {self.email}"
