---
sidebar_position: 5
title: "Multi-Modal Perception"
---

# Multi-Modal Perception

An LLM planning without visual grounding is planning in a fantasy
world. This chapter connects perception (what the robot sees) to
language planning (what the robot should do).

## Vision + Language Integration

```
Camera ──► YOLO Detector ──► Detections ──► Scene Description ──► LLM Context
```

Object detections are converted to a natural language scene description
injected into the LLM prompt:

```
CURRENT SCENE:
I see a red cup on a brown table at position (1.2, 0.5, 0.8) with 94%
confidence. There is a black chair at (0.8, -0.3, 0.4).
The table is directly ahead at 1.0 meters.
```

## Scene Description Generator

```python
def generate_scene_description(detections, robot_pose):
    """Convert object detections to natural language."""
    if not detections:
        return "No objects detected in the current view."

    lines = []
    for det in detections:
        distance = compute_distance(robot_pose, det["position"])
        direction = compute_direction(robot_pose, det["position"])
        lines.append(
            f"- {det['color']} {det['class']} at {distance:.1f}m "
            f"to my {direction} ({det['confidence']*100:.0f}% confidence)"
        )

    return "Objects in view:\n" + "\n".join(lines)
```

## Grounding Validation

Before executing an action, verify the referenced objects exist:

```python
def verify_object_exists(target, detections, max_age=5.0):
    """Check if the target object is in recent detections."""
    for det in detections:
        if det["age"] > max_age:
            continue
        if matches(target, det["class"], det.get("color")):
            return True, det
    return False, None
```

If the object is not in the scene:
1. Report "I don't see that object"
2. Navigate to get a better vantage point
3. Re-scan and retry

## Depth-Informed Localization

RGB detects objects in 2D. Depth camera provides 3D positions:

```python
def pixel_to_world(px, py, depth, intrinsics, camera_tf):
    """Convert 2D pixel + depth to 3D world coordinates."""
    fx, fy, cx, cy = intrinsics
    cam_x = (px - cx) * depth / fx
    cam_y = (py - cy) * depth / fy
    cam_z = depth
    point_cam = np.array([cam_x, cam_y, cam_z, 1.0])
    point_world = camera_tf @ point_cam
    return point_world[:3]
```

## Sensor Fusion

| Sensor | Contribution |
|--------|-------------|
| RGB camera | Object detection, color |
| Depth camera | 3D positions, obstacle detection |
| LiDAR | Mapping, localization |
| IMU | Balance state, fall detection |
| Joint encoders | Current pose, workspace limits |
| Microphone | Voice commands |

When sensors disagree, **conservative wins**: if any sensor suggests
an obstacle, treat it as an obstacle.

## Stale Data Handling

Every piece of sensor data has a timestamp. Discard stale data:

| Data Type | Max Age |
|-----------|---------|
| Object detections | 5 seconds |
| Occupancy grid | 2 seconds |
| Robot state | 0.1 seconds |

If critical data is stale, pause and re-scan before continuing.

## What You Built

- Scene description bridging perception and language planning
- Grounding validation checking LLM plans against reality
- 3D object localization from RGB + depth fusion
- Sensor fusion with conservative conflict resolution
- Stale data handling for real-time operation
