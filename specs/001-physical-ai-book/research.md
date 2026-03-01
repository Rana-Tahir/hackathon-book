# Research: Physical AI & Humanoid Robotics — AI-Native Textbook

**Phase**: 0 — Environment Locking & Research
**Date**: 2026-02-16 (updated from 2026-02-13)
**Feature**: 001-physical-ai-book
**Constitution**: v2.0.0

## Version Compatibility Research (Preserved from v1)

### Decision 1: ROS 2 Distribution

**Decision**: ROS 2 Humble Hawksbill
**Rationale**: Humble is the current LTS release targeting Ubuntu 22.04
and Python 3.10. It has the broadest ecosystem support across Nav2,
Gazebo Fortress, and NVIDIA Isaac ROS packages. Humble's EOL extends
to 2027, providing stability for the book's lifecycle.
**Alternatives considered**:
- ROS 2 Iron (non-LTS; shorter support window; fewer tutorials)
- ROS 2 Jazzy (targets Ubuntu 24.04; would require changing base OS)

### Decision 2: Simulation Platform

**Decision**: Gazebo Fortress as primary; Unity 2022.3 LTS as optional
**Rationale**: Gazebo Fortress is the officially compatible version with
ROS 2 Humble via the `ros_gz` bridge packages. Unity is optional and
lightweight only (§6 Technical Stack Mandate).
**Alternatives considered**:
- Gazebo Garden/Harmonic (not officially paired with Humble)
- Webots (less ecosystem support for humanoid URDF)
- MuJoCo (excellent physics but lacks ROS 2 native integration)

### Decision 3: NVIDIA Isaac Platform

**Decision**: NVIDIA Isaac Sim — lightweight usage only
**Rationale**: Isaac MUST NOT require 24 GB+ VRAM as mandatory setup
(§6). Used for AI-enhanced perception and synthetic data generation
only. Not required for core book functionality.
**Alternatives considered**:
- Isaac Gym (deprecated in favor of Isaac Sim)
- Custom OpenCV pipelines (insufficient for synthetic data generation)

### Decision 4: Edge Deployment Platform

**Decision**: Jetson Orin Nano (8 GB baseline) per §6
**Rationale**: Constitution mandates Jetson Orin Nano as baseline edge
target. 8 GB is sufficient for single-pipeline inference.
**Alternatives considered**:
- Jetson Xavier (end-of-life)
- Intel NUC (not supported by Isaac ROS)

### Decision 5: Voice-to-Text Pipeline

**Decision**: OpenAI Whisper (small model by default)
**Rationale**: Whisper is the most widely adopted open-source STT model.
The `small` model runs on CPU and 8 GB VRAM edge devices.
**Alternatives considered**:
- Google Speech-to-Text (cloud dependency)
- Faster-Whisper (documented as optimization option)

### Decision 6: LLM for Task Planning

**Decision**: Document pattern using local LLM with cloud LLM as
alternative. Safety chain is the critical component, not the LLM.
**Rationale**: The safety chain
(LLM → Structured Output → Validator → Safe Action → ROS 2) is
mandated by §7. The specific LLM is interchangeable.
**Alternatives considered**:
- GPT-4 only (API dependency; cost barrier)
- Fine-tuned model (scope creep; prohibited by §3.5)

### Decision 7: Documentation Platform

**Decision**: Docusaurus 3.x (mandated by §3.7)
**Rationale**: Constitutional requirement. Already set up in `docs/`.
**Alternatives**: None — constitutionally locked.

## RAG Platform Research (New for v2.0.0)

### Decision 8: RAG Backend Architecture

**Decision**: FastAPI backend with Qdrant vector search + OpenAI
embeddings + LLM answer generation.
**Rationale**: FastAPI is constitutionally mandated (§3.7). Qdrant
Cloud free tier provides 1M vectors with 1 GB storage — sufficient
for ~200–250 embeddings from 36 chapters. OpenAI
`text-embedding-3-small` (1536 dimensions) is the smallest viable
embedding model with strong retrieval quality.
**Alternatives considered**:
- LangChain full stack: Too heavy, unnecessary abstraction.
- ChromaDB local: No free hosted tier; requires self-hosting.
- Pinecone: Free tier more limited than Qdrant.

### Decision 9: Embedding Strategy

**Decision**: One-time batch embedding with incremental updates via
content hashing. Chunk size: 600 tokens, overlap: 50 tokens.
**Rationale**: Constitution §3.6 prohibits re-embedding entire corpus
on every deploy. Content hashing (MD5 of chunk text) detects changed
content for incremental updates only. 600-token chunks balance
context richness with retrieval precision within the 500–800 mandated
range.
**Alternatives considered**:
- Sentence-level splitting: Too granular, wastes Qdrant free tier.
- Full-document embedding: Too coarse, poor retrieval precision.
- Auto re-embed on deploy: Prohibited by §3.6.

### Decision 10: Selected-Text Q&A

**Decision**: Browser `getSelection()` API captures selected text,
sent as context alongside user question to RAG endpoint. Backend
uses selected text to boost Qdrant search results via metadata
filtering (chapter, section).
**Rationale**: Simplest implementation satisfying §3.1 without
complex browser extensions or Docusaurus plugins.
**Alternatives considered**:
- Docusaurus plugin with markdown parser: Over-engineered.
- Highlight.js integration: Unnecessary dependency.

### Decision 11: Chat History Storage

**Decision**: Neon Serverless Postgres stores chat sessions with
question, answer, selected_text, chapter, and timestamp. Sessions
are anonymous by default (session ID via localStorage).
**Rationale**: Constitution §3.7 mandates Neon. Chat history enables
conversation continuity and analytics.
**Alternatives considered**:
- LocalStorage only: No server-side analytics.
- Redis: Adds infrastructure cost.

### Decision 12: Deployment Platform

**Decision**: Vercel for Docusaurus, Railway for FastAPI backend.
**Rationale**: Vercel mentioned in §3.7 with excellent Docusaurus
support. Railway offers free tier (500 hours/month) sufficient for
hackathon demo. Both support environment variables natively.
**Alternatives considered**:
- GitHub Pages + Render: Viable but more manual config.
- Fly.io for backend: Viable but Railway simpler for Python.

### Decision 13: Frontend Chatbot Component

**Decision**: Custom React component in Docusaurus via theme
swizzling (`Root.tsx` wrapper). Floating button, expandable panel.
**Rationale**: Docusaurus supports React natively. Swizzling `Root`
injects chatbot globally. OpenAI ChatKit SDK can simplify the UI.
**Alternatives considered**:
- Docusaurus plugin: More complex to maintain.
- iframe embed: Poor UX, no selected-text access.
- Third-party widget: Doesn't integrate with custom RAG backend.

## Hardware Research (Preserved)

### Minimum Workstation Requirements

Isaac Sim requires RTX GPU with minimum 8 GB VRAM for basic scenes.
Gazebo Fortress runs on CPU. Book + RAG system runs CPU-only (§3.5).

### Jetson Orin Nano (8 GB Baseline)

Sufficient for single-pipeline inference (VSLAM or Nav2). Documented
as the constitutional baseline (§6).

### Cloud Fallback

For learners without RTX hardware:
- NVIDIA Omniverse Cloud for Isaac Sim (latency documented)
- AWS RoboMaker for Gazebo (no Isaac)
- Cloud GPU instances (cost documented)

**Constraint**: Real-time robot control from cloud MUST document
latency risk (§6).

## Open Items

None. All research questions resolved.
