---
sidebar_position: 4
title: "Sensor Plugins"
---

# Sensor Plugins

A humanoid robot perceives the world through sensors. In Gazebo,
sensors are implemented as plugins attached to links in the robot model.

## Sensor Overview

| Sensor | Purpose | Gazebo Plugin |
|--------|---------|---------------|
| **IMU** | Orientation, angular velocity, acceleration | `ignition-gazebo-imu-system` |
| **LiDAR** | 2D/3D distance scanning | `ignition-gazebo-sensors-system` (gpu_lidar) |
| **Camera** | RGB images | `ignition-gazebo-sensors-system` (camera) |
| **Depth Camera** | RGB + depth images | `ignition-gazebo-sensors-system` (depth_camera) |
| **Contact** | Collision detection | `ignition-gazebo-contact-system` |

## IMU Sensor

The IMU (Inertial Measurement Unit) provides orientation and
acceleration data, essential for balance control.

Add to the torso link in your SDF:

```xml
<sensor name="imu_sensor" type="imu">
  <always_on>true</always_on>
  <update_rate>200</update_rate>
  <imu>
    <angular_velocity>
      <x><noise type="gaussian"><mean>0.0</mean><stddev>0.001</stddev></noise></x>
      <y><noise type="gaussian"><mean>0.0</mean><stddev>0.001</stddev></noise></y>
      <z><noise type="gaussian"><mean>0.0</mean><stddev>0.001</stddev></noise></z>
    </angular_velocity>
    <linear_acceleration>
      <x><noise type="gaussian"><mean>0.0</mean><stddev>0.01</stddev></noise></x>
      <y><noise type="gaussian"><mean>0.0</mean><stddev>0.01</stddev></noise></y>
      <z><noise type="gaussian"><mean>0.0</mean><stddev>0.01</stddev></noise></z>
    </linear_acceleration>
  </imu>
</sensor>
```

Key parameters:
- **update_rate**: 200 Hz is typical for IMUs
- **noise**: Gaussian noise approximates real IMU behavior
- **always_on**: Sensor publishes even when the GUI is not focused

## LiDAR Sensor

LiDAR provides distance measurements for mapping and obstacle detection.
Attach to the head link for a good vantage point:

```xml
<sensor name="lidar" type="gpu_lidar">
  <always_on>true</always_on>
  <update_rate>10</update_rate>
  <lidar>
    <scan>
      <horizontal>
        <samples>360</samples>
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>
      <resolution>0.01</resolution>
    </range>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.01</stddev>
    </noise>
  </lidar>
</sensor>
```

Parameters:
- **samples**: 360 = one measurement per degree
- **range**: 0.1 to 10.0 meters
- **gpu_lidar**: Uses GPU for ray casting (faster than CPU lidar)

## Camera Sensor

RGB camera for object detection and visual SLAM:

```xml
<sensor name="camera" type="camera">
  <always_on>true</always_on>
  <update_rate>30</update_rate>
  <camera>
    <horizontal_fov>1.3962634</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>100</far>
    </clip>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev>
    </noise>
  </camera>
</sensor>
```

## Depth Camera

Combines RGB with per-pixel depth:

```xml
<sensor name="depth_camera" type="depth_camera">
  <always_on>true</always_on>
  <update_rate>15</update_rate>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>320</width>
      <height>240</height>
    </image>
    <clip>
      <near>0.1</near>
      <far>10</far>
    </clip>
  </camera>
</sensor>
```

## World-Level Plugin Requirements

Sensors require system plugins loaded at the world level:

```xml
<world name="humanoid_world">
  <!-- Required for camera, LiDAR, depth sensors -->
  <plugin
    filename="ignition-gazebo-sensors-system"
    name="ignition::gazebo::systems::Sensors">
    <render_engine>ogre2</render_engine>
  </plugin>

  <!-- Required for IMU -->
  <plugin
    filename="ignition-gazebo-imu-system"
    name="ignition::gazebo::systems::Imu">
  </plugin>

  <!-- Required for contact sensors -->
  <plugin
    filename="ignition-gazebo-contact-system"
    name="ignition::gazebo::systems::Contact">
  </plugin>

  <!-- Required for joint state publishing -->
  <plugin
    filename="ignition-gazebo-joint-state-publisher-system"
    name="ignition::gazebo::systems::JointStatePublisher">
  </plugin>
</world>
```

## Verifying Sensor Output

```bash
# List all Ignition topics
ign topic -l

# Echo IMU data
ign topic -e -t /world/humanoid_world/model/humanoid/link/base_link/sensor/imu_sensor/imu

# Echo LiDAR data
ign topic -e -t /world/humanoid_world/model/humanoid/link/head_link/sensor/lidar/scan

# Echo camera images (check topic exists)
ign topic -l | grep camera
```

## Sensor Placement Summary

| Sensor | Link | Rationale |
|--------|------|-----------|
| IMU | `base_link` (torso) | Measures body orientation for balance |
| LiDAR | `head_link` | Elevated position, 360° view |
| Camera | `head_link` | Forward-facing, human-like perspective |
| Depth camera | `head_link` | Co-located with RGB for fusion |
| Contact | Feet links | Detect ground contact for gait |

## What You Built

- Four sensor types configured with realistic noise models
- World-level plugins enabling sensor simulation
- Sensor placement matching real humanoid robot designs
- Verification commands for each sensor type

Next: bridge these sensor topics to ROS 2.
