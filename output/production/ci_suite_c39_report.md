========================================================================
LTG CI Suite v1.0.0 — Combined Report
Tools dir : /home/wipkat/team/output/tools
Fail-on   : FAIL
========================================================================
  ✓ [PASS ] Stub Integrity Linter
          185 file(s) — 0 PASS / 0 WARN / 0 ERROR
  ⚠ [WARN ] Draw Order Linter v002
          177 file(s) — 136 PASS / 41 WARN / 0 ERROR
  ⚠ [WARN ] Glitch Spec Linter v001
          32 Glitch generator(s) — 4 PASS / 28 WARN (2 suppressed)
  ✓ [PASS ] Spec Sync CI Gate v001
          5 character(s) — 0 P1 FAIL: none / 0 WARN: none
  ✓ [PASS ] Char Spec Linter v001
          3 character(s) — 0 PASS / 0 WARN / 0 FAIL

  ⚠ OVERALL: WARN  (exit code 0)
========================================================================

────────────────────────────────────────────────────────────────────────
Detail: Stub Integrity Linter
────────────────────────────────────────────────────────────────────────
======================================================================
LTG Stub Integrity Linter — Report
Files scanned: 185
  PASS : 185
  WARN : 0
  ERROR: 0
======================================================================

======================================================================
All scanned files pass stub integrity check.
======================================================================

────────────────────────────────────────────────────────────────────────
Detail: Draw Order Linter v002
────────────────────────────────────────────────────────────────────────
WARN   LTG_TOOL_act2_panels_cycle14.py  (3 warning(s))
         [W004] line 196: img.paste() at line 196 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_rgba.convert('RGB'))
         [W004] line 1085: img.paste() at line 1085 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_rgba.convert('RGB'))
         [W004] line 1170: img.paste() at line 1170 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_rgba.convert('RGB'))
WARN   LTG_TOOL_bg_classroom.py  (4 warning(s))
         [W004] line 97: img = alpha_composite() at line 97 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 298: img = alpha_composite() at line 298 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 320: img = alpha_composite() at line 320 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 611: img = alpha_composite() at line 611 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
WARN   LTG_TOOL_bg_classroom.py  (6 warning(s))
         [W004] line 81: img = alpha_composite() at line 81 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 242: img = alpha_composite() at line 242 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, warm_overlay)
         [W004] line 259: img = alpha_composite() at line 259 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, cool_overlay)
         [W004] line 286: img = alpha_composite() at line 286 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 306: img = alpha_composite() at line 306 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 637: img = alpha_composite() at line 637 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
PASS   LTG_TOOL_bg_glitch_layer_encounter.py
PASS   LTG_TOOL_bg_glitch_layer_frame.py
PASS   LTG_TOOL_bg_glitch_storm_colorfix.py
PASS   LTG_TOOL_bg_glitchlayer_frame.py
PASS   LTG_TOOL_bg_grandma_kitchen.py
PASS   LTG_TOOL_bg_grandma_kitchen.py
PASS   LTG_TOOL_bg_grandma_kitchen.py
PASS   LTG_TOOL_bg_grandma_kitchen.py
PASS   LTG_TOOL_bg_grandma_kitchen.py
WARN   LTG_TOOL_bg_millbrook_main_street.py  (1 warning(s))
         [W004] line 459: img.paste() at line 459 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"),
WARN   LTG_TOOL_bg_millbrook_main_street.py  (1 warning(s))
         [W004] line 477: img.paste() at line 477 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"),
WARN   LTG_TOOL_bg_other_side.py  (8 warning(s))
         [W004] line 92: img = alpha_composite() at line 92 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 141: img = alpha_composite() at line 141 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 340: img = alpha_composite() at line 340 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 371: img = alpha_composite() at line 371 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 405: img = alpha_composite() at line 405 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 424: img = alpha_composite() at line 424 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 452: img = alpha_composite() at line 452 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
         [W004] line 526: img = alpha_composite() at line 526 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img = Image.alpha_composite(img, overlay)
PASS   LTG_TOOL_bg_other_side.py
WARN   LTG_TOOL_bg_school_hallway.py  (1 warning(s))
         [W002] line 122: OUTLINE draw call for 'generic' at line 122 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
