---
sidebar_position: 2
title: "End-to-End Testing"
---

# End-to-End Testing

Systematic testing validates that every component works individually
and together. This chapter defines the test plan for the capstone.

## Test Levels

```
Unit Tests ──► Integration Tests ──► System Tests ──► Acceptance Tests
(per node)     (module pairs)        (full pipeline)   (user scenarios)
```

## Unit Tests

Each node is testable in isolation:

### Module 1: Joint Control

```bash
# Verify publisher publishes at correct rate
ros2 topic hz /joint_commands
# Expected: 10 Hz ± 1 Hz

# Verify go_home service
ros2 service call /go_home std_srvs/srv/SetBool "{data: true}"
# Expected: success=true
```

### Module 3: Object Detection

```bash
# Publish a test image, verify detection output
ros2 topic pub /camera/image sensor_msgs/msg/Image <test_data>
ros2 topic echo /detections --once
# Expected: detections with class labels and bounding boxes
```

### Module 4: Safety Filter

```python
# Test with known-safe plan
safe_plan = {"intent": "navigate", "confidence": 0.9,
             "actions": [{"type": "navigate", "destination": "table"}]}
assert safety_filter.validate(safe_plan)[0] == True

# Test with dangerous plan
dangerous_plan = {"intent": "fly", "confidence": 0.9,
                  "actions": [{"type": "launch_missile"}]}
assert safety_filter.validate(dangerous_plan)[0] == False
```

## Integration Tests

Test module pairs working together:

| Test | Modules | Verification |
|------|---------|-------------|
| Sim + Perception | 2 + 3 | Camera images → detections in < 100 ms |
| Perception + Nav | 3 + 3 | SLAM → Nav2 navigates to goal |
| Voice + Action | 4 + 1 | Voice command → joint motion |
| Nav + Safety | 3 + 4 | Navigation goal passes safety filter |

## System Test: Object Retrieval

The full end-to-end test:

```python
def test_object_retrieval():
    """Test the complete voice-commanded object retrieval scenario."""
    # 1. Start simulation with objects on table
    launch_simulation(world="humanoid_world", objects=["red_cup"])

    # 2. Send voice command
    send_audio("go to the table and pick up the red cup")

    # 3. Wait for pipeline to process
    wait_for_action_start(timeout=10.0)

    # 4. Verify navigation started
    assert get_nav_status() == "NAVIGATING"

    # 5. Wait for navigation to complete
    wait_for_nav_complete(timeout=60.0)

    # 6. Verify detection
    detections = get_latest_detections()
    assert any(d["class"] == "cup" for d in detections)

    # 7. Verify interaction
    wait_for_interaction_complete(timeout=30.0)

    # 8. Verify return navigation
    wait_for_nav_complete(timeout=60.0)

    # 9. Verify task completion
    assert get_task_status() == "COMPLETED"
```

## Performance Benchmarks

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Whisper latency | < 2 s | Time from audio end to text |
| LLM latency | < 3 s | Time from text to action plan |
| Safety validation | < 50 ms | Time through all 5 stages |
| Detection FPS | > 10 | `ros2 topic hz /detections` |
| Nav2 goal reach | < 30 s | Time from goal sent to reached |
| Total pipeline | < 10 s | Voice command to first motion |

## Failure Mode Testing

Test that failures are handled gracefully:

| Scenario | Expected Behavior |
|----------|------------------|
| Object not found | Robot reports "I don't see that" |
| Path blocked | Nav2 recovery, then report failure |
| Ambiguous command | Low confidence, ask for clarification |
| Emergency stop | Immediate halt, < 100 ms |
| LLM produces invalid JSON | Retry with cleaned output |
| Sensor failure | Node logs error, does not crash |

## Test Execution

```bash
# Run all tests
cd ~/ros2_ws
colcon test --packages-select humanoid_base perception navigation vla

# Run specific test
colcon test --packages-select humanoid_base --pytest-args -k "test_go_home"

# View test results
colcon test-result --all --verbose
```

## What You Built

- Comprehensive test plan covering unit, integration, and system levels
- Performance benchmarks with measurable targets
- Failure mode testing for graceful degradation
- Automated test execution via colcon
