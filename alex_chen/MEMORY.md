# Alex Chen — Memory

## README Introduction (post-Cycle 21)
- Added 4-paragraph first-person intro section to README.md directly below the logo. Covers: Alex Chen as AI Art Director, project premise (Luma/Glitchkin/CRT TV/comedy-adventure), agentic team structure (6 roles, inbox-driven, PIL generators in output/tools/), iterative process (work cycles → critique cycles → feedback loop). Archived: 20260329_1424_readme_changes.md + all 4 C21 completion reports (bg/char/color/tech).

## Cycle 21 State (current)

**Cycle 21 tasks completed (this cycle):**
- **Alex (self):** Confirmed Kai Nakamura's inbox assignment exists (`kai_nakamura/inbox/20260330_0200_cycle21_tasks.md`). Spot-checked all 9 key pitch assets — all present on disk. Wrote `output/production/pitch_readiness_c21.md` (overall: CONDITIONALLY READY). Archived all C20 completion reports + rehire message + C21 tasks message. Updated MEMORY.md.

**Team change — Cycle 21:**
- Lee Tanaka: DEACTIVATED (storyboard decks complete, Critique 10 prep)
- Kai Nakamura: ACTIVE (new — Technical Art Engineer). First cycle: build `output/tools/ltg_render_lib.py` shared rendering library, apply to at least one generator as proof of concept.

**Pitch readiness summary (Cycle 21):**
- Overall: CONDITIONALLY READY for Critique 10
- Top 3 assets: SF03 v003 (strongest — visual identity statement), Grandma Miri expression sheet v002 (biggest single-cycle leap), Act 2 contact sheet v006 (proves the show has a story arc)
- Risk 1 (LOW-MED): SF02 window pane alpha 160–180 (target 90–110) — mitigation is a single v005 pass if critics flag it
- Risk 2 (MEDIUM): No standalone one-page pitch brief — production bible covers it but not in buyer-facing format
- Lead-with-5 for pitch: SF01 v003 → SF03 v003 → Act2 contact sheet v006 → SF02 v004 → Miri expression sheet v002

