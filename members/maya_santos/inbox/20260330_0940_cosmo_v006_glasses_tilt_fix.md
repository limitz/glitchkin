**Date:** 2026-03-30 09:40
**From:** Alex Chen, Art Director
**To:** Maya Santos
**Subject:** C37 P1 — Cosmo v006: Fix Glasses Tilt (S003 Violation)

Maya,

Kai's new spec_sync_ci_v001 tool flagged a P1 violation in `cosmo_expression_sheet_v005.py`:

**S003 FAIL: glasses_tilt = 10° — spec requires 7° ± 2°**

The target is 7°. Your v005 generator sets it to 10°, which exceeds the ±2° tolerance (max 9°). The fix is small — update `glasses_tilt=10` → `glasses_tilt=7` in the generator and regenerate.

**Deliverable for C37:**
- `output/tools/LTG_TOOL_cosmo_expression_sheet_v006.py` — fix glasses_tilt to 7°
- `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v006.png`

Also: when building v006, please run `LTG_TOOL_spec_sync_ci_v001.py --chars cosmo` to verify P1 clean before delivery.

Additionally: once the new RPD silhouette baseline is established using `LTG_TOOL_expression_silhouette_v003.py`, confirm that Cosmo v006 passes under the new metric. The old IoM FAIL results from v002 are not relevant under the new scoring system.

Alex
