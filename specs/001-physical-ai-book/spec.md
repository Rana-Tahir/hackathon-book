# Feature Specification: Physical AI & Humanoid Robotics — AI-Native Textbook

**Feature Branch**: `001-physical-ai-book`
**Created**: 2026-02-13
**Updated**: 2026-02-16
**Status**: Draft
**Constitution**: v2.0.0
**Input**: User description: "Build a 4-module AI-native interactive textbook on Physical AI and Humanoid Robotics using Docusaurus, with an embedded RAG chatbot (FastAPI + Qdrant + Neon), deployed via Vercel/GitHub Pages."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Learn ROS 2 from Zero to Humanoid Control (Priority: P1)

A software engineer with Python experience but no ROS background
opens Module 1 and follows the curriculum sequentially. They install
ROS 2 Humble on Ubuntu 22.04, build their first node, define a
humanoid URDF, and wire up topics, services, and actions until a
simulated humanoid responds to programmatic commands in Gazebo
Fortress.

**Why this priority**: ROS 2 is the foundation for every subsequent
module. Without a working nervous system, no simulation, perception,
or VLA pipeline can function.

**Independent Test**: A learner with only Python and Linux skills can
complete Module 1 in isolation and have a working ROS 2 humanoid
package that publishes and subscribes to joint commands.

**Acceptance Scenarios**:

1. **Given** a learner with Python and Ubuntu 22.04, **When** they
   follow Module 1 end-to-end, **Then** they produce a running ROS 2
   Humble package with a humanoid URDF that accepts joint commands
   via topics.
2. **Given** a completed Module 1, **When** the learner runs the
   provided launch file, **Then** the ROS graph shows all expected
   nodes, topics, and services without errors.
3. **Given** a learner encounters an error, **When** they consult
   the debugging section, **Then** they find the failure mode
   documented with resolution steps.

---

### User Story 2 — Simulate a Physically Realistic Humanoid (Priority: P1)

A robotics practitioner completes Module 1 and moves to Module 2.
They set up a Gazebo Fortress simulation environment, configure
gravity and collision parameters, attach simulated sensors (LiDAR,
depth cameras, IMUs), and observe the humanoid operating under
realistic physics. They understand sim-to-real transfer principles
and domain randomization techniques.

**Why this priority**: Simulation is the proving ground mandated by
the constitution (§3.4 Artifact-First Integrity). All downstream
perception and action depend on a trustworthy digital twin.

**Independent Test**: A learner can complete Module 2 with only a
URDF from Module 1 and have a physically simulated humanoid
generating sensor data streams.

**Acceptance Scenarios**:

1. **Given** a humanoid URDF from Module 1, **When** the learner
   follows Module 2, **Then** a Gazebo Fortress environment launches
   with gravity, collisions, and rigid body dynamics enabled.
2. **Given** a running simulation, **When** the learner enables
   sensor plugins, **Then** LiDAR, depth camera, and IMU data
   streams are published on documented ROS 2 topics.
3. **Given** sim-to-real coverage, **When** the learner reads the
   domain randomization section, **Then** they can apply
   randomization to bridge the simulation–reality gap.

---

### User Story 3 — Deploy Perception and Navigation on Sim and Edge (Priority: P1)

An AI/ML engineer progresses to Module 3. They implement object
detection pipelines, configure Visual SLAM, and set up Nav2 for
autonomous navigation. They use NVIDIA Isaac in lightweight mode
(no 24 GB+ VRAM required) and follow Jetson Orin Nano deployment
instructions for edge inference.

**Why this priority**: Perception and navigation are the bridge
between simulation and autonomous action — the core intelligence
that enables the capstone.

**Independent Test**: A learner can run a perception pipeline and
Nav2 stack in Gazebo, then follow Jetson deployment instructions
to run inference on edge hardware (8 GB baseline).

**Acceptance Scenarios**:

1. **Given** a simulated environment with sensor data, **When** the
   learner follows Module 3, **Then** a perception pipeline detects
   and localizes objects within the environment.
2. **Given** a configured Nav2 stack, **When** the learner issues a
   navigation goal, **Then** the humanoid navigates to the goal
   while avoiding obstacles.
3. **Given** completed simulation pipelines, **When** the learner
   follows Jetson Orin Nano deployment instructions, **Then** the
   perception pipeline runs within documented resource constraints
   (8 GB VRAM baseline).

---

### User Story 4 — Control a Robot with Natural Language (Priority: P2)

A developer reaches Module 4 and integrates voice input, LLM-based
task planning, and ROS 2 action execution. They issue a spoken
command, observe the LLM decompose it into structured actions, watch
the validator enforce safety constraints, and see the simulated
humanoid execute the plan.

