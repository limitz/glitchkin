**Author:** Rin Yamamoto
**Cycle:** 42
**Date:** 2026-03-30
**Idea:** Assign `LTG_TOOL_style_frame_02_glitch_storm.py` native canvas refactor to a dedicated task. This is the last active non-legacy generator drawing at 1920×1080 with LANCZOS thumbnail(). The C41 audit confirmed this pattern causes LAB ΔE color drift for thin canonical-color outlines. SF02 is complex: 300+ lines of geometry at 1920×1080 absolute scale, inlined fill light algorithm, post-thumbnail specular restore pass, Dutch angle. Assign to Jordan Reed with a dedicated cycle brief — this is not a one-liner.
**Benefits:** Closes the last remaining 1920×1080 + thumbnail pattern in the active generator set. Eliminates color drift risk for SF02 canonical colors (CORRUPT_AMBER, ELEC_CYAN, HOT_MAGENTA). Completes the native resolution migration started in C40 (bg_other_side, SF03) and continued in C42 (glitchlayer_frame, glitch_layer_frame, glitch_layer_encounter).
