---
sidebar_position: 7
title: Debugging ROS 2
---

# Debugging ROS 2

When things go wrong — and they will — these tools and techniques
help you find the problem fast.

## The Debugging Checklist

When a node doesn't work, check these in order:

1. **Is the workspace sourced?** → `echo $AMENT_PREFIX_PATH`
2. **Is the node running?** → `ros2 node list`
3. **Is the topic being published?** → `ros2 topic list` then `ros2 topic echo`
4. **Is the message type correct?** → `ros2 topic info /topic_name -v`
5. **Are parameters loaded?** → `ros2 param list /node_name`
6. **Are transforms valid?** → `ros2 run tf2_tools view_frames`

## Common Problems and Fixes

### "Package not found"

```
Package 'humanoid_base' not found
```

**Fix:** Rebuild and re-source:
```bash
cd ~/ros2_ws
colcon build --packages-select humanoid_base
source install/setup.bash
```

**Why:** ROS 2 caches package paths at source time. After building,
you must re-source for the shell to find new packages.

### "No publishers on topic"

```bash
$ ros2 topic echo /joint_commands
WARNING: topic not published yet
```

**Fix:** Check if the publisher node is running:
```bash
ros2 node list
# If missing, launch it:
ros2 launch humanoid_base humanoid_bringup.launch.py
```

### "Service not available"

```bash
$ ros2 service call /go_home std_srvs/srv/SetBool "{data: true}"
Waiting for service...
```

**Fix:** The service server node isn't running. Start it:
```bash
ros2 run humanoid_base joint_service
```

### "Transform not found"

```
Could not find a connection between 'base_link' and 'left_foot'
```

**Fix:** Check the TF tree:
```bash
# Visualize the full transform tree
ros2 run tf2_tools view_frames
# Creates frames.pdf showing the tree

# Check a specific transform
ros2 run tf2_ros tf2_echo base_link left_foot
```

### Wrong message type

If a subscriber connects but receives no data, the message types
might not match:

```bash
# Check what type is being published
ros2 topic info /joint_commands -v
# Should show: Type: sensor_msgs/msg/JointState
```

### Node crashes on startup

Check the console output for Python tracebacks. Common causes:

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Missing dependency | `pip install <package>` or add to `package.xml` |
| `ParameterNotDeclaredException` | Parameter not declared | Add `self.declare_parameter(...)` |
| `InvalidTopicNameException` | Bad topic name | Remove special characters, use `/valid_name` |

## Logging

### Setting Log Levels

```bash
# Set log level for a running node
ros2 service call /joint_command_publisher/set_logger_level \
  rcl_interfaces/srv/SetLoggerLevel \
  "{logger_name: 'joint_command_publisher', level: 10}"
```

Log levels: DEBUG=10, INFO=20, WARN=30, ERROR=40, FATAL=50.

### Using Logging in Code

```python
self.get_logger().debug('Detailed info for debugging')
self.get_logger().info('Normal operation info')
self.get_logger().warn('Something unexpected')
self.get_logger().error('Something failed')
self.get_logger().fatal('Cannot continue')
```

### Viewing Logs

```bash
# View all ROS 2 logs
ros2 topic echo /rosout

# Filter by node
ros2 topic echo /rosout --filter "msg.name == '/joint_command_publisher'"
```

## RViz Debugging

RViz is your visual debugger for transforms, robot models, and sensor data.

```bash
rviz2
```

Useful displays for Module 1:

| Display | What It Shows |
|---------|---------------|
| **RobotModel** | 3D humanoid from URDF |
| **TF** | Coordinate frame axes on every link |
| **Axes** | Single coordinate frame orientation |

**Common RViz issues:**

- **White robot / no model**: Fixed Frame must be `base_link`
- **No TF data**: `robot_state_publisher` not running or no joint states
- **Flickering model**: TF timestamps out of sync — check `use_sim_time`

## rqt Tools

```bash
# Node graph visualization
rqt_graph

# Plot numeric values over time
rqt_plot /joint_commands/position[0]

# Interactive service caller
rqt_service_caller

# Parameter reconfigure GUI
rqt_reconfigure
```

## Build Debugging

```bash
# Build with verbose output
colcon build --packages-select humanoid_base --event-handlers console_direct+

# Clean and rebuild
rm -rf build/humanoid_base install/humanoid_base
colcon build --packages-select humanoid_base

# Check package dependencies
rosdep check --from-paths src/humanoid_base
```

## Performance Monitoring

```bash
# Check topic publishing rate
ros2 topic hz /joint_commands
# Expected: ~10 Hz

# Check message bandwidth
ros2 topic bw /joint_commands

# Check message latency
ros2 topic delay /joint_commands
```

## Summary

| Tool | Use For |
|------|---------|
| `ros2 node list` | Check running nodes |
| `ros2 topic echo` | See live messages |
| `ros2 topic hz` | Verify publish rates |
| `ros2 service call` | Test services manually |
| `ros2 param list` | Check loaded parameters |
| `ros2 run tf2_tools view_frames` | Visualize TF tree |
| `rqt_graph` | See node connections |
| `rviz2` | Visual debugging |

These tools carry forward to every module. Master them now — you will
use them constantly.
