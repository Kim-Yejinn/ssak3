from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import datetime
from pydantic import BaseModel

from models.laundry import laundry
from models.auth import auth
from models.tutlebot import turtlebot
from models.get import get
from models.select import select
from db.db import get_db

from api.sockethandler.ControlHandler import ControlHandler

router = APIRouter(prefix="/robot")


# robot 등록 Request객체
class robot(BaseModel):
    id: str
    serial_number: str


@router.post("/regist", status_code=status.HTTP_200_OK)  # 로봇 등록
def robotRegist(robot: robot, db: Session = Depends(get_db)):
    try:
        if robot.serial_number is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="입력을 확인하세요.")
        exist_user = db.query(auth).filter(auth.id == robot.id).first()
        if not (exist_user):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="존재하지 않는 사용자 입니다.")  # 아이디가 존재하지 않으면 예외 던지기
        turtle = turtlebot(auth_id=exist_user.auth_id, serial_number=robot.serial_number)
        db.add(turtle)
        db.commit()
    finally:
        db.close()


class User(BaseModel):
    id: str


@router.get("/exist", status_code=status.HTTP_200_OK)  # 유저에게 등록된 로봇있는지 확인
def robotExist(id: str, db: Session = Depends(get_db)):
    exist_user = db.query(auth).filter(auth.id == id).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")
    exist_robot = db.query(turtlebot).filter(turtlebot.auth_id == exist_user.auth_id).first()
    if not (exist_robot):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="등록된 터틀봇이 없습니다.")
    return {"id": exist_user.id, "serial_number": exist_robot.serial_number}


@router.get("/log", status_code=status.HTTP_200_OK)  # 로그 전체 가져오기
def logAll(id: str, db: Session = Depends(get_db)):
    exist_user = db.query(auth).filter(auth.id == id).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")  # 아이디가 존재하지 않으면 예외 던지기
    logs = db.query(get).filter(get.auth_id == exist_user.auth_id).order_by(get.start_time.desc()).all()
    return logs


@router.post("/log-regist", status_code=status.HTTP_200_OK)  # 실험용으로 만들어 본 로그 등록
def registlog(user: User, db: Session = Depends(get_db)):
    exist_user = db.query(auth).filter(auth.id == user.id).first()
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    log = get(auth_id=exist_user.auth_id, start_time=formatted_time, end_time=formatted_time, laundry_cnt=10)
    db.add(log)
    db.commit()
    db.close()


# 로그 삭제
@router.delete("/log/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    # 로그 정보 조회
    log = db.query(get).filter(get.get_id == log_id).first()

    if log:
        db.delete(log)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Log not found")
    db.close()


@router.post("/robot/run", status_code=status.HTTP_200_OK)
def robot_run(member_id: str, laundrys: list, time: int, db: Session = Depends(get_db)):
    # 로봇 동작 시작
    # 현재 로봇 아이디와, 리스트, 작동 시간을 주면 작동
    # 여기서는 바로 작동한다고 가정했다.???
    # 값 받아와서 로그 추가> 이미 위에서 만들어 져있는듯 한데..?
    exist_user = db.query(auth).filter(auth.id == member_id).first()
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    log = get(auth_id=exist_user.auth_id, start_time=formatted_time)
    db.add(log)
    db.commit()

    get_num = get_last_record_id()
    # 선택한 세탁물도 넣어야 함.
    for laundry_name in laundrys:
        laundry_id = db.query(laundry).filter(laundry_name == laundry.laundry_name).first().laundry_id
        laundry_log = select(get_id=get_num, laundry_id=laundry_id)
        db.add(laundry_log)
        db.commit()

    db.close()
    ControlHandler.emit_laundry_start(member_id, get_num, laundrys)
    return {"log_id": log.id}


def get_last_record_id(db: Session = Depends(get_db())):
    # 가장 큰 값 찾기 => 지금 수거 번호
    last_record = db.query(get).order_by(get.get_id.desc()).first()
    if last_record:
        return last_record.id
    return None
