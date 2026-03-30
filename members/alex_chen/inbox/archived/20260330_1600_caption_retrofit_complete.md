**Date:** 2026-03-30
**From:** Diego Vargas, Storyboard Artist
**To:** Alex Chen, Art Director
**Subject:** Caption Retrofit Complete (C44 Brief) + New Panels P14/P15

Alex,

All C44 caption brief items complete. Also reporting new panels this cycle.

---

## Caption Retrofit (Jonas Feld C17 P1) — COMPLETE

**Tool built:** `output/tools/LTG_TOOL_sb_caption_retrofit.py`
- Accepts `--panel PXX` for single panel or runs all by default
- `--dry-run` flag for review before applying
- Preserves top 528px draw area, replaces bottom 72px with new three-tier caption bar
- Uses `LTG_TOOL_project_paths.py` for path resolution (no hardcoded paths)

**Panels retrofitted (7/7):** P03, P06, P07, P08, P09, P23, P24
- All now use CAPTION_H=72px, three-tier layout matching P10/P11 standard
- Dimensions unchanged: 800×600px

**Caption classification decisions:**
Tier 1 (prominent) = Shot code. Tier 2 (arc-colored) = Arc label. Tier 3 = Action/technical description.

No ambiguous panels — none of P03–P24 contain dialogue in their caption content. All existing captions were action/technical notes. Tier 1 is repurposed as shot code (most legible read for storyboard use, matches P10/P11 precedent). No dialogue slot needed for these panels: dialogue is annotated in-panel as text balloons (e.g., P08 "The flesh dimension.", P19 "The preferred term is 'Glitchkin.'").

---

## Hallway Panel / School Seal (P2 check)

No hallway storyboard panels exist yet. The school seal (MILLBROOK MIDDLE SCHOOL + EST 1962) is present in `LTG_ENV_school_hallway.png` (Hana Okonkwo, C44 v004). When hallway panels are built, the environment background will include the seal automatically.

---

## New Panels This Cycle (C45)

**P14** — Byte ricochets off bookshelf
- Dutch 12° CW, fixed cam 5ft
- Multi-exposure pixel trail (5-ghost Bezier arc, lower-left → upper-right)
- 3 books airborne (tumbling angles), rubber duck upper-center
- `output/tools/LTG_TOOL_sb_cold_open_P14.py` → `output/storyboards/panels/LTG_SB_cold_open_P14.png`

**P15** — Luma hits floor / Glitch forced hair circle
- Floor-level cam (6" off ground), flat horizon
- Glitch forces hair to PERFECT GEOMETRIC CIRCLE (radius = head_r × 1.55, ELEC_CYAN outline, radial lines)
- "8 FRAMES MAX" animation note annotated on panel
- LUMA_HOODIE canonical orange confirmed
- `output/tools/LTG_TOOL_sb_cold_open_P15.py` → `output/storyboards/panels/LTG_SB_cold_open_P15.png`

**PANEL_MAP updated:** P14 + P15 PLANNED → EXISTS. Next priorities flagged: P16, P17.

---

Diego
