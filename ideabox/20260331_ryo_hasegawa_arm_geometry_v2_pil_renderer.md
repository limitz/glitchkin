# Idea: render_arm_pil() — PIL renderer for ArmGeometry v2

**Date:** 2026-03-31
**From:** Ryo Hasegawa

## Problem
C52 introduced `compute_arm_geometry()` and `render_arm_cairo()` as the v2 draw_shoulder_arm API. But most existing character generators (expression sheets, lineups, contact sheets) still use PIL-only rendering. They cannot use the new arm geometry without a PIL renderer.

## Proposal
Add `render_arm_pil(draw, geom, style)` that takes the same `ArmGeometry` output from `compute_arm_geometry()` and renders it using PIL ImageDraw calls (tapered_limb from curve_draw, ellipse for deltoid/hand). This completes the dual-render architecture proposed in C51.

## Impact
- All PIL-based generators can use gesture-spine-derived arm geometry without switching to pycairo
- Eliminates duplicated inline arm code in expression sheet generators
- One geometry computation, two render paths — consistent arms everywhere

## Effort
Small — the geometry is already computed. PIL renderer is a thin wrapper around existing curve_draw.tapered_limb + ImageDraw.ellipse calls. ~1 cycle.
