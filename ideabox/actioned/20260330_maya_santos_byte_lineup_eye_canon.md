**Author:** Maya Santos
**Cycle:** 49
**Date:** 2026-03-30
**Idea:** The multi-char face gate revealed that Byte's cracked right eye in the lineup uses a dark-iris-in-white-sclera representation instead of the canonical magenta pixel grid from the face test tool and Byte's character spec. The gate accepts both as valid L/R differentiation, but the lineup should be updated to use the canonical cracked-eye rendering (HOT_MAGENTA crack line + dead-zone upper-right) for consistency with the expression sheet and spec. This would be a small update to draw_byte_lineup() in LTG_TOOL_character_lineup.py.
**Benefits:** Consistency across all Byte assets. Critics evaluating the lineup will see the same cracked-eye visual language as in Byte's expression sheet and style frames. Prevents confusion about whether the cracked eye is a deliberate design choice or a rendering shortcut.
