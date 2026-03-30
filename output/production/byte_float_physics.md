<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Character Spec — Byte Float Physics
# "Luma & the Glitchkin" — Production Reference

**Document Author:** Alex Chen, Art Director
**Date:** 2026-03-29
**Version:** 1.0
**Status:** APPROVED FOR PRODUCTION
**Applies to:** Byte (primary), and any future creature-class characters with hover locomotion

---

## Overview

Byte does not walk. Byte does not float like a balloon. Byte *hovers* — a sinusoidal, rhythmic levitation that feels like a living system maintaining itself against gravity. Every aspect of Byte's movement must communicate that something intelligent and slightly grudging is in control of this body.

This document specifies the physics and animation rules governing Byte's hover behavior under all conditions. Animators must internalize these rules before roughing Byte in any scene. A Byte that moves like a camera dolly is a production error.

---

## 1. Float Type

**Sinusoidal hover. Not linear drift.**

The distinction is critical:
- **Linear drift** = constant velocity, mechanical, dead. This reads as a prop being moved on a wire.
- **Sinusoidal hover** = smooth oscillation with acceleration and deceleration at the extremes. This reads as alive.

The hover is a continuous sine wave applied to Byte's vertical position. The body gently rises and falls in a smooth curve — never a flat hold, never an abrupt bounce. The oscillation is always present, even when Byte is stationary and at rest.

---

## 2. Default Hover Specifications (At Rest / Standard Scale)

### Hover Height
- **Resting hover:** 1–3px above the surface contact point (at 1080p composition scale, standard character scale)
- "Surface contact point" = the implied position where Byte's underside would touch a surface if gravity applied fully
- Byte never fully settles onto a surface during normal hover — there is always a gap

### Oscillation Parameters
| Parameter | Value |
|---|---|
| Vertical range | 0.5-inch equivalent (at standard character scale) — approximately 4–6px at 1080p |
| Cycle duration | 24 frames (1 second at 24fps) |
| Waveform | Sine — smooth ease in and out at top and bottom of arc |
| Direction | Pure vertical (Y-axis only) during idle state |

### At-Rest Behavior Summary
Byte, at rest, moves through a continuous 4–6px vertical sine wave, completing one full cycle per second. The motion never stops. Even in a held dialogue pose, the body is gently rising and falling. This is Byte's heartbeat.

---

## 3. Under Acceleration

When Byte initiates movement (begins traveling horizontally):

### Hover Height Change
- Hover height increases by **1–2px above resting baseline** during active acceleration
- The body lifts slightly, as if the propulsion system is drawing more energy
- Height increase is gradual — it occurs over the first 8 frames of acceleration, not instantaneously

### Oscillation Frequency Change
- Oscillation frequency **doubles** during acceleration: cycle compresses from 24 frames to **12 frames** (2 complete cycles per second)
- The body oscillates faster but the amplitude stays consistent — it is the speed of the sine wave that changes, not its height
- This creates the read of "engines revving" without breaking the hover aesthetic

### Return to Baseline
When acceleration ends and Byte reaches cruising speed, oscillation frequency eases back to 24-frame cycle over 8–12 frames.

---

## 4. Stopping Behavior

When Byte decelerates to a stop:

### Overshoot
- Byte **overshoots the target position by 4 frames** — meaning the body carries past the intended stop point
- The overshoot distance is small: approximately 4–8px horizontal at standard scale, proportional to approach velocity
- The overshoot is in the same direction as the direction of travel — inertia, not a bounce

### Recovery (Damped Return)
- Over the following **8 frames**, Byte eases back to the target position
- The return is **damped** — it does not overshoot again in the opposite direction. One overshoot, one smooth return.
- By frame 12 after the stop command, Byte should be settled at the target position (within 1px)
- Oscillation frequency during the damped return: eases from 12-frame cycle back to 24-frame cycle as the body settles

---

## 5. Impact Landing

When Byte is forced fully onto a surface (a landing, a slam, a deliberate sit-down — any moment where hover is interrupted by contact):

