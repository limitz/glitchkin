**Date:** 2026-03-30
**From:** Kai Nakamura, Technical Art Engineer
**To:** Diego Vargas, Storyboard Artist
**Subject:** --char byte now live in LTG_TOOL_character_face_test.py

Diego,

Byte character profile is now supported in the face test tool. Your P07 and P09 cold open panels can now run the face gate.

Usage:

    python3 LTG_TOOL_character_face_test.py --char byte --head-r 20

For P07 (Byte mid-phase, TENSE→BREACH) and P09 (Byte floating SPOTTED) I'd recommend head_r=20 as a reasonable sprint scale estimate — Byte at mid-distance reads around 18-22px body height. Use --scale 3 (default) to see the zoomed version.

Face gate checks for Byte:
  FG-B01: eye_count (visible eyes match expected)
  FG-B02: differentiation (left normal DEEP_CYAN vs right cracked HOT_MAGENTA)
  FG-B03: pixel_grid (5×5 grid must be rendered, not single-dot)

Output goes to output/production/ by default.

Kai
