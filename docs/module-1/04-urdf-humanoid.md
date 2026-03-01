---
sidebar_position: 4
title: Humanoid URDF
---

# Humanoid URDF

A robot's body is defined in URDF (Unified Robot Description Format) —
an XML specification that describes every link, joint, and physical
property of the robot.

## What URDF Defines

| Element | Purpose | Example |
|---------|---------|---------|
| **Link** | A rigid body with geometry, mass, and inertia | Torso, head, upper arm |
| **Joint** | A connection between two links with motion constraints | Shoulder pitch, knee bend |
| **Visual** | What the robot looks like (for rendering) | Cylinder, box, mesh |
| **Collision** | Simplified geometry for physics (often simpler than visual) | Bounding shapes |
| **Inertial** | Mass and moment of inertia (for dynamics) | Mass, ixx, iyy, izz |

## Our Humanoid: 16 Degrees of Freedom

The humanoid URDF at `code/ros2/urdf/humanoid.urdf.xacro` defines:

| Body Part | Joints | DOF |
|-----------|--------|-----|
| Head | pan, tilt | 2 |
| Left arm | shoulder pitch, shoulder roll, elbow pitch | 3 |
| Right arm | shoulder pitch, shoulder roll, elbow pitch | 3 |
| Left leg | hip pitch, hip roll, knee pitch, ankle pitch | 4 |
| Right leg | hip pitch, hip roll, knee pitch, ankle pitch | 4 |
| **Total** | | **16** |

## Xacro: Macros for URDF

Writing 16 joints by hand is repetitive. Xacro (XML macro) lets you
define reusable templates:

```xml
<xacro:macro name="arm" params="side reflect">
  <link name="${side}_upper_arm">
    <visual>
      <geometry>
        <cylinder radius="0.03" length="0.25"/>
      </geometry>
    </visual>
    <!-- collision and inertial omitted for brevity -->
  </link>

  <joint name="${side}_shoulder_pitch" type="revolute">
    <parent link="base_link"/>
    <child link="${side}_upper_arm"/>
    <origin xyz="0 ${reflect * 0.15} 0.15"/>
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="3.14" effort="20" velocity="2.0"/>
  </joint>
  <!-- elbow joint follows same pattern -->
</xacro:macro>

<!-- Instantiate both arms -->
<xacro:arm side="left" reflect="1"/>
<xacro:arm side="right" reflect="-1"/>
```

The `reflect` parameter mirrors the joint origin for left vs right.

## Converting Xacro to URDF

Xacro files must be processed before use:

```bash
# Convert xacro to plain URDF
cd ~/ros2_ws
source install/setup.bash
xacro code/ros2/urdf/humanoid.urdf.xacro > /tmp/humanoid.urdf

# Validate the URDF
check_urdf /tmp/humanoid.urdf
```

Expected output:

```text
robot name is: humanoid
---------- Successfully Parsed XML ---------------
root Link: base_link has 6 child(ren)
    child(1):  head_link
    child(2):  left_upper_arm
    child(3):  right_upper_arm
    child(4):  left_upper_leg
    child(5):  right_upper_leg
    ...
```

## Visualizing in RViz

Launch RViz with the robot model:

```bash
# Terminal 1: Publish robot description
ros2 run robot_state_publisher robot_state_publisher \
  --ros-args -p robot_description:="$(xacro code/ros2/urdf/humanoid.urdf.xacro)"

# Terminal 2: Publish joint states (interactive sliders)
ros2 run joint_state_publisher_gui joint_state_publisher_gui

# Terminal 3: Open RViz
rviz2
```

In RViz:
1. Add a **RobotModel** display
2. Set **Fixed Frame** to `base_link`
3. Move the joint sliders to see the humanoid articulate

## Joint Limits

Every joint has physical constraints defined in the URDF:

```xml
<limit lower="-1.57"    <!-- minimum angle in radians -->
       upper="1.57"     <!-- maximum angle in radians -->
       effort="20"      <!-- maximum torque in Nm -->
       velocity="2.0"/> <!-- maximum speed in rad/s -->
```

These limits are enforced by the physics engine in simulation and
by motor controllers on real hardware.

## What You Built

You now have a complete humanoid body definition:
- 16 degrees of freedom across head, arms, and legs
- Physical properties (mass, inertia) for dynamics simulation
- Collision geometry for contact detection
- Validated with `check_urdf` and visualized in RViz

Next, you will launch the entire system with a single command.
