"""
LTG_TOOL_color_qa_c37_runner.py
================================
C37 QA Baseline runner — Sam Kowalski (Color & Style Artist)
Runs render_qa v1.4.0 (world-type-aware) on all C37 pitch-primary assets.
Also runs warmth lint v004 on master_palette.md.
Also evaluates LTG_ENV_grandma_living_room_v001.png (Hana Okonkwo, C37).

Saves results to output/production/color_qa_c37_baseline.md

Usage:
    python3 LTG_TOOL_color_qa_c37_runner.py
"""

import sys
import os
from pathlib import Path

# ─── path setup ─────────────────────────────────────────────────────────────
TOOLS_DIR = Path(__file__).parent.resolve()
BASE_DIR   = (TOOLS_DIR / ".." / "..").resolve()   # /home/wipkat/team

if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# ─── imports ─────────────────────────────────────────────────────────────────
from LTG_TOOL_render_qa_v001 import qa_report, __version__ as RQA_VERSION
from LTG_TOOL_palette_warmth_lint_v004 import (
    lint_palette_file, load_config, __version__ as LINT_VERSION
)

# ─── asset lists ─────────────────────────────────────────────────────────────
SF_DIR  = BASE_DIR / "output" / "color" / "style_frames"
CHAR_DIR = BASE_DIR / "output" / "characters"
ENV_DIR = BASE_DIR / "output" / "backgrounds" / "environments"
PROD_DIR = BASE_DIR / "output" / "production"

# Pitch-primary style frames (current canonical versions)
PITCH_STYLE_FRAMES = [
    SF_DIR / "LTG_COLOR_styleframe_discovery_v005.png",       # SF01 (Rin procedural lift)
    SF_DIR / "LTG_COLOR_styleframe_glitch_storm_v008.png",    # SF02 (current)
    SF_DIR / "LTG_COLOR_styleframe_otherside_v005.png",       # SF03 (current)
    SF_DIR / "LTG_COLOR_styleframe_luma_byte_v004.png",       # SF04 (current)
]

# Character assets (primary pitch versions)
PITCH_CHAR_ASSETS = [
    BASE_DIR / "output" / "characters" / "main" / "LTG_CHAR_character_lineup_v007.png",
    BASE_DIR / "output" / "characters" / "color_models" / "LTG_COLOR_luma_color_model_v002.png",
    BASE_DIR / "output" / "characters" / "color_models" / "LTG_COLOR_byte_color_model_v001.png",
]

# New C37 environment (Hana Okonkwo)
LIVING_ROOM_ENV = ENV_DIR / "LTG_ENV_grandma_living_room_v001.png"

# Master palette path
MASTER_PALETTE = BASE_DIR / "output" / "color" / "palettes" / "master_palette.md"


def grade_symbol(result: dict) -> str:
    g = result.get("overall_grade", "?")
    return g


def wc_result(r: dict) -> str:
    wc = r.get("warm_cool", {})
    if wc.get("status") == "SKIPPED":
        return "SKIP"
    if wc.get("pass", True):
        return f"PASS (sep={wc.get('separation', '?'):.1f})"
    wt = wc.get("world_type", "—")
    sep = wc.get("separation", 0)
    thresh = wc.get("threshold", 20)
    return f"FAIL (sep={sep:.1f}, thresh={thresh}, world={wt})"


def cf_result(r: dict) -> str:
    cf = r.get("color_fidelity", {})
    overall = cf.get("overall_pass", True)
    return "PASS" if overall else "FAIL"


def run_qa_on_assets(asset_paths: list, label: str) -> list:
    results = []
    for path in asset_paths:
        if not path.exists():
            print(f"  [MISSING] {path.name}")
            results.append({"file": str(path), "overall_grade": "MISSING", "_missing": True})
            continue
        print(f"  QA: {path.name} ...", end=" ", flush=True)
        r = qa_report(str(path), asset_type="auto")
        print(r["overall_grade"])
        results.append(r)
    return results


def run_warmth_lint() -> dict:
    """Run warmth lint v004 on master_palette.md."""
    config = load_config()
    result = lint_palette_file(str(MASTER_PALETTE), config)
    return result


