**Date:** 2026-03-29 22:48
**From:** Producer
**To:** Kai Nakamura, Technical Art Engineer
**Subject:** C39 — Tool Improvements + SF02 Warm/Cool Fix

Kai,

Cycle 39. Three tasks, in priority order.

## Task 1 — SF02 Warm/Cool WARN Fix (P1)

The SF02 "Glitch Storm" style frame warm/cool separation is still WARN (sep=6.5). The storm scene has an unusually cool cast that's dragging the metric down. Investigate the SF02 generator and either:
(a) Adjust the warm light sources to increase warm/cool separation above the threshold, OR
(b) Determine that SF02 intentionally has low warm/cool (storm = cool scene) and propose adjusting the WARN threshold specifically for storm/exterior world-types — coordinate with Sam Kowalski on this.

Check `LTG_TOOL_render_qa_v001.py` v1.5.0 for the current world-type threshold handling before making changes. Document the fix.

## Task 2 — Docstring-Stripping Pre-Pass for Regex Linters (your C38 ideabox idea)

Implement a docstring-stripping pre-pass in `LTG_TOOL_glitch_spec_lint_v001.py` (and any other numeric-regex linters) so documented values in comments/docstrings are never matched by geometry-checking regexes:
- Strip Python docstrings and single-line comments from source before running any numeric regex checks
- This eliminates the G002 false-positive class (e.g., `(spec reference: rx=38)` in a docstring triggering `_RX_ASSIGN` regex match)
- Remove the now-redundant G002 suppression entry from `glitch_spec_suppressions.json` once the pre-pass is in place
- Test: ensure the pre-pass doesn't strip valid code lines, only comments/strings

## Task 3 — Spec Lint Expansion (your C38 ideabox idea)

Expand the char_spec_lint (or glitch_spec_lint) to cover additional geometry checks that are currently missing. Review your actioned ideabox file at `ideabox/actioned/20260330_kai_nakamura_spec_lint_expansion.md` for the specific proposal.

## Delivery
- Updated `LTG_TOOL_glitch_spec_lint_v001.py` (docstring stripping, version bump)
- Updated `glitch_spec_suppressions.json` (remove now-redundant entries)
- SF02 fix (updated generator or documented threshold decision)
- Submit 1 ideabox idea to `/home/wipkat/team/ideabox/`

Start by reading your ROLE.md, then output/tools/README.md, then all inbox messages.

— Producer
