========================================================================
LTG CI Suite v1.4.0 — Combined Report
Tools dir : /home/wipkat/team/output/tools
Fail-on   : FAIL
========================================================================
  ✓ [PASS ] Stub Integrity Linter
          141 file(s) — 0 PASS / 0 WARN / 0 ERROR
  ⚠ [WARN ] Draw Order Linter
          136 file(s) — 96 PASS / 40 WARN / 0 ERROR  [58 KNOWN]
  ⚠ [WARN ] Glitch Spec Linter
          20 Glitch generator(s) — 7 PASS / 13 WARN
  ✓ [PASS ] Spec Sync CI Gate
          5 character(s) — 0 P1 FAIL: none / 0 WARN: none
  ✓ [PASS ] Char Spec Linter
          3 character(s) — 0 PASS / 0 WARN / 0 FAIL
  ✗ [FAIL ] Dual-Output File Check
          30 output filename conflict(s) — 76 generator(s) involved
  ✗ [FAIL ] Hardcoded Path Check
          168 hardcoded /home/ occurrence(s) in 81 file(s): 33 NEW (FAIL) + 48 KNOWN (migration backlog)
  ✗ [FAIL ] Thumbnail Lint
          66 unwhitelisted .thumbnail() call(s) in 61 generator(s) — native canvas required
  ⚠ [WARN ] Motion Sheet Coverage
          1 character(s) missing motion sheet: grandma_miri

  ✗ OVERALL: FAIL  (exit code 1)  (58 KNOWN issues annotated)
    NOTE: KNOWN issues are pre-existing/expected — annotated for visibility only.
    They do not suppress the overall grade. Remove entries from ci_known_issues.json
    once the underlying issue is fixed.

  ⚠ STALE_KNOWN: 46 suppression(s) are aged and need review
    These entries have been in ci_known_issues.json for a long time.
    Review each: confirm the underlying issue is still a genuine FP,
    then either extend the reason note or remove the entry if the issue is fixed.
      [draw_order_lint] LTG_TOOL_act2_panels_cycle14.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(img_rgba.convert('RGB')) in composite helper — no draw calls 
      [draw_order_lint] LTG_TOOL_bg_classroom.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: Image.alpha_composite() lighting overlay passes — final composites, no 
      [draw_order_lint] LTG_TOOL_bg_millbrook_main_street.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(...)) — final overlay pass, no draw cal
      [draw_order_lint] LTG_TOOL_bg_school_hallway.py code=W002  since=C39  age=6 cycle(s)
        reason: Pattern: draw.rectangle(fill=..., outline=...) — PIL draws fill+outline in one c
      [draw_order_lint] LTG_TOOL_bg_tech_den.py code=W002  since=C39  age=6 cycle(s)
        reason: Pattern: draw.rectangle(fill=..., outline=...) — PIL draws fill+outline in one c
      [draw_order_lint] LTG_TOOL_bodypart_hierarchy.py code=W002  since=C39  age=6 cycle(s)
        reason: Annotation/diagnostic overlay rectangles — draw.rectangle with outline only (no 
      [draw_order_lint] LTG_TOOL_logo_asymmetric.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(base_rgba.convert('RGB')) — per-glyph composite in gradient l
      [draw_order_lint] LTG_TOOL_luma_motion.py code=W001  since=C39  age=6 cycle(s)
        reason: Annotation text draw in motion spec sheet panel header — text label, not actual 
      [draw_order_lint] LTG_TOOL_procedural_draw.py code=W004  since=C39  age=6 cycle(s)
        reason: Library utility functions use img.paste() for compositing; callers rebuild draw 
      [draw_order_lint] LTG_TOOL_sb_a2_cycle15.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_act1_contact_sheet.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(thumb, ...) — thumbnail composite, no draw calls follow. C39 
      [draw_order_lint] LTG_TOOL_sb_panel_a101.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a102.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a103.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a104_kitchen.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a201.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a202.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a204.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a205.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a206_insert.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a207.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a207b.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_panel_a208.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_sb_pilot_cold_open.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste(Image.alpha_composite(base, glow).convert('RGB')) — glow pass
      [draw_order_lint] LTG_TOOL_styleframe_discovery.py code=W004  since=C39  age=6 cycle(s)
        reason: Pattern: img.paste() on split-composite — ghost overlay and side composites, no 
      [glitch_spec_lint] LTG_CHAR_byte_motion.py code=G003  since=C39  age=6 cycle(s)
        reason: Byte motion sheet is not a Glitch expression sheet — multi-expression check does
      [glitch_spec_lint] LTG_CHAR_byte_motion.py code=G005  since=C39  age=6 cycle(s)
        reason: Byte motion sheet has no Glitch body polygon — UV_PURPLE shadow check does not a
      [glitch_spec_lint] LTG_CHAR_byte_motion.py code=G007  since=C39  age=6 cycle(s)
        reason: Byte motion sheet has no Glitch body polygon — VOID_BLACK outline check does not
      [glitch_spec_lint] LTG_TOOL_bg_glitch_storm_colorfix.py code=G005  since=C39  age=6 cycle(s)
        reason: Background-only ENV generator; contains CORRUPT_AMBER storm confetti color but n
      [glitch_spec_lint] LTG_TOOL_bg_glitch_storm_colorfix.py code=G007  since=C39  age=6 cycle(s)
        reason: Background-only ENV generator; contains CORRUPT_AMBER storm confetti color but n
      [glitch_spec_lint] LTG_TOOL_bg_other_side.py code=G007  since=C39  age=6 cycle(s)
        reason: Background-only ENV generator; contains GL color constants but no Glitch charact
      [glitch_spec_lint] LTG_TOOL_byte_motion.py code=G003  since=C39  age=6 cycle(s)
        reason: Byte motion sheet (LTG_TOOL_ canonical); not a Glitch expression sheet. C39 base
      [glitch_spec_lint] LTG_TOOL_byte_motion.py code=G005  since=C39  age=6 cycle(s)
        reason: Byte motion sheet; no Glitch body polygon. C39 baseline FP.
      [glitch_spec_lint] LTG_TOOL_byte_motion.py code=G007  since=C39  age=6 cycle(s)
        reason: Byte motion sheet; no Glitch body polygon. C39 baseline FP.
      [glitch_spec_lint] LTG_TOOL_character_face_test.py code=G003  since=C39  age=6 cycle(s)
        reason: Face-lighting test utility; not a Glitch generator. C39 baseline FP.
      [glitch_spec_lint] LTG_TOOL_character_face_test.py code=G005  since=C39  age=6 cycle(s)
        reason: Face-lighting test utility; no Glitch body polygon. C39 baseline FP.
      [glitch_spec_lint] LTG_TOOL_character_face_test.py code=G006  since=C39  age=6 cycle(s)
        reason: Face-lighting test utility; skin tone color tuples in test fixture trigger organ
      [glitch_spec_lint] LTG_TOOL_character_face_test.py code=G007  since=C39  age=6 cycle(s)
        reason: Face-lighting test utility; no Glitch body polygon. C39 baseline FP.
      [glitch_spec_lint] LTG_TOOL_color_verify.py code=G005  since=C39  age=6 cycle(s)
        reason: Color verification utility; contains palette color tuples that trigger G005 nume
      [glitch_spec_lint] LTG_TOOL_color_verify.py code=G007  since=C39  age=6 cycle(s)
        reason: Color verification utility; contains VOID_BLACK constant but no draw.polygon cal
      [glitch_spec_lint] LTG_TOOL_fidelity_check_c24.py code=G005  since=C39  age=6 cycle(s)
        reason: Fidelity check utility; palette color tuples trigger G005. C39 baseline FP.
      [glitch_spec_lint] LTG_TOOL_fidelity_check_c24.py code=G007  since=C39  age=6 cycle(s)
        reason: Fidelity check utility; VOID_BLACK constant but no draw.polygon. C39 baseline FP
      [glitch_spec_lint] LTG_TOOL_glitch_color_model.py code=G006  since=C39  age=6 cycle(s)
        reason: Color model swatch sheet; SOFT_GOLD swatch (200,160,80) triggers organic-fill ch
      [glitch_spec_lint] LTG_TOOL_glitch_turnaround.py code=G007  since=C39  age=6 cycle(s)
        reason: Turnaround uses draw.polygon with outline color variable (not literal VOID_BLACK
      [glitch_spec_lint] LTG_TOOL_style_frame_02_glitch_storm.py code=G007  since=C39  age=6 cycle(s)
        reason: SF02 uses Glitch body polygon via procedural_draw lib — direct draw.polygon call
      [glitch_spec_lint] LTG_TOOL_style_frame_03_other_side.py code=G007  since=C39  age=6 cycle(s)
        reason: SF03 uses Glitch body polygon via procedural_draw lib — direct draw.polygon call
========================================================================

────────────────────────────────────────────────────────────────────────
Detail: Stub Integrity Linter
────────────────────────────────────────────────────────────────────────
======================================================================
LTG Stub Integrity Linter — Report
Files scanned: 141
  PASS : 141
  WARN : 0
  ERROR: 0
======================================================================

======================================================================
All scanned files pass stub integrity check.
======================================================================

────────────────────────────────────────────────────────────────────────
Detail: Draw Order Linter
────────────────────────────────────────────────────────────────────────
WARN   LTG_TOOL_act2_panels_cycle14.py  (3 warning(s))
         [W004] line 201: img.paste() at line 201 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_rgba.convert('RGB'))  [KNOWN]
         [W004] line 1090: img.paste() at line 1090 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_rgba.convert('RGB'))  [KNOWN]
         [W004] line 1175: img.paste() at line 1175 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_rgba.convert('RGB'))  [KNOWN]
