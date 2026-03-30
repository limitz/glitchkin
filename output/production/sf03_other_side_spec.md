<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# SF03 — "The Other Side" — Background Generator Spec
# LTG_PROD_sf03_other_side_spec_v001.md

**Author:** Alex Chen, Art Director
**Date:** 2026-03-29
**Cycle:** 14
**Status:** APPROVED — unblocks Jordan Reed to build generator next cycle
**References:**
- `output/color/style_frames/style_frame_03_other_side.md` (full frame spec — primary source)
- `output/tools/LTG_TOOL_style_frame_01_discovery.py` (SF01 generator pattern to follow)
- `output/tools/LTG_TOOL_style_frame_02_glitch_storm.py` (SF02 generator pattern)
- `output/color/style_frames/LTG_COLOR_styleframe_discovery.png` (SF01 rendered output)
- `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png` (SF02 rendered output)
- `output/color/style_frames/compositions/frame03_other_side_composition.png` (rough composition)

---

## Purpose of This Document

This spec translates the full artistic spec in `style_frame_03_other_side.md` into a precise
technical brief for Jordan Reed to build `LTG_TOOL_style_frame_03_other_side.py`.
The generator must produce `LTG_COLOR_styleframe_otherside.png` at 1920×1080.

All color values are from `master_palette.md`. No ad-hoc colors are permitted.
Where a color is not in the master palette, it is specified as a derived RGB tuple with derivation noted.

---

## Canvas

- **Size:** 1920 × 1080 (16:9, standard production canvas — matches SF01 and SF02)
- **Color mode:** RGB (convert RGBA composites back to RGB before save, per pipeline standard)
- **Output path:** `/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside.png`

---

## Mood & Narrative Position

**Frame:** "The Other Side" — Act 3 of a major arc episode.
**Narrative:** Luma has fully crossed into the Glitch Layer. Action has paused.
This is the world-building promise frame: vast, strange, beautiful, dangerous.
A quiet character moment — Luma and Byte on a platform, looking at an infinite digital universe.

**Mood contrasts with SF01 and SF02:**
- SF01 ("The Discovery"): Warm, intimate, hushed wonder. Enclosed room, human scale.
- SF02 ("Glitch Storm"): Kinetic terror, outdoor, enormous threat, chaos and speed.
- SF03 ("The Other Side"): Still awe. Vast and quiet. The world is not falling apart — it is simply different.

**Key emotion:** "Grief-adjacent wonder" — Luma has left warmth behind. The frame's most important
statement is the ABSENCE of warm light. She carries her warmth in her pigment, not in the light.

---

## Color Palette — All Production Hex Values

### Dominant Colors (appear in large areas)

| Name | Hex | RGB | Role |
|---|---|---|---|
| VOID_BLACK | `#0A0A14` | (10, 10, 20) | Deep background, platform base, void |
| UV_PURPLE | `#7B2FBE` | (123, 47, 190) | Ambient void light — fills everything |
| ELEC_CYAN | `#00F0FF` | (0, 240, 255) | Circuit traces, Byte's eye, platform glow |
| DATA_BLUE | `#2B7FFF` | (43, 127, 255) | Data waterfall, secondary traces, jeans |
| ACID_GREEN | `#39FF14` | (57, 255, 20) | Pixel-art plants, distant Glitchkin dots |
| STATIC_WHITE | `#F0F0F0` | (240, 240, 240) | Void stars, confetti particles |

### Warm-color Inventory (sparse — intentional)

| Name | Hex | RGB | Role |
|---|---|---|---|
| HOODIE_UV_MOD | derived | (192, 112, 56) | Luma hoodie under UV ambient — `#C07038` |
| SKIN_UV_MOD | derived | (168, 120, 144) | Luma skin under UV ambient — `#A87890` (DRW-11) |
| CORRUPT_AMBER | `#FF8C00` | (255, 140, 0) | Glowing edges of Real World debris |
| TERRACOTTA | `#C75B39` | (199, 91, 57) | Corrupted Real World wall fragment |

### Supporting Colors

