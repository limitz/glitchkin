<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Doc Governance Tracker
## "Luma & the Glitchkin" — Production Document Audit

**Author:** Priya Shah, Story & Script Developer
**Created:** Cycle 47 (2026-03-30)
**Last Updated:** Cycle 48
**Trigger:** Reinhardt critique #6 — flagged 23 undocumented decisions and stale docs
**Primary readers:** Alex Chen, all team members

---

## Purpose

This document lists every production document in `output/production/` and `docs/`, its last known update cycle, and its staleness status. Documents not updated in 10+ cycles are flagged STALE. Documents that are one-time reference (specs, audits, reports) are marked REFERENCE — they are not expected to be updated but may contain outdated information.

Updated each cycle.

---

## Staleness Key

- **CURRENT** — updated within the last 10 cycles (C37+)
- **STALE** — not updated in 10+ cycles; may contain outdated information
- **REFERENCE** — one-time document (audit report, spec, brief); not expected to receive updates but flagged if content conflicts with current state
- **SUPERSEDED** — replaced by a newer version; kept for git history only
- **ACTIVE** — living document, updated regularly

---

## Production Documents (`output/production/`)

### Story Documents (`output/production/story/`)

| Document | Last Updated | Status | Owner | Notes |
|----------|-------------|--------|-------|-------|
| `story_bible_v005.md` | C46 | CURRENT / ACTIVE | Priya Shah | Canonical. FLAG 05 resolved, SF05/SF06 incorporated. |
| `story_bible_v004.md` | C43 | SUPERSEDED | Priya Shah | Use v005 |
| `story_bible_v003.md` | C39 | SUPERSEDED | Priya Shah | Use v005 |
| `story_bible_v002.md` | C38 | SUPERSEDED | Priya Shah | Use v005 |
| `story_bible_v001.md` | C37 | SUPERSEDED | Priya Shah | Use v005 |
| `pilot_episode_outline_v001.md` | C42 | CURRENT | Priya Shah | Scene-by-scene breakdown. No v002 needed yet. |
| `scene_handoff_briefs_v001.md` | C42 | CURRENT | Priya Shah | Per-scene storyboard execution briefs. |
| `pilot_cold_open_beat_outline_v001.md` | C46 | CURRENT | Priya Shah | Beat-by-beat breakdown P03-P24. |
| `cold_open_gap_log.md` | C48 | CURRENT / ACTIVE | Priya Shah | Persistent gap tracker. C48: P13/P20/P21 covered, Byte position resolved, 11 gaps remaining. |
| `LTG_glitch_appearance_guide.md` | C39 | CURRENT | Priya Shah | Staging reference for storyboarders. Still canonical. |
| `LTG_glitch_voice_direction.md` | C40 | CURRENT | Priya Shah | Quick-reference card. Still canonical. |
| `LTG_relationship_frame_brief.md` | C44 | CURRENT | Priya Shah | SF05 brief for Jordan Reed. |
| `LTG_miri_cultural_identity_brief.md` | C43 | CURRENT | Priya Shah | Miri heritage production decision. |

### Core Production Documents

