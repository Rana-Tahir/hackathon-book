from setuptools import find_packages, setup

package_name = 'humanoid_base'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            ['launch/humanoid_bringup.launch.py']),
        ('share/' + package_name + '/config',
            ['config/humanoid_params.yaml']),
        ('share/' + package_name + '/urdf',
            ['urdf/humanoid.urdf.xacro']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Author',
    maintainer_email='author@example.com',
    description='Base ROS 2 package for humanoid robot control',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'joint_command_publisher = humanoid_base.publisher_node:main',
            'joint_state_subscriber = humanoid_base.subscriber_node:main',
            'joint_service = humanoid_base.joint_service:main',
            'move_action_server = humanoid_base.move_action:main',
        ],
    },
)
