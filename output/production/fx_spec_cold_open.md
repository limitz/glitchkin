# FX Specification — Episode 1 Cold Open
# "Luma & the Glitchkin" — Production Reference

**Document Author:** Alex Chen, Art Director
**Date:** 2026-03-29
**Version:** 1.1
**Status:** APPROVED FOR PRODUCTION
**Reference:** Density Scale Document — `fx_confetti_density_scale.md`
**Framerate:** 24fps throughout
**Compositing software:** Natron (open source). All blend mode names in this document (Screen, Add, Multiply, Normal) use Natron's terminology, which follows the industry-standard naming convention.

---

## Overview

The Episode 1 cold open establishes the show's visual language and introduces all three primary FX signatures before the audience even knows what Glitchkin are. These FX moments must land perfectly — they are the first impression of the series' visual identity. This document provides frame-by-frame FX execution specs for the three key FX sequences in the cold open.

---

## FX Moment 1 — Byte Phases Through the CRT Screen
**Scene Reference:** Panel 7 area
**Density Level:** Escalates from Level 0 → Level 2 within this sequence

---

### Story Beat Summary
Luma has just powered on Grandma Miri's old CRT monitor. The screen crackles. Something inside is pushing out. Byte phases from the digital world through the glass face of the CRT and into reality for the first time.

---

### Pre-Event Setup (Frames 1–18)
**Duration:** 18 frames (0.75 seconds)

