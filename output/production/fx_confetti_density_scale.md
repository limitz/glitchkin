# FX Specification — Pixel Confetti Density Scale
# "Luma & the Glitchkin" — Production Reference

**Document Author:** Alex Chen, Art Director
**Date:** 2026-03-29
**Version:** 1.2
**Status:** APPROVED FOR PRODUCTION
**Cycle 3 Change:** Level 2 minimum particle size corrected from 3×3px to 4×4px (2px-multiple compliance).
**Cycle 4 Change:** Pipeline updated to open source stack. All FX compositing performed in Natron. Blend mode names (Screen, Add, Multiply, Normal, etc.) use Natron's terminology, which is consistent with the industry-standard naming convention.

---

## Purpose

Pixel confetti — tiny floating square particles — is the visual signature of glitch activity in *Luma & the Glitchkin*. This document establishes a formal 5-level density scale to ensure the FX department maintains a controlled escalation arc across the series. The pilot must read at Level 1–2. Levels 3 and 4 are reserved for season climaxes. **Blowing the density ceiling early destroys the show's ability to escalate visually.**

---

## The Five Levels

---

### Level 0 — NONE
**"Before Byte exists in the real world"**

#### Particle Count
Zero. No particles on screen.

#### Particle Size Range
N/A.

#### Motion Behavior
N/A. Complete stillness in the digital register. The world looks purely analog.

#### Color Mix
N/A. The real-world warm palette is uncontaminated. No glitch hues anywhere in frame.

#### When to USE
- Pre-series flashbacks showing the world before glitch energy arrives
- Establishing Grandma Miri's house before Luma boots the old CRT
- Any scene that needs to communicate: "This is normal. Nothing has changed yet."
- Cold open before Panel 7 (before Byte phases through)
- Emotional quiet scenes where the glitch world should feel absent (reunion moments, grief scenes)
- Deliberate contrast beats — cut from Level 3 back to Level 0 to reset the audience

#### When NOT to USE
- Any scene where Byte is physically present in the real world
- Any scene where Luma is aware of Glitchkin existence
- Any scene set in The Glitch Layer (even dormant areas have at least Level 1 ambience)
- After Episode 1's inciting incident — Level 0 should feel like a memory of innocence by mid-Season 1

#### Visual Notes
Background art is purely warm-palette. No Electric Cyan, Hot Magenta, Acid Green, or UV Purple anywhere in frame. Line weight on characters is fully stable — no jitter or offset. Environments feel grounded and slightly mundane.

---

### Level 1 — TRACE
**"Byte's casual, everyday presence"**

#### Particle Count
**3–8 particles** visible on screen at any one time. Often fewer than 5.

#### Particle Size Range
**2×2 px to 4×4 px** (at 1080p composition scale). These are tiny — barely visible. The audience should be able to miss them on first viewing. They reward a second watch.

#### Motion Behavior
- Slow, lazy drift. Particles move like dust motes in a sunbeam — unhurried and nearly still.
- Occasional micro-flutter: a particle may twitch one pixel in a random direction once every 8–12 frames. Not on a schedule — randomized.
- No directional pull. Particles drift in slight upward or diagonal paths, with gentle sine-wave oscillation (amplitude: 1–2 px over a 24-frame cycle).
- Particles do NOT interact with each other at this level.
- Particle lifespan: 3–6 seconds before fading out and a new one spawning at a random edge or just off Byte's body.

