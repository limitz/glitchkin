# Critique 13 — Reinhardt Böhm
## Production Design Systems Enforcer — Audit Report
**Date:** 2026-03-29
**Cycle:** 13 (post-C12 remediation audit)
**Scope:** Naming conventions, style guide completeness, doc currency, asset reproducibility, draw-order lint results

---

## Method

Reproducibility test applied to Luma character design (primary asset). New-artist assumption: read `luma.md`, `master_palette.md`, `naming_conventions.md`, and `character_sheet_standards_v001.md` — attempt to produce a compliant character sheet without asking questions. Counted every decision left undefined or contradicted.

---

## System 1 — Naming Convention Compliance

**Score: 74 / 100**

- `run_c31_qa.py` and `test_face_lighting_v001.py` in `output/tools/` active directory are non-compliant. Both are utility/test scripts and must carry `LTG_TOOL_` prefix; they are indexed in `README.md` as PASS by the linter because they aren't in the CHAR/COLOR/BRAND-violation class, but they violate the naming convention stated in `naming_conventions.md` Section "Tool / Script Assets."
- `LTG_TOOL_naming_compliance_copy_v001.py` vs `LTG_TOOL_naming_compliance_copier_v001/v002.py` — three tools with overlapping purpose, no consolidation decision recorded. README says "flagged for consolidation review — Alex Chen to decide" — C31 and still unresolved.
- Legacy violations have been deleted (22 files confirmed gone). This is real progress from C12.

**Bottom line:** Active naming violations reduced to 2 unlabeled scripts; the consolidation ambiguity in the copier tools is a documentation debt that will confuse a new artist.

---

## System 2 — Draw-Order Lint (LTG_TOOL_draw_order_lint_v001.py)

**Score: 52 / 100**

- Lint run result: 120 files — 65 PASS / **55 WARN** / 0 ERROR. 46% of generators still flagged.
- W004 dominates (54 of 55 warnings): `img.paste()`/`alpha_composite()` not followed by `draw = ImageDraw.Draw(img)` refresh. Pattern is systemic across background generators (Kitchen v001–v003 carry 3, 6, and 8 W004s respectively; the SAME bug propagating version-to-version without fix).
- W002 appears in 8 cases across hallway, tech den, and classroom generators: outline drawn before fill in `draw.rectangle()` calls. This is a painter's-algorithm violation with visible rendering consequences — outlines may be partially obscured.
- The lint tool was built specifically to catch W004. Building the tool and not fixing any W004s in the same cycle is a compliance gap. Generators should be fixed in the cycle the linter is deployed.

**Bottom line:** 55 unresolved warnings — nearly half the tool library is flagged — means every background generator is a reproducibility risk, and the W002 fill/outline order violations are already producing incorrect output.

---

## System 3 — character_sheet_standards_v001.md

**Score: 71 / 100**

- Document is well-structured and substantively useful. Sections 1–6 are clear enough to produce conforming output.
- **Section 7 inconsistency log is honest** — credit for documenting known gaps rather than suppressing them. But "flagged for discussion" is not a resolution target. Three open items (Miri line weight, Byte arc weight, Cosmo v004 version chain) have been present since at least C30 with no assigned owner or deadline.
- Cosmo v004 issue is production-critical: `LTG_TOOL_cosmo_expression_sheet_v004.py` is byte-identical to v003 and outputs `_v003.png`. A new artist running v004 gets a v003 output and a naming collision — this is not a flag for discussion, it is a defect requiring a fix.
- Glitch's expression labels use `COVETOUS` in the standards table (Section 7) but the Glitch expression sheet v003 README entry (in tools/README.md) says "YEARNING, REACHING OUT, REMEMBERING." Names do not match. An artist cannot know which label set is canonical.

**Bottom line:** The standards document has a good skeleton, but three known defects have been documented rather than resolved for at least one full critique cycle.

---

## System 4 — Reproducibility Test: Luma Character Sheet

**Score: 41 / 100**

This is the core audit. I attempted to construct a compliant Luma expression sheet using only the project documentation. I found **7 undocumented or contradicted decisions.**

**Gap 1 (CRITICAL — direct contradiction):** `luma.md` Section 3 states Luma's total height is **3.5 heads**. `character_sheet_standards_v001.md` Section 7 states the current sheet (v007, C29) uses **3.2 heads**. Both documents are active. A new artist must guess which is correct. There is no document that records the decision to change this value or supersedes `luma.md`.

