**Author:** Lee Tanaka
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** Build an auto-band-discovery mode for depth_temp_lint that scans warmth at 5% Y increments, finds the maximum-separation FG/BG pair, and suggests override values for new assets. This would replace manual visual inspection when calibrating band positions for a new style frame. Output: recommended fg_y_frac, bg_y_frac, and the separation at those positions. Could be a `--discover` CLI flag or a `discover_bands(path)` API call.
**Benefits:** Any team member adding a new multi-character style frame to DEPTH_TEMP_PNGS could run `--discover` to get correct band positions in one command, then paste the values into depth_temp_band_overrides.json. Reduces calibration time from several minutes of manual scanning to a single CLI call. Prevents future false positives from default bands.
