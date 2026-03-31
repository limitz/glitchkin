# Maya Santos — Skills

## Role & Skills
- Character artist and QA tool builder for Luma & the Glitchkin
- PIL/pycairo rendering, expression sheets, turnarounds, color models, silhouette QA
- Engines: pycairo (primary for new work, bezier curves, LANCZOS downscale from 2x), PIL (legacy tools)
- Libraries authorized: numpy, OpenCV (BGR→RGB on load!), PyTorch, Pillow (canonical I/O)

## Tools Owned
| Tool | File | Version | Notes |
|---|---|---|---|
| **Luma canonical renderer** | `LTG_TOOL_char_luma.py` | v1.1.0 | Modular `draw_luma()`, 7 expressions, pose_mode (front/3q/side/back), unified arm silhouette, leg-torso connectivity fix |
| **Miri canonical renderer** | `LTG_TOOL_char_miri.py` | v1.0.0 | Modular `draw_miri()`, pycairo rebuild, 6 expressions |
| Luma cairo expressions | `LTG_TOOL_luma_cairo_expressions.py` | v2.0.0 | 6-expression sheet, pycairo engine (superseded by char_luma) |
| Luma expression sheet (legacy PIL) | `LTG_TOOL_luma_expression_sheet.py` | v014 | Superseded by cairo for Luma |
| Cosmo expression sheet | `LTG_TOOL_cosmo_expression_sheet.py` | v008 | Cowlick + tape + shoulders |
| Cosmo turnaround | `LTG_TOOL_cosmo_turnaround.py` | v003 | Cowlick + tape all views |
| Miri expression sheet | `LTG_TOOL_grandma_miri_expression_sheet.py` | v008 | Elder posture |
| Miri turnaround | `LTG_TOOL_miri_turnaround.py` | v001 | |
| Byte expression sheet | `LTG_TOOL_byte_expression_sheet.py` | v007 | |
| Glitch expression sheet | `LTG_TOOL_glitch_expression_sheet.py` | v003 | 9 expressions incl. interior desire |
| Glitch body diagram | `LTG_TOOL_glitch_body_primitive_diagram_gen.py` | v001 | |
| Character lineup | `LTG_TOOL_character_lineup.py` | v011 | Two-tier staging, Cosmo visual hook |
| Luma turnaround | `LTG_TOOL_luma_turnaround.py` | v006 | 5 true views (front/3q/side/side-L/back), C54 |
| SF06 Miri-Luma handoff | `LTG_TOOL_sf_miri_luma_handoff.py` | C49 | Elder posture + shoulder displacement |
| Multi-char face gate | `LTG_TOOL_multi_char_face_gate.py` | v1.0.0 | Exports `run_multi_char_face_gate()` |
| Visual hook audit | `LTG_TOOL_visual_hook_audit.py` | v1.0.0 | |
| Silhouette tool | `LTG_TOOL_expression_silhouette.py` | v003 | RPD metric, `--viz-rpd`, `--output-zones` |
| Expression isolator | `LTG_TOOL_expression_isolator.py` | v001 | Single expr at 800x800 |
| Body hierarchy | `LTG_TOOL_bodypart_hierarchy.py` | v002 | `--panel N`, `--chain` |
| Face curve validator | `LTG_TOOL_face_curve_validator.py` | v001 | All 10 Luma expressions PASS |
| Char diff | `LTG_TOOL_char_diff.py` | v001 | Proportion drift detection |
| Luma color model | `LTG_TOOL_luma_color_model.py` | v002 | |
| Elderly proportion ref | `LTG_TOOL_elderly_proportion_reference.py` | v1.0.0 | |
| Luma turnaround | `LTG_TOOL_luma_turnaround.py` | v003 | |

## Character Specs

### Luma (3.2 heads)
- Head 37% of body, eyes 30% of head width, cloud hair 17 overlapping ellipses
- Bean torso (cubic bezier), tapered tube limbs, variable-width strokes
- Eye width canonical: `ew = head_r * 0.22` (HR=105→ew=23px at 1x)
- Right-eye lid drop asymmetry is Luma's signature (re_lid_drop=6 in NEUTRAL)
- Orange hoodie primary, A-line trapezoid shape, pixel accent on chest
- Mitten hands in all rough/reference poses

### Cosmo (4.0 heads)
- Cowlick 0.15 heads tall, glasses bridge tape TAPE_COL=(250,240,220)
- Glasses tilt per expression (7°-10° range, S003 spec max 7°±2°)

### Miri (3.2 heads)
- MIRI_HEAD_RATIO=3.2 explicit constant, 88% circular head
- Wooden hairpins (NOT chopsticks), color (92,58,32)
- Elder posture: ELDER_LEAN_DX ~5px, ELDER_SHOULDER_DROP=3px, ELDER_SHOULDER_INWARD=2px
- Permanent blush (0.0 for CONCERNED only), round glasses always on

### Byte
- Body = OVAL (ellipse), CANONICAL. Body fill = #00D4E8 BYTE_TEAL (GL-01b)
- Hover particles = 10x10px everywhere
- Pixel eye 3x3 grid; crack = void-black overlay LINE, not a pixel state
- STORM arms asymmetric (6,22); RESIGNED symmetric (14,14)

