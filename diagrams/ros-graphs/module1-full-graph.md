# Module 1 ROS Graph

```mermaid
flowchart LR
    subgraph "Nodes"
        RSP[robot_state_publisher]
        PUB[joint_command_publisher]
        SUB[joint_state_subscriber]
        SRV[joint_service]
        ACT[move_action_server]
    end

    subgraph "Topics"
        RD[/robot_description<br/>std_msgs/String]
        JC[/joint_commands<br/>sensor_msgs/JointState]
        JS[/joint_states<br/>sensor_msgs/JointState]
        TF[/tf<br/>tf2_msgs/TFMessage]
        TFS[/tf_static<br/>tf2_msgs/TFMessage]
    end

    subgraph "Services"
        GH[/go_home<br/>std_srvs/SetBool]
    end

    subgraph "Actions"
        MJ[/move_joints<br/>Fibonacci]
    end

    %% Publishers
    RSP -->|publishes| RD
    RSP -->|publishes| TF
    RSP -->|publishes| TFS
    PUB -->|publishes| JC

    %% Subscribers
    SUB -->|subscribes| JS
    RSP -->|subscribes| JS

    %% Services
    SRV -->|serves| GH

    %% Actions
    ACT -->|serves| MJ

    %% External
    JC -.->|"Gazebo/hardware<br/>would subscribe"| EXT[External Controller]
    EXT -.->|"would publish"| JS
```

## Topic Summary Table

| Topic | Type | Publisher | Subscriber | Rate |
|-------|------|----------|------------|------|
| `/joint_commands` | `sensor_msgs/JointState` | `joint_command_publisher` | (Gazebo/hardware) | 10 Hz |
| `/joint_states` | `sensor_msgs/JointState` | (Gazebo/hardware) | `joint_state_subscriber`, `robot_state_publisher` | varies |
| `/robot_description` | `std_msgs/String` | `robot_state_publisher` | (late joiners) | latched |
| `/tf` | `tf2_msgs/TFMessage` | `robot_state_publisher` | (all TF listeners) | matches `/joint_states` |
| `/tf_static` | `tf2_msgs/TFMessage` | `robot_state_publisher` | (all TF listeners) | latched |

## Service Summary

| Service | Type | Server | Description |
|---------|------|--------|-------------|
| `/go_home` | `std_srvs/SetBool` | `joint_service` | Command all joints to zero position |

## Action Summary

| Action | Type | Server | Description |
|--------|------|--------|-------------|
| `/move_joints` | `Fibonacci` (placeholder) | `move_action_server` | Multi-step joint movement with feedback |