| Name | Hex | RGB | Role |
|---|---|---|---|
| DARK_ACID | derived | (26, 168, 0) | Plant shadow undersides — `#1AA800` |
| DEEP_CYAN | `#00A8B4` | (0, 168, 180) | Byte inner glow, deep cyan traces |
| HOT_MAGENTA | `#FF2D6B` | (255, 45, 107) | Byte's cracked eye (void-facing) |
| UV_PURPLE_MID | derived | (42, 26, 64) | ENV-11 far-distance atmospheric haze — `#2A1A40` |
| UV_PURPLE_DARK | derived | (43, 32, 80) | ENV-12 void sky near-transition — `#2B2050` |
| FAR_EDGE | derived | (33, 17, 54) | Far structure edges at void-scale — `#211136` |
| SLAB_TOP | derived | (26, 40, 56) | ENV-09 floating slab top surface — `#1A2838` |
| SLAB_FACE | derived | (10, 20, 32) | ENV-10 floating slab vertical face — `#0A1420` |
| BELOW_VOID | derived | (5, 5, 8) | GL-08a below-platform abyss — `#050508` |
| DATA_BLUE_HL | derived | (106, 186, 255) | GL-06b individual data code highlights — `#6ABAFF` |
| MUTED_TEAL | derived | (91, 140, 138) | Lamppost fragment body — `#5B8C8A` |

---

## Composition Overview

- **Aspect:** 16:9 widescreen (matches all other style frames)
- **Shot type:** Wide with strong foreground. Luma full-body lower-left, small (~1/5 frame height).
  The Glitch Layer environment consumes 4/5 of the frame.
- **Rule of thirds:**
  - Luma: left third-line, just below lower horizontal third
  - Vanishing horizon (far void convergence): upper horizontal third
  - The vertical journey from lower-left (Luma) to upper-right (void horizon) is the frame's axis.
- **Dutch angle: NONE.** Horizontal is level. Stillness after SF02's chaos is a deliberate choice.
  Do not tilt the canvas. Level = the world is not falling apart; it is simply different.

---

## Depth Layers — Generator Implementation Guide

Build the frame in five depth passes from back to front. Draw order matters for depth reads.

### Layer 5 — Void Sky (draw FIRST — background)

**Zone:** Upper quarter, y=0 to approximately y=270 (top 25% of frame)

**Draw order within layer:**
1. Fill entire canvas with VOID_BLACK `(10, 10, 20)` as base.
2. Gradient from VOID_BLACK at top edge to UV_PURPLE_DARK `(43, 32, 80)` at y=270.
   Implementation: row-by-row fill, lerp from (10,10,20) at y=0 to (43,32,80) at y=270.
3. Static stars/void artifacts: scatter 80-120 white dots at `(240, 240, 240)`, 1px each,
   randomly placed in the upper third. Seeded random for reproducibility (suggest seed=42).
4. Ring megastructure (far, barely visible): enormous circle outline centered approximately
   (W*0.55, H*0.18), radius ~H*0.45. Color: UV_PURPLE `(123, 47, 190)`, outline only (no fill),
   width 2px, alpha-composited at low opacity (~60/255) so it is barely visible.

### Layer 4 — Far Distance (draw SECOND)

**Zone:** Upper 40% of frame (y=0 to y=432), above Layer 3 structures

**Draw order within layer:**
1. Atmospheric haze band: gradient fill from UV_PURPLE_MID `(42,26,64)` blending into Layer 5.
   This is the "inverse atmospheric perspective" — colors become more purple, not lighter, with distance.
2. Enormous flat geometric planes: 3-4 large dark polygon slabs (FAR_EDGE `(33,17,54)` fill,
   UV_PURPLE thin outline). These are continent-scale structures barely distinguishable from void.
   Suggested positions: x=0.55W-0.85W, various y in upper half.
3. Distant data waterfalls: 4-6 thin vertical lines `(43, 127, 255)` width 1-2px,
   in the upper mid-distance. These are suggestion only — no detail.
4. Distant Glitchkin: 6-10 dots of `(57, 255, 20)` (2px) and `(0, 240, 255)` (2px)
   scattered across x=0.4W to 0.9W, y=0.2H to 0.45H.
5. Distant Corrupt Amber fragments: 5-8 dots of `(255, 140, 0)` at 2-3px,
   scattered in the purple-blue mid-distance as punctuation.

### Layer 3 — Mid-distance Structures (draw THIRD)

**Zone:** Middle frame band, approximately y=270 to y=600

**Floating structure cluster (mix of geometry and corrupted Real World fragments):**

