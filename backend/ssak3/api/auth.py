# from fastapi import APIRouter
# from fastapi import Depends
# from sqlalchemy.orm import Session
# from starlette import status

# from models.auth import auth
# from db.db import session

# router = APIRouter(prefix="/auth")

# @router.post("/sign-up", status_code=status.HTTP_200_OK)
# def signUp(id: str, name: str, password: str):
#     db = session()
#     try:
#         user = auth(id=id, name=name, password=password)
#         db.add(user)
#         db.commit()
#     finally:
#         db.close()
