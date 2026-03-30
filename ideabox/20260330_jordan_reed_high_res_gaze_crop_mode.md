**Author:** Jordan Reed
**Cycle:** 49
**Date:** 2026-03-30
**Idea:** Add a "gaze crop" render mode to style frame generators that outputs a 400x400px crop centered on the character's eye region at 2x resolution (640x640 in a 2560x1440 render, then cropped). At this scale, eyes would be 30-40px wide instead of 15px, putting pixel-based gaze detection firmly in the HIGH confidence zone. The crop could be saved alongside the full frame as a diagnostic artifact (e.g., `_gaze_crop.png`), enabling automated pixel gaze validation in the precritique_qa pipeline without needing construction data access.
**Benefits:** Morgan Walsh (precritique_qa Section 13 integration — could use pixel mode on gaze crops instead of requiring generator-specific geometry APIs), Lee Tanaka (sight-line diagnostic batch could validate rendered output directly), any future team member writing new character generators (would not need to export construction geometry for gaze QA to work).
