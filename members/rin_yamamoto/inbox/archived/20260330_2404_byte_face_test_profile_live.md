**Date:** 2026-03-30
**From:** Kai Nakamura, Technical Art Engineer
**To:** Rin Yamamoto, Compositor / Style Frame Lead
**Subject:** --char byte now live in LTG_TOOL_character_face_test.py

Rin,

Byte character profile is now supported in the face test tool — unblocks face gate for any Byte-facing style frames:

    python3 LTG_TOOL_character_face_test.py --char byte --head-r 23

Gate checks: FG-B01 (eye count), FG-B02 (left normal DEEP_CYAN / right cracked HOT_MAGENTA), FG-B03 (5×5 pixel grid proportions). At head_r=23 (Luma SF02 sprint scale default), the Byte oval is ~26px wide × ~20px tall — adjust --head-r to match your actual Byte body_ry in the generator.

Kai
