# LTG_COLOR_colorkey_otherside_v001 — Color Key Planning: The Other Side (SF03)

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30
**Cycle:** 14
**Status:** Planning doc — for Jordan Reed's SF03 background build
**References:** style_frame_03_other_side.md, master_palette.md v2.0 (Cycle 14)

---

## Purpose

This document is the color key brief for Jordan Reed's Other Side background (SF03).
It establishes the dominant palette, zone logic, forbidden colors, and key distinctions
from SF01 (warm room) and SF02 (contested street). Jordan should read this before building
any color passes on the Other Side environment.

---

## Scene Identity

**Scene:** "The Other Side" — Luma's first full entry into the Glitch Layer
**Narrative mood:** Quiet awe. Vast. Still. Beautiful and alien.
**Color mission:** Pure digital space — zero warm tones in any light source.
Warmth exists only as *material color* Luma carries from the Real World (her hoodie,
her skin, corrupted RW fragments). No light source in this scene is warm.

---

## Dominant Palette — The Other Side Color Key

All constants match master_palette.md and style_frame_03_other_side.md.

| Role | Name | Hex | RGB | Notes |
|---|---|---|---|---|
| **Dominant base** | Void Black (GL-08) | `#0A0A14` | (10, 10, 20) | Sky, platform material, primary fill |
| **Dominant key** | Electric Cyan (GL-01) | `#00F0FF` | (0, 240, 255) | Circuit traces, ambient key light, hoodie pixels |
| **Depth / atmosphere** | UV Purple (GL-04) | `#7B2FBE` | (123, 47, 190) | Atmospheric haze, ambient fill, ring megastructure |
| **Secondary key** | Data Stream Blue (GL-06) | `#2B7FFF` | (43, 127, 255) | Waterfalls, lit slab edges, depth recession |
| **Accent / biology** | Acid Green (GL-03) | `#39FF14` | (57, 255, 20) | Platform flora, distant Glitchkin |
| **Accent / corruption** | Hot Magenta (GL-02) | `#FF0090` | (255, 0, 144) | Byte's cracked eye, corruption events — ACCENT ONLY |
| **Corrupted RW** | Corrupted Amber (GL-07) | `#FF8C00` | (255, 140, 0) | RW fragment edges — ACCENT ONLY |
| **Near-void** | Below-Void-Black (GL-08a) | `#050508` | (5, 5, 8) | Abyss below platform — deepest anchor |

> **Note on `#FF0090` vs. master palette GL-02 `#FF2D6B`:**
> `#FF0090` (Hot Magenta as specified in task brief, RGB 255,0,144) differs slightly from
> master palette GL-02 `#FF2D6B` (RGB 255,45,107). In the Other Side context, GL-02 `#FF2D6B`
> is the correct production value — use it for Byte's cracked eye and any corruption accent.
> `#FF0090` is not a registered palette entry. Jordan: use `#FF2D6B` for all magenta accents
> in this scene.

---

## Zone Color Logic — Layer by Layer

### Zone 1 — Void Sky (upper 25%)
- **Base:** `#0A0A14` Void Black (darkness at frame top)
- **Transition:** `#2B2050` (ENV-12) at mid-void — deep dark purple, almost black
- **Ring megastructure:** `#7B2FBE` UV Purple outline at extreme distance (barely visible)
- **Static artifacts:** `#F0F0F0` at 1px, sparse, irregular — corrupted pixel noise, not stars
- NO atmospheric gradient toward blue or warm. Void stays dark.

### Zone 2 — Far Distance Structures (upper-mid, 25-50%)
- **Fill:** `#2A1A40` (ENV-11 deep UV atmospheric haze) — structures dissolve into purple
- **Edges (barely):** `#211136` — UV Purple at 20% on Void Black (R:33, G:17, B:54)
- **Data waterfalls:** `#2B7FFF` thin vertical lines only, no detail
- **Glitchkin dots:** `#39FF14` tiny moving dots at this distance
- **Atmospheric rule:** Farther = more UV Purple dominant, closer = more Cyan. INVERSE of real-world atmospheric perspective.

### Zone 3 — Mid-distance Structures (mid-frame, 40-65%)
- **Slab tops:** `#1A2838` (ENV-09) — dark blue-grey under UV ambient
- **Slab verticals:** `#0A1420` (ENV-10) — near-void, strongly receding
- **Glowing slab edges:** `#00F0FF` (navigation paths) or `#2B7FFF` (data-storage structures)
- **Corrupted RW fragments (key storytelling elements):**
  - Terracotta wall fragment: `#C75B39` base + `#FF8C00` Corrupted Amber at cracks/edges
  - Road surface fragment: `#2A2A38` under glitch light + `#FF8C00` at boundary (consuming)
  - Lamppost fragment: `#5B8C8A` body + `#FF8C00` corruption spreading from base

### Zone 4 — Immediate Environment / Platform Area (lower, 60-85%)
- **Platform surface:** `#0A0A14` Void Black
- **Circuit traces (primary):** `#00F0FF` at 80% luminance (structural — slightly dimmer than event traces)
- **Circuit traces (secondary):** `#2B7FFF` Data Stream Blue for secondary lines
- **Pixel-art plants in cracks:** `#39FF14` Acid Green geometric forms
- **Plant shadows:** `#1AA800` (GL-03a Dark Acid Green)
- **Plant highlights (bounce from circuits):** `#00F0FF` faint cyan on top faces
- **Data waterfall (right side, near):** `#2B7FFF` columns + `#6ABAFF` (GL-06b) on brightest code chars
- **Waterfall spray base:** `#7B2FBE` UV Purple where stream impacts surface
- **Settled confetti:** `#00F0FF`, `#F0F0F0`, `#39FF14`, `#2B7FFF` — sparse, 1-3px, static