PASS   LTG_TOOL_alpha_blend_lint.py
WARN   LTG_TOOL_bg_classroom.py  (2 warning(s))
         [W004] line 161: img.paste() at line 161 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(layer.crop((x0, y0, x1, y1)), (x0, y0))  [KNOWN]
         [W004] line 174: img.paste() at line 174 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(layer.crop((x0, y0, x1 + 1, y1 + 1)), (x0, y0))  [KNOWN]
PASS   LTG_TOOL_bg_glitch_layer_encounter.py
PASS   LTG_TOOL_bg_glitch_layer_frame.py
PASS   LTG_TOOL_bg_glitch_storm_colorfix.py
PASS   LTG_TOOL_bg_glitchlayer_frame.py
PASS   LTG_TOOL_bg_grandma_kitchen.py
PASS   LTG_TOOL_bg_luma_study_interior.py
WARN   LTG_TOOL_bg_millbrook_main_street.py  (1 warning(s))
         [W004] line 482: img.paste() at line 482 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"),  [KNOWN]
PASS   LTG_TOOL_bg_other_side.py
WARN   LTG_TOOL_bg_school_hallway.py  (1 warning(s))
         [W002] line 190: OUTLINE draw call for 'generic' at line 190 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)  [KNOWN]
WARN   LTG_TOOL_bg_tech_den.py  (1 warning(s))
         [W002] line 180: OUTLINE draw call for 'generic' at line 180 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)  [KNOWN]
WARN   LTG_TOOL_bodypart_hierarchy.py  (2 warning(s))
         [W002] line 462: OUTLINE draw call for 'generic' at line 462 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([hx0, hy0, hx1, hy1], outline=(0, 200, 60), width=2)  [KNOWN]
         [W002] line 486: OUTLINE draw call for 'generic' at line 486 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([lx, ly, lx + 10, ly + 10], fill=col, outline=(0, 0, 0), width=1)  [KNOWN]
PASS   LTG_TOOL_byte_color_model.py
PASS   LTG_TOOL_byte_commitment_rpd_test.py
PASS   LTG_TOOL_byte_cracked_eye_glyph.py
PASS   LTG_TOOL_byte_expression_sheet.py
PASS   LTG_TOOL_byte_motion.py
PASS   LTG_TOOL_char_diff.py
PASS   LTG_TOOL_char_spec_lint.py
PASS   LTG_TOOL_character_face_test.py
PASS   LTG_TOOL_character_lineup.py
PASS   LTG_TOOL_ci_suite.py
PASS   LTG_TOOL_color_qa_c37_runner.py
PASS   LTG_TOOL_color_verify.py
PASS   LTG_TOOL_colorkey_glitch_covetous_gen.py
PASS   LTG_TOOL_colorkey_glitchstorm_gen.py
PASS   LTG_TOOL_colorkey_otherside_gen.py
PASS   LTG_TOOL_contact_sheet_arc_diff.py
PASS   LTG_TOOL_cosmo_color_model.py
PASS   LTG_TOOL_cosmo_expression_sheet.py
WARN   LTG_TOOL_cosmo_motion.py  (1 warning(s))
         [W001] line 439: HEAD/FACE draw call at line 439 appears before BODY draw call at line 523. Body must be painted before head.  >> draw.text((px + 8, timing_y + 25), "Head settle:   beat 2", fill=BEAT_COLOR)  [KNOWN]
PASS   LTG_TOOL_cosmo_turnaround.py
PASS   LTG_TOOL_costume_bg_clash.py
PASS   LTG_TOOL_cycle13_panel_fixes.py
PASS   LTG_TOOL_draw_order_lint.py
PASS   LTG_TOOL_env_grandma_living_room.py
PASS   LTG_TOOL_expression_isolator.py
PASS   LTG_TOOL_expression_silhouette.py
PASS   LTG_TOOL_face_curve_validator.py
PASS   LTG_TOOL_face_curves_caller_audit.py
PASS   LTG_TOOL_fidelity_check_c24.py
PASS   LTG_TOOL_fill_light_adapter.py
PASS   LTG_TOOL_glitch_body_primitive_diagram_gen.py
PASS   LTG_TOOL_glitch_color_model.py
PASS   LTG_TOOL_glitch_expression_sheet.py
PASS   LTG_TOOL_glitch_motion.py
PASS   LTG_TOOL_glitch_spec_lint.py
PASS   LTG_TOOL_glitch_turnaround.py
PASS   LTG_TOOL_grandma_miri_color_model.py
PASS   LTG_TOOL_grandma_miri_expression_sheet.py
PASS   LTG_TOOL_lineup_palette_audit.py
PASS   LTG_TOOL_lineup_tier_depth_sketch.py
PASS   LTG_TOOL_logo.py
WARN   LTG_TOOL_logo_asymmetric.py  (8 warning(s))
         [W004] line 214: img.paste() at line 214 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))  [KNOWN]
         [W004] line 274: img.paste() at line 274 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))  [KNOWN]
         [W004] line 289: img.paste() at line 289 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))  [KNOWN]
         [W004] line 304: img.paste() at line 304 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))  [KNOWN]
         [W004] line 319: img.paste() at line 319 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))  [KNOWN]
         [W004] line 329: img.paste() at line 329 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))  [KNOWN]
         [W004] line 346: img.paste() at line 346 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))  [KNOWN]
         [W004] line 363: img.paste() at line 363 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))  [KNOWN]
