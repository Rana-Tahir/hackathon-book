---
sidebar_position: 1
title: "Introduction to VLA"
---

# Introduction to Vision-Language-Action

Module 4 connects a language model to the robot's perception and
action systems. The result: a humanoid robot that understands
spoken commands, reasons about its environment, and executes
safe physical actions.

## The VLA Pipeline

```
Voice ──► Whisper ──► Text ──► LLM ──► Action Plan ──► Safety Filter ──► ROS 2
                                ▲
                          Scene Description
                                ▲
                        Object Detection (YOLO)
```

Each stage has a clear input, output, and failure mode.

## Why VLA?

Traditional robot programming requires explicit commands:
```
navigate_to(x=3.0, y=2.0)
pick_up("cup")
```

VLA allows natural language:
```
"Go to the kitchen table and bring me the red cup"
```

The LLM translates natural language into structured action plans
that the safety filter validates before execution.

## Safety Architecture

The LLM never directly controls the robot. Every action plan
passes through a safety filter that enforces:

- **Action whitelist**: Only allowed action types (navigate, detect, interact, stop, speak)
- **Physical bounds**: Navigation distances, velocities within limits
- **Confidence threshold**: LLM must be sufficiently confident
- **Rate limiting**: Maximum command frequency
- **Emergency override**: "Stop" always bypasses the LLM

```
LLM ──► Safety Filter ──► ROS 2 Actions
         ▲
         │ REJECT if unsafe
         │ Log rejection reason
```

## Module 4 Roadmap

| Chapter | Topic |
|---------|-------|
| 2 | Whisper speech-to-text |
| 3 | LLM intent parsing |
| 4 | Safety filter |
| 5 | Multi-modal perception |
| 6 | Debugging VLA |

## Prerequisites

- Module 3 complete (perception and navigation working)
- Python 3.10 with PyTorch
- OpenAI Whisper (`pip install openai-whisper`)
- An LLM (local or API-based)

## What You Will Build

By the end of Module 4:
- Voice commands transcribed to text via Whisper
- LLM parsing commands into structured action plans
- Safety filter validating every action before execution
- Multi-modal perception grounding LLM outputs in visual reality
- Complete VLA pipeline from voice to robot motion
