# 예시 메시지 유형 정의
# 여러 개의 좌표 포인트를 포함하는 메시지
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry

class PointList(Node):
    def __init__(self):
        super().__init__('point_pub')
        self.odom_sub = self.create_subscription(Odometry,'odom',self.odom_callback,50)
        
        
        self.odom_msg=Odometry()
        self.points = []  # Point 메시지의 리스트
    def odom_callback(self,msg):
        self.is_odom=True
        self.odom_msg=msg

# 위 메시지를 메시지 유형으로 등록하고, 메시지 파일을 생성합니다.

def main(args=None):
    rclpy.init(args=args)
    point_pub = PointList()
    ## spin 함수는 노드가 죽지않게 계속 대기상태를 만들어 놓는 함수입니다. spin을 삭제하면 minimal_publisher가 생성되고 바로 main 함수가 끝나게 됩니다.
    rclpy.spin(point_pub)
    point_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()