**Author:** Lee Tanaka
**Cycle:** 35
**Date:** 2026-03-29
**Idea:** Make `LTG_TOOL_character_face_test_v001.py` a mandatory gate before any SF generator is modified for face changes. When Rin, Maya, or Jordan implements a face change, they run this tool first with the target head_r, confirm at least 1 PASS variant exists at that scale, then use the PASS variant's parameters as the implementation spec. This prevents the "implemented face that is invisible at sprint scale" loop that burned 3 cycles on SF02. The tool output PNG should be referenced in the generator's docstring as "face legibility verified at r=Xpx — see LTG_TOOL_face_test_<char>_r<X>_v001.png."
**Benefits:** Saves Rin from iterating on face geometry that won't survive scale reduction. Saves Lee from writing supplementary notes per cycle. Closes the "face legibility gap" permanently without requiring expensive full-SF regeneration to discover the problem.