**Why this priority**: VLA is the capstone-enabling integration that
turns a reactive robot into a conversational agent, but it depends
on all prior modules being solid.

**Independent Test**: A learner can issue a voice command, see the
LLM produce a structured action plan that passes the safety
validator, and observe the ROS 2 actions execute in simulation.

**Acceptance Scenarios**:

1. **Given** a working ROS 2 + simulation + perception stack,
   **When** the learner follows Module 4, **Then** a voice command
   is transcribed, interpreted by an LLM, and translated into
   structured ROS 2 actions via the safety chain
   (LLM → Structured Output → Validator → Safe Action → ROS 2).
2. **Given** an unsafe or ambiguous command, **When** the VLA
   pipeline processes it, **Then** the validator rejects or modifies
   the command before ROS 2 execution.
3. **Given** a completed VLA pipeline, **When** the learner reads
   the hallucination mitigation section, **Then** they understand
   why LLM outputs MUST NEVER directly execute ROS actions.

---

### User Story 5 — Complete the Autonomous Humanoid Capstone (Priority: P2)

A learner who has completed all four modules undertakes the capstone.
They integrate voice input, LLM planning, ROS 2 coordination, Nav2
navigation, vision-based object identification, and manipulation into
a single autonomous humanoid system in simulation.

**Why this priority**: The capstone is the ultimate validation of the
constitution (§12). It proves all modules work together.

**Independent Test**: The capstone can be evaluated against the six
functional steps: receive command, interpret intent, plan actions,
navigate, identify objects, and manipulate/interact.

**Acceptance Scenarios**:

1. **Given** a voice command (e.g., "Pick up the red ball"), **When**
   the capstone system processes it, **Then** the humanoid navigates
   to the object, identifies it visually, and interacts with it.
2. **Given** environmental noise or ambiguity, **When** the system
   operates, **Then** it degrades gracefully with documented failure
   modes and recovery behavior.
3. **Given** a completed capstone, **When** evaluated against
   criteria (functional correctness, noise robustness, physical
   realism, sim-to-real readiness), **Then** all criteria pass.

---

### User Story 6 — Ask the Book Questions via RAG Chatbot (Priority: P1)

A learner reading any chapter encounters a concept they want to
explore. They either select text and ask a question about it, or
use the embedded chatbot to ask a free-form question. The chatbot
answers only from the book's embedded content, grounded in the
selected text or chapter context.

**Why this priority**: The RAG chatbot is a core constitutional
requirement (§3.1 AI-Native by Design). Without it, the book is
static documentation — explicitly prohibited by the constitution.

**Independent Test**: A learner can select text, ask a question,
and receive an answer sourced exclusively from book content with
no speculative or hallucinated robotics claims.

**Acceptance Scenarios**:

1. **Given** a learner reading a chapter, **When** they select text
   and ask a question, **Then** the chatbot answers from the
   selected passage and surrounding context.
2. **Given** a free-form question about ROS 2 topics, **When** the
   chatbot processes it, **Then** it retrieves relevant book content
   via Qdrant and responds with grounded answers.
3. **Given** a question outside the book's scope, **When** the
   chatbot processes it, **Then** it clearly states it cannot answer
   and does not speculate.
4. **Given** the RAG backend, **When** embeddings are checked,
   **Then** chunk size is 500–800 tokens, no redundant content is
   embedded, and usage is within Qdrant Free Tier limits.

---

### User Story 7 — Reproduce All Examples on Standard Hardware (Priority: P1)

A learner with a mid-range RTX workstation (8–12 GB VRAM) follows
the setup instructions and reproduces every code example, simulation,
and pipeline in the book without encountering undocumented
dependencies, hallucinated APIs, or 24 GB+ VRAM requirements.

**Why this priority**: Reproducibility is a non-negotiable quality
standard (§3.4, §3.5). A book that cannot be followed is not a book.

**Independent Test**: A fresh Ubuntu 22.04 environment with
documented prerequisites can run every example from any module.

**Acceptance Scenarios**:

1. **Given** a fresh Ubuntu 22.04 installation with documented
   hardware, **When** the learner follows setup instructions,
   **Then** all dependencies install without errors.
2. **Given** any code example in any module, **When** the learner
   runs it as documented, **Then** it produces the expected output
   without modification.
3. **Given** a learner without RTX hardware, **When** they consult
   the cloud alternatives section, **Then** they find documented
   cloud simulation options with latency warnings.
4. **Given** the book + RAG system only, **When** run on CPU-only
   hardware, **Then** the Docusaurus site and chatbot function
   without GPU.

---

### User Story 8 — Access the Deployed Book Online (Priority: P1)

