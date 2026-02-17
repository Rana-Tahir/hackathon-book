---
sidebar_position: 1
title: "Introduction to Simulation"
---

# Introduction to Simulation

Before a humanoid robot takes its first step in the real world, it must
take thousands of steps in simulation. Simulation is not optional — it is
the primary development environment for physical AI.

## Why Simulate?

| Reason | Explanation |
|--------|-------------|
| **Safety** | A falling simulated robot breaks nothing |
| **Speed** | Run 10x faster than real time |
| **Cost** | No hardware wear, no replacement parts |
| **Reproducibility** | Same test, same conditions, every time |
| **Scale** | Run 100 instances in parallel for training |

## Simulation vs. Reality

Simulation approximates reality. It does not replicate it perfectly.
Understanding this gap — the **sim-to-real gap** — is essential:

- **Physics**: Simulated contact and friction are simplified
- **Sensors**: Simulated noise is Gaussian; real noise is complex
- **Actuators**: Simulated motors respond instantly; real ones have delay
- **Environment**: Simulated worlds are clean; reality is messy

Module 2 teaches you to build effective simulations while respecting
their limitations.

## Our Simulation Stack

| Tool | Role | Version |
|------|------|---------|
| **Gazebo Fortress** | Physics simulation, sensor simulation | LTS (Fortress) |
| **ros_gz** | Bridge between Gazebo and ROS 2 | Compatible with Humble |
| **RViz2** | Visualization and debugging | Ships with ROS 2 Humble |

## Module 2 Roadmap

| Chapter | Topic |
|---------|-------|
| 2 | Gazebo world building |
| 3 | Spawning the humanoid in Gazebo |
| 4 | Sensor plugins (IMU, LiDAR, camera) |
| 5 | ros_gz bridge configuration |
| 6 | Simulation limitations and the sim-to-real gap |
| 7 | Debugging simulation |

## Prerequisites

- Module 1 complete (URDF, ROS 2 nodes working)
- Gazebo Fortress installed (`sudo apt install ros-humble-ros-gz`)
- GPU recommended for sensor rendering (not required)

## What You Will Build

By the end of Module 2, you will have:
- A Gazebo world with ground plane, walls, and obstacles
- Your 16-DOF humanoid spawned and controllable
- IMU, LiDAR, and camera sensors publishing to ROS 2
- A bridge configuration connecting Gazebo to your ROS 2 nodes
- Understanding of what simulation can and cannot tell you
