from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from database import Base
from datetime import datetime

class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    updated_at = Column(TIMESTAMP, default=datetime.now())
