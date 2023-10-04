from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, SmallInteger

from db.db import Base

class schedule(Base):
    __tablename__ = "schedule"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    auth_id = Column(Integer, ForeignKey("auth.auth_id"), nullable=False)
    title = Column(String, nullable=False, default="alarm")
    created_at = Column(DateTime, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)
    date = Column(String)
    type = Column(SmallInteger, nullable=False, default=1)
