<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Lineup Tier Depth Indicator — Staging Recommendation
**Author:** Lee Tanaka, Character Staging & Visual Acting Specialist
**Cycle:** 45
**Date:** 2026-03-30
**Responding to:** Alex Chen C44 brief — Lineup v008 two-tier depth indicator band

---

## Current State

Character lineup v008 (Maya C42) establishes two ground tiers:
- **FG tier** (Luma + Byte): `GROUND_Y = IMG_H × 0.78` (~436px at IMG_H=560)
- **BG tier** (Cosmo + Miri + Glitch): `GROUND_Y = IMG_H × 0.70` (~392px at IMG_H=560)

Delta between tiers: **~44px** at a 560px canvas height. That gap is visible at full resolution
but compresses to near-invisible at thumbnail scale (≤10px at typical contact sheet cell size).
Without a tonal cue at each ground line, critics reading a printed pitch deck can read the
tier offset as inconsistent drawing rather than intentional staging depth.

Sketch showing all three options: `output/production/lineup_tier_depth_sketch.png`

---

## Options Evaluated

### A — Thin Horizontal Rule (between tiers)
A single 1px warm-gray rule drawn at the midpoint between BG_GROUND_Y and FG_GROUND_Y.

**Assessment: NOT RECOMMENDED.**
- The 44px tier gap is already close. A single line midway between them implies a floor boundary,
  not a depth recede — it reads as a stage mark, not an atmospheric cue.
- At thumbnail scale, the rule disappears entirely (sub-pixel).
- In B&W print it reads as a construction line, not a designed element.

### B — Atmospheric Haze Band (between tiers, ≤20% alpha)
A soft low-alpha fog strip blending across the zone between BG_GROUND_Y and FG_GROUND_Y.

**Assessment: PARTIAL — works in color, marginal in print.**
- Warm-white haze between tiers does read spatially in a full-color presentation.
- In B&W print at reduced scale, the alpha value is indistinguishable from the neutral BG.
- Haze runs the risk of obscuring the leg/foot geometry of BG characters (Glitch in
  particular is already shorter — the haze eats his lower body at smaller sizes).
- Would require Rin or Maya to implement as an alpha-composite pass in the generator,
  which is non-trivial given the character draw order (BG chars must render through the haze).

### C — Dual-Warmth Drop-Shadow Bands per Tier (RECOMMENDED)
A short (8–10px) gradient shadow band drawn beneath each tier's ground line:
- **BG tier shadow:** cool slate gradient fading downward from BG_GROUND_Y
- **FG tier shadow:** warm amber gradient fading downward from FG_GROUND_Y

**Assessment: RECOMMENDED.**
- Warm/cool tonal contrast reads at thumbnail scale, in print, and in B&W.
- Aligns directly with the project's established warm/cool palette grammar:
  warm = proximity/real/foreground; cool = distance/digital/background.
  The FG tier being warmer than the BG tier is character-accurate (Luma + Byte are the
  warm-real protagonists; Cosmo, Miri, and Glitch are spatially behind them).
- Implemented as two simple gradient fill loops drawn BEFORE characters — no draw-order
  complications, no alpha composite pass required.
- Shadow bands are ≤10px tall — they are below all character geometry and cannot obscure
  any feet, tails, or floating offsets.
- The dual-temperature read teaches the eye: warm line = close, cool line = far.
  It encodes depth without requiring any text annotation.

---

## Implementation Spec (for Maya Santos)

**Location in generator:** Draw shadow bands immediately after filling panel BG,
before any character draw call.

```python
# BG tier drop-shadow (cool slate)
_BG_SHADOW_COL   = (180, 195, 210)   # cool slate
_BG_SHADOW_H     = 8                  # px

for row in range(_BG_SHADOW_H):
    alpha_frac = 1.0 - row / _BG_SHADOW_H    # fades to 0 downward
    r = int(_BG_SHADOW_COL[0] + (BG[0] - _BG_SHADOW_COL[0]) * (1 - alpha_frac))
    g = int(_BG_SHADOW_COL[1] + (BG[1] - _BG_SHADOW_COL[1]) * (1 - alpha_frac))
    b = int(_BG_SHADOW_COL[2] + (BG[2] - _BG_SHADOW_COL[2]) * (1 - alpha_frac))
    draw.line([(0, BG_GROUND_Y + row), (IMG_W, BG_GROUND_Y + row)], fill=(r, g, b), width=1)

# FG tier drop-shadow (warm amber)
_FG_SHADOW_COL   = (220, 200, 160)   # warm amber
_FG_SHADOW_H     = 10                 # px

for row in range(_FG_SHADOW_H):
    alpha_frac = 1.0 - row / _FG_SHADOW_H
    r = int(_FG_SHADOW_COL[0] + (BG[0] - _FG_SHADOW_COL[0]) * (1 - alpha_frac))
    g = int(_FG_SHADOW_COL[1] + (BG[1] - _FG_SHADOW_COL[1]) * (1 - alpha_frac))
    b = int(_FG_SHADOW_COL[2] + (BG[2] - _FG_SHADOW_COL[2]) * (1 - alpha_frac))
    draw.line([(0, FG_GROUND_Y + row), (IMG_W, FG_GROUND_Y + row)], fill=(r, g, b), width=1)
```

Colors use existing lineup palette — no new palette entries required.

**Annotation bar:** Add "WARM = FG / COOL = BG" to the tier label in the annotation band.
This makes the grammar explicit for pitch reviewers.

---

## Face Test Gate

No face geometry changes. Gate not triggered by this implementation. No tool run required.

---

## Risk Assessment

- **None.** Both shadow bands are drawn below the feet/float level of all characters.
  The only visual territory they occupy is the narrow band between the ground line and
  the label area. The existing 2px SHADOW_LINE elements (current v008) can be retained
  alongside the gradient bands or replaced — either works.
- **Thumbnail stability:** At 64px cell height (arc-diff thumbnail scale), both shadow bands
  remain visible as tonal differentiation. PASS expected on arc-diff comparison.

---

## Sketch Reference

`output/production/lineup_tier_depth_sketch.png` — 1232×546px, 3-panel comparison.
Left panel = Option A, center = Option B, right = Option C (recommended).
All panels use stub silhouettes at correct tier geometry.
