**Author:** Maya Santos
**Cycle:** 50
**Date:** 2026-03-30
**Idea:** Extract `tube_polygon()`, `ellipse_points()`, `bezier3()`, `bezier4()` into a shared module (`output/tools/LTG_LIB_organic_primitives.py`) that all character generators import. The C50 construction prototype proved these are the core primitives needed to replace rectangle/ellipse construction. Currently they live inside the prototype tool. If every character generator copies them, we get drift. One shared module means bug fixes propagate everywhere, and new team members (or tools like lineup/turnaround) get organic shapes for free.
**Benefits:** All character designers (Maya, Lee for style frames, Jordan for layout), plus any future tool that draws characters. Eliminates code duplication across 8+ generator scripts. Makes the full-team character rebuild (if approved) faster — port the import, not the functions.
