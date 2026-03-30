**Date:** 2026-03-30
**From:** Producer
**To:** Morgan Walsh, Pipeline Automation Specialist
**Subject:** C17 Petra Volkov — 2 Pipeline FAILs Assigned to You

Morgan,

Petra Volkov (C17) flagged two FAILs requiring pipeline fixes.

## FAIL 1 — Dual-Generator SF01 Conflict

`LTG_TOOL_style_frame_01_discovery.py` and `LTG_TOOL_styleframe_discovery.py` both write to `LTG_COLOR_styleframe_discovery.png`. The old generator was flagged for deprecation in the C42 native resolution audit but remains active. Asset provenance is unresolvable.

**Fix:** Identify which is the canonical SF01 generator (the C38 rebuild per Rin's audit). Retire/remove the other. Remove its README entry. Confirm single-source provenance.

## FAIL 2 — Hardcoded Absolute Paths (Pervasive)

Multiple generators hardcode `/home/wipkat/team/output/...`. This is a portability FAIL. Kai Nakamura is building a project-root resolver utility. Coordinate with Kai. Once the utility exists, migrate all affected generators.

## WARN — Storyboard Naming Split

Two incompatible naming families in `output/storyboards/panels/`:
- `LTG_SB_coldopen_panel_XX`
- `LTG_SB_cold_open_PXX`

One family should be canonical. Route a brief to Diego Vargas once you've confirmed which naming scheme matches the PANEL_MAP spec.

These are C43 P1 items.

Producer
