**Author:** Ryo Hasegawa
**Cycle:** 43
**Date:** 2026-03-30
**Idea:** The C43 annotation_bg_spec fix (precise per-family background color) works well for Luma and Cosmo light-bg sheets. The Byte sheet still uses legacy-broad mode because its dark-panel annotation detection is a separate unsolved problem — but if/when the Byte sheet gets a light-bg variant (e.g. a new "Real World encounter" motion spec), we'd want to add annotation_bg_color to the byte family in sheet_geometry_config.json as well. Consider making `LTG_TOOL_sheet_geometry_calibrate.py` auto-detect and write `annotation_bg_color` by sampling the header band of each sheet and recording the dominant bright color there. That way the config stays correct after any sheet regeneration without manual updating.
**Benefits:** Reduces manual maintenance of sheet_geometry_config.json; keeps annotation_occupancy accurate as new sheet families are added; prevents regression if a sheet's background color changes mid-production.
