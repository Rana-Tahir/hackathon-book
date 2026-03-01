#!/usr/bin/env python3
"""Whisper speech-to-text pipeline for humanoid voice commands.

Module 4, Artifact A-013

Subscribes to raw audio, transcribes with OpenAI Whisper,
and publishes the transcribed text for downstream processing.

Usage:
    ros2 run vla whisper_pipeline --ros-args -p model_size:=small
"""

import tempfile
import time

import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    import whisper
except ImportError:
    whisper = None


class WhisperPipeline(Node):
    """ROS 2 node for speech-to-text using OpenAI Whisper."""

    # Minimum audio energy to attempt transcription (skip silence)
    MIN_ENERGY_THRESHOLD = 0.01

    def __init__(self):
        super().__init__('whisper_pipeline')

        # Parameters
        self.declare_parameter('model_size', 'small')
        self.declare_parameter('language', 'en')
        self.declare_parameter('no_speech_threshold', 0.6)

        model_size = self.get_parameter('model_size').value
        self.language = self.get_parameter('language').value
        self.no_speech_threshold = self.get_parameter('no_speech_threshold').value

        # Load Whisper model
        if whisper is None:
            self.get_logger().error(
                'openai-whisper not installed. Run: pip install openai-whisper')
            raise RuntimeError('whisper not available')

        self.get_logger().info(f'Loading Whisper model: {model_size}...')
        self.model = whisper.load_model(model_size)
        self.get_logger().info('Whisper model loaded.')

        # Publishers and subscribers
        self.text_pub = self.create_publisher(String, '/voice_command', 10)

        # For file-based input (simpler than raw audio streaming)
        self.file_sub = self.create_subscription(
            String, '/audio_file_path', self.file_callback, 10)

        self.get_logger().info('WhisperPipeline ready. Listening on /audio_file_path')

    def file_callback(self, msg: String):
        """Transcribe an audio file and publish the result."""
        audio_path = msg.data
        self.get_logger().info(f'Transcribing: {audio_path}')

        t_start = time.time()

        try:
            result = self.model.transcribe(
                audio_path,
                language=self.language,
                no_speech_threshold=self.no_speech_threshold,
            )
        except Exception as e:
            self.get_logger().error(f'Transcription failed: {e}')
            return

        t_end = time.time()
        text = result['text'].strip()
        duration_ms = (t_end - t_start) * 1000

        if not text:
            self.get_logger().warn('Empty transcription (silence or noise)')
            return

        self.get_logger().info(
            f'Transcribed in {duration_ms:.0f}ms: "{text}"')

        # Publish
        out = String()
        out.data = text
        self.text_pub.publish(out)

    def transcribe_audio(self, audio_path: str) -> dict:
        """Direct transcription interface (non-ROS).

        Args:
            audio_path: Path to audio file (WAV, MP3, etc.)

        Returns:
            dict with 'text', 'language', and 'segments' keys
        """
        result = self.model.transcribe(
            audio_path,
            language=self.language,
            no_speech_threshold=self.no_speech_threshold,
        )
        return {
            'text': result['text'].strip(),
            'language': result.get('language', self.language),
            'segments': result.get('segments', []),
        }


def main(args=None):
    rclpy.init(args=args)
    node = WhisperPipeline()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
