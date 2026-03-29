# Alex Chen — Memory

## Cycle 12 Lessons
- **Byte ground-floor annotation:** Added dashed `GROUNDFLOOR_COL=(100,168,200)` line at `BASELINE_Y` under Byte, with label "ground floor." and downward arrow. Dmitri P1 (3rd notice) closed. New output: `LTG_CHAR_lineup_v002.png`.
- **Cosmo side glasses refactor:** `_draw_cosmo_glasses()` extended with `is_side=True, front_x=` parameters. Side view now uses shared helper (inline code removed from `draw_cosmo_side()`). All four views now route through the same function. Output: `LTG_CHAR_cosmo_turnaround_v002.png`.
- **Ghost Byte visual surprise (A+ gap):** Faint oval Byte-ghost (alpha 55/255) composite on 3 peripheral monitors via RGBA layer. Implies Byte was watching from all screens before revealing itself — story beat hidden in art. Victoria Ashford A+ direction. Output: `LTG_COLOR_styleframe_discovery_v002.png`. Cycle label: "Ghost Byte".
- **Asymmetric logo:** `LTG_TOOL_logo_asymmetric_v001.py` produces `LTG_BRAND_logo_asymmetric_v001.png`. "Luma" at 180px (dominant left), "&" at 56px (bridge), "the Glitchkin" stacked at 72px (right). Bi-color scan bar below; larger pixel scatter on right as visual counterweight.
- **NEVER overwrite existing assets** — always new versioned files. Naming: `LTG_[CAT]_[descriptor]_v[###].png`.
- **Style frame draw order after RGBA composite:** Must refresh `draw = ImageDraw.Draw(img)` after any `img.paste()` call from compositing, or subsequent draws go to the old surface.

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
- **Hoodie underside = cool ambient** (SHADOW_PLUM, Cycle 8 interim). Away from all light sources — three-light logic demands cool lavender ambient, not warm.
- **Shoe spec:** SHOE_CANVAS=(250,240,220) cream main; SHOE_SOLE=DEEP_COCOA=(59,40,32). Previous code had these inverted.
- **Tendril cp1 must point TOWARD target:** cp1x = start + (target-start)*0.33, not start - offset. The tendril must arc toward Luma, not away.
- **Byte underbody glow:** draw_filled_glow() at bottom quarter of Byte, glow_rgb=ELEC_CYAN, to simulate CRT screen illuminating from below.
- **Charged gap:** Add draw_filled_glow() + pixel scatter at midpoint between tendril tip and Luma's hand. This space is the emotional center.
- **Lamp floor pool:** draw_filled_glow() at (lamp_x+32, H*0.85), rx=120, ry=44, LAMP_PEAK. Required for lamp spatial presence on floor.

## Cycle 11 Lessons
- **Mid-air transition element:** pixel confetti in x=768–960, y=200–700 (lamp–monitor boundary). Left of zone midpoint x=864: SOFT_GOLD/SUNLIT_AMBER/LAMP_PEAK/WARM_CREAM (warm-lit). Right of x=864: ELEC_CYAN/BYTE_TEAL/DEEP_CYAN/STATIC_WHITE (cold-lit). Seeded rng=77, 60 particles. Closes Victoria P1 (2 cycles).
- **Screen pixel figures minimum size = 15px wide.** Full 3-tier structure: head 5×4 + body 9×5 + legs 3×5 each. 7px was sub-legible. Rule: no pixel figures narrower than 14px on 1920px canvas.
- **Logo tagline removed.** "A cartoon series by the Dream Team" deleted from logo_generator.py STEP 11. Show title only on title card. No tagline before pitch.
- **byte.md version header:** Line 6 must always match colophon. v3.1 header now correctly states "3.1". Rule: whenever colophon is updated, update line 6 header on same edit.
- **Style guide sections 9/10/11 added:** Animation Style Notes (movement timing, Byte bob=24f, Luma lean rule, glitch effects instant), Glitchkin Construction Rules (pixel body, no fixed shape, corruption marks mandatory, always <Byte size), Prop Design Guidelines (warm material logic, retro-computing, cables always present, Glitch Layer = pure geometry, transition objects = clean-edge boundary).

## Cycle 10 Lessons
- **byte.md v3.1 complete.** All cube/chamfer/notch references purged from Sections 5, 6, 8, 10, 11, 12, size comparison, rationale. Section 10 (Turnaround) fully rewritten for oval — all five views describe oval arcs, ellipsoid depth, oval silhouettes. Quick Reference table updated. Document is now internally consistent.
- **Show logo exists:** `output/tools/logo_generator.py` → `output/production/show_logo.png`. "Luma" = SUNLIT_AMBER (#D4923A), "&" = WARM_CREAM neutral, "the Glitchkin" = ELEC_CYAN with pixel corruption. Dark void background with warm/cold zone glows and pixel border accents.
- **Luma lean = 48px** (was 28px). 48px at 170px torso = ~16°. Victoria's mandate: active urgency, not passive TV-watching. Rule: lean_offset must be ≥40px for any emotionally active Luma pose.
- **Screen content rule:** CRT screens must have pictorial content implying Byte's world — receding grid lines and pixel figure silhouettes establish origin. A blank cyan screen is "generic." Content is drawn in screen margins around the emergence void (which stays as dark void pocket). Draw order: screen background → grid → pixel figures → emergence void → glow rings.
- **byte.md DO NOT list — oval-specific rule:** Do not make the oval too smooth/round; keep glitch details (scar, cracked eye frame, pixel confetti) as angular/sharp to counterbalance the soft body shape.

## Cycle 9 Lessons
- **HOODIE_AMBIENT = #B06040** (RGB 176,96,64) = CHAR-L-08 finalized. Derivation: HOODIE_SHADOW (#B84A20) blended 70% with DUSTY_LAVENDER (#A89BBF) at 30%. Replaces SHADOW_PLUM permanently. Must retain orange component — pure cool shadow reads as separate material.
- **Couch scale corrected:** couch_left = W*0.16 (was W*0.04), couch_right = W*0.38 (was W*0.44). Span ~422px (~22%), ratio ~4.8:1 vs Luma's 88px. Target is 4:1. This was 4 cycles overdue — never defer couch/prop scale again.
- **Submerge/glow draw order:** Submerge fade must be drawn BEFORE screen-glow. If submerge paints near-black AFTER the glow, the glow is invisible. Rule: establish dark field first, then paint light on top.
- **Overlay draw order:** Atmospheric overlay must be applied BEFORE characters, not after. Characters have baked-in three-light values; applying the overlay on top double-tints warm hoodie (+yellow) and cyan arm (+wash). Fixed: overlay at STEP 3, characters at STEP 4+.
- **False comments propagate:** The "arm span ~21%" comment was false from Cycle 7 and carried forward unchanged. Always verify comment claims match computed geometry.
- **Byte body = OVAL (canonical from Cycle 8).** byte.md updated to Version 3.0; chamfered-box design retired. Any new artist should draw oval, not cube.
- **MIRI-A locked** as canonical Grandma Miri design (bun+chopsticks+cardigan+soldering iron). MIRI-B archived. Maya notified.
- **Cycle 10 remaining gaps:** Luma full-body turnaround, Cosmo silhouette feet/glasses, Glitch Layer background, composite reference image (all 4 characters at scale — Dmitri P0 now 5 cycles overdue), Millbrook sky color, naming convention reconciliation pass.

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
