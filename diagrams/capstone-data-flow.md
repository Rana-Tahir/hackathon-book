# Capstone Data Flow Map

```mermaid
flowchart TB
    subgraph "Module 1: ROS 2 Foundation"
        M1_URDF[URDF Model<br/>A-002]
        M1_NODES[ROS 2 Nodes<br/>A-001]
        M1_TOPICS[Topics & Services<br/>A-004]
        M1_LAUNCH[Launch System]
    end

    subgraph "Module 2: Simulation"
        M2_WORLD[Gazebo World<br/>A-005]
        M2_SENSORS[Sensor Plugins<br/>A-006]
        M2_BRIDGE[ros_gz Bridge]
        M2_PHYSICS[Physics Config<br/>A-007]
    end

    subgraph "Module 3: Perception & Navigation"
        M3_ISAAC[Isaac Sim<br/>A-009]
        M3_VSLAM[Visual SLAM<br/>A-010]
        M3_NAV2[Nav2 Stack<br/>A-011]
        M3_YOLO[Object Detection]
        M3_JETSON[Jetson Config<br/>A-012]
    end

    subgraph "Module 4: VLA"
        M4_WHISPER[Whisper Pipeline<br/>A-013]
        M4_LLM[LLM Intent Parser<br/>A-014]
        M4_SAFETY[Safety Filter<br/>A-015]
        M4_TRANSLATOR[ROS 2 Translator]
    end

    subgraph "Capstone: End-to-End"
        C_VOICE[Voice Input]
        C_PLAN[Action Plan]
        C_EXEC[Execution]
        C_RESULT[Task Completion<br/>A-016, A-017]
    end

    %% Module 1 → Module 2
    M1_URDF -->|Robot model| M2_WORLD
    M1_NODES -->|Control interface| M2_BRIDGE
    M1_TOPICS -->|Topic definitions| M2_SENSORS

    %% Module 2 → Module 3
    M2_SENSORS -->|Camera, LiDAR, IMU| M3_VSLAM
    M2_SENSORS -->|Camera images| M3_YOLO
    M2_WORLD -->|Simulation env| M3_ISAAC
    M2_BRIDGE -->|Sensor data| M3_NAV2

    %% Module 3 → Module 4
    M3_YOLO -->|Detections| M4_LLM
    M3_VSLAM -->|Pose estimate| M4_TRANSLATOR
    M3_NAV2 -->|Navigation goals| M4_TRANSLATOR

    %% Module 4 → Capstone
    M4_WHISPER -->|Transcription| M4_LLM
    M4_LLM -->|Action plan| M4_SAFETY
    M4_SAFETY -->|Validated plan| M4_TRANSLATOR

    %% Capstone flow
    C_VOICE --> M4_WHISPER
    M4_TRANSLATOR --> C_EXEC
    C_EXEC --> C_RESULT

    %% Cross-cutting
    M4_SAFETY -.->|Emergency stop| M1_NODES
    M3_NAV2 -.->|cmd_vel| M1_NODES
```

## Inter-Module Contracts

| From | To | Interface | Message Type |
|------|-----|-----------|-------------|
| Module 1 | Module 2 | URDF → Gazebo spawn | `robot_description` topic |
| Module 2 | Module 3 | Sensor data | `sensor_msgs/Image`, `LaserScan`, `Imu` |
| Module 3 | Module 4 | Object detections | `vision_msgs/Detection2DArray` |
| Module 3 | Module 4 | Robot pose | `nav_msgs/Odometry` + TF |
| Module 4 | Module 3 | Navigation goals | `geometry_msgs/PoseStamped` |
| Module 4 | Module 1 | Joint commands | `sensor_msgs/JointState` |
| Safety | All | Emergency stop | `std_msgs/Bool` on `/emergency_stop` |

## Artifact Dependency Chain

```
A-001 (ROS 2 workspace)
  └── A-002 (URDF) ──► A-005 (Gazebo world)
       └── A-006 (Sensors) ──► A-010 (VSLAM)
            └── A-011 (Nav2) ──► A-013 (Whisper)
                 └── A-014 (LLM) ──► A-015 (Safety)
                      └── A-016 (Capstone integration)
                           └── A-017 (Evaluation)
```
