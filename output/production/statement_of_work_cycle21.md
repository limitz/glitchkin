# Statement of Work — Cycle 21
**Date:** 2026-03-30
**Work Cycles Completed:** 21
**Next:** Critique Cycle 10

---

## Team Change This Cycle
- Lee Tanaka (Storyboard) → **Temporarily Inactive** (Act 1+2 decks complete)
- **Kai Nakamura** (Technical Art Engineer) → **Joined** (procedural rendering, shared library)

---

## Objectives This Cycle

Final pre-Critique 10 pass: build shared rendering library, add STORM/CRACKED Byte expression, kitchen polish, color story documentation, pitch readiness audit.

---

## Deliverables

### Alex Chen — Art Direction
- `output/production/pitch_readiness_c21.md` — Full audit: all 9 key files verified present; overall **CONDITIONALLY READY**; 2 remaining risks (SF02 pane alpha, no standalone pitch brief); lead-with-5 assets identified

### Kai Nakamura — Technical Art Engineering *(first cycle)*
- `output/tools/ltg_render_lib.py` — Shared rendering utility library: 7 functions (`perlin_noise_texture`, `gaussian_glow`, `light_shaft`, `dust_motes`, `catenary_wire`, `scanline_overlay`, `vignette`)
- `output/backgrounds/environments/LTG_ENV_tech_den_v003.png` — Tech Den using library: `light_shaft()` for window beam, `dust_motes()` for particles, `gaussian_glow()` for monitor spill, `vignette()` final pass
- `output/backgrounds/environments/LTG_ENV_glitchlayer_frame_v003.png` — Glitch Layer with `scanline_overlay()` final pass (CRT screen feel)

### Maya Santos — Character Design
- `output/characters/main/LTG_CHAR_byte_expression_sheet_v003.png` — Upgraded to 3×3 9-panel layout; STORM/CRACKED panel added (Section 9B dead-pixel glyph + Hot Magenta crack + body tilt +18°)
- `output/characters/main/LTG_CHAR_luma_classroom_pose_v002.png` — Line weight violations fixed (brows/lids/hair 5-8px→2-3px)

### Jordan Reed — Backgrounds
- `output/backgrounds/environments/LTG_ENV_grandma_kitchen_v002.png` — Floor linoleum tile grid + worn path, upper wall period wallpaper texture, CRT glow radius increased with ambient ring

### Sam Kowalski — Color & Style
- `output/color/palettes/master_palette.md` — "Palette Status" section added; GL complete, Act 2 environments complete; 4 minor cross-check gaps flagged
- `output/color/style_frames/ltg_style_frame_color_story.md` — Full color narrative arc: SF01 warm→SF02 contested→SF03 alien cold

---

## Pre-Critique 10 Package State

### All 4 Characters — COMPLETE
| Character | Expression Sheet | Turnaround | Color Model |
|-----------|-----------------|-----------|-------------|
| Luma | v003 ✓ | ✓ | ✓ |
| Byte | v003 ✓ (STORM/CRACKED added) | ✓ | ✓ |
| Cosmo | v003 ✓ | ✓ | ✓ |
| Grandma Miri | v002 ✓ | v001 ✓ | ✓ |

### Style Frames
- SF01: A+ LOCKED
- SF02: v004, conditionally ready (window pane alpha 160-180, minor)
- SF03: v003, verified ready

### Shared Rendering Library
- `ltg_render_lib.py` built and in use — future generators should import it

### Pitch Readiness
- **Assessment: CONDITIONALLY READY for Critique 10**
- Lead assets: SF01 → SF03 → Act 2 contact sheet v006 → SF02 → Miri expression sheet v002
