import socketio
import asyncio

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

sio = None

class socketSub(Node):

    def __init__(self):
        super().__init__('socket_sub')
        self.socket_day = self.create_subscription(String, '/socket_day', self.socket_day_pub, 20)
        self.socket_temp = self.create_subscription(String, '/socket_temp', self.socket_temp_pub, 10)
        self.socket_weather = self.create_subscription(String, '/socket_weather', self.socket_weather_pub, 10)


    async def socket_day_pub(self, msg):
        global sio
        await sio.emit('turtlebot_time', msg, namespace = '/env')

    async def socket_temp_pub(self, msg):
        global sio
        await sio.emit('turtlebot_temp', msg, namespace = '/env')

    async def socket_weather_pub(self, msg):
        global sio
        await sio.emit('turtlebot_weather', msg, namespace = '/env')


async def client():
    global sio
    # 클라이언트 소켓 생성
    sio = socketio.AsyncClient()
    # 테스트 값
    turtlebotNo = 123

    # 연결
    @sio.event
    async def connect():
        print('connection established')
        # 연결할때 인증 시작
        await sio.emit('authentication', turtlebotNo)        

    @sio.event
    async def disconnect():
        print('disconnected from server')



    # 데이터 수신
    @sio.on('laundry_start')
    async def laundry_start(data):
        print('message received with ', data)


    # 서버 연결
    # namespace : socket.io
    auth_url = 'http://127.0.0.1:8000'
    await sio.connect(auth_url)


    # 터틀 봇 id 연결

    # 송신 테스트
    # await sio.emit('test','TEST')

    await sio.wait()

def main(args = None):
    rclpy.init(args = args)
    socket_node = socketSub()
    asyncio.run(client())
    rclpy.spin(socket_node)


if __name__ == "__main__":
    main() 