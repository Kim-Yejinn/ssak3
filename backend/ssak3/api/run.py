from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import datetime
from pydantic import BaseModel
from typing import List

from models.auth import auth
from models.select import select
from models.get import get
from models.laundry import laundry
from db.db import get_db

router = APIRouter(prefix="/run")

class Start(BaseModel):
    id: str
    laundryList: List[int]


# 세탁물 주행시 선택되는 것들 반영해서 생성
@router.post("/start", status_code=status.HTTP_200_OK)
def registrun(start: Start, db: Session = Depends(get_db)):
    # 유저 확인
    exist_user = db.query(auth).filter(auth.id == start.id).first()

    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    laundry_ids = start.laundryList
    laundry_items = db.query(laundry).filter(laundry.laundry_id.in_(laundry_ids)).all()

    for laundry_id in laundry_ids:
        laundry_item = next((item for item in laundry_items if item.laundry_id == laundry_id), None)
        if not laundry_item:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"{laundry_id}번 세탁물은 존재하지 않는 세탁물입니다. index가 아닌 id값으로 잘 넣었는지 확인 바람")

    # 아니면 어짜피 동작중에는 실행을 못하니깐 생각해보면, auth_id에서 제일 최근 주행로봇의 end_time만 확인하면 될것같음
    first = db.query(get).filter(get.auth_id == exist_user.auth_id).order_by(get.get_id.desc()).first()
    # 사용기록이 있는데, end_time이 없다면 주행중
    if first and first.end_time == None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="로봇이 실행중입니다.")

    # 이제 로봇이 실행중이 아니거나, 첫사용자임

    try:
        # 1. get만들기 사용자번호, 시작시간만 넣어주기
        get_item = get(auth_id=exist_user.auth_id, start_time=datetime.now())
        db.add(get_item)
        db.flush()

        get_id = get_item.get_id

        # 2. request로 들어온 laundry_id로 select에다가 넣어주기
        for laundry_id in start.laundryList:
            select_item = select(get_id=get_id, laundry_id=laundry_id)
            db.add(select_item)

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error: {str(e)}")

    finally:
        db.close()

    return get_id


class Ros(BaseModel):
    index: int
    name: str
    cnt: int

class End(BaseModel):
    id: str
    get_id: int
    laundries: List[Ros]

# 주행 완료시 모든 데이터베이스 등록
# @router.patch("/end", status_code=status.HTTP_200_OK)
# def updaterun(end: End, db: Session = Depends(get_db)):
#     # 유저 확인
#     exist_user = db.query(auth).filter(auth.id == end.id).first()
#
#     if not (exist_user):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="존재하지 않는 사용자 입니다.")
#
#     # laundryList에 있는 값이 데이터 베이스에 잘 들어가 있는지 확인
#     for ros in end.laundries:
#         laundry_item = db.query(laundry).filter(laundry.laundry_ros == ros.name).first()
#         if not laundry_item:
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
#                                 detail="존재하지 않는 세탁물입니다. ros에서 받아오는 이름과 같지 않습니다.")
#
#     get_item = db.query(get).filter(get.get_id == end.get_id).first()
#     if len(get_item) == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="해당 로그가 존재하지 않습니다.")
#
#     if (get_item.end_time):
#         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
#                             detail="벌써 실행 완료 된 로그입니다. 다시 한번 확인해주세요.")
#
#
#     current_time = datetime.now()
#     formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
#
#     get_item.end_time = formatted_time
#



