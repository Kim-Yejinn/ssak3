from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional

from models.auth import auth
from models.schedule import schedule
from db.db import get_db

router = APIRouter(prefix="/schedule")

class Info(BaseModel):
    auth_id: str
    title: Optional[str] = "alarm"
    meridiem: int
    hour: int
    minute: int
    date: Optional[List[int]] = [0, 1, 2, 3, 4, 5, 6]
    # 0: 월, 1: 화, 2: 수, 3: 목, 4: 금, 5: 토, 6: 일
    # meridiem = 0: 'AM', 1: 'PM'

# 스케줄 등록
@router.post("/", status_code=status.HTTP_200_OK)
def registSchedule(info: Info, db: Session = Depends(get_db)):
    # 유저확인
    exist_user = db.query(auth).filter(auth.id == info.auth_id).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    try:
        # 등록시간
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        # 설정 날짜 포맷팅
        schedule_date = ""

        for day in info.date:
            schedule_date += f"{day}"

        if info.meridiem == 1:
            if info.hour != 12:
                info.hour += 12
        elif info.hour == 12:
            info.hour -= 12

        schedule_item = schedule(auth_id=exist_user.auth_id, title=info.title, created_at=formatted_time, hour=info.hour, minute=info.minute, date=schedule_date)
        db.add(schedule_item)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error: {str(e)}")

    finally:
        db.close()

class Item(BaseModel):
    id: int
    title: str
    type: int
    time: str
    day: str

# 스케줄 다 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
def getSchedule(auth_id:str, db:Session = Depends(get_db)):
    # 유저확인
    exist_user = db.query(auth).filter(auth.id == auth_id).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    responses = []

    schedule_items = db.query(schedule).filter(schedule.auth_id == exist_user.auth_id).order_by(schedule.created_at.desc()).all()
    # if not schedule_items:
    #     return None
    for schedule_item in schedule_items:

        response = Item(
            id=schedule_item.schedule_id,
            title=schedule_item.title,
            type=schedule_item.type,
            time=timeTransition(schedule_item.hour, schedule_item.minute),
            day=days(schedule_item.date)
        )
        responses.append(response)

    return responses

# 24시를 12시로 변환
def timeTransition(hour:int, minute_int: int):
    # 24시 12시로 변환
    minute = ""

    # 시간
    if hour >= 12:
        meridiem = "PM"
        if hour != 12:
            hour -= 12
    else:
        meridiem = "AM"
        if hour == 0:
            hour = 12

    if minute_int < 10:
        minute = f"0{minute_int}"

    return f"{hour} : {minute} {meridiem}"

# 날짜 변환
def days(date: str):
    day_bool = [False] * 7
    day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    result = ""

    if len(date) == 7:
        return "every day"
    if len(date) == 1:
        return f"every {day[int(date)]}"
    for day_instance in list(date):
        day_bool[int(day_instance)] = True

    if len(date) == 2:
        if day_bool[5] and day_bool[6]:
            return "every weekend"
    if len(date) == 5:
        check = True
        for i in range(5):
            if not day_bool[i]:
                check = False
                break
        if check:
            return "every weekdays"

    for i in range(7):
        if day_bool[i]:
            result += f"{day[i]} "
    return result

class ScheduleResponse(BaseModel):
    id: int
    title: str
    hour: int
    minute: int
    meridiem: int
    date: List[int]
# meridiem AM: 0, PM: 1

# 스케줄 상세 조회
@router.get("/{schedule_id}", status_code=status.HTTP_200_OK)
def getScheduleDetail(auth_id:str, schedule_id: int, db:Session = Depends(get_db)):
    # 유저확인
    exist_user = db.query(auth).filter(auth.id == auth_id).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    schedule_item = db.query(schedule).filter(schedule.schedule_id == schedule_id).first()

    if not schedule_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="스케줄 내역이 없습니다.")

    if schedule_item.auth_id != exist_user.auth_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="권한이 없습니다.")

    # 24시 12시로
    hour = schedule_item.hour
    meridiem = 0

    if hour >= 12:
        meridiem = 1
        if hour != 12:
            hour -= 12
    else:
        if hour == 0:
            hour = 12

    # date str을 list로 변환
    dates = []
    date_bool = [False] * 7
    for date in list(schedule_item.date):
        date_bool[int(date)] = True

    for i in range(7):
        if date_bool[i]:
            dates.append(i)

    response = ScheduleResponse(
        id=schedule_item.schedule_id,
        title=schedule_item.title,
        hour=hour,
        minute=schedule_item.minute,
        meridiem=meridiem,
        date=dates
    )

    return response

# 스케줄 삭제
@router.delete("/{schedule_id}", status_code=status.HTTP_200_OK)
def deleteSchedule(auth_id: str, schedule_id: int, db: Session = Depends(get_db)):
    # 유저확인
    exist_user = db.query(auth).filter(auth.id == auth_id).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    schedule_item = db.query(schedule).filter(schedule.schedule_id == schedule_id).first()

    if not schedule_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="스케줄 내역이 없습니다.")

    if schedule_item.auth_id != exist_user.auth_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="권한이 없습니다.")

    try:
        db.delete(schedule_item)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error: {str(e)}")
    finally:
        db.close()

class Update(BaseModel):
    auth_id: str
    title: str
    meridiem: int
    hour: int
    minute: int
    date: List[int]

# 스케줄 수정
@router.patch("/{schedule_id}", status_code=status.HTTP_200_OK)
def updateSchedule(update: Update, schedule_id:int, db: Session = Depends(get_db)):
    # 유저확인
    exist_user = db.query(auth).filter(auth.id == update.auth_id).first()
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    schedule_item = db.query(schedule).filter(schedule.schedule_id == schedule_id).first()

    if not schedule_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="스케줄 내역이 없습니다.")

    if schedule_item.auth_id != exist_user.auth_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="수정 권한이 없습니다.")

    try:
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        # 설정 날짜 포맷팅
        schedule_date = ""

        for day in update.date:
            schedule_date += f"{day}"

        if update.meridiem == 1:
            if update.hour != 12:
                update.hour += 12
        elif update.hour == 12:
            update.hour -= 12

        # 저장
        schedule_item.title = update.title
        schedule_item.created_at = formatted_time
        schedule_item.hour = update.hour
        schedule_item.minute = update.minute
        schedule_item.date = schedule_date

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error: {str(e)}")

    finally:
        db.close()


