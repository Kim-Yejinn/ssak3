import torch
import numpy as np
import cv2
import os
import math
import rclpy
import time
import base64
import array

from ssak3.ex_calib import *
from rclpy.node import Node

import sys
sys.path.append('C:/Users/SSAFY/Desktop/project/S09P22B201/ros/catkin_ws/src/ssak3/ssak3')
from a_star import a_star

from sensor_msgs.msg import CompressedImage, LaserScan, Imu
from geometry_msgs.msg import Twist,PoseStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
from ssafy_msgs.msg import TurtlebotStatus, Detection

from squaternion import Quaternion


# 로봇의 위치 정보와 로봇에 달려있는 라이다와 카메라 간의 위치 및 자세 정보
params_bot = {
    "X": 0.0,
    "Y": 0.0,
    "Z":  0.0,
    "YAW": 0.0,
    "PITCH": 0.0,
    "ROLL": 0.0
}

params_lidar = {
    "Range" : 90,
    "CHANNEL" : int(1),
    "localIP": "127.0.0.1",
    "localPort": 9094,
    "Block_SIZE": int(1206),
    "X": 0, # meter
    "Y": 0,
    "Z": 0.02,
    "YAW": 0, # deg
    "PITCH": 0,
    "ROLL": 0
}

params_cam = {
    "WIDTH": 320,
    "HEIGHT": 240,
    "FOV": 90,
    "localIP": "127.0.0.1",
    "localPort": 1232,
    "Block_SIZE": int(65535),
    "UnitBlock_HEIGHT": int(30),
    "X": 0.,
    "Y": 0,
    "Z":  0.8,
    "YAW": 0,
    "PITCH": 40,
    "ROLL": 0
}

def visualize_images(image_out):
    winname = 'laundry detect'
    cv2.imshow(winname, image_out)

# ROS에서 받아온 이미지 데이터를 OpenCV 형식으로 변환하고, 전역 변수에 저장
def img_callback(msg):
    global img_bgr
    global is_img_bgr
    is_img_bgr = True
    np_arr = np.frombuffer(msg.data, np.uint8)
    img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

# ROS에서 받아온 라이다 스캔 데이터를 3D좌표로 변환하고, 전역 변수에 저장
def scan_callback(msg):
    global xyz
    global is_scan
    is_scan = True
    R = np.array(msg.ranges)
    x = R*np.cos(np.linspace(0, 2*np.pi, 360))
    y = R*np.sin(np.linspace(0, 2*np.pi, 360))
    z = np.zeros_like(x)
    xyz = np.concatenate([
        x.reshape([-1, 1]),
        y.reshape([-1, 1]),
        z.reshape([-1, 1])
    ], axis=1)


# ROS에서 받아온 IMU 데이터를 처리하여 로봇의 방향을 나타내는 Yaw 각도를 추출하고, 전역 변수에 저장
def imu_callback(msg):
    global is_imu
    global robot_yaw

    is_imu =True
    imu_q= Quaternion(msg.orientation.w,msg.orientation.x,msg.orientation.y,msg.orientation.z)
    robot_roll, robot_pitch, robot_yaw = imu_q.to_euler()

# ROS에서 받아온 터틀봇의 상태 메시지를 처리하여 터틀봇의 위치 정보를 추출하고, 전역 변수에 저장 
def status_callback(msg):
    global turtlebot_status_msg
    global loc_x,loc_y,loc_z
    global is_status

    is_status = True
    loc_x = msg.twist.angular.x
    loc_y = msg.twist.angular.y
    loc_z = 0.0
    turtlebot_status_msg = msg

# 라이다 데이터를 로봇의 좌표계로 변환하는 행렬계산
def transformMTX_lidar2bot(params_lidar, params_bot):

    lidar_yaw, lidar_pitch, lidar_roll = np.deg2rad(params_lidar["YAW"]), np.deg2rad(params_lidar["PITCH"]), np.deg2rad(params_lidar["ROLL"])
    bot_yaw, bot_pitch, bot_roll = np.deg2rad(params_bot["YAW"]), np.deg2rad(params_bot["PITCH"]), np.deg2rad(params_bot["ROLL"])
    lidar_pos = [params_lidar["X"], params_lidar["Y"], params_lidar["Z"]]
    bot_pos = [params_bot["X"], params_bot["Y"], params_bot["Z"]]
    Tmtx = translationMtx(lidar_pos[0] - bot_pos[0], lidar_pos[1] - bot_pos[1], lidar_pos[2] - bot_pos[2])
    Rmtx = rotationMtx(0, 0, 0)
    RT = np.matmul(Rmtx, Tmtx)

    return RT

