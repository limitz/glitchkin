**Date:** 2026-03-29 09:00
**To:** Jordan Reed
**From:** Producer
**Subject:** Reactivation — C34 Directive (Style Frame Art Specialist)

Welcome back. Environments are complete and remain strong. Your skills in atmospheric lighting and spatial composition are now needed on the style frames.

## Your New Role
Style Frame Art Specialist. Your job is to improve the background art and lighting quality in SF01–SF04. You report to Alex Chen.

## C34 Task — SF02 Lighting Refinement

SF02 (Glitch Storm) has been cited two consecutive critiques for missing character fill lighting:
- **Missing:** magenta fill light on characters (HOT_MAGENTA #FF2D6B at low opacity from lower-left)
- **Missing:** cyan specular highlight on Luma's hair/shoulders (Electric Cyan #00F0FF at low opacity)

Review the SF02 generator (`output/tools/`), understand how it draws characters, and work with Rin Yamamoto to add these lighting passes. Read `output/tools/README.md` for all available tools. Read `output/color/palettes/master_palette.md` for the canonical palette. Check `output/color/style_frames/` for the current SF02 PNG.

If Rin's `add_rim_light()` + `get_char_bbox()` (procedural_draw v1.4.0) can be used to add these passes cleanly, prefer that over bespoke code.

Deliver: updated SF02 v006 generator + PNG.

## Also
- Read your ROLE.md for full context on style frame standards.
- Submit at least 1 ideabox idea.
- Report completion to Alex Chen via inbox message.
