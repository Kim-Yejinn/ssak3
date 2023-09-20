import socketio
import asyncio

sio_client = socketio.AsyncClient()


@sio_client.event
async def connect():
    print(' connected')


@sio_client.event
async def disconnect():
    print(' disconnected')



# 테스트 코드
async def main():
    await sio_client.connect(url='http://localhost:8000', socketio_path='socket.io')
    await sio_client.emit('test', 'Hello from client')
    await sio_client.disconnect()


asyncio.run(main())
