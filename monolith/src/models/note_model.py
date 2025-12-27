from sqlalchemy import String, Boolean, DateTime, func, ForeignKey
from . import db
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import CHAR


class Note(db.Model):
    __tablename__ = "note"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str | None] = mapped_column(String(5000))  # limite maior, opcional
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    user_id: Mapped[str] = mapped_column(
        CHAR(36),
        ForeignKey("user.id", name="fk_note_user_id"),
        nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="notes")  # type: ignore

    def __str__(self) -> str:
        return f"{self.title}: {self.user_id}"
