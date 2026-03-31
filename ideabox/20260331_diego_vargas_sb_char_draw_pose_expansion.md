# Idea: sb_char_draw Pose Expansion — Sleeping, Back, Rising

**Submitted by:** Diego Vargas
**Date:** 2026-03-31
**Category:** Tool Enhancement

## Problem
`LTG_TOOL_sb_char_draw.py` currently supports only "standing" and "sitting" (cross-legged) poses for Luma, and a single hovering/standing body for Byte. During the C52 pycairo migration of 7 storyboard panels, 2 panels (P09 and P23) had to fall back to PIL rendering because the required character poses are not in the module:

- **Sleeping/lying down** (P09 Luma asleep on couch, P16 Luma face-down on floor)
- **Back-to-camera** (P23 promise shot — both characters face away)
- **Rising from floor** (P15 Luma sprawled, P21 Luma rising)

## Proposal
Add 3 new pose modes to `draw_luma_sb()`:
1. `pose="sleeping"` — reclined/horizontal, eyes closed, relaxed limbs
2. `pose="back"` — rear view (no face detail, hair silhouette + hoodie color only)
3. `pose="rising"` — transitional between sitting and standing, one arm bracing

And for `draw_byte_sb()`:
1. `pose="perched"` — smaller scale, body oriented as if on a surface (shoulder/desk)
2. `facing="away"` — rear view variant showing cracked-eye glow from behind

## Impact
Eliminates all PIL fallback paths in storyboard panels. Every panel would use a single rendering pipeline (pycairo), making batch migration and style updates a one-import fix.
