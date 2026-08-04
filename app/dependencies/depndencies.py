from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.dependencies.connection import get_db
from app.Models.user import user

from app.auth import verify_token

secuauth = HTTPBearer()

def get_current_user(tokena: HTTPAuthorizationCredentials = Depends(secuauth),
db:Session=Depends(get_db)):
    token=tokena.credentials
    payload = verify_token(token,t_type="acess")
    email=payload.get("email")
    if email is None:
        raise HTTPException(status_code=401,detail="invalid user")
    existinguser=db.query(user).filter(email==user.email).first()
    if existinguser is None:
         raise HTTPException(status_code=404,detail="user not found")
    return existinguser
