**Date:** 2026-03-30
**From:** Jordan Reed
**Subject:** Scene-Lit Character Pipeline — Shared Module Proposal

## Problem
Characters across all 5 style frames look like cutouts pasted onto backgrounds because they carry baked-in colors regardless of scene lighting. The C50 prototype (SF01 scene-lit) demonstrates that scene-responsive shading dramatically improves integration.

## Proposal
Build `LTG_TOOL_scene_lit_character.py` — a shared module that any style frame generator can import:

1. **`scene_tinted_color(base_color, scene_lights, pixel_pos)`** — Given a base character color and a list of scene light sources (position, color, intensity), returns the color tinted by scene lighting at that pixel position. Replaces all baked character gradients.

2. **`draw_contact_shadow(draw, char_bbox, surface_color)`** — Draws a soft elliptical contact shadow beneath any character. Configurable width, softness, surface color.

3. **`draw_bounce_light(img, char_bbox, surface_color, influence)`** — Applies upward bounce from the ground plane onto the character's lower portion.

4. **`apply_scene_overlay(img, scene_lights)`** — Full-frame lighting overlay that can be called AFTER character draw, so characters receive scene light.

## Why shared module
Every SF generator (01-05) needs the same scene-lighting math. Duplicating it per generator = drift. One module = one fix propagates everywhere.

## Priority
HIGH — this is the single biggest visual quality lever remaining. All critics flag it. The prototype proves it works.
