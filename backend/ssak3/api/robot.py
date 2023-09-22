import os
from datetime import datetime, timedelta
from typing import Tuple

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from models.auth import auth
from db.db import get_db

router = APIRouter(prefix="/robot")
# @router.post("/regist", status_code=status.HTTP_200_O)
# def robotRegist(id: str, number: str, db: Session = Depends(get_db)):
#     db.