**Gap 2 (CRITICAL — broken toolchain):** `LTG_TOOL_luma_expression_sheet_v006.py` is a forwarding stub that imports from `LTG_CHAR_luma_expression_sheet_v006`. That module does not exist on disk. Running the stub throws `ModuleNotFoundError`. The stub is non-functional. The same issue likely applies to other C28 forwarding stubs (`cosmo_turnaround_v002`, `luma_turnaround_v002`, `grandma_miri_expression_sheet_v003`, `luma_expression_sheet_v005`). I tested one; it fails immediately.

**Gap 3:** `luma.md` Section 5 specifies **5 curls** (locked production count). `LTG_TOOL_luma_expression_sheet_v007.py` (current canonical) uses "8-ellipse hair curl cloud" per its README entry. 5 vs 8. No document records which standard supersedes the other.

**Gap 4:** Luma color model (v001) uses eye proportion `eye_r_x=14 at head_r=46` (~0.30 ratio). v007 canonical uses `ew=HR×0.22`. `luma.md` Section 3 says "Each eye is approximately 0.22x head width." The `luma.md` value matches v007 (correct), but the color model silhouette contradicts it. A new artist consulting the color model PNG will learn the wrong proportion for the eyes.

**Gap 5:** `luma.md` does not specify which generator file is canonical for the Luma design. There is no pointer in the character spec to the production tool. Cross-reference between `luma.md` and the generator family (v002 through v007) is absent.

**Gap 6:** No document specifies what happens if a Luma expression sheet must be produced for a character size outside the specified HEAD_R=105 (1×). `character_sheet_standards_v001.md` Section 2 says "never set HEAD_R so large that body/legs fall below panel bottom" — but does not specify the minimum HEAD_R before switching to bust format.

**Gap 7:** Glitch has no character spec file. `output/characters/main/` contains no `glitch.md`. Glitch has three expression sheets, two turnarounds, and a color model — all with no primary spec document. A new artist drawing Glitch has no authoritative source of shape language, proportions, or color breakdown. The tools are the only specification, which violates the system design premise.

**Bottom line:** A new artist cannot produce a correct Luma character sheet from documentation alone — the proportion conflict between `luma.md` and `character_sheet_standards_v001.md` is unresolvable without external information, and the current canonical generator (v007) cannot be run because v006's forwarding stub is broken.

---

## System 5 — naming_conventions.md Currency

**Score: 82 / 100**

- Document is complete for categories, examples, version numbering, and `_FINAL` policy.
- The `output/production/` exemption is clearly stated and rationale is documented — this is good practice.
- **Missing:** No FX or SB asset examples reference actual current assets. The SB section lists hypothetical PDF paths that do not match actual panel file naming (`LTG_SB_ep01_cold_open_seq01_v001.pdf` does not exist; actual panels use `LTG_TOOL_sb_panel_a101_v001.py`). A new artist will be confused about whether the storyboard asset naming examples reflect the real pipeline.
- `LH_INT_` and `GL_` retired prefixes are documented; reconciliation schedule says "wait for Environment Document v3.0" with no version number or cycle target attached to that promise.

**Bottom line:** Convention document is functionally solid but its examples have diverged from actual production practice, which will mislead onboarding artists.

---

## Overall System Health

**Overall Score: 64 / 100** (up from C12 FAIL — meaningful progress, not yet passing)

Progress since C12:
- 22 legacy naming violations deleted: done.
- `naming_conventions.md` exists and is coherent: done.
- `character_sheet_standards_v001.md` updated with current versions: done.
- `LTG_TOOL_draw_order_lint_v001.py` built: done.

Remaining systemic failures:
1. `luma.md` has not been updated to reflect the 3.2-head proportion change — a core spec document contradicts the production tool.
2. Forwarding stubs from C28 are broken. The `LTG_CHAR_*` originals they reference were removed (by the naming cleanup tool run) without updating the stubs. At least 8 stubs are non-functional.
3. 55 draw-order warnings persist with no fix cycle scheduled.
4. Glitch has no character spec document — an entire main character is undocumented at the spec level.
5. Cosmo v004 version chain defect (outputs wrong filename) has been documented but not fixed.

**A new artist cannot reproduce the primary character asset from documentation alone. That is still a FAIL on my standard. The system has improved structurally; the documentation has not kept pace with the generator updates.**
