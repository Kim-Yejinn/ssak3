import socketio

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origin='*')

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='socket.io'
)


@sio_server.event
async def connect(sid, environ, auth):
    print("connected!!!")


@sio_server.event
async def my_event(sid, data):
    print(data)
    pass


@sio_server.on('test')
async def handle_test(sid, data):
    print("tt")
    print(data)
