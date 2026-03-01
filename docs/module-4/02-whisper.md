---
sidebar_position: 2
title: "Speech-to-Text with Whisper"
---

# Speech-to-Text with Whisper

Whisper converts spoken commands into text. It runs locally (no cloud
required) and supports multiple languages.

## Whisper Models

| Model | Parameters | Speed | Accuracy | VRAM |
|-------|-----------|-------|----------|------|
| tiny | 39M | 32x real-time | Basic | 1 GB |
| base | 74M | 16x real-time | Good | 1 GB |
| small | 244M | 6x real-time | Better | 2 GB |
| medium | 769M | 2x real-time | Best practical | 5 GB |

For robotics, **small** balances accuracy and latency. Use **tiny**
on Jetson if latency is critical.

## Installation

```bash
pip install openai-whisper
sudo apt install ffmpeg  # Required dependency
```

## Basic Usage

```python
import whisper

model = whisper.load_model("small")
result = model.transcribe("command.wav")
print(result["text"])
# "Go to the kitchen and pick up the red cup"
```

## ROS 2 Integration

See `code/vla/whisper_pipeline.py` for the complete ROS 2 node:

```python
class WhisperNode(Node):
    def __init__(self):
        super().__init__('whisper_node')
        self.model = whisper.load_model('small')

        self.sub = self.create_subscription(
            Audio, '/audio_raw', self.audio_callback, 10)
        self.pub = self.create_publisher(
            String, '/voice_command', 10)

    def audio_callback(self, msg):
        # Save audio to temp file
        audio_path = self.save_audio(msg)
        # Transcribe
        result = self.model.transcribe(audio_path)
        # Publish text
        text_msg = String()
        text_msg.data = result['text']
        self.pub.publish(text_msg)
```

## Handling Noise

Real robot environments are noisy (motor hum, fans, ambient sound):

- Use a directional microphone pointed at the operator
- Apply voice activity detection (VAD) before Whisper
- Set `no_speech_threshold=0.6` to reject silence hallucination
- Minimum audio duration: 1 second

## What You Built

- Whisper transcribing voice commands locally
- ROS 2 node publishing transcribed text
- Noise handling strategies for robot environments

Next: parse the transcribed text into structured action plans.
