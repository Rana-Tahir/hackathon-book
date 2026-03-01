---
sidebar_position: 4
title: "Safety Filter"
---

# Safety Filter

The safety filter is the gate between the LLM and the robot.
No action reaches ROS 2 without passing every validation stage.

## The Five Validation Stages

```
LLM Output ──► Schema ──► Whitelist ──► Bounds ──► Rate ──► Confidence ──► ROS 2
               Check      Check        Check      Check    Check
```

If any stage rejects, the entire plan is blocked and the rejection
reason is logged.

## Stage 1: Schema Validation

Verify the action plan has the correct structure:

```python
def validate_schema(plan):
    """Check that the plan has required fields and types."""
    if not isinstance(plan, dict):
        return False, "Plan must be a JSON object"
    for field in ["intent", "confidence", "actions"]:
        if field not in plan:
            return False, f"Missing field: {field}"
    if not isinstance(plan["actions"], list):
        return False, "actions must be a list"
    if not 0.0 <= plan["confidence"] <= 1.0:
        return False, "confidence must be 0.0-1.0"
    return True, ""
```

## Stage 2: Action Whitelist

Only allowed action types pass:

```python
ALLOWED_ACTIONS = {"navigate", "detect", "interact", "wait", "speak", "stop"}

def validate_whitelist(plan):
    for action in plan["actions"]:
        if action.get("type") not in ALLOWED_ACTIONS:
            return False, f"Action type '{action.get('type')}' not allowed"
    return True, ""
```

## Stage 3: Physical Bounds

Enforce physical constraints on action parameters:

```python
BOUNDS = {
    "max_nav_distance": 50.0,      # meters
    "max_velocity": 0.5,           # m/s
    "max_wait_duration": 60.0,     # seconds
    "workspace_x": (-10.0, 10.0),  # meters
    "workspace_y": (-10.0, 10.0),
}

def validate_bounds(plan):
    for action in plan["actions"]:
        if action["type"] == "navigate":
            dest = action.get("destination_coords")
            if dest:
                x, y = dest
                if not (BOUNDS["workspace_x"][0] <= x <= BOUNDS["workspace_x"][1]):
                    return False, f"X={x} outside workspace"
        if action["type"] == "wait":
            duration = action.get("duration", 0)
            if duration > BOUNDS["max_wait_duration"]:
                return False, f"Wait {duration}s exceeds max {BOUNDS['max_wait_duration']}s"
    return True, ""
```

## Stage 4: Rate Limiting

Prevent rapid-fire commands that could destabilize the robot:

```python
import time

class RateLimiter:
    def __init__(self, min_interval=2.0):
        self.min_interval = min_interval
        self.last_command_time = 0.0

    def validate(self, plan):
        now = time.time()
        elapsed = now - self.last_command_time
        if elapsed < self.min_interval:
            return False, f"Rate limited: {elapsed:.1f}s < {self.min_interval}s minimum"
        self.last_command_time = now
        return True, ""
```

## Stage 5: Confidence Check

Reject plans where the LLM is uncertain:

```python
def validate_confidence(plan, threshold=0.7):
    if plan["confidence"] < threshold:
        return False, f"Confidence {plan['confidence']:.2f} below threshold {threshold}"
    return True, ""
```

## Complete Safety Filter

See `code/vla/safety_filter.py` for the full implementation:

```python
class SafetyFilter:
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.validators = [
            ("schema", validate_schema),
            ("whitelist", validate_whitelist),
            ("bounds", validate_bounds),
            ("rate", self.rate_limiter.validate),
            ("confidence", validate_confidence),
        ]

    def validate(self, plan):
        rejections = []
        for name, validator in self.validators:
            is_valid, reason = validator(plan)
            if not is_valid:
                rejections.append(f"{name}: {reason}")

        if rejections:
            return False, plan, rejections
        return True, plan, []
```

## Logging Rejections

Every rejection is logged for debugging and safety auditing:

```python
if not is_safe:
    logger.warning("SAFETY REJECTED: %s", rejections)
    logger.warning("Plan was: %s", json.dumps(plan, indent=2))
```

## Tuning the Filter

| Problem | Adjustment |
|---------|-----------|
| Too many false rejections | Lower confidence threshold (not below 0.5) |
| Commands rejected as out of bounds | Measure your environment, expand workspace |
| Rate limiting blocks follow-up commands | Reduce min_interval |
| Hallucinated actions getting through | This should never happen — check whitelist |

**Target: zero false negatives** (never pass a dangerous plan).
Accept some false positives rather than risk unsafe actions.

## What You Built

- Five-stage safety validation pipeline
- Action whitelist preventing hallucinated action types
- Physical bounds enforcing workspace limits
- Rate limiting preventing command flooding
- Confidence gating rejecting uncertain plans
- Complete audit log of all rejections

Next: ground LLM outputs in visual perception.
