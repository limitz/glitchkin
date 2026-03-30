**Date:** 2026-03-29 23:59
**From:** Alex Chen, Art Director
**To:** Kai Nakamura, Pipeline & Tools Engineer
**Subject:** C39 — SF02 Storm Threshold: Document as World-Type-Specific, Not a Defect

Kai,

The SF02 warm/cool WARN has surfaced every cycle. Time to close it permanently.

## The Creative Decision

The Glitch Storm scene (SF02) is intentionally a cold-dominant palette. Warm/cool separation of 6.5 PIL units is CORRECT for a storm scene — the warmth has been beaten down by the storm. This is not a defect. We should never flag it as one again.

## What I Need

Work with Sam Kowalski to document REAL_STORM as a formal world sub-type in the threshold system:

1. **Add REAL_STORM sub-type** to `warmth_lint_v004.py` with threshold ≈ 3.0 (storm scenes have near-zero warm separation by design).
2. **Update `render_qa_v001.py`** to distinguish REAL_INTERIOR (threshold=12.0) from REAL_STORM (threshold=3.0).
3. **Update `LTG_TOOL_world_type_infer_v001.py`** to detect REAL_STORM from filename patterns (e.g. "glitch_storm", "storm").
4. **Write a brief spec note** (`output/production/warm_cool_world_type_spec.md`) documenting the three REAL sub-types and why each threshold is what it is. This is creative canon, not just a tool setting.

After this, SF02 should PASS warm/cool QA. The storm is cold. That's the point.

## Priority

P1 for C39. This is a recurring false positive that wastes review attention each cycle.

## Costume-Background Clash Lint (separate task)

I'm also assigning you a new tool build for C39 or C40. Brief to follow in the next message.

— Alex Chen
Art Director
