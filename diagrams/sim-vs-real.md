# Simulation vs Real-World Separation

```mermaid
flowchart TB
    subgraph "SIMULATION ENVIRONMENT"
        direction TB
        S1[Gazebo Fortress<br/>Physics simulation]
        S2[Isaac Sim<br/>Photorealistic rendering]
        S3[ros_gz Bridge<br/>Sim ↔ ROS 2]
        S4[Simulated Sensors<br/>Gaussian noise models]
        S5[use_sim_time: true<br/>Deterministic clock]
        S6[Domain Randomization<br/>Parameter variation]

        S1 --> S3
        S2 --> S3
        S3 --> S4
        S1 --> S5
        S1 --> S6
    end

    subgraph "SHARED ROS 2 LAYER"
        direction TB
        R1[/joint_commands]
        R2[/joint_states]
        R3[/camera/image]
        R4[/lidar/scan]
        R5[/cmd_vel]
        R6[/tf]
    end

    subgraph "REAL-WORLD ENVIRONMENT"
        direction TB
        H1[Physical Hardware<br/>Actuators + sensors]
        H2[Real Sensors<br/>Complex noise, drift]
        H3[Hardware Drivers<br/>Sensor → ROS 2]
        H4[use_sim_time: false<br/>Wall clock]
        H5[Calibration Data<br/>Measured parameters]

        H1 --> H3
        H2 --> H3
        H1 --> H4
        H1 --> H5
    end

    S3 --> R1 & R2 & R3 & R4 & R5 & R6
    H3 --> R1 & R2 & R3 & R4 & R5 & R6

    subgraph "APPLICATION NODES (Identical)"
        direction TB
        A1[Object Detection]
        A2[Visual SLAM]
        A3[Nav2 Navigation]
        A4[VLA Pipeline]
    end

    R1 & R2 & R3 & R4 & R5 & R6 --> A1 & A2 & A3 & A4
```

## Sim-to-Real Gap Sources

| Dimension | Simulation | Reality | Mitigation |
|-----------|-----------|---------|-----------|
| **Physics** | Rigid body, simplified contact | Deformable, complex friction | Domain randomization |
| **Sensors** | Gaussian noise, fixed bias | Variable noise, drift, outliers | Noise model calibration |
| **Actuators** | Instant response | 10-50 ms latency, backlash | Latency injection in sim |
| **Timing** | Deterministic | Variable jitter | Delay randomization |
| **Environment** | Clean, known geometry | Messy, partially observable | Visual domain randomization |

## Transfer Protocol

1. Develop in simulation (fast iteration)
2. Validate in simulation (nominal + randomized)
3. Deploy to hardware (slow, safe motions first)
4. Measure sim-real gap
5. Calibrate simulation
6. Repeat (expect 3-10 cycles)
