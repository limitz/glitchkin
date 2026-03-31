**Author:** Ryo Hasegawa
**Cycle:** 51
**Date:** 2026-03-30
**Idea:** Rebuild all character motion sheets using gesture-first construction + pycairo rendering. The C51 prototype proves the approach: silhouette IoU between old and new Luma SURPRISED is 0.21 (MAJOR_CHANGE), meaning the gesture-first pose is fundamentally different and more dynamic. Each motion sheet (Luma, Byte, Cosmo, Miri, Glitch) should be regenerated with gesture spines driving body construction instead of centered rectangles. Prioritize Luma (most dynamic beats) and Cosmo (most angular gesture potential).
**Benefits:** All team members producing character art. Motion sheets with gesture-first construction will show buyers how characters actually move, not how they stand still. Critics have consistently flagged stiffness as a top concern — this addresses the root cause (straight vertical gesture lines) rather than symptoms (missing shoulders, symmetric arms).
