"""Move action server for the humanoid robot.

Provides an action server for executing multi-step joint movements
with feedback and cancellation support.

This example uses a simple approach with the FollowJointTrajectory
action pattern. For brevity, it uses a timer-based interpolation
rather than the full control_msgs action type.

Action: /move_joints (custom timer-based movement)
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.callback_groups import ReentrantCallbackGroup
from sensor_msgs.msg import JointState
from example_interfaces.action import Fibonacci
import time
import math


class MoveActionServer(Node):
    """Action server for multi-step humanoid joint movements.

    Uses Fibonacci action as a stand-in to demonstrate the action
    pattern. In production, use control_msgs/FollowJointTrajectory.
    """

    def __init__(self):
        super().__init__('move_action_server')

        self._action_server = ActionServer(
            self,
            Fibonacci,
            '/move_joints',
            self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
        )

        self.publisher_ = self.create_publisher(
            JointState, '/joint_commands', 10
        )

        self.get_logger().info('Move action server ready: /move_joints')

    async def execute_callback(self, goal_handle):
        """Execute a multi-step joint movement with progress feedback."""
        self.get_logger().info('Executing movement...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        # Simulate a multi-step movement over N steps
        order = goal_handle.request.order
        steps = max(order, 5)

        for i in range(1, steps):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Movement cancelled')
                result = Fibonacci.Result()
                result.sequence = feedback_msg.partial_sequence
                return result

            # Publish interpolated joint positions
            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.name = ['head_pan']
            progress = i / steps
            msg.position = [math.sin(progress * math.pi)]
            self.publisher_.publish(msg)

            # Update feedback
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[-1]
                + feedback_msg.partial_sequence[-2]
            )
            goal_handle.publish_feedback(feedback_msg)

            self.get_logger().info(
                f'Step {i}/{steps} complete ({progress:.0%})'
            )
            time.sleep(0.5)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        self.get_logger().info('Movement complete')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = MoveActionServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
