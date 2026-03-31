# Maya Santos — Memory

## Cycle 53 — Modular Character Renderers (COMPLETE)

### Task 1 (P0): LTG_TOOL_char_luma.py v1.0.0 — DONE
- Canonical Luma renderer extracted from LTG_TOOL_luma_cairo_expressions.py
- Public API: `draw_luma(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- Also: `draw_luma_on_context(ctx, cx, ground_y, char_h, expression, pose)` for sheet/scene use
- All 6 expressions: CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED
- All gesture specs preserved (Lee C50 offset chain, amplified 40-60%)
- Self-test: all 6 render clean at 640x480
- Gesture lint: main char panels PASS (17.06px CURIOUS, etc.)
- Face gate: 3 PASS, 1 WARN, 2 FAIL (baseline expected)

### Task 2 (P1): LTG_TOOL_char_miri.py v1.0.0 — DONE
- Full pycairo rebuild of Miri (was PIL-only in grandma_miri_expression_sheet.py)
- Public API: `draw_miri(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- Also: `draw_miri_on_context(ctx, cx, ground_y, char_h, expression, pose)`
- 6 expressions: WARM, SKEPTICAL, CONCERNED, SURPRISED, WISE, KNOWING
- Lee C52 gesture spec fully implemented:
  - Permanent forward lean (MIRI_BASE_LEAN = -4 degrees)
  - Habitual left-hip weight
  - Hands-never-idle (towel, chin eval, chest touch, palm up, etc.)
  - Cardigan physics (longer hem on dropped-shoulder side)
  - Elder posture (shoulder drop + inward, rounded torso)
  - Wooden hairpins, permanent blush (0.0 for CONCERNED), round glasses
- Self-test: all 6 render clean at 608x456
- Gesture lint: main char panel PASS (9.01px WARM)
- Face gate: 2 PASS, 2 WARN, 2 FAIL (WARNs = KNOWING STILLNESS + WELCOMING, subtle at sprint)

### Interface Contract (matches Morgan's planned char_interface.py)
- `draw_X(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface`
- ARGB32 transparent background
- `draw_X_on_context(ctx, cx, ground_y, char_h, expression, pose)` for direct context use
- `cairo_surface_to_pil(surface)` utility exported

## Tools Owned
- LTG_TOOL_char_luma.py v1.0.0 (NEW C53)
- LTG_TOOL_char_miri.py v1.0.0 (NEW C53)
- LTG_TOOL_luma_cairo_expressions.py v2.0.0 (C52, superseded by char_luma for imports)
- (full list in SKILLS.md)

## Next Cycle Priorities
- Cosmo expression rebuild NOT STARTED — Sam has Cosmo modular (check if done)
- Migrate expression sheet generators to import from char_luma.py / char_miri.py
- LTG_TOOL_luma_cairo_expressions.py should be updated to import from char_luma.py
