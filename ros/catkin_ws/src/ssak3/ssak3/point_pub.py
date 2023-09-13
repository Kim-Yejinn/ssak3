# 예시 메시지 유형 정의
# 여러 개의 좌표 포인트를 포함하는 메시지
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

class PointList(Node):
    def __init__(self):
        super().__init__('point_pub')
        self.odom_sub = self.create_subscription(Odometry,'odom',self.odom_callback,50)
        self.goal_pub = self.create_publisher(PoseStamped,'goal_pose',10)

        self.odom_msg=Odometry()

        self.map_size_x=350
        self.map_size_y=350
        self.map_resolution= 0.05
        self.map_offset_x=-8.75-8 
        self.map_offset_y=-8.75-4 

        self.goal_pose_msg = PoseStamped()

        self.goal_pose_msg.header.frame_id = 'map'
        self.grid_cell_point = [184.0, 224.4]

        self.is_odom = False
        self.point_cnt = 0

    def odom_callback(self,msg):
        self.is_odom=True
        self.odom_msg=msg
        if self.is_odom == True and self.point_cnt == 0:
            print('동작 gird : {}'.format(self.goal_pose_msg))
            self.goal_pose_msg.pose.position.x,self.goal_pose_msg.pose.position.y = self.grid_cell_to_pose(self.grid_cell_point)
            self.goal_pub.publish(self.goal_pose_msg)
            self.point_cnt = 2

    def grid_cell_to_pose(self,grid_cell):

        x = 0
        y = 0
        
        x=(grid_cell[0] * self.map_resolution) + self.map_offset_x
        y=(grid_cell[1] * self.map_resolution) + self.map_offset_y

        
        return [x,y]



def main(args=None):
    rclpy.init(args=args)
    point_pub = PointList()
    rclpy.spin(point_pub)
    point_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()