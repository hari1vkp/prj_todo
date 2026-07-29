
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import session

from database import base,sessionlocal
from connection import get_db
from depndencies import get_current_user
from Models.Todos import todos
from Models.user import user
from Models.user import userlogin, userreturn,user as userc,Todo as Todocreate,Todoreturn,Refreshtoken
from auth import create_access_token, hashpass,verify_pass,create_refresh_token, verify_token

app=FastAPI()

base.metadata.create_all(bind=sessionlocal().bind)




@app.put(f"/userupdate/{id}",response_model=userreturn)
def updateuser(id:int,updated:userc,db:session=Depends(get_db),current_user=Depends(get_current_user)):
    singleuser=db.query(user).filter(id==user.id).first()
    if not singleuser:
        raise HTTPException(status_code=404,detail="not found")
    for key,value in updated.model_dump().items():
        setattr(singleuser,key,value)
    db.commit()
    db.refresh(singleuser)
    return singleuser

@app.delete("/user/{id}")
def deluser(id:int,db:session=Depends(get_db),current_user=Depends(get_current_user)):
    singleuser=db.query(user).filter(id==user.id).first()
    if not singleuser:
        raise HTTPException(status_code=404,detail="not found")
    db.delete(singleuser)
    db.commit()
    return{"message":"deleted sucessfully"}

@app.get("/todos",response_model=list[Todoreturn])
def gettodos(db:session=Depends(get_db),current_user=Depends(get_current_user)):
    return db.query(Todo).filter(current_user.id==Todo.user_id).all()

@app.get(f"/todo/{id}")
def getbyid(id:int,db:session=Depends(get_db),currentuser=Depends(get_current_user)):
    singletodo=db.query(Todo).filter(id==Todo.id,Todo.user_id==currentuser.id).first()
    return singletodo

@app.post("/todo",response_model=Todoreturn)
def createdodo(Todocreate:Todocreate ,usertable:session=Depends(get_db),current_user=Depends(get_current_user)):
    todoadd=Todo(**Todocreate.model_dump(),user_id=current_user.id)
    db.add(todoadd)
    db.commit()
    db.refresh(todoadd)
    return todoadd

@app.put(f"/todo/{id}",response_model=Todoreturn)
def altertodo(id:int,updated:Todocreate,db:session=Depends(get_db),current_user=Depends(get_current_user)):
      singletodo=db.query(Todo).filter(id==Todo.id,Todo.user_id==current_user.id).first()
      if not singletodo:
        raise HTTPException(status_code=404,detail="todo not found")
      for key,value in updated.model_dump().items():
        setattr(singletodo,key,value)
      db.commit()
      db.refresh(singletodo)
      return singletodo

@app.delete(f"/todo/{id}")
def deletetodo(id:int,db:session=Depends(get_db),current_user=Depends(get_current_user)):
     singletodo=db.query(Todo).filter(id==Todo.id,Todo.user_id==current_user.id).first()
     db.delete(singletodo)
     db.commit()
     return{"message":f"deleted {id}"}

@app.post("/register" ,response_model=userreturn)
def reg_user(userc:userc, db:session=Depends(get_db)):
    existing_user=db.query(user).filter(userc.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400 ,detail="user already exist")
    newuser=user(name=userc.name,email=userc.email,password=hashpass(userc.password))
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser


@app.post("/login")
def login(userlogin:userlogin,db:session=Depends(get_db)):
    existing_user=db.query(user).filter(userlogin.email==user.email).first()

    if existing_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    if not verify_pass(userlogin.password,existing_user.password):
        raise HTTPException(status_code=400, detail="invalid credentials")
    
    token=create_access_token(userlogin.email)
    refresh_token=create_refresh_token(userlogin.email)
    return {"acess_token":token,"refresh_token":refresh_token,"tokentype":"bearer"}

@app.post("/refresh")
def refresh(ref:Refreshtoken):

    payload=verify_token(ref.refreshtoken,t_type="refresh")
    email=payload.get("email")
    if email is None:
        raise HTTPException(status_code=400,detail="invalid user")
    newacess=create_access_token(email)
    new_refreshtoken=create_refresh_token(email)
    return{"acess_token":newacess,
            "refresh_token":new_refreshtoken,
            "token_type":"bearer"}