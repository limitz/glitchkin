<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Character Export Manifest — "Luma & the Glitchkin"

**Prepared by:** Maya Santos, Character Designer
**Date:** 2026-03-29
**Last Updated:** 2026-03-30 (Cycle 47 — Priya Shah, full reconciliation per Reinhardt critique #6)
**Cycle:** 47
**Status:** Pitch-Ready Export Set

---

## QC Pass Summary (Cycle 23, updated C47)

QC originally performed against `output/production/character_sheet_standards.md` at C23.
All exports checked for: show_guides=False, format (RGB PNG), canvas dimensions,
expression count, grid layout, turnaround completeness, and color model presence.

**C47 update notes:** Miri expression sheet updated to v006 (wooden hairpins, C44). Lineup updated to v010 (two-tier staging, warmth bands, C45). Motion spec sheets added for all 5 characters (Ryo Hasegawa C39-C45). Face gate Byte profile added (Kai Nakamura C45). Luma face curves system active (Kai Nakamura C40-C41). Pipeline resolution now 1280x720 native (C42 onward).

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

**C44 update:** Expression sheet updated to v006. MIRI-A hair accessory changed from chopsticks to dark-stained wooden hairpins (FLAG 05 resolved). Maya Santos executed atomic update across expression sheet + lineup + turnaround + grandma_miri.md. All active Miri PNGs regenerated.

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

| Character | Expression Sheet | Grid | Count | Turnaround | Color Model | Motion Spec | Pitch Status |
|---|---|---|---|---|---|---|---|
| Luma | v004 | 3×2 | 6 | v001 (4-view) | v001 | v001 (Ryo Hasegawa) | PITCH-READY |
| Byte | v004 | 3×3 | 9 | v001 (4-view) | v001 | v003 (COMMITMENT beat, C39) | PITCH-READY |
| Cosmo | v004 | 3×2 | 6 | v002 (4-view) | v001 | v001 (Ryo Hasegawa) | PITCH-READY |
| Grandma Miri | **v006** | 3×2 | 5 | v001 (4-view) | v001 | v001 (Ryo Hasegawa) | PITCH-READY |
| Glitch | v002 | 3×2 | 6 | **v002** (4-view) | v001 | **v001** (C45, 4-panel) | PITCH-READY |

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
| Full Cast Lineup | `LTG_CHAR_character_lineup.png` | 1280×535 | RGB PNG | PITCH-READY |

**Cast:** Luma, Byte, Cosmo, Miri, Glitch (all 5 characters)
**Staging (v008+):** Two-tier ground plane — FG tier (Luma + Byte) at canvas 78%, BG tier (Cosmo + Miri + Glitch) at canvas 70%. FG_SCALE 1.03. Order: Cosmo / Miri / Luma / Byte / Glitch.
**v010 (C45):** Dual-warmth tier depth indicator bands — BG tier 8px cool-slate (#B4C3D2), FG tier 10px warm-amber (#DCC8A0). Annotation bar includes "WARM = FG / COOL = BG" grammar note.
**Notes:** Supersedes flat-baseline lineup (v007 and earlier). Reads as cast dynamics, not character inventory.

---

## Excluded from Pitch Export

- `LTG_CHAR_luma_expression_sheet_guides.png` — construction guides visible, production reference only
- All `_v001`, `_v002`, `_v003` prior-version sheets — superseded, retained for history
- `LTG_CHAR_glitch_expression_sheet.png` — superseded by v002 (800×800 2×2 — canvas too small, 4 expressions)
- `turnarounds/LTG_CHAR_glitch_turnaround.png` — superseded by v002 (UV_PURPLE shadow invisible against dark canvas)

---

## Motion Spec Sheets (Added C47 Update)

All 5 characters now have motion spec sheets (Ryo Hasegawa, C39-C45). These define canonical motion vocabulary: movement beats, timing, and action states per character.

| Character | File | Panels | Key Beats | Cycle |
|---|---|---|---|---|
| Luma | Motion spec sheet | 4 | Movement vocabulary | Ryo Hasegawa |
| Byte | Motion spec sheet v003 | 4 | COMMITMENT beat arc | C39 |
| Cosmo | Motion spec sheet | 4 | Movement vocabulary | Ryo Hasegawa |
| Grandma Miri | Motion spec sheet | 4 | Movement vocabulary | Ryo Hasegawa |
| Glitch | Motion spec sheet v001 | 4 | NEUTRAL HOVER / MISCHIEVOUS APPROACH / COVETOUS LOCK / PANICKED SCATTER | C45 |

**QA:** Motion spec lint (Ryo Hasegawa) PASS for all 5 characters as of C46 (dark-sheet annotation fix applied for Byte + Glitch).

---

## Face Gate System (Added C47 Update)

The face test gate system (`LTG_TOOL_character_face_test.py`) now supports all 4 main characters (luma, cosmo, miri, byte). Byte profile added C45 (Kai Nakamura): 5x5 pixel-grid eye system, left eye DEEP_CYAN normal grid, right eye HOT_MAGENTA crack diagonal + dead-zone upper-right.

Luma face curves system (`luma_face_curves` v1.1.0, Kai Nakamura C41): bezier face system with 9 canonical expressions, `draw_luma_face()` API for generator integration.

---

*character_export_manifest.md — Maya Santos, Character Designer*
*Original Cycle 23 — 2026-03-29*
*Cycle 24 update — 2026-03-29*
*Cycle 47 update — 2026-03-30 — Priya Shah — Full reconciliation: Miri v006 hairpin update, lineup v010 two-tier staging, motion specs (5 chars), face gate Byte profile, face curves system. Per Reinhardt critique #6.*
