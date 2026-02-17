---
sidebar_position: 5
title: "Navigation with Nav2"
---

# Navigation with Nav2

With Visual SLAM providing pose estimates, Nav2 plans collision-free
paths and executes them while reacting to dynamic obstacles.

## Nav2 Architecture

```
              ┌───────────────┐
              │  Behavior Tree │
              │  Navigator     │
              └───────┬───────┘
         ┌────────────┼────────────┐
         ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │ Planner  │ │Controller│ │ Recovery │
   │ Server   │ │ Server   │ │ Server   │
   └────┬─────┘ └────┬─────┘ └──────────┘
        │             │
        ▼             ▼
   ┌─────────────────────┐
   │     Costmap 2D      │
   │ Global + Local      │
   └─────────────────────┘
```

## Costmap Configuration

The costmap represents obstacles as a 2D grid. Two costmaps are used:

- **Global costmap**: Full environment, for path planning
- **Local costmap**: Rolling window around robot, for reactive avoidance

### Critical Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `resolution` | 0.05 m | 5 cm cells balance detail and performance |
| `inflation_radius` | 0.55 m | Robot half-width + safety margin + arm swing |
| `cost_scaling_factor` | 3.0 | How quickly cost decays from obstacles |

## Path Planning (NavFn)

NavFn uses A* on the global costmap to find optimal paths:

```yaml
planner_server:
  ros__parameters:
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: true
      allow_unknown: false
```

## Controller (DWB)

DWB samples velocity commands and scores them for path following:

```yaml
controller_server:
  ros__parameters:
    controller_frequency: 20.0
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      max_vel_x: 0.5           # Humanoid walking speed
      max_vel_y: 0.0           # Non-holonomic
      max_vel_theta: 1.0       # rad/s turning speed
      acc_lim_x: 2.5           # Lower than wheeled robots
      sim_time: 1.7            # Longer planning horizon
```

### Humanoid-Specific Tuning

- **Lower velocities**: 0.3-0.5 m/s walking speed
- **Lower acceleration**: Bipedal locomotion cannot accelerate aggressively
- **Longer sim_time**: Humanoids turn slowly, need more look-ahead
- **Non-holonomic**: `max_vel_y: 0.0` (no sideways walking)

## Sending Navigation Goals

```python
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import math

navigator = BasicNavigator()
navigator.waitUntilNav2Active()

goal = PoseStamped()
goal.header.frame_id = 'map'
goal.pose.position.x = 3.0
goal.pose.position.y = 2.0
goal.pose.orientation.z = math.sin(1.57 / 2.0)
goal.pose.orientation.w = math.cos(1.57 / 2.0)

navigator.goToPose(goal)

while not navigator.isTaskComplete():
    feedback = navigator.getFeedback()

result = navigator.getResult()
if result == TaskResult.SUCCEEDED:
    print("Goal reached!")
```

## Success Criteria

| Metric | Target |
|--------|--------|
| Goal reach rate | 100% |
| Collision count | 0 |
| Path efficiency | Within 1.5x optimal |
| Recovery invocations | < 2 per run |

## Tuning Workflow

1. Visualize everything in RViz2 (costmaps, plans, robot footprint)
2. Identify the problem category (oscillation, corner-cutting, stuck)
3. Change one parameter at a time
4. Record metrics for each run

| Problem | Likely Fix |
|---------|-----------|
| Oscillates left-right | Increase `Oscillation.scale` |
| Cuts corners too close | Increase `BaseObstacle.scale` or `inflation_radius` |
| Stops far from goal | Decrease `xy_goal_tolerance` |
| Gets stuck in narrow passages | Decrease `inflation_radius` carefully |

## What You Built

- Nav2 configured for humanoid dynamics
- Costmaps with proper inflation for safety
- NavFn planner + DWB controller
- Programmatic goal sending
- Systematic tuning workflow

Next: bridge the gap between simulation and real hardware.
