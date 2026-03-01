---
slug: /
sidebar_position: 1
title: Physical AI & Humanoid Robotics
---

# Physical AI & Humanoid Robotics

**Embodied Intelligence in the Physical World**

Build, simulate, and deploy autonomous humanoid robots that see, think,
speak, and act in physically realistic environments.

## What You Will Build

By the end of this book, you will have constructed a complete autonomous
humanoid system that:

- Receives a voice command from a human operator
- Interprets intent using a large language model
- Plans actions through a robotic middleware layer
- Navigates obstacles in a simulated environment
- Identifies objects using computer vision
- Manipulates or interacts with physical objects

All validated in simulation before any real-world deployment.

## Modules

| Module | Title | Focus |
|--------|-------|-------|
| 1 | [The Robotic Nervous System](module-1/introduction) | ROS 2 middleware for robot control |
| 2 | [The Digital Twin](module-2/introduction) | Gazebo simulation |
| 3 | [The AI-Robot Brain](module-3/introduction) | NVIDIA Isaac perception & navigation |
| 4 | [Vision-Language-Action](module-4/introduction) | LLM-driven robotic cognition |
| Capstone | [The Autonomous Humanoid](capstone/integration) | End-to-end integration |

## Prerequisites

- **Python** programming experience
- **Linux** (Ubuntu 22.04) command-line familiarity
- **Basic AI/ML** understanding (what a neural network is, what training means)

No prior ROS or robotics hardware experience is required.

## Hardware Requirements

| Profile | GPU | VRAM | RAM | Use |
|---------|-----|------|-----|-----|
| Workstation (minimum) | RTX 3060 | 8 GB | 32 GB | Modules 1–2 |
| Workstation (recommended) | RTX 4070+ | 12+ GB | 64 GB | All modules |
| Edge deployment | Jetson Orin NX 16 GB | shared | 16 GB | Module 3 deployment |

See the [Prerequisites](appendix/prerequisites) appendix for full setup
instructions and [Cloud Alternatives](appendix/cloud-alternatives) if you
do not have RTX hardware.

## AI Book Assistant

This book includes a built-in **RAG chatbot** powered by the book's own
content. Click the chat button in the bottom-right corner to:

- Ask questions about any topic covered in the book
- **Select text** on any page and click "Ask about this" for context-specific answers
- Get source citations linking back to the relevant chapter and section

The assistant only answers from book content — no hallucinated information.

## Getting Started

1. Start with the [Prerequisites](appendix/prerequisites) to set up your environment
2. Follow Module 1 through Module 4 in order — each builds on the previous
3. Complete the [Capstone](capstone/integration) to integrate everything end-to-end
4. Use the AI Assistant anytime you need help understanding a concept

## Principles

This book follows a **simulation-first** approach. Every behavior is
validated in a digital twin before deployment. **Safety overrides
intelligence** — all autonomous actions pass through safety filters.
Content is **artifact-first** — working code is demonstrated before
explanation.
