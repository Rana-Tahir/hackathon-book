#!/usr/bin/env python3
"""LLM-based intent parser for humanoid robot commands.

Module 4, Artifact A-014

Converts natural language commands into structured JSON action plans
that the safety filter can validate and the ROS 2 translator can execute.

Usage:
    ros2 run vla intent_parser
"""

import json
import re
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Emergency keywords that bypass LLM processing
EMERGENCY_KEYWORDS = frozenset({
    'stop', 'halt', 'freeze', 'emergency', 'cancel', 'abort',
})

SYSTEM_PROMPT = """You are a humanoid robot action planner.

Given a voice command and scene description, output a JSON action plan.

ALLOWED ACTION TYPES (use ONLY these):
- navigate: move to a location. Fields: destination (string)
- detect: find an object visually. Fields: object (string)
- interact: physical manipulation. Fields: action (pick_up|place|push), object (string)
- wait: pause execution. Fields: duration (float, seconds)
- speak: say something. Fields: message (string)
- stop: halt all motion immediately. No additional fields.

OUTPUT FORMAT (valid JSON only, no other text):
{
  "intent": "<short description>",
  "confidence": <0.0-1.0>,
  "actions": [
    {"type": "<action_type>", ...action-specific fields}
  ]
}

RULES:
- Always detect an object before interacting with it.
- Navigate to a location before detecting objects there.
- If the command is ambiguous, set confidence below 0.5.
- Never use action types not in the allowed list.
- Output ONLY valid JSON. No markdown, no explanation.
"""


class IntentParser(Node):
    """ROS 2 node that parses voice commands into action plans."""

    def __init__(self):
        super().__init__('intent_parser')

        self.declare_parameter('confidence_threshold', 0.7)
        self.declare_parameter('max_retries', 2)

        self.confidence_threshold = self.get_parameter('confidence_threshold').value
        self.max_retries = self.get_parameter('max_retries').value

        # Subscribe to voice commands
        self.command_sub = self.create_subscription(
            String, '/voice_command', self.command_callback, 10)

        # Publish structured action plans
        self.plan_pub = self.create_publisher(
            String, '/action_plan', 10)

        self.get_logger().info('IntentParser ready. Listening on /voice_command')

    def command_callback(self, msg: String):
        """Parse a voice command into an action plan."""
        command = msg.data.strip()
        if not command:
            return

        self.get_logger().info(f'Parsing command: "{command}"')

        # Check for emergency keywords first
        emergency = self._check_emergency(command)
        if emergency:
            self.get_logger().warn(f'EMERGENCY command detected: {command}')
            self._publish_plan(emergency)
            return

        # Parse with LLM
        plan = self.parse_intent(command)
        self._publish_plan(plan)

    def parse_intent(self, command: str, scene_description: str = '') -> dict:
        """Parse a command into a structured action plan.

        Args:
            command: Natural language command text.
            scene_description: Current scene from perception (optional).

        Returns:
            Action plan dict with intent, confidence, and actions.
        """
        prompt = self._build_prompt(command, scene_description)

        for attempt in range(self.max_retries + 1):
            try:
                response = self._call_llm(prompt)
                cleaned = self._clean_output(response)
                plan = json.loads(cleaned)
                self._validate_schema(plan)
                self.get_logger().info(
                    f'Parsed: intent={plan["intent"]}, '
                    f'confidence={plan["confidence"]:.2f}, '
                    f'actions={len(plan["actions"])}')
                return plan
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                self.get_logger().warn(
                    f'Parse attempt {attempt+1} failed: {e}')
                if attempt == self.max_retries:
                    return self._error_plan(command, str(e))

        return self._error_plan(command, 'max retries exceeded')

    def _build_prompt(self, command: str, scene: str) -> str:
        """Build the LLM prompt with system instructions and context."""
        parts = [SYSTEM_PROMPT]
        if scene:
            parts.append(f'\nCURRENT SCENE:\n{scene}')
        parts.append(f'\nCOMMAND: {command}')
        return '\n'.join(parts)

    def _call_llm(self, prompt: str) -> str:
        """Call the LLM backend.

        Override this method to use your preferred LLM:
        - OpenAI API
        - Local model (llama.cpp, vLLM)
        - Anthropic API
        """
        # Placeholder: in production, replace with actual LLM call
        self.get_logger().warn('Using placeholder LLM. Override _call_llm().')
        return json.dumps({
            'intent': 'placeholder',
            'confidence': 0.0,
            'actions': [],
        })

    def _clean_output(self, raw: str) -> str:
        """Strip markdown fences and extra text from LLM output."""
        text = raw.strip()
        # Remove markdown code fences
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        return text.strip()

    def _validate_schema(self, plan: dict):
        """Validate the action plan schema."""
        required_fields = ['intent', 'confidence', 'actions']
        for field in required_fields:
            if field not in plan:
                raise ValueError(f'Missing required field: {field}')

        if not isinstance(plan['actions'], list):
            raise ValueError('actions must be a list')

        if not isinstance(plan['confidence'], (int, float)):
            raise ValueError('confidence must be a number')

        if not 0.0 <= plan['confidence'] <= 1.0:
            raise ValueError('confidence must be between 0.0 and 1.0')

        allowed_types = {'navigate', 'detect', 'interact', 'wait', 'speak', 'stop'}
        for action in plan['actions']:
            if not isinstance(action, dict):
                raise ValueError('each action must be a dict')
            if action.get('type') not in allowed_types:
                raise ValueError(f'Unknown action type: {action.get("type")}')

    def _check_emergency(self, text: str) -> dict | None:
        """Check for emergency keywords that bypass LLM."""
        words = set(text.lower().split())
        if words & EMERGENCY_KEYWORDS:
            return {
                'intent': 'emergency_stop',
                'confidence': 1.0,
                'actions': [{'type': 'stop'}],
            }
        return None

    def _error_plan(self, command: str, error: str) -> dict:
        """Create an error action plan."""
        return {
            'intent': 'parse_error',
            'confidence': 0.0,
            'actions': [],
            'error': error,
            'original_command': command,
        }

    def _publish_plan(self, plan: dict):
        """Publish the action plan as JSON string."""
        msg = String()
        msg.data = json.dumps(plan)
        self.plan_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = IntentParser()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
