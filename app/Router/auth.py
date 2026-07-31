from fastapi import APIRouter,HTTPException,Depends

from app.connection import get_db
from app.Schemas.auth import UserLogin,UserCreate,TokenResponse,RefreshRequest
from sqlalchemy.orm import Session
from app.Service.auth_service import Authservices

router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/login",response_model=TokenResponse)
def login(userlogin:UserLogin,db:Session=Depends(get_db)):
    service=Authservices(db)
    return service.login(userlogin.email,userlogin.password)

@router.post("/register",response_model=UserCreate)
def register(userreg:UserCreate,db:Session=Depends(get_db)):
    sevice=Authservices(db)
    return sevice.register(userreg.name,userreg.email,userreg.password)

@router.post("/refresh",response_model=TokenResponse)
def refreshtoken(ref:RefreshRequest,db:Session=Depends(get_db)):
    service=Authservices(db)
    return service.refresh(ref.refresh_token)
