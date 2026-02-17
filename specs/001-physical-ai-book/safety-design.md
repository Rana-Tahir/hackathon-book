# Safety Layer Design

**Date**: 2026-02-13
**Constitution Reference**: Principle V — Safety Over Intelligence

## Architecture

LLM outputs MUST NEVER directly execute ROS 2 commands. The mandatory
pipeline is:

```text
LLM Output → Structured Schema → Validator → Safe Action → ROS 2 Action Server
```

## Structured Output Schema

All LLM outputs MUST conform to a JSON schema:

```json
{
  "intent": "navigate_to_object",
  "target": "red_ball",
  "actions": [
    {"type": "navigate", "goal": {"x": 2.0, "y": 1.5, "theta": 0.0}},
    {"type": "detect", "object": "red_ball"},
    {"type": "interact", "action": "pick_up"}
  ],
  "confidence": 0.92
}
```

## Command Whitelist

Only whitelisted action types are permitted:

| Action Type | Description | ROS 2 Mapping |
|-------------|-------------|--------------|
| `navigate` | Move to goal position | `NavigateToPose` action |
| `detect` | Identify object in scene | Vision detection service |
| `interact` | Pick up / place / push | Manipulation action |
| `stop` | Emergency halt | Cancel all goals |
| `speak` | Voice response | Audio output service |

Any action type NOT in this whitelist is REJECTED.

## Action Validation Rules

Before a command reaches ROS 2, the validator checks:

1. **Schema validity**: Output matches JSON schema
2. **Whitelist check**: All action types are whitelisted
3. **Confidence threshold**: Confidence >= 0.7 (configurable)
4. **Physical bounds**: Navigation goals within environment bounds
5. **Collision safety**: Goal not inside known obstacles
6. **Rate limiting**: Max 1 action sequence per 2 seconds

## Timeout Constraints

| Operation | Timeout | On Timeout |
|-----------|---------|-----------|
| LLM inference | 10 seconds | Return fallback "I didn't understand" |
| Navigation | 60 seconds | Cancel and report failure |
| Object detection | 5 seconds | Skip and report "object not found" |
| Manipulation | 30 seconds | Release and return to safe pose |

## Rollback Strategy

If any action in a sequence fails:

1. Cancel all remaining actions
2. Return robot to last known safe pose
3. Log the failure with full context
4. Report failure to the operator

## Emergency Stop

An emergency stop service MUST be available at all times:

- ROS 2 service: `/emergency_stop`
- Cancels all active goals
- Disables motor commands
- Logs the event
- Requires manual re-enable

## Manual Override Pathway

The operator can always:

1. Issue an emergency stop
2. Override any LLM-generated action
3. Switch to manual teleoperation mode
4. Review and approve action plans before execution (optional mode)

## Hallucination Mitigation

1. **Output parsing**: Strict JSON schema validation; malformed output rejected
2. **Action grounding**: All referenced objects must exist in the current
   scene perception output
3. **Command whitelist**: Only known action types execute
4. **Confidence gating**: Low-confidence outputs trigger clarification request
5. **History check**: Flag repeated failures as potential hallucination pattern
