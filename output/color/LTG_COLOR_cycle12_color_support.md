<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Cycle 12 Color Support Notes
## "Luma & the Glitchkin" — Sam Kowalski, Color & Style Artist

**Date:** 2026-03-30
**Cycle:** 12
**Author:** Sam Kowalski
**References:** master_palette.md v2.0, style_frame_01_discovery.md v2.0,
               style_frame_02_glitch_storm.md v2.0, luma_color_model.md v1.0

---

## Overview

This document provides color support for the three new Cycle 12 assets being developed
by Alex Chen (Art Director) and Maya Santos (Character Designer):

1. **Alex Chen — Visual Surprise element in Style Frame 01** (Victoria Ashford A+ requirement)
2. **Alex Chen — Asymmetric logo layout** (Luma larger/left, Glitchkin smaller/right)
3. **Maya Santos — Neutral/resting expression for Luma** (4×2 or 3×3 expression sheet expansion)

For each asset, this document provides: color guidance, relevant palette entries,
any new derived values that must be registered, and consistency checks.

---

## 1. Style Frame 01 — Visual Surprise Element

### Context
Alex Chen is adding a visual surprise element to Style Frame 01 (The Discovery). The Cycle 11
frame already contains:
- Mid-air pixel confetti transition column (x=768–960, y=200–700) with warm/cold split
- Screen pixel figures scaled to 15px wide, viewer-readable silhouettes
- Monitor interior: receding perspective grid + pixel figures
- Luma lean increased to 48px (~16° forward urgency)

The visual surprise must feel earned and consistent with the established color language.

### Color Guidance for Visual Surprise

**If the surprise involves a new emergent element within the CRT screen:**
- All screen-emission colors must be GL-01 (`#00F0FF` Electric Cyan) for glow
- Any additional Glitch Layer inhabitants visible on screen: use GL-01b Byte Teal (`#00D4E8`)
  for bodies — NOT Electric Cyan — per the Byte Teal usage warning
- Any data structures or geometry: GL-06 Data Stream Blue (`#2B7FFF`) for depth
- Hot Magenta (`#FF2D6B`) acceptable as a single danger/tension accent — NOT as a fill

**If the surprise involves a Real World object reacting to the digital breach:**
- Real World objects retain their base palette colors; glitch contamination reads as
  a Cyan outline or scan-line effect, not a full recolor
- The CRT's warm Muted Teal casing (`#5B8C8A`) under screen glow = DRW-06 (`#3AACAA`)
  on the face nearest the screen — this is already documented and correct
- Do NOT introduce any new light sources that compete with the three-light setup:
  Cyan (right/monitor), Soft Gold (left/lamp), Dusty Lavender (ambient fill)

**If the surprise involves Luma herself (e.g., her hoodie pixels activating):**
- Hoodie pixel activation: the pixel grid uses `#00F0FF` (Electric Cyan) — same as screen
- Grid activation glow must NOT wash over skin zones — the warm/cold boundary at x=W//2
  with the 80px overlap zone is already carefully calibrated (see Cycle 11 header notes)
- If activating pixels on the shadow side (left, lamp-facing): use the warm pixel variant
  `#E8C95A` (Soft Gold) for any illuminated pixels on the warm side. This is not
  currently in the palette as a pixel-activation color — if used, register as:
  **NEW CANDIDATE: CHAR-L-09 — Hoodie Pixel (Warm-Lit Activation)** `#E8C95A` (Soft Gold)
  This would be the lamp-side analog to the screen-lit cyan pixels.
  ACTION REQUIRED: Alex Chen to confirm whether warm-side pixel activation is used;
  if yes, Sam Kowalski to register CHAR-L-09 in master_palette.md Section 5.

**Figure-ground safety check:**
- Whatever the visual surprise is, it must NOT introduce a new color that conflicts
  with Luma's primary warm zone (orange hoodie `#E8722A` / `#E8703A`, warm skin `#C8885A`)
- Check Byte's amber outline rule: if the surprise makes the screen area more Cyan-dominant
  (above 35% of background), verify Byte remains small enough in frame to need the
  Corrupted Amber outline exception — likely yes in SF01 wide shot.

### No New Palette Entries Required (existing assets)
The Cycle 11 frame additions (confetti, pixel figures, screen grid) are already rendered
using documented palette constants. No undocumented inline tuples were identified in
the Cycle 11 style_frame_01_rendered.py header note review.

