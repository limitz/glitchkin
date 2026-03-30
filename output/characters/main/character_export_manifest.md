<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Character Export Manifest — "Luma & the Glitchkin"

**Prepared by:** Maya Santos, Character Designer
**Date:** 2026-03-29
**Cycle:** 23
**Status:** Pitch-Ready Export Set

---

## QC Pass Summary (Cycle 23)

QC performed against `output/production/character_sheet_standards.md`.
All exports checked for: show_guides=False, format (RGB PNG), canvas dimensions,
expression count, grid layout, turnaround completeness, and color model presence.

---

## Luma

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_luma_expression_sheet.png` | 1200×900 | RGB PNG | PITCH-READY |
| Expression Sheet (guides ref) | `LTG_CHAR_luma_expression_sheet_guides.png` | 1200×900 | RGB PNG | PRODUCTION REF (not pitch export) |
| Turnaround | `turnarounds/LTG_CHAR_luma_turnaround.png` | 720×346 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COL_luma_colormodel.png` | confirmed | RGB PNG | PITCH-READY |

**Expressions:** CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED (6 — 3×2 grid)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** OFF on pitch export (`_v004.png`). Guides export preserved as production ref.

**QC notes:** All standards met. show_guides=False confirmed on pitch file. Brow weight fix (v003→v004: 10px→4px at 2×) applied. CURIOUS forward lean and brow asymmetry confirmed. DELIGHTED arm-raised silhouette differentiator confirmed.

---

## Byte

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_byte_expression_sheet.png` | 784×1074 | RGB PNG | PITCH-READY |
| Cracked Eye Glyph | `LTG_CHAR_byte_cracked_eye_glyph.png` | confirmed | RGB PNG | PITCH-READY |
| Turnaround | `turnarounds/LTG_CHAR_byte_turnaround.png` | 720×346 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COL_byte_colormodel.png` | confirmed | RGB PNG | PITCH-READY |

**Expressions:** NEUTRAL/DEFAULT, GRUMPY, SEARCHING, ALARMED, SMUG, RELUCTANT JOY, POWERED DOWN, RESIGNED, STORM/CRACKED (9 — 3×3 grid)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** No guide flag in Byte generator — clean render confirmed.

**QC notes:** Standards compliant. 3×3 grid upgrade from v002 correctly retained. Section 9B glyph spec confirmed: DIM_PX=(0,80,100), crack as void-black LINE overlay (not pixel state), HOT_MAG restricted to body/frame exterior. STORM arm asymmetry (arm_l_dy=6, arm_r_dy=22 — 20+ unit differential) confirmed. RELUCTANT JOY arm_l_dy=-2 (resistance signal) confirmed. Body fill GL-01b #00D4E8 throughout. NOTE: Non-standard canvas size (784×1074) is a pre-standards grandfathered exception per standards document policy.

---

## Cosmo

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_cosmo_expression_sheet.png` | 912×946 | RGB PNG | PITCH-READY |
| Turnaround | `turnarounds/LTG_CHAR_cosmo_turnaround.png` | 720×346 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COL_cosmo_colormodel.png` | confirmed | RGB PNG | PITCH-READY |

**Expressions:** NEUTRAL/OBSERVING, FRUSTRATED/DEFEATED, DETERMINED, SKEPTICAL/ONE-BROW-UP, WORRIED, SURPRISED (6 — 3×2 grid)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** No guide flag in Cosmo generator — clean render confirmed.

**QC notes:** Standards compliant (canvas size grandfathered — pre-standards). Lean formula fix confirmed: tilt_off = body_tilt × 2.5. SKEPTICAL arm posture fix confirmed: arms at near-neutral (arm_l_dy=2, arm_r_dy=2) + body_squash=0.92. No arms-raised false alarm. Glasses at 7° tilt (canonical). Notebook under left arm in applicable shots.

---

