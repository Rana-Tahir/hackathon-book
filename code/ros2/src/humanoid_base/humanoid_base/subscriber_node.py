"""Joint state subscriber node for the humanoid robot.

Subscribes to /joint_states and logs the current positions of
all humanoid joints. Used for monitoring and debugging.

Topic: /joint_states (sensor_msgs/JointState)
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class JointStateSubscriber(Node):
    """Subscribes to joint states and logs them."""

    def __init__(self):
        super().__init__('joint_state_subscriber')

        self.declare_parameter('log_interval', 1.0)
        self.log_interval = self.get_parameter('log_interval').value

        self.subscription = self.create_subscription(
            JointState, '/joint_states', self.listener_callback, 10
        )
        self.last_log_time = self.get_clock().now()

        self.get_logger().info('Joint state subscriber started')

    def listener_callback(self, msg: JointState):
        """Process incoming joint state messages."""
        now = self.get_clock().now()
        elapsed = (now - self.last_log_time).nanoseconds / 1e9

        # Rate-limit logging to avoid flooding the terminal
        if elapsed >= self.log_interval:
            self.last_log_time = now
            self._log_joint_states(msg)

    def _log_joint_states(self, msg: JointState):
        """Format and log joint state information."""
        if not msg.name:
            self.get_logger().warn('Received empty joint state message')
            return

        lines = ['Current joint states:']
        for i, name in enumerate(msg.name):
            pos = msg.position[i] if i < len(msg.position) else 0.0
            lines.append(f'  {name}: {pos:.3f} rad')

        self.get_logger().info('\n'.join(lines))


def main(args=None):
    rclpy.init(args=args)
    node = JointStateSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
