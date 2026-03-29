# Statement of Work — Cycle 17
**Date:** 2026-03-29
**Work Cycles Completed:** 17
**Next Critique:** After Cycle 18 (Critique Cycle 9)

---

## Objectives This Cycle

1. Address producer concern about character refinement depth
2. Complete missing Act 2 storyboard panels (A2-01, A2-05, A2-08)
3. Build missing Act 2 environments (Tech Den, School Hallway)
4. Create Grandma Miri expression sheet (gap in pitch package)
5. Produce refined Luma expression sheet v002

---

## Deliverables

### Alex Chen — Art Direction
- `output/production/char_refinement_directive_c17.md` — Full character refinement standards doc covering construction clarity, 3-tier line weight system, thumbnail readability (Dmitri's 10% squint test), on-model consistency. Identifies 3 critical gaps; provides specific direction for Maya Santos.

### Sam Kowalski — Color & Style
- `output/characters/color_models/LTG_COLOR_grandma_miri_color_model_v001.png` — Full 23-swatch color model sheet (7 groups: Skin, Eyes, Hair, Cardigan, Glasses, Pants, Slippers)
- `output/color/palettes/act2_environments_color_brief.md` — RGB specs for Tech Den (9 surfaces) and School Hallway (11 surfaces). Includes key rule: monitor glow R-channel floor of 150 prevents GL color misread.
- Updated `output/characters/color_models/grandma_miri_color_model.md` with glasses spec, lighting rules

### Jordan Reed — Backgrounds
- `output/backgrounds/environments/LTG_ENV_tech_den_v001.png` — Cosmo's tech workspace, daylight + monitor glow, real-world palette
- `output/backgrounds/environments/LTG_ENV_school_hallway_v001.png` — 3-point perspective, institutional fluorescent, sage/blue-gray alternating lockers

### Lee Tanaka — Storyboard
- `output/storyboards/act2/panels/LTG_SB_act2_panel_a201_v001.png` — Tech Den wide establishing (Cosmo FOCUSED / Luma DETERMINED)
- `output/storyboards/act2/panels/LTG_SB_act2_panel_a205_v001.png` — Millbrook street medium two-shot (Luma ENTHUSIASTIC / Cosmo SKEPTICAL)
- `output/storyboards/act2/panels/LTG_SB_act2_panel_a208_v001.png` — Grandma Miri ECU, SURPRISED→KNOWING, CRT catch light
- `output/storyboards/act2/LTG_SB_act2_contact_sheet_v004.png` — Full 11-panel Act 2 arc (3-row layout, arc-color borders)

### Maya Santos — Character Design
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v002.png` — Refined 6-expression sheet (CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED). Construction guides visible, 3-tier line weight, hair shape language.
- `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v001.png` — 5-expression sheet (WARM/WELCOMING, NOSTALGIC/WISTFUL, CONCERNED, SURPRISED/DELIGHTED, WISE/KNOWING). Crown/glasses/crow's feet/smile lines as canonical silhouette anchors.

---

## Act 2 Storyboard Status (End of Cycle 17)

**Complete (11 panels):**
- A1-04 — classroom near-miss
- A2-01 — Tech Den wide *(NEW C17)*
- A2-02 — Byte MCU / VULNERABLE
- A2-03 — Cosmo SKEPTICAL, restaged (v002)
- A2-04 — Montage + Byte refusal (v002)
- A2-05 — Millbrook street walk-and-talk *(NEW C17)*
- A2-05b — Cosmo with app
- A2-06 MED — Hopeful two-shot (v001)
- A2-06 INSERT — Phone crash
- A2-07 — Byte RESIGNED ECU (v002)
- A2-08 — Grandma Miri returns *(NEW C17)*

**Act 2 storyboard deck is now COMPLETE.**

---

## Environment Status (End of Cycle 17)

| Environment | File | Status |
|-------------|------|--------|
| Glitch Layer | LTG_ENV_glitchlayer_* | Done |
| Other Side (SF03 BG) | LTG_ENV_other_side_bg_v002 | Done |
| Luma's House Study | LTG_ENV_lumashome_study_interior_v001 | Done |
| Grandma's Kitchen | LTG_ENV_grandma_kitchen_v001 | Done |
| Classroom | LTG_ENV_classroom_bg_v002 | Done |
| Tech Den | LTG_ENV_tech_den_v001 | **NEW C17** |
| School Hallway | LTG_ENV_school_hallway_v001 | **NEW C17** |

---

## Tools Added This Cycle
- `LTG_TOOL_grandma_miri_color_model_v001.py`
- `LTG_TOOL_bg_tech_den_v001.py`
- `LTG_TOOL_bg_school_hallway_v001.py`
- `LTG_TOOL_sb_panel_a201_v001.py`
- `LTG_TOOL_sb_panel_a205_v001.py`
- `LTG_TOOL_sb_panel_a208_v001.py`
- `LTG_TOOL_sb_act2_contact_sheet_v004.py`
- `LTG_TOOL_luma_expression_sheet_v002.py`
- `LTG_TOOL_grandma_miri_expression_sheet_v001.py`
