---
sidebar_position: 4
title: "Visual SLAM"
---

# Visual SLAM

Visual SLAM (Simultaneous Localization and Mapping) answers two
questions at once: "Where am I?" and "What does the world look like?"
— using only camera images.

## How Visual SLAM Works

1. **Feature extraction**: Detect distinctive points in each camera frame
2. **Feature matching**: Track features across consecutive frames
3. **Pose estimation**: Compute camera motion from matched features
4. **Map building**: Triangulate 3D positions of tracked features
5. **Loop closure**: Recognize previously visited places to correct drift

## cuVSLAM (GPU-Accelerated)

NVIDIA's cuVSLAM runs the entire pipeline on GPU via `isaac_ros_visual_slam`:

```bash
# Install Isaac ROS Visual SLAM
sudo apt install ros-humble-isaac-ros-visual-slam
```

### Configuration

```yaml
# config/vslam_params.yaml
visual_slam_node:
  ros__parameters:
    enable_imu_fusion: true
    gyro_noise_density: 0.000244
    gyro_random_walk: 0.000019393
    accel_noise_density: 0.001862
    accel_random_walk: 0.003
    image_jitter_threshold_ms: 35.0
    imu_jitter_threshold_ms: 10.0
```

### Launch

```bash
ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam.launch.py
```

### Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/camera/left/image_raw` | `sensor_msgs/Image` | Input |
| `/camera/right/image_raw` | `sensor_msgs/Image` | Input |
| `/imu` | `sensor_msgs/Imu` | Input (optional) |
| `/visual_slam/tracking/odometry` | `nav_msgs/Odometry` | Output |
| `/visual_slam/vis/landmarks_cloud` | `sensor_msgs/PointCloud2` | Output |
| TF: `odom → base_link` | | Output |

## Validating SLAM Accuracy

Compare VSLAM output against Isaac Sim ground truth using
Absolute Trajectory Error (ATE):

```python
import numpy as np

def compute_ate(estimated, ground_truth):
    """Compute ATE RMSE between estimated and ground truth poses.

    Args:
        estimated: Nx3 array of [x, y, z] positions
        ground_truth: Nx3 array of [x, y, z] positions

    Returns:
        ATE RMSE in meters
    """
    errors = np.linalg.norm(estimated - ground_truth, axis=1)
    return np.sqrt(np.mean(errors ** 2))
```

### Target Accuracy

| Environment | ATE RMSE Target |
|-------------|----------------|
| Small room (5x5 m) | < 0.05 m |
| Office (20x20 m) | < 0.15 m |
| Warehouse (50x50 m) | < 0.30 m |

## IMU Fusion

For walking humanoids, IMU fusion is nearly essential. The oscillating
viewpoint during locomotion causes rapid feature motion that pure
visual tracking struggles with. The IMU provides 200 Hz rotation
estimates that bridge gaps between camera frames.

## Integration with Nav2

VSLAM outputs feed directly into Nav2:

```
VSLAM → /odom (Odometry) → Nav2 Controller
VSLAM → TF (odom→base_link) → Nav2 Costmap
Depth Camera → /depth → Nav2 Obstacle Layer
```

## What You Built

- GPU-accelerated Visual SLAM providing real-time localization
- 3D landmark map of the environment
- Accuracy validation against simulation ground truth
- Odometry output feeding into the navigation stack

Next: configure Nav2 for autonomous navigation.
