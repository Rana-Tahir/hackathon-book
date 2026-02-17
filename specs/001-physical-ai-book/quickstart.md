# Quickstart: Physical AI & Humanoid Robotics — AI-Native Textbook

**Date**: 2026-02-16 (updated from 2026-02-13)
**Feature**: 001-physical-ai-book
**Constitution**: v2.0.0

## Quick Start — Book + RAG System (CPU-Only)

The book and RAG chatbot run in CPU-only mode (§3.5).

### Prerequisites

- Node.js 18+ (for Docusaurus)
- Python 3.10+ (for FastAPI backend)
- Git

### Step 1: Clone and Install Frontend

```bash
git clone <repository-url>
cd hackathon-book/docs
npm install
npm run build    # Verify Docusaurus builds
npm start        # Dev server at localhost:3000
```

### Step 2: Set Up Backend

```bash
cd hackathon-book/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
cp .env.example .env
# Fill in:
#   OPENAI_API_KEY=sk-...
#   QDRANT_URL=https://xxx.qdrant.io
#   QDRANT_API_KEY=...
#   NEON_DATABASE_URL=postgresql://...
```

### Step 4: Run Embedding Pipeline (One-Time)

```bash
python scripts/embed_content.py
# Embeds ~36 chapters into ~200-250 vectors in Qdrant
```

### Step 5: Start Backend

```bash
uvicorn app.main:app --reload --port 8000
# API at localhost:8000/api/health
```

### Step 6: Verify

- [ ] `localhost:3000` — Docusaurus site loads
- [ ] `localhost:8000/api/health` — Returns "healthy"
- [ ] Chatbot responds to questions from book content

## Full Development Setup (Robotics + Simulation)

For working with the ROS 2/Gazebo/VLA code artifacts, you need
Ubuntu 22.04 and RTX hardware. See `hardware/workstation/install.sh`.

### Prerequisites

- Ubuntu 22.04 LTS
- RTX 3060+ (8 GB VRAM minimum)
- 32 GB RAM minimum
- 100 GB free SSD

### Step 1: Run Install Script

```bash
bash hardware/workstation/install.sh
```

### Step 2: Build ROS 2 Workspace

```bash
cd code/ros2
colcon build
source install/setup.bash
```

### Step 3: Launch Simulation

```bash
# Module 1: ROS 2 humanoid
ros2 launch humanoid_base humanoid_bringup.launch.py

# Module 2: Gazebo world
gz sim code/gazebo/worlds/humanoid_world.sdf
```

### Validation

- [ ] `ros2 --version` returns Humble
- [ ] `gz sim --version` returns Fortress
- [ ] `colcon build` succeeds in `code/ros2/`
- [ ] Docusaurus build succeeds in `docs/`
- [ ] Backend health check passes

## Cloud Alternative

If RTX hardware is unavailable:
1. Use NVIDIA Omniverse Cloud for Isaac Sim workloads
2. Use AWS RoboMaker for Gazebo simulation
3. Book + RAG system runs CPU-only (no GPU needed)

**Warning**: Cloud simulation introduces network latency. Real-time
robot control from cloud MUST document latency risk (§6).
