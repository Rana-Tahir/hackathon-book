---
sidebar_position: 2
title: "Isaac Sim Setup"
---

# Isaac Sim Setup

NVIDIA Isaac Sim provides photorealistic simulation with physically
accurate sensors, perfect for training perception models and
generating synthetic data.

## Why Isaac Sim?

| Feature | Gazebo Fortress | Isaac Sim |
|---------|----------------|-----------|
| Physics | DART (adequate) | PhysX 5 (superior) |
| Rendering | Ogre2 (functional) | RTX ray tracing (photorealistic) |
| Sensor simulation | Basic noise models | Physically-based sensor models |
| Synthetic data | Manual | Built-in Replicator |
| Domain randomization | Custom scripts | Built-in tools |
| GPU acceleration | Optional | Required and native |

We use both: Gazebo for fast iteration, Isaac Sim for perception
training and validation.

## Installation

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | RTX 2070 (8 GB) | RTX 3080+ (10+ GB) |
| RAM | 32 GB | 64 GB |
| Storage | 50 GB SSD | 100 GB NVMe |
| OS | Ubuntu 22.04 | Ubuntu 22.04 |
| Driver | NVIDIA 525+ | Latest stable |

### Install Steps

```bash
# 1. Install NVIDIA Omniverse Launcher
# Download from https://www.nvidia.com/en-us/omniverse/

# 2. Install Isaac Sim via Omniverse Launcher
# Open Launcher → Exchange → Isaac Sim → Install

# 3. Verify installation
cd ~/.local/share/ov/pkg/isaac-sim-*/
./isaac-sim.sh --help

# 4. Install Isaac ROS packages
sudo apt install ros-humble-isaac-ros-common
```

## ROS 2 Bridge

Isaac Sim connects to ROS 2 natively through the OmniGraph system:

1. Open Isaac Sim
2. Load or create a scene
3. Add OmniGraph nodes for ROS 2 publishing
4. Topics appear in ROS 2 automatically

```bash
# Verify Isaac Sim topics are visible
ros2 topic list
# Should show /camera/rgb, /camera/depth, /imu, etc.
```

## Loading the Humanoid

Import the URDF into Isaac Sim:

1. **File → Import → URDF**
2. Select `code/ros2/urdf/humanoid.urdf.xacro` (process xacro first)
3. Configure joint drive types (position or velocity)
4. Place the robot in the scene

```bash
# Pre-process xacro to URDF
xacro code/ros2/urdf/humanoid.urdf.xacro > /tmp/humanoid.urdf

# Or use the Isaac Sim Python API
from omni.isaac.core.utils.urdf import import_urdf
import_urdf("/tmp/humanoid.urdf")
```

## Warehouse Scene

Isaac Sim includes pre-built environments. The warehouse scene provides
realistic indoor testing:

```python
from omni.isaac.core import World
from omni.isaac.nucleus import get_assets_root_path

world = World()
assets_root = get_assets_root_path()
warehouse_usd = assets_root + "/Isaac/Environments/Simple_Warehouse/warehouse.usd"
world.scene.add_default_ground_plane()
```

## Synthetic Data Generation

Isaac Sim's Replicator generates labeled training data:

- RGB images with bounding box labels
- Depth images
- Semantic segmentation masks
- Instance segmentation
- 3D bounding boxes

This data trains perception models (YOLO, etc.) without manual labeling.

## What You Built

- Isaac Sim installed and configured for ROS 2
- Humanoid robot imported from URDF
- Warehouse scene loaded for testing
- Understanding of synthetic data generation capabilities

Next: train and deploy object detection.
