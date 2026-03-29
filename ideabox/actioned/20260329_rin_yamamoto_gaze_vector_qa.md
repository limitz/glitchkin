**Author:** Rin Yamamoto
**Cycle:** 38
**Date:** 2026-03-29
**Idea:** Build a gaze-vector QA tool that, given a character's eye center coordinates and pupil offset, computes the direction of gaze as a 2D vector and checks whether that vector intersects a named target region (e.g. "Byte position", "CRT screen", "other character"). The tool would output a visual annotation showing the gaze line projected from both eyes to the scene, making sight-line errors (Ingrid critique C15: "Luma is pointing not seeing") detectable before iteration review.
**Benefits:** Prevents sight-line failures from slipping through review. Rin currently has to reason about pupil offset direction by hand — a tool that computes and draws the gaze ray from eye center + pupil offset + head turn offset would make gaze verification automatic and repeatable. Jordan and Maya would also benefit for any full-scale style frame with two or more characters who need to share visual attention.
