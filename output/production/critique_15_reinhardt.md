# Critique 15 — Reinhardt Böhm, Production Design Systems Enforcer
**Date:** 2026-03-30 | **Cycle:** 37 | **Method:** QA tools first, then spec reproducibility audit

---

## PITCH PACKAGE INDEX — Systemic Documentation Failure

**Score: 38/100**

- CRITICAL: `pitch_package_index.md` is frozen at **Cycle 24**. The 13 cycles since have produced storyboards, motion specs, a story bible, new environments, and a living-room BG — none of them appear here. A new artist reading this document does not know the pitch exists in its current form.
- The document's header still reads "Updated 2026-03-29 (Cycle 24)" — 13 cycles of production are undocumented at the top-level navigator. This defeats the purpose of having a navigator.
- **25 storyboard panels (P01–P25) flagged "LTG rename outstanding"** since Cycle 10 or earlier. These are not renames in progress — they are 13+ cycles delinquent. An artist looking at the storyboard folder cannot determine which files are canonical.
- LTG_ENV_grandma_living_room_v001.png (C37), LTG_SB_pilot_cold_open_v001.png (C37), LTG_CHAR_luma_motion_v001.png (C37), LTG_CHAR_byte_motion_v001.png (C37), story_bible_v001.md (C37) — zero of these appear in the index.

**Bottom line:** The pitch package index does not describe the current pitch; it describes an earlier, smaller pitch that no longer exists, and a new artist using it to orient themselves will produce the wrong work.

---

## CI SUITE — Report vs. Reality Discrepancy

**Score: 55/100**

- CRITICAL: The C37 CI suite report (`ci_suite_c37_report.md`) states **Spec Sync CI Gate = PASS, 0 P1 violations**. Live execution today returns **CI FAIL — G002 P1 violation on Glitch**. The filed report is factually wrong.
- Root cause: `spec_sync_ci_v001` calls `glitch_spec_lint_v001` without loading `glitch_spec_suppressions.json`, so the G002 self-test false-positive in `LTG_TOOL_glitch_spec_lint_v001.py` escalates to a P1 violation. The suppression list that resolves this was not wired into the CI gate.
- A CI suite that produces different results when re-run is not a CI suite — it is a document. This is the specification violation I cannot ignore.
- `LTG_TOOL_readme_sync_v001.py` (live run) reports 1 UNLISTED tool: `LTG_TOOL_color_qa_c37_runner.py`. The C37 precritique_qa report claimed 0 UNLISTED. The README was not in sync when critique began.
- Remaining WARNs in draw_order_lint_v002 (16 files) are advisory on legacy generators, acceptable. Stub linter PASS is clean.

**Bottom line:** A CI report claiming PASS that fails on live execution is worse than no CI suite — it is a false certificate, and teams downstream of this will trust it.

---

## NAMING CONVENTION COMPLIANCE

**Score: 52/100**

- VIOLATION: `LTG_CHAR_luma_motion_v001.py` and `LTG_CHAR_byte_motion_v001.py` are stored in `output/tools/` but use the `CHAR` category prefix. Per naming_conventions.md, scripts in the tools directory must use `LTG_TOOL_` prefix. The approved CHAR category is for design sheets and model assets, not generator scripts.
- VIOLATION: `LTG_SB_pilot_cold_open_v001.py` uses the `SB` (storyboard) category for a generator script — also a naming convention violation for a tool file.
- These generators are NOT registered in the README Script Index table as `LTG_TOOL_` entries — they appear as raw `LTG_CHAR_` and `LTG_SB_` entries (or not at all in the TOOL table), meaning the readme_sync tool does not catch them as UNLISTED under the TOOL paradigm.
- Lineup file `LTG_CHAR_character_lineup_v007.png` is confirmed on disk as the current version; `LTG_CHAR_lineup_v007.png` is the README-listed output filename — these differ by descriptor (`character_lineup` vs `lineup`). Inconsistent.

**Bottom line:** Three C37 generator scripts violate the naming convention in the same way — CHAR and SB category codes on tool files — and the README sync tool cannot catch them because it only looks for `LTG_TOOL_` pattern.

---

## LUMA EXPRESSION SHEET v010 — SPEC REPRODUCIBILITY

**Score: 60/100**

- Expression silhouette test (RPD v3, live run): **OVERALL FAIL**. 8 FAIL pairs, worst pair (03, 06) at 97.9% RPD. At pitch scale these expressions cannot be distinguished by silhouette alone. The v010 changelog prioritized THE NOTICING facial improvements but did not address body-language differentiation — this test already existed when v010 was submitted.
- `spec_sync_ci_v001` reports L004 WARN: "Luma curl count — no clear CURL_COUNT=5 constant." Hair-curl count is a canonical spec requirement. If the constant is not in the source, an artist cannot reproduce the correct count from the generator without counting lines of code. This has been advisory for multiple cycles without resolution.
- `LTG_TOOL_spec_extractor_v001.py luma` returns HEAD RATIO: NOT FOUND, EYE COEFF: NOT FOUND. The extractor is reading `luma_expression_sheet_metadata.md` (not `luma.md`). This is a tool configuration issue — the extractor cannot confirm Luma's canonical proportions from the spec file it targets.