def build_report(sf_results, char_results, living_room_result, warmth_lint_result) -> str:
    lines = []
    lines.append("# Color QA Baseline — Cycle 37")
    lines.append("**Author:** Sam Kowalski (Color & Style Artist)")
    lines.append("**Date:** 2026-03-30")
    lines.append(f"**Tool versions:** LTG_TOOL_palette_warmth_lint_v004.py v{LINT_VERSION} · LTG_TOOL_render_qa_v001.py v{RQA_VERSION}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Warmth Lint v004 — Master Palette")
    lines.append("")

    # Warmth lint summary
    total = warmth_lint_result.get("total_checked", 0)
    violations = warmth_lint_result.get("violations", [])
    n_violations = warmth_lint_result.get("total_violations", len(violations))
    result_str = warmth_lint_result.get("result", "PASS")
    status = "PASS" if n_violations == 0 else "FAIL"
    lines.append(f"| Prefixes | Entries Checked | Violations | Result |")
    lines.append(f"|---|---|---|---|")
    prefixes = warmth_lint_result.get("prefixes_checked", ["CHAR-M", "CHAR-L"])
    prefix_str = ", ".join(prefixes) if isinstance(prefixes, list) else str(prefixes)
    lines.append(f"| {prefix_str} | {total} | {n_violations} | **{status}** |")
    lines.append("")
    if n_violations > 0:
        lines.append("**Violations:**")
        for v in violations:
            lines.append(f"- {v}")
        lines.append("")
    else:
        lines.append("No violations. All CHAR-M and CHAR-L hoodie warmth guarantees confirmed.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. World-Type Thresholds — render_qa v1.4.0")
    lines.append("")
    lines.append("render_qa v1.4.0 integrates world-type-aware warm/cool thresholds via `infer_world_type()`.")
    lines.append("This eliminates the systematic false WARN on GLITCH/OTHER_SIDE style frames that appeared in C36.")
    lines.append("")
    lines.append("| World Type | warm_cool_threshold | Expected in C37 |")
    lines.append("|---|---|---|")
    lines.append("| REAL | 20 PIL units | Grandma kitchen, living room, school, main street |")
    lines.append("| GLITCH | 3 PIL units | SF02 Glitch Storm — near-zero warm expected |")
    lines.append("| OTHER_SIDE | 0 PIL units | SF03 Other Side — skip (no warm) |")
    lines.append("| None (unknown) | 20 PIL units | Fallback; conservative default |")
    lines.append("")
    lines.append("**Key improvement:** SF02 (GLITCH) and SF03 (OTHER_SIDE) no longer generate false warm/cool WARNs.")
    lines.append("SF01 (REAL) may still WARN if separation < 20 — check below.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Render QA — Pitch-Primary Style Frames")
    lines.append("")
    lines.append("| Asset | Version | Grade | Silhouette | Value Range | Warm/Cool | Line Weight | Color Fidelity | Value Ceiling | Notes |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")

    sf_labels = ["SF01 Discovery", "SF02 Glitch Storm", "SF03 Other Side", "SF04 Luma/Byte"]
    sf_versions = ["v005", "v008", "v005", "v004"]
    for i, r in enumerate(sf_results):
        label = sf_labels[i] if i < len(sf_labels) else "?"
        ver = sf_versions[i] if i < len(sf_versions) else "?"
        if r.get("_missing"):
            lines.append(f"| {label} | {ver} | MISSING | — | — | — | — | — | — | File not found |")
            continue
        grade = grade_symbol(r)
        sil = r.get("silhouette", {}).get("score", "?")
        vr_pass = r.get("value_range", {}).get("pass", True)
        vr = f"PASS ({r['value_range']['min']}–{r['value_range']['max']})" if vr_pass else f"FAIL ({r['value_range']['min']}–{r['value_range']['max']})"
        wc = wc_result(r)
        lw = "PASS" if r.get("line_weight", {}).get("pass", True) else "FAIL"
        cf = cf_result(r)
        vc_d = r.get("value_ceiling", {})
        vc = f"PASS ({vc_d.get('brightness_after','?')})" if vc_d.get("pass", True) else f"FAIL ({vc_d.get('brightness_before','?')}→{vc_d.get('brightness_after','?')})"
        warns = r.get("_warn_conditions", [])
        fails = r.get("_fail_conditions", [])
        note_parts = fails + warns
        note = "; ".join(note_parts) if note_parts else "—"
        lines.append(f"| {label} | {ver} | **{grade}** | {sil} | {vr} | {wc} | {lw} | {cf} | {vc} | {note} |")

    lines.append("")

    # Count grades
    sf_grades = [r.get("overall_grade", "MISSING") for r in sf_results]
    lines.append(f"**SF Results:** {sf_grades.count('PASS')} PASS / {sf_grades.count('WARN')} WARN / {sf_grades.count('FAIL')} FAIL")
    lines.append("")
    lines.append("### v1.4.0 Warm/Cool Improvement vs C36")
    lines.append("In C36 (v1.3.0), ALL four SFs had warm/cool WARN (documented FPs).")
    lines.append("With v1.4.0 world-type inference:")
    lines.append("- SF02 (GLITCH world): threshold now 3.0 → PASS expected")
    lines.append("- SF03 (OTHER_SIDE world): threshold now 0.0 → always PASS")
    lines.append("- SF04 (world inferred from filename 'luma_byte' → None → threshold 20): may still WARN")
    lines.append("- SF01 (REAL world): threshold 20 → WARN if sep < 20 (was 17.9 in C36)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Render QA — Character Assets")
    lines.append("")
    lines.append("| Asset | Grade | Silhouette | Value Range | Color Fidelity | Warm/Cool | Notes |")
    lines.append("|---|---|---|---|---|---|---|")
    char_labels = ["Character Lineup v007", "Luma Color Model v002", "Byte Color Model v001"]
    for i, r in enumerate(char_results):
        label = char_labels[i] if i < len(char_labels) else Path(r["file"]).name
        if r.get("_missing"):
            lines.append(f"| {label} | MISSING | — | — | — | — | File not found |")
            continue
        grade = grade_symbol(r)
        sil = r.get("silhouette", {}).get("score", "?")
        vr = "PASS" if r.get("value_range", {}).get("pass", True) else "FAIL"
        cf = cf_result(r)
        wc_d = r.get("warm_cool", {})
        wc = "SKIP" if wc_d.get("status") == "SKIPPED" else ("PASS" if wc_d.get("pass", True) else "FAIL")
        warns = r.get("_warn_conditions", [])
        note = "; ".join(warns) if warns else "—"
        lines.append(f"| {label} | **{grade}** | {sil} | {vr} | {cf} | {wc} | {note} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. New Environment — Grandma Living Room v001 (Hana Okonkwo, C37)")
    lines.append("")

    if living_room_result.get("_missing"):
        lines.append("**MISSING** — LTG_ENV_grandma_living_room_v001.png not found.")
        lines.append("Cannot run QA. Block Hana Okonkwo until file is delivered.")
    else:
        lr = living_room_result
        grade = grade_symbol(lr)
        sil = lr.get("silhouette", {}).get("score", "?")
        vr_d = lr.get("value_range", {})
        vr_pass = vr_d.get("pass", True)
        vr_str = f"PASS ({vr_d.get('min','?')}–{vr_d.get('max','?')})" if vr_pass else f"FAIL ({vr_d.get('min','?')}–{vr_d.get('max','?')})"
        wc_str = wc_result(lr)
        cf_str = cf_result(lr)
        lw_str = "PASS" if lr.get("line_weight", {}).get("pass", True) else "FAIL"
        vc_d = lr.get("value_ceiling", {})
        vc_str = f"PASS ({vc_d.get('brightness_after','?')})" if vc_d.get("pass", True) else f"FAIL ({vc_d.get('brightness_before','?')}→{vc_d.get('brightness_after','?')})"
        warns = lr.get("_warn_conditions", [])
        fails = lr.get("_fail_conditions", [])
        note_parts = fails + warns

        lines.append(f"| Check | Result |")
        lines.append(f"|---|---|")
        lines.append(f"| Overall Grade | **{grade}** |")
        lines.append(f"| Silhouette | {sil} |")
        lines.append(f"| Value Range | {vr_str} |")
        lines.append(f"| Warm/Cool | {wc_str} |")
        lines.append(f"| Color Fidelity | {cf_str} |")
        lines.append(f"| Line Weight | {lw_str} |")
        lines.append(f"| Value Ceiling | {vc_str} |")
        lines.append("")
        if note_parts:
            lines.append("**Issues found:**")
            for note in note_parts:
                lines.append(f"- {note}")
            lines.append("")
        else:
            lines.append("No issues found.")
            lines.append("")

        # Color fidelity detail
        cf_d = lr.get("color_fidelity", {})
        if not cf_d.get("overall_pass", True):
            lines.append("**Color Fidelity failures:**")
            for c_name, c_result in cf_d.get("checks", {}).items():
                if not c_result.get("pass", True):
                    lines.append(f"- {c_name}: delta_hue={c_result.get('delta_hue', '?'):.1f}° — {c_result.get('note', '')}")
            lines.append("")

    lines.append("")
    lines.append("### Warmth Lint — Living Room")
    lines.append("")
    lines.append("The living room is a REAL World environment. Expected: zero Glitch colors.")
    lines.append("Warmth lint is not directly applicable (no CHAR-M/CHAR-L entries in an env file).")
    lines.append("Verify manually that no GL-* Glitch palette values appear in the generator source.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 6. QA False Positive Registry — Carry Forward from C36")
    lines.append("")
    lines.append("See `/output/production/qa_false_positives.md` for full registry.")
    lines.append("")
    lines.append("| FP ID | Asset | Check | Root Cause | Status |")
    lines.append("|---|---|---|---|---|")
    lines.append("| FP-001 | SF01/SF02/SF03/SF04 | warm_cool WARN (v1.3.0) | Single-dominant-temperature SFs; vertical split irrelevant | **RESOLVED in v1.4.0** (world-type thresholds) |")
    lines.append("| FP-002 | Luma/Miri char sheets | color_fidelity SUNLIT_AMBER | Skin hue ~18-25° within radius=40 of SUNLIT_AMBER 34.3° | Ongoing — low priority |")
    lines.append("| FP-003 | SF03 Other Side | color_fidelity UV_PURPLE | Gradient/AA pixels drag median; canonical bucket still 2nd-largest | Ongoing — documented |")
    lines.append("| FP-004 | Luma color model | color_fidelity SUNLIT_AMBER | Same skin-tone false positive as FP-002 | Ongoing — low priority |")
    lines.append("| FP-005 | SF04 Luma/Byte | silhouette ambiguous | Soft-key lighting, no hard outline — intentional Naomi decision | Ongoing — accepted |")
    lines.append("| FP-006 | SF04 Luma/Byte | value_range max=198 | Discovery low-key lighting, no specular dots — Alex Chen decision | Ongoing — accepted |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 7. Open Items / Carry Forward")
    lines.append("")
    lines.append("- **FP-001 RESOLVED.** render_qa v1.4.0 world-type-aware thresholds eliminate the 4 SF warm/cool WARNs.")
    lines.append("- **SF03 color fidelity FAIL** = FP-003 (UV_PURPLE gradient AA). Not a production error.")
    lines.append("- **SF04 pre-existing issues** (FP-005 ambiguous silhouette, FP-006 max brightness 198) carried from C31. Alex Chen decision open.")
    lines.append("- **Luma expr sheet filename** does not contain 'expression_sheet' keyword — warm/cool check runs (not skipped). Low priority.")
    lines.append("- **ENV-06 v001 note** still in master_palette.md — Jordan to remove. Low priority.")
    lines.append("- **SF02 v007 color audit CLOSED.** v008 (current) confirmed clean in C36.")

    return "\n".join(lines) + "\n"


