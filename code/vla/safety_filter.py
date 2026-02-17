#!/usr/bin/env python3
"""Safety filter for humanoid robot action plans.

Module 4, Artifact A-015

Validates every action plan from the LLM before it reaches ROS 2.
Five-stage validation: schema, whitelist, bounds, rate, confidence.

No action reaches the robot without passing ALL stages.

Usage:
    ros2 run vla safety_filter
"""

import json
import logging
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

logger = logging.getLogger('safety_filter')

# Allowed action types — anything not in this set is rejected
ALLOWED_ACTIONS = frozenset({
    'navigate', 'detect', 'interact', 'wait', 'speak', 'stop',
})

# Physical bounds for action parameters
BOUNDS = {
    'max_nav_distance': 50.0,       # meters
    'max_velocity': 0.5,            # m/s
    'max_wait_duration': 60.0,      # seconds
    'workspace_x': (-10.0, 10.0),   # meters
    'workspace_y': (-10.0, 10.0),   # meters
    'workspace_z': (0.0, 2.0),      # meters
}


def validate_schema(plan: dict) -> tuple[bool, str]:
    """Stage 1: Verify the plan has required fields and types."""
    if not isinstance(plan, dict):
        return False, 'Plan must be a JSON object'

    for field in ('intent', 'confidence', 'actions'):
        if field not in plan:
            return False, f'Missing required field: {field}'

    if not isinstance(plan['actions'], list):
        return False, 'actions must be a list'

    if not isinstance(plan['confidence'], (int, float)):
        return False, 'confidence must be a number'

    if not 0.0 <= plan['confidence'] <= 1.0:
        return False, 'confidence must be between 0.0 and 1.0'

    return True, ''


def validate_whitelist(plan: dict) -> tuple[bool, str]:
    """Stage 2: Only allowed action types pass."""
    for i, action in enumerate(plan['actions']):
        if not isinstance(action, dict):
            return False, f'Action {i} is not a dict'
        action_type = action.get('type')
        if action_type not in ALLOWED_ACTIONS:
            return False, f'Action type "{action_type}" not in whitelist'

    return True, ''


def validate_bounds(plan: dict) -> tuple[bool, str]:
    """Stage 3: Enforce physical constraints on parameters."""
    for i, action in enumerate(plan['actions']):
        atype = action['type']

        if atype == 'navigate':
            coords = action.get('destination_coords')
            if coords and isinstance(coords, (list, tuple)) and len(coords) >= 2:
                x, y = coords[0], coords[1]
                if not (BOUNDS['workspace_x'][0] <= x <= BOUNDS['workspace_x'][1]):
                    return False, f'Action {i}: x={x} outside workspace'
                if not (BOUNDS['workspace_y'][0] <= y <= BOUNDS['workspace_y'][1]):
                    return False, f'Action {i}: y={y} outside workspace'

        elif atype == 'wait':
            duration = action.get('duration', 0)
            if duration > BOUNDS['max_wait_duration']:
                return False, (
                    f'Action {i}: wait {duration}s exceeds max '
                    f'{BOUNDS["max_wait_duration"]}s')
            if duration < 0:
                return False, f'Action {i}: negative wait duration'

        elif atype == 'interact':
            allowed_interactions = {'pick_up', 'place', 'push'}
            interaction = action.get('action', '')
            if interaction and interaction not in allowed_interactions:
                return False, f'Action {i}: interaction "{interaction}" not allowed'

    return True, ''


class RateLimiter:
    """Stage 4: Prevent rapid-fire commands."""

    def __init__(self, min_interval: float = 2.0):
        self.min_interval = min_interval
        self.last_command_time = 0.0

    def validate(self, plan: dict) -> tuple[bool, str]:
        now = time.time()
        elapsed = now - self.last_command_time
        if elapsed < self.min_interval:
            return False, (
                f'Rate limited: {elapsed:.1f}s since last command '
                f'(minimum {self.min_interval}s)')
        self.last_command_time = now
        return True, ''


def validate_confidence(plan: dict, threshold: float = 0.7) -> tuple[bool, str]:
    """Stage 5: Reject plans where the LLM is uncertain."""
    confidence = plan.get('confidence', 0.0)
    if confidence < threshold:
        return False, (
            f'Confidence {confidence:.2f} below threshold {threshold}')
    return True, ''


class SafetyFilter(Node):
    """ROS 2 node implementing the five-stage safety validation pipeline."""

    def __init__(self):
        super().__init__('safety_filter')

        # Parameters
        self.declare_parameter('confidence_threshold', 0.7)
        self.declare_parameter('rate_limit_seconds', 2.0)

        confidence_threshold = self.get_parameter('confidence_threshold').value
        rate_limit = self.get_parameter('rate_limit_seconds').value

        self.rate_limiter = RateLimiter(min_interval=rate_limit)

        # Build validator chain
        self.validators = [
            ('schema', validate_schema),
            ('whitelist', validate_whitelist),
            ('bounds', validate_bounds),
            ('rate', self.rate_limiter.validate),
            ('confidence', lambda p: validate_confidence(p, confidence_threshold)),
        ]

        # Subscribe to action plans
        self.plan_sub = self.create_subscription(
            String, '/action_plan', self.plan_callback, 10)

        # Publish validated plans
        self.validated_pub = self.create_publisher(
            String, '/validated_plan', 10)

        # Publish rejection reasons (for monitoring)
        self.rejection_pub = self.create_publisher(
            String, '/safety_rejections', 10)

        self.get_logger().info(
            f'SafetyFilter ready. confidence>={confidence_threshold}, '
            f'rate_limit={rate_limit}s')

    def plan_callback(self, msg: String):
        """Validate an incoming action plan."""
        try:
            plan = json.loads(msg.data)
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Invalid JSON in action plan: {e}')
            return

        is_safe, validated_plan, rejections = self.validate(plan)

        if is_safe:
            self.get_logger().info(
                f'SAFETY PASSED: intent={plan.get("intent")}')
            out = String()
            out.data = json.dumps(validated_plan)
            self.validated_pub.publish(out)
        else:
            self.get_logger().warn(
                f'SAFETY REJECTED: {rejections}')
            rej_msg = String()
            rej_msg.data = json.dumps({
                'rejected': True,
                'reasons': rejections,
                'plan': plan,
            })
            self.rejection_pub.publish(rej_msg)

    def validate(self, plan: dict) -> tuple[bool, dict, list[str]]:
        """Run all validation stages on a plan.

        Returns:
            (is_safe, plan, rejections) tuple.
        """
        rejections = []

        for name, validator in self.validators:
            is_valid, reason = validator(plan)
            if not is_valid:
                rejections.append(f'{name}: {reason}')

        if rejections:
            return False, plan, rejections

        return True, plan, []


def main(args=None):
    rclpy.init(args=args)
    node = SafetyFilter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
