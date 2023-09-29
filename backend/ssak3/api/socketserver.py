import socketio
from api.sockethandler.EnvHandler import EnvHandler
from api.sockethandler.ControlHandler import ControlHandler
from api.sockethandler.AuthHandler import AuthHandler

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origin='*')

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='socket.io'
)

sio_server.register_namespace(EnvHandler('/env'))
sio_server.register_namespace(ControlHandler('/control'))
sio_server.register_namespace(AuthHandler('/auth_turtle'))


# 서버 자체 연결과 관련된 이벤트 처리
@sio_server.event
async def connect(sid, environ, auth=None):
    print("server Connected")


@sio_server.event
async def disconnect(sid):
    print("server Disconnect")
