from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Models.Todos import Todo


class Todoservice:
    def __init__(self,db:Session):
        self.db=db

    def get_all_todos(self,user_id:int):
        todos=self.db.query(Todo).filter(user_id==Todo.user_id).all()
        if todos:
            return todos
       

    def get_todo_by_id(self,id:int,user_id:int):
        gettodo= self.db.query(Todo).filter(user_id==Todo.user_id,Todo.id==id).first()
        if gettodo:
            return gettodo
        raise HTTPException(status_code=404,detail="todonotfound")

    def create_todo(self,tasks:str,desc:str,user_id:int):
            todoadd=Todo(task=tasks,desc=desc,user_id=user_id)
            self.db.add(todoadd)
            self.db.commit()
            self.db.refresh(todoadd)
            return todoadd

    def update_todo(self,task:str,desc:str,todo_id:int,user_id:int):
            singletodo=self.get_todo_by_id(todo_id,user_id)
            if singletodo:
                  singletodo.desc=desc
                  singletodo.task=task
                  self.db.commit()
                  self.db.refresh(singletodo)
                  return singletodo
            raise HTTPException(status_code=404,detail="not found")
            
    def deltodo(self,todo_id:int,user_id:int):
            singletodo=self.get_todo_by_id(todo_id,user_id)
            
            if singletodo:
                self.db.delete(singletodo)
                self.db.commit()
                return singletodo
            raise HTTPException(status_code=409,detail="not found")