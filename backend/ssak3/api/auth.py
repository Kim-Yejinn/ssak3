import os
from datetime import datetime, timedelta
from typing import Tuple

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext
from jose import JWTError, jwt
import redis

from models.auth import auth
from db.db import get_db

router = APIRouter(prefix="/auth")

ACCESS_TOKEN_TIME = os.getenv("ACCESS_TOKEN_EXPIRE_TIME")
REFRESH_TOKEN_TIME = os.getenv("REFRESH_TOKEN_EXPIRE_TIME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DATABASE")
REDIS_PW = os.getenv("REDIS_PASSWORD")
rd = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB) # redis 연결


pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/sign-up", status_code=status.HTTP_200_OK)
def signUp(id: str, name: str, password: str, db: Session = Depends(get_db)):
    try:
        exist_user = db.query(auth).filter(auth.id == id).first()
        if(exist_user):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="이미 존재하는 아이디 입니다.") # 중복된 아이디는 예외 던지기
        hash_pw = pw_context.hash(password) # 비밀번호 암호화
        user = auth(id=id, name=name, password=hash_pw)
        db.add(user)
        db.commit()
    finally:
        db.close()



@router.post("/log-in", status_code=status.HTTP_200_OK)
# def logIn(id: str, password: str, db: Session = Depends(get_db)):
def logIn(
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
        db: Session = Depends(get_db)
):
    exist_user = db.query(auth).filter(auth.id == form_data.username).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

    if not (pw_context.verify(form_data.password, exist_user.password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호를 잘못 입력하셨습니다.")

    atk_time = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_TIME))
    rtk_time = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_TIME))

    atk_data = {
        "sub": form_data.username,
        "exp": atk_time
    }
    access_token = jwt.encode(atk_data, SECRET_KEY, ALGORITHM)

    rtk_data = {
        "sub": form_data.username,
        "exp": rtk_time
    }
    refresh_token = jwt.encode(rtk_data, SECRET_KEY, ALGORITHM)

    return {"accessToken": access_token, "refreshToken": refresh_token}



@router.post("/log-in", status_code=status.HTTP_200_OK)
# def logIn(id: str, password: str, db: Session = Depends(get_db)):
def logIn(
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
        db: Session = Depends(get_db)
):
    exist_user = db.query(auth).filter(auth.id == form_data.username).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

    if not (pw_context.verify(form_data.password, exist_user.password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호를 잘못 입력하셨습니다.")

    atk_time = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_TIME))
    rtk_time = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_TIME))

    atk_data = {
        "sub": form_data.username,
        "exp": atk_time
    }
    access_token = jwt.encode(atk_data, SECRET_KEY, ALGORITHM)

    rtk_data = {
        "sub": form_data.username,
        "exp": rtk_time
    }
    refresh_token = jwt.encode(rtk_data, SECRET_KEY, ALGORITHM)

    return {"accessToken": access_token, "refreshToken": refresh_token}



@router.post("/log-in", status_code=status.HTTP_200_OK)
def logIn(id: str, password: str, db: Session = Depends(get_db)):
    exist_user = db.query(auth).filter(auth.id == id).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

    if not (pw_context.verify(password, exist_user.password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호를 잘못 입력하셨습니다.")

    atk_time = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_TIME))
    rtk_time = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_TIME))

    atk_data = {
        "type": "atk",
        "sub": id,
        "exp": atk_time
    }
    access_token = jwt.encode(atk_data, SECRET_KEY, ALGORITHM)

    rtk_data = {
        "type": "rtk",
        "sub": id,
        "exp": rtk_time
    }
    refresh_token = jwt.encode(rtk_data, SECRET_KEY, ALGORITHM)
    rd.set(id, refresh_token, int(REFRESH_TOKEN_TIME)*60)
    # print(rd.get(id))

    return {"accessToken": access_token, "refreshToken": refresh_token}

@router.delete("/log-out", status_code=status.HTTP_200_OK)
def logOut(id: str):
    rd.delete(id)

@router.get("/retoken")
def reToken(id: str):
    atk_time = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_TIME))

    atk_data = {
        "type": "atk",
        "sub": id,
        "exp": atk_time
    }
    access_token = jwt.encode(atk_data, SECRET_KEY, ALGORITHM)

    refresh_token = rd.get(id)

    return {"accessToken": access_token, "refreshToken": refresh_token}