WARN   LTG_TOOL_bg_school_hallway.py  (1 warning(s))
         [W002] line 115: OUTLINE draw call for 'generic' at line 115 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
WARN   LTG_TOOL_bg_school_hallway.py  (1 warning(s))
         [W002] line 167: OUTLINE draw call for 'generic' at line 167 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
WARN   LTG_TOOL_bg_tech_den.py  (1 warning(s))
         [W002] line 152: OUTLINE draw call for 'generic' at line 152 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
WARN   LTG_TOOL_bg_tech_den.py  (1 warning(s))
         [W002] line 159: OUTLINE draw call for 'generic' at line 159 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
WARN   LTG_TOOL_bg_tech_den.py  (1 warning(s))
         [W002] line 159: OUTLINE draw call for 'generic' at line 159 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
WARN   LTG_TOOL_bg_tech_den.py  (1 warning(s))
         [W002] line 170: OUTLINE draw call for 'generic' at line 170 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
PASS   LTG_TOOL_byte_color_model.py
PASS   LTG_TOOL_byte_cracked_eye_glyph.py
PASS   LTG_TOOL_byte_expression_sheet.py
PASS   LTG_TOOL_byte_expression_sheet.py
PASS   LTG_TOOL_byte_expression_sheet.py
PASS   LTG_TOOL_byte_expression_sheet.py
PASS   LTG_TOOL_byte_expression_sheet.py
PASS   LTG_TOOL_byte_expression_sheet.py
PASS   LTG_TOOL_byte_motion.py
PASS   LTG_TOOL_byte_motion.py
PASS   LTG_TOOL_char_diff.py
PASS   LTG_TOOL_char_spec_lint.py
PASS   LTG_TOOL_character_face_test.py
WARN   LTG_TOOL_character_lineup.py  (1 warning(s))
         [W002] line 182: OUTLINE draw call for 'generic' at line 182 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([cx - lw*2, bb, cx - 4, bb + leg_h], fill=LUMA_PANTS, outline=LIN
WARN   LTG_TOOL_character_lineup.py  (1 warning(s))
         [W002] line 186: OUTLINE draw call for 'generic' at line 186 appears before the corresponding FILL call. Fill must be painted before outline.  >> draw.rectangle([cx - lw*2, bb, cx - 4, bb + leg_h], fill=LUMA_PANTS, outline=LIN
PASS   LTG_TOOL_character_lineup.py
PASS   LTG_TOOL_character_lineup.py
PASS   LTG_TOOL_character_lineup.py
PASS   LTG_TOOL_ci_suite.py
PASS   LTG_TOOL_color_qa_c37_runner.py
PASS   LTG_TOOL_color_verify.py
PASS   LTG_TOOL_color_verify.py
PASS   LTG_TOOL_colorkey_glitchstorm_gen.py
PASS   LTG_TOOL_colorkey_otherside_gen.py
PASS   LTG_TOOL_contact_sheet_arc_diff.py
PASS   LTG_TOOL_cosmo_color_model.py
PASS   LTG_TOOL_cosmo_expression_sheet.py
PASS   LTG_TOOL_cosmo_expression_sheet.py
PASS   LTG_TOOL_cosmo_expression_sheet.py
PASS   LTG_TOOL_cosmo_expression_sheet.py
PASS   LTG_TOOL_cosmo_expression_sheet.py
PASS   LTG_TOOL_cosmo_expression_sheet.py
PASS   LTG_TOOL_cosmo_expression_sheet.py
PASS   LTG_TOOL_cosmo_turnaround.py
PASS   LTG_TOOL_cycle13_panel_fixes.py
PASS   LTG_TOOL_draw_order_lint.py
PASS   LTG_TOOL_draw_order_lint.py
PASS   LTG_TOOL_env_grandma_living_room.py
PASS   LTG_TOOL_env_grandma_living_room.py
PASS   LTG_TOOL_expression_isolator.py
PASS   LTG_TOOL_expression_silhouette.py
PASS   LTG_TOOL_expression_silhouette.py
PASS   LTG_TOOL_expression_silhouette.py
PASS   LTG_TOOL_fidelity_check_c24.py
PASS   LTG_TOOL_fill_light_adapter.py
PASS   LTG_TOOL_glitch_color_model.py
PASS   LTG_TOOL_glitch_expression_sheet.py
PASS   LTG_TOOL_glitch_expression_sheet.py
PASS   LTG_TOOL_glitch_expression_sheet.py
PASS   LTG_TOOL_glitch_spec_lint.py
PASS   LTG_TOOL_glitch_turnaround.py
PASS   LTG_TOOL_glitch_turnaround.py
PASS   LTG_TOOL_grandma_miri_color_model.py
PASS   LTG_TOOL_grandma_miri_expression_sheet.py
PASS   LTG_TOOL_grandma_miri_expression_sheet.py
PASS   LTG_TOOL_grandma_miri_expression_sheet.py
PASS   LTG_TOOL_grandma_miri_expression_sheet.py
PASS   LTG_TOOL_lineup_palette_audit.py
WARN   LTG_TOOL_logo_asymmetric.py  (7 warning(s))
         [W004] line 169: img.paste() at line 169 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 184: img.paste() at line 184 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 199: img.paste() at line 199 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 215: img.paste() at line 215 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 226: img.paste() at line 226 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 244: img.paste() at line 244 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 262: img.paste() at line 262 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
WARN   LTG_TOOL_logo_asymmetric.py  (8 warning(s))
         [W004] line 132: img.paste() at line 132 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 192: img.paste() at line 192 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 207: img.paste() at line 207 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 222: img.paste() at line 222 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 237: img.paste() at line 237 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 247: img.paste() at line 247 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 264: img.paste() at line 264 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
         [W004] line 281: img.paste() at line 281 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert("RGB"))
PASS   LTG_TOOL_logo.py
PASS   LTG_TOOL_luma_act2_standing_pose.py
PASS   LTG_TOOL_luma_classroom_pose.py
PASS   LTG_TOOL_luma_cold_overlay_swatches.py
PASS   LTG_TOOL_luma_color_model.py
PASS   LTG_TOOL_luma_color_model.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
PASS   LTG_TOOL_luma_expression_sheet.py
WARN   LTG_TOOL_luma_motion.py  (1 warning(s))
         [W001] line 350: HEAD/FACE draw call at line 350 appears before BODY draw call at line 364. Body must be painted before head.  >> draw.text((hcx + hr + 22, hcy - 12), "+8° head tilt", fill=BEAT_COLOR)
PASS   LTG_TOOL_luma_turnaround.py
PASS   LTG_TOOL_luma_turnaround.py
PASS   LTG_TOOL_luma_turnaround.py
PASS   LTG_TOOL_miri_turnaround.py
PASS   LTG_TOOL_motion_spec_lint.py
PASS   LTG_TOOL_naming_cleanup.py
PASS   LTG_TOOL_naming_compliance_copier.py
PASS   LTG_TOOL_naming_compliance_copier.py
PASS   LTG_TOOL_naming_compliance_copy.py
PASS   LTG_TOOL_palette_warmth_lint.py
PASS   LTG_TOOL_palette_warmth_lint.py
PASS   LTG_TOOL_palette_warmth_lint.py
PASS   LTG_TOOL_palette_warmth_lint.py
PASS   LTG_TOOL_palette_warmth_lint.py
PASS   LTG_TOOL_pilot_cold_open.py
PASS   LTG_TOOL_precritique_qa.py
WARN   LTG_TOOL_procedural_draw.py  (4 warning(s))
         [W004] line 302: img.paste() at line 302 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(result)
         [W004] line 601: img.paste() at line 601 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert(img.mode))
         [W004] line 632: img.paste() at line 632 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert(img.mode))
         [W004] line 659: img.paste() at line 659 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(base_rgba.convert(img.mode))
