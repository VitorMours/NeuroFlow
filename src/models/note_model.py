from sqlalchemy import String, Boolean, DateTime, func, ForeignKey
from . import db
import uuid 
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Note(db.Model):
    __tablename__ = "note"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", name="fk_note_user_id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="notes") #type: ignore

    def __str__(self) -> None:
        return f"{self.title}: {self.user_id}"



