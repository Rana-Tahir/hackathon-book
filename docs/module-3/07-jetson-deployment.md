---
sidebar_position: 7
title: "Jetson Deployment"
---

# Jetson Deployment

The NVIDIA Jetson Orin is the target edge platform for running
perception and navigation on the robot itself, untethered from
a workstation.

## Jetson Orin Profiles

| Model | GPU Cores | RAM | TDP | Use Case |
|-------|-----------|-----|-----|----------|
| Orin Nano | 1024 | 8 GB | 15W | Basic detection |
| Orin NX | 2048 | 16 GB | 25W | Detection + SLAM |
| AGX Orin | 2048 | 32-64 GB | 60W | Full pipeline |

For the full perception + navigation pipeline, **Orin NX 16GB** is
the minimum recommendation. AGX Orin is preferred.

## JetPack Installation

```bash
# Flash JetPack 6.x via SDK Manager (on host PC)
# Or install from pre-flashed SD card image

# Verify CUDA
nvcc --version
# Expected: CUDA 12.x

# Verify TensorRT
dpkg -l | grep tensorrt
# Expected: TensorRT 8.6+

# Install ROS 2 Humble
sudo apt install ros-humble-desktop
```

## Model Optimization with TensorRT

Convert models for Jetson inference:

```bash
# YOLO → TensorRT (run ON the Jetson)
yolo export model=yolov8s.pt format=engine half=True device=0

# The resulting yolov8s.engine is optimized for THIS specific Jetson
# DO NOT copy engine files between different Jetson models
```

### Performance Expectations

| Model | PyTorch FPS | TensorRT FP16 FPS |
|-------|-------------|-------------------|
| YOLOv8n | 30 | 80+ |
| YOLOv8s | 15 | 45+ |
| Whisper tiny | 0.3x real-time | 1.5x real-time |

## Power Management

Jetson supports multiple power modes:

```bash
# Check current power mode
sudo nvpmodel -q

# Set maximum performance (higher power)
sudo nvpmodel -m 0
sudo jetson_clocks

# Set power-saving mode (lower performance)
sudo nvpmodel -m 1
```

For walking humanoids, use max performance mode during active
operation and power-saving during idle.

## Deployment Architecture

```
Jetson Orin (on-robot)
├── Camera driver → /camera/image
├── YOLO detector → /detections
├── cuVSLAM → /odom, TF
├── Nav2 → /cmd_vel
└── Safety filter → validated actions

Workstation (off-robot, optional)
├── RViz2 (visualization)
├── rqt (monitoring)
└── Development/debugging
```

Connect Jetson to workstation via Ethernet for ROS 2 topic
visibility across machines.

## ROS 2 Multi-Machine Setup

```bash
# On both machines, set the same ROS_DOMAIN_ID
export ROS_DOMAIN_ID=42

# Verify connectivity
# On Jetson:
ros2 topic pub /test std_msgs/String "data: hello"

# On workstation:
ros2 topic echo /test
```

## Thermal Management

Humanoid robots often have limited airflow. Monitor thermals:

```bash
# Check temperature
cat /sys/devices/virtual/thermal/thermal_zone*/temp

# Monitor GPU temperature
tegrastats
```

If temperatures exceed 85°C, reduce power mode or improve cooling.

## What You Built

- Jetson Orin configured for robot deployment
- Models optimized with TensorRT for real-time inference
- Multi-machine ROS 2 setup for remote monitoring
- Power and thermal management for mobile operation