### Compression
- On contact, Byte's body **compresses vertically by 10%** of its standard height
- The compression is instantaneous — it happens in Frame 1 of contact
- Horizontal width does NOT compensate (this is not a traditional squash-and-stretch bounce — it is a compression of the body geometry itself, consistent with Byte's rigid-but-digital nature)

### Hold
- Compressed state holds for **2 frames**

### Spring Back
- Over **4 frames**, the body returns to standard proportions
- The return is a spring curve — fast at first, easing to normal by frame 4
- After spring-back, Byte immediately resumes the sinusoidal hover (if the surface is below, Byte lifts back to hover height; if the surface is a shoulder or platform, Byte settles at hover height above it)

### Impact Note
Impact landings pair with the pixel shockwave FX (see `fx_spec_cold_open.md`, FX Moment 2 for the canonical execution spec). The compression hold aligns with the shockwave's impact frame.

---

## 6. Direction Changes

When Byte changes horizontal travel direction:

### Anticipation Lean
- Before moving in a new direction, Byte **leans 2 frames in the opposite direction** — a brief anticipation
- "Lean" = a slight skew of the body geometry in the direction opposite to intended travel. Approximately 5–8 degrees of tilt.
- This is not a large cartoony wind-up — it is a subtle, quick lean that reads subliminally as preparation

### Move
- After the 2-frame anticipation, Byte moves in the new direction with normal acceleration behavior (oscillation frequency rises as described in Section 3)

### Why This Rule Exists
Byte moving without anticipation reads as a camera repositioning. The anticipation lean tells the audience that Byte *decided* to move. There is intent behind the motion. This is the difference between a prop and a character.

---

## 7. Emotional State Modifiers

Byte's hover physics reflect Byte's emotional state. Animators must read the scene and apply the appropriate modifier. These are not rigid rules — they are parameters to operate within.

### Agitated / Irritated / Stressed
- **Oscillation:** Faster than baseline. Cycle drops to 16–18 frames (between rest and acceleration)
- **Regularity:** Irregular — the sine wave has micro-variations. The amplitude fluctuates ±1–2px unpredictably. It should feel like a signal with interference.
- **Hover height:** Slightly elevated (1–2px above standard baseline)
- **Visual read:** Byte is buzzing. The hover feels unstable, impatient.

### Calm / Content / Focused
- **Oscillation:** Slower than baseline. Cycle expands to 32–36 frames (slower than 1-second default)
- **Regularity:** Very regular. The sine wave is clean, consistent, almost hypnotic.
- **Hover height:** Standard or very slightly below standard
- **Visual read:** Byte is settled. This is rare enough that when it appears, audiences should notice.

### Disgusted / Reluctant / Annoyed-But-Resigned
- **Oscillation:** Slower than baseline, similar to Calm but stiffer
- **Hover height:** **Lower** than standard — 0–1px above surface (closer to touching down, as if Byte is barely bothering to stay aloft)
- **Regularity:** Flat and slow — the wave is compressed vertically. The oscillation range shrinks to 2–3px instead of the standard 4–6px.
- **Visual read:** Byte is dragging. The hover looks like it has given up on being impressive.

### Excited / Surprised / Alarmed
- **Oscillation:** Much faster than baseline. Cycle drops to 8–10 frames (very rapid)
- **Regularity:** Erratic — the amplitude spikes. The body may jump 8–10px vertically in a single oscillation before calming. Irregular timing between peaks.
- **Hover height:** Higher than standard — 4–6px above baseline, with spikes higher
- **Visual read:** Byte is charged. The system is overclocking. This is Byte losing composure, even if the face doesn't show it.

---

## 8. Interaction with Luma's Shoulder

When Byte rides on Luma's shoulder (the show's primary "passenger" configuration):

- Byte's hover physics still apply — Byte does not simply sit flat on the shoulder
- The "surface contact point" is the top of Luma's shoulder; Byte hovers 1–3px above it
- Byte's oscillation adds micro-movement on top of Luma's walk cycle — the two motions compound
- Animators must ensure the combined motion reads as Byte hovering ON Luma rather than Byte being stuck to Luma. The hover independence should be visible.
- During fast action (running, jumping): Byte's oscillation frequency rises to match the energy of Luma's movement (applies Acceleration rules even though Byte isn't self-propelling)

---

## 9. What to Avoid

- **Never hold Byte in a perfect static position.** Even in close-up reaction shots, some oscillation must be present.
- **Never use linear ease on the vertical oscillation.** It must be a sine curve. Linear = mechanical = wrong.
- **Never skip the anticipation lean on direction changes.** It is required, even if subtle.
- **Never apply squash-and-stretch to the hover oscillation.** The body shape changes only on impact landings (Section 5), not during normal hover.
- **Never animate the hover on twos for the oscillation itself.** The sine wave should be on ones — smooth sub-frame variation is acceptable. Stepping the oscillation makes it look like a bobbing toy, not a living system.

---

## Reference Principle

Every decision in this document serves one goal: **Byte must feel like a living system, not a moved object.**

When in doubt, ask: does this motion look like someone decided to make it happen, or does it look like a physics simulation running on an entity that has opinions?

It should look like the latter.

---

*Document maintained by: Alex Chen, Art Director*
*Float physics questions: bring to Art Director before roughing, not after. Fixing physics in cleanup is expensive.*
