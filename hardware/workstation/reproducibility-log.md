# Reproducibility Test Log

**Date**: 2026-02-14
**Target**: Ubuntu 22.04 LTS (clean install)
**Status**: Partial — static analysis and build validation completed

## Environment Verification

| Component | Expected Version | Verified |
|-----------|-----------------|----------|
| Ubuntu | 22.04 LTS | Pending (requires clean VM) |
| ROS 2 | Humble Hawksbill | Pending |
| Gazebo | Fortress | Pending |
| Python | 3.10.x | Pending |
| Node.js | 20.x | Pending |
| Nav2 | Humble | Pending |
| Isaac Sim | 4.2+ | Pending |

## Chapter-by-Chapter Reproducibility

### Module 1: The Robotic Nervous System (ROS 2)

| Chapter | Key Commands/Artifacts | Status |
|---------|----------------------|--------|
| 01 — Introduction | Conceptual, no commands | N/A |
| 02 — Nodes & Topics | `ros2 run`, publisher/subscriber nodes | Pending |
| 03 — Services & Actions | `ros2 service call`, action server | Pending |
| 04 — URDF Humanoid | URDF file, `robot_state_publisher` | Pending |
| 05 — Launch & Params | Launch file, YAML params | Pending |
| 06 — Topic Reference | Reference table, no executable commands | N/A |
| 07 — Debugging | `rqt_graph`, `ros2 topic hz` | Pending |

### Module 2: Building the Virtual World (Gazebo)

| Chapter | Key Commands/Artifacts | Status |
|---------|----------------------|--------|
| 01 — Introduction | Conceptual overview | N/A |
| 02 — Gazebo World | SDF world file, `gz sim` | Pending |
| 03 — Spawning Humanoid | `ros2 run ros_gz_sim create` | Pending |
| 04 — Sensors | Plugin configuration, topic verification | Pending |
| 05 — ROS-GZ Bridge | Bridge config, message mapping | Pending |
| 06 — Simulation Limits | Conceptual, domain randomization theory | N/A |
| 07 — Debugging | Gazebo diagnostic commands | Pending |

### Module 3: Perception & Navigation (Isaac Sim + Nav2)

| Chapter | Key Commands/Artifacts | Status |
|---------|----------------------|--------|
| 01 — Introduction | Prerequisites check | Pending |
| 02 — Isaac Sim | Omniverse setup, ROS 2 bridge | Pending |
| 03 — Object Detection | YOLO node, TensorRT export | Pending |
| 04 — Visual SLAM | cuVSLAM configuration | Pending |
| 05 — Navigation | Nav2 config, costmap tuning | Pending |
| 06 — Sim-to-Real | Domain randomization workflow | Pending |
| 07 — Jetson Deployment | `nvpmodel`, `jetson_clocks` | Pending (requires Jetson) |
| 08 — Debugging | Diagnostic procedures | Pending |

### Module 4: Voice-Language-Action Pipeline

| Chapter | Key Commands/Artifacts | Status |
|---------|----------------------|--------|
| 01 — Introduction | Architecture overview | N/A |
| 02 — Whisper | `whisper_pipeline.py` node | Pending |
| 03 — Intent Parsing | `intent_parser.py` node | Pending |
| 04 — Safety Filter | `safety_filter.py` node | Pending |
| 05 — Multi-Modal | Scene description + grounding | Pending |
| 06 — Debugging | Stage diagnostic protocol | Pending |

### Capstone

| Chapter | Key Commands/Artifacts | Status |
|---------|----------------------|--------|
| 01 — Integration | Full launch config | Pending |
| 02 — Testing | Unit/integration/system tests | Pending |
| 03 — Next Steps | Resource links | N/A |

## Build Validation (Completed)

| Artifact | Command | Result |
|----------|---------|--------|
| Docusaurus site | `npx docusaurus build` | **PASS** — compiled successfully |
| Install script syntax | `bash -n install.sh` | **PASS** — no errors |
| API accuracy audit | Automated grep + verification | **PASS** — no hallucinated APIs |
| ROS 2 package structure | `resource/`, `package.xml`, `setup.py` | **PASS** — ament_python compliant |

## Notes
- Full reproducibility requires a clean Ubuntu 22.04 VM or container
- Jetson-specific chapters require Orin NX/AGX hardware
- Isaac Sim chapters require NVIDIA GPU with Omniverse installed
