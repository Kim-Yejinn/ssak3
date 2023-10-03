import socketio

from fastapi import Depends
from sqlalchemy.orm import Session
from db.db import get_db

from models.turtlebot import turtlebot
from models.get import get



def findUser(num: int, db: Session = Depends(get_db)):
    user = db.query(turtlebot).filter(turtlebot.turtlebot_id == num).first()
    return user



class ControlHandler(socketio.AsyncNamespace):


    async def on_connect(self, sid, environ):
        print("control connected")

    async def on_disconnect(self, sid):
        print("control disconnected")

    # 세탁물 정보 확인
    async def on_result(self, sid, data):
        # 결과가 json으로 들어온다고 가정함
        from api.run import updaterun
        from api.run import Ros
        from api.run import End
        # 총 개수와 터틀봇 번호로 들어왔다면 (String으로)
        turtlebot_no = data['turtlebot_no']

        # ros 응답 형태 확인 후 수정해야 함.
        # ros에는 name : cnt 형태로 보내야 할듯

        user = findUser(turtlebot_no)

        if (user):
            end = End()
            end.get_id = sid
            end.id = user

            # 응답 확인 후 수정
            end.laundries.append(Ros('skirts', data['skirts']))
            end.laundries.append(Ros('pants', data['pants']))

            updaterun(end)
