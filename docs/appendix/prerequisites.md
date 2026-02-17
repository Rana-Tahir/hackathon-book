---
sidebar_position: 3
title: Prerequisites
---

# Prerequisites

Everything you need before starting this book.

## Required Skills

| Skill | Level | How to Verify |
|-------|-------|--------------|
| Python programming | Intermediate | You can write classes, use pip, and debug exceptions |
| Linux CLI (Ubuntu) | Basic | You can navigate directories, install packages, edit files |
| AI/ML concepts | Basic | You know what a neural network is and what "training" means |

## NOT Required

- Prior ROS or robotics experience
- Prior hardware or embedded systems experience
- Advanced mathematics beyond basic linear algebra

## Software

Install everything using the provided script:

```bash
bash hardware/workstation/install.sh
```

Or install manually — see [versions.md](https://github.com/your-repo/versions.md)
for the complete locked version matrix.

### Core Stack

| Software | Version | Install Method |
|----------|---------|---------------|
| Ubuntu | 22.04 LTS | Fresh install or VM |
| Python | 3.10 | System default on Ubuntu 22.04 |
| ROS 2 | Humble Hawksbill | APT repository |
| Gazebo | Fortress | `ros-humble-ros-gz` |
| Nav2 | Humble release | `ros-humble-navigation2` |
| Node.js | 18+ LTS | NodeSource repository |

### Optional (Module 3+)

| Software | Version | Install Method |
|----------|---------|---------------|
| NVIDIA Isaac Sim | 4.2+ | Omniverse Launcher |
| JetPack | 6.x | NVIDIA SDK Manager (Jetson only) |
| Unity | LTS | Unity Hub |

## Hardware

See the hardware requirements file (`hardware/requirements.md` in the repository root) for full
specifications. Summary:

- **Minimum**: RTX 3060 (8 GB VRAM), 32 GB RAM, 8-core CPU
- **Recommended**: RTX 4070+ (12+ GB VRAM), 64 GB RAM, 12+ core CPU
- **Edge**: Jetson Orin NX 16 GB (Module 3 deployment)

No RTX hardware? See [Cloud Alternatives](cloud-alternatives).
