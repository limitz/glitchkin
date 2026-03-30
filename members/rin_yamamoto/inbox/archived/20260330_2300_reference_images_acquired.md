**Date:** 2026-03-30 23:00
**From:** Producer
**To:** Rin Yamamoto

Reference images are now available in `reference/` (gitignored, local only). Key folders for your work:

- `reference/crt/` (18 files) — CRT glow in dark rooms. Build `LTG_TOOL_glow_profile_extract.py` (fit Gaussian to radial falloff → σ_x/σ_y for glow generators).
- `reference/glitches/` (10 files) — Datamoshing, pixel sorting. Build `LTG_TOOL_uv_hue_cluster.py` (hue histogram → validate UV_PURPLE 270°±15° dominance).
- `reference/scanline closeup/` (6 files) — Scanline pitch and inter-line darkness ratios.
- `reference/crt static/` (5 files) — Spatial frequency distribution for corruption texture.
- `reference/crt afterglow/` (3 files) — Phosphor decay hue shift (CORRUPT_AMBER path).

Full updated list: `docs/reference_shopping_list.md`. The glow profile extractor and UV hue cluster tools are HIGH/MEDIUM priority — build when you have bandwidth.
