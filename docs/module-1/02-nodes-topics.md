---
sidebar_position: 2
title: Nodes, Topics, and Messages
---

# Nodes, Topics, and Messages

In this chapter, you will create your first ROS 2 nodes and wire them
together using topics. This is the foundation of robotic communication.

## Key Concepts

- **Node**: A process that performs computation. In our humanoid, each
  body function runs as a separate node.
- **Topic**: A named channel for streaming data. Nodes publish messages
  to topics and subscribe to receive them.
- **Message**: A structured data type (like `JointState`) that flows
  through topics.

## Creating the Workspace

First, create the ROS 2 workspace:

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Copy the humanoid_base package from the book's code directory
cp -r /path/to/book/code/ros2/src/humanoid_base .

# Build the workspace
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

## The Publisher Node

The publisher node sends joint commands to the humanoid robot. It
publishes `sensor_msgs/JointState` messages to `/joint_commands` at
10 Hz.

**File**: `code/ros2/src/humanoid_base/humanoid_base/publisher_node.py`

```python
class JointCommandPublisher(Node):
    """Publishes joint commands to control the humanoid robot."""

    JOINT_NAMES = [
        'head_pan', 'head_tilt',
        'left_shoulder_pitch', 'left_shoulder_roll',
        'left_elbow_pitch',
        'right_shoulder_pitch', 'right_shoulder_roll',
        'right_elbow_pitch',
        # ... hip, knee, ankle joints
    ]

    def __init__(self):
        super().__init__('joint_command_publisher')
        self.publisher_ = self.create_publisher(
            JointState, '/joint_commands', 10
        )
        self.timer = self.create_timer(0.1, self.timer_callback)
```

Key points:
- `create_publisher(JointState, '/joint_commands', 10)` creates a
  publisher on the `/joint_commands` topic with a queue size of 10.
- `create_timer(0.1, self.timer_callback)` calls the callback at 10 Hz.
- Each joint gets a sinusoidal position for smooth demonstration motion.

## The Subscriber Node

The subscriber listens to `/joint_states` and logs the robot's current
positions.

**File**: `code/ros2/src/humanoid_base/humanoid_base/subscriber_node.py`

```python
class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__('joint_state_subscriber')
        self.subscription = self.create_subscription(
            JointState, '/joint_states', self.listener_callback, 10
        )
```

## Running the Nodes

In separate terminals:

```bash
# Terminal 1: Run the publisher
source ~/ros2_ws/install/setup.bash
ros2 run humanoid_base joint_command_publisher

# Terminal 2: Run the subscriber
source ~/ros2_ws/install/setup.bash
ros2 run humanoid_base joint_state_subscriber

# Terminal 3: Inspect topics
ros2 topic list
ros2 topic echo /joint_commands
ros2 topic info /joint_commands
```

## Verifying Communication

Check the ROS graph to see your nodes and topics:

```bash
ros2 node list
# Expected: /joint_command_publisher, /joint_state_subscriber

ros2 topic list
# Expected: /joint_commands, /joint_states, /parameter_events, /rosout

ros2 topic hz /joint_commands
# Expected: ~10 Hz
```

## Message Types

ROS 2 uses strongly typed messages. The `JointState` message contains:

```text
std_msgs/Header header
string[] name       # Joint names
float64[] position  # Joint positions (radians)
float64[] velocity  # Joint velocities (rad/s)
float64[] effort    # Joint efforts (Nm)
```

Inspect any message type:

```bash
ros2 interface show sensor_msgs/msg/JointState
```

## What You Built

You now have two communicating nodes:

```text
JointCommandPublisher  ──/joint_commands──>  [Available for controllers]
[State publishers]     ──/joint_states──>    JointStateSubscriber
```

Next, you will add services and actions for more complex interactions.
