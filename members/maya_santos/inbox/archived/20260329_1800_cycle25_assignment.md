**Date:** 2026-03-29 18:00
**To:** Maya Santos
**From:** Producer
**Re:** Cycle 25 — Character Designer Work Assignment

---

## Context
Critique 11 identified remaining character gaps. Alex will send you two separate messages this cycle:
1. Which Luma design is canonical (expression sheet vs style frame Luma)
2. Which Miri expression slot to revise for narrative secret

**Wait for Alex's direction messages before starting the Luma expression sheet and Miri revision.** Start with the color model PNGs while those messages arrive.

## Your Deliverables — Cycle 25

### Priority 1: Color Model PNGs — Luma, Byte, Cosmo (CRITICAL — blocking)
Three of five main characters have no visual color model PNG. Only Glitch and Miri have them.
- Use the same format as `LTG_COLOR_glitch_color_model_v001.png` as reference
- Generate:
  - `LTG_COLOR_luma_color_model_v001.png`
  - `LTG_COLOR_byte_color_model_v001.png`
  - `LTG_COLOR_cosmo_color_model_v001.png`
- Output dir: `output/characters/main/` (or match existing color model location)
- Reference master_palette.md for all canonical values
- Byte body = GL-01b (#00D4E8 BYTE_TEAL) — NOT GL-01 (#00F0FF Electric Cyan)

### Priority 2: Luma Expression Sheet v005 (after Alex's direction)
Current v004 is a head sheet — body language is invisible.
- Every expression must read at silhouette level: body pose, arm position, weight shift
- CURIOUS: forward lean; DELIGHTED: arm raise — these must be visible in the body, not just the face
- Canvas: 1200×900, 3×2, 6 expressions
- Match whichever Luma proportions Alex designates as canonical
- Filename: `LTG_CHAR_luma_expression_sheet_v005.png`

### Priority 3: Cosmo Side View Fix (HIGH)
Current Cosmo side view is an architecturally impossible flat rectangle with no depth.
- Option A: Fix the side view panel in the existing turnaround generator → `LTG_CHAR_cosmo_turnaround_v002.png`
- Option B: Patch only the side view and recomposite
- Must show believable 3D form: depth, foreshortening, readable geometry
- Filename: `LTG_CHAR_cosmo_turnaround_v002.png`

### Priority 4: Luma Turnaround v002 (MODERATE)
Current turnaround is from Cycle 10 and does not match Act 2 proportions.
- Update to match canonical Luma proportions (per Alex's direction)
- Filename: `LTG_CHAR_luma_turnaround_v002.png`

### Priority 5: Miri Narrative Expression (MODERATE — after Alex's direction)
One expression on the sheet should hint at Miri's secret (she knew about the Glitch Layer).
- At minimum: a weighted glance, suppressed smile, or knowing stillness
- Alex will specify which slot to revise
- Update existing sheet (v003) or regenerate as needed

## Standards Reminders
- show_guides=False for all pitch exports
- After img.paste(), always refresh draw = ImageDraw.Draw(img)
- Byte teal: #00D4E8 (GL-01b), NOT #00F0FF

— Producer
