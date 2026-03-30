<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Staging Brief — Cold Open P07 and P09
**Author:** Lee Tanaka, Character Staging & Visual Acting Specialist
**Date:** 2026-03-30
**For:** Diego Vargas
**Cycle:** 42

---

## P07 — Monitor Bulging / Dutch Tilt 8° CW / Byte Phases Through

### Beat Description
The moment before Byte crosses from the Glitch world into the real world. The CRT monitor is under physical pressure from the inside. Dutch tilt signals: the rules of the room are about to break.

### Camera
- **Shot type:** MED WIDE
- **Angle:** Low angle (camera at floor level, looking slightly up)
- **Dutch tilt:** 8° clockwise — applied to the entire draw area (not individual elements). Use `draw_area.rotate(-8, expand=False, fillcolor=DEEP_SPACE)` then paste back. Caption bar stays horizontal.
- **Focal point:** Monitor, center-right frame. Characters frame-left are secondary.

### Monitor (hero element)
- The monitor face BOWS OUTWARD — convex distortion visible as a curved rectangle. The bezel edge should show stress lines (2–3 thin cracks radiating from lower-left corner of screen face).
- Screen surface: white-hot center (overpressure luminance peak), distortion rings breaking OUTSIDE the bezel boundary. The screen is about to lose containment — rings that stay inside the bezel read as "effect," rings that break the boundary read as "physics violation / danger."
- Screen color: ELEC_CYAN dominant, white-hot center, edges showing VOID_BLACK vacuum zones.
- The monitor should fill ~40–45% of frame width, positioned at 55–65% x (camera-right of center).

### Byte (partially phased)
- Byte is caught mid-phase. His lower half is still inside the screen (ELEC_CYAN, slightly transparent / desaturated), his upper body and face are emerging into the real world (teal body color, pixel confetti preceding him).
- Expression: **DETERMINED + ALARMED** — eyes wide, slight open-mouth pixel shape. This is effortful. He is not gliding through — he is pushing through a membrane.
- Body geometry at mid-phase: lower half treated as if behind glass (reduced opacity 50–60%); upper half full opacity with a pixel confetti burst at the screen boundary (the crossing threshold).
- Position: center-frame to camera-right. His emergence creates a spatial anchor.

### Room (context)
- Room visuals at this point are already contaminated: ELEC_CYAN light is bleeding from multiple monitors (not just the hero one). Warm domestic light is on the losing side — visible on the far-left margin only.
- Any visible furniture in frame should read at low angle: table edge at bottom, cable bundles at floor level.

### Staging Notes
- **Dutch tilt = maximum perceptual disruption.** At 8°, the floor line is no longer horizontal. This signals to the audience: the room's geometry cannot be trusted. It is the spatial equivalent of a dramatic chord.
- **Byte's emergence directionality.** His body vector should be slightly upward (he is rising as he comes through). Not straight horizontal. The confetti trail at the screen boundary shows entry angle.
- **Low angle strengthens Byte's physical presence.** Even though he is tiny, a floor-level camera looking up means his head breaks the upper horizon — he reads as occupying vertical space.

### Key Geometry (suggested)
- PW=800, DRAW_H=540 (standard)
- Monitor center: (int(PW*0.60), int(DRAW_H*0.42))
- Monitor face bow: ellipse from (int(PW*0.42), int(DRAW_H*0.22)) to (int(PW*0.80), int(DRAW_H*0.72)) — slightly wider than tall to show forward bow
- Byte body center: (int(PW*0.57), int(DRAW_H*0.45)) — emerging from screen center
- Floor line (low angle): y = int(DRAW_H * 0.78) on untilted canvas, will shift post-tilt

### Arc Label
**TENSE → BREACH** — arc color: Hot Magenta (`(255, 45, 107)`)

---

## P09 — Byte Floating / Spots Luma / Cautious Approach Begins

### Beat Description
First beat after Byte is fully in the real world. He floats 18 inches off the floor, scanning the room. He spots Luma on the couch — first eye contact (or one-sided eye contact, since Luma is still asleep). His posture shifts from scan mode to cautious approach.

This beat has TWO emotional temperatures in sequence within a single panel:
1. **SCANNING** — head turning, cracked eye actively processing, normal eye semi-closed (relaxed scan, not alarm)
2. **SPOTTED** — moment his scan lands on Luma, expression shifts to a heightened state (curious + cautious, NOT threatening)

If it's too complex to show both in a single image, choose the **SPOTTED** moment — it's more narratively useful.