---

## 2. Asymmetric Logo Layout

### Context
Alex Chen is developing an asymmetric logo alternative: Luma larger/left, Glitchkin
characters smaller/right. This is a secondary layout to the primary show logo.

### Color Guidance for Asymmetric Logo

**Luma's name / wordmark (left, dominant):**
- Primary: `#E8722A` (Warm Orange — Luma's hoodie color) — this is the character-identity color
- Outline/stroke: `#3B2820` (Deep Cocoa) — universal line color
- Inner glow accent if any: `#00F0FF` (Electric Cyan) — keeps the hoodie pixel connection
- Background context: if the logo is on a warm ground, the Cyan glow reads as intrusion/magic
  (appropriate for the show's premise); on a dark/void ground it reads as pure energy

**"Glitchkin" wordmark (right, subordinate):**
- The Glitchkin name should read as digitally unstable compared to Luma's name
- Primary: `#00F0FF` (Electric Cyan) with `#FF2D6B` (Hot Magenta) accent or outline
- If individual Glitchkin characters are depicted alongside, their markings use
  `#39FF14` (Acid Green) per GL-03 — this is NOT the same as Byte's colors
- Byte specifically: `#00D4E8` (Byte Teal) for body, `#FF8C00` (Corrupted Amber) for outline
  accent or eye detail

**Ampersand / connector (&):**
- The connector between "Luma" and "the Glitchkin" is a visual bridge between warm and cold
- Suggest: `#FF8C00` (Corrupted Amber) — the bridge color between Real World warmth and
  Glitch energy. It reads as neither fully warm nor fully digital.
- Alternative: use it as a pixel-grid ampersand, with pixels transitioning from
  `#E8C95A` (Soft Gold) on the warm side to `#00F0FF` (Cyan) on the digital side

**Size hierarchy — color consistency rule:**
- The smaller Glitchkin silhouettes on the right MUST have lower visual weight than Luma
- Achieve this through saturation reduction (not value reduction) on Glitchkin elements
  at half-size: reduce Acid Green from `#39FF14` to approximately `#28C010` (more muted)
  for secondary silhouette use. This is an acceptable inline reduction for the logo only —
  no palette entry needed if used exclusively in logo context.
- If this muted Acid Green appears in any other asset, register as GL-03b.

**Background options for logo:**
| Background | Luma Name | Glitchkin Name | Mood |
|---|---|---|---|
| `#FAF0DC` (Warm Cream) | `#E8722A` warm orange | `#00F0FF` + `#FF2D6B` | Safe/accessible |
| `#0A0A14` (Void Black) | `#E8722A` + gold glow | `#00F0FF` electric | High-drama/poster |
| `#1A1428` (Night Sky)  | `#FAF0DC` warm white | `#00F0FF` + `#7B2FBE` | Cinematic/title card |

Recommend: the Void Black background is the strongest for pitch use — maximum contrast,
electric feel, Luma's warm orange name pops immediately.

---

## 3. Luma Neutral/Resting Expression — Color Notes

### Context
Maya Santos is adding a neutral/resting expression to Luma's expression sheet.
The existing expressions (Reckless Excitement, Guilty Sheepishness, etc.) all have
specific color cues (blush, eye highlight states, etc.). The neutral expression
requires a clean base with no expression-specific color overlays.

### Color Specification for Neutral Expression

**Skin:** `#C4A882` (RW-10 Warm Tan — canonical neutral base)
- NOT the lamp-lit derivation `#C8885A` (CHAR-L-01)
- The neutral/model-sheet skin base is always RW-10, per Section 7 of master_palette.md
- This is the key distinction: the neutral expression must use the canonical neutral base
  so it can serve as the lighting-reference face for painters

**Eye state (neutral):**
- Iris: `#C87D3E` (Warm Amber — from luma_color_model.md)
- Pupil: `#3B2820` (Deep Cocoa — same as line)
- White: `#FAF0DC` (Warm Cream — never pure white)
- Highlight dot: `#F0F0F0` (Static White — single dot, upper-left position)
- Eyelid line: standard weight `#3B2820` Deep Cocoa
- Neutral eyes: approximately 75% open — neither wide (excitement) nor heavy-lidded (bored)
  This is defined as "eyes where the top eyelid intersects the top of the iris at mid-position"

**Mouth (neutral):**
- Closed, slight natural curve — neither smile nor frown
- Line color: `#3B2820` (Deep Cocoa) — standard weight
- No tongue, no interior shadow (those are expression-specific)
- No blush — the neutral expression has NO blush marks

**Blush disambiguation update:**
- The neutral expression sets the zero-point reference: no blush at all
- Painters can now calibrate: neutral = zero; Reckless Excitement = full-opacity
  round circles outer cheeks only; Guilty Sheepishness = 60% elongated crossing nose
- This is the three-point reference system (zero / 60% / 100%)

**Hair (neutral):**
- Base: `#1A0F0A` (Near-Black Espresso — luma_color_model.md)
- Shadow: `#0A0A14` (Void Black for depth between curl masses)
- Highlight: `#3D1F0F` (Warm Dark Brown, crown only — small shape)
- In a neutral expression, hair is undisturbed — no windstream motion arcs,
  no DRW-17 storm-magenta rim. Pure canonical color model.

**No new palette entries required.**
All neutral expression colors are existing, documented palette entries.
The neutral expression is the canonical skin tone reference — it must match master_palette.md
exactly, without any scene-derived modifications.

### DRW-16 Painter Warning — Still Outstanding
**CARRY FORWARD:** DRW-16 (Shoulder Under Waterfall Blue, `#9A7AA0`) — the hoodie orange
right shoulder under Data Stream Blue waterfall light in Style Frame 03. This warning has
been carried forward since Cycle 7 (Naomi Bridges, DRW-16 notation). The neutral
expression sheet does not include this scenario, but it must still be added to
luma_color_model.md as a painter warning note for Glitch Layer scenes.
**This is outstanding work for the next available cycle.** Not blocked by Cycle 12 assets.

---

## Color Consistency Summary — Cycle 12

| Asset | New Colors Needed | Palette Action |
|---|---|---|
| SF01 Visual Surprise | CHAR-L-09 warm pixel activation — IF warm-side pixel activation is used | Conditional — Alex to confirm |
| Asymmetric Logo | GL-03b muted Acid Green — IF Glitchkin silhouettes appear in other assets | Conditional — logo use only = no entry needed |
| Luma Neutral Expression | None — all colors are existing documented entries | No action required |
| SF02 Glitch Storm Color Key PNG | None — all colors documented in SF02 spec + master palette | Generated: LTG_COLOR_colorkey_glitchstorm.png |

**Master palette version remains 2.0.** No new entries required this cycle unless
Alex confirms warm-side pixel activation for SF01 visual surprise.

---

## Files Created This Cycle

| File | Location | Purpose |
|---|---|---|
| `LTG_COLOR_colorkey_glitchstorm.png` | `/output/color/color_keys/thumbnails/` | SF02 rendered color key (Priority 3) |
| `LTG_TOOL_colorkey_glitchstorm_gen.py` | `/output/tools/` | Generator script for above |
| `LTG_TOOL_naming_compliance_copy.py` | `/output/tools/` | Creates LTG-compliant named copies |
| `LTG_COL_luma_colormodel.png` | `/output/characters/color_models/swatches/` | LTG-compliant copy |
| `LTG_COL_byte_colormodel.png` | `/output/characters/color_models/swatches/` | LTG-compliant copy |
| `LTG_COL_cosmo_colormodel.png` | `/output/characters/color_models/swatches/` | LTG-compliant copy |
| `LTG_COL_miri_colormodel.png` | `/output/characters/color_models/swatches/` | LTG-compliant copy |
| `LTG_COLOR_colorkey_sunny_afternoon.png` | `/output/color/color_keys/thumbnails/` | LTG-compliant copy |
| `LTG_COLOR_colorkey_nighttime_glitch.png` | `/output/color/color_keys/thumbnails/` | LTG-compliant copy |
| `LTG_COLOR_colorkey_glitchlayer_entry.png` | `/output/color/color_keys/thumbnails/` | LTG-compliant copy |
| `LTG_COLOR_colorkey_quiet_moment.png` | `/output/color/color_keys/thumbnails/` | LTG-compliant copy |
| `LTG_COLOR_cycle12_color_support.md` (this file) | `/output/color/` | Color support notes |

---

*Sam Kowalski — Cycle 12 (2026-03-30)*
