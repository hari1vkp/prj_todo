from sqlalchemy import Integer, String, Column
from database import base


class user(base):
    __tablename__ = "usertable"
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Todo(base):
    __tablename__ = "Todo"
    task = Column(String)
    id = Column(Integer, index=True, primary_key=True)
    desc = Column(String)
