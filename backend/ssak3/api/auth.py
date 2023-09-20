from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext

from models.auth import auth
from db.db import session

router = APIRouter(prefix="/auth")

pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/sign-up", status_code=status.HTTP_200_OK)
def signUp(id: str, name: str, password: str):
    db = session()
    try:
        exist_user = db.query(auth).filter(auth.id == id).first()
        if(exist_user):
            # status_code=status.HTTP_409_CONFLICT
            # return {"message": "이미 존재하는 아이디 입니다."}
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="이미 존재하는 아이디 입니다.") # 중복된 아이디는 예외 던지기
        hash_pw = pw_context.hash(password) # 비밀번호 암호화
        user = auth(id=id, name=name, password=hash_pw)
        db.add(user)
        db.commit()
        # response = {"statusCode": status.HTTP_200_OK, }
        # return response
    finally:
        db.close()

