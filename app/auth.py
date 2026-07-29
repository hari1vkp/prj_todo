from datetime import datetime, timedelta,timezone
from jose import JWTError, jwt
from fastapi import HTTPException
from passlib.context import CryptContext

alg = "HS256"
secretkey = "hari"
exp = 10
exp_ref=7

pass_con = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashpass(passw: str):
    return pass_con.hash(passw)


def verify_pass(userpass: str, hashpass: str):
    return pass_con.verify(userpass, hashpass)


def create_access_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=exp)
    payload = {"email": email,"Type":"acess", "exp": expire.timestamp()}
    return jwt.encode(payload, secretkey, alg)

def create_refresh_token(email:str):
    expire = datetime.now(timezone.utc) + timedelta(days=exp_ref)
    payload = {"email": email,"Type":"refresh", "exp": expire.timestamp()}
    return jwt.encode(payload, secretkey, alg)


def verify_token(token: str,t_type:str="acess"):
    try:
        payload = jwt.decode(token, secretkey, algorithms=[alg])
        if payload.get("Type") != t_type:
                raise HTTPException(
                status_code=401,
                detail=f"Invalid {t_type} token"
            )
        return payload
        
    except JWTError:
        raise HTTPException(status_code=400, detail="invalid user")
