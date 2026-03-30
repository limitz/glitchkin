**Author:** Diego Vargas
**Cycle:** 49
**Date:** 2026-03-30
**Idea:** Add a secondary C4 (Character Presence) method to the visual blank test that uses color-cluster detection instead of edge density. The current edge-density metric penalizes panels with smooth cel-shaded character fills (P13, P17, P20 all FAIL despite having clear character silhouettes). A hue-cluster method would detect distinct color regions in character zones and pass panels where characters are present but drawn with flat fills and minimal internal edge detail.
**Benefits:** Would eliminate 3-5 false FAILs in the current cold open panel set, particularly for TWO_SHOT and quiet-beat panels. Benefits all team members who use the blank test for pre-delivery QA.
