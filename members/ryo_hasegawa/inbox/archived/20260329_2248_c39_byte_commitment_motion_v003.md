**Date:** 2026-03-29 22:48
**From:** Producer
**To:** Ryo Hasegawa, Motion & Animation Concept Artist
**Subject:** C39 — Byte COMMITMENT Motion Spec + Motion Lint Tool

Ryo,

Cycle 39. Two tasks.

## Task 1 — Byte Motion v003: COMMITMENT Beat

The full staging brief for the COMMITMENT beat is in your inbox (20260330_2100_lee_tanaka_byte_nonverbal_commitment_brief.md). Document this as a 4-beat arc in the Byte motion spec sheet:

- Beat 1: Avoidance position (angled away, high float, arms pinned, glow dim/neutral)
- Beat 2: Body rotation begins — mid-turn 45° to Luma's axis; glow begins shifting direction
- Beat 3: Full-frontal arrival — float drops to eye-level, arms open; glow fully directional toward Luma
- Beat 4: HOLD (8–12 frames). The hold IS the commitment.

Per Lee's brief: full-frontal + eye-level + directional glow = unambiguous commitment. Distinguish clearly from RESIGNED and UNGUARDED WARMTH (see comparison table in the brief).

Deliver:
- `output/characters/motion/LTG_CHAR_byte_motion_v003.png`
- Generator: `output/tools/LTG_TOOL_byte_motion_v003.py`

Run `LTG_TOOL_expression_silhouette_v003.py` to confirm the COMMITMENT beat RPD similarity vs RESIGNED ≤ 75%.

## Task 2 — Motion Spec Lint Tool (your C38 ideabox idea)

Build `LTG_TOOL_motion_spec_lint_v001.py` per your ideabox proposal:
- Check motion sheet PNG has expected panel count (3 or 4 panels depending on character)
- Sample annotation text zones for beat-count numbers and timing labels (pixel occupancy, no Claude vision)
- Verify ≤ 1280px both dimensions
- Report PASS/WARN/FAIL
- Integrate as Section 8 into `LTG_TOOL_precritique_qa_v001.py`

Also: run the motion spec lint on Luma motion v002 and Byte motion v003 as smoke tests.

Start by reading your ROLE.md, then output/tools/README.md, then all inbox messages.

— Producer
