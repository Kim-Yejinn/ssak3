import httpx
import socketio

from sqlalchemy.orm import Session
from db.db import get_db

from models.turtlebot import turtlebot
from models.auth import auth

# authid 구하기
def finduser(num: str):
    db: Session = next(get_db())
    user = db.query(turtlebot).filter(turtlebot.serial_number == num).first()
    return user.auth_id

# 유저 id 구하기
def findid(num: int):
    db: Session = next(get_db())
    id = db.query(auth).filter(auth.auth_id == num).first()
    return id.id

class ControlHandler(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ):
        print("control connected")

    async def on_disconnect(self, sid):
        print("control disconnected")

    # 세탁물 정보 확인
    async def on_result(self, sid, data):
        operate_no = data['operateNo']
        serial_no = data['serialNo']
        result_list = data['result']

        user = finduser(str(serial_no))
        id = findid(user)

        if (user):
            result = []
            result.append({"name":"shirts", "cnt":int(result_list[0])})
            result.append({"name":"pants", "cnt":int(result_list[1])})

            # 응답 확인 후 수정
            # 로컬
            # url = "http://127.0.0.1:8000/run/end"

            # 서버
            url = "https://https://j9b201.p.ssafy.io/api/run/end"

            async with httpx.AsyncClient() as client:
                response = await client.patch(url, json = {"id":id, "get_id":operate_no, "laundries":result})
                
                if response.status_code == 200:
                    print("동작 저장")
                else:
                    print("동작 저장 실패")
