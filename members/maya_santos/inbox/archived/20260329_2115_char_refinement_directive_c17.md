**Date:** 2026-03-29 21:15
**From:** Alex Chen, Art Director
**To:** Maya Santos, Character Designer
**Re:** Cycle 17 Character Refinement Assignments

Maya,

I've completed a full review of all main character sheets in response to a producer concern about production refinement. The full directive is at:

`/home/wipkat/team/output/production/char_refinement_directive_c17.md`

Read it in full before starting work. Summary of your assignments this cycle, in priority order:

## Priority 1: Grandma Miri Expression Sheet

This is the most urgent gap. Miri has no expression sheet — only a turnaround and color model. Produce:
- Tool: `LTG_TOOL_miri_expression_sheet_v001.py`
- Output: `LTG_CHAR_miri_expression_sheet_v001.png`
- 6 expressions: NEUTRAL/WARM, KNOWING SMILE, QUIET CONCERN, GENUINE LAUGH, FOCUSED/WORKING, SKEPTICAL/AMUSED
- Full spec in directive Part 4, Assignment 1

Key Miri construction reminders: 3.2 head height, MIRI-A design (bun + chopstick pair + wide cardigan + soldering iron), crow's feet always at 50% line weight, permanent cheek blush #D4956B at 25% opacity, smile lines at 40% weight. All from grandma_miri.md v1.2.

## Priority 2: Line Weight Audit and Fix Pass

Review all four existing expression sheet tools:
- `LTG_TOOL_byte_expression_sheet_v002.py`
- `LTG_TOOL_cosmo_expression_sheet_v001.py`
- `LTG_TOOL_luma_expression_sheet_v002.py` (or v003)
- `LTG_TOOL_luma_act2_standing_pose_v001.py`

Enforce three-tier weight system: silhouette 3px, interior structure 2px, surface detail 1px. This is the root of the producer's "not refined enough" concern. If regeneration is needed, update in place.

## Priority 3: Luma Act 2 Pose Lean Fix

In `LTG_TOOL_luma_act2_standing_pose_v001.py`, increase forward lean from -5° to -8° and propagate through all limb origin points. Regenerate as `LTG_CHAR_luma_act2_standing_pose_v003.png`.

## Submission requirements

For each completed asset, note:
1. Squint test result ("passed — [X] expressions distinct at 10% scale")
2. On-model confirmation ("on-model with [character].md v[X.X]")
3. Line weight confirmation ("three tiers implemented: 3/2/1px")

The locked specs table in Part 5 of the directive is your checklist.

—Alex Chen, Art Director
