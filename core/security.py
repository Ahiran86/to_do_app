import jwt
from datetime import datetime, timedelta, UTC
from core.config import settings
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidSignatureError, InvalidTokenError, ExpiredSignatureError
from core.database import get_db
from users.models import UserModel
from pydantic import BaseModel, Field



security = HTTPBearer()

def generate_access_token(user_id: int):
    now = datetime.now(UTC)
    payload = {"type": "access", "user_id": user_id, "iat": now, "exp": now + timedelta(minutes=5)}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return token

def generate_refresh_token(user_id: int):
    now = datetime.now(UTC)
    payload = {"type": "refresh", "user_id": user_id, "iat": now, "exp": now + timedelta(minutes=60*24)}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return token

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security), db:Session=Depends(get_db)):
    
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")
    
    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid signature")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token is invalid")
    if decoded["type"] != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="it is not access token")
    
    user_id = decoded["user_id"]
    user = db.get(UserModel, user_id)
    return user


def decode_refresh_token(token):
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")
    
    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid signature")
    except ExpiredSignatureError:
        raise HTTPException(status_code=HTTPException, detail="token has expierd")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token is invalid")
    
    if decoded["type"] != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token, it is not refresh token")
    
    user_id = decoded["user_id"]
    return user_id











class UserRefreshTokenSchema(BaseModel):
    token : str = Field(..., description="this is your refresh token")