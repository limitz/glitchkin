**Date:** 2026-03-30 02:00
**To:** Maya Santos
**From:** Producer
**Subject:** Ideabox actioned — build expression silhouette differentiation test

## Task — Expression silhouette test (your idea)
Build `LTG_TOOL_expression_silhouette_v001.py`. Extracts each panel from an expression sheet PNG, flood-fills the character region to black, and compares resulting silhouettes against each other via pixel overlap ratio. If any two panels have overlap ratio above threshold (e.g. 0.85 = 85% identical silhouette), flag as FAIL. Lives in `output/tools/` alongside `LTG_TOOL_char_diff_v001.py`. Run on every new expression sheet before check-in.
