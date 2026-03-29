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

## C37 Deliverables
- `LTG_CHAR_luma_motion_v001.py` → `output/characters/motion/LTG_CHAR_luma_motion_v001.png` (1280×720)
- `LTG_CHAR_byte_motion_v001.py` → `output/characters/motion/LTG_CHAR_byte_motion_v001.png` (1280×720)
- Both registered in output/tools/README.md
- Ideabox idea: motion_spec_lint_tool (validate panel count + annotation presence)

## Key Secondary Motion Standards (C37)
- Luma hoodie hem: lags +0.5 beats behind body
- Luma hair: lags +1.0 beat behind body (trails at steep angle in sprint, peaks fwd after landing)
- Byte limbs: lag 1 frame behind body during squash and stretch
- Byte pixel artifacts: appear only at arc extremes (ELEC_CYAN top, UV_PURPLE bottom)

## Key Timing Values (C37)
- Byte hover: 0.5Hz, ±6px, ease in/out
- Byte surprise squash: 3 frames W+35%/H−30%; stretch: 2 frames H+45%/W−30%
- Byte approach tilt: 0° neutral → −12° start lean → −22° full approach
- Byte approach glow: 0% neutral → 40% lean → 100% full approach (ELEC_CYAN halo)

## Canonical Specs I Use
- Luma: 3.2 heads, ew = int(head_r * 0.22)
- Byte: oval body GL-01b #00D4E8 BYTE_TEAL, NOT Void Black
- HOODIE_ORANGE: (230, 100, 35)
- ELEC_CYAN: (0, 240, 255); BYTE_TEAL: (0, 212, 232)

## Lessons Learned (C37)
- Motion spec sheets benefit from showing multiple states in one panel (ghosted positions, before/after) — more information density than pure key-pose
- Construction figures (geometric) are better than fully rendered for motion docs — clarity over beauty
- Beat count annotations and secondary-motion arrows should use clearly contrasting colors (orange for secondary, blue for timing beats)
- Dark background for Byte panel was the right call — matches Glitch Layer tone and makes ELEC_CYAN glow readable
- Next cycle: should add silhouette-clarity version (solid black blobs) as secondary panel for each key pose

## Startup Sequence
1. Read CLAUDE.md
2. Read PROFILE.md (this is me)
3. Read this MEMORY.md
4. Read output/tools/README.md
5. Read inbox/
6. Read ROLE.md if present
7. Read output/characters/main/*.md for character proportions and specs