PASS   LTG_TOOL_proportion_audit_c37_runner.py
PASS   LTG_TOOL_proportion_audit.py
PASS   LTG_TOOL_proportion_audit.py
PASS   LTG_TOOL_proportion_audit.py
PASS   LTG_TOOL_proportion_verify.py
PASS   LTG_TOOL_readme_sync.py
PASS   LTG_TOOL_render_lib.py
PASS   LTG_TOOL_render_qa.py
WARN   LTG_TOOL_sb_a2_cycle15.py  (1 warning(s))
         [W004] line 178: img.paste() at line 178 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_act1_contact_sheet.py  (1 warning(s))
         [W004] line 164: img.paste() at line 164 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(thumb, (thumb_x, thumb_y))
WARN   LTG_TOOL_sb_act1_contact_sheet.py  (1 warning(s))
         [W004] line 163: img.paste() at line 163 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(thumb, (thumb_x, thumb_y))
PASS   LTG_TOOL_sb_act1_full_contact_sheet.py
PASS   LTG_TOOL_sb_act2_contact_sheet.py
PASS   LTG_TOOL_sb_act2_contact_sheet.py
PASS   LTG_TOOL_sb_act2_contact_sheet.py
PASS   LTG_TOOL_sb_act2_contact_sheet.py
WARN   LTG_TOOL_sb_panel_a101.py  (1 warning(s))
         [W004] line 86: img.paste() at line 86 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a102.py  (1 warning(s))
         [W004] line 89: img.paste() at line 89 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a103.py  (2 warning(s))
         [W004] line 94: img.paste() at line 94 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
         [W004] line 126: img.paste() at line 126 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a103.py  (1 warning(s))
         [W004] line 105: img.paste() at line 105 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a104_kitchen.py  (1 warning(s))
         [W004] line 98: img.paste() at line 98 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a201.py  (1 warning(s))
         [W004] line 109: img.paste() at line 109 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a202.py  (1 warning(s))
         [W004] line 108: img.paste() at line 108 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
