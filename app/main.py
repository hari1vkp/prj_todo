
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import session
from app.database import base,sessionlocal
from app.connection import get_db
from app.depndencies import get_current_user
from app.Models.Todos import Todo
from app.Models.user import user
from app.auth import create_access_token, hashpass,verify_pass,create_refresh_token, verify_token
from app.Router import todo,user,auth
from app.Schemas.Token import user as userc,userlogin,userreturn,Refreshtoken
app=FastAPI()

base.metadata.create_all(bind=sessionlocal().bind)
app.include_router(todo.router)



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