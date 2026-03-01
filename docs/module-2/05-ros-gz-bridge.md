---
sidebar_position: 5
title: "ros_gz Bridge"
---

# ros_gz Bridge

Gazebo (Ignition) uses its own transport layer, separate from ROS 2.
The `ros_gz_bridge` converts messages between the two systems so your
ROS 2 nodes can read Gazebo sensors and send Gazebo commands.

## How the Bridge Works

```
Gazebo Sensor ──► Ignition Transport ──► ros_gz_bridge ──► ROS 2 Topic
ROS 2 Command ──► ros_gz_bridge ──► Ignition Transport ──► Gazebo Actuator
```

The bridge maps:
- **Ignition message types** ↔ **ROS 2 message types**
- **Ignition topic names** ↔ **ROS 2 topic names**

## Message Type Mappings

| Data | Ignition Type | ROS 2 Type |
|------|--------------|------------|
| IMU | `ignition.msgs.IMU` | `sensor_msgs/msg/Imu` |
| LaserScan | `ignition.msgs.LaserScan` | `sensor_msgs/msg/LaserScan` |
| Image | `ignition.msgs.Image` | `sensor_msgs/msg/Image` |
| PointCloud | `ignition.msgs.PointCloudPacked` | `sensor_msgs/msg/PointCloud2` |
| Clock | `ignition.msgs.Clock` | `rosgraph_msgs/msg/Clock` |
| Twist | `ignition.msgs.Twist` | `geometry_msgs/msg/Twist` |
| JointState | `ignition.msgs.Model` | `sensor_msgs/msg/JointState` |

## Bridge Configuration

### Command-Line Bridge

```bash
# Bridge a single topic
ros2 run ros_gz_bridge parameter_bridge \
  /imu@sensor_msgs/msg/Imu[ignition.msgs.IMU

# Bridge multiple topics
ros2 run ros_gz_bridge parameter_bridge \
  /imu@sensor_msgs/msg/Imu[ignition.msgs.IMU \
  /lidar@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan \
  /camera/image@sensor_msgs/msg/Image[ignition.msgs.Image \
  /clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock
```

The syntax is:
```
/topic_name@ros2_type[ignition_type    # Ignition → ROS 2 (subscribe from Gazebo)
/topic_name@ros2_type]ignition_type    # ROS 2 → Ignition (publish to Gazebo)
/topic_name@ros2_type@ignition_type    # Bidirectional
```

### Launch File Bridge

```python
from launch_ros.actions import Node

bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=[
        '/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU',
        '/lidar/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
        '/camera/image@sensor_msgs/msg/Image[ignition.msgs.Image',
        '/camera/depth@sensor_msgs/msg/Image[ignition.msgs.Image',
        '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
        '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
    ],
    parameters=[{'use_sim_time': True}],
    output='screen',
)
```

## Topic Name Mapping

Gazebo sensor topics have long auto-generated names:

```
/world/humanoid_world/model/humanoid/link/head_link/sensor/lidar/scan
```

The bridge can remap these to shorter ROS 2 names:

```bash
ros2 run ros_gz_bridge parameter_bridge \
  /world/humanoid_world/model/humanoid/link/head_link/sensor/lidar/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan \
  --ros-args -r /world/humanoid_world/model/humanoid/link/head_link/sensor/lidar/scan:=/lidar/scan
```

## Clock Synchronization

When using simulation time, all ROS 2 nodes must use the Gazebo clock:

1. Bridge the `/clock` topic
2. Set `use_sim_time: true` on every ROS 2 node
3. Launch with `--ros-args -p use_sim_time:=true`

```bash
# Verify clock is being published
ros2 topic hz /clock
# Should show ~1000 Hz (one message per physics step)
```

## Verifying the Bridge

```bash
# Check that bridged topics appear in ROS 2
ros2 topic list

# Verify data is flowing
ros2 topic hz /imu         # Should match sensor update_rate
ros2 topic hz /lidar/scan  # Should match sensor update_rate
ros2 topic hz /camera/image

# Echo a message
ros2 topic echo /imu --once
```

## Complete Simulation Launch

Combining world, robot, and bridge into one launch file:

```python
def generate_launch_description():
    return LaunchDescription([
        # 1. Start Gazebo
        ExecuteProcess(cmd=['ign', 'gazebo', world_file]),

        # 2. Robot state publisher
        Node(package='robot_state_publisher', ...),

        # 3. Spawn robot
        Node(package='ros_gz_sim', executable='create', ...),

        # 4. Bridge sensors to ROS 2
        Node(package='ros_gz_bridge', executable='parameter_bridge',
             arguments=[...]),

        # 5. Your ROS 2 nodes
        Node(package='humanoid_base', executable='joint_state_subscriber', ...),
    ])
```

## Common Bridge Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Topic exists but 0 Hz | Wrong message type mapping | Check exact Ignition type |
| Bridge crashes | Incompatible ros_gz version | `apt install ros-humble-ros-gz` |
| High latency | Too many image topics | Reduce camera resolution or rate |
| Missing topic | Bridge started before Gazebo | Add launch delay |

## What You Built

- ros_gz bridge connecting Gazebo sensors to ROS 2
- Topic remapping for clean namespaces
- Clock synchronization for simulation time
- Complete launch file integrating all components

Next: understand the limitations of simulation.