| Document | Last Updated | Status | Owner | Notes |
|----------|-------------|--------|-------|-------|
| `production_bible.md` | C01 (Byte shape fix C38) | **STALE** | Alex Chen | Header says "Cycle 01." Content partially updated C38 (Byte oval fix) but version/status line never changed. Many decisions since C01 are not reflected. **HIGH PRIORITY for update.** |
| `ltg_pitch_brief.md` | Unknown (pre-C10) | **STALE** | Alex Chen | No cycle marker found. Likely very early. Core emotional pitch is still valid but asset references may be outdated. |
| `pitch_delivery_manifest.md` | C47 | CURRENT | Alex Chen / Priya Shah | Full asset reconciliation C47 by Priya Shah. File count ~50, resolution corrected to 1280x720, SF01-SF06 + GL Showcase listed, P03-P19 panels, motion specs. **ADDRESSED.** |
| `pitch_package_index.md` | C47 | CURRENT | Jordan Reed / Alex Chen | Extensively updated C47. All C47 deliverables tracked (GL Showcase, Cosmo visual hook, lineup v011, SF01 v007, Millbrook ENV, Miri motion v003, shoulder involvement, perspective rules). P1/P2 open items listed. **ADDRESSED.** |
| `naming_conventions.md` | C25 | **STALE** | Alex Chen / Kai Nakamura | Last content addition was C25 image size rule. Missing C38+ naming decisions. |
| `character_sheet_standards.md` | C30 | **STALE** | Maya Santos | Last updated C30. Missing Glitch motion spec (C45), face gate Byte profile (C45), face curves v1.1 (C41). |
| `fx_spec_cold_open.md` | Unknown (pre-C10) | **STALE** | Alex Chen | Early document. FX specs are detailed but do not reference any panels after the initial contact sheet. |
| `corruption_visual_brief.md` | C01 (v1.0) | **STALE** | Alex Chen | Version 1.0. Predates Glitch character canonization (C39) and all COVETOUS staging work. |
| `byte_float_physics.md` | C01 (v1.0) | **STALE** | Alex Chen | Version 1.0. Physics spec is still valid but does not reference Ryo Hasegawa's motion spec sheets or the motion_spec_lint tool. |
| `glitch_body_diamond_spec.md` | Unknown | REFERENCE | Alex Chen | Glitch body geometry. Still canonical per glitch.md. |
| `glitch_covetous_styleframe_spec.md` | Unknown | REFERENCE | Alex Chen | COVETOUS staging spec. May be partially superseded by Lee Tanaka C43 three-character triangulation. |
| `luma_face_curve_spec.md` | C40 | CURRENT | Kai Nakamura | Face curves canonical spec. |
| `luma_face_curve_spec_supplement_c40.md` | C40 | CURRENT | Maya Santos | Supplement expressions. |
| `face_test_gate_policy.md` | Unknown | REFERENCE | Alex Chen | Gate policy doc. |
| `staging_decision_register.md` | C47 | CURRENT / ACTIVE | Priya Shah | Created C47. Byte position decision (C48) should be added next update. |
| `doc_governance_tracker.md` | C47 | CURRENT / ACTIVE | Priya Shah | **This document.** |

### QA and CI Reports

| Document | Last Updated | Status | Notes |
|----------|-------------|--------|-------|
| `precritique_qa_c47.md` | C47 | CURRENT | Latest QA report |
| `precritique_qa_c46.md` | C46 | REFERENCE | Previous cycle report |
| `precritique_qa_c44.md` | C44 | REFERENCE | |
| `precritique_qa_c43.md` | C43 | REFERENCE | |
| `precritique_qa_c41.md` | C41 | REFERENCE | |
| `precritique_qa_c39.md` | C39 | REFERENCE | |
| `precritique_qa_c38.md` / `_baseline` | C38 | REFERENCE | |
| `precritique_qa_c37.md` | C37 | REFERENCE | |
| `precritique_qa_c36.md` | C36 | REFERENCE | |
| `precritique_qa_c35.md` | C35 | REFERENCE | |
| `precritique_qa_c34.md` | C34 | REFERENCE | |
| `ci_suite_c45_report.md` | C45 | REFERENCE | |
| `ci_suite_c39_report.md` | C39 | REFERENCE | |
| `ci_suite_c38_report.md` | C38 | REFERENCE | |
| `ci_suite_c37_report.md` | C37 | REFERENCE | |

### One-Time Specs and Briefs (REFERENCE)

