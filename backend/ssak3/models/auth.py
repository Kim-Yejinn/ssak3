from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, validator, EmailStr

from db.db import Base


class auth(Base):
    __tablename__ = "auth"

    auth_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, unique=True,  nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

# class Token(BaseModel):
#     access_token: str
#     refresh_token: str
#     username: str