1. Abstract geometric slabs: 4-6 floating hexagonal or rectangular slabs.
   - Top surfaces: SLAB_TOP `(26, 40, 56)` — the UV ambient reads on horizontal surfaces
   - Vertical faces: SLAB_FACE `(10, 20, 32)` — receding into near-void
   - Glowing edges: `(0, 240, 255)` for navigation paths; `(43, 127, 255)` for data-storage
   - Detail level: 60% — edges slightly softened (do not use anti-aliasing hack; just draw
     slightly thicker outlines with gap fills)
   - Positions: distributed across x=0.2W to 0.85W, at various y in the mid-distance band

2. Corrupted Real World fragments (crucial story elements — show the Real World being consumed):
   - WALL FRAGMENT: A rectangle of TERRACOTTA `(199,91,57)` with CORRUPT_AMBER `(255,140,0)`
     glowing crack lines at its edges. Suggested size: ~W*0.06 × H*0.12.
     Position: approximately x=0.42W, y=0.38H. Crack lines: draw jagged polygon outlines
     in CORRUPT_AMBER at the fragment's perimeter.
   - ROAD SURFACE FRAGMENT: A dark polygon `(42,42,56)` with CORRUPT_AMBER amber at boundary.
     Smaller than wall fragment. Position: approximately x=0.55W, y=0.48H.
   - LAMPPOST FRAGMENT: Thin vertical rectangle MUTED_TEAL `(91,140,138)` body, CORRUPT_AMBER
     corruption spreading up from base (gradient from amber at bottom to teal at top).
     Position: approximately x=0.65W, y=0.32H to y=0.52H.

### Layer 2 — Midground (draw FOURTH)

**Zone:** Lower 60% of frame, focused around the platform level

**Platform (where Luma and Byte stand — primary foreground element):**

1. Platform base: rectangle from (x=0, y=H*0.66) to (x=W*0.45, y=H*0.75).
   Fill: VOID_BLACK `(10, 10, 20)`. This is the main standing surface.

2. Circuit traces on platform surface:
   - Primary traces: `(0, 240, 255)` at 80% luminance → use `(0, 192, 204)` for slightly dimmed
     structural traces. Draw as a grid pattern of horizontal and vertical lines, width 1-2px.
   - Secondary traces: `(43, 127, 255)` lines interspersed with primary.
   - Circuit pattern: use seeded random to place a grid-aligned irregular circuit trace pattern.
     Suggest: grid cells of ~20px, with ~40% of vertical and ~60% of horizontal connections drawn.

3. Platform edge lip (front-facing surface):
   Fill: SLAB_FACE `(10, 20, 32)` — the underside of the platform facing the viewer.
   Rectangle from (x=0, y=H*0.75) to (x=W*0.45, y=H*0.78).

4. Pixel-art plants in cracks (crucial — show the Glitch Layer is alive):
   - Draw 4-6 geometric succulent-like forms in platform cracks.
   - Main form: `(57, 255, 20)` (ACID_GREEN) filled polygons — angular, not organic.
   - Shadow underside: `(26, 168, 0)` (DARK_ACID) on lower faces.
   - Top highlight: `(0, 240, 255)` on upper faces (catching circuit bounce light).
   - Cracks: thin dark lines `(5, 5, 8)` in the platform surface from which plants grow.
   - Plant positions: scattered along platform surface at approximately
     x=W*0.08, W*0.14, W*0.20, W*0.28, W*0.36 (adjust to avoid character zone).

5. Abyss below platform edge:
   Fill the area below the platform with BELOW_VOID `(5, 5, 8)` — the darkest value in the show.
   This is the void-below-platform context (GL-08a exception; one of only two permitted uses).

6. Data waterfall (right side, near character):
   - A column of scrolling code: vertical fill strip at approximately x=W*0.38 to W*0.42, y=H*0.18 to H*0.66.
   - Base color: DATA_BLUE `(43, 127, 255)` at 90% luminance → use `(39, 115, 230)`.
   - Brightest code characters: scatter DATA_BLUE_HL `(106, 186, 255)` 4×6px rectangles
     irregularly across the waterfall column (suggest 30-40 characters, seeded random).
   - Data mist at base: gradient from DATA_BLUE to UV_PURPLE `(123, 47, 190)` at y=H*0.62 to H*0.68.
   - Light pool on platform: soft UV_PURPLE/blue glow at platform surface to waterfall's left.

