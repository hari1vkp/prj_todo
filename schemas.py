from pydantic import BaseModel


class base(BaseModel):
    name: str
    email: str
    password: str


class user(base):
    pass


class userlogin(BaseModel):
    email: str
    password: str


class userreturn(base):
    id: int


class Todo(BaseModel):
    task: str
    desc: str


class Todoreturn(Todo):
    id: int
