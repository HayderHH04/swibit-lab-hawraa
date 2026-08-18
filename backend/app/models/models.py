from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean , default=False)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, default="medium")
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    owner = relationship("User", back_populates="tasks")