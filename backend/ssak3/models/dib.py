from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.db import Base

class dib(Base):
    __tablename__ = "dib"

    dib_id = Column(Integer, primary_key=True, autoincrement=True)
    auth_id = Column(Integer, ForeignKey("auth.auth_id"), nullable=False)
    laundry_id = Column(Integer, ForeignKey("laundry.laundry_id"), nullable=False)
