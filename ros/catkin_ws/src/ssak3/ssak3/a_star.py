import rclpy
import numpy as np
from rclpy.node import Node
import os
from geometry_msgs.msg import Pose,PoseStamped
from squaternion import Quaternion
from nav_msgs.msg import Odometry,OccupancyGrid,MapMetaData,Path
from math import pi,cos,sin
from collections import deque
from queue import PriorityQueue


# a_star 노드는  OccupancyGrid map을 받아 grid map 기반 최단경로 탐색 알고리즘을 통해 로봇이 목적지까지 가는 경로를 생성하는 노드입니다.
# 로봇의 위치(/pose), 맵(/map), 목표 위치(/goal_pose)를 받아서 전역경로(/global_path)를 만들어 줍니다. 
# goal_pose는 rviz2에서 2D Goal Pose 버튼을 누르고 위치를 찍으면 메시지가 publish 됩니다. 
# 주의할 점 : odom을 받아서 사용하는데 기존 odom 노드는 시작했을 때 로봇의 초기 위치가 x,y,heading(0,0,0) 입니다. 로봇의 초기위치를 맵 상에서 로봇의 위치와 맞춰줘야 합니다. 
# 따라서 sub2의 odom 노드를 수정해줍니다. turtlebot_status 안에는 정답데이터(절대 위치)가 있는데 그 정보를 사용해서 맵과 로봇의 좌표를 맞춰 줍니다.

# 노드 로직 순서
# 1. publisher, subscriber 만들기
# 2. 파라미터 설정
# 3. 맵 데이터 행렬로 바꾸기
# 4. 위치(x,y)를 map의 grid cell로 변환
# 5. map의 grid cell을 위치(x,y)로 변환
# 6. goal_pose 메시지 수신하여 목표 위치 설정
# 7. grid 기반 최단경로 탐색

