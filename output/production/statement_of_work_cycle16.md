# Statement of Work — Cycle 16
**Project:** Luma & the Glitchkin
**Date:** 2026-03-29
**Cycle:** 16 of ongoing

---

## Work Completed This Cycle

### Sam Kowalski — Color & Style Artist

**Byte Expression Sheet v002 — 3 Critical Color Fixes**
- Shadow corrected: `BYTE_SH` → GL-01a Deep Cyan `#00A8C0` (was grey-shifted)
- ALARMED background corrected: warm cocoa → cold danger blue `(18,28,44)`
- Pixel faceplate proportionalized: `eye_size` now derived from `body_ry` — consistent across all expressions
- Output: `LTG_CHAR_byte_expression_sheet_v002.png` (regenerated)

**SF02 Glitch Storm Generator — Color Fix**
- DRW-07 corrected: `#C07A70` → `#C8695A` (storm hoodie correct saturation)
- ENV-06 verified: G=172>R=150 AND B=162>R=150 — both rules satisfied
- Output: `LTG_COLOR_styleframe_glitch_storm_v002.png` (regenerated with color fix)

**SF03 "Other Side" Color Review — Delivered to Alex Chen**
- 6-point color audit: UV ambient, atmospheric perspective, Byte dual-eye legibility, confetti density, abyss value, DRW-18 hair rim
- All pass; minor flags: upper-right depth tier collapse + mid-air confetti physics for v002

---

### Maya Santos — Character Designer

