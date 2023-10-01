from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from typing import List

from models.auth import auth
from models.laundry import laundry
from models.dib import dib
from db.db import get_db

router = APIRouter(prefix="/dib")

# dib 할때 request body에 보낼꺼
class Info(BaseModel):
    user_id: str
    laundry_id: int


 # 사용자 찜 등록
 # 프론트에서 찜 등록 안되있으면 포스트로 보내서 등록
@router.post("/", status_code=status.HTTP_200_OK)
def registdib(info: Info, db: Session = Depends(get_db)):


    # 아이디가 존재하지 않으면 예외 던지기
    exist_user = db.query(auth).filter(auth.id == info.user_id).first()

    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    # 세탁물 존재 여부
    exist_laundry = db.query(laundry).filter(laundry.laundry_id == info.laundry_id).first()

    if not (exist_laundry):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 세탁물 입니다.")

    # 현재 찜이 되어있는지 판단
    exist_dib = db.query(dib).filter(dib.auth_id == exist_user.auth_id, dib.laundry_id == exist_laundry.laundry_id).first()
    if (exist_dib):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="프론트 탓입니다. delete로 요청보내세요")
    else:
        dib_item = dib(auth_id=exist_user.auth_id, laundry_id=info.laundry_id)
        db.add(dib_item)
        db.commit()

    db.close()

# 찜 삭제
# 찜 되어있는지 아닌지는 프론트에서 판단해서 요청 보내기
@router.delete("/{laundry_id}", status_code=status.HTTP_200_OK)
def deletedib(user_id:str, laundry_id:int, db:Session = Depends(get_db)):
    exist_user = db.query(auth).filter(auth.id == user_id).first()

    # 아이디가 존재하지 않으면 예외 던지기
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    # 세탁물 존재 여부
    exist_laundry = db.query(laundry).filter(laundry.laundry_id == laundry_id).first()

    if not (exist_laundry):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 세탁물 입니다.")

    # 삭제할 찜 있는지 판단
    dib_item = db.query(dib).filter(dib.auth_id == exist_user.auth_id, dib.laundry_id == exist_laundry.laundry_id).first()
    if (dib_item):
        db.delete(dib_item)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="프론트 탓입니다. post로 요청보내세요")
    db.close()


# 찜 목록 전체불러오기
# 주행페이지 이동시 찜되어있는건 프론트에서 ON 해놓기
@router.get("/", status_code=status.HTTP_200_OK)
def getdibs(id: str, db:Session = Depends(get_db)):

    exist_user = db.query(auth).filter(auth.id == id).first()
    # 아이디가 존재하지 않으면 예외 던지기
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    # 찜목록
    dibs = db.query(dib).filter(dib.auth_id == exist_user.auth_id).order_by(dib.laundry_id.asc()).all()

    if len(dibs) == 0:
        return None

    responses = []
    for dib_item in dibs:
        response = db.query(laundry).filter(laundry.laundry_id == dib_item.laundry_id).first()
        if response:
            responses.append(response)

    return responses


# 혹시몰라서, laundry다 가져오면서 찜여부 포함해서 넣기
@router.get("/list", status_code=status.HTTP_200_OK)
def getdibs(id: str, db:Session = Depends(get_db)):

    exist_user = db.query(auth).filter(auth.id == id).first()
    # 아이디가 존재하지 않으면 예외 던지기
    if not (exist_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="존재하지 않는 사용자 입니다.")

    # 찜목록 - laundry_id만 저장
    dibs = db.query(dib.laundry_id).filter(dib.auth_id == exist_user.auth_id).order_by(dib.laundry_id.asc()).all()


    #laundry 리스트 가져오기
    laundry_items = db.query(laundry).all()

    responses = []
    for laundry_item in laundry_items:
        is_dib = laundry_item.laundry_id in [dib[0] for dib in dibs]
        # is_dib 필드 추가
        setattr(laundry_item, 'is_dib', is_dib)
        responses.append(laundry_item)

    return responses