PASS   LTG_TOOL_sb_panel_a203.py
WARN   LTG_TOOL_sb_panel_a204.py  (1 warning(s))
         [W004] line 105: img.paste() at line 105 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a205.py  (1 warning(s))
         [W004] line 105: img.paste() at line 105 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a206_insert.py  (1 warning(s))
         [W004] line 101: img.paste() at line 101 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a207.py  (1 warning(s))
         [W004] line 123: img.paste() at line 123 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a207b.py  (1 warning(s))
         [W004] line 98: img.paste() at line 98 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a208.py  (1 warning(s))
         [W004] line 102: img.paste() at line 102 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_panel_a208.py  (1 warning(s))
         [W004] line 106: img.paste() at line 106 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
WARN   LTG_TOOL_sb_pilot_cold_open.py  (1 warning(s))
         [W004] line 145: img.paste() at line 145 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(Image.alpha_composite(base, glow).convert('RGB'))
PASS   LTG_TOOL_sf02_fill_light_fix_c35.py
PASS   LTG_TOOL_spec_extractor.py
PASS   LTG_TOOL_spec_sync_ci.py
PASS   LTG_TOOL_stub_linter.py
WARN   LTG_TOOL_style_frame_01_discovery.py  (3 warning(s))
         [W004] line 223: img.paste() at line 223 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_with_ghost.convert("RGB"))
         [W004] line 752: img.paste() at line 752 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_left.convert("RGB"), (0, 0))
         [W004] line 767: img.paste() at line 767 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_right.convert("RGB"), (W // 2 - 80, 0))
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_02_glitch_storm.py
PASS   LTG_TOOL_style_frame_03_other_side.py
PASS   LTG_TOOL_style_frame_03_other_side.py
PASS   LTG_TOOL_style_frame_03_other_side.py
PASS   LTG_TOOL_style_frame_03_other_side.py
PASS   LTG_TOOL_style_frame_03_other_side.py
WARN   LTG_TOOL_styleframe_discovery.py  (3 warning(s))
         [W004] line 235: img.paste() at line 235 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_with_ghost.convert("RGB"))
         [W004] line 806: img.paste() at line 806 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_left.convert("RGB"), (0, 0))
         [W004] line 823: img.paste() at line 823 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_right.convert("RGB"), (split_x, 0))
WARN   LTG_TOOL_styleframe_discovery.py  (3 warning(s))
         [W004] line 231: img.paste() at line 231 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_with_ghost.convert("RGB"))
         [W004] line 802: img.paste() at line 802 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_left.convert("RGB"), (0, 0))
         [W004] line 818: img.paste() at line 818 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_right.convert("RGB"), (split_x, 0))