# 로봇의 좌표계를 global(map)에서의 좌표계로 변환하는 행렬계산
def transformMTX_bot2map():
    global robot_yaw
    global loc_x
    global loc_y
    global loc_z

    bot_yaw, bot_pitch, bot_roll = np.deg2rad(robot_yaw), np.deg2rad(0.0), np.deg2rad(0.0)
    map_yaw, map_pitch, map_roll = np.deg2rad(0.0), np.deg2rad(0.0), np.deg2rad(0.0)
    bot_pos = [loc_x, loc_y, loc_z]
    map_pos = [0.0, 0.0, 0.0]
    Tmtx = translationMtx(bot_pos[0] - map_pos[0], bot_pos[1] - map_pos[1], bot_pos[2] - map_pos[2])
    Rmtx = rotationMtx(bot_yaw, bot_pitch, bot_roll)
    RT = np.matmul(Rmtx, Tmtx)

    return RT

# 라이다 좌표계를 로봇 좌표계로 변환하는 함수
def transform_lidar2bot(xyz_p):
    global RT_Lidar2Bot
    xyz_p = np.matmul(xyz_p, RT_Lidar2Bot.T)
    return xyz_p

# 로봇 좌표계를 map(global)에서의 좌표계로 변환하는 함수
def transform_bot2map(xyz_p):
    global RT_Bot2Map
    xyz_p = np.matmul(xyz_p, RT_Bot2Map.T)
    return xyz_p

def cur_callback(msg):
    print(f"msg : {msg}")
    global is_send
    is_send = False

