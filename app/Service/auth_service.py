
from app.Models.user import user
from app.auth import create_access_token,create_refresh_token,verify_pass,verify_token,hashpass
from fastapi import HTTPException
from sqlalchemy.orm import Session

class Authservices:
    def __init__(self,db:Session):
        self.db=db

    def register(self,name:str,email:str,password:str):
        existing_usr=self.db.query(user).filter(user.email==email).first()
        if existing_usr:
            raise HTTPException(status_code=400,detail="user alreadyexist")
        newusr=user(name=name,email=email,password=hashpass(password))
        self.db.add(newusr)
        self.db.commit()
        self.db.refresh(newusr)
        return newusr

    def login(self,email:str,password:str):
        existing_usr=self.db.query(user).filter(user.email==email).first()
        if existing_usr is None:
            raise HTTPException(status_code=401, detail="inavaid user")
        if not verify_pass(password,existing_usr.password):
            raise HTTPException(status_code=401,detail="invalid password")
        acesstoken=create_access_token(email)
        refreshtoken=create_refresh_token(email)
        return {
            "access_token": acesstoken,
            "refresh_token": refreshtoken,
            "token_type": "bearer"
        }

    def refresh(self,ref:str):
        payload=verify_token(ref,t_type="refresh")
        email=payload.get("email")
        existing_usr=self.db.query(user).filter(user.email==email).first()
        if  existing_usr is None:
            raise HTTPException(status_code=401, detail="inavaid user")
        acesstoken=create_access_token(email)
        refreshtoken=create_refresh_token(email)
        return {
            "access_token": acesstoken,
            "refresh_token": refreshtoken,
            "token_type": "bearer"
        }
