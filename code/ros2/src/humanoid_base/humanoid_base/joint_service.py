"""Joint position service for the humanoid robot.

Provides a service to request specific joint positions.
Uses std_srvs/SetBool as a simple example; a real implementation
would use a custom service type.

Service: /set_joint_positions (std_srvs/SetBool)
"""

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from sensor_msgs.msg import JointState


class JointService(Node):
    """Service node that accepts joint position requests."""

    HOME_POSITIONS = {
        'head_pan': 0.0, 'head_tilt': 0.0,
        'left_shoulder_pitch': 0.0, 'left_shoulder_roll': 0.0,
        'left_elbow_pitch': 0.0,
        'right_shoulder_pitch': 0.0, 'right_shoulder_roll': 0.0,
        'right_elbow_pitch': 0.0,
        'left_hip_pitch': 0.0, 'left_hip_roll': 0.0,
        'left_knee_pitch': 0.0, 'left_ankle_pitch': 0.0,
        'right_hip_pitch': 0.0, 'right_hip_roll': 0.0,
        'right_knee_pitch': 0.0, 'right_ankle_pitch': 0.0,
    }

    def __init__(self):
        super().__init__('joint_service')

        self.srv = self.create_service(
            SetBool, '/go_home', self.go_home_callback
        )
        self.publisher_ = self.create_publisher(
            JointState, '/joint_commands', 10
        )

        self.get_logger().info('Joint service ready: /go_home')

    def go_home_callback(self, request, response):
        """Move all joints to home position when requested."""
        if request.data:
            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.name = list(self.HOME_POSITIONS.keys())
            msg.position = list(self.HOME_POSITIONS.values())
            msg.velocity = [0.0] * len(self.HOME_POSITIONS)
            msg.effort = [0.0] * len(self.HOME_POSITIONS)

            self.publisher_.publish(msg)

            response.success = True
            response.message = 'All joints moved to home position'
            self.get_logger().info('Joints moved to home position')
        else:
            response.success = False
            response.message = 'Request denied: data=False'

        return response


def main(args=None):
    rclpy.init(args=args)
    node = JointService()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
