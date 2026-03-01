"""Joint command publisher node for the humanoid robot.

Publishes joint position commands to /joint_commands at 10 Hz.
Each message contains target positions for the humanoid's joints.

Topic: /joint_commands (sensor_msgs/JointState)
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math


class JointCommandPublisher(Node):
    """Publishes joint commands to control the humanoid robot."""

    # Humanoid joint names matching the URDF definition
    JOINT_NAMES = [
        'head_pan', 'head_tilt',
        'left_shoulder_pitch', 'left_shoulder_roll',
        'left_elbow_pitch',
        'right_shoulder_pitch', 'right_shoulder_roll',
        'right_elbow_pitch',
        'left_hip_pitch', 'left_hip_roll',
        'left_knee_pitch', 'left_ankle_pitch',
        'right_hip_pitch', 'right_hip_roll',
        'right_knee_pitch', 'right_ankle_pitch',
    ]

    def __init__(self):
        super().__init__('joint_command_publisher')

        # Declare parameters with defaults
        self.declare_parameter('publish_rate', 10.0)
        self.declare_parameter('wave_amplitude', 0.5)

        rate = self.get_parameter('publish_rate').value
        self.amplitude = self.get_parameter('wave_amplitude').value

        self.publisher_ = self.create_publisher(
            JointState, '/joint_commands', 10
        )
        self.timer = self.create_timer(1.0 / rate, self.timer_callback)
        self.t = 0.0

        self.get_logger().info(
            f'Joint command publisher started at {rate} Hz'
        )

    def timer_callback(self):
        """Publish joint commands with a simple sinusoidal wave pattern."""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.JOINT_NAMES

        # Generate smooth joint positions using sine waves
        # Each joint gets a slightly phase-shifted wave
        positions = []
        for i, _ in enumerate(self.JOINT_NAMES):
            phase = i * 0.3
            position = self.amplitude * math.sin(self.t + phase)
            positions.append(position)

        msg.position = positions
        msg.velocity = [0.0] * len(self.JOINT_NAMES)
        msg.effort = [0.0] * len(self.JOINT_NAMES)

        self.publisher_.publish(msg)
        self.t += 0.1


def main(args=None):
    rclpy.init(args=args)
    node = JointCommandPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
