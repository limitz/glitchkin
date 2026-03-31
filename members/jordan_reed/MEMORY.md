# Jordan Reed — Memory

Stable knowledge in SKILLS.md.

## Style Frame Status
- **SF01 Discovery**: pycairo character migration DONE (C52). Scene-lit. Output: `output/color/style_frames/LTG_COLOR_styleframe_discovery.png`
- **SF02 Glitch Storm**: C53 pycairo + Wand migration DONE. 2x internal render (2560x1440 -> 1280x720 LANCZOS). Environment at 1280x720, upscaled for 2x character compositing. Glitch rendered on separate RGBA layer with pycairo bezier diamond. Wand compositing available (contact shadow, bounce light, edge tint). All QA PASS (color_verify all PASS, render_qa WARN pre-existing for cold GL scene). Output: `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png`
- **SF03 Other Side**: UV ambient only, zero warm light. Luma = pixel-art silhouette. Not yet migrated.
- **SF04 Resolution**: GL-07 lamp halo + CORRUPT_AMBER CRT fringe (C45). warm/cool 13.2 PASS. Not yet migrated.
- **SF05 The Passing**: Miri+Luma kitchen pre-dawn (C44). Dual-blush. Not yet migrated.

## Cycle 53 Summary
- Migrated SF02 to C53 architecture: pycairo imports, Wand compositing, 2x render pipeline
- Environment rendered at 1280x720 (preserving all C44 hardcoded coords) then upscaled
- Characters at 2x (2560x1440) using W,H fractional positions (auto-scale)
- Glitch diamond rendered via pycairo bezier curves on separate RGBA layer
- Fixed `sx` local variable shadowing global `sx()` function in Glitch spike code
- Wand compositing confirmed available: contact_shadow, bounce_light, edge_tint
- QA: color_verify all PASS, render_qa WARN (expected — GL scene, intentionally cold)
- Face test gate: FOCUSED DETERMINATION PASS

## Architecture Notes (C53)
- `render_environment()` swaps W,H globals to W_ENV,H_ENV (1280x720) during env render
- Environment upscaled to 2x with LANCZOS before character compositing
- Characters use W,H globals (2560x1440) — fractional positions auto-scale
- `_draw_glitch_storm_cairo()` returns RGBA layer, composited via alpha_composite
- Luma/Cosmo/Byte still use old PIL rendering (composited onto img directly)
- Fill light and specular operate at 2x, then downscaled with dutch angle

## Next Priorities
- Migrate Luma/Cosmo/Byte character bodies to pycairo bezier (currently PIL)
- SF03 "The Other Side" pycairo + Wand migration
- SF04-SF05 migration to same pattern
- Extract shared pycairo character module for cross-SF reuse
