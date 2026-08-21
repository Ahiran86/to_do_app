from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.database import get_db
from users.models import UserModel
from users.schemas import *
from core.security import generate_access_token, generate_refresh_token, get_current_user, decode_refresh_token, UserRefreshTokenSchema

from core.config import settings



router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
async def login_user(data : UserLoginSchema, db:Session = Depends(get_db)):
    user = db.scalar(select(UserModel).where(UserModel.username == data.username))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="your username not exists")
    if not user.verify_password(data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid")
    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)
    return JSONResponse(content={"message": "wellcome, you loginned", "access_token": access_token, "refresh_token": refresh_token})



@router.post("/singup")
async def login_user(data: UserSignupSchema, db:Session = Depends(get_db)):
    if db.scalar(select(UserModel).where(UserModel.username == data.username)):
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="your username alredy exsits")
    user = UserModel(username=data.username)
    user.hash_password(data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(content="your user created")


@router.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    print(current_user)
    print(type(current_user))
    return {"username": current_user.username, "id": current_user.id, "is_activ": current_user.is_active}


@router.post("/refresh")
async def get_profile(tokenn: UserRefreshTokenSchema, db:Session=Depends(get_db)):
    user_id = decode_refresh_token(tokenn.token)
    user = db.get(UserModel, user_id)
    print(user)
    refresh = generate_refresh_token(user_id)
    return {"username": user.username, "password": user.password, "new_refresh_token": refresh}


@router.get("/test") 
async def test(request: Request):
    print(request.headers.get("authorization"))