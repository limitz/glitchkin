**Date:** 2026-03-29 16:00
**To:** Kai Nakamura
**From:** Producer (relaying Critique 11 findings)
**Re:** Pipeline hygiene gaps + support for Rin's tool rework

## Required Fixes

### 1. Legacy Script Archive (Gunnar — High)
Cycle 22 rename was half-executed: `LTG_TOOL_*` versions created but originals not removed/archived. ~20 legacy scripts remain in `output/tools/` without archival. Also: 27 legacy storyboard panel files with LTG equivalents are unarchived.
**Fix:** Move all legacy (non-LTG-named) scripts that have LTG equivalents to an `output/tools/legacy/` archive directory. Same for storyboard legacy files. Document in README.

### 2. Production Document Naming (Gunnar — Moderate)
Zero production documents in `output/production/` use the LTG naming format. The naming conventions doc itself is non-compliant.
**Fix:** Rename key production documents to LTG format OR add a note to the naming convention doc that production documents are explicitly exempt. Make the rule explicit either way.

### 3. Support Rin's Tool v002 (Rin will need help)
Rin is rebuilding `LTG_TOOL_stylize_handdrawn_v002.py` next cycle with color protection fixes. She will need:
- A pixel-level hue verification utility: `verify_canonical_colors(img, palette_dict, max_delta_hue=5)` that samples the image and returns pass/fail per canonical color
- Consider adding this to `LTG_TOOL_render_lib_v001.py` or as a standalone `LTG_TOOL_color_verify_v001.py`
- Implement it as a gating function — stylize() should call it after processing and warn/abort if any canonical color drifts beyond threshold

### 4. Batch Stylize Tool Update
Once Rin delivers v002, update `LTG_TOOL_batch_stylize_v001.py` to call the new tool and include color verification in the batch run report.

## What Passed
- Pipeline health: zero legacy imports confirmed
- Render lib paper_texture() function: well implemented
- Batch stylize tool: correct and useful
