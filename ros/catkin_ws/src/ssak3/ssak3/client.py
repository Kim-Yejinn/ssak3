import socketio
import asyncio

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import threading

sio=None
# sio = socketio.AsyncClient()

class socketSub(Node):

    def __init__(self):
        super().__init__('socket_sub')
        self.socket_day = self.create_subscription(String, '/socket_day', self.socket_day_pub, 20)
        self.socket_temp = self.create_subscription(String, '/socket_temp', self.socket_temp_pub, 10)
        self.socket_weather = self.create_subscription(String, '/socket_weather', self.socket_weather_pub, 10)


    # 위의 subscription 등록 이후 각 기능을 아래에 추가하면 됩니다.
    # 우선은 String을 기준으로 작성했고, 이후 Json추가 예정

    # namespace는
    # auth - 터틀봇 번호 인증
    # env - 날씨, 시간, 온도 정보 보냄
    # control - 제어 관련 정보
    #   - result : 수거 완료 정보
    #   - laundry_start : 수거 목록 수신 및 시작 요청

    # 이외에는 back에서 추가 필요

    async def socket_day_pub(self, msg):
        global sio
        print("..")
        if sio:
            print(msg)  
            await sio.emit('turtlebot_time', msg.data, namespace = '/env')

    async def socket_temp_pub(self, msg):
        global sio
        if sio:
            await sio.emit('turtlebot_temp', msg.data, namespace = '/env')

    async def socket_weather_pub(self, msg):
        global sio
        if sio:
            await sio.emit('turtlebot_weather', msg.data, namespace = '/env')


async def client():
    global sio
    # 클라이언트 소켓 생성
    sio = socketio.AsyncClient()
    # 테스트 값
    turtlebotNo = 123
    print("start")
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
    auth_url = 'http://127.0.0.1:8000'
    await sio.connect(auth_url, namespaces =['/', '/env', '/auth', '/control'])


    # 테스트
    # await sio.emit('turtlebot_time', 'test0', namespace = '/env')

    await sio.wait()


def main(args = None):
    # rclpy.init(args=args)
    # socket_node = socketSub()

    # # 이벤트 루프 내에서 클라이언트와 노드 실행
    # loop = asyncio.get_event_loop()
    # loop.create_task(client())
    # rclpy.spin(socket_node)

    rclpy.init(args=None)

    socket_node = socketSub()
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(socket_node)

    # client_thread = threading.Thread(target=asyncio.run, args=(client(),))
    # client_thread.start()  # 클라이언트 함수를 스레드로 실행


    client_thread =threading.Thread(target=asyncio.run, args=(client(),))  # asyncio.ensure_future()를 사용하여 클라이언트 함수를 실행
    client_thread.start()
    
    executor.spin()

    # await asyncio.gather(
    #     client(),  # client() 함수 실행
    #     executor.spin()  # 노드 실행
    # )

    # task1 = asyncio.create_task(run(client()))
    # task2 = asyncio.create_task(rclpy.spin(socket_node)) 
    
    # await asyncio.gather(task1, task2)

    socket_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    # asyncio.create_task(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # t= asyncio.run(main())
    # temp = main()
    # start()
    # asyncio.run(start())
    main()