A learner visits the publicly deployed book URL. The Docusaurus site
loads quickly with a clean, minimal UI. They navigate between modules,
interact with the RAG chatbot, and watch the demo video — all within
a publicly accessible, reproducible deployment.

**Why this priority**: Hackathon compliance (§3.7) requires a public
deployment with all base functionality operational.

**Independent Test**: The deployed URL is publicly accessible, loads
the Docusaurus site, and the RAG chatbot responds to queries.

**Acceptance Scenarios**:

1. **Given** a public URL, **When** a user visits it, **Then** the
   Docusaurus site loads with all four modules navigable.
2. **Given** the deployed site, **When** a user interacts with the
   chatbot, **Then** responses come from the FastAPI backend via
   Qdrant with grounded answers.
3. **Given** the public GitHub repo, **When** a developer clones it,
   **Then** they can build and run the site locally with documented
   instructions.
4. **Given** the demo video requirement, **When** the video is
   played, **Then** it demonstrates core functionality in ≤ 90
   seconds.

---

### Edge Cases

- What happens when a learner does not have RTX hardware? Cloud
  simulation alternatives MUST be documented with latency warnings.
- What happens when a voice command is in a language other than
  English? The book MUST document supported languages and
  limitations.
- What happens when ROS 2 Humble or Gazebo Fortress versions receive
  patches? The book MUST pin exact versions and document
  known-compatible ranges.
- What happens when simulation physics diverge from real-world
  behavior? The book MUST include a sim-to-real gap discussion
  with domain randomization techniques.
- What happens when an LLM hallucinates an unsafe action? The safety
  chain (§7) MUST reject it before ROS 2 execution.
- What happens when the RAG chatbot is asked something outside the
  book? It MUST refuse to speculate and state its limitation.
- What happens when Qdrant Free Tier limits are approached? The
  embedding strategy MUST use metadata filtering over re-embedding.
- What happens when API keys are accidentally exposed? The
  deployment MUST use environment variables exclusively (§9).

## Requirements *(mandatory)*

### Functional Requirements

**Content & Curriculum:**

- **FR-001**: The book MUST contain exactly four instructional modules
  plus one capstone, in the order: Foundations & ROS 2, Simulation &
  Digital Twins, Perception & Navigation, VLA & Capstone.
- **FR-002**: Module 1 MUST cover ROS 2 Humble architecture (nodes,
  topics, services, actions), URDF humanoid modeling, launch files,
  parameter management, and the robotic nervous system metaphor.
- **FR-003**: Module 2 MUST cover Gazebo Fortress (worlds, plugins,
  sensors), humanoid digital twins, sim-to-real transfer, domain
  randomization, and NVIDIA Isaac lightweight integration.
- **FR-004**: Module 3 MUST cover sensor fusion, object detection,
  Nav2 navigation, SLAM, path planning, and
  perception-to-planning interface contracts.
- **FR-005**: Module 4 MUST cover LLM-based intent interpretation,
  VLA pipeline architecture, the safety chain
  (LLM → Structured Output → Validator → Safe Action → ROS 2),
  and edge deployment on Jetson Orin Nano.
- **FR-006**: The capstone MUST demonstrate a simulated humanoid that
  receives a voice command, interprets intent via LLM, plans actions
  via ROS 2, navigates via Nav2, identifies objects via vision, and
  manipulates/interacts with the target object.
- **FR-007**: Every module MUST include failure modes and debugging
  guidance for each major pipeline or workflow.
- **FR-008**: All instructional material MUST build toward the
  capstone (§3.3 Capstone-Driven Architecture).

**Platform & Deployment:**

- **FR-009**: The book MUST be built using Docusaurus and pass
  production build without errors.
- **FR-010**: The book MUST be deployed via GitHub Pages or Vercel
  and be publicly accessible.
- **FR-011**: The book MUST include an embedded RAG chatbot with
  context-aware answering and selected-text question answering.
- **FR-012**: The RAG backend MUST use FastAPI, Qdrant Cloud (free
  tier), and Neon Serverless Postgres.
- **FR-013**: The RAG chatbot MUST answer only from embedded book
  content and MUST NOT speculate on robotics claims.
- **FR-014**: The public GitHub repository MUST be clean,
  documented, and reproducible.
- **FR-015**: A demo video (≤ 90 seconds) MUST demonstrate core
  functionality.

**Resource & Embedding Constraints:**

- **FR-016**: All examples MUST be runnable on a mid-range RTX GPU
  (8–12 GB VRAM) or equivalent cloud instance.
- **FR-017**: The book + RAG system MUST function in CPU-only mode.
- **FR-018**: NVIDIA Isaac usage MUST NOT require 24 GB+ VRAM as a
  mandatory setup.
- **FR-019**: Embeddings MUST use 500–800 token chunks with minimal
  overlap and canonical content only.
