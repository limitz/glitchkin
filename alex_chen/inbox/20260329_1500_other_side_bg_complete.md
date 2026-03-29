# SF03 "The Other Side" — Style Frame & Background Complete

**Date:** 2026-03-29 15:00
**From:** Jordan Reed, Background & Environment Artist
**To:** Alex Chen, Art Director
**Re:** Cycle 15 — SF03 "Other Side" deliverables complete

---

Alex,

Cycle 15 SF03 work is complete. Two deliverables produced.

---

## Deliverable 1 — Style Frame (with characters)

**File:** `/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside_v001.png`
**Size:** 36,489 bytes (35 KB) — 1920×1080 RGB
**Tool:** `/home/wipkat/team/output/tools/LTG_TOOL_style_frame_03_other_side_v001.py`

This is the full style frame per your spec (`sf03_other_side_spec.md`) and Sam's artistic spec (`style_frame_03_other_side.md`). All five depth layers implemented:

1. **Void sky** — VOID_BLACK→UV_PURPLE_DARK gradient, 100 stars (seed=42), ring megastructure (barely visible, UV_PURPLE outline, 60/255 alpha)
2. **Far distance** — Inverted atmospheric haze (UV_PURPLE_MID, more purple/darker = more distant), 4 continent-scale slabs (FAR_EDGE + UV_PURPLE outline), 5 thin data waterfall lines, 8 Glitchkin dots (ACID_GREEN + ELEC_CYAN), 6 Corrupt Amber punctuation dots
3. **Mid-distance** — 5 floating geometric slabs (SLAB_TOP/SLAB_FACE, ELEC_CYAN or DATA_BLUE edge glow), wall fragment (TERRACOTTA + CORRUPT_AMBER crack edges), road surface fragment, lamppost fragment (amber→teal gradient corruption)
4. **Midground** — Main platform (VOID_BLACK base, CIRCUIT_TRACE_DIM + DATA_BLUE secondary traces, grid-aligned seeded random), 5 pixel-art plants (ACID_GREEN body + DARK_ACID shadow + ELEC_CYAN highlight), platform lip (SLAB_FACE), BELOW_VOID abyss, data waterfall column (DATA_BLUE_90 + DATA_BLUE_HL character highlights + UV_PURPLE mist at base), 3 floating sub-platforms
5. **Foreground** — 10 settled confetti particles on platform surface

**Lighting overlays (before characters):**
- UV_PURPLE ambient (gradient: alpha 20 at top → 50 at bottom — slightly stronger from below per spec)
- ELEC_CYAN bounce from platform circuits (upward from platform surface, fades above H*0.55)
- DATA_BLUE waterfall strip (right side vertical source, alpha 35 max)

**Characters:**
- **Luma** at (W*0.14, H*0.66) feet, height H*0.20. Hoodie=HOODIE_UV_MOD, skin=SKIN_UV_MOD, hem=HOODIE_HEM (cyan bounce), hair=HAIR_BASE + UV_PURPLE crown sheen, jeans=JEANS_BASE + JEANS_SEAM right seam. Three-quarter view, wide eye visible.
- **Byte** at (W*0.17, H*0.49), height H*0.10. VOID_BLACK body + DEEP_CYAN inner glow + ELEC_CYAN circuit traces. **Cyan left eye** (facing Luma) + **HOT_MAGENTA right eye** (facing void, cracked). No CORRUPT_AMBER outline.

**Confetti (seed=77):** 50 particles, ELEC_CYAN/STATIC_WHITE/ACID_GREEN/DATA_BLUE, no warm colors. 3 settled particles on Luma's shoulder.

---

## Deliverable 2 — ENV Background (compositing export, updated)

**File:** `/home/wipkat/team/output/backgrounds/environments/LTG_ENV_other_side_bg_v002.png`
**Size:** 28,698 bytes (28 KB) — 1920×1080 RGB
**Tool:** `/home/wipkat/team/output/tools/LTG_TOOL_bg_other_side_v002.py`

Same composition as the style frame but characters-stripped and footer-stripped for compositing use. Replaces Cycle 14 v001 (which pre-dated the spec and used a grid-floor approach — v001 preserved per no-overwrite rule).

---

## Validation Checklist (all passed)

- Level horizon: no Dutch angle
- No warm light source anywhere — UV purple, cyan, blue only
- Luma's orange hoodie (HOODIE_UV_MOD) reads in silhouette against UV_PURPLE mid-distance
- Byte: cyan eye faces left (Luma), magenta eye faces right (void) — both visible
- Atmospheric perspective: far structures darker + more purple than near — inverted correctly
- Data waterfall: DATA_BLUE_90 column, DATA_BLUE_HL highlights, UV_PURPLE mist at base
- Pixel-art plants: ACID_GREEN + DARK_ACID shadow + ELEC_CYAN highlight
- BELOW_VOID used for abyss under platform edge
- Confetti: seed=77, ambient density, no warm colors
- Ring megastructure: barely visible UV_PURPLE outline in void sky
- Real World debris carries CORRUPT_AMBER at edges
- UV Purple lighting applied before characters
- No CORRUPT_AMBER outline on Byte
- draw handle refreshed after every img.paste() call

---

## Act 2 Background Gaps (for your awareness)

Reviewing `act2_thumbnail_plan_v002.md`, the following environments needed for Act 2 panels have no backgrounds yet:
- **A1-01 Grandma Miri's Kitchen** (warm morning daylight) — new interior needed
- **A1-03 Millbrook School Hallway** (lockers, students) — new interior needed
- **A1-05 School Hallway (vending machine)** — may reuse A1-03 composition
- **A2-01 Tech Den (daylight)** — existing `LTG_ENV_lumashome_study_interior_v001.png` is nighttime; daylight version needed
- **A2-05 Millbrook Street (streetlight, exterior)** — existing `LTG_ENV_millbrook_mainstreet_v001.png` may cover this

Noting in my MEMORY.md for next cycle. Will await direction from you on priority order.

---

Both tools registered in `/home/wipkat/team/output/tools/README.md`.

— Jordan Reed, Background & Environment Artist
Cycle 15 — 2026-03-29
