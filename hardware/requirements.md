# Hardware Requirements

**Status**: LOCKED
**Date**: 2026-02-13

## Development Workstation

### Minimum (Modules 1–2)

| Component | Specification |
|-----------|--------------|
| OS | Ubuntu 22.04 LTS |
| CPU | 8-core x86_64 (Intel i7 12th gen / AMD Ryzen 7 7700X) |
| RAM | 32 GB DDR4/DDR5 |
| GPU | NVIDIA RTX 3060 |
| VRAM | 8 GB |
| Storage | 100 GB SSD (NVMe preferred) |
| Network | Internet connection for package downloads |

### Recommended (All Modules + Isaac Sim)

| Component | Specification |
|-----------|--------------|
| OS | Ubuntu 22.04 LTS |
| CPU | 12+ core x86_64 (Intel i9 13th gen / AMD Ryzen 9 7950X) |
| RAM | 64 GB DDR5 |
| GPU | NVIDIA RTX 4070 or higher |
| VRAM | 12+ GB |
| Storage | 256 GB NVMe SSD |
| Network | Internet connection for package downloads |

### Important Notes

- Running Gazebo + Isaac Sim simultaneously on a single GPU is NOT
  recommended. Use one simulator per session.
- Isaac Sim requires Ampere (RTX 30xx) or Ada Lovelace (RTX 40xx) GPU.
  Pascal (GTX 10xx) and Turing (RTX 20xx) are NOT supported.
- 32 GB RAM is the absolute floor for concurrent Gazebo + ROS 2.
  64 GB is needed for Isaac Sim workloads.

## Edge Deployment (Jetson Orin)

### Module 3 Baseline

| Component | Specification |
|-----------|--------------|
| Module | Jetson Orin NX 16 GB |
| GPU | Ampere iGPU, ~100 TOPS |
| RAM | 16 GB shared (CPU + GPU) |
| Storage | 64 GB eMMC + NVMe expansion |
| JetPack | 6.x (Ubuntu 22.04 base) |
| Use Case | CNN inference, VSLAM, Nav2 navigation |

### Full Capstone (Recommended)

| Component | Specification |
|-----------|--------------|
| Module | Jetson AGX Orin 64 GB |
| GPU | Ampere iGPU, ~275 TOPS |
| RAM | 64 GB shared (CPU + GPU) |
| Storage | 64 GB eMMC + NVMe expansion |
| JetPack | 6.x (Ubuntu 22.04 base) |
| Use Case | Multi-pipeline inference, small LLM on-device |

### Jetson Notes

- Orin NX 16 GB can run VSLAM + Nav2 concurrently but NOT an LLM.
- AGX Orin 64 GB is required for on-device LLM inference (7B class).
- JetPack 6.x ships Ubuntu 22.04, enabling native ROS 2 Humble.
- CUDA libraries on Jetson are aarch64; use L4T base containers.

## Training vs Inference Separation

| Environment | Hardware | Purpose |
|-------------|----------|---------|
| Workstation (RTX) | x86_64 + discrete GPU | Training, simulation, development |
| Jetson Orin | aarch64 + integrated GPU | Inference, edge deployment |
| Cloud (optional) | GPU instances | Simulation offload (NOT real-time control) |

Training code and inference code MUST be in separate directories.
No mixed-environment configurations are permitted.

## Cloud Alternatives

For learners without RTX hardware:

| Service | Use Case | Limitation |
|---------|----------|-----------|
| NVIDIA Omniverse Cloud | Isaac Sim | Latency; no real-time control |
| AWS RoboMaker | Gazebo simulation | Limited to Gazebo; no Isaac |
| Google Cloud GPU | General simulation | Cost; setup complexity |

**CRITICAL**: Cloud may be used for simulation and training ONLY.
Real-time robot control from cloud is PROHIBITED. Latency makes
cloud-based control unsafe for autonomous systems.
