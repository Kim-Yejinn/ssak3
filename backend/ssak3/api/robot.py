import os
from datetime import datetime, timedelta
from typing import Tuple

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from models.auth import auth
from models.tutlebot import turtlebot
from db.db import get_db

router = APIRouter(prefix="/robot")
@router.post("/regist", status_code=status.HTTP_200_OK)
def robotRegist(id: str, number: str, db: Session = Depends(get_db)):
    try:
        if number is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="입력을 확인하세요.")
        exist_user = db.query(auth).filter(auth.id == id).first()
        if not (exist_user):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="존재하지 않는 사용자 입니다.") # 아이디가 존재하지 않으면 예외 던지기
        robot = turtlebot(auth_id=exist_user.auth_id, serial_number=number)
        db.add(robot)
        db.commit()
    finally:
        db.close()