**Next: Critique 10** (this cycle, after Kai's work is committed)

---

## Cycle 20 State (archived)

**Cycle 20 tasks completed (this cycle):**
- **Alex (self):** Wrote ROLE.md for all 5 team members (alex_chen, maya_santos, jordan_reed, sam_kowalski, lee_tanaka). Updated pitch_package_index.md with all C19 deliverables. Archived all C19 completion reports and roles/cycle20 tasks messages.

**C20 incoming (not yet indexed — arrived this cycle):**
- **Sam Kowalski:** SF03 v003 VERIFIED — GL-01b confirmed, BYTE_GLOW discrepancy closed as acceptable, color narrative passes, CLEAR for Critique 10. SF02 v004 CONDITIONALLY READY — storefront geometric confirmed, glow cones alpha 90–110 correct, window pane rects at alpha 160–180 (not blocking — pane vs glow distinction). Note: if critics flag panes, v005 fix is alpha 100/90.
- **Lee Tanaka:** Act 2 contact sheet v006 (A2-02 v002 incorporated, arc label updated to "VULNERABLE (RESIGNED-55%)"). Act 1 full contact sheet v001 (5 panels: cold open A1-01–A1-04 + classroom NEAR-MISS with scene-break border).
- **Jordan Reed:** Tech Den v002 — window light shaft (trapezoid SUNLIT_AMBER, feathered, dust motes seed 77), monitor glow spill on desk/chair/shelving (RGB 180,200,210 — zero Glitch palette), right-half bedding/pillows/poster/printouts/device added, Cosmo jacket RW-08 Dusty Lavender clearly rendered.

**Open pitch package index items (C20 deliverables not yet added):**
- Act 2 contact sheet v006 — LTG_SB_act2_contact_sheet_v006.png
- Act 1 full contact sheet v001 — LTG_SB_act1_full_contact_sheet_v001.png
- Tech Den v002 — LTG_ENV_tech_den_v002.png
- SF03 v003 color review updated (final verified)
- SF02 v004 color notes updated (conditional ready, window pane note on record)

**Next critique:** Critique 10 (after Cycle 21 — one cycle away)

---

## Cycle 19 State (archived)

**Cycle 19 assignments dispatched (this cycle):**
- **Alex (self):** Translated Critique 9 findings into four team inbox messages. Updated production_bible.md v4.0 with Section 12 (permanent record of SF03 Void Black spec violation). Archived critique summary + all C18 completion reports.

**Cycle 19 open work (awaiting team delivery):**
- **Jordan Reed:** SF03 v003 (Byte body GL-01b fix + eye radius + magenta slash removal), SF02 v004 (storefront = shattered window, window glow = per-window downward cone at alpha 80–100), School Hallway v002 (artifact + human evidence + low camera), Millbrook v002 (power lines perspective + sag + varied weight, road plane + center line)
- **Maya Santos:** Miri expression sheet v002 REBUILD (5 full-body expressions with body posture + hands; replace NOSTALGIC with SKEPTICAL/AMUSED), Luma expression sheet v003 DELIGHTED fix (arms raised + bounce on toes + forward lean), Cosmo expression sheet v003 SKEPTICAL lean formula fix (tilt_off multiplier 0.4 → 2.5)
- **Sam Kowalski:** SF03 v003 color review (Byte body GL-01b confirm, eye contrast ≥4.5:1 cyan, ≥3.0:1 magenta), hoodie base color reconcile (#E8722A luma_color_model.md vs #E8703A master_palette.md canonical), SF02 v004 warm/cool balance review
- **Lee Tanaka:** A1-03 v002 rebuild (MCU, CRT-lit face below-left, legible pixel shapes on screen, caption "Discovery"), A2-08 v002 camera fix (Luma POV eye-level OR two-shot, no low angle), NEW panel A2-07b (kitchen doorway bridging shot — Miri silhouette, warm light behind), Act 2 contact sheet v005

**Sam dependency on Jordan:** Sam cannot start SF03 or SF02 reviews until Jordan delivers v003/v004. Sam can start hoodie reconciliation immediately.

**Critique 9 critical findings (permanent):**
- SF03 BYTE BODY = VOID BLACK (10,10,20) — spec violation, body invisible on UV Purple. Fixed in C19. Documented in production_bible.md Section 12.
- SF02 storefront still HUD-read (C+, 3 cycles unresolved), window glow left-edge gradient still wrong (D, 4 cycles)
- Miri sheet face-only, no body language — C. Rebuild assigned.
- Luma DELIGHTED/SURPRISED squint fail — body must differentiate
- Cosmo SKEPTICAL lean formula produces 2.4px (invisible) — multiplier fix assigned
- A1-03 compositionally passive — MCU rebuild assigned
- A2-08 wrong camera grammar (low angle) — intimacy fix assigned
- A2-07→A2-08 hard cut across settings — new bridging panel A2-07b assigned

**What's working (C9 positives):**
- SF03 atmospheric perspective: correct
- Act 2 arc: Carmen A- — coherent, color-coded, structurally complete
- A2-01 vs A2-07 cohesion: Carmen A-
- Luma cold overlay (Sam C18): Naomi A-
- Master palette Act 2 (Sam C18): Naomi A

**Next critique:** Critique 10 (after Cycle 21, i.e., every 3 cycles from C18 → C21)

---

## Cycle 18 State (archived)

**Cycle 18 work completed (this cycle):**
- **Alex (self):** README logo moved to top (Task 1). Pitch package index updated with all C16 + C17 assets (Task 2). SF02/SF03 pre-critique assessment written: `output/production/sf02_sf03_precritique_c18.md` (Task 3). All C17 completion reports archived.

**Also received C18 Maya Santos report:** A2-02 Byte RESIGNED MCU v002 delivered (`LTG_SB_act2_panel_a202_v002.png`). 55% aperture (transitional), parabolic droopy lid, downcast pupil +7px, ↓ pixel glyph, transitional arm posture. Added to pitch package index under C18 additions.

**Key index additions (C16+C17):**
- Section 1.3: Luma expression sheet v002 (refined, C17), Grandma Miri expression sheet v001 (C17, closes CRITICAL gap)
- Section 1.4: Grandma Miri color model v001 (23 swatches, C17)
- Section 1.5: Tech Den v001 (C17), School Hallway v001 (C17), Classroom v002 (C16), Miri's Kitchen v001 (C16)
- Section 1.6 (via C16 additions): SF02 v003 (Takeshi fixes), SF03 v002 (Takeshi+Naomi fixes)
- Character sheets: Byte v002 re-regen (RESIGNED eye fix), Cosmo v002 (SKEPTICAL lean + WORRIED/SURPRISED), Luma Act2 pose v002 (mitten hand)
- Storyboard: A2-07 real panel, A2-03 restage, A2-06 MED, A2-04 Byte added, contact sheet v003 (C16), A2-01/A2-05/A2-08, contact sheet v004 (C17)
- Section 3.5 (new): Production standards doc (char_refinement_directive_c17.md)

**SF02/SF03 pre-critique summary (for Critique 9):**
- SF02 v003: Dutch angle ✓, DRW-07 ✓, storm building lighting ✓, ENV-06 ✓. RISKS: storefront lower-right element (Victoria P1, unconfirmed fixed), warm window glow still absent (emotional anchor invisible). Expect ~B+ if storefront clean.
- SF03 v002: Waterfall luminance ✓, slab variety/bridging ✓, DRW-18 hair rim ✓. RISKS: Byte dual-eye legibility (high), Luma silhouette density (moderate), pixel plant visibility (moderate). Expect ~B+ if Byte eyes read.
- **Most likely C9 critics for SF02/SF03:** Victoria Ashford, Naomi Bridges, Dmitri Volkov, Takeshi Murakami, Aisha Okafor.

**Next critique:** Critique 9 (after Cycle 18).

## Cycle 17 State (archived)

**Cycle 17 work completed (this cycle):**
- **Alex (self):** Read all main character sheets (luma.md v2.0, cosmo.md v2.0, byte.md v3.2, grandma_miri.md v1.2). Reviewed all PNGs in output/characters/. Reviewed critic feedback cycles 8 and 15. Wrote `output/production/char_refinement_directive_c17.md`. Archived both producer inbox messages.

**Directive summary:**
- Defines "refined" for LTG: construction clarity, 3-tier line weight (3/2/1px), thumbnail expression readability, on-model consistency, emotional triangle (eyes+mouth+body).
- **Gap 1 (CRITICAL):** No expression sheet for Grandma Miri. Blocks Act 2 performance quality and pitch package completeness.
- **Gap 2 (CRITICAL):** Line weight undifferentiation across expression sheets — producer concern root cause. 3-tier weight not consistently enforced as visibly distinct.
- **Gap 3 (SIGNIFICANT):** Luma Act 2 standing pose -5° lean imperceptible; turnaround not reconciled with Act 2 pose.
- **Maya Santos C17 assignments:** (1) Miri expression sheet — 6 expressions, LTG_CHAR_miri_expression_sheet_v001.png; (2) Line weight audit and fix pass on all existing expression sheet tools; (3) Luma Act 2 pose lean fix to -8°.

**Directive sent to Maya Santos inbox:** `maya_santos/inbox/20260329_2115_char_refinement_directive_c17.md`. Lee and Jordan streams continue independently (Act 2 panels, environments).

**Next critique:** Cycle 18 (next cycle after 17).

## Cycle 16 State (archived)

**Cycle 16 completed work (mid-cycle):**
- **Maya Santos DONE:** Byte RESIGNED right eye fixed (45% aperture, +10px downcast pupil, parabolic lid droop, body_tilt +14°). Cosmo SKEPTICAL lean +6° added, 2 new expressions (WORRIED, SURPRISED) added — sheet now 6/6. Luma Act 2 pose mitten geometry corrected. New files: `LTG_CHAR_byte_expression_sheet_v002.png` (regen), `LTG_CHAR_cosmo_expression_sheet_v002.png`, `LTG_CHAR_luma_act2_standing_pose_v002.png`.
- **Sam Kowalski DONE:** BYTE_SH shadow corrected to GL-01a `(0,168,192)`. BG_ALARM corrected to cold `(18,28,44)`. Faceplate sizing made proportional. DRW-07 `DRW_HOODIE_STORM` corrected to `(200,105,90)`. ENV-06 verified correct. SF03 color review notes sent (see inbox archived). DRW-18 hair sheen present in generator but thin — Jordan to amplify.
- **Lee Tanaka UNBLOCKED:** A2-07 confirmed unblocked. Notified via inbox.
- **Jordan Reed IN PROGRESS:** SF02 v003, SF03 v002, Classroom v002, Grandma Miri's Kitchen — SF03 color notes relayed. DRW-07 fix confirmed in SF02 v002 generator before Jordan's v003 regen.
- README.md updated for Cycle 16 with ASCII art and visual language swatch.
- Next critique: Cycle 18.

**Open items still awaited:**
- Jordan: SF02 v003, SF03 v002, Classroom v002, Kitchen v001
- Lee: A2-07, A2-03 restage, A2-06 MED two-shot, A2-04 Byte addition, contact sheet v003

## Cycle 15 Lessons
- **RESIGNED expression delivered:** `LTG_TOOL_byte_expression_sheet_v002.py` adds 8th expression. Key distinctions: `↓` pixel symbol (distinct from flat-line NEUTRAL), `droopy_resigned` right eye (NO suppressed smile, downcast pupil — distinct from RELUCTANT JOY's `droopy`), arms arm_x_scale=0.50 (tighter than NEUTRAL 0.75), body_tilt=+8 (backward avoidance lean). A2-02 no longer blocked. Lee Tanaka notified.
- **SF03 already complete:** Jordan Reed's `LTG_TOOL_style_frame_03_other_side_v001.py` was built this cycle (Cycle 15 per README) — full generator including characters and lighting overlay. `LTG_COLOR_styleframe_otherside_v001.png` exists. All 3 style frames now pitch-ready. Task was to "check if BG ready and composite" — BG existed AND Jordan's full tool already handled the composite. My role: verify, register, update index.
- **Pitch package index updated through Cycle 15:** All Cycle 13/14/15 additions documented. Style frames now COMPLETE (was PARTIAL). Byte.md now v3.2 (was incorrectly listed as v3.1 with header note). Open blockers revised.
- **Tools README:** `LTG_TOOL_byte_expression_sheet_v002.py` registered. Jordan's SF03 tools were already registered.
- **droopy vs droopy_resigned:** `droopy` = RELUCTANT JOY (lower-lid smile crinkle present). `droopy_resigned` = RESIGNED (no crinkle, pupil fully downcast, heavier lid 50% vs 55%, shorter highlight). Must never be confused — one suppresses joy, the other has surrendered.
- **Sam Kowalski SF03 color notes:** Requested for Cycle 16 review. Five questions: UV purple ambient read, inverted atmos perspective, Byte eye pair legibility, confetti density, abyss below platform.

## Cycle 14 Lessons
- **Byte float-gap dimension arrow (Dmitri P1 — RESOLVED):** Replaced Cycle 12 "ground floor." caption with a proper engineering dimension arrow in `LTG_TOOL_character_lineup_v003.py`. Two-headed vertical arrow (GROUNDFLOOR_COL), horizontal serif ticks at each tip, "0.25 HU" label beside shaft. Arrow positioned at `byte_cx + body_rx + 10`. Output: `LTG_CHAR_lineup_v003.png`.
- **Misnamed tools corrected:** `LTG_CHAR_luma_expression_sheet_v002.py` → `LTG_TOOL_luma_expression_sheet_v002.py` (note added in header). `bg_glitch_layer_encounter.py` → `LTG_TOOL_bg_glitch_layer_encounter_v001.py` (moved to tools/). Both originals retained per version preservation policy.
- **Glitch Layer frame canonical:** `LTG_ENV_glitchlayer_frame_v001.png` = CANONICAL (81,483 bytes, Cycle 11 regen). `v002` = archive copy (80,664 bytes, older render). Documented in compliance checklist.
- **SF03 spec written:** `/output/production/sf03_other_side_spec.md` — full generator spec for Jordan Reed. Five depth layers, all RGB values, lighting setup, draw order, validation checklist. Jordan notified via inbox. Key rule: NO warm light (inverted atmospheric perspective — purple gets darker with distance, not lighter).
- **SF01 v003 assessment:** Ghost Bytes at alpha 90/105 — A+, pitch-ready. Top-left monitor relocation confirmed correct (warm lamp bleed zone clean). SF01 v003 LOCKED as canonical Discovery style frame.
- **Compliance checklist updated:** Cycle 14 pass documented — all tool renames, glitch layer frame canonicalization, and lineup generator correction noted.

## Cycle 13 Lessons
- **Ghost Byte alpha fix (SF01 v003):** Body alpha 55→90, eye glints 65–70→105. Top-left monitor removed (warm lamp bleed kills contrast). Two ghosts (top-right + mid-left) instead of three. Victoria B+→A+ calibrated. Output: `LTG_COLOR_styleframe_discovery_v003.png`.
- **Asymmetric logo v002:** "&" now warm-to-cold gradient (SUNLIT_AMBER left → ELEC_CYAN right) via per-column alpha composite. "the/Glitchkin" gap reduced 30% (int(H*0.04)→int(H*0.028)). Output: `LTG_BRAND_logo_asymmetric_v002.png`.
- **SF02 character composite v002:** Byte hovering LEFT (~28%), Luma CENTER (~45%), Cosmo RIGHT (~62%). Byte = VOID_BLACK body (storm variant, intentional). CORRUPT_AMBER outlines on all characters for figure-ground. char_h raised to 18% from 15%. Dutch angle still applied last. Output: `LTG_COLOR_styleframe_glitch_storm_v002.png`.
- **Byte cracked-eye glyph:** 7×7 dead-pixel pattern with diagonal crack fracture. Dead zone upper-right, alive zone lower-left, Hot Magenta crack line. Reference PNG at 4 scales + in-eye mockups. Documented in byte.md Section 9B. Lee Tanaka notified. Output: `LTG_CHAR_byte_cracked_eye_glyph_v001.png`.
- **BRAND ratified, COL retired:** naming_conventions.md updated to v1.1. BRAND = show logos/identity. COL was never valid — use COLOR only. Compliance checklist updated.
- **Byte storm-scene variant (Naomi flag resolved):** VOID_BLACK body in SF02 is INTENTIONAL — Byte consumed by Void/Corruption during storm. Visible only by CORRUPT_AMBER outline. Narrative color statement. Documented in byte.md Section 13A.
- **byte.md version 3.2:** Sections 9B (cracked-eye glyph) and 13A (storm-scene variant) added. Version header and colophon updated.
- **.gitignore added:** `/home/wipkat/team/.gitignore` with `__pycache__/` and `*.pyc`. Resolves JT P2 flag.
- **TERRACOTTA_CYAN_LIT color fix (Jordan Reed ENV-06):** SF02 v002 script had TERRA_CYAN_LIT=(154,140,138) — wrong (reads warm grey, G<R). Corrected to (150,172,162): G=172>R, B=162>R — reads cyan-tinted. Script edited inline; output regenerated (248,858 bytes).
- **CHAR-L-11 registered (Sam Kowalski request):** Warm-side hoodie pixel activation = #E8C95A (Soft Gold). Registered as CHAR-L-11 (not CHAR-L-09b — shoe canvas slot kept). Message sent to Sam to add to master_palette.md.

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
