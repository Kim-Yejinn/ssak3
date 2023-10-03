from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ssak3',
            node_executable='odom',
            node_name='odom'
        ),
        Node(
            package='ssak3',
            node_executable='load_map',
            node_name='loadMap'
        ),
        Node(
            package='ssak3',
            node_executable='a_star',
            node_name='a_star'
        ),
        Node(
            package='ssak3',
            node_executable='a_star_local_path',
            node_name='astarLocalpath'
        ),
        Node(
            package='ssak3',
            node_executable='path_tracking',
            node_name='followTheCarrot'
        ),
        Node(
            package='ssak3',
            node_executable='laundry',
            node_name='laundry_detector'
        ),
        Node(
            package='ssak3',
            node_executable='up_object',
            node_name='up_object'
        ),
        '''
        point_pub은 개별 실행
        Node(
            package='ssak3',
            node_executable='point_pub',
            node_name='PointList'
        ),
       '''
    ])