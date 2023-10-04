import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from ssafy_msgs.msg import Detection, LaundryPose, LaundryList, Finish
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
        # self.detect_sub = self.create_subscription(LaundryPose, 'laundry_pose', self.detect_callback, 1)
        self.socket_sub = self.create_subscription(LaundryList, 'socket_start', self.socket_callback, 1)
        self.finish_pub = self.create_publisher(Finish,'is_finish',10)
        self.odom_msg=Odometry()
        self.a_star_instance = a_star()

        self.goal_pose_msg = PoseStamped()
        self.is_finish_msg = Finish()

        self.goal_pose_msg.header.frame_id = 'map'
        self.pose_dest_point = []
        # 여러 경로들을 설정 나중에 세탁물을 발견했을 때 경로를 추가하여 이동
        # 거실과 부엌을 탐색하는 경로 설정
        self.grid_cell_point = []

        ''' 
        거실
        self.grid_cell_point.append([217, 72])
        self.grid_cell_point.append([267, 72])
        self.grid_cell_point.append([289, 111])
        self.grid_cell_point.append([292, 138])
        self.grid_cell_point.append([233, 155])
        self.grid_cell_point.append([218, 100])
        '''
        '''
        방1
        '''
        self.room_list = [[189, 129],
                          [190, 55],
                          [163, 55],
                          [160, 102],
                          [138, 47],
                          [115, 47],
                          [87, 79],
                          [93, 123],
                          [114, 123],
                          [218, 100]]
        for _ in self.room_list:
            self.grid_cell_point.append(_)
        
        self.goal_pose_msg.pose.position.x,self.goal_pose_msg.pose.position.y = self.a_star_instance.grid_cell_to_pose(self.grid_cell_point[0])
        self.goal_pub.publish(self.goal_pose_msg)
        self.grid_cell_point.pop(0)

        self.is_odom = False
        self.point_cnt = 0

        # self.turtle_x = 0.0
        # self.turtle_y = 0.0

        # 선택된 세탁물 저장
        self.laundry_list = ['shirts', 'pants']
        # self.laundry_list = ['shirts']

        self.laundry_pose_cnt = 0
    def socket_callback(self, msg):
        self.laundry_list = []
        # temp_list = msg
        print(f'소켓 : {msg.laundrylist}')
        for _ in msg.laundrylist:
            if _ == 1:
                self.laundry_list.append('shirts')
            elif _ == 2:
                self.laundry_list.append('pants')
        print(f'세탁물 리스트 : {self.laundry_list}')

        # self.laundry_list = msg


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
        print(f'현재 목적지 : {goal_x} , {goal_y}')
        self.is_finish_msg.is_finish = False
        self.finish_pub.publish(self.is_finish_msg)
    
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
        # print(f'왜 리스트가 비었다고 그럼? {self.pose_dest_point}')
        self.pose_dest_point.pop(0) # pose
        # print(f'POP하고 나서? {self.pose_dest_point}')

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
        # if self.laundry_pose_cnt == 1:
        #     if(len(msg.x) != 0):
        #         for i in range(len(msg.name)):
        #             if msg.name[i] in self.laundry_list:
        #                 # print(f'msg : {msg}')
        #                 print(f'msg : {msg.x[i]} y: {msg.y[i]}')
        #                 # self.grid_cell_point.insert(0, [msg.x[0], msg.y[0]])
        #                 self.goal_pose_msg.pose.position.x,self.goal_pose_msg.pose.position.y = [msg.x[i], msg.y[i]]
        #                 self.goal_pub.publish(self.goal_pose_msg) # grid
        #                 # self.grid_cell_point.pop(0)
        #     self.laundry_pose_cnt = 0
        # else:
        #     self.laundry_pose_cnt = 1
        if(len(msg.x) != 0):
            for i in range(len(msg.name)):
                if msg.name[i] in self.laundry_list:
                    # print(f'msg : {msg}')
                    print(f'msg : {msg.x[i]} y: {msg.y[i]}')
                    # self.grid_cell_point.insert(0, [msg.x[0], msg.y[0]])
                    self.goal_pose_msg.pose.position.x,self.goal_pose_msg.pose.position.y = [msg.x[i], msg.y[i]]
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
        # print('현재 위치 : {}'.format(msg))
        # self.grid_cell_point.pop(0)
        # if len(self.a_star_instance.grid_cell_point) > 0:
            # self.a_star_instance.grid_cell_point.pop(0)
        # self.a_star_instance.point_list_pop()
        if msg.pose.position.x != 100.0 and msg.pose.position.x != 200.0:
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
                else:
                    self.is_finish_msg.is_finish = True
                    self.finish_pub.publish(self.is_finish_msg)
                    self.laundry_list = ['shirts']




def main(args=None):
    rclpy.init(args=args)
    point_pub = PointList()
    rclpy.spin(point_pub)
    point_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()