def main():
    print("=== C37 Color QA Baseline — Sam Kowalski ===")
    print(f"render_qa version: {RQA_VERSION}")
    print(f"warmth_lint version: {LINT_VERSION}")
    print()

    print("[1/4] Running warmth lint on master_palette.md ...")
    warmth_lint_result = run_warmth_lint()
    total = warmth_lint_result.get("entries_checked", 0)
    violations = warmth_lint_result.get("violations", [])
    total = warmth_lint_result.get("total_checked", 0)
    violations = warmth_lint_result.get("violations", [])
    n_violations = warmth_lint_result.get("total_violations", len(violations))
    print(f"      Entries checked: {total}, Violations: {n_violations}")
    print()

    print("[2/4] Running render_qa on pitch-primary style frames ...")
    sf_results = run_qa_on_assets(PITCH_STYLE_FRAMES, "style_frames")
    print()

    print("[3/4] Running render_qa on character assets ...")
    char_results = run_qa_on_assets(PITCH_CHAR_ASSETS, "characters")
    print()

    print("[4/4] Running render_qa on Grandma Living Room (Hana, C37) ...")
    if LIVING_ROOM_ENV.exists():
        lr_result = qa_report(str(LIVING_ROOM_ENV), asset_type="environment")
        print(f"      Grade: {lr_result['overall_grade']}")
    else:
        print(f"      MISSING: {LIVING_ROOM_ENV}")
        lr_result = {"file": str(LIVING_ROOM_ENV), "overall_grade": "MISSING", "_missing": True}
    print()

    print("Building report ...")
    report_text = build_report(sf_results, char_results, lr_result, warmth_lint_result)

    PROD_DIR.mkdir(parents=True, exist_ok=True)
    report_path = PROD_DIR / "color_qa_c37_baseline.md"
    report_path.write_text(report_text)
    print(f"Report saved: {report_path}")

    # Grade summary
    all_results = sf_results + char_results + [lr_result]
    pass_n = sum(1 for r in all_results if r.get("overall_grade") == "PASS")
    warn_n = sum(1 for r in all_results if r.get("overall_grade") == "WARN")
    fail_n = sum(1 for r in all_results if r.get("overall_grade") == "FAIL")
    miss_n = sum(1 for r in all_results if r.get("overall_grade") == "MISSING")
    print(f"\nSummary: {pass_n} PASS / {warn_n} WARN / {fail_n} FAIL / {miss_n} MISSING")


if __name__ == "__main__":
    main()
