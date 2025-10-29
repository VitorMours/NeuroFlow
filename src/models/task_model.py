from sqlalchemy import DateTime, String, Boolean, ForeignKey, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db
import uuid


class Task(db.Model):
    __tablename__ = "task"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    task: Mapped[str] = mapped_column(String(50), nullable=False)
    task_description: Mapped[str | None] = mapped_column(String(300))
    task_conclusion: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", name="fk_task_user_id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="tasks") # type:ignore
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    

    def toggle_conclusion(self) -> None:
        self.task_conclusion = not self.task_conclusion

    def __str__(self) -> str:
        return f"<{self.user_id} -> {self.task} {self.task_conclusion}>"
    
    def to_json(self) -> dict[str, str | bool]:
        return {
            "id": self.id,
            "task": self.task,
            "task_description": self.task_description,
            "task_conclusion": self.task_conclusion,
            "user_id": self.user_id
        }
        