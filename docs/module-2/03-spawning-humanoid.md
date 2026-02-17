---
sidebar_position: 3
title: "Spawning the Humanoid"
---

# Spawning the Humanoid

With the world running, the next step is placing your humanoid robot
inside it. This involves converting the URDF to SDF and spawning the
model into the running Gazebo instance.

## URDF to SDF Conversion

Gazebo uses SDF internally. When you spawn a URDF model, it is
automatically converted. However, some URDF features do not map
cleanly to SDF:

| URDF Feature | SDF Support |
|-------------|-------------|
| Links and joints | Full support |
| Visual/collision geometry | Full support |
| Inertial properties | Full support |
| Mimic joints | Not supported |
| Transmissions | Ignored (use Gazebo plugins) |

## Spawning via ros_gz

The `ros_gz_sim` package provides a spawn service:

```bash
# Terminal 1: Start Gazebo with the world
ign gazebo code/gazebo/worlds/humanoid_world.sdf

# Terminal 2: Publish robot description
ros2 run robot_state_publisher robot_state_publisher \
  --ros-args -p robot_description:="$(xacro code/ros2/urdf/humanoid.urdf.xacro)"

# Terminal 3: Spawn the robot
ros2 run ros_gz_sim create \
  -name humanoid \
  -topic robot_description \
  -z 1.0
```

The `-z 1.0` spawns the robot 1 meter above the ground so it can
settle under gravity without starting embedded in the floor.

## Gazebo Plugins for Joint Control

To control joints in Gazebo, attach the `JointPositionController` plugin
to each joint. Add this to your SDF model or use the Gazebo plugin
system:

```xml
<!-- In the model SDF or via spawn -->
<plugin
  filename="ignition-gazebo-joint-position-controller-system"
  name="ignition::gazebo::systems::JointPositionController">
  <joint_name>left_shoulder_pitch</joint_name>
  <p_gain>100</p_gain>
  <d_gain>10</d_gain>
</plugin>
```

For all 16 joints, you need 16 controller plugins. A launch file
automates this.

## Verifying the Spawn

After spawning, verify the robot is correctly loaded:

```bash
# List models in Gazebo
ign model --list
# Should show: humanoid

# Check joint states are being published
ros2 topic echo /joint_states

# View in RViz alongside Gazebo
rviz2
```

## Common Spawn Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Robot flies away | Inertia values too small | Check `<inertial>` in URDF |
| Robot sinks through floor | No collision geometry | Add `<collision>` to all links |
| Robot invisible in Gazebo | Missing visual mesh | Check `<visual>` geometry paths |
| Joints don't move | No controller plugin | Add JointPositionController |
| Robot spawns sideways | Wrong origin orientation | Check `<origin rpy>` in URDF |

## Launch File for Simulation

Create a combined launch file that starts everything:

```python
# launch/simulation.launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command
import os

def generate_launch_description():
    urdf_file = 'code/ros2/urdf/humanoid.urdf.xacro'

    return LaunchDescription([
        # Start Gazebo
        ExecuteProcess(
            cmd=['ign', 'gazebo', 'code/gazebo/worlds/humanoid_world.sdf'],
            output='screen',
        ),

        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_file]),
                'use_sim_time': True,
            }],
        ),

        # Spawn robot (with delay)
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'humanoid',
                '-topic', 'robot_description',
                '-z', '1.0',
            ],
            output='screen',
        ),
    ])
```

## What You Built

- Humanoid robot spawned in Gazebo with full physics
- Joint controllers attached for position control
- Combined launch file for one-command startup
- Verification workflow for common spawn issues

Next: add sensors to the robot.
