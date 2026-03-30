**Author:** Morgan Walsh
**Cycle:** 50
**Date:** 2026-03-30
**Idea:** Add 3 new character-focused sections to precritique_qa: Section 15 (Face Quality Gate using face_test + face_landmark_detector), Section 16 (Silhouette Distinctiveness using Kai's new tool), and Section 17 (Thumbnail Readability using the new LTG_TOOL_thumbnail_readability). This would raise character-specific checks from 30% to ~43% of the pipeline, directly addressing the audit finding that we have been measuring backgrounds 2x more than characters.
**Benefits:** The whole team benefits — generators get actionable character feedback before critic cycles instead of discovering face/readability issues from critics. Critics can focus on subjective appeal instead of catching basic structural problems.
