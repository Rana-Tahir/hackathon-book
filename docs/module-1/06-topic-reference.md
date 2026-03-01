---
sidebar_position: 6
title: Topic & Service Reference
---

# Topic & Service Reference

This page is a complete reference for every ROS 2 topic, service,
and action exposed by the Module 1 humanoid base system.

## Topics

### `/joint_commands` (Published)

Sinusoidal joint position commands for all 16 DOF.

| Field | Value |
|-------|-------|
| **Type** | `sensor_msgs/msg/JointState` |
| **Publisher** | `joint_command_publisher` |
| **Rate** | 10 Hz (configurable via `publish_rate`) |
| **Frame ID** | `base_link` |

**Message fields:**

```
header:
  stamp: <current time>
  frame_id: "base_link"
name: [head_pan, head_tilt, left_shoulder_pitch, ...]  # 16 joints
position: [0.25, -0.1, 0.5, ...]  # radians (sinusoidal)
velocity: []
effort: []
```

**Joint names (16 total):**

| Group | Joints |
|-------|--------|
| Head | `head_pan`, `head_tilt` |
| Left arm | `left_shoulder_pitch`, `left_shoulder_roll`, `left_elbow_pitch` |
| Right arm | `right_shoulder_pitch`, `right_shoulder_roll`, `right_elbow_pitch` |
| Left leg | `left_hip_pitch`, `left_hip_roll`, `left_knee_pitch`, `left_ankle_pitch` |
| Right leg | `right_hip_pitch`, `right_hip_roll`, `right_knee_pitch`, `right_ankle_pitch` |

### `/joint_states` (Subscribed)

Joint state feedback (published by `robot_state_publisher` or simulation).

| Field | Value |
|-------|-------|
| **Type** | `sensor_msgs/msg/JointState` |
| **Subscriber** | `joint_state_subscriber` |
| **Log rate** | Every 1.0 s (configurable via `log_interval`) |

### `/robot_description` (Published)

URDF XML string for the robot model.

| Field | Value |
|-------|-------|
| **Type** | `std_msgs/msg/String` |
| **Publisher** | `robot_state_publisher` |
| **Latched** | Yes (transient local QoS) |

### `/tf` and `/tf_static`

Transform tree computed from URDF and joint states.

| Field | Value |
|-------|-------|
| **Type** | `tf2_msgs/msg/TFMessage` |
| **Publisher** | `robot_state_publisher` |

## Services

### `/go_home`

Commands all joints to their home (zero) position.

| Field | Value |
|-------|-------|
| **Type** | `std_srvs/srv/SetBool` |
| **Server** | `joint_service` |

**Request:**
```
data: true   # Trigger go-home
```

**Response:**
```
success: true
message: "All joints set to home position"
```

**Calling the service:**
```bash
ros2 service call /go_home std_srvs/srv/SetBool "{data: true}"
```

## Actions

### `/move_joints`

Multi-step joint movement with progress feedback.

| Field | Value |
|-------|-------|
| **Type** | `action_msgs` (Fibonacci stand-in) |
| **Server** | `move_action_server` |

**Note:** Module 1 uses the Fibonacci action type as a placeholder.
Module 2 replaces this with a custom action interface for actual
joint trajectory execution.

**Sending a goal:**
```bash
ros2 action send_goal /move_joints example_interfaces/action/Fibonacci \
  "{order: 5}"
```

## Introspection Commands

Quick-reference for debugging the running system:

```bash
# List all active topics
ros2 topic list

# Show topic type and publishers/subscribers
ros2 topic info /joint_commands -v

# Echo live messages
ros2 topic echo /joint_commands

# Measure publishing rate
ros2 topic hz /joint_commands

# List all services
ros2 service list

# Show service type
ros2 service type /go_home

# List all actions
ros2 action list

# Show action info
ros2 action info /move_joints

# View the full node graph
ros2 node list
ros2 node info /joint_command_publisher
```

## QoS Profiles

All Module 1 nodes use default QoS (reliable, volatile, keep-last 10).
The `robot_description` topic uses transient-local durability so
late-joining subscribers receive the URDF.

## What You Built

A complete communication layer:
- 1 command topic (16-joint sinusoidal demo)
- 1 state feedback subscription
- 1 service (go_home)
- 1 action server (multi-step movement)
- TF transform tree from URDF

Next, learn how to debug when things go wrong.