### Glitch
- Diamond body: rx=34, ry=38, ry>rx always
- Confetti: HOT_MAG/UV_PURPLE only (never cyan/acid)
- Right eye = destabilized bleed of left = corruption read
- Shadow facets: use CORRUPT_AMB_SH (not UV_PURPLE) on dark backgrounds

## Body Connectivity Pattern (C54)
- Legs must overlap torso bottom: `fl_top = (x, torso_bot_y - leg_w_top * 0.8)`
- Hip bridge fills junction: filled ellipse-ish shape spanning both leg tops, fill=PANTS
- Unified arm silhouette: combine upper+forearm bezier pts into one list, call `_draw_unified_arm()`
  — `_draw_unified_arm(ctx, upper + fore[1:], w_shoulder, w_wrist, fill, line_col, lw)`
  — The `[1:]` on fore avoids duplicate elbow point
  — Wrist cap: `ctx.arc(all_pts[-1], w_wrist, 0, pi)` rounds the end

## Key Pitfalls / Gotchas
- **squint_top_r**: Use BG overdraw + lid line, NOT r_open scaling (scales symmetrically = wince not squint). Pass `panel_bg` through render chain.
- **THE NOTICING gaze**: `gaze_dx=-0.5` in EXPR_SPECS is fallback only. Rightward gaze lives in `_FACE_CURVES_OVERRIDES` (LI/RI_CENTER_dx: +6). Do NOT remove either.
- **le_lid_drop / re_lid_drop**: Scalar values in pts_dict, added at RENDER TIME. Extract directly from `pts_dict["re_lid_drop"]`, not as P1 delta.
- **Silhouette RPD**: Column-projection dominated by trunk mass at small panel scale. Arms must extend far beyond body to register. Direction flipping (opposite lean) is most effective differentiator.
- **Arms-mode silhouette FAIL**: Known measurement limit for human chars — shared torso column dominates. Full-mode is the primary production metric.
- **6-expression sheets**: 15 pairs to check (vs 1 for 2-panel). Structurally harder to pass silhouette.
- **Shoulder involvement**: `_shoulder_dy()` = % of arm raise, capped. Torso gains 8 vertices (outer, deltoid_peak, inner x 2 sides + bottom corners).
- **Copyright headers**: ONLY on files inside `output/`. Nowhere else.
- **Image size rule**: All output PNGs <=1280px on longest side. Use PIL thumbnail with LANCZOS.
- **OpenCV**: Uses BGR by default — always `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` on load.
- **Dark BG shadow rule**: UV_PURPLE disappears on dark void. Use CORRUPT_AMB_SH instead.
- **Hierarchy tool false positives**: Uses Luma color index — non-Luma chars produce palette FAILs. Not real defects.
- **char_spec_lint pattern mismatch**: Looks for `LTG_TOOL_grandma_miri_expression_sheet_v*.py` but file has no version suffix — Kai should fix.

## Three-Tier Line Weight (2x render, canonical)
- Head outline: width=4 (~2px at 1x)
- Structure (torso, arms, legs, eye ovals, brows, mouth): width=3 (~1.5px)
- Detail (nose, laces, crinkles): width=2 (~1px)
- Hair strand arcs: width=3 (NOT 6). width=6 = manga/overworked.

## Modular Renderer Pattern (C53/C54)
- Canonical renderer per character: `LTG_TOOL_char_X.py`
- Public: `draw_X(expression, pose, scale, facing, scene_lighting, pose_mode) -> cairo.ImageSurface`
- Context: `draw_X_on_context(ctx, cx, ground_y, char_h, expression, pose)` for sheets/scenes
- All return ARGB32 transparent bg. `cairo_surface_to_pil()` for PIL conversion.
- GESTURE_SPECS dict per character: offset chain values from Lee's specs
- Miri: MIRI_BASE_LEAN = -4 adds to per-expression torso_lean. Never vertical.

## Pose Mode Architecture (C54)
- `pose_mode` param on `draw_luma()`: "side" | "front" | "threequarter" | "back"
- Each mode has its own render function: `_draw_luma_front`, `_draw_luma_threequarter`, `_draw_luma_back`
- "side" = existing `_draw_luma_on_context` (unchanged)
- Front: symmetric torso (sh_w=0.95 head_r), both eyes equal, no offset chain, nose = dot
- 3/4: near eye full, far eye foreshortened (rx=0.14 head_r), offset chain 50% of side
- Back: hair covers face area (extra blobs at y=0, y=0.2), no face, nape crease, back seam
- `facing="left"` flip only applies to "side" and "threequarter" modes

## Key Production Rules
- Full body in every expression panel (head to feet) — bust format insufficient for silhouette differentiation
- Every expression needs unique SILHOUETTE, not just unique face features
- Backward lean (positive body_tilt) = skeptical/avoidance; forward (negative) = engaged
- Corrugator kink (inner brow UP) = worry; V-brows = aggression
- Bilateral brow raise = surprised; asymmetric = skeptical
- Droopy lid needs parabolic sag curve on lower lid, not just reduced aperture
- Narrative stillness CAN be an expression (total lack of movement = silhouette statement)