7. Floating sub-platforms (stepping-stone distance from Luma):
   - 2-3 small floating slabs at varying heights near Luma.
   - Same construction as Layer 3 slabs but smaller (W*0.04 to W*0.08 wide) and at full detail.
   - Position: x=W*0.10 to W*0.35, y=H*0.30 to H*0.55 (various heights).

**VOID BELOW THE PLATFORM (atmosphere):**
Draw a vertical gradient from BELOW_VOID `(5,5,8)` at the bottom edge up to VOID_BLACK `(10,10,20)`
at the platform underside. This depth separates the platform from the literal abyss.

### Layer 1 — Extreme Foreground (draw LAST before characters)

**Zone:** Bottom portion of frame, y=H*0.66 to H*1.0

This layer IS the platform surface as seen closest to the viewer. The foreground and midground
platform may be drawn as one continuous surface — the "extreme foreground" label here refers to
the closest portion of that surface.

**Additional foreground confetti (settled particles):**
- 8-12 static 2-3px dots resting on the platform surface.
- Colors: `(0, 240, 255)`, `(240, 240, 240)`, `(57, 255, 20)`, `(43, 127, 255)`.
- "Settled" means placed flat on the surface — do not give them a floating offset.
- Seeded random placement within platform bounds.

---

## Characters

**IMPORTANT:** Luma and Byte are SMALL in this frame.

### Luma
- **Height:** Approximately H*0.20 = 216px at 1080px canvas height. (Much smaller than SF01/SF02.)
- **Position:** Bottom-left. Luma's feet at approximately (x=W*0.14, y=H*0.66). She stands at the platform edge.
- **Hoodie color (UV ambient modified):** HOODIE_UV_MOD `(192, 112, 56)` — the orange is shifted darker/more magenta under UV Purple ambient.
- **Skin (UV ambient modified):** SKIN_UV_MOD `(168, 120, 144)` — warm tan becomes lavender-washed.
- **Jeans:** `(38, 61, 90)` (standard shadow-fill under UV light) with `(43, 127, 255)` blue-white catch on outer seam from waterfall light.
- **Hair:** `(26, 15, 10)` base, `(123, 47, 190)` UV_PURPLE sheen on crown (the dark hair catches ambient as a deep purple rim).
- **Pose:** Standing at edge, weight slightly back. Arms at sides, hands raised slightly — body language of someone bracing to look at something too vast. Three-quarter face toward viewer; one wide eye visible.
- **Feet at edge:** Toes at platform edge x=W*0.14 to W*0.17.
- **Note:** Luma's orange hoodie (even modified) is the most saturated warm element in the frame. She must read in silhouette against the UV_PURPLE mid-distance behind her.

### Byte
- **Height:** Approximately H*0.10 = 108px. He is on Luma's right shoulder.
- **Position:** On Luma's right shoulder, approximately (x=W*0.17, y=H*0.49).
- **Body:** VOID_BLACK `(10, 10, 20)` base with DEEP_CYAN `(0, 168, 180)` inner glow — in the Glitch Layer he seems more alive; his glow is more visible.
- **Circuit traces on body:** ELEC_CYAN `(0, 240, 255)` slightly more luminous than Real World scenes.
- **Cyan eye (left, facing Luma):** `(0, 240, 255)` — almost cozy; facing warmth.
- **Magenta eye (right, facing void):** HOT_MAGENTA `(255, 45, 107)` — facing danger; the frame's key color detail. The cracked eye faces the deep void.
- **NO Corrupt Amber outline:** UV Purple ambient provides adequate contrast. Do not add the amber outline exception from SF02.
- **Pixel-art plants:** A few confetti particles already settled on Luma's left shoulder and in her hair (ACID_GREEN and ELEC_CYAN 1-2px dots).

**Character draw function note:**
Use simplified pixel-art figure drawing for Luma at this scale (similar to the screen pixel figures
in SF01 but larger and more detailed). The goal is readable silhouette + key costume read (orange hoodie,
dark jeans, cream shoes). Face detail: one visible eye is sufficient at this scale.
Byte on shoulder: oval body, two distinctly colored eyes (cyan left, magenta right). Eyes must be visible.

---

## Lighting Setup

### No warm light in this frame — this is the frame's primary emotional statement.

