---
sidebar_position: 1
title: "Introduction: The Robotic Nervous System"
---

# Module 1: The Robotic Nervous System

**Focus**: ROS 2 middleware for humanoid robot control

## What You Will Build

In this module, you will construct a complete robotic nervous system
using ROS 2 (Robot Operating System 2). By the end, your humanoid
robot will have:

- A brain (nodes that process information)
- Nerves (topics that carry messages)
- Reflexes (services for quick request-response)
- Coordinated movements (actions for long-running tasks)
- A body (URDF model defining its physical structure)

## Why ROS 2?

ROS 2 is the standard middleware for modern robotics. It provides:

- **Distributed communication**: Nodes can run on different machines
  and communicate seamlessly over DDS (Data Distribution Service).
- **Real-time capable**: ROS 2 supports real-time operating system
  integration, critical for safe robot control.
- **Language support**: Write nodes in Python (rclpy) or C++ (rclcpp).
- **Ecosystem**: Thousands of packages for perception, navigation,
  manipulation, and more.

This book uses **ROS 2 Humble Hawksbill**, the current LTS release
targeting Ubuntu 22.04 and Python 3.10.

## ROS 2 Architecture

ROS 2 uses a **publish-subscribe** model built on DDS:

```text
┌──────────┐    /joint_commands     ┌──────────┐
│ Planner  │ ──────────────────────>│ Controller│
│  Node    │      (Topic)           │   Node   │
└──────────┘                        └──────────┘
      │                                   │
      │  /plan_request                    │  /joint_states
      │  (Service)                        │  (Topic)
      ▼                                   ▼
┌──────────┐                        ┌──────────┐
│  Task    │                        │  State   │
│ Manager  │                        │ Monitor  │
└──────────┘                        └──────────┘
```

**Key Concepts**:

| Concept | Purpose | Analogy |
|---------|---------|---------|
| Node | A single process that performs computation | A neuron |
| Topic | A named bus for streaming messages | A nerve fiber |
| Service | Synchronous request-response | A reflex arc |
| Action | Asynchronous long-running task with feedback | A coordinated movement |
| Parameter | Runtime configuration value | A sensitivity setting |

## Module Structure

| Chapter | Topic | Artifact |
|---------|-------|----------|
| 2 | Nodes, Topics, and Messages | Publisher + subscriber nodes |
| 3 | Services and Actions | Service server + action server/client |
| 4 | Humanoid URDF | URDF model validated in RViz |
| 5 | Launch Files and Parameters | Multi-node launch configuration |
| 6 | Topic Reference | Complete topic/message flow table |
| 7 | Debugging | Failure modes and resolution |

## Prerequisites

Before starting this module:

- [ ] Ubuntu 22.04 installed
- [ ] ROS 2 Humble installed (`source /opt/ros/humble/setup.bash`)
- [ ] `colcon` build tools installed
- [ ] Python 3.10 available
- [ ] A terminal with `ros2` commands working

Verify your installation:

```bash
source /opt/ros/humble/setup.bash
ros2 --version
# Expected: ros2 0.x.x (Humble)
```

## Learning Outcome

After completing this module, you will be able to construct and control
a humanoid robot's nervous system using ROS 2 — building nodes,
wiring topics, defining services and actions, modeling the robot's
body in URDF, and launching the complete system from a single command.
