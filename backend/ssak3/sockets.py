import socketio

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origin='*')

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='socket.io'
)


@sio_server.event
async def connect(sid, environ, auth = None):
    print("connected!!!")
    pass
@sio_server.event
async def disconnect(sid):
    print("disconnected!!!")
    pass

@sio_server.event
async def my_event(sid, data):
    print(data)
    pass


@sio_server.on('test')
async def handle_test(sid, data):
    print("back 테스트(back/ros to back)")
    print(data)
    pass


@sio_server.on('testros')
async def ros_test(sid, data):
    print("ros 테스트(back to ros)")
    await sio_server.emit('testcallback', "ros TEST")
