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

class Run(BaseModel):
    id: str
    laundryList: List[int]


# 세탁물 주행시 선택되는 것들 반영해서 생성
@router.post("/", status_code=status.HTTP_200_OK)
def registrun(run: Run, db: Session = Depends(get_db)):
    # 유저 확인
    exist_user = db.query(auth).filter(auth.id == run.id).first()

    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")
    
    # laundryList에 있는 값이 데이터 베이스에 잘 들어가 있는지 확인
    for laundry_id in run.laundryList:
        laundry_item = db.query(laundry).filter(laundry.laundry_id==laundry_id).first()
        if not laundry_item:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="존재하지 않는 세탁물입니다. index가 아닌 id값으로 잘 넣었는지 확인 바람")

    # # 실행중인 로봇이 있다면 막아주기 (근데 첫사용자는 걸러줘야함)
    # is_first = db.query(get).filter(get.auth_id == exist_user.auth_id).first()
    # if (is_first):
    #     is_run = db.query(get).filter(get.auth_id == exist_user.auth_id, get.end_time == None).first()
    #     if not (is_run):
    #         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #                             detail="로봇이 실행중입니다.")

    # 아니면 어짜피 동작중에는 실행을 못하니깐 생각해보면, auth_id에서 제일 최근 주행로봇의 end_time만 확인하면 될것같음
    first = db.query(get).filter(get.auth_id == exist_user.auth_id).order_by(get.get_id.desc()).first()
    # 사용기록이 있는데, end_time이 없다면 주행중
    if first and first.end_time == None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="로봇이 실행중입니다.")

    # 이제 로봇이 실행중이 아니거나, 첫사용자임

    # 1. get만들기 사용자번호, 시작시간만 넣어주기
    get_item = get(auth_id=exist_user.auth_id, start_time=datetime.now())
    db.add(get_item)
    db.commit()

    get_id = get.get_id

    # 2. request로 들어온 laundry_id로 select에다가 넣어주기
    for laundry_id in run.laundryList:
        select_item = select(get_id=get_id, laundry_id=laundry_id)
        db.add(select_item)
    db.commit()








