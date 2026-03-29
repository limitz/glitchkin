# Character Export Manifest — "Luma & the Glitchkin"

**Prepared by:** Maya Santos, Character Designer
**Date:** 2026-03-29
**Cycle:** 23
**Status:** Pitch-Ready Export Set

---

## QC Pass Summary (Cycle 23)

QC performed against `output/production/character_sheet_standards_v001.md`.
All exports checked for: show_guides=False, format (RGB PNG), canvas dimensions,
expression count, grid layout, turnaround completeness, and color model presence.

---

## Luma

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_luma_expression_sheet_v004.png` | 1200×900 | RGB PNG | PITCH-READY |
| Expression Sheet (guides ref) | `LTG_CHAR_luma_expression_sheet_v004_guides.png` | 1200×900 | RGB PNG | PRODUCTION REF (not pitch export) |
| Turnaround | `turnarounds/LTG_CHAR_luma_turnaround_v001.png` | 720×346 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COL_luma_colormodel_v001.png` | confirmed | RGB PNG | PITCH-READY |

**Expressions:** CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED (6 — 3×2 grid)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** OFF on pitch export (`_v004.png`). Guides export preserved as production ref.

**QC notes:** All standards met. show_guides=False confirmed on pitch file. Brow weight fix (v003→v004: 10px→4px at 2×) applied. CURIOUS forward lean and brow asymmetry confirmed. DELIGHTED arm-raised silhouette differentiator confirmed.

---

## Byte

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_byte_expression_sheet_v004.png` | 784×1074 | RGB PNG | PITCH-READY |
| Cracked Eye Glyph | `LTG_CHAR_byte_cracked_eye_glyph_v001.png` | confirmed | RGB PNG | PITCH-READY |
| Turnaround | `turnarounds/LTG_CHAR_byte_turnaround_v001.png` | 720×346 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COL_byte_colormodel_v001.png` | confirmed | RGB PNG | PITCH-READY |

**Expressions:** NEUTRAL/DEFAULT, GRUMPY, SEARCHING, ALARMED, SMUG, RELUCTANT JOY, POWERED DOWN, RESIGNED, STORM/CRACKED (9 — 3×3 grid)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** No guide flag in Byte generator — clean render confirmed.

**QC notes:** Standards compliant. 3×3 grid upgrade from v002 correctly retained. Section 9B glyph spec confirmed: DIM_PX=(0,80,100), crack as void-black LINE overlay (not pixel state), HOT_MAG restricted to body/frame exterior. STORM arm asymmetry (arm_l_dy=6, arm_r_dy=22 — 20+ unit differential) confirmed. RELUCTANT JOY arm_l_dy=-2 (resistance signal) confirmed. Body fill GL-01b #00D4E8 throughout. NOTE: Non-standard canvas size (784×1074) is a pre-standards grandfathered exception per standards document policy.

---

## Cosmo

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_cosmo_expression_sheet_v004.png` | 912×946 | RGB PNG | PITCH-READY |
| Turnaround | `turnarounds/LTG_CHAR_cosmo_turnaround_v002.png` | 720×346 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COL_cosmo_colormodel_v001.png` | confirmed | RGB PNG | PITCH-READY |

**Expressions:** NEUTRAL/OBSERVING, FRUSTRATED/DEFEATED, DETERMINED, SKEPTICAL/ONE-BROW-UP, WORRIED, SURPRISED (6 — 3×2 grid)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** No guide flag in Cosmo generator — clean render confirmed.

**QC notes:** Standards compliant (canvas size grandfathered — pre-standards). Lean formula fix confirmed: tilt_off = body_tilt × 2.5. SKEPTICAL arm posture fix confirmed: arms at near-neutral (arm_l_dy=2, arm_r_dy=2) + body_squash=0.92. No arms-raised false alarm. Glasses at 7° tilt (canonical). Notebook under left arm in applicable shots.

---

## Grandma Miri

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_grandma_miri_expression_sheet_v002.png` | 1200×900 | RGB PNG | PITCH-READY |
| Turnaround | `turnarounds/LTG_CHAR_miri_turnaround_v001.png` | 1600×800 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COL_miri_colormodel_v001.png` | confirmed | RGB PNG | PITCH-READY |

