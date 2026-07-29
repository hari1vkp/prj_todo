from sqlalchemy import Integer, String, Column,ForeignKey
from sqlalchemy.orm import relationship
from app.database import base


class user(base):
    __tablename__ = "usertable"
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    todos = relationship("Todo", back_populates="owner")