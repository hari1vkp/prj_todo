
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
app.include_router(auth.router)



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



