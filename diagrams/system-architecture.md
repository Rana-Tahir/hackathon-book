# System Architecture Diagram

```mermaid
flowchart LR
    subgraph Input
        MIC[Microphone]
        CAM[Camera]
        LIDAR[LiDAR]
        IMU[IMU]
    end

    subgraph "Voice Pipeline"
        MIC --> WHISPER[Whisper STT]
        WHISPER --> LLM[LLM Intent Parser]
    end

    subgraph "Safety Layer"
        LLM --> VALIDATOR[Safety Filter]
        VALIDATOR -->|Schema| V1[Stage 1]
        VALIDATOR -->|Whitelist| V2[Stage 2]
        VALIDATOR -->|Bounds| V3[Stage 3]
        VALIDATOR -->|Rate| V4[Stage 4]
        VALIDATOR -->|Confidence| V5[Stage 5]
    end

    subgraph "Perception"
        CAM --> YOLO[YOLO Detection]
        CAM --> VSLAM[cuVSLAM]
        LIDAR --> COSTMAP[Costmap 2D]
        YOLO --> SCENE[Scene Description]
        SCENE --> LLM
    end

    subgraph "Navigation (Nav2)"
        VSLAM --> ODOM[Odometry]
        ODOM --> PLANNER[NavFn Planner]
        COSTMAP --> PLANNER
        PLANNER --> CONTROLLER[DWB Controller]
    end

    subgraph "ROS 2 Middleware"
        VALIDATOR -->|Validated Plan| TRANSLATOR[ROS 2 Translator]
        TRANSLATOR --> NAV_GOAL[Navigate Goal]
        TRANSLATOR --> DETECT_CMD[Detect Command]
        TRANSLATOR --> INTERACT_CMD[Interact Command]
        NAV_GOAL --> PLANNER
        CONTROLLER --> CMD_VEL[/cmd_vel]
    end

    subgraph "Actuation"
        CMD_VEL --> JOINTS[Joint Controllers]
        JOINTS --> HUMANOID[16-DOF Humanoid]
        IMU --> BALANCE[Balance Monitor]
        BALANCE --> JOINTS
    end

    subgraph "Simulation"
        HUMANOID --> GAZEBO[Gazebo Fortress]
        HUMANOID --> ISAAC[Isaac Sim]
    end
```

## Data Flow Summary

| Stage | Input | Output | Latency Target |
|-------|-------|--------|---------------|
| Whisper | Audio WAV | Text string | < 2 s |
| LLM Intent | Text + scene | JSON action plan | < 3 s |
| Safety Filter | Action plan | Validated plan | < 50 ms |
| ROS 2 Translator | Validated plan | Action goals | < 10 ms |
| Nav2 | Goal pose | cmd_vel | 50 ms (20 Hz) |
| Joint Controller | cmd_vel | Joint positions | 1 ms (1000 Hz) |
