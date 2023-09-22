import rclpy
from rclpy.node import Node

from ssafy_msgs.msg import TurtlebotStatus, HandControl
# from std_msgs.msg import Int16


class up_object(Node):
    def __init__(self):
        super().__init__('up_object')

        self.status_sub = self.create_subscription(TurtlebotStatus,'/turtlebot_status',self.status_callback,10)
        self.control_pub = self.create_publisher(HandControl, 'hand_control', 10)
        
        time_period=0.05 
        self.timer = self.create_timer(time_period, self.timer_callback)
        
        
        #이동
        # self.hand_conrtrol_msg = Int16()

        self.is_status = False
        self.control_msg = HandControl()
        self.status_msg = TurtlebotStatus()



    def timer_callback(self):
        if self.is_status == True:
            if self.status_msg.can_lift == True:
                self.control_msg.control_mode = 2
                self.control_pub.publish(self.control_msg)
        #     else:
        #         print("들수있는 상태가 아닌데?")
        # else:
        #     print("터틀봇 상태못받아옴")

        self.control_msg.control_mode = 1
        self.control_msg.put_distance = 0.0
        self.control_msg.put_height = 100.0
        if self.status_msg.can_put == False:
            # print(f"can put : {self.status_msg}")
            self.control_pub.publish(self.control_msg)

        self.control_msg.control_mode = 3
        self.control_pub.publish(self.control_msg)



    def status_callback(self, msg):
        self.is_status = True
        self.status_msg = msg


def main(args=None):
    rclpy.init(args=args)

    up = up_object()

    rclpy.spin(up)


    up.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
