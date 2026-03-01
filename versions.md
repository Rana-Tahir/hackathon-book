# Version Lock Matrix

**Status**: LOCKED
**Date**: 2026-02-13
**Rule**: No version upgrades permitted mid-authoring. If a conflict is
discovered, pause implementation, update this file, and re-validate
affected modules.

## Software Stack

| Component | Version | Source | Notes |
|-----------|---------|--------|-------|
| Ubuntu | 22.04 LTS (Jammy) | Official ISO | Base OS for all development |
| Python | 3.10.x | System (Ubuntu 22.04) | Do NOT use 3.11+; ROS 2 Humble requires 3.10 |
| ROS 2 | Humble Hawksbill | `ros-humble-desktop` | LTS; EOL May 2027 |
| Gazebo | Fortress | `ros-humble-ros-gz` | Use `ros_gz` bridge, NOT `gazebo_ros_pkgs` (Classic) |
| Nav2 | Humble release (1.1.x) | `ros-humble-navigation2` | Tied to Humble APT repo |
| NVIDIA Isaac Sim | 4.2+ | Omniverse Launcher / NGC | Requires Omniverse Kit 106; ROS 2 Humble bridge |
| JetPack | 6.x | NVIDIA SDK Manager | Jetson Orin; Ubuntu 22.04 base; verify latest at developer.nvidia.com |
| CUDA | 12.x | Bundled with JetPack | Aligned with JetPack 6.x; aarch64 on Jetson |
| TensorRT | 10.x | Bundled with JetPack | For inference optimization on Jetson |
| Unity | 2022.3 LTS or Unity 6 LTS | Unity Hub | Verify ROS-TCP-Connector compatibility |
| Whisper | Latest stable | `pip install openai-whisper` | Pin exact version in requirements.txt |
| faster-whisper | Latest stable | `pip install faster-whisper` | Optional: 4x faster, lower VRAM |
| Docusaurus | 3.6.x | npm | Requires Node.js 18+ |
| Node.js | 18.x or 20.x LTS | Official repo | For Docusaurus build |

## Python Dependencies

```text
# requirements.txt (pin exact versions during Phase 0 validation)
openai-whisper>=20240930
faster-whisper>=1.0.0
torch>=2.1.0
transformers>=4.36.0
rclpy  # Provided by ROS 2 Humble
```

## ROS 2 Packages

```text
ros-humble-desktop
ros-humble-ros-gz
ros-humble-navigation2
ros-humble-nav2-bringup
ros-humble-rviz2
ros-humble-robot-state-publisher
ros-humble-joint-state-publisher
ros-humble-xacro
```

## Known Compatibility Warnings

- Do NOT use Gazebo Classic 11 (`gazebo_ros_pkgs`) with Humble; use
  Gazebo Fortress via `ros_gz`.
- Isaac Sim 4.x dropped Pascal GPU support; requires Ampere (RTX 30xx)
  or Ada Lovelace (RTX 40xx).
- Isaac Sim native ROS 2 bridge and `ros_gz` bridge MUST NOT run
  simultaneously; they conflict on topic routing.
- JetPack CUDA libraries are aarch64; NOT compatible with x86 Docker
  containers. Use NVIDIA L4T base containers.
- Nav2 behavior tree XML from Foxy/Galactic is NOT compatible with
  Humble; do not copy from older tutorials.
- Whisper requires `ffmpeg` installed system-wide; missing this is the
  most common install failure.
