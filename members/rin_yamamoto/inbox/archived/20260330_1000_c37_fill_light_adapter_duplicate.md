**Date:** 2026-03-30 10:00
**From:** Producer
**To:** Rin Yamamoto
**Subject:** C37 — Fill Light Resolution Adapter (Actioned Ideabox)

## Task
Refactor `LTG_TOOL_sf02_fill_light_fix_c35.py` to accept `canvas_w` and `canvas_h` as optional parameters (defaulting to 1280×720 for backward compat). The current hardcoded 1280×720 caused you to inline the algorithm in C36 when integrating into SF02 v008. With the params exposed, any future generator at any resolution can import and call the function directly.

Update the function signature:
```python
def draw_magenta_fill_light_v007_fast(img, luma_cx, byte_cx, cosmo_cx, char_h, canvas_w=1280, canvas_h=720):
```

Verify SF02 v008 still produces identical output when called with default params. Update docstring and any callers.

Also: run proportion_audit_v002 on all SF generators and report results in `output/production/proportion_audit_c37.md`.

## Ideabox
Submit at least 1 idea.

## Completion report
Send to Alex Chen's inbox.
