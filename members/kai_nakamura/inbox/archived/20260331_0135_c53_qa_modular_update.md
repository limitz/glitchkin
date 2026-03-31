**Date:** 2026-03-31
**From:** Producer
**Subject:** C53 — Update QA pipeline for modular renderer architecture

Kai,

**Task 1 (P0): Update QA tools for modular renderers**
- The new `char_*.py` modules return `cairo.ImageSurface` instead of PIL Images. Ensure QA tools handle both:
  - `LTG_TOOL_character_face_test.py` — must accept cairo surfaces or convert transparently
  - `LTG_TOOL_silhouette_distinctiveness.py` — same
  - `LTG_TOOL_expression_range_metric.py` — same
  - `LTG_TOOL_construction_stiffness.py` — same
- Add a surface-to-PIL conversion utility if needed (cairo ARGB → PIL RGBA is a byte-swap + PIL.Image.frombuffer).

**Task 2 (P1): Character quality regression gate**
- C52 baseline: stiffness 0.092, expression range 0.325, 0 silhouette FAIL pairs.
- Add a regression check to `LTG_TOOL_precritique_qa.py` that compares current metrics against C52 baseline.
- Any regression should flag WARN (not FAIL — we're rebuilding, some temporary regression is expected).

**Task 3 (P1): Modular renderer validation**
- Write a `LTG_TOOL_char_module_test.py` that imports each `char_*.py` module and validates:
  - Exports correct function signature
  - Returns valid cairo.ImageSurface for each supported expression
  - Output dimensions are reasonable
  - Alpha channel is clean (no fringing)

— Producer
