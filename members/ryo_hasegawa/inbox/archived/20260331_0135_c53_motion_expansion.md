**Date:** 2026-03-31
**From:** Producer
**Subject:** C53 — Expand motion sheets using modular renderers

Ryo,

**Task (P1): Cosmo motion sheet**
- Cosmo has no motion/action poses yet beyond `LTG_TOOL_cosmo_motion.py` (which may be old PIL).
- Once Sam's `char_cosmo.py` canonical renderer is available (or use existing cosmo expression code), build a gesture-first Cosmo motion sheet.
- Follow same approach as your C52 Luma motion rebuild: 4 panels, gesture-first construction, lint 6/6 PASS target.
- Key Cosmo motion: tech-focused gestures (typing, pointing at screen, adjusting glasses), angular body language per Lee's spec.

**Task (P2): Byte motion sheet update**
- If time permits, update `LTG_TOOL_byte_motion.py` to import from `char_byte.py` once Rin delivers it.
- Byte motion = digital glitching, floating, size-shift, pixel scatter.

Run `LTG_TOOL_motion_spec_lint.py` on all outputs.

— Producer
