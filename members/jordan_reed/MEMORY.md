# Jordan Reed — Memory

Stable knowledge in SKILLS.md.

## Style Frame Status
- **SF01 Discovery**: pycairo character migration DONE (C52). Scene-lit. Luma+Byte smooth bezier curves, gradient fills, contact shadow, bounce light, post-character lighting overlay. Output: `output/color/style_frames/LTG_COLOR_styleframe_discovery.png`
- **SF02 Glitch Storm**: native 1280x720 (C44 refactor). Magenta fill + cyan specular (C34). Dutch angle. Intentionally cold scene (warm/cool WARN expected).
- **SF03 Other Side**: UV ambient only, zero warm light. Luma = pixel-art silhouette.
- **SF04 Resolution**: GL-07 lamp halo + CORRUPT_AMBER CRT fringe band (C45). warm/cool 13.2 PASS.
- **SF05 The Passing**: Miri+Luma kitchen pre-dawn (C44). Dual-blush logic implemented.
- **Next priority**: Extract pycairo character functions into shared module for SF02-SF05 migration. Build Miri and Cosmo using same approach.

## Cycle 52 Summary
- Migrated SF01 characters to pycairo bezier curves with gradient fills (LinearGradient, RadialGradient)
- 2x internal render (2560x1440 -> 1280x720 LANCZOS) for smooth AA
- Wand contact shadow (gaussian_blur) with PIL+scipy fallback
- All C38 posture/expression + C47 sight-line geometry preserved
- QA: render_qa PASS (WARN pre-existing), color_verify all PASS
- Ideabox: cairo character library proposal

## Cycle 51 Summary
- freetype-py eval: AA identical to PIL (both use FreeType backend), 13x slower. Verdict: freetype-py for logo/title only, PIL for labels.
- Wand eval: BLOCKED on ImageMagick (`libmagickwand-dev` not installed). PIL+scipy covers blur.
- Key finding: PIL + scipy + numpy covers everything Wand offers without system dependency.

## Next Priorities
- Shared pycairo character module for SF02-SF05 migration
- Build Miri and Cosmo pycairo renderers
- SF02-SF05 character migration to pycairo
