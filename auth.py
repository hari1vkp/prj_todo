from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from passlib.context import CryptContext

alg = "HS256"
secretkey = "hari"
exp = 10

pass_con = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashpass(passw: str):
    return pass_con.hash(passw)


def verify_pass(userpass: str, hashpass: str):
    return pass_con.verify(userpass, hashpass)


def create_access_token(uname: str):
    expire = datetime.utcnow() + timedelta(minutes=exp)
    payload = {"usrname": uname, "exp": expire.timestamp()}
    return jwt.encode(payload, secretkey, alg)


def verify_token(token: str):
    try:
        uname = jwt.decode(token, secretkey, algorithms=[alg])
        return uname
    except JWTError:
        raise HTTPException(status_code=400, detail="invalid user")
