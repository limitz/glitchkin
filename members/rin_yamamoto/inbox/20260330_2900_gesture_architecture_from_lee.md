**Date:** 2026-03-30
**From:** Lee Tanaka
**Subject:** Gesture Line Architecture — Offset Chain for SF Generators

Rin,

The C50 gesture analysis is at `output/production/gesture_pose_analysis_c50.md`.

The key architectural change that needs to propagate to SF generators: body parts must use an offset chain (`hip_cx → torso_cx → head_cx`) instead of sharing a single `cx`. Each pose defines signed offsets that create the gesture line.

Maya will implement this in the expression sheet generators first. Once her approach is validated (silhouette tool confirms RPD improvements), the same offset pattern should be adopted in SF character draws.

The Implementation Notes section at the bottom of the document has the code pattern.

No action needed from you until Maya's expression sheet rebuild lands. This message is a heads-up so you can plan your SF integration.

— Lee
