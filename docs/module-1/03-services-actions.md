---
sidebar_position: 3
title: Services and Actions
---

# Services and Actions

Topics work well for streaming data, but sometimes you need:

- A **request-response** pattern (services)
- A **long-running task** with progress feedback (actions)

## Services: Quick Request-Response

A service is a synchronous call. The client sends a request and waits
for a response. Use services for operations that complete quickly.

**Example**: Move all joints to home position.

**File**: `code/ros2/src/humanoid_base/humanoid_base/joint_service.py`

```python
class JointService(Node):
    def __init__(self):
        super().__init__('joint_service')
        self.srv = self.create_service(
            SetBool, '/go_home', self.go_home_callback
        )

    def go_home_callback(self, request, response):
        if request.data:
            # Publish home positions to /joint_commands
            response.success = True
            response.message = 'All joints moved to home position'
        return response
```

### Running the Service

```bash
# Terminal 1: Start the service
ros2 run humanoid_base joint_service

# Terminal 2: Call the service
ros2 service call /go_home std_srvs/srv/SetBool "{data: true}"
```

### When to Use Services

| Use Case | Why |
|----------|-----|
| Reset to home position | Quick, atomic operation |
| Query current state | Read-only, fast |
| Enable/disable a mode | Toggle operation |

## Actions: Long-Running Tasks with Feedback

Actions are for tasks that take time — like moving to a target position
through multiple intermediate steps. Actions provide:

- **Goal**: What you want to achieve
- **Feedback**: Progress updates during execution
- **Result**: Final outcome when complete
- **Cancellation**: Ability to stop mid-execution

**File**: `code/ros2/src/humanoid_base/humanoid_base/move_action.py`

```python
class MoveActionServer(Node):
    def __init__(self):
        super().__init__('move_action_server')
        self._action_server = ActionServer(
            self, Fibonacci, '/move_joints',
            self.execute_callback
        )

    async def execute_callback(self, goal_handle):
        for i in range(steps):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return result
            # Publish interpolated joint positions
            goal_handle.publish_feedback(feedback_msg)
        goal_handle.succeed()
        return result
```

### Running the Action

```bash
# Terminal 1: Start the action server
ros2 run humanoid_base move_action_server

# Terminal 2: Send a goal
ros2 action send_goal /move_joints example_interfaces/action/Fibonacci "{order: 10}"
```

### Services vs Actions

| Feature | Service | Action |
|---------|---------|--------|
| Duration | Milliseconds | Seconds to minutes |
| Feedback | None | Continuous progress |
| Cancellation | Not supported | Supported |
| Use case | Quick queries, toggles | Movement, navigation |

## What You Built

Your humanoid now has three communication patterns:

```text
Topics:   Streaming data    (joint commands, joint states)
Services: Quick operations  (go home, query status)
Actions:  Complex movements (multi-step trajectories)
```

Next, you will define the robot's physical body using URDF.
