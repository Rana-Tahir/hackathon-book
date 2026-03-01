---
sidebar_position: 3
title: "Object Detection"
---

# Object Detection

Object detection tells the robot what it sees: identifying objects
in camera images with bounding boxes, class labels, and confidence
scores.

## YOLO Overview

YOLO (You Only Look Once) processes an entire image in a single
neural network pass, making it fast enough for real-time robotics:

| Metric | YOLOv8n | YOLOv8s | YOLOv8m |
|--------|---------|---------|---------|
| Params | 3.2M | 11.2M | 25.9M |
| FPS (RTX 3080) | 300+ | 200+ | 100+ |
| FPS (Jetson Orin) | 60+ | 40+ | 20+ |
| mAP (COCO) | 37.3 | 44.9 | 50.2 |

For humanoid robotics, YOLOv8s is the sweet spot: fast enough for
real-time on Jetson, accurate enough for reliable detection.

## Installation

```bash
# Install ultralytics (YOLO)
pip install ultralytics

# Verify GPU support
python3 -c "import torch; print(torch.cuda.is_available())"
```

## ROS 2 Detection Node

```python
#!/usr/bin/env python3
"""YOLO object detection ROS 2 node."""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose
from cv_bridge import CvBridge
from ultralytics import YOLO


class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.declare_parameter('model', 'yolov8s.pt')
        self.declare_parameter('confidence_threshold', 0.5)

        model_path = self.get_parameter('model').value
        self.confidence = self.get_parameter('confidence_threshold').value

        self.model = YOLO(model_path)
        self.bridge = CvBridge()

        self.sub = self.create_subscription(
            Image, '/camera/image', self.detect_callback, 10)
        self.pub = self.create_publisher(
            Detection2DArray, '/detections', 10)

        self.get_logger().info(f'Loaded {model_path}, threshold={self.confidence}')

    def detect_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        results = self.model(cv_image, verbose=False)

        det_array = Detection2DArray()
        det_array.header = msg.header

        for result in results:
            for box in result.boxes:
                if box.conf[0] < self.confidence:
                    continue
                det = Detection2D()
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                det.bbox.center.position.x = (x1 + x2) / 2
                det.bbox.center.position.y = (y1 + y2) / 2
                det.bbox.size_x = x2 - x1
                det.bbox.size_y = y2 - y1

                hyp = ObjectHypothesisWithPose()
                hyp.hypothesis.class_id = result.names[int(box.cls[0])]
                hyp.hypothesis.score = float(box.conf[0])
                det.results.append(hyp)
                det_array.detections.append(det)

        self.pub.publish(det_array)


def main():
    rclpy.init()
    node = ObjectDetector()
    rclpy.spin(node)
    rclpy.shutdown()
```

## Testing with Isaac Sim

1. Start Isaac Sim with the warehouse scene
2. Launch the detection node
3. Place objects in the scene (cups, chairs, tables)
4. Verify detections in RViz2 or via `ros2 topic echo /detections`

```bash
# Run the detector
ros2 run perception object_detector --ros-args -p confidence_threshold:=0.5

# Check detections
ros2 topic echo /detections
```

## TensorRT Optimization

For Jetson deployment, convert to TensorRT:

```bash
# Export to TensorRT (run on target hardware)
yolo export model=yolov8s.pt format=engine device=0

# Use the TensorRT model
ros2 run perception object_detector \
  --ros-args -p model:=yolov8s.engine
```

Expected speedup: 2-3x over PyTorch inference.

## What You Built

- YOLO object detection integrated as a ROS 2 node
- Real-time detection from camera images
- TensorRT export path for Jetson deployment
- Detection results published as standard `Detection2DArray` messages

Next: Visual SLAM for localization and mapping.
