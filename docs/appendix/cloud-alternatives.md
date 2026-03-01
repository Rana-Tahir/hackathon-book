---
sidebar_position: 1
title: Cloud Alternatives
---

# Cloud Simulation Alternatives

If you do not have an RTX-enabled workstation, cloud services can
provide GPU-accelerated simulation environments for portions of this
book.

## Available Options

| Service | Use Case | Modules Supported |
|---------|----------|------------------|
| NVIDIA Omniverse Cloud | Isaac Sim workloads | Module 3 |
| AWS RoboMaker | Gazebo simulation | Module 2 |
| Google Cloud GPU instances | General simulation | Modules 2–3 |

## Latency Warning

Cloud simulation introduces network latency between your terminal and
the simulator. This latency is acceptable for:

- Training and data generation
- Offline simulation runs
- Development and debugging

## Cloud Real-Time Control: PROHIBITED

**Real-time robot control from cloud is NOT supported and MUST NOT be
attempted.** Network latency makes cloud-based control unsafe for
autonomous systems. The round-trip delay between a sensor reading and
a motor command can exceed safety thresholds, leading to:

- Delayed obstacle avoidance
- Missed emergency stop signals
- Unstable locomotion control loops

All real-time control MUST run on local hardware (workstation or Jetson).

## Jetson Deployment

Jetson edge deployment (Module 3) requires physical hardware. There is
no cloud substitute for edge inference validation. If you do not have
a Jetson Orin, you can still complete the simulation portions of
Module 3 but must skip the deployment sections.