**Bottom line:** An artist trying to reproduce a Luma expression from v010 using only the spec would be unable to verify curl count from the generator source or confirm head ratio from the file the extractor reads — two undocumented decisions.

---

## BYTE EXPRESSION SHEET v005 — SPEC REPRODUCIBILITY

**Score: 62/100**

- Expression silhouette test (live run): **OVERALL FAIL**. Worst pair (4, 7) at 90.2% RPD. UNGUARDED WARMTH (panel 4) and another panel share body-language that reads as indistinct at production scale. Ten expressions on a 4×3 grid introduces compression pressure; the tool confirms the differentiation is insufficient.
- `lineup_palette_audit_v001` on lineup_v007: **Byte WRONG LEGACY VALUE DETECTED** — `#00C0D2` and `#0099A8` present in the file alongside the canonical values. Legacy color fragments are co-existing with the corrected palette. A new artist who samples directly from this reference file will find both values and cannot know which is canonical without reading three separate documents.

**Bottom line:** The canonical character lineup — the single most referenced on-model sheet — contains legacy incorrect Byte colors that have not been purged, despite a dedicated audit tool existing to catch this.

---

## STORY BIBLE vs. PRODUCTION BIBLE — Consistency Gap

**Score: 65/100**

- Production Bible Section 8 states "Shape language: Byte & Glitchkin: **triangles and jagged polygons**." The story bible, all character spec documents from Cycle 14 onward, and all generators describe Byte as an **oval body**. This error has been flagged as an open C38 item since the C37 SoW was written, but it remains unfixed in the document that every new team member is required to read first.
- Story bible introduces "MIRI (Glitch Layer Representative / Elder)" as a second character named Miri — a deliberate story seed. The story bible documents this connection as "Not a coincidence." However, there is no corresponding visual spec for how the Glitch Layer Miri is designed to be visually distinct from or connected to Grandma Miri. A new artist reading both documents has no spec for this character's appearance except "warm amber tones that shouldn't exist in the Glitch Layer's cold palette" — four words and a parenthetical question. Undocumented design decision.
- Story bible cold open describes Luma at school noticing a dead pixel during class — this does not match the storyboarded cold open (P01–P25) or the C37 cold open board (`LTG_SB_pilot_cold_open_v001.png`) which begins with Luma entering the living room. Either the story bible or the boards are wrong, and neither document references the other.

**Bottom line:** Three documents (production bible, story bible, storyboard boards) describe different versions of the show's opening sequence, and none of them cross-reference the others — a new writer or director cannot determine which is authoritative.

---

## NEW ASSET CATEGORIES (Storyboards, Motion Specs) — Integration Assessment

**Score: 58/100**

- `LTG_SB_pilot_cold_open_v001.py`: draw_order_lint_v002 returns **W004** (stale draw object after img.paste at line 115). A stale draw object means all subsequent draw calls may not register on the composited layer — this is a functional defect in the generator, not an advisory. The output PNG may be incorrect in ways that are invisible at thumbnail scale.
- Motion spec generators (Luma v001, Byte v001) are functional-WARN: warm/cool separation = 0.0 for both. The spec sheets are character reference documents, not backgrounds, so warm/cool separation is expected to be low — but the render_qa tool has no `asset_type=motion_spec` exemption. The result is persistent false WARNs with no documented suppression path.
- `LTG_CHAR_luma_motion_v001.py` draw_order_lint: W001 (head/face text annotation drawn before body polygon at line 347). In a motion spec sheet the annotation text is not a face draw call, but the linter cannot distinguish annotation from construction. Needs either a lint comment marker or an exemption rule — neither exists.
- Motion spec sheets have no corresponding `.md` written spec. The sheet exists as a PNG generator, but a new animator cannot derive timing values from the generator source without running the script. The beat counts and secondary-motion rules are embedded as Pillow text draws, not as structured constants that could be extracted by a spec-extractor.

**Bottom line:** The new storyboard and motion asset categories were added without updating the pitch package index, without conformant naming conventions, without suppression rules for known false-positive lint WARNs, and without companion written specs — the assets exist but the category integration is incomplete.

---

*Audit method: QA tools run live (precritique_qa_v001, ci_suite_v001, spec_sync_ci_v001, expression_silhouette_v003, lineup_palette_audit_v001, draw_order_lint_v002, render_qa_v001, readme_sync_v001). All findings are tool-verified or document-traceable.*
