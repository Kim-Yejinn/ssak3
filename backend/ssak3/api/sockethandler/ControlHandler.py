

import socketio

from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime

from db.db import get_db

from models.tutlebot import turtlebot
from models.get import get


def updatelog(operate_no: str, result_cnt : str,  db: Session = Depends(get_db())):

    # 터틀봇 번호로 사용자를 찾고
    # user_no = db.query(turtlebot).filter(turtlebot.serial_number == turtlebot_no).first().auth_id
    # # 사용자의 마지막 로그를 가져와
    # last_item = db.query(db.query(get).filter(user_no == get.auth_id).order_by(desc(get.get_id)).first())
    # # 카운트랑 완료 시간도 넣는다.
    # last_item.laundry_cnt = result_cnt
    # last_item.end_time = datetime.now()
    # # 업데이트 한다
    # db.commit()

    # =====
    # 애초에 작업을 시킬때 수거 번호를 저장하고 있으면 안되는 건가?
    last_item = db.query(get).filter(operate_no == get.get_id).first()
    last_item.laundry_cnt = result_cnt

    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    last_item.end_time =formatted_time
    # # 업데이트 한다
    db.commit()
    db.close()

class ControlHandler(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ):
        print("control connected")

    async def on_disconnect(self, sid):
        print("control disconnected")



    # 세탁물 정보 확인
    async def on_result(self,sid,data):
        
        # 결과가 json으로 들어온다고 가정함

        # 총 개수와 작동 번호로 들어왔다면 (String으로)
        result_cnt = data['result']
        turtlebot_no = data['operateNo']
        # 값을 업데이트 해주고
        updatelog(turtlebot_no, result_cnt)


    # 세탁 시작
    async def emit_laundry_start(self,member_id, op_id, laundry):
        # 수거해야 할 목록도 보내야 함.
        # db에서 언제 요청을 해야 하는가? - 요청후 바로

        # id를 이용해서 해당 터틀봇만 작동하는 코드 추가하기

        # 현재 작동 번호도 같이 보내기
        obj = {"laundry": laundry, "op_id" : op_id}
        await self.emit("laundry_start", obj)