class a_star(Node):

    def __init__(self):
        super().__init__('a_Star')
        # 로직 1. publisher, subscriber 만들기
        self.map_sub = self.create_subscription(OccupancyGrid,'map',self.map_callback,1)
        self.odom_sub = self.create_subscription(Odometry,'odom',self.odom_callback,1)
        self.goal_sub = self.create_subscription(PoseStamped,'goal_pose',self.goal_callback,1)
        self.a_star_pub= self.create_publisher(Path, 'global_path', 1)
        
        # 맵
        self.map_msg=OccupancyGrid()
        self.odom_msg=Odometry()
        self.is_map=False
        self.is_odom=False
        self.is_found_path=False
        self.is_grid_update=False


        # 로직 2. 파라미터 설정
        self.goal = [184,224] 
        self.map_size_x=350
        self.map_size_y=350
        self.map_resolution= 0.05
        self.map_offset_x=-8.75-8 # -7-8.75
        self.map_offset_y=-8.75-4 # 10 - 8.75
    
        self.GRIDSIZE=350 


        self.dx = [-1,0,0,1,-1,-1,1,1]
        self.dy = [0,1,-1,0,-1,1,-1,1]
        self.dCost = [1,1,1,1,1.414,1.414,1.414,1.414]


    def grid_update(self):
        self.is_grid_update=True
        '''
        로직 3. 맵 데이터 행렬로 바꾸기
        '''
        map_to_grid=np.array(self.map_msg.data)
        # order : C- row 우선, F: column 우선 
        self.grid=np.reshape(map_to_grid, (350,350), order='F')


    def pose_to_grid_cell(self,x,y):
        map_point_x = 0
        map_point_y = 0
        '''
        로직 4. 위치(x,y)를 map의 grid cell로 변환 
        (테스트) pose가 (-8,-4)라면 맵의 중앙에 위치하게 된다. 따라서 map_point_x,y 는 map size의 절반인 (175,175)가 된다.
        pose가 (-16.75,12.75) 라면 맵의 시작점에 위치하게 된다. 따라서 map_point_x,y는 (0,0)이 된다.
        '''
        map_point_x= int(( x - self.map_offset_x ) / self.map_resolution)
        map_point_y= int(( y - self.map_offset_y ) / self.map_resolution)
        
        return map_point_x,map_point_y


    def grid_cell_to_pose(self,grid_cell):

        x = 0
        y = 0
        '''
        로직 5. map의 grid cell을 위치(x,y)로 변환
        (테스트) grid cell이 (175,175)라면 맵의 중앙에 위치하게 된다. 따라서 pose로 변환하게 되면 맵의 중앙인 (-8,-4)가 된다.
        grid cell이 (350,350)라면 맵의 제일 끝 좌측 상단에 위치하게 된다. 따라서 pose로 변환하게 되면 맵의 좌측 상단인 (0.75,6.25)가 된다.
        '''

        x=(grid_cell[0] * self.map_resolution) + self.map_offset_x
        y=(grid_cell[1] * self.map_resolution) + self.map_offset_y

        
        return [x,y]


    def odom_callback(self,msg):
        self.is_odom=True
        self.odom_msg=msg


    def map_callback(self,msg):
        self.is_map=True
        self.map_msg=msg
        

    def goal_callback(self,msg):
        
        if msg.header.frame_id=='map':
            '''
            로직 6. goal_pose 메시지 수신하여 목표 위치 설정
            '''             
            goal_x=msg.pose.position.x
            goal_y=msg.pose.position.y
            goal_cell= self.pose_to_grid_cell(goal_x, goal_y)
            # self.goal 출력해보면 (328,223) 이렇게 나온다.
            self.goal = list(goal_cell)
            print("goal좌표 : {}".format(self.goal))
            # goal_w = msg.pose.orientation.w
            if goal_y==100.0 and goal_x==100.0:
                self.final_path.reverse()
                print("돌아가기!")
                self.global_path_msg = Path()
                self.global_path_msg.header.frame_id = 'map'
                if self.final_path != None:
                    for grid_cell in self.final_path:
                        tmp_pose = PoseStamped()
                        waypoint_x, waypoint_y = self.grid_cell_to_pose(
                            grid_cell)
                        tmp_pose.pose.position.x = waypoint_x
                        tmp_pose.pose.position.y = waypoint_y
                        tmp_pose.pose.orientation.w = 1.0
                        self.global_path_msg.poses.append(tmp_pose)

                    print("메세지 생성 종료")
                    if len(self.final_path) != 0:
                        self.a_star_pub.publish(self.global_path_msg)
                        print("메세지 전송 완료")
                        return
            goal_cell=self.pose_to_grid_cell(goal_x, goal_y)

            if goal_cell[0] <= 350 and goal_cell[1] <= 350:
                self.goal = [goal_cell[0], goal_cell[1]]
            else:
                print('좌표가 map 을 벗어났습니다.')
            
            print(msg)
            

            if self.is_map ==True and self.is_odom==True  :
                if self.is_grid_update==False :
                    self.grid_update()

                self.final_path=[]

                x=self.odom_msg.pose.pose.position.x
                y=self.odom_msg.pose.pose.position.y
                start_grid_cell=self.pose_to_grid_cell(x,y)
                start_grid_cell = list(start_grid_cell)
                # 이전 어디서 왔는가
                self.path = [[0 for col in range(self.GRIDSIZE)] for row in range(self.GRIDSIZE)]
                # 출발 -> 해당 지점까지의 비용은 얼마인가
                self.cost = np.array([[self.GRIDSIZE*self.GRIDSIZE for col in range(self.GRIDSIZE)] for row in range(self.GRIDSIZE)])

                
                # 다익스트라 알고리즘을 완성하고 주석을 해제 시켜주세요. 
                # 시작지, 목적지가 탐색가능한 영역이고, 시작지와 목적지가 같지 않으면 경로탐색을 합니다.

                print("start : ")
                print(start_grid_cell[0])
                print(start_grid_cell[1])
                if self.grid[start_grid_cell[0]][start_grid_cell[1]] ==0  and self.grid[self.goal[0]][self.goal[1]] ==0  and start_grid_cell != self.goal :
                    print("search")
                    self.dijkstra(start_grid_cell)
                
                

                self.global_path_msg=Path()
                self.global_path_msg.header.frame_id='map'
                for grid_cell in reversed(self.final_path) :
                    tmp_pose=PoseStamped()
                    waypoint_x,waypoint_y=self.grid_cell_to_pose(grid_cell)
                    tmp_pose.pose.position.x=waypoint_x
                    tmp_pose.pose.position.y=waypoint_y
                    tmp_pose.pose.orientation.w=1.0
                    self.global_path_msg.poses.append(tmp_pose)
            
                if len(self.final_path)!=0 :
                    print("send map")
                    self.a_star_pub.publish(self.global_path_msg)
                else:
                    print("error map")

    # Manhattan distance vs Euclidean distance 뭐가 나은가..
    def heuristic(self, start, goal):
        x1, y1 = start
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)


    def dijkstra(self,start):


        Q = PriorityQueue()
        # Q.put((우선 순위, 좌표))
        # 우선 순위에 비용을 넣겠다. 그러면 비용이 작은 좌표부터 나올 것이다.
        Q.put((1, start))
        self.cost[start[0]][start[1]] = 1
        found = False


        while not Q.empty():
            
            if found:
                break

            # Q.get() 하면 (우선순위, [ , ]) 이렇게 나온다.
            current = Q.get()[1]
            # print("current:", current)
            if current == self.goal:
                found = True

            for i in range(8):

                # 다음
                next = [current[0]+self.dx[i], current[1]+self.dy[i]]

                if next[0] >= 0 and next[1] >= 0 and next[0] < self.GRIDSIZE and next[1] < self.GRIDSIZE:
                    # 맵의 데이터를 이용한다.
                    # 다음 확인할 칸이 벽이 아니라면
                    if self.grid[next[0]][next[1]] < 50:

                        # 여기에서의 현재는 다음 이동할 노드
                        # 현재 상태의 비용 (출발지 -> 현재)
                        g = self.cost[current[0]][current[1]] + self.dCost[i]
                        # 현재 상태에서 다음 상태로 이동할 때 휴리스틱 함수(현재 -> 목적지)
                        h = self.heuristic(next, self.goal)
                        f = g + h

                        # 만약, 다음에 저장된 값이 지금보다 작다면
                        if g < self.cost[next[0]][next[1]]:
                            # 넥스트를 넣어준다.
                            # Q.put((f, next))
                            Q.put((f, next))
                            self.path[next[0]][next[1]] = current
                            self.cost[next[0]][next[1]] = g

        node = self.goal
        self.final_path.append(node)


        while node != start:
            nextNode = self.path[node[0]][node[1]]
            self.final_path.append(nextNode)
            node = nextNode




        
def main(args=None):
    rclpy.init(args=args)

    global_planner = a_star()

    rclpy.spin(global_planner)


    global_planner.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
