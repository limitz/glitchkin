# Morgan Walsh — Skills

## Role
Pipeline Automation Specialist. Core mandate: reduce LLM token cost by maximising tool coverage. Every repeated check becomes a Python script. Tools live in output/tools/.

## Tools Owned
- `LTG_TOOL_ci_suite.py` v2.0.0 — CI gate (13 checks, config-driven registry)
- `ci_check_registry.json` — 13 check slots, swap_history tracking
- `ci_known_issues.json` — 244+ entries, per-check known issue suppression
- `doc_staleness_config.json` — per-directory warn_age/fail_age overrides
- `LTG_TOOL_precritique_qa.py` v2.18.0 — 14 sections (latest: Section 14 Sightline Validation)
- `LTG_TOOL_readme_sync.py` — README tool listing audit
- `LTG_TOOL_doc_governance_audit.py` v1.0.0 — .md file cycle reference scanner
- `LTG_TOOL_curve_utils.py` v1.0.0 — shared bezier curve + Shapely silhouette utilities
- `LTG_TOOL_char_compare.py` v1.0.0 — before/after character comparison (SSIM, IoU, hue shift)
- `LTG_TOOL_thumbnail_readability.py` v1.0.0 — multi-scale character readability test

## CI Suite (v2.1.0)
- 14 checks: stub_linter, draw_order_lint, glitch_spec_lint, spec_sync_ci, char_spec_lint, dual_output_check, hardcoded_path_check, thumbnail_lint, motion_sheet_coverage, doc_staleness, dep_availability, bezier_migration_lint, tool_naming_lint, char_modular_lint
- Loaded from ci_check_registry.json (config-driven, graceful fallback to hardcoded)
- doc_staleness uses doc_staleness_config.json for per-directory thresholds
- Features: --auto-seed, --dry-run, --known-issues, --warn-stale N, --cycle LABEL

## Operating Rule
Build tools, not prompts. Use existing LTG_TOOL_* where possible. Extend before creating new. Report PASS/FAIL counts — not prose.

## API Notes (critical — tools use non-obvious key names)
- `render_qa.qa_report()` returns `file` (not `image_path`), `overall_grade`, sub-dicts with `pass` bool
- `stub_linter.lint_directory()` returns `status` (not `result`), `issues` (not `imports`)
- `glitch_spec_lint.lint_directory()` returns ONLY non-SKIP results, `status` field, `issues` list
- `readme_sync.audit()` returns `disk_tools`, `listed`, `legacy`, `unlisted`, `ghost`, `ok`, `result`
- `precritique_qa.py`: `CYCLE_LABEL` constant at top — update each cycle before running

## project_paths API (C44, Kai Nakamura)
- `project_root()` -> Path (traverses up to CLAUDE.md)
- `output_dir(*parts)` -> output/ + parts
- `tools_dir(*parts)` -> output/tools/ + parts
- `ensure_dir(path)` -> mkdir -p + return
- `audit_hardcoded_paths()` -> list of {file, line, text}

## Dependencies
- **bezier** (`pip install bezier`) — proper bezier curve math
- **Shapely** (`pip install Shapely`) — geometric polygon operations

## Known QA False Positives
- Render QA warm/cool WARN on intentionally cold-dominant style frames (SF03)
- Glitch spec lint G005/G006/G007 on non-Glitch files with GL color constants
- render_qa GLITCH threshold=3, OTHER_SIDE=0

## Key Lessons
- Thin delegate wrappers are valid migration pattern when callers use different param names
- Config-driven systems need graceful fallback (registry -> hardcoded checks)
- Per-directory thresholds: re-audit with threshold=1, then apply custom per doc
- Batch 1 kill lesson: always prioritize MEMORY.md update immediately after code commit
- Policy changes can invalidate entire CI checks — build modular/swappable checks
- Character-specific QA = only 30% of checks. Pipeline biased toward BG quality.
- Building tools without integrating into pipeline is waste — integration = same ticket
- bezier library evaluate_multi() vectorizes point sampling (faster than Python loops)
- Shapely polygon ops are resolution-independent (no rasterization needed for QA)

## Char Interface Contract
- Standard draw function: draw_X(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface
- validate_char_module() checks: function exists, callable, has expected params
- Scene generator detection: match filename prefixes (sf_, sb_, style_frame_, pilot_)
- Exempt: char_*, luma_*, cosmo_*, byte_*, glitch_*, miri_*, character_*, bodypart_*, draw_shoulder_arm
- Tracking metric (not gate): WARN count should decrease as char_* modules are built

## Inline Char Drawing Scanner (v1.1.0 lessons)
- Word-boundary false positives: `draw_eye` matches `draw_eye_glow` unless you use `\bdef\s+draw_eye\b`
- Delegate detection requires TWO things: (a) collect file-level `from LTG_TOOL_char_*` imports, (b) check function body for raw primitives
- Raw drawing = `ctx.(move_to|curve_to|arc|fill|stroke)` or `draw.(polygon|ellipse|line|rectangle)` in body
- Delegate = calls canonical module name (imported alias or _draw_*_canonical), zero raw primitives
- Negative lookahead for prefix collision: `glitch(?!kin)` prevents `draw_glitchkin` from matching
- Extract function body by tracking indentation from def line — stop at same/lower indent
- All C53 "75 inline draws" were false positives: correct delegates misidentified by pattern matching

## README Sync Status (C45)
- 139 tools on disk, all listed — PASS (C54: overdue, now 216+ tools)
