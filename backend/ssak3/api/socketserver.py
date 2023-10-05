import socketio
from api.sockethandler.EnvHandler import EnvHandler
from api.sockethandler.ControlHandler import ControlHandler

from fastapi import Depends
from sqlalchemy.orm import Session
from models.turtlebot import turtlebot
from db.db import get_db

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origin='*',
    ping_timeout=500
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path=''
)



# 서버 자체 연결과 관련된 이벤트 처리
@sio_server.event
async def connect(sid, environ, auth=None):
    # import uuid
    # custom_sid = str(uuid.uuid4())
    print("server Connected")
    # print(sid)
    # await sio_server.emit('custom_sid', custom_sid)



@sio_server.event
async def disconnect(sid):
    print("server Disconnect")


# 터틀봇 인증 및 연결 관리
class AuthHandler(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        print("auth connected")
        # print(sid)

    async def on_disconnect(self, sid):
        print("auth disconnected")
        # print(sid)

    async def on_authenticate(self, client_sid, data):
        # 등록된 터틀봇 번호인지 확인
        # data로 turtlebotNo가 번호가 들어감
        print("try turtlebot auth")
        print(data)
        # auth_data = 123
        # print(auth_data)

        # 테스트용 데이터
        # 보낼때 int로 보내면 int로 옴.
        print(type(data))
        # print(type(auth_data))

        # if exist_turtlebot(data):
        #     print("auth success")
        #
        #     # 모든 namespace에 터틀봇 추가
        #     # for namespace in sio_server.namespace_handlers.values():
        #     #     namespace.enter_room(custom_id, data)
        #
        # else:
        #     print("auth fail")
        #     await sio_server.disconnect(client_sid)
        #     await sio_server.emit('auth_fail', 'fail')

        print("finish")


# 거북이 등록 되어있는지 확인
def exist_turtlebot(turtlebot_no: int, db: Session = Depends(get_db)):
    log = db.query(turtlebot).filter(turtlebot.turtlebot_id == turtlebot_no).first()

    if log:
        # 있을 경우
        return True
    else:
        return False


# name space 등록
sio_server.register_namespace(EnvHandler('/env'))
sio_server.register_namespace(ControlHandler('/control'))
sio_server.register_namespace(AuthHandler('/auth_turtle'))


async def emit_laundry_start(member_id, op_id, laundry):
    # 수거해야 할 목록과 시작 요청.
    # 해당 작동 번호도 함께 보냄 -> 나중에 수정을 위함

    # id를 이용해서 해당 터틀봇만 작동하는 코드 추가하기
    print(member_id)

    obj = {"laundry": laundry, "op_id": int(op_id)}
    await sio_server.emit("laundry_start", obj)
