---
sidebar_position: 6
title: "Debugging VLA"
---

# Debugging VLA

VLA pipelines have multiple failure modes across four subsystems.
When the robot does not do what you expect, find which stage failed.

## Diagnostic Protocol

Work backwards from the output:

```
1. Did ROS 2 receive action goals? → Check action servers
2. Did the safety filter pass? → Check rejection log
3. Did the LLM produce valid JSON? → Check intent parser output
4. Did Whisper transcribe correctly? → Check transcription log
```

## Whisper Failures

| Issue | Cause | Fix |
|-------|-------|-----|
| No output | Silent audio / ffmpeg missing | Check mic; `apt install ffmpeg` |
| Wrong words | Background noise / wrong model | Use directional mic; try `medium` model |
| Hallucinated text | Silence input | Add VAD preprocessing |
| Slow transcription | CPU-only inference | Use GPU; try `tiny` model |

## LLM Failures

| Issue | Cause | Fix |
|-------|-------|-----|
| Invalid JSON | Markdown fences in output | Strip fences in post-processing |
| Wrong intent | Insufficient examples | Add few-shot examples to prompt |
| Hallucinated actions | Weak constraints | Strengthen system prompt |
| High latency | Large model | Use smaller model or local inference |

## Safety Filter False Positives

| Issue | Fix |
|-------|-----|
| Confidence too strict | Lower threshold (not below 0.5) |
| Bounds too tight | Measure environment, expand workspace |
| Rate limit too aggressive | Reduce min_interval |
| Missing action type | Add to whitelist after review |

## ROS 2 Action Errors

| Issue | Cause | Fix |
|-------|-------|-----|
| Server not found | Node not running | Check `ros2 action list` |
| Goal rejected | Invalid parameters | Validate coordinates, check TF |
| No motion | Goal = current position | Verify translator output |
| Oscillation | Goal tolerance too tight | Increase `goal_tolerance` |

## End-to-End Checklist

- [ ] Audio capture: `/audio_raw` has data
- [ ] Whisper: Transcription matches spoken words
- [ ] LLM: Valid JSON with correct intent
- [ ] Safety: Plan passes all 5 stages
- [ ] ROS 2: Action goals accepted
- [ ] Motion: Joint commands publishing
- [ ] Simulation: Gazebo running, clock advancing
- [ ] Transforms: TF tree complete

## Logging Best Practices

Log at every stage with structured fields:

```python
logger.info("WHISPER: text='%s' confidence=%.2f", text, conf)
logger.info("LLM: intent=%s actions=%d", intent, len(actions))
logger.info("SAFETY: passed=%s rejections=%s", passed, rejections)
logger.info("ROS2: goal=%s server=%s", goal, server)
```

## Performance Profiling

```python
import time
t0 = time.time()
transcription = whisper.transcribe(audio)
t1 = time.time()
intent = parser.parse(transcription)
t2 = time.time()
is_safe, _, reasons = safety.validate(intent)
t3 = time.time()
logger.info("TIMING: whisper=%.0fms llm=%.0fms safety=%.0fms",
            (t1-t0)*1000, (t2-t1)*1000, (t3-t2)*1000)
```

## What You Learned

- Diagnose by working backwards from output
- Whisper failures: environmental (noise, ffmpeg)
- LLM failures: prompt-related (constraints, examples)
- Safety filter: threshold-related (too strict)
- ROS 2 failures: configuration-related (servers, frames)
- Structured logging at every stage is essential
