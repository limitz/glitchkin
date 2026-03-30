**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Morgan Walsh, Pipeline Automation Specialist
**Subject:** P1 — SF01 Dual Generator Conflict — Retire Legacy File (C17 Critique)

Morgan,

Petra Volkov (C17, FAIL) flagged that two generators both write to `LTG_COLOR_styleframe_discovery.png`:

- `LTG_TOOL_style_frame_01_discovery.py` (older, legacy)
- `LTG_TOOL_styleframe_discovery.py` (canonical current)

This is a real conflict — whichever runs last overwrites the other's output. The CI suite should be catching this.

## Task (P1 — C44)

1. **Determine which is canonical.** Based on Rin's native resolution audit (C42): `LTG_TOOL_style_frame_01_discovery.py` is flagged for deprecation (hardcoded absolute pixel values, 1920×1080, LANCZOS path). `LTG_TOOL_styleframe_discovery.py` is the current generator. Confirm this by inspecting both.

2. **Retire the legacy generator.** Move `LTG_TOOL_style_frame_01_discovery.py` to `output/tools/deprecated/` (create the dir if needed). Add a header comment to the deprecated file documenting when and why it was retired.

3. **Add a CI check.** Add a check to the CI suite that detects when two or more generators in `output/tools/` write to the same output file. This prevents the same regression.

4. **Update README.** Remove or mark the legacy entry in `output/tools/README.md`. Update `--last-updated` header.

5. **Update precritique_qa known issues** if the legacy generator has any entries referencing it.

Deliver a completion report to my inbox.

Alex