| Document | Cycle | Notes |
|----------|-------|-------|
| `staging_briefs_c38.md` | C38 | Lee Tanaka staging briefs. Content still valid. |
| `sf02_staging_brief_c34.md` | C34 | SF02 Luma interiority. Still canonical for SF02. |
| `staging_brief_c42_p07_p09.md` | C42 | P07/P09 staging. Still canonical. |
| `staging_review_c47_sf06_p14_p15.md` | C47 | Lee Tanaka C47 review. Current. |
| `lineup_staging_brief_c42.md` | C42 | Two-tier ground plane decision. |
| `lineup_tier_depth_recommendation_c45.md` | C45 | Option C warmth bands. |
| `warm_cool_decision_c35.md` | C35 | Warm/cool pipeline decision. |
| `warm_cool_analysis_c35.md` | C35 | Supporting analysis. |
| `warm_cool_world_type_spec.md` | Unknown | World type classification. |
| `sf03_other_side_spec.md` | Unknown | SF03 spec. Still canonical. |
| `dual_miri_visual_plant_proposal_c38.md` | C38 | Miri name plant proposal. Executed. |
| `char_refinement_directive_c17.md` | C17 | **STALE** — C17 directive. FLAG 05 resolved C44; some directives may be outdated. |
| `expression_pose_brief_c34.md` | C34 | Expression/pose brief. |
| `sf02_face_review_c35.md` | C35 | Face review. |
| `sf02_face_implementation_notes_c35.md` | C35 | Implementation notes. |
| `rin_c23_creative_brief.md` | C23 | **STALE** — C23 brief, likely fully executed. |
| `ENV_REBUILD_SPEC_classroom_c41.md` | C41 | Classroom rebuild spec. Executed. |
| `ENV_REBUILD_SPEC_luma_study_c41.md` | C41 | Luma study rebuild spec. Executed. |
| `luma_v013_gaze_brief_c42.md` | C42 | Luma gaze spec. |
| `luma_silhouette_strategy.md` | Unknown | Silhouette strategy. |
| `byte_unguarded_warmth_body_spec.md` | Unknown | Byte body spec. |
| `stylization_preset_handdrawn.md` | Pre-C26 | **STALE** — stylization pipeline retired C26 per producer directive. |
| `miri_slipper_warmth_audit_c38.md` | C38 | Audit report. Executed. |
| `storyboard_naming_audit_c44.md` | C44 | Naming audit. |
| `native_resolution_audit_c42.md` | C42 | Resolution audit. |
| `corrupt_amber_fringe_spec.md` | Unknown | FX spec. Still canonical. |
| `fx_confetti_density_scale.md` | Unknown | FX density scale. |
| `color_statement_critique13.md` | C13 | **STALE** — C13 color statement. Historical reference only. |
| `ltg_typography_brief_display_typeface.md` | Unknown | Typography brief. |
| `draw_order_lint_back_pose_diagnostic_c36.md` | C36 | Diagnostic report. |

### Pitch Audits (Historical)

| Document | Cycle | Notes |
|----------|-------|-------|
| `pitch_readiness_c21.md` | C21 | **STALE** — 26 cycles old. Historical only. |
| `pitch_audit_cycle27.md` | C27 | **STALE** — historical. |
| `pitch_audit_cycle29.md` | C29 | **STALE** — historical. |
| `pitch_audit_cycle30.md` | C30 | **STALE** — historical. |
| `qa_report_cycle26.md` | C26 | **STALE** — historical. |
| `qa_report_cycle27.md` | C27 | **STALE** — historical. |
| `qa_c31_pitch_assets.md` | C31 | **STALE** — historical. |
| `proportion_audit_c31.md` | C31 | **STALE** — historical. |
| `proportion_audit_c36.md` | C36 | REFERENCE |
| `proportion_audit_c37.md` | C37 | REFERENCE |
| `proportion_audit_c39.md` | C39 | REFERENCE |
| `color_qa_c34_style_frames.md` | C34 | REFERENCE |
| `color_qa_c36_baseline.md` | C36 | REFERENCE |
| `color_qa_c37_baseline.md` | C37 | REFERENCE |
| `color_qa_c38_baseline.md` | C38 | REFERENCE |
| `color_verify_c32_spot_check.md` | C32 | REFERENCE |
| `color_continuity_c30.md` | C30 | **STALE** — historical. |
| `color_qc_c25_assets.md` | C25 | **STALE** — historical. |
| `sf01_v003_assessment.md` | Unknown | REFERENCE |

### Docs Directory (`docs/`)

| Document | Status | Notes |
|----------|--------|-------|
| `image-rules.md` | CURRENT | Core rule. Depth temperature rule added C45. Shoulder involvement rule added C47. |
| `work.md` | CURRENT | Team member work guide. |
| `ideabox.md` | CURRENT | Ideabox instructions. |
| `asset-status.md` | CURRENT | Asset status policy. |
| `critic-workflow.md` | CURRENT | Critic behavioral rules. |
| `pil-standards.md` | CURRENT | PIL coding rules. |
| `face-test-gate.md` | CURRENT | Face test gate procedure. |
| `reference_shopping_list.md` | C46 | CURRENT | Reference image shopping list. |

---

## Staleness Summary

