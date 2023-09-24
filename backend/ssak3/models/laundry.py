from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from db.db import Base

class laundry(Base):
    __tablename__ = "laundry"

    laundry_id = Column(Integer, primary_key=True, autoincrement=True)
    laundry_name = Column(String, nullable=False)
    laundry_type = Column(String, nullable=False)