PASS   LTG_TOOL_luma_act2_standing_pose.py
PASS   LTG_TOOL_luma_classroom_pose.py
PASS   LTG_TOOL_luma_cold_overlay_swatches.py
PASS   LTG_TOOL_luma_color_model.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_face_curves.py
WARN   LTG_TOOL_luma_motion.py  (1 warning(s))
         [W001] line 378: HEAD/FACE draw call at line 378 appears before BODY draw call at line 392. Body must be painted before head.  >> draw.text((hcx + hr + 22, hcy - 12), "+8° head tilt", fill=BEAT_COLOR)  [KNOWN]
PASS   LTG_TOOL_luma_turnaround.py
PASS   LTG_TOOL_miri_motion.py
PASS   LTG_TOOL_miri_turnaround.py
PASS   LTG_TOOL_motion_spec_lint.py
PASS   LTG_TOOL_naming_cleanup.py
PASS   LTG_TOOL_naming_compliance_copier.py
PASS   LTG_TOOL_naming_compliance_copy.py
PASS   LTG_TOOL_palette_warmth_lint.py
PASS   LTG_TOOL_pilot_cold_open.py
PASS   LTG_TOOL_pixel_font_v001.py
PASS   LTG_TOOL_precritique_qa.py
WARN   LTG_TOOL_procedural_draw.py  (4 warning(s))
         [W004] line 307: img.paste() at line 307 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(result)  [KNOWN]
         [W004] line 606: img.paste() at line 606 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert(img.mode))  [KNOWN]
         [W004] line 637: img.paste() at line 637 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert(img.mode))  [KNOWN]
         [W004] line 664: img.paste() at line 664 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert(img.mode))  [KNOWN]
PASS   LTG_TOOL_project_paths.py
PASS   LTG_TOOL_proportion_audit.py
PASS   LTG_TOOL_proportion_audit_c37_runner.py
PASS   LTG_TOOL_proportion_verify.py
PASS   LTG_TOOL_readme_sync.py
PASS   LTG_TOOL_render_lib.py
PASS   LTG_TOOL_render_qa.py
WARN   LTG_TOOL_sb_a2_cycle15.py  (1 warning(s))
         [W004] line 183: img.paste() at line 183 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_act1_contact_sheet.py  (1 warning(s))
         [W004] line 168: img.paste() at line 168 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(thumb, (thumb_x, thumb_y))  [KNOWN]
PASS   LTG_TOOL_sb_act1_full_contact_sheet.py
PASS   LTG_TOOL_sb_act2_contact_sheet.py
PASS   LTG_TOOL_sb_caption_retrofit.py
WARN   LTG_TOOL_sb_cold_open_P03.py  (1 warning(s))
         [W004] line 92: img.paste() at line 92 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P06.py  (1 warning(s))
         [W004] line 100: img.paste() at line 100 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P07.py  (2 warning(s))
         [W004] line 115: img.paste() at line 115 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
         [W004] line 194: img.paste() at line 194 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(img.convert('RGBA'), glass_overlay).convert('RGB  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P08.py  (1 warning(s))
         [W004] line 108: img.paste() at line 108 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P09.py  (1 warning(s))
         [W004] line 125: img.paste() at line 125 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P10.py  (1 warning(s))
         [W004] line 120: img.paste() at line 120 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P11.py  (1 warning(s))
         [W004] line 104: img.paste() at line 104 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P14.py  (2 warning(s))
         [W004] line 120: img.paste() at line 120 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
         [W004] line 192: img.paste() at line 192 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P15.py  (1 warning(s))
         [W004] line 116: img.paste() at line 116 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P23.py  (1 warning(s))
         [W004] line 102: img.paste() at line 102 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_cold_open_P24.py  (1 warning(s))
         [W004] line 100: img.paste() at line 100 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_ep05_covetous.py  (1 warning(s))
         [W004] line 112: img.paste() at line 112 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a101.py  (1 warning(s))
         [W004] line 91: img.paste() at line 91 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a102.py  (1 warning(s))
         [W004] line 94: img.paste() at line 94 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a103.py  (1 warning(s))
         [W004] line 110: img.paste() at line 110 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a104_kitchen.py  (1 warning(s))
         [W004] line 103: img.paste() at line 103 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a201.py  (1 warning(s))
         [W004] line 114: img.paste() at line 114 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a202.py  (1 warning(s))
         [W004] line 113: img.paste() at line 113 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
PASS   LTG_TOOL_sb_panel_a203.py
WARN   LTG_TOOL_sb_panel_a204.py  (1 warning(s))
         [W004] line 110: img.paste() at line 110 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a205.py  (1 warning(s))
         [W004] line 110: img.paste() at line 110 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a206_insert.py  (1 warning(s))
         [W004] line 106: img.paste() at line 106 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a207.py  (1 warning(s))
         [W004] line 128: img.paste() at line 128 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a207b.py  (1 warning(s))
         [W004] line 103: img.paste() at line 103 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_panel_a208.py  (1 warning(s))
         [W004] line 111: img.paste() at line 111 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
WARN   LTG_TOOL_sb_pilot_cold_open.py  (1 warning(s))
         [W004] line 150: img.paste() at line 150 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))  [KNOWN]
PASS   LTG_TOOL_sf02_fill_light_fix_c35.py
PASS   LTG_TOOL_sf04_luma_byte_v005.py
PASS   LTG_TOOL_sf_covetous_glitch.py
PASS   LTG_TOOL_sf_covetous_glitch_c43.py
PASS   LTG_TOOL_sf_miri_luma_handoff.py
PASS   LTG_TOOL_sheet_geometry_calibrate.py
PASS   LTG_TOOL_sight_line_diagnostic.py
PASS   LTG_TOOL_sobel_vp_detect.py
PASS   LTG_TOOL_spec_extractor.py
PASS   LTG_TOOL_spec_sync_ci.py
PASS   LTG_TOOL_stub_linter.py
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_03_other_side.py
WARN   LTG_TOOL_style_frame_04_resolution.py  (1 warning(s))
         [W004] line 182: img.paste() at line 182 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(CEIL_DARK, [0, 0, W, ceil_y])  [KNOWN]
PASS   LTG_TOOL_style_frame_05_relationship.py
WARN   LTG_TOOL_styleframe_discovery.py  (3 warning(s))
         [W004] line 255: img.paste() at line 255 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_with_ghost.convert("RGB"))  [KNOWN]
         [W004] line 923: img.paste() at line 923 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_left.convert("RGB"), (0, 0))  [KNOWN]
         [W004] line 939: img.paste() at line 939 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_right.convert("RGB"), (split_x, 0))  [KNOWN]
