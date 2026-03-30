========================================================================
LTG CI Suite v1.5.0 — Combined Report
Tools dir : /home/wipkat/team/output/tools
Fail-on   : FAIL
========================================================================
  ✓ [PASS ] Stub Integrity Linter
          142 file(s) — 0 PASS / 0 WARN / 0 ERROR
  ⚠ [WARN ] Draw Order Linter
          137 file(s) — 96 PASS / 41 WARN / 0 ERROR  [59 KNOWN]
  ⚠ [WARN ] Glitch Spec Linter
          21 Glitch generator(s) — 7 PASS / 14 WARN
  ✓ [PASS ] Spec Sync CI Gate
          5 character(s) — 0 P1 FAIL: none / 0 WARN: none
  ✓ [PASS ] Char Spec Linter
          3 character(s) — 0 PASS / 0 WARN / 0 FAIL
  ⚠ [WARN ] Dual-Output File Check
          30 KNOWN conflict(s) (all by-design) — 76 generator(s) involved
  ⚠ [WARN ] Hardcoded Path Check
          169 hardcoded /home/ occurrence(s) in 82 KNOWN file(s) (migration backlog — no new violations)
  ⚠ [WARN ] Thumbnail Lint
          67 .thumbnail() call(s) in 62 KNOWN generator(s) (migration backlog — no new violations)
  ⚠ [WARN ] Motion Sheet Coverage
          1 character(s) missing motion sheet: grandma_miri

  ⚠ OVERALL: WARN  (exit code 0)  (59 KNOWN issues annotated)
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