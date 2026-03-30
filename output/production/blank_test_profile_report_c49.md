<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Visual Blank Test — Panel-Type Profile Report (C49)

**Author:** Diego Vargas
**Date:** 2026-03-30
**Tool:** `output/tools/LTG_TOOL_visual_blank_test.py`

## Summary

Added 6 panel-type profiles (ECU, MCU, WIDE, INSERT, OTS, TWO_SHOT) to the visual blank test tool. Each profile adjusts thresholds for all 6 checks based on what is visually expected for that shot type. Auto-detection assigns profiles from the PANEL_TYPE_MAP.

## Reclassification Results

21 panels tested. Comparison: DEFAULT thresholds (C48) vs. profiled thresholds (C49).

| Panel | Type | DEFAULT (C48) | Profiled (C49) | Change |
|-------|------|---------------|----------------|--------|
| P03   | ECU      | WARN | PASS | UPGRADED |
| P06   | ECU      | FAIL | WARN | UPGRADED |
| P07   | WIDE     | WARN | WARN | — |
| P08   | MCU      | WARN | WARN | — |
| P09   | WIDE     | WARN | PASS | UPGRADED |
| P10   | OTS      | WARN | WARN | — |
| P11   | ECU      | FAIL | WARN | UPGRADED |
| P13   | TWO_SHOT | FAIL | FAIL | — |
| P14   | MCU      | FAIL | FAIL | — |
| P15   | MCU      | FAIL | FAIL | — |
| P16   | ECU      | WARN | WARN | — |
| P17   | TWO_SHOT | FAIL | FAIL | — |
| P18   | INSERT   | WARN | PASS | UPGRADED |
| P19   | TWO_SHOT | WARN | WARN | — |
| P20   | TWO_SHOT | FAIL | FAIL | — |
| P21   | WIDE     | WARN | PASS | UPGRADED |
| P22   | ECU      | WARN | PASS | UPGRADED |
| P22a  | MCU      | WARN | WARN | — |
| P23   | OTS      | PASS | PASS | — |
| P24   | WIDE     | PASS | PASS | — |
| EP05  | TWO_SHOT | WARN | WARN | — |

## Reclassification Summary

- **7 panels upgraded** (false WARNs/FAILs resolved by appropriate profile):
  - P03 (ECU): WARN -> PASS (depth cue threshold relaxed for ECU)
  - P06 (ECU): FAIL -> WARN (silhouette contrast threshold relaxed — internal contrast carries)
  - P09 (WIDE): WARN -> PASS (internal contrast recognized)
  - P11 (ECU): FAIL -> WARN (ECU face panel — quadrant spread and depth cues relaxed)
  - P18 (INSERT): WARN -> PASS (prop panel — no depth cue or character presence required)
  - P21 (WIDE): WARN -> PASS (wide shot — internal contrast carries)
  - P22 (ECU): WARN -> PASS (ECU screen panel — relaxed thresholds appropriate)

- **0 panels downgraded** (no panel that previously passed now fails)

- **5 panels remain FAIL** (genuine edge density issues — C4):
  - P13 (TWO_SHOT): edge density 0.7 — characters may be too smooth/low-contrast
  - P14 (MCU): edge density 1.5 — borderline, action panel with large flat fills
  - P15 (MCU): edge density 1.2 — floor-level panel, large flat floor area
  - P17 (TWO_SHOT): edge density 1.3 — stillness beat, intentionally quiet composition
  - P20 (TWO_SHOT): edge density 0.6 — names-exchanged beat, very quiet panel

## Analysis

The FAILs are all on C4 (Character Presence / edge density). These panels have stylistically low edge detail — large smooth fills, quiet compositions, or simplified forms at MED scale. This is not necessarily a rendering error. The edge density metric measures gradient magnitude, so panels with broad flat character fills and minimal internal detail will score low.

**Recommendation:** C4 thresholds for TWO_SHOT may need further tuning once more panels exist. Alternatively, a secondary C4 method using color-cluster detection (distinct hue regions in character zones) could supplement edge density for panels with smooth cel-shaded style.

## Batch Summary by Type

| Type       | PASS | WARN | FAIL |
|------------|------|------|------|
| ECU        | 2    | 3    | 0    |
| INSERT     | 1    | 0    | 0    |
| MCU        | 0    | 2    | 2    |
| OTS        | 1    | 1    | 0    |
| TWO_SHOT   | 0    | 2    | 3    |
| WIDE       | 3    | 1    | 0    |
