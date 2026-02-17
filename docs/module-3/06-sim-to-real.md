---
sidebar_position: 6
title: "Sim-to-Real Transfer"
---

# Sim-to-Real Transfer

The sim-to-real gap is the difference between how your robot performs
in simulation versus the real world. Bridging this gap is one of the
hardest problems in robotics.

## Sources of the Gap

| Source | Simulation | Reality |
|--------|-----------|---------|
| Physics | Rigid body, simplified contact | Deformable, complex friction |
| Sensors | Gaussian noise | Complex, environment-dependent |
| Actuators | Instant response | Latency, backlash, thermal limits |
| Environment | Clean, known | Messy, partially observable |
| Timing | Deterministic | Variable latency, jitter |

## Domain Randomization

The primary mitigation technique: randomize simulation parameters
so the trained controller is robust to the full range of conditions.

### What to Randomize

```python
# Example domain randomization configuration
randomization = {
    'friction': {'min': 0.3, 'max': 1.2},
    'link_mass_scale': {'min': 0.8, 'max': 1.2},
    'joint_damping_scale': {'min': 0.5, 'max': 2.0},
    'sensor_noise_scale': {'min': 0.5, 'max': 3.0},
    'control_delay_ms': {'min': 0, 'max': 20},
    'gravity_z': {'min': -9.9, 'max': -9.7},
    'ground_height_offset': {'min': -0.02, 'max': 0.02},
}
```

### Implementation in Isaac Sim

Isaac Sim's Replicator API supports domain randomization natively:

```python
import omni.replicator.core as rep

with rep.trigger.on_frame():
    # Randomize lighting
    rep.modify.attribute(
        light, 'intensity',
        rep.distribution.uniform(500, 3000))

    # Randomize material color
    rep.randomizer.color(
        surfaces, colors=rep.distribution.uniform((0,0,0), (1,1,1)))

    # Randomize object positions
    rep.randomizer.scatter_3d(
        objects, surface=table,
        check_for_collisions=True)
```

## System Identification

Before randomization, calibrate your simulation to match reality
as closely as possible:

1. **Measure real parameters**: friction, mass, inertia, motor response
2. **Set simulation parameters** to measured values
3. **Compare behaviors**: Run the same motion in sim and real
4. **Adjust** until nominal simulation is close to reality
5. **Then add randomization** to cover remaining uncertainty

## Transfer Workflow

```
1. Train in simulation (domain randomized)
2. Validate in simulation (nominal parameters)
3. Deploy to hardware (start with slow/safe motions)
4. Measure performance gap
5. Adjust simulation parameters
6. Repeat 1-5 (expect 3-10 cycles)
```

## Perception Transfer

Visual models trained on synthetic data often fail on real images due to:

- **Appearance gap**: Rendered textures differ from real materials
- **Lighting gap**: Simulation lighting is simpler than real-world
- **Background gap**: Real backgrounds are more cluttered

Mitigations:
- Train on both synthetic and real images (mixed dataset)
- Use domain randomization for textures, lighting, backgrounds
- Fine-tune on a small real-world dataset

## What You Learned

- The sim-to-real gap affects physics, sensors, actuators, and perception
- Domain randomization makes controllers robust to parameter uncertainty
- System identification reduces the gap before randomization
- Transfer is iterative: expect multiple sim-real cycles
- Perception transfer requires visual domain randomization
