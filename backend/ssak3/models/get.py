from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from db.db import Base

class get(Base):
    __tablename__ = "get"

    get_id = Column(Integer, primary_key=True, autoincrement=True)
    auth_id = Column(Integer, ForeignKey("auth.auth_id"), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    laundry_cnt = Column(Integer, nullable=False, default=0)
