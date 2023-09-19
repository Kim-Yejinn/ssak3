from setuptools import setup

package_name = 'ssak3'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='SSAFY',
    maintainer_email='kky156@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = ssak3.my_node:main',
            'load_map = ssak3.load_map:main',
            'odom = ssak3.odom:main',     
            'a_star = ssak3.a_star:main',
            'a_star_local_path = ssak3.a_star_local_path:main',
            'path_pub = ssak3.path_pub:main',
            'path_tracking = ssak3.path_tracking:main',
            'point_pub = ssak3.point_pub:main',
            'up_object = ssak3.up_object:main',
            'slam = ssak3.slam:main',
            'laundry = ssak3.laundry_detect:main',
            'ex_calib = ssak3.ex_calib:main'
        ],
    },
)
