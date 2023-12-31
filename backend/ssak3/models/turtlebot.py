from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from db.db import Base

class turtlebot(Base):
    __tablename__ = "turtlebot"

    turtlebot_id = Column(Integer, primary_key=True, autoincrement=True)
    auth_id = Column(Integer, ForeignKey('auth.auth_id')) #db테이블 이름 써야 함
    serial_number = Column(String, nullable=False)
    turtlebot_status = Column(Integer, nullable=False, default=0)
