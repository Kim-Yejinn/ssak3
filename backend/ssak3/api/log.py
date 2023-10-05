from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional

from models.auth import auth
from models.get import get
from models.select import select
from models.laundry import laundry
from db.db import get_db

router = APIRouter(prefix="/log")

# 로그안에 세탁물 디테일
class Detail(BaseModel):
    idx: int
    name: str
    cnt: int

# 진행완료된 로그들
class Log(BaseModel):
    get_id: int
    get_name: str
    laundry_cnt: int
    laundries: List[Detail]
    start_time: str
    end_time: str
    total_time: str

# 진행중인 로그
class LogInProgress(BaseModel):
    get_id: int
    get_name: str
    expected_time: Optional[str]
    start_time: str

# 제일 큰 단위
class LogList(BaseModel):
    log_in_progress: Optional[LogInProgress] = None
    log: List[Log]

@router.get("", status_code=status.HTTP_200_OK)
def getlog(id: str, db: Session = Depends(get_db)):

    # 변수 초기화 ( 예상시간 )
    log_cnt = 0
    log_time_sum = timedelta()

    # 유저 확인
    exist_user = db.query(auth).filter(auth.id == id).first()

    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    # 로그들 아이디별 정렬
    log_items = db.query(get).filter(get.auth_id==exist_user.auth_id).order_by(get.get_id.desc()).all()

    response = LogList(
        log=[]
    )

    for log_item in log_items:
        # 진행중인 로그가 있다면
        if not log_item.end_time:

            start = log_item.start_time.strftime('%H:%M')
            response.log_in_progress = LogInProgress(
                get_id=log_item.get_id,
                get_name=log_item.get_name,
                start_time=start
            )
        # 진행완료된 로그들
        else:
            # 통계치를 위한 예상시간 계산
            log_cnt += 1
            log_time_sum += log_item.end_time - log_item.start_time

            # 개별 로그 들에 들어갈 세탁물 정리
            laundry_items = []

            # select랑 laundry랑 조인해서 세탁물 이름, 개수 가져오기
            select_items = (db.query(select, laundry)
                            .join(select, select.laundry_id == laundry.laundry_id)
                            .filter(select.get_id == log_item.get_id)
                            .all())

            for select_item in select_items:
                laundry_item = Detail(
                    idx=select_item[1].laundry_id,
                    name=select_item[1].laundry_name,
                    cnt=select_item[0].cnt
                )
                laundry_items.append(laundry_item)

            start = log_item.start_time.strftime('%H:%M')
            end = log_item.end_time.strftime('%H:%M')

            # total_time_delta = timedelta()
            time_delta = log_item.end_time-log_item.start_time
            total_time_delta = int(time_delta.total_seconds())

            total_time = ""

            if total_time_delta >= (60 * 60 * 24):
                total_time = f"{total_time_delta // (60 * 60 * 24)}일 "
            elif total_time_delta >= 60 * 60:
                total_time = f"약 {total_time_delta // (60 * 60)}시간 "
            elif total_time_delta >= 0:
                total_time = f"{total_time_delta // 60}분 "
            else:
                total_time = f"{total_time_delta}초"


            # 로그 추가
            log_instance = Log(
                get_id=log_item.get_id,
                get_name=log_item.get_name,
                laundry_cnt=log_item.laundry_cnt,
                laundries=laundry_items,
                start_time=start,
                end_time=end,
                total_time=total_time
            )
            response.log.append(log_instance)

    # 마지막 예상시간 반영 but 진행중인 로그가 있거나, 세탁물이 없지 않다면 추가
    if response.log_in_progress and log_cnt != 0:
        expect = int(log_time_sum.total_seconds()) // log_cnt
        response.log_in_progress.expected_time = timetransition(expect)

    return response

def timetransition(total_time_delta: int):
    total_time = ""

    day = total_time_delta // (60 * 60 * 24)
    total_time_delta %= 60 * 60 * 24
    hour = total_time_delta // (60 * 60)
    total_time_delta %= (60 * 60)
    minute = total_time_delta // 60
    total_time_delta %= 60
    second = total_time_delta

    if day != 0:
        total_time += f"{day}일 "
    if hour != 0:
        total_time += f"{hour}시간 "
    if minute != 0:
        total_time += f"{minute}분 "
    if second == 0:
        if len(total_time) == 0:
            total_time += f"{second}초"
    else:
        total_time += f"{second}초"

    return total_time


@router.delete("/{get_id}", status_code=status.HTTP_200_OK)
def deletelog(auth_id: str, get_id: int, db: Session = Depends(get_db)):

    # 유저 확인
    exist_user = db.query(auth).filter(auth.id == auth_id).first()

    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    log = db.query(get).filter(get.get_id == get_id).first()

    # 삭제된 로그가 아닌지 확인
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="이미 삭제된 로그입니다.")

    # 로그 권한 확인
    if not log.auth_id == exist_user.auth_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="권한이 없습니다.")

    # 삭제 transaction 시작
    try:
        # 자식 삭제
        db.query(select).filter(select.get_id == log.get_id).delete()

        # 부모 삭제
        db.delete(log)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error: {str(e)}")

    finally:
        db.close()