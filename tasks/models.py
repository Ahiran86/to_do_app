from sqlalchemy import func, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from datetime import datetime

class TaskModel(Base):
    __tablename__ = "tasks"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    title : Mapped[str] = mapped_column(String(50), nullable=False)
    description : Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_complete :  Mapped[bool] = mapped_column(nullable=False, default=False)
    created_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user : Mapped["UserModel"] = relationship("UserModel", back_populates="tasks") #type:ignore

