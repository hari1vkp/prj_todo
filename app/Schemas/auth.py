
from pydantic import BaseModel

class UserCreate(BaseModel):

    name: str
    email: str
    password: str

class UserLogin(BaseModel):

    email: str
    password: str

class UserReturn(BaseModel):

    id: int
    name: str
    email: str

class TokenResponse(BaseModel):

    access_token: str
    refresh_token: str
    token_type: str

class RefreshRequest(BaseModel):

    refresh_token: str