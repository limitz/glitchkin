**Date:** 2026-03-29 19:00
**To:** Kai Nakamura
**From:** Producer (via Alex Chen)
**Re:** Cycle 26 — Rendering QA Pipeline + Procedural Generation Collaboration

---

## Context
Producer directive: focus on aesthetics and rendering quality for the next 3 cycles. Your job this cycle is to build the quality assessment infrastructure.

---

## Deliverable 1: LTG_TOOL_render_qa_v001.py (PRIMARY)

Build a quality assessment tool that can evaluate any rendered PNG against LTG rendering standards.

Required checks:

**A. Silhouette Readability**
- Accept a character PNG (with transparent or dark background)
- Generate a B&W silhouette (threshold at 128 on alpha or darkness)
- Check: is the silhouette readable at 100×100px? (i.e., does it have distinct shape?)
- Score: distinct/ambiguous/blob

**B. Value Range Check**
- Convert to grayscale
- Check that the image uses full value range (darkest pixel ≤ 30, brightest ≥ 225)
- Flag "value compression" if range is < 150 (e.g., 80–200 = compressed, weak)

**C. Color Fidelity Check**
- Wrap `verify_canonical_colors()` from `LTG_TOOL_color_verify_v001.py`
- Report per-color drift

**D. Warm/Cool Separation Check**
- For style frames: check that warm and cool zones are distinct
- Sample pixels in the upper half vs lower half (or left vs right) and check if average hue differs by at least 20°
- Flag "flat palette" if no warm/cool separation exists

**E. Line Weight Consistency**
- Detect edges (use PIL ImageFilter or similar)
- Sample line widths at 20 random points
- Check if line widths cluster around the 3-tier standard (thin/mid/thick)
- Flag extreme outliers

**Report format:**
```python
qa_report(img_path) -> dict with keys:
  "silhouette": {"score": "distinct|ambiguous|blob", "thumbnail": PIL_Image}
  "value_range": {"min": int, "max": int, "range": int, "pass": bool}
  "color_fidelity": {dict from verify_canonical_colors()}
  "warm_cool": {"warm_hue": float, "cool_hue": float, "separation": float, "pass": bool}
  "overall_grade": "PASS|WARN|FAIL"
```

Also build:
- `qa_batch(directory) -> list[dict]` — run qa_report on all PNGs in a directory
- `qa_summary_report(results, output_path)` — write a Markdown summary of batch results

Output: `output/tools/LTG_TOOL_render_qa_v001.py`

---

## Deliverable 2: Run QA on All C25 New Assets

Once the tool is built, run it on all new assets from Cycle 25:
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v005.png`
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v002.png`
- `output/characters/main/turnarounds/LTG_CHAR_cosmo_turnaround_v002.png`
- `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v003.png`
- `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v001.png`
- All 3 new color model PNGs

Save QA results to: `output/production/qa_report_cycle26.md`

---

## Deliverable 3: Coordinate with Rin
Rin is building `LTG_TOOL_procedural_draw_v001.py` with `silhouette_test()` and `value_study()` functions. Align your interfaces — her functions should be importable into your QA tool, or vice versa.

---

## Standards
- Tool output ≤ 1280px for any generated images; prefer small test images (640px)
- Add the QA tool to `output/tools/README.md`

— Producer (via Alex Chen)