### Zone 5 — Abyss (below platform edge)
- **Color:** `#050508` Below-Void-Black (GL-08a) — the darkest value in the show
- The void below the platform edge is the absolute dark anchor of the frame

---

## Character Color Support

### Luma (foreground, lower-left)
- **Skin (UV ambient):** `#A87890` (DRW-11 — lavender-washed warm skin)
- **Skin shadow:** `#5A3A5A` (DRW-12 — deep lavender-plum)
- **Skin highlight (cyan bounce from below):** `#4AB0B0` (DRW-13 — forehead, nose, cheekbones)
- **Hoodie main (UV ambient):** `#C07038` (DRW-14 — orange modified toward magenta-brown by UV)
- **Hoodie lower hem (cyan bounce):** `#5AA8A0` (DRW-15 — practically teal at feet)
- **Hoodie right shoulder (waterfall):** `#9A7AA0` (DRW-16 — complex orange+blue-white mix)
- **Hoodie pixel grid:** `#00F0FF` — matches ambient (she belongs here in some unspoken way)
- **Jeans:** `#263D5A` base, `#2B7FFF` lit seam (waterfall)
- **Hair:** `#3B2820` base + `#7B2FBE` UV rim on crown

### Byte (on Luma's right shoulder)
- **Body fill:** `#00D4E8` (GL-01b Byte Teal) with `#00A8B4` inner glow
- **Circuit traces:** `#00F0FF` — slightly more luminous (he is "home")
- **Cyan eye (facing Luma):** `#00F0FF`
- **Magenta eye (facing void):** `#FF2D6B` (GL-02)
- **No Corrupted Amber outline exception** — UV ambient provides adequate figure-ground separation
  (Byte's dark body reads distinctly against purple background, unlike cyan-dominant SF02)

---

## Saturation Hierarchy (MANDATORY)

Characters > Platform flora > Slab edges > Background structures > Void

- Luma's `#C07038` hoodie (modified): still substantially more saturated than any background zone
- Byte's `#00D4E8` body: more saturated than ENV-09/10 structural fills
- Background structures must NEVER match or exceed character saturation
- Acid Green flora in platform cracks is bright but spatially near — acceptable local saturation peak

---

## Forbidden in This Scene

1. **NO warm light sources.** No lamp glow, no golden-hour window spill, no warm ambient fill.
   Warmth only as carried pigment (Luma's material colors, RW fragments).
2. **NO Soft Gold (`#E8C95A`) or Sunlit Amber (`#D4923A`) in any light source.**
3. **NO Terracotta (`#C75B39`) as an active light.** Only as a corrupted fragment material color.
4. **NO grey or achromatic values** in background fills — all neutrals must have a cyan or UV hue bias.
5. **NO warm-tinted shadows** — shadows trend UV Purple, not brown.
6. **NO Acid Green in storm-confetti format** — flora and pixel only, not storm-density scatter.

---

## Distinctness from SF01 and SF02

| Parameter | SF01 (Warm Room) | SF02 (Glitch Storm) | SF03 (Other Side) |
|---|---|---|---|
| **Key light** | Soft Gold `#E8C95A` | Electric Cyan `#00F0FF` (crack) | UV Purple `#7B2FBE` (ambient void) |
| **Dominant fill** | Warm Cream `#FAF0DC` | Night Sky `#1A1428` | Void Black `#0A0A14` |
| **Accent** | Terracotta `#C75B39` | Hot Magenta `#FF2D6B` | Acid Green `#39FF14` + Cyan circuit |
| **Warm tone presence** | Dominant | Contested (warm windows vs cyan key) | Zero (pigment only) |
| **Atmospheric feel** | Cozy, safe, analog | Violent, contested | Vast, still, alien |
| **Dutch angle** | No | Yes (+4°) | No (level — stillness) |
| **Glitch elements** | One screen, lamp-lit | Full storm, crack event | Ambient radiation, settled |

**Key distinction rule:** If any color in SF03 could plausibly appear in SF01 as an *active light
source*, it is wrong. Audit every light source against this test.

---

## Notes for Jordan Reed

1. The level horizon (no dutch angle) is intentional — use it. The stillness is the mood.
2. The corrupted Real World fragments are storytelling elements — make them readable. The terracotta
   with amber edges must read as "something that belongs somewhere else." Do not let them get lost.
3. Scale communication is the primary compositional job. Use all five depth layers. Make the
   far-distance structures feel enormous by making Luma feel small.
4. Atmospheric perspective is INVERTED: foreground = cyan, saturated; distance = UV Purple, dark.
   This is the opposite of how Real World atmospherics work. Remind yourself constantly.
5. The platform plants (`#39FF14`) are an important warmth-temperature contrast — a small, living,
   bright local element against the vast cold. Do not omit them.

---

*Sam Kowalski — Color & Style Artist — Cycle 14 — 2026-03-30*
