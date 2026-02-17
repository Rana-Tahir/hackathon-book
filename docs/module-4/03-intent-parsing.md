---
sidebar_position: 3
title: "LLM Intent Parsing"
---

# LLM Intent Parsing

The intent parser converts natural language commands into structured
JSON action plans that the robot can execute.

## Input and Output

**Input** (from Whisper):
```
"Go to the kitchen table and pick up the red cup"
```

**Output** (structured JSON):
```json
{
  "intent": "fetch_object",
  "confidence": 0.92,
  "actions": [
    {"type": "navigate", "destination": "kitchen_table"},
    {"type": "detect", "object": "red cup"},
    {"type": "interact", "action": "pick_up", "object": "red cup"}
  ]
}
```

## System Prompt

The system prompt constrains the LLM to produce valid action plans:

```python
SYSTEM_PROMPT = """You are a humanoid robot action planner.

Given a voice command, output a JSON action plan.

ALLOWED ACTION TYPES (use ONLY these):
- navigate: move to a location
- detect: find an object visually
- interact: physical manipulation (pick_up, place, push)
- wait: pause for a duration
- speak: say something to the user
- stop: halt all motion immediately

OUTPUT FORMAT (JSON only, no other text):
{
  "intent": "<short description>",
  "confidence": <0.0-1.0>,
  "actions": [
    {"type": "<action_type>", ...action-specific fields}
  ]
}

RULES:
- Always detect an object before interacting with it
- Navigate to a location before detecting objects there
- If the command is unclear, set confidence below 0.5
- Never output action types not in the list above
"""
```

## Implementation

See `code/vla/intent_parser.py` for the complete implementation:

```python
import json
import re


class IntentParser:
    def __init__(self, llm_client, system_prompt=SYSTEM_PROMPT):
        self.client = llm_client
        self.system_prompt = system_prompt

    def parse(self, command_text, scene_description=""):
        prompt = f"{self.system_prompt}\n\nSCENE: {scene_description}\n\nCOMMAND: {command_text}"

        response = self.client.generate(prompt)
        cleaned = self._clean_output(response)

        try:
            plan = json.loads(cleaned)
            self._validate_schema(plan)
            return plan
        except (json.JSONDecodeError, ValueError) as e:
            return {
                "intent": "parse_error",
                "confidence": 0.0,
                "actions": [],
                "error": str(e)
            }

    def _clean_output(self, raw):
        """Strip markdown fences and extra text."""
        text = raw.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def _validate_schema(self, plan):
        """Validate the plan has required fields."""
        required = ["intent", "confidence", "actions"]
        for field in required:
            if field not in plan:
                raise ValueError(f"Missing required field: {field}")
        if not isinstance(plan["actions"], list):
            raise ValueError("actions must be a list")
```

## Emergency Keywords

Critical commands bypass the LLM entirely:

```python
EMERGENCY_KEYWORDS = {"stop", "halt", "freeze", "emergency", "cancel"}

def check_emergency(text):
    words = set(text.lower().split())
    if words & EMERGENCY_KEYWORDS:
        return {"intent": "emergency_stop", "confidence": 1.0,
                "actions": [{"type": "stop"}]}
    return None
```

## What You Built

- LLM-based intent parser producing structured action plans
- System prompt constraining output to valid action types
- Schema validation catching malformed responses
- Emergency keyword bypass for safety-critical commands

Next: validate action plans through the safety filter.
