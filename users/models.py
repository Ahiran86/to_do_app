from core.database import Base
from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username : Mapped[str] = mapped_column()
    password : Mapped[str] = mapped_column()
    is_active : Mapped[bool] = mapped_column(default=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())
    tasks : Mapped[list["TaskModel"]] = relationship("TaskModel", back_populates="user") #type:ignore

    def hash_password(self, plain_password):
        self.password = pwd_context.hash(plain_password)
    
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)