PASS   LTG_TOOL_styleframe_luma_byte.py
WARN   LTG_TOOL_thumbnail_preview_v001.py  (1 warning(s))
         [W002] line 67: OUTLINE draw call for 'generic' at line 67 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x1 + i, y1 + i, x2 - i, y2 - i], outline=color)  [KNOWN]
PASS   LTG_TOOL_uv_purple_linter.py
PASS   LTG_TOOL_vanishing_point_lint.py
PASS   LTG_TOOL_warmth_inject.py
PASS   LTG_TOOL_warmth_inject_hook.py
PASS   LTG_TOOL_world_type_infer.py

Summary: 136 file(s) — 96 PASS / 40 WARN / 0 ERROR

────────────────────────────────────────────────────────────────────────
Detail: Glitch Spec Linter
────────────────────────────────────────────────────────────────────────
======================================================================
LTG Glitch Spec Linter v1.4.0 — Report
Glitch generators found: 20
  PASS : 7
  WARN : 13
======================================================================

[WARN] LTG_CHAR_byte_motion.py
  - G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_bg_glitch_storm_colorfix.py
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_bg_other_side.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_byte_motion.py
  - G003: Multi-Glitchkin frame has only 0 unique expression(s) — at least 2 required. Found: none
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_character_face_test.py
  - G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - G006: Possible organic/warm fill detected — fill=(120, 120, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(120, 120, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_character_lineup.py
  - G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(168, 152, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 130, 90). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(140, 120, 100). Glitch body fill must use CORRUPT_AMBER family only (spec §10).

[WARN] LTG_TOOL_color_verify.py
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[PASS] LTG_TOOL_colorkey_glitch_covetous_gen.py
  All checks passed.

[WARN] LTG_TOOL_fidelity_check_c24.py
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[PASS] LTG_TOOL_glitch_body_primitive_diagram_gen.py
  All checks passed.

[WARN] LTG_TOOL_glitch_color_model.py
  - G006: Possible organic/warm fill detected — fill=(200, 160, 80). Glitch body fill must use CORRUPT_AMBER family only (spec §10).

[PASS] LTG_TOOL_glitch_expression_sheet.py
  All checks passed.

[WARN] LTG_TOOL_glitch_motion.py
  - G003: Multi-Glitchkin frame has only 0 unique expression(s) — at least 2 required. Found: none
  - G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).

[PASS] LTG_TOOL_glitch_spec_lint.py
  All checks passed.

[WARN] LTG_TOOL_glitch_turnaround.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[PASS] LTG_TOOL_sb_ep05_covetous.py
  All checks passed.

[PASS] LTG_TOOL_sf_covetous_glitch.py
  All checks passed.

[PASS] LTG_TOOL_sf_covetous_glitch_c43.py
  All checks passed.

[WARN] LTG_TOOL_style_frame_02_glitch_storm.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_03_other_side.py
  - G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - G008: Interior states (YEARNING/COVETOUS/HOLLOW) detected but no bilateral eye rule found. Spec §6.3: interior states require IDENTICAL left+right eye glyphs — asymmetric destabilization must be SKIPPED for these states.

======================================================================
Checks: G001 dimensions | G002 body ratio | G003 multi-uniqueness |
        G004 crack order | G005 UV shadow | G006 organic fill |
        G007 void outline | G008 interior bilateral
Suppressions: glitch_spec_suppressions.json

13 Glitch generator(s) have spec violations. Review before critique.
======================================================================

────────────────────────────────────────────────────────────────────────
Detail: Spec Sync CI Gate
────────────────────────────────────────────────────────────────────────
========================================================================
LTG Spec Sync CI Gate — v1.1.0
Characters: luma, cosmo, miri, byte, glitch
========================================================================

  ────────────────────────────────────────────────────────────────────
  WARN    LUMA  [(no file found)]
  ────────────────────────────────────────────────────────────────────
  ERROR: No generator files found for 'luma' in /home/wipkat/team/output/tools. Patterns: ['LTG_TOOL_luma_expression_sheet_v*.py', 'LTG_TOOL_luma_turnaround_v*.py']

  ────────────────────────────────────────────────────────────────────
  WARN    COSMO  [(no file found)]
  ────────────────────────────────────────────────────────────────────
  ERROR: No generator files found for 'cosmo' in /home/wipkat/team/output/tools. Patterns: ['LTG_TOOL_cosmo_expression_sheet_v*.py', 'LTG_TOOL_cosmo_turnaround_v*.py']

  ────────────────────────────────────────────────────────────────────
  WARN    MIRI  [(no file found)]
  ────────────────────────────────────────────────────────────────────
  ERROR: No generator files found for 'miri' in /home/wipkat/team/output/tools. Patterns: ['LTG_TOOL_grandma_miri_expression_sheet_v*.py']

  ────────────────────────────────────────────────────────────────────
  WARN    BYTE  [(no file found)]
  ────────────────────────────────────────────────────────────────────
  ERROR: No generator files found for 'byte' in /home/wipkat/team/output/tools. Patterns: ['LTG_TOOL_byte_expression_sheet_v*.py', 'LTG_TOOL_byte_expressions_generator.py']

  ────────────────────────────────────────────────────────────────────
  WARN    GLITCH  [...OL_bg_glitch_storm_colorfix.py, LTG_TOOL_bg_other_side.py]
  ────────────────────────────────────────────────────────────────────
  Checks: 7 PASS / 13 WARN / 0 FAIL
  No P1 violations.

========================================================================
P1 violations: 0  |  Per-char: LUMA:WARN, COSMO:WARN, MIRI:WARN, BYTE:WARN, GLITCH:WARN  |  CI PASS
CI RESULT: PASS
========================================================================

────────────────────────────────────────────────────────────────────────
Detail: Char Spec Linter
────────────────────────────────────────────────────────────────────────

======================================================================
WARN    Luma  ((no file))
======================================================================
  ERROR: No generator files found for 'luma' in /home/wipkat/team/output/tools. Patterns: ['LTG_TOOL_luma_expression_sheet_v*.py', 'LTG_TOOL_luma_turnaround_v*.py']

======================================================================
WARN    Cosmo  ((no file))
======================================================================
  ERROR: No generator files found for 'cosmo' in /home/wipkat/team/output/tools. Patterns: ['LTG_TOOL_cosmo_expression_sheet_v*.py', 'LTG_TOOL_cosmo_turnaround_v*.py']

======================================================================
WARN    Grandma Miri  ((no file))
======================================================================
  ERROR: No generator files found for 'miri' in /home/wipkat/team/output/tools. Patterns: ['LTG_TOOL_grandma_miri_expression_sheet_v*.py']

======================================================================
WARN    Byte  ((no file))
======================================================================
  ERROR: No generator files found for 'byte' in /home/wipkat/team/output/tools. Patterns: ['LTG_TOOL_byte_expression_sheet_v*.py', 'LTG_TOOL_byte_expressions_generator.py']

======================================================================
TOTAL: 0 PASS / 0 WARN / 0 FAIL across 4 character(s)

────────────────────────────────────────────────────────────────────────
Detail: Dual-Output File Check
────────────────────────────────────────────────────────────────────────
DUAL-OUTPUT CONFLICTS (30 output file(s) claimed by multiple generators):
  LTG_CHAR_byte_expression_sheet.png
    ← LTG_TOOL_byte_expression_sheet.py
    ← LTG_TOOL_sb_a2_cycle15.py
  LTG_CHAR_byte_motion.png
    ← LTG_CHAR_byte_motion.py
    ← LTG_TOOL_byte_motion.py
  LTG_CHAR_luma_motion.png
    ← LTG_CHAR_luma_motion.py
    ← LTG_TOOL_luma_motion.py
  LTG_COLOR_sf_covetous_glitch.png
    ← LTG_TOOL_sf_covetous_glitch.py
    ← LTG_TOOL_sf_covetous_glitch_c43.py
  LTG_ENV_tech_den.png
    ← LTG_TOOL_bg_tech_den.py
    ← LTG_TOOL_render_lib.py
    ← LTG_TOOL_warmth_inject.py
  LTG_SB_act1_panel_a101.png
    ← LTG_TOOL_sb_act1_contact_sheet.py
    ← LTG_TOOL_sb_act1_full_contact_sheet.py
    ← LTG_TOOL_sb_panel_a101.py
  LTG_SB_act1_panel_a102.png
    ← LTG_TOOL_sb_act1_contact_sheet.py
    ← LTG_TOOL_sb_act1_full_contact_sheet.py
    ← LTG_TOOL_sb_panel_a102.py
  LTG_SB_act1_panel_a103.png
    ← LTG_TOOL_sb_act1_contact_sheet.py
    ← LTG_TOOL_sb_act1_full_contact_sheet.py
    ← LTG_TOOL_sb_panel_a103.py
  LTG_SB_act1_panel_a104.png
    ← LTG_TOOL_sb_act1_contact_sheet.py
    ← LTG_TOOL_sb_act1_full_contact_sheet.py
    ← LTG_TOOL_sb_panel_a104_kitchen.py
  LTG_SB_act2_contact_sheet.png
    ← LTG_TOOL_sb_a2_cycle15.py
    ← LTG_TOOL_sb_act2_contact_sheet.py
  LTG_SB_act2_panel_a104.png
    ← LTG_TOOL_act2_panels_cycle14.py
    ← LTG_TOOL_sb_a2_cycle15.py
    ← LTG_TOOL_sb_act1_full_contact_sheet.py
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a104_kitchen.py
  LTG_SB_act2_panel_a201.png
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a201.py
  LTG_SB_act2_panel_a202.png
    ← LTG_TOOL_act2_panels_cycle14.py
    ← LTG_TOOL_sb_a2_cycle15.py
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a202.py
  LTG_SB_act2_panel_a203.png
    ← LTG_TOOL_sb_a2_cycle15.py
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a203.py
  LTG_SB_act2_panel_a204.png
    ← LTG_TOOL_sb_a2_cycle15.py
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a204.py
  LTG_SB_act2_panel_a205.png
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a205.py
  LTG_SB_act2_panel_a205b.png
    ← LTG_TOOL_act2_panels_cycle14.py
    ← LTG_TOOL_sb_a2_cycle15.py
    ← LTG_TOOL_sb_act2_contact_sheet.py
  LTG_SB_act2_panel_a206.png
    ← LTG_TOOL_act2_panels_cycle14.py
    ← LTG_TOOL_sb_a2_cycle15.py
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a206_insert.py
  LTG_SB_act2_panel_a206_med.png
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a206_insert.py
  LTG_SB_act2_panel_a207.png
    ← LTG_TOOL_sb_a2_cycle15.py
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a207.py
  LTG_SB_act2_panel_a207b.png
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a207b.py
  LTG_SB_act2_panel_a208.png
    ← LTG_TOOL_sb_act2_contact_sheet.py
    ← LTG_TOOL_sb_panel_a208.py
  LTG_SB_cold_open_P03.png
    ← LTG_TOOL_sb_caption_retrofit.py
    ← LTG_TOOL_sb_cold_open_P03.py
  LTG_SB_cold_open_P06.png
    ← LTG_TOOL_sb_caption_retrofit.py
    ← LTG_TOOL_sb_cold_open_P06.py
  LTG_SB_cold_open_P07.png
    ← LTG_TOOL_sb_caption_retrofit.py
    ← LTG_TOOL_sb_cold_open_P07.py
  LTG_SB_cold_open_P08.png
    ← LTG_TOOL_sb_caption_retrofit.py
    ← LTG_TOOL_sb_cold_open_P08.py
  LTG_SB_cold_open_P09.png
    ← LTG_TOOL_sb_caption_retrofit.py
    ← LTG_TOOL_sb_cold_open_P09.py
  LTG_SB_cold_open_P23.png
    ← LTG_TOOL_sb_caption_retrofit.py
    ← LTG_TOOL_sb_cold_open_P23.py
  LTG_SB_cold_open_P24.png
    ← LTG_TOOL_sb_caption_retrofit.py
    ← LTG_TOOL_sb_cold_open_P24.py
  LTG_SB_pilot_cold_open.png
    ← LTG_SB_pilot_cold_open.py
    ← LTG_TOOL_sb_pilot_cold_open.py

────────────────────────────────────────────────────────────────────────
Detail: Hardcoded Path Check
────────────────────────────────────────────────────────────────────────
  FAIL  LTG_CHAR_byte_motion.py  (1 hit(s)) — not in known_issues
    L 614      out_dir = "/home/wipkat/team/output/characters/motion"
  FAIL  LTG_CHAR_luma_motion.py  (1 hit(s)) — not in known_issues
    L 646      out_dir = "/home/wipkat/team/output/characters/motion"
  FAIL  LTG_SB_pilot_cold_open.py  (2 hit(s)) — not in known_issues
    L  33          /home/wipkat/team/output/storyboards/
    L  46  OUTPUT_DIR  = "/home/wipkat/team/output/storyboards"
  FAIL  LTG_TOOL_byte_cracked_eye_glyph.py  (2 hit(s)) — not in known_issues
    L  32  Output: /home/wipkat/team/output/characters/main/LTG_CHAR_byte_cracked_eye_glyph
    L  44  OUTPUT_PATH = "/home/wipkat/team/output/characters/main/LTG_CHAR_byte_cracked_ey
  FAIL  LTG_TOOL_byte_expression_sheet.py  (1 hit(s)) — not in known_issues
    L 988      out_dir = "/home/wipkat/team/output/characters/main"
  FAIL  LTG_TOOL_ci_suite.py  (6 hit(s)) — not in known_issues
    L 129                from LTG_TOOL_project_paths to detect /home/-prefixed absolute
    L 589      Scan all active .py files in tools_dir for hardcoded /home/ paths.
    L 620              return "PASS", "0 hardcoded /home/ path(s) in active generators", ""
    L 656              lines.append("  → Migrate: replace /home/wipkat/team/output/... with
    L 663                  f"{total_hits} hardcoded /home/ occurrence(s) in {len(by_file)} 
    L 669                  f"{total_hits} hardcoded /home/ occurrence(s) in {len(by_file)} 
  FAIL  LTG_TOOL_color_qa_c37_runner.py  (1 hit(s)) — not in known_issues
    L  26  BASE_DIR   = (TOOLS_DIR / ".." / "..").resolve()   # /home/wipkat/team
  FAIL  LTG_TOOL_colorkey_otherside_gen.py  (2 hit(s)) — not in known_issues
    L  35  Output: /home/wipkat/team/output/color/color_keys/thumbnails/
    L  48  OUTPUT_DIR = "/home/wipkat/team/output/color/color_keys/thumbnails"
  FAIL  LTG_TOOL_contact_sheet_arc_diff.py  (2 hit(s)) — not in known_issues
    L  22      /home/wipkat/team/output/storyboards/LTG_TOOL_arc_diff_output.png
    L  81  DEFAULT_OUTPUT = "/home/wipkat/team/output/storyboards/LTG_TOOL_arc_diff_output.
  FAIL  LTG_TOOL_env_grandma_living_room.py  (2 hit(s)) — not in known_issues
    L  40  Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandma_living
    L1124      out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandm
  FAIL  LTG_TOOL_fidelity_check_c24.py  (1 hit(s)) — not in known_issues
    L  29  BASE = "/home/wipkat/team/output"
  FAIL  LTG_TOOL_logo.py  (2 hit(s)) — not in known_issues
    L  41  CANONICAL_OUTPUT = "/home/wipkat/team/output/production/LTG_BRAND_logo.png"
    L  42  UNDERLYING_OUTPUT = "/home/wipkat/team/output/production/LTG_BRAND_logo_asymmetr
  FAIL  LTG_TOOL_luma_act2_standing_pose.py  (1 hit(s)) — not in known_issues
    L 686          "/home/wipkat/team/output/characters/main/"
  FAIL  LTG_TOOL_luma_classroom_pose.py  (1 hit(s)) — not in known_issues
    L 480      out_dir = "/home/wipkat/team/output/characters/main"
  FAIL  LTG_TOOL_luma_cold_overlay_swatches.py  (1 hit(s)) — not in known_issues
    L 235      out_path = "/home/wipkat/team/output/characters/color_models/swatches/LTG_CO
  FAIL  LTG_TOOL_naming_compliance_copier.py  (1 hit(s)) — not in known_issues
    L  26  BASE = "/home/wipkat/team/output"
  FAIL  LTG_TOOL_naming_compliance_copy.py  (1 hit(s)) — not in known_issues
    L  54  BASE = "/home/wipkat/team/output"
  FAIL  LTG_TOOL_project_paths.py  (9 hit(s)) — not in known_issues
    L  13  found.  This eliminates all hardcoded /home/wipkat/team paths across the
    L  22      # Replace:  OUTPUT_PATH = "/home/wipkat/team/output/backgrounds/..."
    L  33      OLD:  PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
    L  36      OLD:  out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_
    L  39      OLD:  BASE = "/home/wipkat/team/output"
    L 112          # → /home/wipkat/team/output/backgrounds/environments/LTG_ENV_foo.png
    L 191  def audit_hardcoded_paths(tools_directory=None, pattern="/home/"):
    L 199          pattern (str): String to search for.  Default "/home/" catches any
    L 232          print("PASS — no hardcoded /home/ paths found in output/tools/*.py")
  FAIL  LTG_TOOL_sb_act1_full_contact_sheet.py  (3 hit(s)) — not in known_issues
    L  34    /home/wipkat/team/output/storyboards/LTG_SB_act1_full_contact_sheet.png
    L  40  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
    L  41  OUTPUT_DIR  = "/home/wipkat/team/output/storyboards"
  FAIL  LTG_TOOL_sb_act2_contact_sheet.py  (3 hit(s)) — not in known_issues
    L  38    /home/wipkat/team/output/storyboards/act2/LTG_SB_act2_contact_sheet.png
    L  44  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
    L  45  ACT2_DIR    = "/home/wipkat/team/output/storyboards/act2"
  FAIL  LTG_TOOL_sb_caption_retrofit.py  (1 hit(s)) — not in known_issues
    L  69      PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
  FAIL  LTG_TOOL_sb_cold_open_P10.py  (1 hit(s)) — not in known_issues
    L  55  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  FAIL  LTG_TOOL_sb_cold_open_P11.py  (1 hit(s)) — not in known_issues
    L  47  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  FAIL  LTG_TOOL_sb_cold_open_P14.py  (1 hit(s)) — not in known_issues
    L  49  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  FAIL  LTG_TOOL_sb_cold_open_P15.py  (1 hit(s)) — not in known_issues
    L  52  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  FAIL  LTG_TOOL_sb_panel_a203.py  (2 hit(s)) — not in known_issues
    L  37    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a203.png
    L  45  PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
  FAIL  LTG_TOOL_sf02_fill_light_fix_c35.py  (1 hit(s)) — not in known_issues
    L 356      out_path = "/home/wipkat/team/output/tools/LTG_SNAP_sf02_fill_light_test.png
  FAIL  LTG_TOOL_sf04_luma_byte_v005.py  (2 hit(s)) — not in known_issues
    L  55  Output: /home/wipkat/team/output/color/style_frames/LTG_SF_luma_byte_v005.png
    L  73  OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_SF_luma_byte_v005
  FAIL  LTG_TOOL_sf_miri_luma_handoff.py  (1 hit(s)) — not in known_issues
    L 897      out_dir  = "/home/wipkat/team/output/color/style_frames"
  FAIL  LTG_TOOL_style_frame_05_relationship.py  (2 hit(s)) — not in known_issues
    L  62    /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_sf05.png
    L  84  OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_
  FAIL  LTG_TOOL_styleframe_luma_byte.py  (2 hit(s)) — not in known_issues
    L  42  Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_luma_by
    L  60  OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_
  FAIL  LTG_TOOL_world_type_infer.py  (1 hit(s)) — not in known_issues
    L 209                    "/home/wipkat/team/output/color/style_frames/LTG_COLOR_stylefr
  FAIL  run_c31_qa.py  (2 hit(s)) — not in known_issues
    L  24  Output: /home/wipkat/team/output/production/qa_c31_pitch_assets.md
    L  38  ROOT = Path("/home/wipkat/team")
  KNOWN LTG_TOOL_act2_panels_cycle14.py  (7 hit(s)) — migration backlog
    L  32    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a104.png
    L  33    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a202.png
    L  34    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a205b.png
    L  35    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a206.png
    L  36    /home/wipkat/team/output/storyboards/LTG_SB_act2_contactsheet.png
    L  44  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
    L  45  SHEETS_DIR  = "/home/wipkat/team/output/storyboards"
  KNOWN LTG_TOOL_bg_classroom.py  (2 hit(s)) — migration backlog
    L  34  Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_classroom_bg.p
    L 751      out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_classr
  KNOWN LTG_TOOL_bg_glitch_layer_encounter.py  (2 hit(s)) — migration backlog
    L  61  Save: /home/wipkat/team/output/backgrounds/environments/bg_glitch_layer_encounte
    L 554          '/home/wipkat/team/output/backgrounds/environments/bg_glitch_layer_encou
  KNOWN LTG_TOOL_bg_glitch_layer_frame.py  (2 hit(s)) — migration backlog
    L  37  Save: /home/wipkat/team/output/backgrounds/environments/glitch_layer_frame.png
    L 357          '/home/wipkat/team/output/backgrounds/environments/glitch_layer_frame.pn
  KNOWN LTG_TOOL_bg_glitch_storm_colorfix.py  (2 hit(s)) — migration backlog
    L  43  Output: /home/wipkat/team/output/backgrounds/environments/
    L  55  OUTPUT_PATH = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_glitch_
  KNOWN LTG_TOOL_bg_glitchlayer_frame.py  (2 hit(s)) — migration backlog
    L  22  Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_glitchlayer_fr
    L 314          '/home/wipkat/team/output/backgrounds/environments/LTG_ENV_glitchlayer_f
  KNOWN LTG_TOOL_bg_grandma_kitchen.py  (3 hit(s)) — migration backlog
    L  54  Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandma_kitche
    L1461      out_dir = "/home/wipkat/team/output/backgrounds/environments"
    L1502      out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandm
  KNOWN LTG_TOOL_bg_millbrook_main_street.py  (2 hit(s)) — migration backlog
    L 846      out_dir = "/home/wipkat/team/output/backgrounds/environments"
    L 905      out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_millbr
  KNOWN LTG_TOOL_bg_other_side.py  (1 hit(s)) — migration backlog
    L 379      out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_other_
  KNOWN LTG_TOOL_bg_school_hallway.py  (2 hit(s)) — migration backlog
    L  62  Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_school_hallway
    L 927      out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_school
  KNOWN LTG_TOOL_bg_tech_den.py  (2 hit(s)) — migration backlog
    L  43  Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_tech_den.png
    L 850      out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_tech_d
  KNOWN LTG_TOOL_character_lineup.py  (2 hit(s)) — migration backlog
    L  49  Output: /home/wipkat/team/output/characters/main/LTG_CHAR_character_lineup.png
    L 992      out_dir = "/home/wipkat/team/output/characters/main"
  KNOWN LTG_TOOL_colorkey_glitch_covetous_gen.py  (1 hit(s)) — migration backlog
    L  55  OUTPUT_PATH = "/home/wipkat/team/output/color/color_keys/LTG_COLOR_colorkey_glit
  KNOWN LTG_TOOL_colorkey_glitchstorm_gen.py  (2 hit(s)) — migration backlog
    L  32  Output: /home/wipkat/team/output/color/color_keys/thumbnails/
    L  44  OUTPUT_DIR = "/home/wipkat/team/output/color/color_keys/thumbnails"
  KNOWN LTG_TOOL_cosmo_motion.py  (1 hit(s)) — migration backlog
    L 640      out_dir = "/home/wipkat/team/output/characters/motion"
  KNOWN LTG_TOOL_logo_asymmetric.py  (2 hit(s)) — migration backlog
    L  20      before falling through to system font paths. No hardcoded /home/wipkat/team 
    L  50  # Project-path resolution (Kai Nakamura, Cycle 44) — no hardcoded /home/wipkat/t
  KNOWN LTG_TOOL_luma_motion.py  (1 hit(s)) — migration backlog
    L 583      out_dir = "/home/wipkat/team/output/characters/motion"
  KNOWN LTG_TOOL_precritique_qa.py  (1 hit(s)) — migration backlog
    L 112  REPO_ROOT   = Path(__file__).resolve().parent.parent.parent  # /home/wipkat/team
  KNOWN LTG_TOOL_sb_a2_cycle15.py  (13 hit(s)) — migration backlog
    L  31    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a203.png
    L  32    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a204.png
    L  33    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a207.png  (place
    L  34    /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_a2_02.png       (copy)
    L  35    /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_a2_03.png
    L  36    /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_a2_04.png
    L  37    /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_a2_07.png
    L  38    /home/wipkat/team/output/storyboards/act2/LTG_SB_act2_contact_sheet.png
    L  47  PANELS_DIR     = "/home/wipkat/team/output/storyboards/panels"
    L  48  ACT2_PANELS    = "/home/wipkat/team/output/storyboards/act2/panels"
    L  49  SHEETS_DIR     = "/home/wipkat/team/output/storyboards"
    L  50  ACT2_SHEETS    = "/home/wipkat/team/output/storyboards/act2"
    L 864      Output: /home/wipkat/team/output/storyboards/act2/LTG_SB_act2_contact_sheet.
  KNOWN LTG_TOOL_sb_act1_contact_sheet.py  (7 hit(s)) — migration backlog
    L  30    /home/wipkat/team/output/storyboards/LTG_SB_act1_coldopen_contact_sheet.png
    L  37  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
    L  38  OUTPUT_DIR  = "/home/wipkat/team/output/storyboards"
    L  97          "/home/wipkat/team/output/tools/LTG_TOOL_sb_panel_a101.py",
    L  98          "/home/wipkat/team/output/tools/LTG_TOOL_sb_panel_a102.py",
    L  99          "/home/wipkat/team/output/tools/LTG_TOOL_sb_panel_a103.py",   # v002
    L 100          "/home/wipkat/team/output/tools/LTG_TOOL_sb_panel_a104_kitchen.py",
  KNOWN LTG_TOOL_sb_cold_open_P03.py  (1 hit(s)) — migration backlog
    L  29  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_cold_open_P06.py  (1 hit(s)) — migration backlog
    L  35  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_cold_open_P07.py  (1 hit(s)) — migration backlog
    L  45  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_cold_open_P08.py  (1 hit(s)) — migration backlog
    L  38  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_cold_open_P09.py  (1 hit(s)) — migration backlog
    L  52  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_cold_open_P23.py  (1 hit(s)) — migration backlog
    L  37  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_cold_open_P24.py  (1 hit(s)) — migration backlog
    L  35  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_ep05_covetous.py  (1 hit(s)) — migration backlog
    L  46  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a101.py  (1 hit(s)) — migration backlog
    L  31  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a102.py  (1 hit(s)) — migration backlog
    L  30  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a103.py  (1 hit(s)) — migration backlog
    L  35  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a104_kitchen.py  (1 hit(s)) — migration backlog
    L  36  PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a201.py  (3 hit(s)) — migration backlog
    L  27    /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a201.png
    L  35  ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
    L  36  PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a202.py  (2 hit(s)) — migration backlog
    L  32    /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a202.png
    L  45  ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
  KNOWN LTG_TOOL_sb_panel_a204.py  (2 hit(s)) — migration backlog
    L  38    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a204.png
    L  46  PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a205.py  (3 hit(s)) — migration backlog
    L  27    /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a205.png
    L  35  ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
    L  36  PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a206_insert.py  (2 hit(s)) — migration backlog
    L  35    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a206_med.png
    L  43  PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a207.py  (2 hit(s)) — migration backlog
    L  36    /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a207.png
    L  43  PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a207b.py  (2 hit(s)) — migration backlog
    L  37  ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
    L  38  PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_panel_a208.py  (3 hit(s)) — migration backlog
    L  33    /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a208.png
    L  41  ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
    L  42  PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
  KNOWN LTG_TOOL_sb_pilot_cold_open.py  (2 hit(s)) — migration backlog
    L  39          /home/wipkat/team/output/storyboards/
    L  52  OUTPUT_DIR  = "/home/wipkat/team/output/storyboards"
  KNOWN LTG_TOOL_sf_covetous_glitch.py  (1 hit(s)) — migration backlog
    L 671      out_path = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_sf_covetou
  KNOWN LTG_TOOL_sf_covetous_glitch_c43.py  (1 hit(s)) — migration backlog
    L 861      out_path = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_sf_covetou
  KNOWN LTG_TOOL_sight_line_diagnostic.py  (4 hit(s)) — migration backlog
    L  67        output_dir  = "/home/wipkat/team/output/production",
    L 126  OUTPUT_DIR_DEFAULT = "/home/wipkat/team/output/production"
    L 823      SF01_V006 = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_stylefram
    L 824      SF01_V005 = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_stylefram
  KNOWN LTG_TOOL_style_frame_02_glitch_storm.py  (3 hit(s)) — migration backlog
    L  52  Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_
    L  78  OUTPUT_PATH  = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe
    L  79  NOLIGHT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe
  KNOWN LTG_TOOL_style_frame_03_other_side.py  (2 hit(s)) — migration backlog
    L  58  Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_othersi
    L 945      OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_stylefr
  KNOWN LTG_TOOL_style_frame_04_resolution.py  (3 hit(s)) — migration backlog
    L  42    /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_sf04.png
    L  69  OUTPUT_PATH  = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe
    L  70  NOLIGHT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe
  KNOWN LTG_TOOL_styleframe_discovery.py  (3 hit(s)) — migration backlog
    L  45  Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discove
    L  68  OUTPUT_PATH        = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styl
    L  69  NOLIGHT_PATH       = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styl
  → Migrate: replace /home/wipkat/team/output/... with output_dir() from LTG_TOOL_project_paths
  → Add entry to ci_known_issues.json under hardcoded_path_check once resolved

────────────────────────────────────────────────────────────────────────
Detail: Thumbnail Lint
────────────────────────────────────────────────────────────────────────
  FAIL  LTG_CHAR_byte_motion.py  (1 hit(s))
    L 612      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_CHAR_luma_motion.py  (1 hit(s))
    L 644      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_SB_pilot_cold_open.py  (1 hit(s))
    L 987      sheet.thumbnail((1280, 720), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_bg_classroom.py  (1 hit(s))
    L 749      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_bg_grandma_kitchen.py  (1 hit(s))
    L1469      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_bg_luma_study_interior.py  (1 hit(s))
    L 738      rgb_img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_bg_other_side.py  (1 hit(s))
    L 369      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_bg_school_hallway.py  (1 hit(s))
    L 929      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_bodypart_hierarchy.py  (1 hit(s))
    L 498      out.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_byte_commitment_rpd_test.py  (1 hit(s))
    L 218      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_byte_expression_sheet.py  (1 hit(s))
    L 980      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_byte_motion.py  (1 hit(s))
    L 714      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_character_face_test.py  (1 hit(s))
    L 904      sheet.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_character_lineup.py  (1 hit(s))
    L 983          img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_colorkey_glitch_covetous_gen.py  (1 hit(s))
    L 423      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_cosmo_expression_sheet.py  (1 hit(s))
    L 727      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_cosmo_motion.py  (1 hit(s))
    L 638      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_cosmo_turnaround.py  (1 hit(s))
    L 804      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_costume_bg_clash.py  (1 hit(s))
    L 250      thumb.thumbnail((_ANALYSIS_MAX_PX, _ANALYSIS_MAX_PX), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_env_grandma_living_room.py  (1 hit(s))
    L1190      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_expression_isolator.py  (1 hit(s))
    L 341          img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_expression_silhouette.py  (2 hit(s))
    L 644      out.thumbnail((1280, 1280), Image.LANCZOS)
    L 787      strip.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_face_curve_validator.py  (1 hit(s))
    L 878      sheet.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_glitch_body_primitive_diagram_gen.py  (1 hit(s))
    L 360      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_glitch_motion.py  (1 hit(s))
    L 545      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_grandma_miri_expression_sheet.py  (1 hit(s))
    L 833      sheet.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_lineup_tier_depth_sketch.py  (1 hit(s))
    L 251      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_luma_color_model.py  (1 hit(s))
    L 358      model.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_luma_expression_sheet.py  (1 hit(s))
    L1434      sheet.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_luma_face_curves.py  (1 hit(s))
    L 739      sheet.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_luma_motion.py  (1 hit(s))
    L 581      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_luma_turnaround.py  (1 hit(s))
    L 810      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_miri_motion.py  (1 hit(s))
    L 713      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_pixel_font_v001.py  (1 hit(s))
    L 572      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_procedural_draw.py  (3 hit(s))
    L 485      crop.thumbnail((1280, 1280), Image.LANCZOS)
    L 502      annotated.thumbnail((1280, 1280), Image.LANCZOS)
    L 894          canvas.thumbnail((640, 640), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_caption_retrofit.py  (1 hit(s))
    L 241      new_img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P03.py  (1 hit(s))
    L 345      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P06.py  (1 hit(s))
    L 487      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P07.py  (1 hit(s))
    L 608      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P08.py  (1 hit(s))
    L 500      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P09.py  (1 hit(s))
    L 606      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P10.py  (1 hit(s))
    L 340      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P11.py  (1 hit(s))
    L 333      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P14.py  (1 hit(s))
    L 485      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P15.py  (1 hit(s))
    L 359      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P23.py  (1 hit(s))
    L 527      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_cold_open_P24.py  (1 hit(s))
    L 677      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_ep05_covetous.py  (1 hit(s))
    L 609      img.thumbnail((1280, 1280))
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sb_pilot_cold_open.py  (1 hit(s))
    L1214      sheet.thumbnail((1280, 720), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sf02_fill_light_fix_c35.py  (1 hit(s))
    L 357      result.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sf04_luma_byte_v005.py  (1 hit(s))
    L 941          img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_sf_miri_luma_handoff.py  (1 hit(s))
    L 944      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_style_frame_02_glitch_storm.py  (1 hit(s))
    L  17    - Eliminates img.thumbnail() LANCZOS pass at end — the source of SUNLIT_AMBER
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_style_frame_03_other_side.py  (1 hit(s))
    L 921      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_style_frame_04_resolution.py  (1 hit(s))
    L 983      img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_styleframe_discovery.py  (1 hit(s))
    L1098          img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_styleframe_luma_byte.py  (1 hit(s))
    L 785          img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_thumbnail_preview_v001.py  (3 hit(s))
    L  54      img.thumbnail((target_w, target_h), Image.LANCZOS)
    L 108      thumb_raw.thumbnail((THUMB_W, THUMB_H), Image.LANCZOS)
    L 158      sheet.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_warmth_inject.py  (1 hit(s))
    L 313          result_img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  LTG_TOOL_warmth_inject_hook.py  (1 hit(s))
    L 117      result_img.thumbnail((1280, 1280), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.
  FAIL  test_face_lighting.py  (1 hit(s))
    L 173          canvas.thumbnail((640, 640), Image.LANCZOS)
         → Use native 1280×720 canvas instead.
         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.

────────────────────────────────────────────────────────────────────────
Detail: Motion Sheet Coverage
────────────────────────────────────────────────────────────────────────
  WARN  grandma_miri: LTG_CHAR_grandma_miri_expression_sheet.png exists but LTG_CHAR_grandma_miri_motion.png is missing