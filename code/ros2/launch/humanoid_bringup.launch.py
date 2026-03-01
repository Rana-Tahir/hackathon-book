"""Launch file for the humanoid robot base system.

Launches all Module 1 nodes:
- robot_state_publisher (URDF → TF)
- joint_command_publisher (sinusoidal demo commands)
- joint_state_subscriber (state monitor)
- joint_service (go_home service)
- move_action_server (multi-step movement action)

Usage:
  ros2 launch humanoid_base humanoid_bringup.launch.py
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory('humanoid_base')

    # Path to URDF xacro
    urdf_file = os.path.join(pkg_dir, 'urdf', 'humanoid.urdf.xacro')

    # Path to parameter file
    params_file = os.path.join(pkg_dir, 'config', 'humanoid_params.yaml')

    # Robot state publisher — converts URDF to TF transforms
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_file])
        }],
        output='screen',
    )

    # Joint command publisher — demo sinusoidal movement
    joint_command_publisher = Node(
        package='humanoid_base',
        executable='joint_command_publisher',
        parameters=[params_file],
        output='screen',
    )

    # Joint state subscriber — monitors joint states
    joint_state_subscriber = Node(
        package='humanoid_base',
        executable='joint_state_subscriber',
        parameters=[params_file],
        output='screen',
    )

    # Joint service — go_home service
    joint_service = Node(
        package='humanoid_base',
        executable='joint_service',
        output='screen',
    )

    # Move action server — multi-step movement
    move_action_server = Node(
        package='humanoid_base',
        executable='move_action_server',
        output='screen',
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_command_publisher,
        joint_state_subscriber,
        joint_service,
        move_action_server,
    ])
