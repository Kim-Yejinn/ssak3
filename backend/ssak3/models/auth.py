from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class auth(Base):
    auth_id: int
    id: str
    name: str
    password: str