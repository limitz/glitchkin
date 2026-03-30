# Rebuild Spec: LTG_ENV_classroom_bg — Cycle 41
**Author:** Hana Okonkwo
**Date:** 2026-03-30
**Cycle:** 40
**Based on:** C16 critique feedback (Sven: FAIL grade), C40 brief

---

## Current State (C40 QA)
```
Silhouette:  blob
Value range: min=10 max=252 range=242 PASS
Warm/cool:   separation=9.3 FAIL (threshold: 12)
Line weight: mean=414.65px outliers=3 FAIL
Grade:       FAIL
```

## Problems to Solve

### 1. Silhouette reads as blob (CRITICAL)
The classroom background has no strong value contrast zones. Desk rows, wall, and floor blend together — characters placed in the room will merge with desks or walls. Full redesign of value structure needed.

**Fix:**
- Establish a clear value hierarchy: bright walls/ceiling (70-80 value), mid-tone desks/floor (40-60), dark desk shadows/crevices (≤30)
- Use lighting to carve out a clear "character staging zone" where students sit
- Character staging zone (center of desk rows, VP-facing) should be at least 20 value units lighter or darker than character costumes (Luma: warm cream hoodie, Cosmo: lavender)

### 2. Warm/cool separation FAIL (9.3 vs threshold 12)
The dual-source lighting in the current generator is correctly conceived (warm left window, cool right fluorescent) but the execution is too muddy — overlapping patches cancel each other.

**Fix:**
- Hard commit to the dual-source structure: LEFT half warm (SUNLIT_AMBER gradient, max alpha 60), RIGHT half cool (fluorescent blue-green, max alpha 50)
- Do NOT blend/overlap in the center. Clean transition at canvas center.
- After generation, run warmth_inject if still failing. The dual-source split should get there without injection.

### 3. Line weight FAIL (mean=414.65px, outliers=3)
The current generator is producing very thick strokes — likely from large polygon outlines or rectangle borders. Outlines on large shapes should be width=1 or omitted.

**Fix:**
- All outline strokes: width=1 maximum
- Remove any explicit outline from large wall/floor polygons
- Structural lines (floor edge, ceiling edge, window frame): width=1-2
- Desk edges visible at character staging: width=1 with LINE_DARK fill

### 4. Perspective and depth
The camera is back-right 3/4 view. This is correct. Problems to fix:
- Floor tiles must converge properly to the vanishing point (current tiles are nearly horizontal)
- Desk rows must recede in proper perspective: rows are shorter and higher on page toward VP
- Foreground desk corner is MANDATORY as depth anchor (was in spec, may not be rendering correctly)

---

## Architecture Spec

### Canvas
`1280×720px` — switch from 1920×1080 to match all other current environments. 1920 was legacy spec.

### Camera
- 3/4 angle from back-right corner looking toward front-left
- VP_X = int(W * 0.15), VP_Y = int(H * 0.32) — slightly lower than current, gives cleaner desk depth

### Zones
| Zone | Content | Value | Light |
|---|---|---|---|
| Upper wall + ceiling | Fluorescent fixtures, bulletin boards | 70-80 | Fluorescent cool |
| Left wall strip | Windows (3), warm shaft entry | 60-70 | Warm SUNLIT_AMBER |
| Board wall (front) | Chalkboard + equations, teacher desk | 40-55 | Mixed |
| Desk rows | 4 rows, receding perspective | 50-65 | Dual-source |
| Floor | Linoleum tiles, worn path | 55-70 | Floor pools |
| FG anchor | Near desk corner, backpack on floor | 30-50 | Shadow |

### Lighting System
```
LEFT source:  SUNLIT_AMBER (212,146,58) — windows, left wall, warm shaft through windows
RIGHT source: FLUORO_LIGHT (216,232,208) — overhead fixtures, right wall
Split:        Clean at x=W//2. No muddy overlap zone.
```

### Key Details (Inhabitant Evidence — v002 additions to preserve)
- Wear marks on 65% of desks (lighter worn paths)
- Scattered worksheets on 55% of desks
- Forgotten backpack on floor near Luma's desk (BACKPACK_MAIN ~52,88,148)
- Chalk dust near board tray (CHALK_DUST ~200,198,190)
- Water bottle on nearest desk corner

### Required QA Gates Before Submission
1. `render_qa`: silhouette=distinct, warm/cool≥12, line_weight outliers≤1 → PASS or WARN
2. Figure-ground: check Luma hoodie (250,240,220) and Cosmo lavender (168,155,191) vs desk fill — need ≥20 value units separation
3. Value floor ≤30 confirmed via `render_qa min`

---

## Execution Notes for C41
- **New script**: `LTG_TOOL_bg_classroom_v002.py` (overwrite existing file — git tracks history)
- Import `LTG_TOOL_render_lib` for `light_shaft()`, `vignette()`, `scanline_overlay()` (classroom fluorescents warrant subtle scanline)
- Use seeded RNG (seed=44)
- Reference `output/color/palettes/master_palette.md` for canonical colors