**Byte RESIGNED Expression — Right Eye Geometry Fix**
- `droopy_resigned` style reworked: aperture 45% (vs NEUTRAL 60%), pupil +10px downcast, parabolic drooping lower lid (7px center sag), dim highlight, no smile crinkle
- Body tilt amplified: +8° → +14° for silhouette differentiation
- Output: `LTG_CHAR_byte_expression_sheet_v002.png` (geometry fix applied over Sam's color fix)

**Cosmo Expression Sheet — SKEPTICAL Fix + 2 New Expressions**
- SKEPTICAL backward lean: -3° → +6° (body-language anchor per Dmitri's direction)
- New expression: WORRIED (A2-02 beat) — corrugator kink, arms in, compressed mouth
- New expression: SURPRISED (A2-04c beat) — bilateral brow raise, arms up, open oval mouth
- Sheet now fully populated: 6/6 expressions
- Output: `LTG_CHAR_cosmo_expression_sheet_v002.png`

**Luma Act 2 Standing Pose — Mitten Hand Fix**
- Raised right arm hand: removed finger differentiation, replaced with clean rounded oval
- Output: `LTG_CHAR_luma_act2_standing_pose_v002.png`

---

### Jordan Reed — Background & Environment Artist

**SF02 Glitch Storm v003 — Full Fix Pass**
- Dominant cold confetti: DATA_BLUE 70% dominant — no warm colors, no rainbow spread
- Dutch angle: 4.0° — visibly perceptible
- Byte CORRUPT_AMBER outline: 3px solid `#C87A20` — visible in storm sky
- Storm rim lighting: ELEC_CYAN right/top + UV_PURPLE base bounce on buildings
- DRW-07 corrected value `(200,105,90)` applied
- Tool: `LTG_TOOL_style_frame_02_glitch_storm_v003.py`
- Output: `LTG_COLOR_styleframe_glitch_storm_v003.png` (241 KB)

**SF03 Other Side v002 — Fix Pass**
- Waterfall luminance: alpha max 110 (was 255) — reads as ambient data flow, not wall
- Mid-distance floating arch bridge added at 40–65% x / 49–60% y with hanging pillars
- Right-side void: 7 slabs with seeded scale variation + polygon skew — irregular depth
- DRW-18 UV Purple hair rim `#7B2FBE` applied to Luma's hair crown
- Tool: `LTG_TOOL_style_frame_03_other_side_v002.py`
- Output: `LTG_COLOR_styleframe_otherside_v002.png` (35 KB)

**Classroom Background v002 — Fix Pass**
- Unified dual-source lighting: warm LEFT + cool RIGHT, clean crossover, no muddy overlap
- Inhabitant evidence: wear marks, worksheets, backpack, chalk dust, water bottle
- Tool: `LTG_TOOL_bg_classroom_v002.py`
- Output: `LTG_ENV_classroom_bg_v002.png` (91 KB)

**Grandma Miri's Kitchen — New Background**
- Warm morning daylight, pre-digital appliances, CRT TV through doorway (story element)
- Lived-in: crossword, tea mug, toast, dish rack, plant, fridge magnets, worn linoleum
- Zero Glitch palette — all Real World colors
- Tool: `LTG_TOOL_bg_grandma_kitchen_v001.py`
- Output: `LTG_ENV_grandma_kitchen_v001.png` (39 KB)

---

### Lee Tanaka — Storyboard Artist

**A2-07 — RESIGNED ECU (drew for real, placeholder retired)**
- ECU on Byte's cracked eye, 7×7 dead-pixel glyph at ~30% frame width
- RESIGNED expression: droopy lid, ↓ pixel glyph, arms drawn in, flat short mouth
- Deep void background with circuit traces
- Tool: `LTG_TOOL_sb_panel_a207_v001.py`
- Output: `LTG_SB_act2_panel_a207_v002.png`

**A2-03 — Full Restage (Cosmo SKEPTICAL)**
- Camera fully spec'd: cowboy shot / eye-level / neutral observer / labeled in-panel
- 2-point perspective room with eyeline guide
- Whiteboard as third character: 5-step color-coded Doomed Plan with circling arrows, crossed-out success, ???
- Cosmo FG-left / Luma BG-right / Whiteboard center-right
- Tool: `LTG_TOOL_sb_panel_a203_v002.py`
- Output: `LTG_SB_act2_panel_a203_v002.png`

**A2-06 MED — New Establishing Shot**
- Cosmo + Luma two-shot, exterior night, both expectant/hopeful
- Phone showing active GLITCH FREQ app — makes INSERT's failure emotionally meaningful
- Tool: `LTG_TOOL_sb_panel_a206_insert_v001.py`
- Output: `LTG_SB_act2_panel_a206_med_v001.png`

**A2-04 v002 — Byte as Non-Participant**
- TR quadrant: Byte back fully turned, floating in corner, arms folded, "nope"
- Three-way contrast: Luma trying / Cosmo helping / Byte refusing
- Tool: `LTG_TOOL_sb_panel_a204_v002.py`
- Output: `LTG_SB_act2_panel_a204_v002.png`

**Act 2 Contact Sheet v003**
- 8 panels, 4×2 layout, full arc with arc-label colors coded per emotional temperature
- Arc: NEAR-MISS → VULNERABLE → SKEPTICAL → INVESTIGATING → DETERMINED → HOPEFUL → FAILURE → RESIGNED
- Tool: `LTG_TOOL_sb_act2_contact_sheet_v003.py`
- Output: `LTG_SB_act2_contact_sheet_v003.png`

---

### Alex Chen — Art Director

**Work Coordination:** Assigned and tracked all Cycle 16 tasks. Relayed Sam's SF03 color notes to Jordan Reed.

**README.md Update:** Full rewrite with ASCII logo art, color language swatches, character portraits, style frame status grid, storyboard progress bars, environment inventory, pipeline table, and cycle history timeline.

---

## Style Frame Status After Cycle 16

| Frame | File | Status |
|-------|------|--------|
| SF01 Discovery | `LTG_COLOR_styleframe_discovery_v003.png` | **A+ LOCKED** |
| SF02 Glitch Storm | `LTG_COLOR_styleframe_glitch_storm_v003.png` | **Fixes applied — pending review** |
| SF03 Other Side | `LTG_COLOR_styleframe_otherside_v002.png` | **Fixes applied — pending review** |

## Storyboard Status After Cycle 16

| Panel | File | Status |
|-------|------|--------|
| A1-04 | `LTG_SB_act2_panel_a104_v001.png` | Done |
| A2-02 | `LTG_SB_act2_panel_a202_v001.png` | Done |
| A2-03 | `LTG_SB_act2_panel_a203_v002.png` | **Restaged this cycle** |
| A2-04 | `LTG_SB_act2_panel_a204_v002.png` | **Byte added this cycle** |
| A2-05b | `LTG_SB_act2_panel_a205b_v001.png` | Done |
| A2-06 INSERT | `LTG_SB_act2_panel_a206_v001.png` | Done |
| A2-06 MED | `LTG_SB_act2_panel_a206_med_v001.png` | **New this cycle** |
| A2-07 | `LTG_SB_act2_panel_a207_v002.png` | **Drew for real this cycle** |
| Contact Sheet | `LTG_SB_act2_contact_sheet_v003.png` | **Updated this cycle** |

## Remaining Act 2 Panels (not started)
- A2-01: Wide establishing — tech den after school
- A2-05: Exterior wide — Millbrook street streetlight
- A2-08: Grandma Miri returns — front door/hallway

---

*Next critique: after Cycle 18 (Critique Cycle 9)*
