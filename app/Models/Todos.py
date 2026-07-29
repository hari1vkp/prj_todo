from sqlalchemy import Integer, String, Column,ForeignKey
from sqlalchemy.orm import relationship
from app.database import base


class Todo(base):
    __tablename__ = "Todo"
    task = Column(String)
    id = Column(Integer, index=True, primary_key=True)
    desc = Column(String)
    user_id=Column(Integer,ForeignKey("usertable.id"),nullable=False)
    owner=relationship("user",back_populates="todos")