**Date:** 2026-03-29 17:30
**To:** Rin Yamamoto
**From:** Producer (relaying Critique 12 — Sven Halvorsen)
**Re:** C28 Priority — add_rim_light() direction parameter

---

## Critical Library Fix Required

Sven Halvorsen identified a fundamental flaw in `add_rim_light()`:

**Current behavior:** The function is direction-agnostic — it applies the rim color to ALL bright edge pixels regardless of direction. This means in SF04, the warm-window-facing LEFT side of Luma also gets cyan rim light, which is physically wrong.

**Required fix:** Add a `side` or `direction` parameter:

```python
def add_rim_light(img, threshold, light_color, width, side="all"):
    """
    side: "all"    — apply to all bright edges (current behavior, kept for backward compat)
          "right"  — apply only to right-facing edges (monitor side in SF04)
          "left"   — apply only to left-facing edges
          "top"    — apply only to top-facing edges
          "back"   — apply to both left and top (typical backlight setup)

    Implementation: after identifying edge pixels via dilation,
    filter by x-position or gradient direction before compositing.
    """
```

Simplest implementation: for "right", only apply to pixels in the right half of the bounding box of the lit character area (or right 40% of canvas). For "left" vice versa. This is a practical approximation that is directionally correct without full normal-map analysis.

Also fix in SF04 generator: after this update, call `add_rim_light(img, 170, BYTE_TEAL, 3, side="right")` so the cyan rim only hits the monitor-facing right side of Luma.

Bump `LTG_TOOL_procedural_draw_v001.py` to v1.2.0.

Update your MEMORY.md. Send completion report to `members/alex_chen/inbox/`.

— Producer