### Camera
- **Shot type:** MED WIDE
- **Angle:** Slightly elevated — camera at 4–5 feet height (above floor level but below Byte's floating position). This puts Byte at eye level or slightly above camera, and Luma on the couch at the same horizontal band.
- **Dutch tilt:** NONE. The room geometry has reasserted after P07's disruption. A flat horizon here signals the world has stabilized into a new (strange) normal.
- **Composition:** Byte in frame-right (floating), couch / Luma form in frame-left background. Both must be visible but Byte is the active element (foreground, larger).

### Byte (active element, frame-right)
- **Floating height:** Visible distance between feet and floor. Floor recedes in perspective below him. Pixel confetti drifting downward beneath him (gravity ghost — the confetti still falls even though Byte doesn't).
- **Cracked eye state:** SEARCHING / PROCESSING. Cyan + magenta alternating pixel dots (3 dots each). Eye aperture wide.
- **Normal eye state:** Wide open, iris shifted LEFT (toward Luma / toward frame-left). This is the sight-line. The pupil MUST shift left — centered pupils mean he's looking at the audience.
- **Body posture (SPOTTED):** Slight lean forward (body_tilt = -2 to -3°) — not alarm lean, curiosity lean. Arms at mid-position (not raised, not tucked). Head cocked 5–8° toward Luma.
- **Glow state:** Desaturation ring fully established at his feet on the floor plane (digital nature bleaches the analogue surface). ELEC_CYAN ambient glow around body — not directional yet (he hasn't committed toward Luma).

### Luma (context element, frame-left background)
- Luma is ASLEEP on the couch. She does not know Byte is there yet.
- Background-scale: smaller than Byte (depth reads). Warm skin tones, orange hoodie visible. Couch edge and pillow at frame-left.
- She should be WARM — the domestic anchor that Byte is oriented toward.
- No active expression (she's asleep), but body should suggest comfortable, careless sleep posture (one arm dangling off cushion edge, head at a slight tilt).

### Spatial Geometry
- Byte's sight-line (normal eye pupil offset) must visually connect to Luma's body on the couch. Draw a dotted sight-line annotation from Byte's eye toward Luma (like P03's sight-line annotation or the brow-differential annotations from C38). This is a production document — annotate spatial facts.
- Floor plane: perspective-correct. Byte's feet-to-floor gap should read clearly. The floor area between Byte and the couch should show some pixel confetti drifting (his trail from emergence position).
- Background monitors: present but defocused — they have returned to normal CRT static (gray-green phosphor glow, no cyan contamination). This sells the idea that the "breach" was Byte-specific, not an ongoing invasion.

### Staging Notes
- **Eye-level vs floating.** The camera being at 4–5 feet means Byte (floating at 18") is slightly ABOVE camera eyeline. This gives him a subtle spatial authority without making him threatening. He is looking DOWN-LEFT at Luma — that slight downward angle in his gaze adds tenderness, not dominance.
- **The cautious approach has already started.** Byte's body lean (+confetti trail) should show he is mid-motion toward the couch — not stationary. He has already made the unconscious choice to investigate. The beat is the moment he becomes aware of that choice.
- **Warm/cool gradient reads the story.** Byte is cool (cyan glow, desaturation ring) in the right half; Luma is warm (amber/orange hoodie, warm skin) in the left half. The color gradient IS the narrative tension: two incompatible worlds inhabiting one frame.

### Key Geometry (suggested)
- PW=800, DRAW_H=540 (standard)
- Byte body center: (int(PW*0.65), int(DRAW_H*0.40)) — floating (feet at y~int(DRAW_H*0.62))
- Floor plane: y_near = int(DRAW_H*0.78), recedes to vp_y = int(DRAW_H*0.32)
- Couch near-edge: x = int(PW*0.02), y = int(DRAW_H*0.50)
- Luma head: (int(PW*0.18), int(DRAW_H*0.38))
- Byte sight-line: dotted rule from eye at ~(int(PW*0.60), int(DRAW_H*0.37)) toward Luma head

### Arc Label
**CURIOUS / FIRST ENCOUNTER** — arc color: ELEC_CYAN (`(0, 212, 232)`)

---

## Shared Technical Notes for P07 and P09

- **Pixel confetti distribution:** All confetti uses 4–7 sided irregular polygons (the Cycle 11 standard — NO rectangles for Glitchkin shapes). For confetti scatter, still use small irregular polys, not dots or squares.
- **Face test gate:** If Byte's face appears at any scale, run `LTG_TOOL_character_face_test.py --char byte` before submitting. P07 (partial emergence) and P09 (floating) both include Byte face elements.
- **After `img.paste()`, always refresh `draw = ImageDraw.Draw(img)`** — pil-standards.md requirement.
- **Naming:** `LTG_SB_cold_open_P07.png` and `LTG_SB_cold_open_P09.png` (matching the C41 convention from brief). Generators: `LTG_TOOL_sb_cold_open_P07.py` and `LTG_TOOL_sb_cold_open_P09.py`.
- **Register both generators in `output/tools/README.md`.**

---

## After Delivery

Send completion report to Alex Chen's inbox. Update PANEL_MAP.md: P07 and P09 status PLANNED → EXISTS.

Lee Tanaka
