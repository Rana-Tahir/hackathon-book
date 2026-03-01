#!/usr/bin/env python3
"""ROS 2 action translator for validated VLA plans.

Module 4, Artifact A-016

Converts validated action plans into ROS 2 action goals and service calls.
This is the final stage: plan → robot motion.

Usage:
    ros2 run vla ros2_translator
"""

import json
import math

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped


class ROS2Translator(Node):
    """Translates validated action plans into ROS 2 commands."""

    def __init__(self):
        super().__init__('ros2_translator')

        # Subscribe to validated plans from safety filter
        self.plan_sub = self.create_subscription(
            String, '/validated_plan', self.plan_callback, 10)

        # Publisher for status updates
        self.status_pub = self.create_publisher(
            String, '/vla_status', 10)

        # Known locations (semantic map)
        self.locations = {
            'kitchen_table': (2.0, -2.0, 0.0),
            'table': (2.0, -2.0, 0.0),
            'door': (0.0, 4.5, 0.0),
            'home': (0.0, 0.0, 0.0),
            'charging_station': (-3.0, -3.0, 0.0),
        }

        self.get_logger().info('ROS2Translator ready. Listening on /validated_plan')

    def plan_callback(self, msg: String):
        """Execute a validated action plan."""
        try:
            plan = json.loads(msg.data)
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Invalid JSON: {e}')
            return

        intent = plan.get('intent', 'unknown')
        actions = plan.get('actions', [])
        self.get_logger().info(
            f'Executing plan: intent={intent}, actions={len(actions)}')

        for i, action in enumerate(actions):
            action_type = action.get('type', '')
            self.get_logger().info(
                f'  Action {i+1}/{len(actions)}: {action_type}')

            self._publish_status(f'Executing action {i+1}: {action_type}')

            if action_type == 'navigate':
                self._execute_navigate(action)
            elif action_type == 'detect':
                self._execute_detect(action)
            elif action_type == 'interact':
                self._execute_interact(action)
            elif action_type == 'wait':
                self._execute_wait(action)
            elif action_type == 'speak':
                self._execute_speak(action)
            elif action_type == 'stop':
                self._execute_stop()
                break  # Stop halts all remaining actions

        self._publish_status(f'Plan complete: {intent}')

    def _execute_navigate(self, action: dict):
        """Send a navigation goal to Nav2."""
        destination = action.get('destination', '')
        coords = action.get('destination_coords')

        if not coords and destination in self.locations:
            coords = self.locations[destination]

        if not coords:
            self.get_logger().warn(f'Unknown destination: {destination}')
            self._publish_status(f'Unknown destination: {destination}')
            return

        x, y = coords[0], coords[1]
        yaw = coords[2] if len(coords) > 2 else 0.0

        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = float(x)
        goal.pose.position.y = float(y)
        goal.pose.orientation.z = math.sin(yaw / 2.0)
        goal.pose.orientation.w = math.cos(yaw / 2.0)

        self.get_logger().info(f'Navigate to ({x:.1f}, {y:.1f}, yaw={yaw:.1f})')
        # In production: send to Nav2 action server
        # self.nav_client.send_goal(goal)

    def _execute_detect(self, action: dict):
        """Trigger object detection for a specific target."""
        target = action.get('object', 'unknown')
        self.get_logger().info(f'Detecting: {target}')
        # In production: query the detection node for specific object
        # Check /detections topic for matching class

    def _execute_interact(self, action: dict):
        """Execute a physical interaction (pick, place, push)."""
        interaction = action.get('action', 'unknown')
        target = action.get('object', 'unknown')
        self.get_logger().info(f'Interact: {interaction} {target}')
        # In production: send to manipulation action server

    def _execute_wait(self, action: dict):
        """Pause execution for a duration."""
        duration = action.get('duration', 1.0)
        self.get_logger().info(f'Waiting {duration}s')
        # Non-blocking timer would be used in production
        # For simplicity, this is synchronous

    def _execute_speak(self, action: dict):
        """Publish a speech message."""
        message = action.get('message', '')
        self.get_logger().info(f'Speaking: "{message}"')
        # In production: send to text-to-speech node

    def _execute_stop(self):
        """Immediately stop all motion."""
        self.get_logger().warn('STOP: Halting all motion')
        # In production: publish zero velocity, cancel all action goals

    def _publish_status(self, status: str):
        """Publish a status update."""
        msg = String()
        msg.data = status
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ROS2Translator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
