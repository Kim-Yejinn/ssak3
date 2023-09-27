from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from db.db import Base

class select(Base):
    __tablename__ = "select"

    select_id = Column(Integer, primary_key=True, autoincrement=True)
    get_id = Column(Integer, ForeignKey("get.get_id"), nullable=False)
    laundry_id = Column(Integer, ForeignKey("laundry.laundry_id"), nullable=False)