- **Frame 1–6:** CRT screen shows only static (#0A0A14 base with #F0F0F0 scan-line noise). Density: Level 0. No confetti particles. Dead silence in the digital register.
- **Frame 7–12:** Static thickens. Scan-line spacing tightens (lines go from 6px apart to 3px apart). The static begins to show faint structure — a pattern in the noise, like a face trying to form. Color: #0A0A14 / #F0F0F0. Still no particles.
- **Frame 13–18:** The screen surface begins to bow outward — very slightly, 2–3px distortion at center — as if something is pressing from the inside. First confetti particles appear (Level 1, 3–5 particles) floating off the screen glass. They are Electric Cyan (#00F0FF) at 35% opacity. Their motion is slow and confused — they drift away from the screen surface and disperse.

---

### Phase-Through Event (Frames 19–48)
**Duration:** 30 frames (1.25 seconds) — this is the central spectacle moment

**Frame 19–22: The Surface Tension Moment**
- The screen surface bulges noticeably — the geometry of the glass distorts into a dome shape, roughly 40px diameter at composition scale.
- Color of the bulge: The glass surface takes on Electric Cyan (#00F0FF) as a specular color instead of its normal screen-glow white.
- Scan-lines on the screen surface stretch to follow the dome shape — they warp concentrically outward from the bulge point.
- Particle count jumps to Level 1+ (8–10 particles). Motion becomes directional — pulled toward the bulge point. Particles orbit the bulge center loosely.
- Faint UV Purple (#7B2FBE) halo appears at the bulge edge — a single pixel-wide glow line. 40% opacity.

**Frame 23–24: The Pop — Impact Frame**
- The screen surface shatters outward in a star-burst pattern of pixel-fragments. NOT glass — these are PIXEL TILES, each 4×4 px or 8×8 px, erupting from the screen face.
- This is the "hero frame" — hold or almost-hold here (2 frames at 24fps is perceptible as a held moment).
- Pixel tile color: Mixed Electric Cyan (#00F0FF) and Static White (#F0F0F0).
- The burst pattern is radially symmetric — NOT random. It emanates from the exact center of the bulge point in clean radial lines, like the spokes of a wheel made of pixels.
- Byte's hand/claw (or first visible body part) punches through the center of the burst. The rest of Byte is still inside the screen. Only the lead limb is visible.
- SOUND NOTE: This frame is the sync point for the "CRACK" sound effect. The visuals and the audio must be frame-accurate here.

**Frame 25–32: Byte Emerges**
- Byte pulls through the screen with fluid, momentum-driven motion. The character moves in an arc — not a straight horizontal push, but a slight upward trajectory like a person climbing out of water.
- As Byte's body crosses the screen plane, pixel tiles continue to spray outward from the breach point, trailing behind the body outline.
- Byte's body at this moment has a "phase shimmer" — every other frame, the character art has a 1–2px cyan (#00F0FF) offset duplicate at 50% opacity, shifted 2 pixels right and 1 pixel up. This creates a misregistered-print feel, indicating incomplete materialization.
- Particle count: Level 2. 18–22 particles. Full Electric Cyan and Acid Green (#39FF14) mix per the Level 2 color spec.
- The screen surface behind Byte shows a visible breach: a ragged pixel-edged hole where Byte pushed through. The hole edges glow Electric Cyan (#00F0FF) with a 4px outer glow at 60% opacity.

**Frame 33–40: Landing Arc**
- Byte is now fully clear of the screen surface. The phase shimmer begins to stabilize — the offset duplicate fades out over these 8 frames (from 50% to 0% opacity).
- Byte descends toward the desk surface, still in arc trajectory.
- The pixel tiles from the burst begin settling. Some fall toward the desk surface (gravity). Some continue drifting upward and off-screen (lighter particles ignore gravity). Some simply fade out (40% opacity → 0% over 6 frames).
- The breach hole in the CRT screen: The glowing cyan edges begin to dim. The hole is still visible but no longer emitting.

**Frame 41–48: Residual Glow**
- Byte nears the desk surface. Confetti particles: Level 1 (settling back to baseline Byte presence density).
- The CRT screen surface: The breach hole slowly fills back in with static — the pixel edges crumble inward like a healing wound in digital space. Takes approximately 8 frames for the screen to fully "heal." The scan-lines reform across the repaired surface.
- Final confetti state: 4–6 Level 1 particles floating near Byte, establishing the resting ambient of Byte's presence.

---

### Layer Order — Byte Phase-Through
(Bottom to Top)
1. Background (Grandma Miri's desk, wall, room)
2. CRT monitor body (physical object)
3. CRT screen breach glow (Electric Cyan inner glow on breach edges) — additive blend mode
4. Byte character art
5. Byte phase shimmer duplicate — screen blend mode, 50% → 0% opacity
6. Pixel tile fragments (primary burst particles) — Screen blend mode for brightest tiles
7. Confetti particles (small, ambient)
8. CRT screen glass warp distortion layer (over Byte for the portion of body still inside screen)
9. Screen static / scan-line overlay (partial, over the monitor only)

---

### Color Specifications — Phase-Through

| Element | Hex | Opacity | Blend Mode |
|---|---|---|---|
| Pixel tiles (primary) | #00F0FF | 100% | Screen |
| Pixel tiles (secondary) | #F0F0F0 | 80% | Normal |
| Breach hole edge glow | #00F0FF | 60% | Additive |
| Dimensional halo | #7B2FBE | 40% | Additive |
| Phase shimmer duplicate | #00F0FF tint | 50% → 0% | Screen |
| Confetti (Trace) | #00F0FF | 35% | Normal |
| Confetti (Presence) | #00F0FF / #39FF14 | 60% | Normal |

---

## FX Moment 2 — The Pixel Shockwave When Byte Lands
**Scene Reference:** Panel 8
**Density Level:** Level 2 → Brief Level 3 spike → Level 1 resolution

---

### Story Beat Summary
Byte lands on the desk surface. The impact is not just physical — it's the first moment Byte's full digital mass makes contact with the analog world. The desk surface responds with a pulse of glitch energy radiating outward from the landing point.

---

### Pre-Impact (Frames 1–6)
**Duration:** 6 frames (0.25 seconds)

- Byte is in descent, 3–4 inches above the desk surface.
- Shadow beneath Byte: NOT a drop shadow (those are forbidden per style guide). Instead, a cyan (#00F0FF) pulse circle, roughly 8px radius, appears on the desk surface at the projected landing point. It breathes once (grows from 6px to 10px to 8px radius) in these 6 frames, anticipating the impact like the desk "senses" what is coming.
- Confetti particles (from Phase-Through residual): Level 2, settling toward Level 1.

---

### Impact Frame (Frame 7)
**Duration:** 1 frame — this is the KEY frame

- Byte touches the desk surface.
- This single frame contains: Byte body at lowest contact position (squash pose — Byte compresses vertically ~20% for maximum impact read), AND the first frame of the shockwave ring.
- Shockwave ring: A pixel-edged circle (not smooth — the edge is made of 4×4 px blocks arranged in a circle, like a pixel-art ring) erupts from the landing point. Radius: 0 → 24px in this one frame.
- Ring color: Electric Cyan (#00F0FF). Ring width: 4px (one tile thick).
- This frame also shows a brief screen-flash: the entire frame flashes 15% brighter for 1 frame. This is the "impact bloom."

---

### Shockwave Expansion (Frames 8–18)
**Duration:** 11 frames (0.46 seconds)

**Frame 8–10: Primary Ring Expansion**
- The primary ring expands from 24px → 120px radius.
- Ring opacity: 100% at Frame 8, dropping to 70% by Frame 10.
- Ring thickness: starts at 4px, expands to 6px as it travels outward (rings thicken as they travel, then thin before vanishing — like a ripple in water).
- A second ring spawns at the landing point at Frame 9. Same specs, slightly smaller initial radius (0 → 16px). This is the "echo ring."
- Confetti BURST: 20–30 small particles (4×4 px) erupt from the landing point in all directions. These are the fastest-moving particles in the sequence — they travel at 3x normal confetti drift speed. This is the Level 3 spike moment.

**Frame 11–14: Secondary Ring and Particle Scatter**
- Primary ring: 120px → 240px. Opacity fading: 70% → 30%.
- Echo ring: 16px → 80px. Opacity: 100% → 50%.
- A third ring spawns at Frame 11. This one is NOT cyan — it is Acid Green (#39FF14). Same pixel-tile construction. This ring travels slower (20px per 2-frame beat vs. the cyan ring's 30px per 2-frame beat).
- Burst particles from the impact: Now scattering in arcing paths, decelerating. They spread across the desk surface and begin drifting upward once they lose horizontal velocity.
- The desk surface shows "digital bruising" under the landing point — a faint (20% opacity) pixel-dither circle approximately 32px radius, with #39FF14 and #00F0FF pixels alternating in a checkerboard pattern. This persists for approximately 2 seconds before fading.

**Frame 15–18: Ring Decay**
- Primary ring: Reaches 300px radius, fades to 5% opacity and disappears at Frame 17.
- Echo ring: Reaches 150px radius, fades to 0% at Frame 18.
- Green ring: Reaches 80px radius, fades to 0% at Frame 18.
- Burst particles: Now drifting freely as confetti, transitioning back to Level 2 density and behavior.

---

### Post-Impact Resolution (Frames 19–30)
**Duration:** 12 frames (0.5 seconds)

- Byte springs back up from the squash pose (stretch up) — showing the physicality of the landing.
- Confetti settles from Level 3 burst back to Level 1 over these 12 frames. Particle count: 40 → 8.
- The "digital bruise" on the desk surface fades from 20% → 0% opacity.
- Level 1 particles resume normal slow drift around Byte, establishing the resting state.

---

### Layer Order — Pixel Shockwave
(Bottom to Top)
1. Background (desk surface, environment)
2. Digital bruise (desk surface dither pattern) — Multiply blend mode
3. Shockwave rings (all three) — Additive blend mode
4. Landing anticipation circle — Additive blend mode
5. Byte character art (including squash/stretch animation)
6. Impact burst particles (fast-moving ejection phase)
7. Confetti particles (Level 1–3, transitioning)
8. Impact bloom flash (entire frame overlay, white at 15% opacity, 1 frame only)

---

### Color Specifications — Pixel Shockwave

| Element | Hex | Opacity | Blend Mode |
|---|---|---|---|
| Landing anticipation circle | #00F0FF | 60% pulse | Additive |
| Primary shockwave ring | #00F0FF | 100% → 0% | Additive |
| Echo ring | #00F0FF | 100% → 0% | Additive |
| Green ring | #39FF14 | 80% → 0% | Additive |
| Digital bruise (pixel 1) | #00F0FF | 20% → 0% | Multiply |
| Digital bruise (pixel 2) | #39FF14 | 20% → 0% | Multiply |
| Impact bloom flash | #FFFFFF | 15% (1 frame only) | Normal |
| Burst particles | #00F0FF / #39FF14 | 80% → 50% | Normal |

---

## FX Moment 3 — Monitors Flickering to Life Simultaneously
**Scene Reference:** Panels 23–24 area
**Density Level:** Level 1 (ambient) → Level 2 (at flicker peak) → Level 1 (resolution)

---

### Story Beat Summary
A later beat in the cold open. Luma (and/or Byte's influence) causes all of Grandma Miri's old monitors — multiple CRT and early LCD screens arranged across the room — to flicker on simultaneously. It's a moment of wonder, not fear: the room transforms from dim and dusty to alive with glitch light.

---

### Pre-Flicker State (Frames 1–12)
**Duration:** 12 frames (0.5 seconds) — held establishing moment

- All monitors are dead dark. Room is lit by warm practical light only (desk lamp amber #E8C95A, window light warm cream #FAF0DC).
- No confetti particles present (Level 1 Byte ambient only — 3–5 particles near Byte).
- The room reads as entirely warm-palette. This is the "before" state that makes the "after" magical.

---

### Pre-Flicker Warning (Frames 13–18)
**Duration:** 6 frames (0.25 seconds)

- A faint hum is implied visually: the dust motes near each monitor screen begin to vibrate — a micro-jitter on 2-3 small background particles near each screen (this requires adding tiny particles in those zones even before the monitors activate).
- Byte (if visible): perks up — a pose change indicating awareness, digital sense "hearing" something.
- The screens of the monitors: a faint sub-surface glow appears on 2–3 of the screens (not all) — the phosphor behind the glass warming up. Color: #0A0A14 shifting toward a very dark cyan (#001A1F). Barely perceptible. Opacity: 10–15% on the screen surface only.

---

### The Simultaneous Flicker (Frames 19–30)
**Duration:** 12 frames (0.5 seconds)

**Frame 19–21: The Sequence Begins (NOT simultaneous yet)**
- The largest/most central monitor flickers ON first — one frame of pure #F0F0F0 white-static at 100% opacity (Frame 19), then a frame of dim phosphor glow (#003A45 dark teal), then Frame 21 shows its screen resolving into rolling static (#0A0A14 with #F0F0F0 scan-line static pattern).
- CRITICAL: This first monitor triggers a cascading effect. Think of it as a chain of dominoes — the first flicker creates a pulse that causes the others.

**Frame 22–24: The Cascade**
- Frame 22: The two monitors nearest to the first one flicker ON simultaneously (both at once). Same flash pattern: 1 frame white static → settling to scan-line static.
- Frame 23: Two more monitors further out flicker ON. If there are distant/smaller monitors, they flicker here.
- Frame 24: The final remaining monitors (the smallest, the ones at the room's edges) all flicker ON simultaneously. Full room is now alive.

**Frame 25–30: The Room Transforms**
- All monitors are now displaying rolling static. The room is washed in a blue-tinted #003A45 glow from multiple directions.
- The warm ambient light is now competing with cool monitor glow. The room's color temperature shifts — this should be reflected in the background art or achieved with a cool blue-tinted overlay layer (15–25% opacity) on the full composition.
- Confetti particles: SPAWN FROM EACH MONITOR SIMULTANEOUSLY. 3–5 particles per monitor surface, drifting away from the screens. If there are 6 monitors, that's 18–30 new particles entering the scene — a Level 2 density burst across the full room.
- Particles from different monitors have slightly different drift directions, creating the sense that each screen has its own micro-field.

---

### Post-Flicker Wonder State (Frames 31–60)
**Duration:** 30 frames (1.25 seconds) — the "hold on wonder" moment

- Monitors continue rolling static but now display fragments of data — pixels that briefly resolve into shapes (a flicker of Byte's face, a fragment of code, a pixel-art smiley that vanishes before anyone's sure they saw it). These are rapid subliminal flickers, 1–2 frames each, not long enough to read clearly. The subliminal content is FOR THE AUDIENCE — Luma hasn't processed it yet.
- Confetti particles from all monitors slowly converge toward Byte over these 30 frames. The drift direction shifts — from "away from screens" to "toward Byte's position." By Frame 60, Byte is at the center of all the particle motion.
- Particle count: peaks at Level 2 (~22 particles) at Frame 31, gently declining to Level 1 (~6–8 particles) by Frame 60.
- The room's blue-tinted overlay: gradually normalizes as the eye adjusts. Fade the overlay from 20% → 8% opacity over these 30 frames. By end of shot, the room feels BOTH warm and glitch-lit — the two palettes have made peace.

---

### Screen Content Specifications (Subliminal Flashes, Frames 31–60)

Each monitor should show 1–2 subliminal flashes in this window. Total across all monitors: 6–8 distinct flicker images.

| Flicker Content | Monitor | Frame | Duration | Opacity |
|---|---|---|---|---|
| Byte's eye (isolated, close-up) | Monitor 1 (largest) | 35 | 1 frame | 60% |
| Fragment of scrolling code (#39FF14 on #0A0A14) | Monitor 3 | 40 | 2 frames | 50% |
| Pixel-art humanoid figure, waving | Monitor 2 | 44 | 1 frame | 45% |
| The word "HELP" in 8×8 pixel font | Monitor 5 (small, distant) | 48 | 1 frame | 40% |
| A map or grid — impossible to identify | Monitor 4 | 52 | 2 frames | 55% |
| Byte's full silhouette | Monitor 1 | 58 | 1 frame | 70% |

Note: The "HELP" flash on Monitor 5 is a story plant — it's visible if you're looking, easy to miss. It plants a mystery that pays off later in the season.

---

### Layer Order — Monitors Flickering to Life
(Bottom to Top)
1. Background (room art — desk, shelves, walls)
2. Monitor bodies (physical objects — screens are masked openings in this layer)
3. Monitor phosphor base glow (per-monitor layers) — Screen blend mode
4. Monitor screen static (per-monitor, within screen bounds) — Normal
5. Monitor subliminal flicker content — Normal, within screen bounds only
6. Cool blue room-wash overlay (full composition) — Multiply, 20% → 8% opacity
7. Per-monitor confetti particle emitters (confetti streams from each screen)
8. Ambient confetti particles (Byte's baseline Level 1)
9. Byte character art (if in frame)
10. Foreground objects (anything between camera and monitors that characters would pass behind)

---

### Color Specifications — Monitor Sequence

| Element | Hex | Opacity | Blend Mode |
|---|---|---|---|
| Monitor screen flash | #F0F0F0 | 100% (1 frame) | Normal |
| Monitor phosphor glow | #003A45 | 60% | Screen |
| Screen static (dark) | #0A0A14 | 100% | Normal |
| Screen static (light dots) | #F0F0F0 | 70% | Normal |
| Room-wash cool overlay | #00334D | 20% → 8% | Multiply |
| Per-monitor confetti | #00F0FF | 60% → 40% | Normal |
| Subliminal flicker content | varies (see table) | 40–70% | Normal |
| Code text (subliminal) | #39FF14 | 50% | Normal |

---

## FX Production Notes — All Three Moments

### Technical Requirements
- All confetti particles are **square** (equal width and height). No rectangles, no circles. This is absolute.
- Particles must be pixel-aligned — they snap to a 1px grid. No sub-pixel positioning. This maintains the retro-digital aesthetic.
- Particle sizes are always multiples of 2px (2px, 4px, 8px, 16px, 32px). Never odd pixel sizes like 3px or 5px.

> **Compliance confirmation (Cycle 3):** All particle sizes specified in this document comply with the 2px-multiple rule above. The conflict previously identified between this document and `fx_confetti_density_scale.md` (which formerly specified a 3×3px Level 2 minimum) has been resolved — the density scale document was corrected to 4×4px minimum in v1.1. All specs are now consistent.

### Escalation Continuity
The three FX moments form a deliberate arc within the cold open:
- Moment 1 (Phase-Through): Introduces the glitch aesthetic. Dense local FX, contained to the CRT.
- Moment 2 (Shockwave): Establishes physical impact — shows that Byte's presence has weight and consequence in the real world.
- Moment 3 (Monitors): Room-scale FX. The world itself is responding. This escalates the scope from "one object reacting" to "the environment reacting."

This arc is intentional and must be preserved. Do not reduce Moment 3 to match the scale of Moment 1.

### Sign-Off Requirement
All three FX sequences require Art Director sign-off before final render. Provide animatic with rough FX pass for review at intermediate stage.

---

*Document maintained by: Alex Chen, Art Director*
*FX Technical Lead should reference this document for all cold open work. Any deviations from spec require written approval.*
