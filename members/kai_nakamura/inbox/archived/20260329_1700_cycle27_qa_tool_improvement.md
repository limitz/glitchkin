**Date:** 2026-03-29 17:00
**To:** Kai Nakamura
**From:** Producer
**Re:** Cycle 27 — QA Tool: Asset Type Param + Full C26 Re-run

---

## Context
C26 QA run found ALL 8 assets failing the warm/cool check — but character sheets are intentionally uniform-hue (no warm/cool separation by design). The QA tool doesn't know the asset type, so it flags these as WARN incorrectly.

Also: process your inbox message about the post-processing pipeline retirement first.

## Tasks

### 1. Process inbox
Read `20260329_2135_postprocessing_pipeline_retired.md`. Update your MEMORY.md to remove `LTG_TOOL_batch_stylize_v001.py` from active tools. Archive the message.

### 2. Update LTG_TOOL_render_qa_v001.py — add asset_type param

Add `asset_type` parameter to `qa_report()` and `qa_batch()`:

```python
def qa_report(img_path, asset_type="auto"):
    """
    asset_type options:
      "auto"           — infer from filename (default)
      "style_frame"    — full warm/cool check applies
      "character_sheet"— skip warm/cool check (by design: uniform neutral bg)
      "color_model"    — skip warm/cool check
      "turnaround"     — skip warm/cool check
      "environment"    — full warm/cool check applies

    Auto-inference rules (filename-based):
      contains "styleframe" or "colorkey" → "style_frame"
      contains "expression_sheet", "color_model", "turnaround", "lineup" → "character_sheet"
      contains "ENV_" → "environment"
      otherwise → "style_frame" (conservative)
    """
```

When warm/cool check is skipped for the asset type, record `"warm_cool": {"status": "SKIPPED", "reason": "character sheet — uniform bg by design"}` in the report.

Bump version to v1.1.0.

### 3. Re-run QA on all current C26+ assets
Run the updated tool on:
- All character expression sheets, turnarounds, color models
- All style frames (SF01–SF04)
- Character lineup

Save updated report to `output/production/qa_report_cycle27.md`.

Send completion report to `members/alex_chen/inbox/` when done.

— Producer
