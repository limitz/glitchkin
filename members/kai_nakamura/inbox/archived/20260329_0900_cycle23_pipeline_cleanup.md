**Date:** 2026-03-29 09:00
**To:** Kai Nakamura
**From:** Producer
**Re:** Cycle 23 — Pipeline Cleanup & Rin Integration Support

## Assignment

Cycle 23 priorities for Kai:

1. **Remove Deprecated Wrapper** — Delete `output/tools/ltg_render_lib.py` (the deprecated shim that wraps `LTG_TOOL_render_lib_v001.py`):
   - Before deleting, grep the entire `output/` directory to confirm no scripts still import it
   - If any scripts still import `ltg_render_lib`, update them to use `LTG_TOOL_render_lib_v001`
   - After confirming zero references, delete the file
   - Update `output/tools/README.md` to remove any mention of the deprecated wrapper
   - Document the cleanup in the README

2. **Support Rin Yamamoto's Tool Integration** — Rin is building `LTG_TOOL_stylize_handdrawn_v001.py`. She will extend the PIL pipeline with stylization post-processing. Your role:
   - Review her tool once delivered to confirm it follows pipeline conventions (naming, import style, function signatures)
   - Ensure her tool is compatible with `LTG_TOOL_render_lib_v001.py` imports
   - If she needs any new utility functions in the render lib (e.g., noise helpers), implement them and document in README
   - Coordinate via inbox if dependencies arise

3. **Tools README Update** — After all Cycle 23 tool work is complete:
   - Update `output/tools/README.md` to reflect current state: list all active tools, their functions, and usage examples
   - Archive or remove entries for any removed tools

## Notes
- Import convention: `from output.tools.LTG_TOOL_render_lib_v001 import *`
- All tools must be Python PIL/NumPy only (open source)
- LTG naming: `LTG_TOOL_[descriptor]_v[###].py`
