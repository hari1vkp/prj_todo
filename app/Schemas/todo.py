from pydantic import BaseModel

class Todo(BaseModel):
    task: str
    desc: str


class Todoreturn(Todo):
    id: int