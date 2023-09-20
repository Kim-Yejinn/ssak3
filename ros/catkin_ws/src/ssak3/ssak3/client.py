import socketio
import asyncio

async def client():
    # 클라이언트 소켓 생성
    sio = socketio.AsyncClient()


    # 연결
    @sio.event
    async def connect():
        print('connection established')

    @sio.event
    async def disconnect():
        print('disconnected from server')

    # 데이터 수신 콜백함수
    @sio.on('testcallback')
    async def aircon_on(data):
        print('message received with ', data)


    # 서버 연결
    await sio.connect('http://127.0.0.1:8000')

    # 데이터 송신
    await sio.emit('test','TEST')

    await sio.wait()

def main(args = None):
    asyncio.run(client())

if __name__ == "__main__":
    main() 