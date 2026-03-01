# Artifact Registry

**Phase**: 1 — Design & Contracts
**Date**: 2026-02-13
**Feature**: 001-physical-ai-book

## Purpose

Canonical registry of all artifacts produced by the book. Each artifact
has a unique ID, owning module, filesystem location, and validation
method. No artifact may exist outside this registry.

## Module 1 Artifacts — The Robotic Nervous System (ROS 2)

| ID | Artifact | Type | Location | Validation | FR |
|----|----------|------|----------|-----------|-----|
| A-001 | ROS 2 humanoid workspace | code-package | `code/ros2/` | `colcon build` succeeds | FR-002, FR-003 |
| A-002 | Humanoid URDF model | urdf | `code/ros2/urdf/humanoid.urdf.xacro` | `check_urdf` passes | FR-003 |
| A-003 | ROS graph diagrams | diagram | `diagrams/ros-graphs/` | Matches running `rqt_graph` output | FR-003 |
| A-004 | Topic/message flow tables | table | `docs/module-1/topics.md` | All topics verified via `ros2 topic list` | FR-003 |

## Module 2 Artifacts — The Digital Twin (Gazebo & Unity)

| ID | Artifact | Type | Location | Validation | FR |
|----|----------|------|----------|-----------|-----|
| A-005 | Gazebo humanoid world | simulation-scene | `code/simulation/gazebo/worlds/` | `gz sim` launches; humanoid visible | FR-004, FR-005 |
| A-006 | Sensor simulation configs | pipeline | `code/simulation/sensors/` | LiDAR, depth, IMU topics publish data | FR-004 |
| A-007 | Physics parameter docs | table | `docs/module-2/physics.md` | Parameters match Gazebo world file | FR-005 |
| A-008 | Gazebo vs Unity comparison | table | `docs/module-2/comparison.md` | Covers rendering, physics, ROS integration | FR-005 |

## Module 3 Artifacts — The AI-Robot Brain (NVIDIA Isaac)

| ID | Artifact | Type | Location | Validation | FR |
|----|----------|------|----------|-----------|-----|
| A-009 | Isaac Sim scenes | simulation-scene | `code/isaac/scenes/` | Isaac Sim loads scene without errors | FR-006, FR-007 |
| A-010 | VSLAM pipeline | pipeline | `code/isaac/vslam/` | Robot localizes in simulated environment | FR-006, FR-007 |
| A-011 | Nav2 navigation stack | pipeline | `code/navigation/` | `NavigateToPose` action reaches goal | FR-006, FR-007 |
| A-012 | Jetson deployment config | config | `hardware/jetson/` | Pipeline runs on Jetson within VRAM limits | FR-007, FR-013 |

## Module 4 Artifacts — Vision-Language-Action (VLA)

| ID | Artifact | Type | Location | Validation | FR |
|----|----------|------|----------|-----------|-----|
| A-013 | Voice command pipeline | pipeline | `code/vla/voice/` | Whisper transcribes test utterances | FR-008, FR-009 |
| A-014 | LLM → ROS 2 action bridge | code-package | `code/vla/llm-bridge/` | LLM output maps to valid ROS 2 actions | FR-008, FR-009 |
| A-015 | Safety/hallucination filter | code-package | `code/vla/safety/` | Unsafe commands rejected; safe commands pass | FR-009 |

## Capstone Artifacts — The Autonomous Humanoid

| ID | Artifact | Type | Location | Validation | FR |
|----|----------|------|----------|-----------|-----|
| A-016 | Capstone integration | code-package | `code/vla/capstone/` | Full voice-to-action pipeline executes | FR-010 |
| A-017 | Capstone evaluation results | table | `docs/capstone/evaluation.md` | All 4 criteria documented with results | FR-011 |

## Cross-Cutting Artifacts

| ID | Artifact | Type | Location | Validation | FR |
|----|----------|------|----------|-----------|-----|
| A-018 | Version lock file | config | `versions.md` | All versions verified installable | FR-017 |
| A-019 | Hardware requirement matrix | table | `hardware/requirements.md` | Specs match tested configurations | FR-013 |
| A-020 | Docusaurus site | documentation | `docs/` | `npm run build` succeeds | FR-018 |

## Artifact Status Tracking

Status progression: `PLANNED → IN_PROGRESS → VALIDATED → DOCUMENTED`

All artifacts begin as `PLANNED`. Status updates tracked during
`/sp.tasks` execution.
