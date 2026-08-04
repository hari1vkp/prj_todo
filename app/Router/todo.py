from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session

from app.dependencies.depndencies import get_current_user
from app.dependencies.connection import get_db
from app.Schemas.todo import Todo as Todocreate,Todoreturn
from app.Models.Todos import Todo
from app.Service.todo_service import Todoservice

router=APIRouter(prefix="/todo",tags=["todo"])

@router.get("/",response_model=list[Todoreturn])
def get_all_todo(db:Session=Depends(get_db),currentuser=Depends(get_current_user)):
    services=Todoservice(db)
    return services.get_all_todos(currentuser.id)

@router.get(f"/{id}",response_model=Todoreturn)
def get_byid(todoid:int,db:Session=Depends(get_db),currentusr=Depends(get_current_user)):
    services=Todoservice(db)
    return services.get_todo_by_id(todoid,currentusr.id)

@router.post("/",response_model=Todocreate)
def create_todo(todo:Todocreate,db:Session=Depends(get_db),currntusr=Depends(get_current_user)):
    services=Todoservice(db)
    return services.create_todo(todo.task,todo.desc,currntusr.id)

@router.put(f"/{id}",response_model=Todocreate)
def update_todo(todo:Todocreate,id:int,db:Session=Depends(get_db),currnt=Depends(get_current_user)):
    sevices=Todoservice(db)
    updated=sevices.update_todo(todo.task,todo.desc,id,currnt.id)
    return updated

@router.delete(f"/{id}")
def delete_todo(id:int,db:Session=Depends(get_db),currnt=Depends(get_current_user)):
    services=Todoservice(db)
    deleted=services.deltodo(id,currnt.id)
    if deleted:
        return {"message":f"{id} deleted"}
    