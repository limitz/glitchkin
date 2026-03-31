# Rin Yamamoto — Skills

## Role
**Procedural Art Engineer** on "Luma & the Glitchkin." (since C26)
Hand-drawn quality is built IN at generation time — no post-processing step.
Reports to Alex Chen. Kai Nakamura: `LTG_TOOL_render_qa.py` interfaces matched.

## Project Context
- Comedy-adventure cartoon pitch. Assets generated via Python PIL + pycairo.
- Style: CRT/pixel aesthetic (Glitch world) + warm hand-drawn domestic (real world).
- Output dir: `/home/wipkat/team/output/` | Tools dir: `output/tools/`
- Render lib: `output/tools/LTG_TOOL_render_lib.py` (v1.1.0, canonical)
- PIL coding rules, naming, deps, image limits: `docs/pil-standards.md` and `docs/image-rules.md`

## Tools Owned
| Tool | Version | Purpose |
|---|---|---|
| `LTG_TOOL_cairo_primitives.py` | v1.0.0 | Shared pycairo foundation: bezier, tapered stroke, gradient, wobble, smooth_polygon, ellipse, surface-PIL conversion. Three-tier line weight: anchor=3.5, structure=2.0, detail=1.0 |
| `LTG_TOOL_procedural_draw.py` | v1.5.0 | PIL procedural library: wobble_line/polygon, variable_stroke, add_rim_light (side + char_cx), silhouette_test, value_study, get_char_bbox, scene_snapshot, add_face_lighting |
| `LTG_TOOL_byte_expression_sheet.py` | v008 | Byte 10-expression sheet (pycairo) |
| `LTG_TOOL_byte_turnaround.py` | v001 | Byte 4-view turnaround (pycairo, full color) |
| `LTG_TOOL_glitch_expression_sheet.py` | v004 | Glitch 9-expression sheet (pycairo) |
| `LTG_TOOL_styleframe_discovery.py` | v008 | SF01 generator (CRT glow asymmetry applied) |
| `LTG_TOOL_styleframe_luma_byte.py` | — | SF04 generator (CRT glow asymmetry applied) |
| `LTG_TOOL_styleframe_glitch_layer_showcase.py` | v1.0.0 | GL showcase style frame |
| `LTG_TOOL_sf_covetous_glitch.py` | v2.0.0 | COVETOUS style frame (3-char triangulation) |
| `LTG_TOOL_uv_purple_linter.py` | v1.1.0 | UV_PURPLE dominance lint + GLITCH_DARK_SCENE subtype |
| `LTG_TOOL_precritique_qa.py` | v2.16.1 | Pre-critique QA runner (11 sections) |
| `LTG_TOOL_glow_profile_extract.py` | v2.0.0 | CRT glow Gaussian fitting (isotropic + anisotropic) |
| `LTG_TOOL_scanline_pitch_extract.py` | v1.0.0 | Autocorrelation scanline pitch detection |
| `LTG_TOOL_fill_light_adapter.py` | v1.1.0 | Scene fill-light presets (JSON registry) |
| `LTG_TOOL_alpha_blend_lint.py` | v1.0.0 | Differential alpha blend lint (composited vs unlit) |
| `LTG_TOOL_proportion_audit.py` | — | SF eye-width/head-radius ratio audit |

## pycairo / Rendering Specs
- **Engine decision:** pycairo for characters, PIL for backgrounds, PIL for compositing
- Cairo path model: move_to, curve_to, fill_preserve + stroke (no redraw needed)
- `draw_tapered_stroke()`: perpendicular offsets along resampled path -> filled polygon, round caps via arcs
- `draw_wobble_path()`: sine noise + random jitter on bezier control points, seeded RNG
- PIL interop: numpy byte reorder BGRA->RGB from cairo ARGB32, ~0.44ms for 640x640
- Byte oval wobble: amplitude=0.8, freq=0.12, seed per expression name
- Glitch diamond: draw_smooth_polygon bulge_frac=0.06 (not 0.12 default — too rounded)
- Cairo clipping (ctx.clip()) for shadow/highlight on oval body — clip to ellipse, fill rect
- BACK view convention: use shadow color as primary fill (BYTE_SH / CORRUPT_AMB_SH)
- Three-tier line weight: anchor=3.5, structure=2.0, detail=1.0