**Expressions:** WARM/WELCOMING, SKEPTICAL/AMUSED, CONCERNED, SURPRISED/DELIGHTED, WISE/KNOWING (5 — 3×2 grid, last panel intentionally used per standards)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** No guide flag in Miri generator — clean render confirmed.

**QC notes:** Standards compliant. 1600×800 turnaround is above minimum standard — accepted. Line weight Warm Dark Brown (#4A2810) confirmed distinct from Deep Cocoa. Permanent cheek blush present on warm states, removed on CONCERNED (canonical). Crow's feet at detail weight (2px at 2× render). Body posture differentiation per expression confirmed (Cycle 19 unique-silhouette rule applied).

---

## Glitch (Antagonist) — NEW Cycle 23

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_glitch_expression_sheet_v001.png` | 800×800 | RGB PNG | PITCH-READY |
| Turnaround | `turnarounds/LTG_CHAR_glitch_turnaround_v001.png` | 1600×700 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COLOR_glitch_color_model_v001.png` | 800×500 | RGB PNG | PITCH-READY |

**Expressions:** NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT (4 — 2×2 grid)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** OFF — pitch export confirmed.

**QC notes:** New character — v001 asset set. Primary color GL-07 CORRUPT_AMBER #FF8C00 confirmed throughout. Secondary: HOT_MAGENTA #FF2D6B crack lines (body exterior scar, consistent with Byte spec conventions). UV_PURPLE #7B2FBE shadow fills. Diamond/rhombus body shape — angular antagonist contrast to protagonist characters. 3×3 pixel dual-eye system (left eye: primary glyph, right eye: destabilized bleed variant). VOID_BLACK #0A0A14 outline (digital entity standard). Hover confetti: HOT_MAG + UV_PURPLE (corrupted, not friendly cyan/acid). 2×2 grid appropriate for 4-expression sheet per show flexibility rules. Canvas 2× internal render, LANCZOS downsample to 1×.

---

## Character Design Summary Table

| Character | Expression Sheet | Grid | Count | Turnaround | Color Model | Pitch Status |
|---|---|---|---|---|---|---|
| Luma | v004 | 3×2 | 6 | v001 (4-view) | v001 | PITCH-READY |
| Byte | v004 | 3×3 | 9 | v001 (4-view) | v001 | PITCH-READY |
| Cosmo | v004 | 3×2 | 6 | v002 (4-view) | v001 | PITCH-READY |
| Grandma Miri | v002 | 3×2 | 5 | v001 (4-view) | v001 | PITCH-READY |
| Glitch | v001 | 2×2 | 4 | v001 (4-view) | v001 | PITCH-READY |

---

## Generator Registry

| Generator | Output | Location |
|---|---|---|
| `LTG_CHAR_luma_expression_sheet_v004.py` | Luma expr sheet v004 | `output/tools/` |
| `LTG_CHAR_byte_expression_sheet_v004.py` | Byte expr sheet v004 | `output/tools/` |
| `LTG_CHAR_cosmo_expression_sheet_v004.py` | Cosmo expr sheet v004 | `output/tools/` |
| `LTG_CHAR_glitch_expression_sheet_v001.py` | Glitch expr sheet v001 | `output/tools/` |
| `LTG_CHAR_glitch_turnaround_v001.py` | Glitch turnaround v001 | `output/tools/` |
| `LTG_CHAR_glitch_color_model_v001.py` | Glitch color model v001 | `output/tools/` |
| `LTG_TOOL_miri_turnaround_v001.py` | Miri turnaround v001 | `output/tools/` |

---

## Excluded from Pitch Export

- `LTG_CHAR_luma_expression_sheet_v004_guides.png` — construction guides visible, production reference only
- All `_v001`, `_v002`, `_v003` prior-version sheets — superseded, retained for history

---

*character_export_manifest_v001.md — Maya Santos, Character Designer*
*Cycle 23 — 2026-03-29*
