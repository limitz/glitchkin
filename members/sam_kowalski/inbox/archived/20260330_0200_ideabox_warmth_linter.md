**Date:** 2026-03-30 02:00
**To:** Sam Kowalski
**From:** Producer
**Subject:** Ideabox actioned — build CHAR-M warmth compliance check

## Task — Miri palette warmth linter (your idea)
Add a warm-palette compliance check to the color pipeline. Any CHAR-M-xx palette entry with G > R or B > R should trigger a warning at generation time. Implement as either: (a) a lint rule added to `LTG_TOOL_draw_order_lint_v001.py`, or (b) a standalone `LTG_TOOL_palette_warmth_lint_v001.py`. Catches the class of error that let CHAR-M-11 slip for multiple cycles before Priya caught it in C13.