def main(args=None):

    os_file_path = os.path.abspath(__file__)
    full_path = os_file_path.replace('install\\ssak3\\Lib\\site-packages\\ssak3\\laundry_detect.py', 
                                        'src\\ssak3\\yolov5')
    local_yolov5_path = os_file_path.replace('install\\ssak3\\Lib\\site-packages\\ssak3\\laundry_detect.py', 
                                        'src\\ssak3\\model\\best_final.pt')
    model = torch.hub.load(full_path, 'custom', path = local_yolov5_path, source = 'local', force_reload = True)
    
    global g_node
    global is_img_bgr
    global is_scan
    global is_imu
    global is_status
    global is_send

    is_img_bgr = False
    is_scan = False
    is_imu = False
    is_status = False
    is_send = False

    global loc_x
    global loc_y
    global loc_z

    rclpy.init(args=args)
    g_node = rclpy.create_node('laundry_detector')

    subscription_turtle = g_node.create_subscription(TurtlebotStatus, '/turtlebot_status',status_callback, 10)
    subscription_img = g_node.create_subscription(CompressedImage, '/image_jpeg/compressed', img_callback, 10)
    subscription_scan = g_node.create_subscription(LaserScan, '/scan', scan_callback, 10)
    subscription_imu = g_node.create_subscription(Imu, '/imu', imu_callback, 10)
    publisher_detect = g_node.create_publisher(Detection, "/laundry_detect", 10)
    goal_sub = g_node.create_subscription(PoseStamped,'cur_pose',cur_callback,1)
    
    publisher_goal_pub = g_node.create_publisher(PoseStamped,'goal_pose',10)
    # a_star_instance = a_star()
    goal_pose_msg = PoseStamped()
    turtlebot_status_msg = TurtlebotStatus()
    
    l2c_trans = LIDAR2CAMTransform(params_cam, params_lidar)

    global RT_Lidar2Bot
    global RT_Bot2Map

    time.sleep(1)
    while rclpy.ok():
        
        time.sleep(0.05)
        
        for _ in range(5):
            rclpy.spin_once(g_node)
        
        detections = Detection()
        temp_detection = []

        if is_img_bgr and is_scan and is_status and is_imu:

            # print("hello")
            # print(is_scan)

            results = model(img_bgr)
            loc_z = 0.0
            xyz_p = xyz[np.where(xyz[:, 0] >= 0)] #
            xyz_c = l2c_trans.transform_lidar2cam(xyz_p) #라이다 포인트의 좌표를 카메라 이미지 좌표로 변환한 후 반환 
            xy_i = l2c_trans.project_pts2img(xyz_c, False)# 그 반환한 값을 2D 이미지 좌표로 프로젝션한다. 
            xyii = np.concatenate([xy_i, xyz_p], axis = 1)


            RT_Lidar2Bot = transformMTX_lidar2bot(params_lidar, params_bot)
            RT_Bot2Map = transformMTX_bot2map()

            info = results.pandas().xyxy[0]
            info_result = info[info['confidence'] > 0.65].to_numpy()
            boxes_detect = info[info['confidence'] > 0.65][['xmin', 'ymin', 'xmax', 'ymax']].to_numpy()
            image_process = np.squeeze(results.render())
            if len(info_result) == 0:
                pass
                detections.x = []
                detections.y = []
                detections.name = []
                detections.distance = []
                detections.cx = []
                detections.cy = []
            else:
                print(info_result)
                all_boxes = []
                for box in boxes_detect:
                    box_np = np.array(box)
                    x = box_np.T[0]
                    y = box_np.T[1]
                    w = (box_np.T[2] - box_np.T[0])
                    h = (box_np.T[3] - box_np.T[1])
                    bbox = np.vstack([
                        x.astype(np.int32).tolist(),
                        y.astype(np.int32).tolist(),
                        w.astype(np.int32).tolist(),
                        h.astype(np.int32).tolist()
                    ]).T
                    all_boxes.append(bbox)

                all_boxes = np.array(all_boxes)

                ostate_list = []
                angles = []

                for k, bbox in enumerate(all_boxes):
                    for i in range(bbox.shape[0]):
                        x = int(bbox[i, 0])
                        y = int(bbox[i, 1])
                        w = int(bbox[i, 2])
                        h = int(bbox[i, 3])

                        cx = int(x + (w / 2))
                        cy = int(y + (h / 2))

                        xyv = xyii[np.logical_and(xyii[:, 0] >= x + (w / 3), xyii[:, 0] <= x + w - (w / 3)), :]
                        xyv = xyv[np.logical_and(xyv[:, 1] >= y, xyv[:, 1] <= y + h), :]
                        if len(xyv) == 0:
                            continue
                        # else:
                        #     print("xyv")
                        #     print(xyv)

                        ostate = np.median(xyv, axis=0)
                        
                        relative_x = ostate[2]
                        relative_y = ostate[3]
                        relative_z = ostate[4]

                        relative = np.array([relative_x, relative_y, relative_z, 1])

                        object_global_pose = transform_bot2map(transform_lidar2bot(relative))

                        x2 = loc_x + relative_x * math.cos(robot_yaw)
                        y2 = loc_y + relative_x * math.sin(robot_yaw)
                        angles.append(robot_yaw * 180.0 / math.pi)

                        ostate_list.append(object_global_pose)

                        detections.x.append(x2)
                        detections.y.append(y2)
                        # detections.x.append(object_global_pose[0])
                        # detections.y.append(object_global_pose[1])
                        detections.distance.append(relative_x)
                        detections.cx.append(cx)
                        detections.cy.append(cy)
                        detections.name.append(info.name[k])
                        temp_detection.append([detections.x, detections.y])
                print(detections.x)
                print(detections.y)
                print(f"temp_detection : {temp_detection}")
                if len(temp_detection) != 0:
                    print(f'보내기 가능? : {is_send}')
                    if is_send == False:
                        publisher_detect.publish(detections)
                        is_send = True

                # if not math.isnan(detections.x[0]):
                #     goal_pose_msg.pose.position.x = detections.x[0]
                #     goal_pose_msg.pose.position.y = detections.y[0]
                #     publisher_goal_pub.publish(goal_pose_msg)

            image_process = draw_pts_img(image_process, xy_i[:, 0].astype(np.int32), xy_i[:, 1].astype(np.int32))
            visualize_images(image_process)
            
        cv2.waitKey(1)

    g_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()








