**Author:** Diego Vargas
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** Add panel-type profiles to the visual blank test tool (ECU_SCREEN, MCU_CHARACTER, WIDE_SCENE, INSERT_PROP) that automatically adjust check thresholds based on the panel's camera type. ECU screen panels inherently have low FG/BG delta but high internal contrast; MCU costume panels have low edge density but strong silhouette. A --type flag or auto-detection from the caption bar shot code would eliminate false FAILs and make the tool more actionable across all 25 cold open panels.
**Benefits:** All team members running blank tests get fewer false positives. Lee Tanaka's staging reviews can reference blank test results without caveats. Critics get panels that have been pre-validated against type-appropriate standards.
