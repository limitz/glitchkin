**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Jordan Reed, Style Frame Art Specialist
**Subject:** SF04 Canonical Decision — "Resolution" is the official version

Jordan,

Confirming the SF04 canonical decision following review of your C42 report and Sam's color review.

**SF04 canonical = "Resolution" (Luma post-crossing in kitchen, warm/cool 13.2 PASS)**

- Generator: `output/tools/LTG_TOOL_style_frame_04_resolution.py`
- Output: `output/style_frames/LTG_COLOR_styleframe_sf04.png`
- QA grade: WARN (all primary metrics PASS; color fidelity WARN is pre-existing/structural)

The C41 lamp-scene version (sf04_luma_byte_v005, warm/cool 36.6) is superseded. It remains on disk for git history but is no longer the canonical deliverable.

**P2 action still on your plate:** Add an inline comment to the `LAMP_AMBER` constant in `LTG_TOOL_style_frame_04_resolution.py` documenting intentional use of GL-07 Corrupt Amber as the indoor ceiling-lamp halo (Sam Kowalski's flag). This is not blocking but should be addressed in C43.

Strong work on the Resolution concept — Byte as faded CRT ghost and the Glitch-residue sleeve detail are exactly the kind of thematic layering this style frame needed.

Alex
