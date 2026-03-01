# Module Interface Contracts

**Phase**: 1 — Design & Contracts
**Date**: 2026-02-13
**Feature**: 001-physical-ai-book

## Purpose

Defines the explicit interface contracts between modules. Each module
produces outputs that downstream modules consume. These contracts MUST
be satisfied before a downstream module begins authoring.

## Contract: Module 1 → Module 2

**Producer**: Module 1 (The Robotic Nervous System)
**Consumer**: Module 2 (The Digital Twin)

| Output | Format | Location | Validation |
|--------|--------|----------|-----------|
| Humanoid URDF | `.urdf` or `.xacro` file | `code/ros2/urdf/` | `check_urdf` passes without errors |
| ROS 2 workspace | `colcon` workspace | `code/ros2/` | `colcon build` succeeds |
| Joint command topics | ROS 2 topic definitions | Documented in Module 1 | `ros2 topic list` shows expected topics |

**Contract Rule**: Module 2 MUST NOT begin until the URDF loads
successfully in Gazebo Fortress via the `ros_gz` bridge.

## Contract: Module 2 → Module 3

**Producer**: Module 2 (The Digital Twin)
**Consumer**: Module 3 (The AI-Robot Brain)

| Output | Format | Location | Validation |
|--------|--------|----------|-----------|
| Gazebo simulation world | `.sdf` world file | `code/simulation/gazebo/` | `gz sim` launches without crash |
| LiDAR data stream | ROS 2 `sensor_msgs/LaserScan` | Published topic | `ros2 topic echo` shows data |
| Depth camera stream | ROS 2 `sensor_msgs/Image` | Published topic | `ros2 topic echo` shows data |
| IMU data stream | ROS 2 `sensor_msgs/Imu` | Published topic | `ros2 topic echo` shows data |

**Contract Rule**: Module 3 MUST NOT begin until all three sensor
streams publish valid data in the Gazebo simulation.

## Contract: Module 3 → Module 4

**Producer**: Module 3 (The AI-Robot Brain)
**Consumer**: Module 4 (Vision-Language-Action)

| Output | Format | Location | Validation |
|--------|--------|----------|-----------|
| VSLAM localization | ROS 2 `geometry_msgs/PoseStamped` | Published topic | Robot pose updates in real-time |
| Nav2 navigation stack | ROS 2 action server | `code/navigation/` | `NavigateToPose` action completes |
| Object detection results | ROS 2 `vision_msgs/Detection2DArray` | Published topic | Detections appear for known objects |

**Contract Rule**: Module 4 MUST NOT begin until Nav2 can navigate
to a goal point and VSLAM provides localization in the simulated
environment.

## Contract: All Modules → Capstone

**Producer**: Modules 1–4
**Consumer**: Capstone (The Autonomous Humanoid)

| Output | Source Module | Validation |
|--------|-------------|-----------|
| ROS 2 workspace + URDF | 1 | Workspace builds; URDF loads |
| Gazebo world + sensors | 2 | Simulation runs; sensors publish |
| VSLAM + Nav2 | 3 | Robot localizes and navigates |
| Voice → LLM → Actions | 4 | Voice command produces action sequence |
| Safety filter | 4 | Unsafe commands are rejected |

**Contract Rule**: Capstone integration begins only after all four
module outputs are validated independently.

## Safety Contract (Cross-Cutting)

Applies to all modules and the capstone per Constitution Principle V.

| Requirement | Enforcement Point |
|-------------|------------------|
| Motor commands pass safety filter | Between LLM output and ROS 2 action server |
| RL outputs clamped to safe envelope | Within control nodes (Module 1) |
| Language commands validated | Before translation to ROS 2 actions (Module 4) |
| Emergency stop functional | ROS 2 service available at all times |
| Unsafe commands logged and rejected | Safety filter in `code/vla/safety/` |
