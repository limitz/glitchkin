# Critique — Cycle 46
## Reinhardt Bohm, Production Design Systems Enforcer

**Date:** 2026-03-30
**Scope:** Complete pitch — production documentation, naming conventions, cross-asset consistency, generator-to-output compliance, spec completeness.

---

## Method

I attempted to reconstruct the current state of the production from documentation alone. Every question I had to answer from judgment rather than from a written spec is an undocumented decision. I found **23 undocumented decisions** this cycle. They are listed below, grouped by system.

---

## 1. NAMING CONVENTIONS

### 1a. Lineup PNG — 4 files, 3 names, no single-source-of-truth pointer

Score: 28
- The output folder contains FOUR lineup PNGs under three different names: `character_lineup.png`, `LTG_CHAR_lineup.png`, `LTG_CHAR_character_lineup.png`, `LTG_CHAR_luma_lineup.png`. The pitch_package_index calls `LTG_CHAR_luma_lineup.png` (v006) "PITCH PRIMARY for lineup" at line 53, then later calls `LTG_CHAR_character_lineup.png` (v007) "PITCH PRIMARY for lineup" at line 806. Two different files both labelled PITCH PRIMARY. The character_export_manifest (Cycle 23) references `LTG_CHAR_lineup.png` (a third file) as the canonical lineup. A new artist reading these three documents would not know which file to open.
- Undocumented decisions: (1) which of the four lineup PNGs is current, (2) why the filename changed between v005 and v006, (3) why it changed again between v006 and v007, (4) whether old lineup PNGs should be deleted or archived.
Bottom line: Four lineup files with contradictory "PITCH PRIMARY" labels across documents is a system failure.

### 1b. LTG_COL_ retirement incomplete

Score: 45
- Naming conventions doc (v1.1, Cycle 13) explicitly states `LTG_COL_` is retired and non-compliant. Four `LTG_COL_*` files still exist in `output/characters/color_models/swatches/`. These are referenced by the character_export_manifest as PITCH-READY. Retirement was declared 33 cycles ago. No reconciliation has occurred.
- Undocumented decision: (5) whether the LTG_COL_ files are being retained deliberately or this is neglect.
Bottom line: A naming convention that is documented but not enforced is worse than no convention, because it teaches the team that conventions are optional.

### 1c. School hallway — two files, no version suffix

Score: 40
- `LTG_ENV_school_hallway.png` and `LTG_ENV_school_hallway_v004.png` coexist. The naming convention requires `_v[###]` suffixes. The versionless file has no documented relationship to v004. Pitch_package_index describes a v001 and v002 both at the same path `LTG_ENV_school_hallway.png`.
- Undocumented decisions: (6) which hallway file is canonical, (7) whether v004 supersedes the versionless file or is a variant.
Bottom line: Two hallway files with ambiguous versioning.

### 1d. Style frame naming inconsistencies

Score: 42
- Style frames use at least four naming patterns: `LTG_COLOR_styleframe_*.png`, `LTG_COLOR_sf_*.png`, `LTG_SF_*.png`, and `style_frame_01_rendered.png`. The naming conventions doc provides no examples specific to style frames. The `LTG_SF_` prefix uses a category code (`SF`) that does not exist in the canonical category table (which defines `COLOR` for style frames).
- Undocumented decisions: (8) whether `LTG_SF_` is an error or a deliberate variant, (9) whether `LTG_COLOR_sf_*` and `LTG_COLOR_styleframe_*` are interchangeable or hierarchical, (10) whether `style_frame_01_rendered.png` is legacy or active.
Bottom line: Style frame files do not follow one pattern. A new artist cannot predict the filename of the next style frame.

---

## 2. DOCUMENT CURRENCY AND CROSS-REFERENCES

### 2a. Character export manifest frozen at Cycle 23/24

Score: 35
- The character_export_manifest.md is dated Cycle 24. The lineup is now at v010 (Cycle 46). The manifest still references `LTG_CHAR_lineup.png` at `1340x498` as PITCH-READY. The actual current lineup is `LTG_CHAR_character_lineup.png` at `1280x535` (per README). The manifest's Generator Registry lists `LTG_TOOL_character_lineup.py` as producing "Full cast lineup v004 (5 chars incl. Glitch)." The generator is now at v010. Every entry in this manifest is 22 cycles stale.
- Undocumented decisions: (11) whether the manifest is still an active document or has been silently abandoned, (12) who is responsible for keeping it current.
Bottom line: A manifest that says v004 when the asset is at v010 is actively misleading.