WARN   LTG_TOOL_styleframe_discovery.py  (3 warning(s))
         [W004] line 244: img.paste() at line 244 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(img_with_ghost.convert("RGB"))
         [W004] line 912: img.paste() at line 912 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_left.convert("RGB"), (0, 0))
         [W004] line 928: img.paste() at line 928 is NOT followed by 'draw = ImageDraw.Draw(img)' refresh within the next 5 substantive lines at the same scope. Subsequent draw calls will operate on the stale draw object.   >> img.paste(composited_right.convert("RGB"), (split_x, 0))
PASS   LTG_TOOL_styleframe_luma_byte.py
PASS   LTG_TOOL_styleframe_luma_byte.py
PASS   LTG_TOOL_styleframe_luma_byte.py
PASS   LTG_TOOL_styleframe_luma_byte.py
PASS   LTG_TOOL_warmth_inject_hook.py
PASS   LTG_TOOL_warmth_inject.py
PASS   LTG_TOOL_world_type_infer.py

Summary: 177 file(s) — 136 PASS / 41 WARN / 0 ERROR

────────────────────────────────────────────────────────────────────────
Detail: Glitch Spec Linter v001
────────────────────────────────────────────────────────────────────────
======================================================================
LTG Glitch Spec Linter v1.3.0 — Report
Glitch generators found: 32
  PASS : 4
  WARN : 28
  (suppressed issues across all files: 2)
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
  - G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
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

[WARN] LTG_TOOL_character_lineup.py
  - G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(168, 152, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 130, 90). Glitch body fill must use CORRUPT_AMBER family only (spec §10).

[WARN] LTG_TOOL_character_lineup.py
  - G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(168, 152, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 130, 90). Glitch body fill must use CORRUPT_AMBER family only (spec §10).

[WARN] LTG_TOOL_character_lineup.py
  - G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(168, 152, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - G006: Possible organic/warm fill detected — fill=(212, 130, 90). Glitch body fill must use CORRUPT_AMBER family only (spec §10).

[WARN] LTG_TOOL_color_verify.py  [1 suppressed]
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.

[WARN] LTG_TOOL_color_verify.py  [1 suppressed]
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.

[WARN] LTG_TOOL_fidelity_check_c24.py
  - G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_glitch_color_model.py
  - G006: Possible organic/warm fill detected — fill=(200, 160, 80). Glitch body fill must use CORRUPT_AMBER family only (spec §10).

[PASS] LTG_TOOL_glitch_expression_sheet.py
  All checks passed.

[PASS] LTG_TOOL_glitch_expression_sheet.py
  All checks passed.

[PASS] LTG_TOOL_glitch_expression_sheet.py
  All checks passed.

[PASS] LTG_TOOL_glitch_spec_lint.py
  All checks passed.

[WARN] LTG_TOOL_glitch_turnaround.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_glitch_turnaround.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_02_glitch_storm.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_02_glitch_storm.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_02_glitch_storm.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_02_glitch_storm.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_02_glitch_storm.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_02_glitch_storm.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_02_glitch_storm.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_03_other_side.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_03_other_side.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_03_other_side.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_03_other_side.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

[WARN] LTG_TOOL_style_frame_03_other_side.py
  - G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).

======================================================================
Checks: G001 dimensions | G002 body ratio | G003 multi-uniqueness |
        G004 crack order | G005 UV shadow | G006 organic fill |
        G007 void outline | G008 interior bilateral
Suppressions: glitch_spec_suppressions.json

28 Glitch generator(s) have spec violations. Review before critique.
======================================================================

