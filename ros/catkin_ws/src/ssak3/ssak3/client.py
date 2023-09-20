import socketio

# 클라이언트 소켓 생성
sio = socketio.Client()


# 연결
@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

# 데이터 수신 콜백함수
@sio.on('testcallback')
def aircon_on(data):
    print('message received with ', data)


# 서버 연결
sio.connect('http://127.0.0.1:8000')

# 데이터 송신
sio.emit('test','TEST')

sio.wait()