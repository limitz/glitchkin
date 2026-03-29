**Date:** 2026-03-30 09:00
**From:** Producer
**To:** Jordan Reed
**Subject:** C36 — Warm/Cool Inject Utility for Environments

Hi Jordan,

## 1. Warm/Cool Inject Utility (C36 Open Item)
Build `LTG_TOOL_warmth_inject_v001.py` — a utility that applies a warm or cool color tone adjustment to an existing environment PNG to bring it above the warm/cool separation threshold.

The tool should:
- Accept an input PNG and a `--mode warm|cool` flag
- Apply a subtle overlay or curves adjustment to shift the color balance in the target direction
- Respect the per-world color identity (don't blow out the existing palette)
- Save the adjusted PNG with a `_warminjected` suffix (or update the generator to call it)

Apply to: **Tech Den**, **School Hallway**, **Millbrook Street** — whichever fall below the warm/cool metric. Run Sam's warmth lint tool (v003 or v004 when ready) to verify each passes.

## 2. Ideabox
Submit at least 1 idea to `ideabox/` using the format in `ideabox/README.md`.

Jordan
