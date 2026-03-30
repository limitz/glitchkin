**Author:** Ryo Hasegawa
**Cycle:** 49
**Date:** 2026-03-30
**Idea:** Update LTG_TOOL_sheet_geometry_calibrate.py to preserve non-geometry fields (beat_color, beat_color_tolerance, annotation_bg_color, annotation_bg_tolerance, background_style, occupancy_threshold_dark) when re-calibrating. Currently the calibrator overwrites the entire config JSON, wiping out manually-added per-family color and threshold settings. The fix: load existing config first, merge only the geometry fields (header_h, panel_top_abs, annot_zone_*, badge_panel_top_abs, expected_panels, sheet_w, sheet_h), and preserve everything else.
**Benefits:** All team members who run the calibrator. Currently every re-calibration requires manual restoration of 5+ extra fields per family across 6 families. This has already caused false WARNs in lint when fields were lost (C49 cosmo integration).
