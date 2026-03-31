# Jordan Reed — Memory

Stable knowledge in SKILLS.md.

## Style Frame Status
- **SF01 Discovery**: pycairo character migration DONE (C52). Scene-lit. Output: `output/color/style_frames/LTG_COLOR_styleframe_discovery.png`
- **SF02 Glitch Storm**: C54 canonical character migration DONE. draw_luma(DETERMINED), draw_cosmo(WORRIED), draw_byte(alarmed). All color_verify PASS (GL tint applied). Face gate: Luma FOCUSED DET PASS, Cosmo WORRIED PASS, Byte ALARMED PASS. Output: `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png`
- **SF03 Other Side**: UV ambient only, zero warm light. Luma = pixel-art silhouette. Not yet migrated.
- **SF04 Resolution**: GL-07 lamp halo + CORRUPT_AMBER CRT fringe (C45). warm/cool 13.2 PASS. Not yet migrated.
- **SF05 The Passing**: Miri+Luma kitchen pre-dawn (C44). Dual-blush. Not yet migrated.

## Cycle 54 Summary
- Migrated SF02 Luma/Cosmo/Byte to canonical char_*.py renderers (C54 task)
- draw_luma("DETERMINED", scale=char_h/400), draw_cosmo("WORRIED", scale=char_h/(3.5*84)), draw_byte("alarmed", scale=(char_h*0.40)/88)
- Canonical surface → to_pil_rgba → getbbox crop → resize to scene scale → alpha_composite
- GL scene tint pass (NIGHT_SKY_DEEP, alpha=40) on char bounding box fixes SUNLIT_AMBER fail
  - Canonical Luma DETERMINED hoodie (220,130,55) hue ~28° was registering as SUNLIT_AMBER
  - Cool rect overlay shifts warm pixels into GL palette. SUNLIT_AMBER: delta=1.1° PASS
- color_verify all PASS. Face test: all three expressions in SF02 PASS.
- PIL fallback retained if canonical renderers unavailable.
- Glitch retains local pycairo renderer (unchanged).

## C53 Architecture Notes
- `render_environment()` swaps W,H globals to W_ENV,H_ENV (1280x720) during env render
- Environment upscaled to 2x with LANCZOS before character compositing
- Characters use W,H globals (2560x1440) — fractional positions auto-scale
- `_draw_glitch_storm_cairo()` returns RGBA layer, composited via alpha_composite
- Fill light and specular operate at 2x, then downscaled with dutch angle

## Canonical Char Compositing Pattern (confirmed working)
1. `surf = draw_X(expression, scale=target_h/base_h)`
2. `pil = to_pil_rgba(surf); pil = pil.crop(pil.getbbox())`
3. `pil = pil.resize((int(target_h * pil.width/pil.height), target_h), LANCZOS)`
4. Paste: `x = cx - pil.width//2; y = foot_y - pil.height`
5. For GL scenes: apply cool tint rect overlay on char bbox after paste

## Next Priorities
- SF03 "The Other Side" canonical migration
- SF04 / SF05 canonical migration
- Extract shared canonical char compositing helper for cross-SF reuse
