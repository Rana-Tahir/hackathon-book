---
sidebar_position: 7
title: "Debugging Simulation"
---

# Debugging Simulation

When simulation goes wrong, the failure can manifest in confusing ways.
Follow this systematic approach to find and fix problems.

## General Debugging Strategy

1. **Check terminal output.** Launch with `output='screen'`
2. **Check the ROS 2 graph.** `ros2 node list`, `ros2 topic list`
3. **Check Gazebo state.** `ign model --list`, `ign topic -l`
4. **Isolate the layer.** Is the problem in Gazebo, the bridge, or ROS 2?

## Gazebo Crash on Launch

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Invalid SDF | `ign sdf -k file.sdf` | Fix XML errors |
| GPU driver issue | `glxinfo \| grep OpenGL` | Update drivers or use `LIBGL_ALWAYS_SOFTWARE=1` |
| Missing meshes | Check `IGN_GAZEBO_RESOURCE_PATH` | Set path or use absolute URIs |
| Out of memory | Check system memory | Simplify meshes, reduce models |

## Robot Doesn't Appear

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| URDF not published | `ros2 topic echo /robot_description --once` | Start robot_state_publisher |
| Xacro error | `xacro file.xacro > /tmp/test.urdf` | Fix xacro syntax |
| Zero inertia | Check `<inertial>` blocks | Add mass and inertia to all links |
| Bad spawn height | Robot embedded in ground | Spawn at `-z 1.0` |

## Sensors Not Publishing

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Plugin not loaded | `ls /usr/lib/*/ign-gazebo-6/plugins/` | Add world-level plugin |
| Sensor not on link | Check SDF structure | Move sensor inside `<link>` |
| No render engine | Check GPU availability | Add `<render_engine>ogre2</render_engine>` |
| Update rate = 0 | Check SDF | Set positive `<update_rate>` |

## Bridge Not Working

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Topic name mismatch | `ign topic -l` vs bridge args | Use exact Ignition topic name |
| Message type mismatch | Check type mappings table | Fix type string (e.g., `IMU` not `Imu`) |
| Bridge started too early | Bridge log shows no connection | Add launch delay |

## Robot Explodes or Vibrates

| Cause | Fix |
|-------|-----|
| Near-zero inertia | Use realistic values: `m * L^2 / 12` |
| Overlapping collisions | Spawn above ground; check default pose |
| Step size too large | Reduce `max_step_size` to 0.0005 |
| PID gains too high | Start low, increase P, add D, minimal I |

## Diagnostic Commands

| Command | Purpose |
|---------|---------|
| `ign gazebo --version` | Check Gazebo version |
| `ign sdf -k file.sdf` | Validate SDF |
| `ign topic -l` | List Ignition topics |
| `ign topic -e -t /topic` | Echo Ignition topic |
| `ign model --list` | List models |
| `ros2 topic hz /topic` | Check publish rate |
| `ros2 topic echo /topic --once` | View one message |
| `IGN_VERBOSE=4 ign gazebo` | Verbose debug output |

## When All Else Fails

1. Reproduce with a minimal example
2. Verify version compatibility (`dpkg -l | grep ignition`)
3. Kill stale processes: `pkill -f "ign gazebo"; pkill -f ros2`
4. Start fresh with verbose logging
