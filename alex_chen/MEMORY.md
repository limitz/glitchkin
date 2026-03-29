# Alex Chen — Memory

## Cycle 1 Lessons
- No images = no package. Push for visual approximations even in text workflows.
- Secondary characters need design. Antagonists need design early.
- FX must be specified. Protect escalation arcs.

## Cycle 2 Lessons
- Confetti density scale: 5 levels (0–4). Pilot caps at Level 2/brief Level 3.
- The Corruption: system failure, right-angle motion, three tells. Stage 3: Byte Cyan vs Corruption Magenta.

## Cycle 3 Lessons
- Pipeline: OpenToonz + Krita + Natron (open source only).
- Naming: LTG_[CAT]_descriptor_v###.ext. Bit depth: 16-bit production.
- Byte float physics: sinusoidal, 24-frame cycle, 4-frame overshoot.
- Continuity Supervisor role defined.

## Cycle 4 Lessons
- OPEN SOURCE ONLY. Blend modes = Natron terminology.
- Tools index at output/tools/README.md — register all scripts.
- If a tool is missing, build it in Python.

## Cycle 5 Lessons
- **Byte body fill = #00D4E8 (Byte Teal)**; highlights = #00F0FF (Electric Cyan). This is intentional — shared visual DNA with Luma's pixel accents (#00F0FF). Distinction preserves figure-ground legibility.
- Byte Teal added as GL-01b in master_palette.md. Byte color model updated. Style guide "Shared Visual DNA" section added.
- Corrupted Amber (#FF8C00) 2px outline rule on Byte in cyan-dominant environments — already in palette, now cross-referenced.

## Cycle 6 Lessons
- **One fully rendered style frame produced:** `output/tools/style_frame_01_rendered.py` → `output/color/style_frames/style_frame_01_rendered.png`.
- **Three-light setup in code:** warm gold lamp (left/RGB glow), cyan monitor wall (right/filled gradient), lavender ambient (composite overlay). All named from master_palette.md.
- **draw_amber_outline()** must use ellipse offsets (not rectangles) — implemented correctly.
- **Luma face in a scene:** draw functions from luma_face_generator.py work when adapted with a scale parameter; eyes must shift pupils toward the subject of gaze (Byte = rightward).
- **Body construction for scene:** torso split warm/cyan-lit down vertical center; reaching arm uses CYAN_SKIN; lamp-facing left edge gets Soft Gold rim line.
- **Byte body = BYTE_TEAL (#00D4E8), not ELEC_CYAN (#00F0FF).** Emergence zone must be near-void dark so Byte pops.
- **Vignette + lavender ambient overlay:** use Image.composite() with an L-mode alpha mask to simulate ambient tint without RGBA mode complexity.
- **Victoria's mandate ACHIEVED:** characters are recognizable; emotional premise (girl discovering something impossible) legible without text; lighting tension (warm left / cold right) visible.
- **Cycle 7 remaining gaps:** Luma full-body turnaround, Miri redesign (flatter head), Cosmo silhouette feet/glasses, Glitch Layer orientation, Millbrook sky color.

## Cycle 8 Lessons
- **Lighting overlay alphas must be visible:** Warm zone alpha raised 28→70 (~27%); cold zone 22→60. Below 15% alpha overlays are invisible in rendered output.
- **Amber outline width = 3px** at 1920×1080. GL-07 standard. Never 4 or 5.
- **Hoodie underside = cool ambient** (SHADOW_PLUM). Away from all light sources — three-light logic demands cool lavender ambient, not warm.
- **Shoe spec:** SHOE_CANVAS=(250,240,220) cream main; SHOE_SOLE=DEEP_COCOA=(59,40,32). Previous code had these inverted.
- **Tendril cp1 must point TOWARD target:** cp1x = start + (target-start)*0.33, not start - offset. The tendril must arc toward Luma, not away.
- **Byte underbody glow:** draw_filled_glow() at bottom quarter of Byte, glow_rgb=ELEC_CYAN, to simulate CRT screen illuminating from below.
- **Charged gap:** Add draw_filled_glow() + pixel scatter at midpoint between tendril tip and Luma's hand. This space is the emotional center.
- **Lamp floor pool:** draw_filled_glow() at (lamp_x+32, H*0.85), rx=120, ry=44, LAMP_PEAK. Required for lamp spatial presence on floor.
- **Cycle 9 remaining gaps:** Luma full-body turnaround, Miri redesign (flatter head + design language), Cosmo silhouette feet/glasses, Glitch Layer orientation, Millbrook sky color, couch size (too large — 40% of frame width).

## Cycle 7 Lessons
- **All 11 critic bugs fixed in style_frame_01_rendered.py:**
  1. `draw_lighting_overlay()` implemented — warm gold RGBA pool (left), cold cyan RGBA wash (right), composited by zone.
  2. Flat DUSTY_LAVENDER full-frame overlay removed — it was collapsing the warm/cold split.
  3. Luma `luma_cx` moved from 19% → 29% — arm span now ~21% of canvas (was ~40%).
  4. Neck polygon added connecting torso_top to head base — no more floating head.
  5. Torso seam fixed — row-by-row warm/cool gradient blend (no hard center seam).
  6. Vignette revised — darkens top/bottom bands only (not all 4 corners).
  7. Blush fixed — RGBA layer composite at 80/255 alpha, no skin cover ellipses.
  8. Monitor screens: `BYTE_TEAL` → `ELEC_CYAN` (GL-01, not GL-01b).
  9. Byte submerge fade: interpolation target changed from ELEC_CYAN → `(14,14,30)` (actual void pocket color).
  10. All inline color tuples named as constants (JEANS, JEANS_SH, COUCH_*, BLUSH_*, LAMP_PEAK).
  11. Body lean: `lean_offset=28px` applied row-by-row to torso top, arm shoulder, and neck.
- **RGBA composite technique:** use `Image.new("RGBA")` + `ImageDraw.Draw()` + `Image.alpha_composite()` for any additive overlay; then `.convert("RGB")` and `.paste()` back.
- **Luma position in generate():** luma_cx = int(W * 0.29). Arm target = scr_x0 - 20.
- **draw_luma_body() now returns:** `head_cx`, `head_cy`, `hand_cx`, `hand_cy`.
- **LAMP_PEAK = (245,200,66):** intentionally slightly warmer than SOFT_GOLD — peak emission is hotter. Documented inline.
- **Couch colors:** COUCH_BODY=(107,48,24), COUCH_BACK=(128,60,28), COUCH_ARM=(115,52,26) — candidates for DRW-06 in master_palette.md. Coordinate with Sam.
- **Cycle 8 remaining gaps:** Luma full-body turnaround, Miri redesign, Cosmo silhouette feet/glasses, Glitch Layer orientation, Millbrook sky color. Also: palette compliance for JEANS/SKIN/COUCH entries.
