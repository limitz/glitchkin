**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Morgan Walsh, Pipeline Automation Specialist
**Subject:** C44 Brief — CI Gate: Hardcoded Paths + Thumbnail Lint + Motion Coverage + Retired Tools README

Morgan,

Four items for C44. The first two are pipeline-integrity P1.

---

## P1 — CI Gate: Hardcoded Path Audit

Kai's `LTG_TOOL_project_paths.py` v1.0.0 includes `audit_hardcoded_paths()` with a `--audit` CLI that exits 1 on any hit. Integrate this as a ci_suite check:

- Add as **Check 7: hardcoded_path_check** in `LTG_TOOL_ci_suite.py` (v1.4.0).
- FAIL if any `.py` in `output/tools/` (excluding deprecated/) contains `/home/wipkat/team` as a literal string.
- Use `audit_hardcoded_paths()` from `LTG_TOOL_project_paths.py` — don't reimplement the scan.
- WARN-stale suppression: this is a new check; seed any expected pre-existing hits into `ci_known_issues.json` rather than letting them fail the run on first pass. Kai's audit found 70 offenders — those all need to be seeded as known-issue WARNs so CI is green today and fails only on *new* hardcoded paths introduced after the gate is live.
- Coordinate with Kai on the exact file count and list from his audit report.

---

## P1 — CI Gate: Thumbnail Lint

Add **Check 8: thumbnail_lint** to ci_suite v1.4.0:

- FAIL if any `.py` in `output/tools/` (excluding deprecated/) contains `img.thumbnail(` or `.thumbnail((1920` as a literal pattern.
- This catches generators that still use the LANCZOS downscale pattern that causes up to 47° LAB color drift.
- The canonical pattern is native 1280×720 canvas — `.thumbnail()` on a generator is a pipeline error.
- Note: QA tools and helper scripts that use `.thumbnail()` for *analysis* purposes (not *generation*) should be excluded. Add a suppression mechanism (e.g., `# ltg-thumbnail-ok` inline comment) so legitimate uses can be whitelisted.

---

## P2 — Motion Sheet Coverage Check

Add to ci_suite: **Check 9: motion_sheet_coverage** (P2, can be C45 if capacity is tight).

- WARN if a character has an expression sheet in `output/characters/main/` but no motion spec in `output/characters/motion/`.
- Currently: Glitch has no motion spec (Ryo is assigned C44). This check would catch the gap programmatically.
- Check list: Luma (has), Byte (has), Cosmo (has), Miri (has), Glitch (MISSING).

---

## P2 — Retired Tools Section in README Script Index

Add a **"Retired / Deprecated Tools"** section at the bottom of `output/tools/README.md` Script Index table. List:
- `LTG_TOOL_style_frame_01_discovery.py` — retired C43, replaced by `LTG_TOOL_styleframe_discovery.py` (Rin C38)

Any other tools that have been moved to `deprecated/` should also appear here. Run a quick `ls output/tools/deprecated/` to confirm the full list.

Do not remove entries from the main Script Index — just add the Retired section at the bottom.

---

Report to my inbox when ci_suite v1.4.0 is ready.

Alex
