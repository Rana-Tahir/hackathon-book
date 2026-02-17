---
sidebar_position: 1
title: "Capstone Integration"
---

# Capstone Integration

The capstone project integrates every module into a single end-to-end
demonstration: a humanoid robot that receives a voice command,
perceives its environment, plans a sequence of actions, validates
them for safety, and executes them in simulation.

## The Full Pipeline

```
Voice Command
    │
    ▼
Whisper (Module 4) ──► Text
    │
    ▼
Scene Description ◄── YOLO Detection (Module 3)
    │                       ▲
    ▼                       │
LLM Intent Parser ──► Action Plan
    │
    ▼
Safety Filter (Module 4) ──► Validated Plan
    │
    ▼
ROS 2 Translator
    │
    ├──► Nav2 (Module 3) ──► Robot Navigation
    ├──► Joint Controllers (Module 1) ──► Arm Motion
    └──► Speech Synthesis ──► Audio Response
    │
    ▼
Gazebo / Isaac Sim (Module 2) ──► Physics + Rendering
```

## What You Will Demonstrate

The capstone scenario: **Voice-Commanded Object Retrieval**

1. Operator says: "Go to the table and bring me the red cup"
2. Whisper transcribes the command
3. YOLO + depth camera build a scene description
4. LLM produces an action plan: navigate → detect → pick up → navigate back
5. Safety filter validates every action
6. Robot navigates to the table using Nav2
7. Robot detects the red cup using YOLO
8. Robot picks up the cup (simulated grasp)
9. Robot navigates back to the operator
10. Robot confirms task completion

## Integration Architecture

Each module provides a ROS 2 interface. Integration is wiring:

| Module | Provides | Consumes |
|--------|----------|----------|
| Module 1 | Joint control, TF tree | Joint commands |
| Module 2 | Physics simulation, sensor data | Robot model, world |
| Module 3 | Object detection, SLAM, Nav2 | Camera/LiDAR data |
| Module 4 | Voice → Action pipeline | Scene description, Nav2 goals |

## Launch Configuration

A single launch file starts everything:

```python
# launch/capstone.launch.py
def generate_launch_description():
    return LaunchDescription([
        # Simulation
        IncludeLaunchDescription('simulation.launch.py'),
        # Perception
        IncludeLaunchDescription('perception.launch.py'),
        # Navigation
        IncludeLaunchDescription('navigation.launch.py'),
        # VLA Pipeline
        IncludeLaunchDescription('vla_pipeline.launch.py'),
    ])
```

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Voice command → first action | < 5 seconds |
| Object detection accuracy | > 90% mAP |
| Navigation success rate | 100% (no collisions) |
| Safety filter false negatives | 0 |
| End-to-end task completion | > 80% |

## What You Will Build

- Complete integration of all four modules
- Single-command launch for the entire system
- End-to-end test scenario with measurable success criteria
- Foundation for extending to new tasks and environments
