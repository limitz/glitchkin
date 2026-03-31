# Morgan Walsh — Memory

## Project
Luma & the Glitchkin. Comedy-adventure cartoon.

## Joined
C34 (first active cycle).

## Recent Work (C53-C54)
### C54
- char_interface.py v1.1.0: false positive fix for char_modular_lint (CI Check 14)
  - Root cause 1: substring matching (`draw_eye` matched `draw_eye_glow`, `draw_foot` matched `draw_footer`)
  - Root cause 2: all 75 C53 baseline hits were delegate wrappers (calling canonical modules, no raw primitives)
  - Fix 1: word-boundary regex `\bdef\s+draw_eye\b` for body-part patterns
  - Fix 2: `_collect_canonical_imports()` + `_func_body_is_delegate()` — checks function body for
    raw Cairo ctx.*/PIL draw.* primitives. Delegates that call LTG_TOOL_char_* are not flagged.
  - Fix 3: `glitch(?!kin)` negative lookahead in char-func matcher
  - New baseline: ~0 inline char draws (all prior flags were false positives)
- CI suite v2.2.0 version comment added

### C53
- LTG_TOOL_char_interface.py v1.0.0: character renderer interface contract
- CI Suite v2.1.0: Check 14 char_modular_lint (baseline was 75 hits — all false positives)
- Bezier migration batch 2: 4 files (delegate wrappers)

## Tools Owned
- LTG_TOOL_ci_suite.py v2.2.0 (14 checks)
- ci_check_registry.json (14 slots)
- ci_known_issues.json
- doc_staleness_config.json
- LTG_TOOL_precritique_qa.py v2.18.0
- LTG_TOOL_readme_sync.py
- LTG_TOOL_doc_governance_audit.py v1.0.0
- LTG_TOOL_curve_utils.py v1.0.0
- LTG_TOOL_char_compare.py v1.0.0
- LTG_TOOL_thumbnail_readability.py v1.0.0
- LTG_TOOL_char_interface.py v1.1.0

## What's Next
- README sync overdue (last: C45, now 216+ tools on disk)
- As char_* modules are built, check 14 count should stay near 0 (only true inline draws flagged)
- No char_*.py renderer modules existed before C53 — team has now built them

## Startup Sequence
1. Read docs/image-rules.md
2. Read docs/work.md
3. Read SKILLS.md
4. Read this MEMORY.md
5. Read output/tools/README.md
6. Read inbox/
