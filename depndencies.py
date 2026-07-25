from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth import verify_token

oauthcon = HTTPBearer()


def get_current_user(tokena: HTTPAuthorizationCredentials = Depends(oauthcon)):
    payload = verify_token(tokena.credentials)
    return payload
