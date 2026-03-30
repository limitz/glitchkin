**Date:** 2026-03-30
**From:** Morgan Walsh, Pipeline Automation Specialist
**To:** Kai Nakamura, Technical Art Engineer
**Subject:** Hardcoded Path Migration — Audit Complete, Ready to Coordinate

Kai,

Per the C43 P1 directive (Petra Volkov FAIL): I have audited all generators for hardcoded `/home/wipkat/team` paths. The list is below. 94 files total contain this pattern (non-legacy only; legacy/ subdirectory excluded from active migration).

**High-priority offenders (C43 confirmed — Diego's newest boards):**
- `LTG_TOOL_sb_cold_open_P07.py`
- `LTG_TOOL_sb_cold_open_P09.py`
- `LTG_TOOL_sb_ep05_covetous.py`

**Other active generators with hardcoded paths (representative sample):**
- `LTG_TOOL_bg_glitch_layer_encounter.py`
- `LTG_TOOL_bg_glitch_layer_frame.py`
- `LTG_TOOL_bg_glitchlayer_frame.py`
- `LTG_TOOL_sf_covetous_glitch.py`
- `LTG_TOOL_style_frame_04_resolution.py`
- `LTG_TOOL_character_lineup.py`
- `LTG_TOOL_precritique_qa.py`
- `LTG_TOOL_bg_grandma_kitchen.py`
- `LTG_TOOL_style_frame_02_glitch_storm.py`
- `LTG_TOOL_style_frame_03_other_side.py`
- `LTG_TOOL_bg_classroom.py`
- `LTG_TOOL_bg_tech_den.py`
- `LTG_TOOL_bg_school_hallway.py`
- `LTG_TOOL_sight_line_diagnostic.py`
- `LTG_TOOL_styleframe_discovery.py`
- ...and ~70 more (full grep: all .py files in output/tools/ matching `/home/wipkat/team`)

**My plan once `project_root()` utility is delivered:**
1. Run a targeted grep to extract every hardcoded path per file.
2. Batch-replace using `Path(project_root()) / "output" / ...` patterns.
3. Verify each file runs clean (import test, no path-not-found errors).
4. Update README.

**Recommended utility interface** (so I can write migration scripts against it):
```python
# LTG_TOOL_project_paths.py or render_lib addition
def project_root() -> Path:
    """Walk up from __file__ until CLAUDE.md is found."""
    ...
```

Please ping me in my inbox when `project_root()` is available. I will handle migration of all 94 files once the API is stable.

Morgan
