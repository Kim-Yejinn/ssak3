import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from ssafy_msgs.msg import Detection
# 자꾸 모듈을 못가져와서 path설정 해줌
import sys
sys.path.append('C:/Users/SSAFY/Desktop/project/S09P22B201/ros/catkin_ws/src/ssak3')

from ssak3.a_star import a_star


class PointList(Node):
    def __init__(self):
        super().__init__('point_pub')
        self.odom_sub = self.create_subscription(Odometry,'odom',self.odom_callback,50)
        self.goal_pub = self.create_publisher(PoseStamped,'goal_pose',10)
        self.goal_sub = self.create_subscription(PoseStamped,'goal_pose',self.goal_callback,1)
        self.cur_sub = self.create_subscription(PoseStamped,'cur_pose',self.cur_callback,1)
        self.detect_sub = self.create_subscription(Detection, 'laundry_detect', self.detect_callback, 1)
        self.odom_msg=Odometry()

        self.goal_pose_msg = PoseStamped()

        self.goal_pose_msg.header.frame_id = 'map'
        self.pose_dest_point = []
        # 여러 경로들을 설정 나중에 세탁물을 발견했을 때 경로를 추가하여 이동
        # 거실과 부엌을 탐색하는 경로 설정
        self.grid_cell_point = []
        # self.grid_cell_point.append([149.0, 151.0])
        # self.grid_cell_point.append([134.0, 232.0])
        # self.grid_cell_point.append([193.0, 228.0])
        # self.grid_cell_point.append([198.0, 127.0])
        # self.grid_cell_point.append([213.0, 74.0])
        # self.grid_cell_point.append([149.0, 50.0])
        # self.grid_cell_point.append([166.0, 159.0])
        # self.grid_cell_point.append([149.0, 98.0])

        self.is_odom = False
        self.point_cnt = 0

        self.a_star_instance = a_star()

    '''
    grid는 [350, 350]좌표, pose는 [rviz2상에 실제 좌표]
    '''
    '''
    목적지가 찍히면 해당 좌표(pose)를 저장한다.
    '''
    def goal_callback(self, msg):
        goal_x=msg.pose.position.x
        goal_y=msg.pose.position.y
        self.pose_dest_point.insert(0, [goal_x, goal_y]) # pose
    
    # def point_list_is_not_empty(self):
    #     print(f'list empty : {self.grid_dest_point}')
    #     if len(self.grid_dest_point) == 0:
    #         return False
    #     else:
    #         return True
    
    '''
    pose리스트 하나를 지운다 (도착시 실행)
    '''
    def pose_list_pop(self):
        print(f'왜 리스트가 비었다고 그럼? {self.pose_dest_point}')
        self.pose_dest_point.pop(0) # pose
        print(f'POP하고 나서? {self.pose_dest_point}')

    '''
    pose의 첫번 째 원소를 얻는다. (원래 목적지 저장용)
    '''
    def get_point_list(self):
        print(f'list get : {self.grid_dest_point}')
        return self.pose_dest_point[0] # pose
    
    
    # def insert_point_list(self, point):
    #     self.pose_dest_point.insert(0, point) # pose
    #     print(f'self : {self} asd {self.pose_dest_point}')

    '''
    세탁물 발견 좌표를 퍼블리시 한다.
    '''
    def detect_callback(self, msg):
        if(len(msg.x) != 0):
            print(f'msg : {msg}')
            print(f'msg : {msg.x[0]} y: {msg.y[0]}')
            # self.grid_cell_point.insert(0, [msg.x[0], msg.y[0]])
            self.goal_pose_msg.pose.position.x,self.goal_pose_msg.pose.position.y = [msg.x[0], msg.y[0]]
            self.goal_pub.publish(self.goal_pose_msg) # grid
            # self.grid_cell_point.pop(0)

    def odom_callback(self,msg):
        self.is_odom=True
        self.odom_msg=msg
        # if self.is_odom == True and self.point_cnt == 0:
    
    '''
    목적지 도착 시 실행 함수
    도착하면 저장되어있던 pose삭제

    '''
    def cur_callback(self, msg):
        print('현재 위치 : {}'.format(msg))
        # self.grid_cell_point.pop(0)
        # if len(self.a_star_instance.grid_cell_point) > 0:
            # self.a_star_instance.grid_cell_point.pop(0)
        # self.a_star_instance.point_list_pop()
        self.pose_list_pop() # grid
        # print('동작 gird : {}'.format(self.goal_pose_msg))
        '''
        goal_pose 남아있던게 있으면 이거 먼저 실행
        '''
        if len(self.pose_dest_point) > 0:
            self.goal_pose_msg.pose.position.x,self.goal_pose_msg.pose.position.y = self.pose_dest_point[0]
            self.pose_list_pop()
            self.goal_pub.publish(self.goal_pose_msg)

        # 남아 있던게 없으면 다시 원래 루트 따라서 이동
        else:
            if len(self.grid_cell_point) > 0:
                self.goal_pose_msg.pose.position.x,self.goal_pose_msg.pose.position.y = self.a_star_instance.grid_cell_to_pose(self.grid_cell_point[0])
                self.goal_pub.publish(self.goal_pose_msg)
                self.grid_cell_point.pop(0)



def main(args=None):
    rclpy.init(args=args)
    point_pub = PointList()
    rclpy.spin(point_pub)
    point_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()