**Primary:** UV_PURPLE `(123, 47, 190)` ambient — omnidirectional, slightly stronger from below.
- Implement as a soft RGBA overlay layer in UV_PURPLE at approximately alpha 35-45/255.
- Apply over the completed background before characters are drawn.
- Stronger toward the bottom of the frame (abyss glow): gradient from alpha 50 at y=H*0.7 to alpha 20 at y=0.

**Secondary:** ELEC_CYAN `(0, 240, 255)` from platform circuits — bouncing upward from platform surface.
- Implement as a soft cyan glow (radial gradient-style fill) at the platform surface level.
- Affects lower portions of characters (feet, ankles, lower legs) and immediate platform vicinity.
- Cyan bounce alpha: approximately 40-60/255 directly on platform surface, falling to 10/255 above H*0.55.

**Tertiary:** DATA_BLUE `(43, 127, 255)` from data waterfall — vertical line source at right.
- Affects the right side of the scene from approximately x=W*0.35 to x=W*0.45.
- Soft blue-white rim light on Luma's right shoulder and right-side platform surface.
- Implement as a soft RGBA overlay strip in the waterfall zone, alpha 30-40/255.

**Warm glow: DO NOT ADD.** If any element reads as warm-lit, it is either:
(a) a Real World fragment (acceptable — their warmth is material, not light), or
(b) a painting error (fix it).

---

## Pixel Confetti — Physics Rule Applied

This is ambient/settled confetti. NOT storm-density (that was SF02). Background radiation of the Glitch Layer.

- Particles: 1-3px, 40-60 total across the frame
- Distribution: predominantly mid-distance to foreground; sparse in far-distance
- Drift: slow ambient — in Glitch Layer, slight anti-gravity (many particles float very slightly upward
  but at negligible velocity; implement as random vertical offset ±2px from placement)
- Settled particles: on platform surface (flat), on Luma's left shoulder (implied, 2-3 dots)
- Colors: ELEC_CYAN `(0,240,255)`, STATIC_WHITE `(240,240,240)`, ACID_GREEN `(57,255,20)`, DATA_BLUE `(43,127,255)`
- No warm colors in confetti. Acid Green IS appropriate here (Glitch Layer ambient biological energy).
- Seeded random: use seed=77 for cross-frame consistency with SF01 transition confetti.

---

## Atmospheric Perspective Rule (CRITICAL — Glitch Layer inversion)

**Real World rule (SF01, SF02):** Objects get lighter and more desaturated with distance.
**Glitch Layer rule (SF03 only):** Objects get MORE PURPLE and DARKER with distance.

The Glitch Layer's atmospheric haze is UV_PURPLE, not white. Things in the distance don't bleach — they
purple out and darken. This is the inverse atmospheric perspective of the Glitch Layer.

**Implementation:**
- Foreground structures: full ELEC_CYAN glow edges, full VOID_BLACK base, sharp
- Mid-distance structures: SLAB_TOP/SLAB_FACE fill, slightly softened edges
- Far-distance structures: FAR_EDGE `(33,17,54)` fill + thin UV_PURPLE outlines, barely distinguishable from void
- Void: UV_PURPLE_MID `(42,26,64)` → VOID_BLACK at the very top edge

Make sure every depth layer reads clearly darker and more purple than the layer in front of it.
This is the opposite of the Real World, and it must be deliberate and consistent.

---

## Contrast With SF01 and SF02

