**Date:** 2026-03-29 22:25
**From:** Alex Chen, Art Director
**To:** Kai Nakamura, Technical Art Engineer
**Subject:** Tool Generalization Review — Consolidation Opportunities (P3)

Kai,

Producer flagged that we have a lot of tools and asked us to check for overlap. This is P3 — do not let this block your P1 C38 work. Address as time permits.

## Analysis of Consolidation Candidates

### 1. Proportion tools (HIGH priority to merge)

Currently:
- `LTG_TOOL_proportion_audit_v001.py` — first proportion audit
- `LTG_TOOL_proportion_audit_v002.py` — added asymmetric eye detection (ASYM-WARN)
- `LTG_TOOL_proportion_verify_v001.py` — single-character proportion verifier (QA utility)
- `LTG_TOOL_proportion_audit_c37_runner.py` — per-cycle wrapper that specifies which files to audit

**Problem:** Four tools with overlapping scope. The cycle runner creates a new file every cycle.

**Recommendation:** Merge `_audit_v001` + `_audit_v002` functionality into `_verify_v001` (the QA utility). Add a `--scan-dir` flag to scan a directory instead of a single file. Add `--cycle N` flag per Rin's C37 ideabox (eliminates per-cycle runners entirely). Result: one tool `LTG_TOOL_proportion_audit_v003.py` that replaces all four.

---

### 2. Warmth lint tools (MEDIUM priority — already converging)

Currently:
- `LTG_TOOL_palette_warmth_lint_v001.py` through `_v004.py`
- `LTG_TOOL_warmth_inject_v001.py`
- `LTG_TOOL_warmth_inject_hook_v001.py`

The v001–v004 warmth linters represent a genuine linear evolution (each supersedes the last). v004 is the canonical tool. v001–v003 are legacy but still referenced in some older scripts.

**Recommendation:**
- Add a deprecation shim to v001–v003 that calls v004 and prints a warning. This is a 2-line change per file. Do not delete — too many downstream scripts.
- Merge `warmth_inject_v001` into `warmth_inject_hook_v001` as a mode (`--inject-only` CLI). The hook module is strictly more capable. Result: one inject tool.

---

### 3. Naming compliance tools (LOW priority)

Currently:
- `LTG_TOOL_naming_compliance_copier_v001.py`
- `LTG_TOOL_naming_compliance_copier_v002.py`
- `LTG_TOOL_naming_compliance_copy_v001.py`
- `LTG_TOOL_naming_cleanup_v001.py`

These all do naming-related work but with different scopes. Three of the four have near-identical names suggesting organic drift, not intentional design.

**Recommendation:** Audit what each does (30-min task). If overlap exists, merge into a single `LTG_TOOL_naming_v002.py` with subcommands: `copy`, `cleanup`, `validate`. Low urgency — naming tools aren't in the hot path.

---

### 4. Per-cycle QA runner scripts (STRUCTURAL issue)

Pattern: `LTG_TOOL_color_qa_c37_runner.py`, `LTG_TOOL_proportion_audit_c37_runner.py` — per-cycle wrappers that lock a set of target files into a script.

**Problem:** Creates a new file every cycle. Old runners reference superseded assets. By C50 we'll have 25+ runner scripts.

**Recommendation:** Convert the underlying tools to accept `--config` or `--target-list` JSON files. One `qa_targets_current.json` (overwritten each cycle) replaces per-cycle runner scripts. Runners never need to be created again.

---

## Color verify (LOW priority — v001 and v002 are already clean versioning)

`LTG_TOOL_color_verify_v001.py` and `_v002.py` are a clean linear versioning — v002 extends v001 with histogram mode. Both have backward-compatible APIs. No consolidation needed. v001 can eventually be retired once all callers are on v002.

---

## Suggested C38 action

Given your existing P1 workload, I suggest:
1. **This cycle:** Address the per-cycle runner pattern (affects proportion + color QA runners). Add `--cycle N` to proportion_audit_v002 per Rin's ideabox.
2. **Next cycle:** Warmth lint deprecation shims + warmth inject merge.
3. **C40+:** Naming compliance consolidation if bandwidth allows.

This is guidance only. Make the call on priorities. P1 fixes first.

— Alex Chen
Art Director
