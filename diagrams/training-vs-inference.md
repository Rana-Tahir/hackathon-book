# Training vs Inference Separation

```mermaid
flowchart TB
    subgraph "TRAINING (Workstation / Cloud)"
        direction TB
        T1[Synthetic Data Generation<br/>Isaac Sim Replicator]
        T2[Domain Randomization<br/>Physics, textures, lighting]
        T3[Model Training<br/>YOLO, RL policies]
        T4[Validation<br/>ATE, mAP, success rate]
        T5[Export<br/>ONNX → TensorRT]

        T1 --> T2 --> T3 --> T4 --> T5
    end

    subgraph "INFERENCE (Robot / Jetson)"
        direction TB
        I1[Camera Feed<br/>30 FPS RGB + Depth]
        I2[TensorRT Engine<br/>FP16 optimized]
        I3[Detections<br/>Bounding boxes + classes]
        I4[VSLAM<br/>Pose estimation]
        I5[Nav2<br/>Path following]
        I6[VLA Pipeline<br/>Voice → Action]

        I1 --> I2 --> I3
        I1 --> I4 --> I5
        I6 --> I5
    end

    T5 -->|Optimized model<br/>file transfer| I2

    subgraph "KEY RULES"
        R1["Training uses GPU clusters<br/>(hours to days)"]
        R2["Inference uses edge GPU<br/>(milliseconds per frame)"]
        R3["Never train on the robot"]
        R4["Never deploy unvalidated models"]
    end
```

## Separation Rules

| Concern | Training | Inference |
|---------|----------|-----------|
| **Hardware** | RTX 4090 / A100 / Cloud | Jetson Orin NX/AGX |
| **Precision** | FP32 (accuracy) | FP16 (speed) |
| **Batch size** | 16-128 | 1 (single frame) |
| **Latency** | Not critical | < 100 ms required |
| **Data** | Synthetic + real labeled | Live sensor stream |
| **Output** | Model weights (.pt) | Predictions per frame |
| **Location** | Off-robot | On-robot |
