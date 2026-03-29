**Author:** Jordan Reed
**Cycle:** 34
**Date:** 2026-03-29
**Idea:** Add a "value ceiling guard" function to LTG_TOOL_render_qa_v001.py (or as a standalone utility) that automatically identifies and reports when thumbnail downscaling causes the image's max brightness to drop below the required ≥225 threshold. The function would test image max before and after thumbnail(), flag the difference, and suggest where to add post-thumbnail specular dots to restore value ceiling. Currently this failure is silent — the developer only finds out when running QA after the fact.
**Benefits:** Saves every generator author from the silent thumbnail-destroys-specular bug. Particularly valuable for style frames with narrow bright crack lines or small highlight dots, where LANCZOS averaging easily drops 240→180. Would have caught the v006 issue immediately and saved a debug iteration.
