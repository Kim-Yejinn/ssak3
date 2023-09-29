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

    if len(start.laundryList) == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="세탁물을 한개 이상 선택해주세요.")

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
    name: str
    cnt: int

class End(BaseModel):
    id: str
    get_id: int
    laundries: List[Ros]

# 주행 완료시 모든 데이터베이스 등록
@router.patch("/end", status_code=status.HTTP_200_OK)
def updaterun(end: End, db: Session = Depends(get_db)):
    # 유저 확인
    exist_user = db.query(auth).filter(auth.id == end.id).first()

    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    get_item = db.query(get).filter(get.get_id == end.get_id).first()
    if len(get_item) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="해당 로그가 존재하지 않습니다.")

    if (get_item.end_time):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="벌써 실행 완료 된 로그입니다. 다시 한번 확인해주세요.")

    # 저장 transaction 시작
    try:
        # laundry_cnt 변수 설정
        sum = 0

        # 1. get_item end_time 저장
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        get_item.end_time = formatted_time

        # 2. query로 selected 찾아서 cnt 수정
        ros_items = end.laundries
        laundry_names: List[str]

        for ros_name in ros_items:
            laundry_names.append(ros_name)

        # join해서 get_id에 해당하는 select_id를 가져오기
        select_items = (db.query(select, laundry)
                       .join(select, select.laundry_id == laundry.laundry_id)
                       .filter(select.get_id == end.get_id,
                               laundry.laundry_ros.in_(laundry_names))
                       .all())

        for ros in ros_items:
            name = ros.name
            cnt = ros.cnt
            select_item = next((item for item in select_items if item[1].laundry_ros == name), None)
            if not select_item:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail=f"{Ros.name} 세탁물은 존재하지 않는 세탁물입니다. index가 아닌 id값으로 잘 넣었는지 확인 바람")
            else:
                sum += cnt
                select_item[0].cnt = cnt

        # 3. cnt 다 합해서 get_item laundry_cnt수정
        get_item.laundry_cnt = sum
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error: {str(e)}")

    finally:
        db.close()

