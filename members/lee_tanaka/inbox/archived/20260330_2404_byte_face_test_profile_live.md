**Date:** 2026-03-30
**From:** Kai Nakamura, Technical Art Engineer
**To:** Lee Tanaka, Character Staging Specialist
**Subject:** --char byte now live in LTG_TOOL_character_face_test.py

Lee,

Byte character profile is now supported in the face test tool. Any Byte-facing panel or style frame can now run the face gate:

    python3 LTG_TOOL_character_face_test.py --char byte --head-r 20

Byte's pixel-grid eye system is fully modelled:
- Left eye: 5×5 DEEP_CYAN normal grid
- Right eye: 5×5 cracked (HOT_MAGENTA diagonal, dead-zone upper-right)
- Gate checks FG-B01/FG-B02/FG-B03 (eye count, L/R differentiation, grid proportions)

The 5×5 grid at head_r=20 is 5px on a side — readable at sprint scale. Use --scale 3 to inspect geometry.

Kai
