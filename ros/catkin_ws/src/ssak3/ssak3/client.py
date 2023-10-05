import socketio
import asyncio
import ssl
import aiohttp
import requests

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from ssafy_msgs.msg import LaundryList, Result, Finish

import threading

import json

sio = None
connected = False
serialNo = "qwe123qwe123"
operateNo = None

# 나중에 turtlebot_status에서 한번만 보내도록 바꾸기
sendWeather = False
sendTemp = False
sendDay = False

laundry_list_msg = LaundryList()
laundry_send = False



class socketSub(Node):

    def __init__(self):
        super().__init__('socket_sub')
        self.socket_day = self.create_subscription(String, '/socket_day', self.socket_day_pub, 20)
        self.socket_temp = self.create_subscription(String, '/socket_temp', self.socket_temp_pub, 10)
        self.socket_weather = self.create_subscription(String, '/socket_weather', self.socket_weather_pub, 10)
        # 세탁물 수거 결과 값 입력 받으면 실행할 것 -> 해당 파일에서 여기로 보내는것 추가해야 함
        # 우선 수거 개수가 String으로 온다고 가정했음. 
        self.socket_result_sub = self.create_subscription(Result, 'result_list', self.socket_result_pub, 10)
        # 세탁물 수거 시작 시 어디로 가야 할지 여기에 publish 추가하기
        self.socket_start_pub = self.create_publisher(LaundryList, 'socket_start', 30)
        time_period = 0.1
        self.timer = self.create_timer(time_period, self.timer_callback)
        self.is_finish_sub = self.create_subscription(Finish, 'is_finish', self.finish_callback, 1)

    def finish_callback(self, msg):
        if msg.is_finish == True:
            global sio
            global connected
            global operateNo
            global serialNo

            url = "https://j9b201.p.ssafy.io/api/run/end"

            # Request Body 데이터
            data = {
                "id": "qwe123",
                "get_id": operateNo,
                "laundries": [
                    {
                        "name": "shirts",
                        "cnt": 1
                    },
                    {
                        "name": "pants",
                        "cnt": 1
                    }
                ]
            }

            # PATCH 요청 보내기
            response = requests.patch(url, json=data)

            # 응답 확인
            if response.status_code == 200:
                print("PATCH 요청이 성공적으로 보내졌습니다.")
                print("응답 내용:", response.text)
            else:
                print("PATCH 요청에 실패했습니다.")
                print("상태 코드:", response.status_code)


    async def timer_callback(self):
        global laundry_send
        global laundry_list_msg

        if laundry_send :
            self.socket_start_pub.publish(laundry_list_msg)
            laundry_send =False

    # 위의 subscription 등록 이후 각 기능을 아래에 추가하면 됩니다.
    # namespace는
    # auth - 터틀봇 번호 인증
    # env - 날씨, 시간, 온도 정보 보냄
    #   - turtlebot_time
    #   - turtlebot_temp
    #   - turtlebot_weather
    # control - 제어 관련 정보
    #   - result : 수거 완료 정보
    #   - laundry_start : 수거 목록 수신 및 시작 요청

    # 이외에는 back에서 추가 필요

    async def socket_day_pub(self, msg):
        global sio
        global connected
        global serialNo
        global sendDay
        if sio and connected and sendDay:
            
            data = str(msg.data)
            date_parts = data.split("/")
            
            if len(date_parts) == 4:
                month = date_parts[0]
                day = date_parts[1]
                hour = date_parts[2]
                minute = date_parts[3]

                obj = {"month":month, "day":day, "hour": hour, "minute":minute}
                await sio.emit('turtlebot_time', obj, namespace = '/env')
                sendDay = False
            else:
                print("status send error!!!")

    async def socket_temp_pub(self, msg):
        global sio
        global connected
        global serialNo
        global sendTemp
        if sio and connected and sendTemp:
            await sio.emit('turtlebot_temp', msg.data, namespace = '/env')
            sendTemp = False
    
    async def socket_weather_pub(self, msg):
        global sio
        global connected
        global serialNo
        global sendWeather
        if sio and connected and sendWeather:
            await sio.emit('turtlebot_weather', msg.data, namespace = '/env')
            sendWeather = False

# 만약 터틀봇 돌고난 뒤 결과가 들어 왔을 경우 서버로 보내기
    async def socket_result_pub(self, msg):
        pass
        # if sio and connected and operateNo:
        #     print(list(msg.result_list))
        #     # print(operateNo)
        #     print(type(operateNo))
        #     obj = {"serialNo":serialNo, "operateNo" : operateNo, "result" : list(msg.result_list)}
        #     await sio.emit('result', obj, namespace = '/control')
        #     operateNo = None

    
async def client():
    global sio
    global connected
    global serialNo

    # 테스트 값
    print("start")
    
    # 서버 작동 확인 후 다시 테스트
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # 이거 경로 확인
    ssl_context.load_cert_chain('C:/Users/SSAFY/Desktop/cert.pem',
                                'C:/Users/SSAFY/Desktop/privkey.pem')
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    http_session = aiohttp.ClientSession(connector=connector)
    sio = socketio.AsyncClient(http_session=http_session)

    # 연결
    @sio.event
    async def connect():
        global connected
        global serialNo
        print('connection established')
        # 연결할때 인증 시작
        connected = True


    @sio.event
    async def disconnect():
        print('disconnected from server')

    # 인증 안되면 보내기 종료
    @sio.on('auth_fail')
    async def auth_fail(data):
        global connected
        print(data)
        connected = False

    @sio.on('weather')
    async def weather(data):
        global sendWeather
        sendWeather = True
        sendDay = True
        sendTemp = True
        

    # 데이터 수신
    @sio.on('laundry_start')
    async def laundry_start(data):
        # data는 리스트로 들어오게 된다.
        global operateNo
        global laundry_list_msg
        global laundry_send
        
        # 출력
        print('laundry', data['laundry'])
        print('operate_id', data['op_id'])
        
        laundry_list_msg.laundrylist = data['laundry']
        operateNo = data['op_id']
        laundry_send = True



    # 서버 연결 -> 백 올린뒤 확인 필요
    # back의 경우 경로에 /api 추가해야 함. socket의 경우 자동으로 마지막에 /socket.io가 추가됨.
    # 따라서 직접적으로 지정 필요
    # 아닐 경우 /socket.io 경로로 접근하여 front의 값 받아옴.
    
    # 서버
    auth_url = 'https://j9b201.p.ssafy.io/api'
    await sio.connect(auth_url, socketio_path="/api/socket.io", namespaces =['/', '/auth_turtle', '/env', '/control'], wait_timeout = 3)
    
    # 로컬
    # auth_url = 'http://127.0.0.1:8000/socket.io'
    # await sio.connect(auth_url, namespaces =['/', '/auth_turtle', '/env', '/control'], wait_timeout = 3)
    
    print("connect")
    while not connected:
        await asyncio.sleep(0.1)

    print("connect ros")
    # 터틀봇 인증
    await sio.emit('authenticate', serialNo, namespace = '/auth_turtle')       

    await sio.wait()


def main(args = None):

    rclpy.init(args=None)

    socket_node = socketSub()
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(socket_node)

    client_thread =threading.Thread(target=asyncio.run, args=(client(),))  
    client_thread.start()
    executor.spin()

    socket_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":

    main()