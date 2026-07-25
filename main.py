
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import session

from database import base,sessionlocal
from connection import get_db
from depndencies import get_current_user
from models import user,Todo
from schemas import userlogin, userreturn,user as userc,Todo as Todocreate,Todoreturn
from auth import create_access_token, hashpass,verify_pass

app=FastAPI()

base.metadata.create_all(bind=sessionlocal().bind)

@app.get("/",response_model=list[userreturn])
def getll(db:session=Depends(get_db)):
    return db.query(user).all()

@app.get(f"/user/{id}",response_model=userreturn)
def getuser(id:int,db:session=Depends(get_db)):
    singleuser= db.query(user).filter(user.id==id).first()
    if not singleuser:
        raise HTTPException(status_code=404 ,detail="not found")
    return singleuser

@app.post("/usercreate",response_model=userreturn)
def createuser(users:userc ,db:session=Depends(get_db)):
    useradd=user(**users.dict())
    db.add(useradd)
    db.commit()
    db.refresh(useradd)
    return useradd

@app.put(f"/userupdate/{id}",response_model=userreturn)
def updateuser(id:int,updated:userc,db:session=Depends(get_db)):
    singleuser=db.query(user).filter(id==user.id).first()
    if not singleuser:
        raise HTTPException(status_code=404,detail="not found")
    for key,value in updated.dict().items():
        setattr(singleuser,key,value)
    db.commit()
    db.refresh(singleuser)
    return singleuser

@app.delete("/user/{id}")
def deluser(id:int,db:session=Depends(get_db)):
    singleuser=db.query(user).filter(id==user.id).first()
    if not singleuser:
        raise HTTPException(status_code=404,detail="not found")
    db.delete(singleuser)
    db.commit()
    return{"message":"deleted sucessfully"}

@app.get("/todos",response_model=list[Todoreturn])
def gettodos(db:session=Depends(get_db),current_user=Depends(get_current_user)):
    return db.query(Todo).all()

@app.get(f"/todo/{id}")
def getbyid(id:int,db:session=Depends(get_db)):
    singletodo=db.query(Todo).filter(id==Todo.id).first()
    return singletodo

@app.post("/todo",response_model=Todoreturn)
def createdodo(Todocreate:Todocreate ,db:session=Depends(get_db)):
    todoadd=Todo(**Todocreate.dict())
    db.add(todoadd)
    db.commit()
    db.refresh(todoadd)
    return todoadd

@app.put(f"/todo/{id}",response_model=Todoreturn)
def altertodo(id:int,updated:Todocreate,db:session=Depends(get_db),):
      singletodo=db.query(Todo).filter(id==Todo.id).first()
      if not singletodo:
        raise HTTPException(status_code=404,detail="todo not found")
      for key,value in updated.dict().items():
        setattr(singletodo,key,value)
      db.commit()
      db.refresh(singletodo)
      return singletodo

@app.delete(f"/todo/{id}")
def deletetodo(id:int,db:session=Depends(get_db)):
     singletodo=db.query(Todo).filter(id==Todo.id).first()
     db.delete(singletodo)
     db.commit()
     return{"message":f"deleted {id}"}

@app.post("/register" ,response_model=userreturn)
def registeruser(userc:userc,db:session=Depends(get_db)):
    existing_user=db.query(user).filter(user.email==userc.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="user already exist")
    new_user=user(name=userc.name,email=userc.email,password=hashpass(userc.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(loginuser:userlogin,db:session=Depends(get_db)):
    existing_user=db.query(user).filter(user.email==loginuser.email).first()
    if existing_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    
    if not verify_pass(loginuser.password,existing_user.password):
        raise HTTPException(status_code=401,detail="invalid credentials")

    token=create_access_token(existing_user.email)
    return{"token":token,
            "token_type": "bearer"}
    