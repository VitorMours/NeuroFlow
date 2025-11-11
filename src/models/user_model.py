from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import uuid
from . import db
from sqlalchemy.dialects.mysql import CHAR


class User(db.Model):
    """
    Modelo responsável por criar usuários no banco de dados
    e estruturar seus relacionamentos com tarefas e anotações.
    """

    __tablename__ = "user"

    id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)

    # Relações
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")  # type: ignore
    notes: Mapped[List["Note"]] = relationship(back_populates="user")  # type: ignore

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        if self.first_name:
            return self.first_name
        return "O usuário ainda não possui nome cadastrado"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}: {self.email}"
