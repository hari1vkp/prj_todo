from pydantic import BaseModel

class Refreshtoken(BaseModel):
    refreshtoken:str


class base(BaseModel):
    name: str
    email: str
    password: str
    
class user(base):
    pass


class userlogin(BaseModel):
    email: str
    password: str


class userreturn(base):
    id: int
