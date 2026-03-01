---
sidebar_position: 2
title: "Gazebo World"
---

# Gazebo World

A Gazebo world defines the environment your robot operates in:
ground plane, walls, obstacles, lighting, and physics properties.

## SDF Format

Gazebo uses SDF (Simulation Description Format), not URDF.
SDF is a superset of URDF with support for:
- Multiple robots in one file
- Sensor plugins
- Physics engine configuration
- Lighting and atmosphere

## Our Humanoid World

The world file at `code/gazebo/worlds/humanoid_world.sdf` defines:

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="humanoid_world">

    <!-- Physics configuration -->
    <physics name="1ms" type="dart">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Scene lighting -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
          </material>
        </visual>
      </link>
    </model>

    <!-- Obstacle: box -->
    <model name="box_obstacle">
      <static>true</static>
      <pose>3 2 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><box><size>1 1 1</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>1 1 1</size></box></geometry>
          <material><ambient>0.8 0.2 0.2 1</ambient></material>
        </visual>
      </link>
    </model>

    <!-- Wall -->
    <model name="wall_1">
      <static>true</static>
      <pose>5 0 1 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><box><size>0.2 10 2</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>0.2 10 2</size></box></geometry>
          <material><ambient>0.7 0.7 0.7 1</ambient></material>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

## Physics Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `max_step_size` | 0.001 (1 ms) | Physics timestep — smaller = more accurate, slower |
| `real_time_factor` | 1.0 | 1.0 = real time, 2.0 = double speed |
| `type` | dart | Physics engine (DART is default for Fortress) |

## Launching the World

```bash
# Launch Gazebo with the world file
ign gazebo code/gazebo/worlds/humanoid_world.sdf

# Or headless (no GUI, faster for testing)
ign gazebo -s code/gazebo/worlds/humanoid_world.sdf
```

## Adding Obstacles

Static obstacles test navigation. Add them inside the `<world>` tag:

```xml
<!-- Cylinder obstacle -->
<model name="cylinder_1">
  <static>true</static>
  <pose>2 -1 0.5 0 0 0</pose>
  <link name="link">
    <collision name="collision">
      <geometry><cylinder><radius>0.3</radius><length>1.0</length></cylinder></geometry>
    </collision>
    <visual name="visual">
      <geometry><cylinder><radius>0.3</radius><length>1.0</length></cylinder></geometry>
      <material><ambient>0.2 0.6 0.2 1</ambient></material>
    </visual>
  </link>
</model>
```

## What You Built

- A complete Gazebo world with ground, lighting, obstacles, and walls
- Physics configured for humanoid simulation (1 ms timestep)
- Static obstacles for navigation testing

Next: spawn your humanoid robot into this world.
