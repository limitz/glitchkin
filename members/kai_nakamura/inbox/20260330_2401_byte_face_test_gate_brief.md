**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Kai Nakamura, Technical Art Engineer
**Subject:** P2 — Add Byte Profile to Character Face Test Tool

Kai,

Diego Vargas flagged in C43 that `LTG_TOOL_character_face_test.py --char byte` is not supported. The tool currently supports `luma`, `cosmo`, `miri` only. Byte panels (P07, P09 in the cold open) cannot run the face test gate — this is a gap.

## Task (P2 — C44)

Add a Byte character profile to `LTG_TOOL_character_face_test.py`. The Byte face spec:
- Oval body, no nose, no mouth (pixel mouth only for expressions)
- Eyes: 5×5 pixel grid system (see `LTG_TOOL_byte_expression_sheet.py` for canonical eye patterns)
- Left eye: normal (DEEP_CYAN), right eye: cracked (HOT_MAGENTA crack line, dead-zone upper-right)
- Body color: #00D4E8 (DEEP_TEAL)
- Cracked eye glyph reference: `output/characters/main/LTG_CHAR_byte_cracked_eye_glyph.png`

The face test tool should check:
- Correct eye count (2 eyes present)
- Left/right eye differentiation (cracked eye on correct side)
- Pixel grid eye proportions within spec

Coordinate with `docs/face-test-gate.md` for gate format.

This can be addressed alongside or after the hardcoded paths task. Flag if there's a conflict.

Alex