────────────────────────────────────────────────────────────────────────
Detail: Spec Sync CI Gate v001
────────────────────────────────────────────────────────────────────────
========================================================================
LTG Spec Sync CI Gate — v1.0.0
Characters: luma, cosmo, miri, byte, glitch
========================================================================

  ────────────────────────────────────────────────────────────────────
  WARN    LUMA  [LTG_TOOL_luma_expression_sheet.py]
  ────────────────────────────────────────────────────────────────────
  Checks: 4 PASS / 1 WARN / 0 FAIL
  No P1 violations.

  Advisory WARNs (1) — not a CI failure:
    WARN [L004] L004: Luma curl count: spec requires exactly 5 curls. No clear CURL_COUNT=5 constant or range(5) ...

  ────────────────────────────────────────────────────────────────────
  WARN    COSMO  [LTG_TOOL_cosmo_expression_sheet.py]
  ────────────────────────────────────────────────────────────────────
  Checks: 4 PASS / 1 WARN / 0 FAIL
  No P1 violations.

  Advisory WARNs (1) — not a CI failure:
    WARN [S002] S002: Eye-width coefficient 0.18 not confirmed in source. Check that `ew = int(HR * 0.18)` patter...

  ────────────────────────────────────────────────────────────────────
  WARN    MIRI  [LTG_TOOL_grandma_miri_expression_sheet.py]
  ────────────────────────────────────────────────────────────────────
  Checks: 3 PASS / 2 WARN / 0 FAIL
  No P1 violations.

  Advisory WARNs (2) — not a CI failure:
    WARN [M001] M001: Head-to-body ratio 3.2 not confirmed. No ratio-like constant near spec value found.
    WARN [M005] M005: Crow's feet / smile-line detail: expected keyword(s) ['crow', 'crinkle', 'CROW', 'smile_lin...

  ────────────────────────────────────────────────────────────────────
  PASS    BYTE  [LTG_TOOL_byte_expression_sheet.py]
  ────────────────────────────────────────────────────────────────────
  Checks: 2 PASS / 0 WARN / 0 FAIL
  No P1 violations.

  ────────────────────────────────────────────────────────────────────
  WARN    GLITCH  [...ch_storm_colorfix_v001.py, LTG_TOOL_bg_other_side.py]
  ────────────────────────────────────────────────────────────────────
  Checks: 4 PASS / 28 WARN / 0 FAIL
  No P1 violations.

========================================================================
P1 violations: 0  |  Per-char: LUMA:WARN, COSMO:WARN, MIRI:WARN, BYTE:PASS, GLITCH:WARN  |  CI PASS
CI RESULT: PASS
========================================================================

────────────────────────────────────────────────────────────────────────
Detail: Char Spec Linter v001
────────────────────────────────────────────────────────────────────────

======================================================================
WARN    Luma  (LTG_TOOL_luma_expression_sheet.py)
======================================================================
  PASS  [L001]
  PASS  [L002]
  PASS  [L003]
  WARN  [L004] L004: Luma curl count: spec requires exactly 5 curls. No clear CURL_COUNT=5 constant or range(5) in hair context found. Verify hair generator uses exactly 5 curl indicators.
  PASS  [L005]

  Summary: 4 PASS / 1 WARN / 0 FAIL  →  WARN

======================================================================
WARN    Cosmo  (LTG_TOOL_cosmo_expression_sheet.py)
======================================================================
  PASS  [S001]
  WARN  [S002] S002: Eye-width coefficient 0.18 not confirmed in source. Check that `ew = int(HR * 0.18)` pattern is present.
  PASS  [S003]
  PASS  [S004]
  PASS  [S005]

  Summary: 4 PASS / 1 WARN / 0 FAIL  →  WARN

======================================================================
WARN    Grandma Miri  (LTG_TOOL_grandma_miri_expression_sheet.py)
======================================================================
  WARN  [M001] M001: Head-to-body ratio 3.2 not confirmed. No ratio-like constant near spec value found.
  PASS  [M002]
  PASS  [M003]
  PASS  [M004]
  WARN  [M005] M005: Crow's feet / smile-line detail: expected keyword(s) ['crow', 'crinkle', 'CROW', 'smile_line', 'smile line', 'laugh_line'] not found in source.

  Summary: 3 PASS / 2 WARN / 0 FAIL  →  WARN

======================================================================
WARN    Byte  (LTG_TOOL_byte_expression_sheet.py)
======================================================================
  WARN  [B001] B001: Byte oval W:H ratio not confirmed. Expected `bw` and `bh` (or body_w/body_h) constants with bw >= bh. Spec: oval is ~1.0:0.85 W:H (wider than tall).
  PASS  [B002]
  PASS  [B003]
  PASS  [B004]
  PASS  [B005]

  Summary: 4 PASS / 1 WARN / 0 FAIL  →  WARN

======================================================================
TOTAL: 15 PASS / 5 WARN / 0 FAIL across 4 character(s)