## Grandma Miri

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_grandma_miri_expression_sheet.png` | 1200×900 | RGB PNG | PITCH-READY |
| Turnaround | `turnarounds/LTG_CHAR_miri_turnaround.png` | 1600×800 | RGB PNG | PITCH-READY |
| Color Model | `../color_models/LTG_COL_miri_colormodel.png` | confirmed | RGB PNG | PITCH-READY |

**Expressions:** WARM/WELCOMING, SKEPTICAL/AMUSED, CONCERNED, SURPRISED/DELIGHTED, WISE/KNOWING (5 — 3×2 grid, last panel intentionally used per standards)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** No guide flag in Miri generator — clean render confirmed.

**QC notes:** Standards compliant. 1600×800 turnaround is above minimum standard — accepted. Line weight Warm Dark Brown (#4A2810) confirmed distinct from Deep Cocoa. Permanent cheek blush present on warm states, removed on CONCERNED (canonical). Crow's feet at detail weight (2px at 2× render). Body posture differentiation per expression confirmed (Cycle 19 unique-silhouette rule applied).

---

## Glitch (Antagonist) — Cycle 23/24

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Expression Sheet | `LTG_CHAR_glitch_expression_sheet.png` | 1200×900 | RGB PNG | PITCH-READY |
| Expression Sheet (superseded) | `LTG_CHAR_glitch_expression_sheet.png` | 800×800 | RGB PNG | SUPERSEDED |
| Turnaround | `turnarounds/LTG_CHAR_glitch_turnaround.png` | 1600×700 | RGB PNG | PITCH-READY |
| Turnaround (superseded) | `turnarounds/LTG_CHAR_glitch_turnaround.png` | 1600×700 | RGB PNG | SUPERSEDED (shadow contrast issues) |
| Color Model | `../color_models/LTG_COLOR_glitch_color_model.png` | 800×500 | RGB PNG | PITCH-READY |

**Expressions:** NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT, STUNNED, CALCULATING (6 — 3×2 grid)
**Turnaround views:** FRONT, 3/4, SIDE, BACK (4 views)
**show_guides:** OFF — pitch export confirmed.

**QC notes (Cycle 24):**
- Canvas upgraded: 800×800 2×2 → 1200×900 3×2. Expression panels now properly sized for pitch review. Character fills panels at readable scale (presentation failure in v001 corrected per Alex Chen direction).
- 2 new expressions added (Alex Chen direction): STUNNED (electric jolt, full HOT_MAG eyes, ELEC_CYAN brows, open scream mouth, wide electro-scatter confetti) and CALCULATING (calm plotting, ACID_GREEN left eye only, right eye dim, one arm raised planning gesture, sparse confetti, tight mouth). Total 6 expressions.
- MISCHIEVOUS vs TRIUMPHANT: differentiated at silhouette level. MISCHIEVOUS = tilt+20 + diagonal arms (l=-6, r=+14) = scheming lean. TRIUMPHANT = stretch=1.35 + both arms raised (l=-20, r=-22) = victory pose. Different silhouette shapes.
- PANICKED: tilt=-14, squash=0.55, arm_l_dy=18/arm_r_dy=6 (flailing differential), HOT_MAG brows width=3 steep rake. Confetti spread=38px, count=22.
- Turnaround v002: SIDE view shadow contrast fixed — CORRUPT_AMB_SH fill (was UV_PURPLE, nearly invisible against dark canvas). Added Void Black divider lines between lit/shadow facets. BACK view: same fix on base fill. FRONT and 3/4 views unchanged.
- Integration check PASS: VOID_BLACK outline = digital entity standard. Amber/HOT_MAG palette distinct from all protagonists. Diamond body = strong angular contrast to Luma/Cosmo/Miri organic + Byte oval.

---

## Character Design Summary Table

| Character | Expression Sheet | Grid | Count | Turnaround | Color Model | Pitch Status |
|---|---|---|---|---|---|---|
| Luma | v004 | 3×2 | 6 | v001 (4-view) | v001 | PITCH-READY |
| Byte | v004 | 3×3 | 9 | v001 (4-view) | v001 | PITCH-READY |
| Cosmo | v004 | 3×2 | 6 | v002 (4-view) | v001 | PITCH-READY |
| Grandma Miri | v002 | 3×2 | 5 | v001 (4-view) | v001 | PITCH-READY |
| Glitch | v002 | 3×2 | 6 | **v002** (4-view) | v001 | PITCH-READY |

---

## Generator Registry

| Generator | Output | Location |
|---|---|---|
| `LTG_CHAR_luma_expression_sheet.py` | Luma expr sheet v004 | `output/tools/` |
| `LTG_CHAR_byte_expression_sheet.py` | Byte expr sheet v004 | `output/tools/` |
| `LTG_CHAR_cosmo_expression_sheet.py` | Cosmo expr sheet v004 | `output/tools/` |
| `LTG_CHAR_glitch_expression_sheet_v002.py` | Glitch expr sheet v002 (PITCH EXPORT) | `output/tools/` |
| `LTG_CHAR_glitch_expression_sheet_v001.py` | Glitch expr sheet v001 (superseded) | `output/tools/` |
| `LTG_CHAR_glitch_turnaround_v002.py` | Glitch turnaround v002 (PITCH EXPORT — shadow fix) | `output/tools/` |
| `LTG_CHAR_glitch_turnaround_v001.py` | Glitch turnaround v001 (superseded) | `output/tools/` |
| `LTG_CHAR_glitch_color_model_v001.py` | Glitch color model v001 | `output/tools/` |
| `LTG_TOOL_miri_turnaround.py` | Miri turnaround v001 | `output/tools/` |
| `LTG_TOOL_character_lineup.py` | Full cast lineup v004 (5 chars incl. Glitch) | `output/tools/` |

---

## Character Lineup

| Asset | File | Dimensions | Format | Status |
|---|---|---|---|---|
| Full Cast Lineup | `LTG_CHAR_lineup.png` | 1340×498 | RGB PNG | PITCH-READY |

**Cast:** Luma, Byte, Cosmo, Miri, Glitch (all 5 characters at correct relative scale)
**Reference:** 1 head unit = 80px. Luma=280px, Byte=162px (floating), Cosmo=320px, Miri=256px, Glitch=170px (floating).
**Notes:** Glitch added in Cycle 24. Engineering dimension arrow (Byte float gap = 0.25 HU) retained from v003. Height reference lines updated with Glitch scale annotation.

---

## Excluded from Pitch Export

- `LTG_CHAR_luma_expression_sheet_guides.png` — construction guides visible, production reference only
- All `_v001`, `_v002`, `_v003` prior-version sheets — superseded, retained for history
- `LTG_CHAR_glitch_expression_sheet.png` — superseded by v002 (800×800 2×2 — canvas too small, 4 expressions)
- `turnarounds/LTG_CHAR_glitch_turnaround.png` — superseded by v002 (UV_PURPLE shadow invisible against dark canvas)

---

*character_export_manifest.md — Maya Santos, Character Designer*
*Cycle 24 update — 2026-03-29*
*Original Cycle 23 — 2026-03-29*