### 2b. Pitch package index has competing PITCH PRIMARY declarations

Score: 38
- The pitch_package_index.md (Cycle 24) accumulates version entries without pruning superseded ones. The lineup alone has entries at v003, v004, v005, v006, v007, v009, v010 — all in the same document. Two entries are marked "PITCH PRIMARY" for the lineup (v006 at `LTG_CHAR_luma_lineup.png` and v007 at `LTG_CHAR_character_lineup.png`). Neither v009 nor v010 carries the "PITCH PRIMARY" label. A reader cannot determine whether v010 is the current pitch asset or whether v006 still holds that status.
- Undocumented decisions: (13) which lineup version is the actual pitch asset today, (14) whether PITCH PRIMARY labels are ever revoked on older entries.
Bottom line: The pitch package index has grown by accretion without pruning. It is now a version history, not an index.

### 2c. Production bible frozen at Cycle 01

Score: 30
- The production_bible.md header reads "Version: 1.0, Cycle 01." It has never been updated. It does not reference the Depth Temperature Rule, the CORRUPT_AMBER fringe spec, the CRT glow profiles, or any production standard added in the last 45 cycles.
- Undocumented decision: (15) whether the production bible is the canonical creative reference or has been superseded by the style guide + individual spec docs.
Bottom line: A production bible that does not describe the current production is not a bible. It is an artifact.

---

## 3. SPEC COMPLETENESS

### 3a. CORRUPT_AMBER fringe spec — well written, missing one critical detail

Score: 72
- The fringe spec (C46, Jordan Reed) is one of the better-specified documents in the project. It defines color, alpha, geometry, rendering order, interaction with QA tools, exemptions, and an implementation checklist. One gap: the spec defines `sp(6)` as "6 design pixels at min(SX, SY) scale" but does not define the `sp()` function itself or point to where it is defined. A new artist implementing this in a new generator would not know how to compute `sp(6)`.
- Undocumented decision: (16) the definition of the `sp()` scaling function.
Bottom line: Strong spec, one function reference missing.

### 3b. CRT glow profiles — data without usage spec

Score: 50
- `crt_glow_profiles_c46.json` provides extracted glow parameters from 17 reference photos. The README notes recommended generator params (`sigma_frac=0.1165`, `fwhm_frac=0.2744`). But no production document specifies: how these parameters should be consumed by ENV generators, whether existing generators should be updated to use them, or what the acceptable variance is.
- Undocumented decisions: (17) whether CRT glow profiles are advisory or mandatory for generators, (18) the tolerance for deviation from the recommended params.
Bottom line: Data exists. Usage spec does not.

### 3c. Depth Temperature Rule — documented in image-rules.md, not in style guide

Score: 55
- The Depth Temperature Rule (warm=foreground, cool=background) was codified in C45 and lives in `docs/image-rules.md`. The style guide (`output/style_guide.md`) Section 4 mentions warm foreground / cool background as a "DO" but does not reference the formal rule, the tier system, or the lineup implementation (Option C). A new artist reading only the style guide would get the principle but not the specification.
- Undocumented decision: (19) whether image-rules.md or style_guide.md is the canonical source for composition rules.
Bottom line: The rule exists in two places at different levels of detail, with no cross-reference.

---

## 4. GENERATOR-TO-OUTPUT COMPLIANCE

### 4a. Glitch spec lint — 14 WARNs across generators

Score: 40
- The precritique QA (C46) reports 14 Glitch spec lint WARNs across 8 generators: missing UV_PURPLE shadow offset (G005), missing VOID_BLACK outline (G007), organic fills in Glitch body (G006), draw-order violations (G004), bilateral eye rule violations (G008). These are not new — many have persisted across multiple cycles. The glitch_spec_lint tool correctly identifies them. The generators have not been updated.
- Undocumented decisions: (20) whether these WARNs are accepted deviations or genuine defects awaiting fix, (21) the priority and ownership of each.
Bottom line: 14 lint violations with no documented triage is an unmanaged backlog.

