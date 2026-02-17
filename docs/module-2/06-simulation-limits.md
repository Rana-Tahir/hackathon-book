---
sidebar_position: 6
title: "Simulation Limits"
---

# Simulation Limits

Simulation is powerful but imperfect. Every simulator makes
approximations that create gaps between simulated and real-world
behavior. Understanding these limits prevents dangerous overconfidence.

## The Sim-to-Real Gap

The sim-to-real gap is the difference between simulated and real behavior:

- **Physics**: Contact forces, friction, and deformation are simplified
- **Sensors**: Real noise is complex, not just Gaussian
- **Actuators**: Real motors have delays, backlash, and nonlinear behavior
- **Environment**: Real environments are messy and partially observable

## Physics Inaccuracies

### Contact Modeling

Real contact involves microscopic surface deformation, pressure
distribution, and stick-slip transitions. Gazebo models this as
point contacts with Coulomb friction — good enough for rigid objects
on flat surfaces, insufficient for:

- Soft contacts (rubber feet on compliant surfaces)
- Edge contacts (foot partially on a step)
- Multi-finger grasping

### Joint Modeling

Real joints have backlash (dead zone on reversal), compliance
(flex under load), and nonlinear friction. Standard Gazebo joints
are rigid constraints with constant friction.

## Sensor Noise vs. Reality

| Property | Simulation | Reality |
|----------|-----------|---------|
| Random noise | Gaussian, constant stddev | Varies with distance, angle, material |
| Bias drift | Constant or absent | Temperature-dependent, aging |
| Outliers | Not modeled | Occasional wild readings |
| Saturation | Hard clip | Nonlinear near limits |
| Time delay | Fixed | Variable, bus-dependent |

### LiDAR-Specific Gaps

- Surface reflectivity ignored (black objects absorb laser)
- Rain, fog, dust not modeled
- Motion distortion (spinning LiDAR) not simulated

### Camera-Specific Gaps

- No motion blur
- No auto-exposure
- No lens distortion (pinhole model)
- Limited dynamic range

## Actuator Modeling Gaps

Often the largest source of sim-to-real gap for humanoids:

**Command latency**: In simulation, commands apply in 1 ms. In reality,
communication bus (1-5 ms) + motor controller (1-2 ms) + current
ramp-up (5-20 ms) = 10-50 ms total delay.

**Torque limits**: Simulated motors produce any commanded torque
instantly. Real motors have current limits, back-EMF at high speeds,
and thermal derating.

## Domain Randomization Preview

The primary technique for bridging the sim-to-real gap:
instead of making simulation perfect, randomize parameters across
a wide range that includes reality.

| Parameter | Randomization Range |
|-----------|-------------------|
| Friction coefficients | 0.3 – 1.2 |
| Link masses | 80% – 120% of nominal |
| Joint damping | 50% – 200% of nominal |
| Sensor noise | 50% – 300% of nominal |
| Control delay | 0 – 20 ms |
| Ground height | -2 cm to +2 cm |

If a controller works across all variations, it should work in
reality (which is just one point in the parameter space).

## Practical Guidelines

1. **Never trust simulation blindly.** Plan for real-world testing.
2. **Calibrate your simulation.** Measure real parameters and use them.
3. **Start simple.** Get basic behaviors working first, then add noise.
4. **Track the gap.** Measure real vs. simulated behavior and improve.
5. **Budget for iteration.** Expect 3-10 sim-deploy-measure cycles.

## What You Learned

- Simulation approximates reality; it does not replicate it
- Contact, sensors, and actuators all have modeling gaps
- Domain randomization is the primary mitigation strategy
- Calibration reduces the gap; randomization covers what remains
- Always validate on real hardware before deployment
