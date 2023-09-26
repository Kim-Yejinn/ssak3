
import rclpy
from rclpy.node import Node

from nav_msgs.msg import Path
from ssafy_msgs.msg import EnviromentStatus
from std_msgs.msg import String

import os



class turtlebotStatus(Node):

    def __init__(self):
        super().__init__('turtlebot_status')

        self.envir_sub = self.create_subscription(
            EnviromentStatus, '/envir_status', self.envir_status_callback, 10)
        
        self.socket_day = self.create_publisher(String, '/socket_day', 20)
        self.socket_temp = self.create_publisher(String, '/socket_temp', 10)
        self.socket_weather = self.create_publisher(String, '/socket_weather', 10)


        self.is_weather = False
        self.envir_msg = EnviromentStatus()

        time_period = 0.1
        self.timer = self.create_timer(time_period, self.timer_callback)

    def envir_status_callback(self, msg): 
        self.is_weather = True
        self.envir_msg = msg


    def timer_callback(self):
        if self.is_weather == True:
            # 시뮬레이터에서 날씨를 받아서 세팅

            # 정보 받아오기
            month = self.envir_msg.month
            day = self.envir_msg.day
            hour = self.envir_msg.hour
            minute = self.envir_msg.minute
            temp = self.envir_msg.temperature
            weather = self.envir_msg.weather

            today = str(month) +"/" + str(day) + "/" + str(hour) + "/" + str(minute)
            # print("==== 시뮬레이터 정보 ====")
            # print(today)
            # print(temp)
            # print(weather)
            # print("========================")

            # 소켓으로 보내기
            self.socket_day.publish(String(data = str(today)))
            self.socket_temp.publish(String(data = str(temp)))
            self.socket_weather.publish(String(data = str(weather)))

def main(args=None):
    rclpy.init(args=args)
    turtlebot_status = turtlebotStatus()
    rclpy.spin(turtlebot_status)
    weather.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()