#### Color Mix
- **70% Electric Cyan (#00F0FF)** — Byte's primary glow color
- **30% Static White (#F0F0F0)** — neutral noise, barely visible against light backgrounds
- No Hot Magenta, no Acid Green at this level. This is calm and benign.

#### Opacity
30–50%. These should feel like afterimages, not solid shapes.

#### When to USE
- Any scene where Byte is physically present but not actively using abilities
- Byte sitting on Luma's shoulder during dialogue scenes
- Luma doing homework with Byte nearby
- Incidental background presence — Byte watching TV, napping, sulking
- Any scene communicating: "Everything is fine, but Byte is here"
- Opening and closing of episode as a visual bookend

#### When NOT to USE
- During Level 0 scenes (obviously)
- During high-action sequences — do NOT leave particle count at Level 1 during a chase; escalate to Level 2 or 3 as appropriate
- Do not use Level 1 to indicate active glitch danger — it reads as safe. If the scene is dangerous, the density level must reflect that.
- Do not use Level 1 during scenes where Byte is visibly distressed or actively using powers

---

### Level 2 — PRESENCE
**"Active glitch activity"**

#### Particle Count
**12–25 particles** on screen. Clearly visible. The audience now consciously registers that something glitchy is happening.

#### Particle Size Range
**4×4 px to 8×8 px.** Particles are now readable as deliberate graphic elements, not ambient noise. A mix of sizes should always be present — never all the same size.

> **Correction note (Cycle 3):** Minimum size corrected from 3×3px to 4×4px to comply with the production-wide rule that all particle sizes must be even-number multiples of 2px (2px, 4px, 8px, 16px, 32px). Odd pixel sizes (3px, 5px, etc.) are never permitted. See `fx_spec_cold_open.md` Technical Requirements section.

#### Motion Behavior
- Medium drift speed — roughly 2–3x Level 1's velocity.
- Particles have mild directionality: they pull toward the source of glitch activity (toward Byte, toward a glitching object, toward an active portal).
- **Pixel tumble:** Particles rotate 90 degrees on their axis occasionally (every 6–10 frames). Since they are square, this creates a subtle flip effect.
- Some particles (roughly 1 in 4) will briefly **split** — one particle becomes two half-sized particles for 2–3 frames, then one disappears.
- Particles cluster loosely around the center of activity without full directional streaming.
- Lifespan: 1.5–3 seconds. Faster turnover than Level 1, feeding a sense of ongoing activity.

#### Color Mix
- **50% Electric Cyan (#00F0FF)**
- **30% Acid Green (#39FF14)** — first appearance of this color in the particle system
- **20% Static White (#F0F0F0)**
- No Hot Magenta yet. Hot Magenta is an indicator of danger/corruption, not general activity.

#### Opacity
55–75%. Fully legible. These particles are meant to be seen.

#### When to USE
- Byte actively using a minor ability (communicating with a Glitchkin, reading digital information)
- A minor Glitchkin causing trouble in the real world (scrambling a TV signal, pixelating a photo)
- Any time Luma and the team are actively tracking or pursuing a Glitchkin
- The Glitch Layer during inactive/background conditions
- Transitional moments — entering or exiting a glitch zone
- Byte's mood is elevated but not alarmed

#### When NOT to USE
- Do not hold Level 2 for more than 60 consecutive seconds of screen time — it loses urgency
- Do not use Level 2 for scenes that should feel safe and casual (use Level 1)
- Do not use Level 2 for crisis moments — escalate to Level 3

---

### Level 3 — BREACH
**"Major glitch event"**

#### Particle Count
**40–80 particles** on screen. The screen is now actively busy with particle activity. At this density, particles become part of the composition — they must be accounted for in background staging so they don't obscure critical story information.

#### Particle Size Range
**4×4 px to 16×16 px.** Large particles now present. The scale range is critical — having both tiny (4 px) and large (16 px) particles simultaneously creates the sense of a chaotic system rather than a simple shower effect. Do not flatten to a uniform size.

#### Motion Behavior
- Fast, turbulent motion. Particles no longer drift — they move with purpose and speed.
- **Directional streaming:** Particles stream visibly toward or away from the breach point. Think of them like sparks from a welding torch.
- **Collision behavior:** Large particles that pass near each other briefly form composite shapes (L-shaped, T-shaped, irregular rectangles) for 1–2 frames before separating. This suggests a digital system struggling to maintain integrity.
- **Screen-edge splatter:** 10–15% of particles exit the frame edge and re-enter from an adjacent edge, wrapping the composition. This creates the feeling that the glitch has broken the frame boundaries.
- Particles move at 3 distinct speed layers (slow, medium, fast) creating visual depth.
- Lifespan: 0.5–1.5 seconds. Rapid spawning and despawning is part of the visual chaotic read.

#### Color Mix
- **40% Electric Cyan (#00F0FF)**
- **30% Hot Magenta (#FF2D6B)** — first significant appearance of Hot Magenta, indicating real threat
- **20% Acid Green (#39FF14)**
- **10% UV Purple (#7B2FBE)** — portal energy, suggests dimensional instability

#### Opacity
70–90%. Most particles are near-opaque. The visual noise is real.

#### Background Art Treatment
At Level 3, the real-world background palette begins to desaturate. Warm colors lose 20–30% saturation. The glitch palette begins to contaminate the environment. Scan-line overlays intensify on any electronic surfaces in frame.

#### When to USE
- A significant Glitchkin breach (multiple Glitchkin entering the real world simultaneously)
- Byte manifesting a major ability under pressure
- A dimensional border thinning (the Glitch Layer bleeding into reality)
- A villain confrontation with significant glitch-energy expenditure
- Any sequence requiring the audience to feel genuinely alarmed for the characters

#### When NOT to USE
- Do not use Level 3 for anything less than a genuine climactic beat
- Do not sustain Level 3 for more than 30 seconds without brief partial relief (a character getting to safety, a temporary containment) — sustained maximum anxiety in animation is exhausting
- Never use Level 3 in the first half of Episode 1 — it must be earned

---

### Level 4 — CHAOS
**"Climactic/Crisis Moment"**

#### Particle Count
**120–200+ particles** on screen. The particle system is now a primary visual element, not a secondary FX layer. The composition is *built around* the particle field, not the other way around.

#### Particle Size Range
**2×2 px to 32×32 px.** Full spectrum. Large particles now approach icon-size and should have recognizable shapes: pixel-skulls, corrupted letter fragments, broken interface elements. Small particles fill the gaps. The scale contrast is extreme and intentional.

#### Motion Behavior
- The system is at full chaos — no single behavioral rule dominates. Multiple behavior states occur simultaneously:
  - **Streaming:** Large particle clusters streak in one direction like a digital meteor shower
  - **Orbiting:** Medium particles orbit a central chaos point in tight ellipses
  - **Shattering:** Existing particles abruptly split into 4–8 tiny fragments
  - **Magnetism:** Small particles snap to character silhouettes and crawl along the outline (this should feel threatening — as if the system is trying to consume the characters)
- Frame-rate corruption effect: some particles visibly "drop frames" — they skip 2–3 positions instead of animating smoothly, creating a jittery, broken-system feel
- Z-depth: particles exist in clear foreground and background layers. Foreground particles are 100% opacity and large. Background particles are small and semi-transparent.

#### Color Mix
- **35% Hot Magenta (#FF2D6B)** — dominant, alarming, danger
- **25% Electric Cyan (#00F0FF)** — fighting back, Byte's energy trying to resist
- **20% Void Black (#0A0A14)** — corruption consuming light, ominous patches
- **15% Acid Green (#39FF14)**
- **5% UV Purple (#7B2FBE)** — deep dimensional tear

#### Opacity
Full range — 40% to 100% — creating layered depth. Some particles pulse opacity (breathing), suggesting a living, hungry system.

#### Background Art Treatment
- Real-world background colors are nearly fully desaturated at Level 4. The warm world is gone — everything is cold and glitch-contaminated.
- Scan-lines are heavy and visible on all surfaces.
- Architecture may show visible pixel-corruption at edges (geometry fragmenting into blocks).
- The sky, if visible, should show color banding (like a corrupted image file).

#### Sound Design Note (for reference)
Level 4 visuals should be paired with audio that includes: high-pitched digital screeching, low sub-bass rumble (digital "earthquake"), and rapid-fire glitch stutter sounds. The visual and audio chaos should feel synchronized.

#### When to USE
- Season finale climax
- A Corruption event reaching Stage 3 (see Corruption Visual Brief)
- The moment everything goes wrong and the characters have no easy solution
- Use ONCE per episode maximum. Ideally only 2–3 times per season.

#### When NOT to USE
- Do not use Level 4 for anything less than a true season-defining crisis
- Do not use Level 4 and immediately resolve the crisis in the same scene — the audience needs to feel the weight of maximum chaos before relief arrives
- **Never use Level 4 in the pilot.** The pilot maximum is Level 3, and that only briefly. The pilot should peak at Level 2 with one short Level 3 moment.
- Do not use Level 4 more than once in a single episode — it ceases to be "chaos" if the bar is reset multiple times

---

## Density Quick Reference

| Level | Name | Particle Count | Primary Colors | Max Duration Per Scene | Pilot Cap |
|---|---|---|---|---|---|
| 0 | None | 0 | — | Unlimited | Allowed |
| 1 | Trace | 3–8 | Cyan, White | Unlimited | Allowed |
| 2 | Presence | 12–25 | Cyan, Green, White | 60 sec | Allowed (preferred max) |
| 3 | Breach | 40–80 | Cyan, Magenta, Green, Purple | 30 sec | One brief moment only |
| 4 | Chaos | 120–200+ | Magenta, Cyan, Black, Green | 20 sec | NOT IN PILOT |

---

## Transition Rules

Density levels must escalate and descend with intention, not snap cuts (unless a snap cut is a story beat).

- **Escalation:** Move through levels sequentially. Do not jump from Level 1 to Level 4 in a single cut. You may skip one level (1 to 3) in a fast-cut action sequence, but it should feel like an acceleration, not a jump.
- **Descend:** After a Level 3 or 4 event, return to Level 1 (never 0 unless dramatically motivated) within 2–4 scenes. The glitch world doesn't disappear; it calms.
- **Resting state:** The series' default resting state when Byte is present is Level 1. This is the baseline from which all drama escalates.

---

*Document maintained by: Alex Chen, Art Director*
*For questions about density scale application to specific scenes, bring to the Art Director for review before animating.*