### 4b. README Script Index — 3 UNLISTED tools, 1 GHOST

Score: 52
- Three tools on disk are not registered in the README Script Index (`LTG_TOOL_sb_caption_retrofit.py`, `LTG_TOOL_sb_cold_open_P16.py`, `LTG_TOOL_sb_cold_open_P17.py`). One README entry has no corresponding file (`LTG_TOOL_style_frame_01_discovery.py` — retired to deprecated/ in C43 but not removed from README). The QA tool correctly flags these. They persist.
- Undocumented decision: (22) whether README sync is a blocking gate or advisory.
Bottom line: README sync has been WARN for multiple cycles. Either it is a gate (enforce it) or it is not (remove the check).

### 4c. Warm/cool calibration report suggests threshold change, no decision recorded

Score: 45
- `warmcool_calibration_report_c46.md` concludes "REAL_INTERIOR threshold of 12.0 NEEDS ADJUSTMENT — 6/7 photos fall below. Recommend lowering to ~1.8." No follow-up decision document exists. The REAL_INTERIOR threshold in render_qa remains 12.0. The report recommends a change; no one has accepted or rejected it.
- Undocumented decision: (23) whether the REAL_INTERIOR threshold has been formally reviewed and retained at 12.0, or whether this recommendation is pending.
Bottom line: An unresolved recommendation is an open question in the spec.

---

## 5. PREVIOUSLY REVIEWED ASSETS — FIT CHECK

### 5a. Storyboard panels P18/P19 (new C46)

Score: 65
- P18 and P19 exist at canonical paths (`LTG_SB_cold_open_P18.png`, `LTG_SB_cold_open_P19.png`). PANEL_MAP updated. Naming is compliant. Generator scripts exist on disk (`LTG_TOOL_sb_cold_open_P16.py`, `P17.py`) — note these are for P16/P17, not P18/P19. The P18/P19 generators are not visible in the tools directory listing. If they were generated by scripts that are not registered, that is an additional README sync gap.
- No naming or structural violations detected for the panel PNGs themselves.
Bottom line: Panels are correctly placed and named. Generator registration status unclear.

### 5b. Lineup v010 (new C46)

Score: 55
- The v010 lineup implements the C45 Depth Temperature Rule (Option C dual-warmth bands). The README documents this. The pitch_package_index documents this. The character_export_manifest does not (frozen at v004). The lineup PNG is at `LTG_CHAR_character_lineup.png` (1280x535). No other document or manifest confirms which lineup file is the current pitch reference.
Bottom line: Good feature addition, poor document trail.

### 5c. Color fidelity WARNs — persistent across all style frames

Score: 48
- All four pitch style frames have BYTE_TEAL LAB deltaE WARNs (22.83-30.53, threshold 5.0). SUNLIT_AMBER WARNs range 16.76-44.94. These have been present for many cycles. No document records whether these are accepted deviations (e.g., compositing intentionally shifts these colors) or genuine palette drift requiring correction.
- This is not a new finding. It is an old finding that remains unresolved and undocumented.
Bottom line: Persistent color WARNs without a documented disposition are an open spec gap.

---

## SUMMARY

| Area | Undocumented Decisions | Worst Score |
|------|----------------------|-------------|
| Naming conventions | 10 | 28 |
| Document currency | 5 | 30 |
| Spec completeness | 4 | 45 |
| Generator compliance | 3 | 40 |
| Fit check (new assets) | 1 | 55 |
| **Total** | **23** | — |

**Overall Production System Score: 38**

The production has strong tooling (precritique_qa, glitch_spec_lint, ci_suite, UV_PURPLE linter, CRT glow profiler, depth_temp_lint). The tools are well-built and correctly identify problems. What is missing is the layer above the tools: decision records, document maintenance, and naming enforcement. The tools say "here is a problem." Nobody writes down "here is what we decided about that problem." The result is a production where the automation is ahead of the documentation. That is better than the reverse, but it is not a producible system.

A new artist joining this production today would need to ask at least 23 questions that the documentation should have answered. That number should be zero.