## Modular Renderer Pattern (C53)
- Interface: `draw_<char>(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- Return FORMAT_ARGB32 transparent surface, character centered with margin
- Scene lighting: clip to body shape, apply tint as alpha overlay (max 0.4 intensity)
- Facing flip: negate tilt, swap L/R arm offsets, flip eye positions
- Surface sizing: body_size * 3 wide, * 2.8 tall + margins for arms/antenna/particles
- Convenience wrapper: `draw_<char>_to_pil()` for PIL pipeline integration
- Expression specs as dict table, not function args — single source of truth

## Key Pitfalls / Gotchas
- **PIL draw context:** After `variable_stroke()`, `add_rim_light()`, `add_face_lighting()`: ALWAYS refresh draw context
- **add_rim_light char_cx:** MUST pass char_cx for any left-of-center character — without it right-side rim cut at 0.50W
- **Eye width canonical:** `ew = int(head_r * 0.22)` where head_r = RADIUS not height/diameter
- **get_char_bbox():** spans ALL chars in frame — useless for single-char rim. Use known geometry when multi-char.
- **cv2 LAB format:** 8-bit scaled. ALWAYS unscale: `L*100/255; a-128; b-128` before ΔE/chroma/hue math
- **VOID_BLACK threshold:** use max(R,G,B) < 30 (max-channel), not per-channel
- **Chroma guard (C* >= 8):** mandatory on hue-angle checks — near-zero chroma gives unstable hue angles
- **ΔE vs hue-angle:** ΔE includes L* — dark variant of a hue has huge ΔE from mid-tone. Hue-angle matching captures family identity independent of lightness.
- **LANCZOS hue drift:** 1920x1080 draw + LANCZOS thumbnail -> blended pixels shift LAB hue. Fix: native 1280x720 canvas.
- **Alpha overlays of canonical colors:** alpha <= ~20 keeps composited pixels outside radius-60 sample zone
- **lerp gradients:** end at _MID/_DARK variants, not canonical color (avoids near-canonical blended pixels)
- **JSON:** no `+0.8` positive floats — only `-0.8` and `0.8`
- **glitch_spec_lint G004:** DOTALL regex spans all lines. Place draw_glitch_body() BEFORE all other draw.line() functions.
- **G008 bilateral:** code-level constant `BILATERAL_EYES = True` — comments get stripped
- **CRT glow asymmetry:** 0.70 below-midpoint intensity. Draw dimmed ellipse, overdraw upper half with per-scanline spans.
- **Anisotropic glow fitting:** data-hungry — most refs don't have clean axis-aligned falloff. Isotropic sigma_frac=0.1165 is stable and confirmed.

## Canonical Palette
| Color | Hex | RGB | GL code |
|---|---|---|---|
| CORRUPT_AMBER | #FF8C00 | (255,140,0) | GL-07 |
| BYTE_TEAL | #00D4E8 | (0,212,232) | GL-01b |
| UV_PURPLE | #7B2FBE | (123,47,190) | GL-04 |
| HOT_MAGENTA | #FF2D6B | (255,45,107) | GL-06 |
| ELECTRIC_CYAN | #00F0FF | (0,240,255) | GL-01a |
| SUNLIT_AMBER | #D4923A | (212,146,58) | RW-03 |

## Key Calibration Values
- CRT glow: sigma_frac=0.1165, fwhm_frac=0.2744, amplitude=49.4, baseline=4.1
- Scanline pitch (phosphor closeups): mean 25.8px, darkness ratio 0.502, recommended spacing=26
- UV_PURPLE hue family: h deg 255-325, C* >= 8. Canonical h deg ~306 deg. UV_PURPLE_DARK GL-04a (58,16,96) h deg ~271.5 deg
- CRT glow asymmetry: below_mult=0.70

## RETIRED (C26)
All stylization post-process scripts in `output/tools/legacy/`. Do NOT reference/fix/regenerate.

## Joined
Cycle 23 (2026-03-29)
