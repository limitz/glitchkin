<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Native Resolution Audit — C42
**Author:** Rin Yamamoto
**Date:** 2026-03-30
**Context:** C41 root cause: generators drawing at 1920×1080 then LANCZOS thumbnail() to
1280×720 cause anti-aliased thin outlines to produce blended pixels with shifted LAB hue
values (UV_PURPLE ΔE up to 27.78). Fix: native 1280×720 canvas eliminates downscale entirely.

---

## Pattern 1: 1920×1080 + LANCZOS thumbnail() [HIGH RISK — LAB ΔE color drift]

| Generator | Status | Action |
|---|---|---|
| `LTG_TOOL_style_frame_02_glitch_storm.py` | **FLAGGED — SIGNIFICANT REFACTOR** | 300+ lines of geometry at 1920×1080 absolute pixel scale. Inlined fill light algorithm (`draw_magenta_fill_light_c36`) explicitly at 1920×1080. Post-thumbnail specular restore pass (scales back from thumbnail size). C37 MEMORY explicitly notes: "SF02 v008's inlined algorithm is at 1920×1080. The refactored module is for future use — v008 does NOT need updating." Refactor requires rescaling all character geometry, fill light algorithm, and Dutch angle transform. **Not changed this cycle.** |

**Recommendation:** SF02 refactor is a dedicated cycle task for Jordan Reed or Rin Yamamoto.
The specular restore post-thumbnail pass adds additional complexity. Assign when SF02 is
next in active edit cycle.

---

## Pattern 2: 1920×1080 without thumbnail() [size rule violation, no LANCZOS color drift]

These generators save at full 1920×1080 — violates the ≤1280px size rule (docs/image-rules.md)
but do NOT have the LANCZOS anti-aliasing color drift risk. Geometry is mostly fraction-based
(`int(W * frac)`, `int(H * frac)`), making a one-line canvas change safe.

### Fixed this cycle (canvas changed to 1280×720)

| Generator | Change | Notes |
|---|---|---|
| `LTG_TOOL_bg_glitchlayer_frame.py` | W,H = 1280,720 | Fraction-based geometry. Absolute platform heights (ph=14 to 46) will render proportionally larger — acceptable. No canonical color regions at those positions. Output: `LTG_ENV_glitchlayer_frame.png`. |
| `LTG_TOOL_bg_glitch_layer_frame.py` | W,H = 1280,720 | Same pattern as above (older version / near-duplicate). Output: `glitch_layer_frame.png`. |
| `LTG_TOOL_bg_glitch_layer_encounter.py` | W,H = 1280,720 | Fraction-based geometry. Absolute platform heights (ph=24 to 44) — same assessment. Output: `LTG_ENV_glitchlayer_encounter.png`. |

### Flagged — significant geometry refactoring required

| Generator | Reason |
|---|---|
| `LTG_TOOL_bg_glitch_storm_colorfix.py` | Many hardcoded absolute pixel values (520, 380, 1380, 1500, 1620, 1760, etc.) throughout cloud/storm geometry. Converting requires rescaling every shape. Assign to Jordan Reed. |
| `LTG_TOOL_style_frame_01_discovery.py` | Largely superseded by `LTG_TOOL_styleframe_discovery.py` (C38 canonical rebuild at 1280×720). Both output to `LTG_COLOR_styleframe_discovery.png`. Many hardcoded absolute values (lean 48px, screen figures 15px, etc.). Recommend: deprecate in favor of canonical C38 version. |

---

## Summary

| Total generators audited | 6 |
|---|---|
| Fixed this cycle (native 1280×720) | 3 |
| Flagged — significant refactor | 3 |
| Already native 1280×720 (from C41) | 2 (LTG_TOOL_bg_other_side.py, LTG_TOOL_style_frame_03_other_side.py) |

---

## Lessons

- The C41 LANCZOS color drift risk is ONLY for Pattern 1 (thumbnail downscale from 1920).
  Pattern 2 (no thumbnail) saves at wrong size but has no hue drift — different risk profile.
- Fraction-based geometry (`int(W * frac)`) makes canvas constant change trivial.
  Absolute pixel values (platform heights, cloud shapes, character px positions) need
  explicit rescaling when changing canvas.
- SF02 refactor complexity: the post-thumbnail specular restore pass is
  1920-aware and would need to be completely removed (redrawn at native 1280 scale).
  This is a full session of work, not a one-liner.
