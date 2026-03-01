---
sidebar_position: 5
title: Launch Files & Parameters
---

# Launch Files & Parameters

Launch files start multiple nodes with a single command. Parameters
let you configure nodes without changing source code.

## The Launch File

Our launch file lives at `code/ros2/launch/humanoid_bringup.launch.py`.
It starts five nodes:

| Node | Purpose |
|------|---------|
| `robot_state_publisher` | Converts URDF to TF transforms |
| `joint_command_publisher` | Publishes sinusoidal joint commands |
| `joint_state_subscriber` | Monitors and logs joint states |
| `joint_service` | Provides `/go_home` service |
| `move_action_server` | Multi-step movement action server |

## Running the Launch File

```bash
cd ~/ros2_ws
source install/setup.bash
ros2 launch humanoid_base humanoid_bringup.launch.py
```

All five nodes start together. Press `Ctrl+C` to stop them all.

## How the Launch File Works

```python
def generate_launch_description():
    pkg_dir = get_package_share_directory('humanoid_base')

    # Load URDF via xacro
    urdf_file = os.path.join(pkg_dir, 'urdf', 'humanoid.urdf.xacro')

    # Load parameter file
    params_file = os.path.join(pkg_dir, 'config', 'humanoid_params.yaml')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_file])
        }],
        output='screen',
    )
    # ... more nodes ...
```

Key points:
- `get_package_share_directory` finds the installed package path
- `Command(['xacro ', urdf_file])` processes xacro at launch time
- `parameters=[params_file]` loads a YAML parameter file
- `output='screen'` shows node output in the terminal

## Parameters

Parameters are runtime configuration values. Our parameter file
at `code/ros2/config/humanoid_params.yaml`:

```yaml
joint_command_publisher:
  ros__parameters:
    publish_rate: 10.0        # Hz
    wave_amplitude: 0.5       # radians

joint_state_subscriber:
  ros__parameters:
    log_interval: 1.0         # seconds
```

### Reading Parameters in Code

```python
class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__('joint_command_publisher')

        # Declare with default, then read
        self.declare_parameter('publish_rate', 10.0)
        rate = self.get_parameter('publish_rate').value
```

### Overriding Parameters at Runtime

```bash
# Override via command line
ros2 run humanoid_base joint_command_publisher \
  --ros-args -p publish_rate:=20.0

# Override in launch file
ros2 launch humanoid_base humanoid_bringup.launch.py \
  --ros-args -p joint_command_publisher.publish_rate:=20.0
```

### Querying Parameters

```bash
# List all parameters for a node
ros2 param list /joint_command_publisher

# Get a specific parameter
ros2 param get /joint_command_publisher publish_rate

# Set at runtime (if node allows)
ros2 param set /joint_command_publisher publish_rate 5.0
```

## Launch Arguments

Launch arguments let users customize behavior without editing files:

```python
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim = DeclareLaunchArgument(
        'use_sim', default_value='false',
        description='Launch in simulation mode'
    )
    # Use the argument value
    sim_value = LaunchConfiguration('use_sim')
```

```bash
# Pass argument at launch
ros2 launch humanoid_base humanoid_bringup.launch.py use_sim:=true
```

## What You Learned

- Launch files start multiple nodes with one command
- Parameters configure nodes without code changes
- YAML files organize parameters by node name
- Parameters can be overridden via CLI or queried at runtime
- Launch arguments make launch files flexible

Next, explore the full topic and service reference.
