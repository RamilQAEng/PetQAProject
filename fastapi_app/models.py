from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .dependencies import Base

class Task(Base):
    __tablename__ = "tasks_task"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