- **FR-020**: Re-embedding the entire corpus on every deploy is
  prohibited.
- **FR-021**: Embedding usage MUST stay within Qdrant Free Tier
  limits.
- **FR-022**: Metadata filtering MUST be preferred over
  re-embedding.

**Safety & Security:**

- **FR-023**: LLM outputs MUST NEVER directly execute ROS actions.
  The safety chain
  (LLM → Structured Output → Validator → Safe Action → ROS 2)
  is mandatory.
- **FR-024**: No API keys in the repository. Environment variables
  are mandatory for all secrets.
- **FR-025**: No hallucinated APIs, hardware capabilities, or
  invented interfaces. All references MUST be verifiable.
- **FR-026**: Every code example MUST be reproducible on documented
  hardware without modification.

**Artifact Integrity:**

- **FR-027**: Every technical claim MUST be backed by working ROS 2
  packages, valid URDF models, launchable simulation, or
  reproducible commands.
- **FR-028**: Software versions MUST be pinned: Ubuntu 22.04 LTS,
  ROS 2 Humble, Gazebo Fortress, Nav2, NVIDIA Isaac (lightweight).
- **FR-029**: Cloud simulation alternatives MUST be documented with
  latency risk warnings for real-time robot control.

### Key Entities

- **Module**: A self-contained instructional unit with defined scope,
  required coverage areas, required artifacts, and a learning
  outcome. Exactly four modules exist.
- **Artifact**: A concrete deliverable produced by a module (ROS 2
  package, URDF model, simulation scene, perception pipeline,
  diagram, or table).
- **Capstone**: An integrative project that combines all module
  outputs into a single autonomous humanoid system.
- **RAG Chatbot**: An embedded AI assistant that answers questions
  from book content only, using FastAPI + Qdrant + Neon.
- **Hardware Profile**: A documented set of hardware requirements
  (mid-range RTX workstation, Jetson Orin Nano 8 GB) with
  CPU/GPU/VRAM constraints.
- **Safety Chain**: The mandatory validation pipeline
  (LLM → Structured Output → Validator → Safe Action → ROS 2)
  that prevents LLM hallucinations from reaching actuators.

## Optional Bonus Features

These features are NOT required but are defined for consistency if
implemented. Each MUST comply with the constitution (§4).

- **Authentication (Better-Auth)**: Signup/signin with user hardware
  and software background collection. No plaintext secrets.
- **Personalization Layer**: Per-chapter button that adapts content to
  user background. MUST NOT alter factual correctness or hallucinate
  alternate APIs.
- **Urdu Translation**: Per-chapter toggle preserving code formatting,
  technical accuracy, and semantic fidelity.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A learner with Python and Linux skills but no ROS
  experience can complete Module 1 and produce a working humanoid
  ROS 2 package.
- **SC-002**: All four modules and the capstone are fully authored
  with every required artifact present.
- **SC-003**: 100% of code examples reproduce without modification
  on a mid-range RTX workstation (8–12 GB VRAM) running
  Ubuntu 22.04.
- **SC-004**: The capstone humanoid successfully receives a voice
  command, plans, navigates, identifies, and interacts with an
  object in simulation.
- **SC-005**: The Docusaurus build completes without errors and is
  publicly deployed.
- **SC-006**: The RAG chatbot answers book-based questions correctly,
  refuses out-of-scope queries, and stays within Qdrant Free Tier
  embedding limits.
- **SC-007**: Every module includes at least one debugging/failure
  mode section per major workflow.
- **SC-008**: Zero hallucinated APIs, hardware capabilities, or
  speculative robotics claims in the final content.
- **SC-009**: The complete book guides a learner from zero ROS
  knowledge to a working autonomous humanoid simulation.
- **SC-010**: No example requires 24 GB+ VRAM or GPU-heavy training.
- **SC-011**: The book + RAG system runs in CPU-only mode.
- **SC-012**: The public GitHub repo is clean, documented, and
  reproducible on a fresh Ubuntu 22.04 install.
- **SC-013**: Demo video demonstrates core functionality in ≤ 90
  seconds.

## Assumptions

- Target stack is locked: Ubuntu 22.04 LTS, ROS 2 Humble, Gazebo
  Fortress, Nav2, NVIDIA Isaac (lightweight).
- English is the primary language for voice commands; multi-language
  support is a documented limitation, not a feature.
- Learners have internet access for downloading dependencies.
- The Docusaurus site maps each module to a top-level documentation
  section.
- OpenAI Agents / ChatKit SDK is used for the RAG chatbot frontend
  integration.
- Jetson Orin Nano (8 GB) is the baseline edge deployment target.
- The 4-module structure is non-negotiable (§11).
