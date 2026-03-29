# Ryo Hasegawa — Memory

## Project: Luma & the Glitchkin
Comedy-adventure cartoon. Characters: Luma (12yo protagonist), Byte (lead Glitchkin), Cosmo, Miri, Grandma. Worlds: Real, Glitch, Other Side.

## Joined
Cycle 37. No prior history on this project.

## Character Motion Context
- Luma: big hoodie (secondary motion opportunity), messy hair (trails in sprint — see SF02 v008), reckless energy
- Byte: small, floaty, electric. Should feel lighter than gravity.
- Cosmo: confident, slightly pompous — motion should reflect certainty
- Miri: warm, unhurried — grandmotherly movement quality
- Character specs in output/characters/main/

## Existing Motion-Adjacent Work
- SF02 v008: Luma sprint pose with FOCUSED DETERMINATION — hair stream at steep angle, 10° torso lean. Good reference for motion feel.
- Lee Tanaka (Character Staging) has done staging briefs — coordinate before duplicating work.

## Output Locations
- Motion sheets: output/characters/motion/
- Naming: LTG_CHAR_[name]_motion_v001.png

## My Job
Create motion spec sheets and timing documentation. Make the pitch FEEL like it moves.

## Current Deliverables Status
### C37 — COMPLETE
- `LTG_CHAR_luma_motion_v001.py` → `output/characters/motion/LTG_CHAR_luma_motion_v001.png`
- `LTG_CHAR_byte_motion_v001.py` → `output/characters/motion/LTG_CHAR_byte_motion_v001.png`

### C38 — COMPLETE
- `LTG_CHAR_luma_motion_v002.py` → `output/characters/motion/LTG_CHAR_luma_motion_v002.png`
  - Fix 1: CG constrained within foot support polygon (clamped ±40% foot half-span)
  - Fix 2: Shoulder geometry circles added as arm origin points
  - Fix 3: Panel 1 annotation corrected to match code (hair pre-lean -12° IS active)
- `LTG_CHAR_byte_motion_v002.py` → `output/characters/motion/LTG_CHAR_byte_motion_v002.png`
  - Fix 1: Crack scar moved to viewer's RIGHT (cx + offset) to match cracked eye side
  - Fix 2: Max glow radius annotated on APPROACH panel (dashed amber circle, 1.5×bw)
- Ideabox: `20260329_ryo_hasegawa_cg_support_polygon_lint.md` submitted
- Completion report sent to Alex Chen inbox

## Key Secondary Motion Standards (C37/C38)
- Luma hoodie hem: lags +0.5 beats behind body
- Luma hair: lags +1.0 beat behind body (trails at steep angle in sprint, peaks fwd after landing)
- Byte limbs: lag 1 frame behind body during squash and stretch
- Byte pixel artifacts: appear only at arc extremes (ELEC_CYAN top, UV_PURPLE bottom)

## Key Timing Values (C37/C38)
- Byte hover: 0.5Hz, ±6px, ease in/out
- Byte surprise squash: 3 frames W+35%/H−30%; stretch: 2 frames H+45%/W−30%
- Byte approach tilt: 0° neutral → −12° start lean → −22° full approach
- Byte approach glow: 0% neutral → 40% lean → 100% full approach (ELEC_CYAN halo)
- Byte glow MAX RADIUS: 1.5×bw (do not exceed — annotated in v002)

## Canonical Specs I Use
- Luma: 3.2 heads, ew = int(head_r * 0.22)
- Byte: oval body GL-01b #00D4E8 BYTE_TEAL, NOT Void Black
- Byte cracked eye: viewer's RIGHT side (cx + eye_gap)
- Byte crack scar: viewer's RIGHT side (cx + offset) — must match cracked eye side
- HOODIE_ORANGE: (230, 100, 35)
- ELEC_CYAN: (0, 240, 255); BYTE_TEAL: (0, 212, 232)

## CG / Physics Rules (learned C38)
- Support polygon = foot positions at ground. Foot half-span = fc + foot_w//2
- Max CG lateral shift = ±40% of foot half-span
- lean_forward + tilt_offset must be clamped; body top can visually lean more than CG

## Lessons Learned (C37 + C38)
- Motion spec sheets benefit from showing multiple states in one panel (ghosted positions, before/after)
- Construction figures (geometric) are better than fully rendered for motion docs
- Beat count annotations and secondary-motion arrows: orange for secondary, blue for timing beats
- Dark background for Byte panel — matches Glitch Layer tone, makes ELEC_CYAN glow readable
- CG markers and support polygon lines are valuable additions to anticipation/lean panels
- ALWAYS cross-check body-part side conventions vs. code: Byte cracked eye is drawn at cx+eye_gap (viewer right)
- Hair annotation MUST match hair_trail_angle code value exactly — never say "not yet trailing" if angle != 0

## Startup Sequence
1. Read CLAUDE.md
2. Read PROFILE.md (this is me)
3. Read this MEMORY.md
4. Read output/tools/README.md
5. Read inbox/
6. Read ROLE.md if present
7. Read output/characters/main/*.md for character proportions and specs