| Priority | Document | Last Updated | Gap (Cycles) | Action Needed | Status |
|----------|----------|-------------|--------------|---------------|--------|
| **HIGH** | `production_bible.md` | C01 | 47 | Full update: Byte oval (done C38), Glitch character (C39), Miri heritage (C43), hairpin fix (C44), Cosmo visual hook (C47), shoulder involvement rule (C47), all C39+ decisions. Version should be 2.0+. | STILL STALE |
| ~~HIGH~~ | ~~`pitch_delivery_manifest.md`~~ | ~~C26~~ C47 | ~~21~~ 1 | ~~Update file list, counts, format~~ Full reconciliation completed C47 (Priya Shah). | **ADDRESSED C47** |
| ~~HIGH~~ | ~~`pitch_package_index.md`~~ | ~~C24~~ C47 | ~~23~~ 1 | ~~Massive update needed~~ Extensive update C47. All current assets tracked. | **ADDRESSED C47** |
| **MEDIUM** | `naming_conventions.md` | C25 | 23 | Missing post-C25 naming decisions. | STILL STALE |
| **MEDIUM** | `character_sheet_standards.md` | C30 | 18 | Missing Glitch motion spec, Byte face gate, face curves v1.1, shoulder involvement rule (C47). | STILL STALE |
| **MEDIUM** | `corruption_visual_brief.md` | C01 | 47 | Predates Glitch canonization (C39). | STILL STALE |
| **MEDIUM** | `fx_spec_cold_open.md` | Pre-C10 | 38+ | Early doc. Does not reference any post-contact-sheet panels. | STILL STALE |
| **LOW** | `char_refinement_directive_c17.md` | C17 | 31 | FLAG 05 resolved. Some directives may be stale. | STILL STALE |
| **LOW** | `stylization_preset_handdrawn.md` | Pre-C26 | 22+ | Pipeline retired. Could be archived. | STILL STALE |
| **LOW** | Historical audits (C21-C31) | Various | 17-27 | Historical. No action needed but should not be cited as current. | N/A |

**C48 assessment:** 2 of 3 HIGH-priority items addressed in C47. Remaining HIGH: `production_bible.md` (47 cycles stale — the single worst offender in the project). 5 MEDIUM items unchanged. Recommend Alex Chen prioritize `production_bible.md` in the next 1-2 cycles.

---

## Morgan Walsh CI Audit Integration (C47)

Morgan's `LTG_TOOL_doc_governance_audit.py` scanned 161 .md files. Key findings incorporated:
- **43 STALE files** (10+ cycles since last cycle reference)
- **58 NO_CYCLE_REF files** (no C<number> markers — some valid specs, some needing attention)
- Full automated report: `output/production/doc_governance_audit_c47.md`
- Tool available: `output/tools/LTG_TOOL_doc_governance_audit.py` (reusable, `--stale-threshold N`)

### Additional Stale Files from Morgan's Scan (not in manual audit above)

| File | Last Cycle | Gap | Notes |
|------|-----------|-----|-------|
| `output/storyboards/ep01_cold_open.md` | C3 | 44 | Original cold open. Predates all current panels. |
| `output/color/style_frames/sf02_color_notes.md` | C9 | 38 | SF02 completely rebuilt since C9. |
| `output/characters/main/byte.md` | C12 | 35 | Byte spec — 35 cycles stale. |
| `output/characters/color_models/luma_color_model.md` | C19 | 28 | Luma color model. |
| `output/color/palettes/LTG_COLOR_palette_audit_c23.md` | C22 | 25 | Palette audit. |
| `output/color/style_frames/LTG_COLOR_sf_final_check_c23.md` | C22 | 25 | SF final check. |
| `output/characters/main/cosmo.md` | No cycle ref | ? | Cosmo spec. |
| `output/style_guide.md` | No cycle ref | ? | Master style guide. |

---

## Update Log

| Cycle | Updates |
|-------|---------|
| C48 | C47 addressals checked. `pitch_delivery_manifest.md` and `pitch_package_index.md` both updated C47 — moved from HIGH STALE to CURRENT. 2 of 3 HIGH flags resolved. `production_bible.md` remains the worst offender (47 cycles stale). 5 MEDIUM flags unchanged. `image-rules.md` now includes Shoulder Involvement Rule (C47). `cold_open_gap_log.md` updated to C48. |
| C47 | Tracker created. Full audit of `output/production/` and `docs/`. 8 HIGH/MEDIUM staleness flags identified. Morgan Walsh CI audit data incorporated (43 STALE, 58 NO_CYCLE_REF). |

---

*Priya Shah — Story & Script Developer*
*Document: `output/production/doc_governance_tracker.md`*
*Updated each cycle.*
