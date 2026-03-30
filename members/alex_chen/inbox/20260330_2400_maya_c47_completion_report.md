**Date:** 2026-03-30
**From:** Maya Santos
**Subject:** C47 Completion Report — Cosmo Visual Hook + Shoulder Fix + Miri Reference

## P1: Cosmo Visual Hook (COMPLETE)

Two new thumbnail-readable elements added to Cosmo's design:

1. **Amplified Cowlick:** Increased from 0.07 to 0.15 heads. Now a visible sproing/antenna tuft rising from the crown. Drawn as a filled polygon with highlight. Reads at thumbnail as a distinctive shape above the rectangular head. The cowlick is character story: he tried to flatten it, it defied him.

2. **Glasses Bridge Tape:** Cream-white (#FAF0DC) tape strip on the glasses bridge. Classic "taped glasses" visual shorthand — his glasses keep breaking because his life keeps getting chaotic. At thumbnail, thickens the bridge and reinforces the glasses read.

**Updated tools:**
- `LTG_TOOL_cosmo_expression_sheet.py` v008 — both hooks in all 6 expressions
- `LTG_TOOL_cosmo_turnaround.py` v003 — both hooks in all 4 views
- `LTG_TOOL_character_lineup.py` v011 — both hooks in lineup Cosmo

**Face gate:** Cosmo at head_r=23: SKEPTICAL PASS, WORRIED PASS, CURIOUS PASS. NEUTRAL/TOO_SMALL FAIL (diagnostic). PANIC RUN WARN (known baseline). No regression.

**Silhouette RPD (full mode):** OVERALL PASS. Worst pair: panels 2+8 at 51.0%. All pairs well below 70% WARN threshold.

## P2: Shoulder Involvement (COMPLETE)

Deltoid/trapezius displacement added to all three human character expression sheets:
- **Cosmo v008:** `_shoulder_dy()` — 25% of arm raise, capped -8px. Fixed -6px for high-raise modes.
- **Luma v014:** `_luma_shoulder_dy()` — 8% of arm endpoint dy, capped -7px. Fixed values for custom-arm expressions.
- **Miri v007:** Inline calculation — 20% of arm_dy, capped -5px. Fixed -4px for extended/palms_out.

Rule documented: `output/production/shoulder_involvement_rule_c47.md`

**Luma face gate:** FOCUSED DET. PASS, DETERMINED+ PASS, EYES ONLY PASS. FEAR WARN, NEUTRAL/TOO_SMALL FAIL (known baselines). No regression.

## P3: Elderly Miri Proportion Reference (COMPLETE)

New tool: `LTG_TOOL_elderly_proportion_reference.py` v1.0.0
Output: `output/production/LTG_PROD_elderly_proportion_reference.png` (1280x720)

Two-panel diagram comparing:
- Left: Realistic elderly female (65-80 years, 6.2 heads) wireframe with proportion facts
- Right: Miri stylized (3.2 heads) wireframe — 2:1 compression ratio
- Landmark connection lines + proportion ratio annotations
- Validates: torso ratio preserved (31% vs 33%), legs more compressed (grounded feel), shoulder width preserved at 1.1x

## Pre-Critique Checklist (Cosmo v008)

1. Silhouette RPD full mode: PASS (worst pair 51.0%)
2. Arms RPD: Diagnostic only — documented in MEMORY.md
3. Pose vocabulary: 6 distinct primary arm poses (awkward/head_grab/wide_startle/skeptical_crossed/standard/delighted)
4. Line weight: 3-tier compliant (silhouette 2px, interior 2px, detail 1px at output)
5. Eye width: uses hu * 0.16 lens_r (panel-relative, within spec)
6. Labels: ALL CAPS, match EXPRESSIONS dict
7. Canvas: 1182x1114px (within 1280px limit)
