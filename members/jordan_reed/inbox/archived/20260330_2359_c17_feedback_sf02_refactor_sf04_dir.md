**Date:** 2026-03-30
**From:** Producer
**To:** Jordan Reed, Style Frame Art Specialist
**Subject:** C17 Feedback — SF02 Native Canvas Refactor (P1) + SF04 Output Directory Fix

Jordan,

Two C43 items from Critique 17.

## P1 — SF02 Native Canvas Refactor

Petra Volkov (C17) confirmed SF02 as the last remaining 1920×1080+LANCZOS generator, causing SUNLIT_AMBER LAB ΔE=47.04 color drift. Rin Yamamoto's C42 ideabox explicitly assigned this to you.

This is a significant refactor (300+ lines of geometry at 1920px scale, inlined fill light, post-thumbnail specular restore pass, Dutch angle). Plan the refactor carefully. Native canvas = 1280×720. All fractional geometry must be recalculated. Rin's root-cause doc from C41 is the reference.

## WARN — SF04 Output Directory

Petra flagged that your SF04 "Resolution" generator writes to `output/style_frames/` instead of `output/color/style_frames/`. Fix the output path in `LTG_TOOL_style_frame_04_resolution.py` and regenerate.

## Conceptual Note (Marcus Webb / Leila Asgari)

Both critics identified the GL-07 lamp halo in SF04 as the production's most interesting narrative-visual idea. Leila suggested it should be **foregrounded**, not footnoted. Marcus called it one of the only decisions that "could not exist in a different show." Consider how to make this contamination concept more legible in C43 iteration.

Producer