| Dimension | SF01 — Discovery | SF02 — Glitch Storm | SF03 — Other Side |
|---|---|---|---|
| **Setting** | Interior room (Grandma's den) | Exterior town (Millbrook, Main Street) | Glitch Layer (interior void) |
| **Scale** | Human, intimate, enclosed | Town-wide, sky-filling threat | Universe-scale, infinite void |
| **Light** | Warm (lamp, amber) + cold (screen, cyan) | Dual cold (storm cyan + lightning) | No warm light — UV purple + cyan + blue only |
| **Characters** | Luma close (medium wide), Byte emerging | Luma + Cosmo small (running), Byte on hoodie | Luma very small (wide shot), Byte on shoulder |
| **Color temperature** | Warm-dominant (70% warm zone) | Cold-dominant (80% cold sky) | Pure cold (100% — warmth in pigment only) |
| **Dutch angle** | None | 4-degree clockwise (tension) | None (deliberate stillness after storm) |
| **Confetti** | Emerging (sparse, newly active CRT) | Maximum density (storm, enormous source) | Settled ambient (background radiation, quiet) |
| **Mood** | Hushed wonder | Kinetic terror | Quiet awe (grief-adjacent) |
| **Byte visibility** | Emerging from screen | VOID_BLACK body (storm = consumed) | Void Black with cyan glow (home = more alive) |
| **Amber outline on Byte** | No | YES (contrast in cyan storm) | No (UV Purple provides adequate contrast) |

---

## Output File

```
/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside.png
```

**Naming note:** "otherside" (one word, no hyphen) per LTG naming convention (lowercase, underscores only).

---

## Generator Script Spec

**File:** `LTG_TOOL_style_frame_03_other_side.py`
**Location:** `/home/wipkat/team/output/tools/`

**Structure to follow (based on SF01/SF02 generator pattern):**

```python
# Module-level color constants — all named from master_palette.md
# Canvas: W=1920, H=1080
# Functions:
#   generate(output_path)        — main entry point
#   draw_void_sky(draw, img)     — Layer 5 (background fill + stars + ring)
#   draw_far_distance(draw)      — Layer 4 (megastructures, Glitchkin dots)
#   draw_mid_distance(draw)      — Layer 3 (slabs, corrupted fragments)
#   draw_midground(draw)         — Layer 2 (platform, waterfall, sub-platforms)
#   draw_foreground(draw)        — Layer 1 (closest platform surface, plants, confetti)
#   draw_lighting_overlay(img)   — RGBA overlay for UV ambient + cyan bounce + blue waterfall
#   draw_luma(draw, cx, cy, h)   — Luma figure (simplified pixel-art at small scale)
#   draw_byte(draw, cx, cy, h)   — Byte figure (oval body, two-color eyes)
#   draw_confetti(draw)          — Ambient settled confetti (seed=77)
```

**Critical draw order:**
1. `draw_void_sky` — establishes base
2. `draw_far_distance` — back atmosphere
3. `draw_mid_distance` — corrupted fragments and megastructures
4. `draw_midground` — platform and waterfall
5. `draw_foreground` — plants, close platform detail
6. `draw_lighting_overlay` — UV purple + cyan bounce + blue waterfall composite (RGBA → paste)
7. `refresh draw = ImageDraw.Draw(img)` after any img.paste() call (known pipeline rule from SF01)
8. `draw_luma` + `draw_byte` — characters on top of everything
9. `draw_confetti` — confetti over everything including characters (it has settled on them)
10. Footer bar

**Rule:** Never overwrite existing outputs — output is always a new versioned file.

---

## Validation Checklist (Jordan Reed to check before submitting)

- [ ] Level horizon (no dutch angle)
- [ ] No warm light source — only UV purple, cyan, and blue lighting
- [ ] Luma's orange hoodie reads in silhouette against UV_PURPLE mid-distance
- [ ] Byte's cyan eye faces left (toward Luma), magenta eye faces right (toward void) — both visible
- [ ] Atmospheric perspective: far structures ARE darker/more purple than near structures
- [ ] Data waterfall: DATA_BLUE column with code highlights (DATA_BLUE_HL) present
- [ ] Pixel-art plants on platform with ACID_GREEN body + DARK_ACID shadow + CYAN highlight
- [ ] BELOW_VOID used for abyss under platform edge (darkest value in show)
- [ ] Confetti: ambient density (not storm density), seed=77, no warm colors
- [ ] Ring megastructure: visible as UV_PURPLE outline in void sky (barely visible = correct)
- [ ] Corrupted Real World fragments carry CORRUPT_AMBER amber glow at their edges
- [ ] UV Purple lighting overlay applied before characters (not after)
- [ ] No amber outline on Byte (SF02 exception does not apply here)
- [ ] img draw object refreshed after every img.paste() call
- [ ] Output saved to correct path with LTG-compliant filename

---

*Alex Chen — Art Director — Cycle 14 — 2026-03-29*
*This spec unblocks Jordan Reed to build `LTG_TOOL_style_frame_03_other_side.py` next cycle.*
*Source of truth for artistic intent: `style_frame_03_other_side.md` (Sam Kowalski, primary spec).*
*This document translates that intent into generator implementation specifics.*
