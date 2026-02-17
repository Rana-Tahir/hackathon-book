---
sidebar_position: 8
title: "Debugging Perception"
---

# Debugging Perception

Perception failures are subtle — the system runs without crashing
but produces wrong results. This chapter provides systematic
approaches to diagnosing issues at each stage.

## Detection Failures

### No Detections

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Camera not publishing | `ros2 topic hz /camera/image` | Check camera driver/bridge |
| Wrong image encoding | `ros2 topic info /camera/image -v` | Match encoding (bgr8, rgb8) |
| Confidence too high | Lower threshold to 0.1 temporarily | Adjust `confidence_threshold` |
| Model not loaded | Check node startup logs | Verify model path exists |
| Wrong input resolution | Check model expected vs actual | Resize input or retrain |

### False Positives

- Lower confidence threshold captures more true positives but also
  more false positives
- Use a higher threshold (0.7+) for safety-critical detections
- Filter by detection size (ignore very small or very large boxes)
- Filter by expected object location (ignore ceiling detections)

### False Negatives

- Object too small in frame (move closer or use higher resolution)
- Object occluded (plan viewpoints for better coverage)
- Object not in training data (fine-tune or retrain with new data)
- Lighting too different from training (domain randomization)

## SLAM Failures

### Tracking Lost

```
[WARN] Visual SLAM tracking lost. Attempting relocalization...
```

Causes:
- **Rapid motion**: Walking causes head oscillation → enable IMU fusion
- **Featureless environment**: Blank walls → add visual texture or use LiDAR
- **Lighting change**: Entering/leaving bright areas → adjust camera exposure

### Drift

SLAM accumulates small errors over time. Detect drift by:

```bash
# Record a loop trajectory (return to start)
# Compare final pose to initial pose
# Drift = distance between them
```

Mitigations:
- Enable loop closure detection
- Add more keyframes (`keyframe_threshold: 0.2`)
- Fuse with IMU data

### Map Quality

Visualize the landmark cloud in RViz2. A good map shows:
- Dense points on surfaces
- Clean edges on walls
- No floating points in free space

A bad map shows:
- Sparse, scattered points
- Duplicate surfaces (drift without loop closure)
- Points behind walls (wrong matches)

## Navigation Failures

### Path Not Found

```bash
# Check the costmap in RViz2
# Common causes:
# - Goal inside inflated obstacle
# - Environment not fully mapped
# - Costmap not clearing old obstacles
```

### Robot Gets Stuck

Check the local costmap for phantom obstacles:

```bash
# Clear the costmap
ros2 service call /local_costmap/clear_entirely_costmap std_srvs/srv/Empty

# If this fixes it, the issue is stale sensor data in the costmap
```

### Recovery Loops

If the robot cycles through recovery behaviors without making progress:

1. Check if the goal is reachable (not inside a wall)
2. Reduce inflation radius if passages are too narrow
3. Increase `movement_time_allowance` if the robot is slow

## Performance Debugging

```bash
# Check node CPU usage
ros2 run rqt_top rqt_top

# Check topic rates
ros2 topic hz /detections
ros2 topic hz /visual_slam/tracking/odometry
ros2 topic hz /cmd_vel

# Check transform latency
ros2 run tf2_ros tf2_monitor
```

### Expected Rates

| Topic | Target Rate |
|-------|-------------|
| `/camera/image` | 30 Hz |
| `/detections` | 10-30 Hz |
| `/visual_slam/tracking/odometry` | 30-60 Hz |
| `/cmd_vel` | 20 Hz |
| `/scan` (LiDAR) | 10 Hz |

If any topic is below target, the bottleneck is usually GPU
(for detection/SLAM) or CPU (for Nav2).

## Diagnostic Tools Summary

| Tool | Purpose |
|------|---------|
| `ros2 topic hz` | Check data flow rates |
| `ros2 topic echo --once` | Inspect message content |
| `rviz2` | Visualize detections, map, costmap, path |
| `rqt_image_view` | View camera feed with overlays |
| `rqt_graph` | See node connectivity |
| `tf2_monitor` | Check transform chain health |
| `tegrastats` | Jetson GPU/CPU/thermal monitoring |

## What You Learned

- Perception debugging requires systematic stage-by-stage diagnosis
- Detection failures are usually threshold or data issues
- SLAM failures are usually motion or environment issues
- Navigation failures are usually costmap configuration issues
- Always check data flow rates first — missing data is the most common root cause
