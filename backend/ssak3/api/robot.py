from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import datetime

from models.auth import auth
from models.tutlebot import turtlebot
from models.get import get
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

@router.get("/log", status_code=status.HTTP_200_OK)
def logAll(id:str, db: Session = Depends(get_db)):
    exist_user = db.query(auth).filter(auth.id == id).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")  # 아이디가 존재하지 않으면 예외 던지기
    logs = db.query(get).filter(get.auth_id == exist_user.auth_id).all()
    return logs

@router.post("/log-regist", status_code=status.HTTP_200_OK) # 실험용으로 만들어 본 것
def registlog(id:str, db: Session = Depends(get_db)):
    exist_user = db.query(auth).filter(auth.id == id).first()
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    log = get(auth_id=exist_user.auth_id, start_time=formatted_time, end_time=formatted_time, laundry_cnt=10)
    db.add(log)
    db.commit()
    db.close()