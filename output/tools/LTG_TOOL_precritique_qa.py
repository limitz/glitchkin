#!/usr/bin/env python3
"""
LTG_TOOL_precritique_qa.py
================================
Pre-Critique QA Pipeline for "Luma & the Glitchkin."

Single entry-point script that chains all existing QA tools and produces a
consolidated Markdown report at output/production/precritique_qa_cNN.md.

Tools chained (in order):
  1. LTG_TOOL_render_qa.py       — size/resolution/quality checks on pitch PNGs
                                        (v1.3.0: adds Check F value ceiling guard)
  2. LTG_TOOL_color_verify.py    — canonical color fidelity on style frames
  3. LTG_TOOL_proportion_verify.py — head/body proportion checks on character sheets
  4. LTG_TOOL_stub_linter.py     — broken import detection in output/tools/
  5. LTG_TOOL_palette_warmth_lint.py — CHAR-M + CHAR-L hoodie warmth compliance on master_palette.md
                                             (v005 available; v004 used here for stable import)
  6. LTG_TOOL_glitch_spec_lint.py    — Glitchkin generator spec validation
  7. LTG_TOOL_readme_sync.py     — README Script Index completeness audit
  8. LTG_TOOL_motion_spec_lint.py — Motion spec sheet structural checks (Ryo Hasegawa C39)
  9. Delta Report                     — compare current run vs last run (qa_baseline_last.json)
 10. Arc-Diff Gate (informational)    — contact sheet version diff (Lee Tanaka C38 ideabox idea)
     LTG_TOOL_contact_sheet_arc_diff.compare_contact_sheets(). Compares current and prior
     contact sheet versions. CHANGED > 3: NOTE listing changed panels. REMOVED > 0: WARN.
     Does not affect overall PASS/WARN/FAIL score — informational gate only.

Output:
    output/production/precritique_qa_c<NN>.md
    output/tools/qa_baseline_last.json  (updated each run)

Exit codes:
    0 — All checks PASS
    1 — One or more WARN
    2 — One or more FAIL/ERROR

Author: Morgan Walsh (Pipeline Automation Specialist)
Created: Cycle 34 — 2026-03-29
Version: 2.6.0 (C39 Morgan Walsh: arc-diff gate Section 10 added — contact sheet changelog for critics.
              Lineup suppression expansion complete — glitch_spec_lint v1.4.0 file_prefix mode;
              character_lineup_* G006/G007 now auto-suppressed via prefix.)
Version: 2.5.0 (C39 Ryo Hasegawa: motion spec lint Section 8 added.)
Version: 2.4.0 (C39 Sam Kowalski: warmth lint v001→v004; CHAR-L hoodie + REAL_STORM threshold.)
"""

import os
import sys
import json
import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup — allow running from any cwd
# ---------------------------------------------------------------------------
REPO_ROOT   = Path(__file__).resolve().parent.parent.parent  # /home/wipkat/team
TOOLS_DIR   = REPO_ROOT / "output" / "tools"
OUTPUT_DIR  = REPO_ROOT / "output"
PROD_DIR    = REPO_ROOT / "output" / "production"
PALETTE_MD  = REPO_ROOT / "output" / "color" / "palettes" / "master_palette.md"
BASELINE_JSON = TOOLS_DIR / "qa_baseline_last.json"

# Cycle label — update each cycle
CYCLE_LABEL = "C39"

if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# ---------------------------------------------------------------------------
# Import QA tools
# ---------------------------------------------------------------------------
from LTG_TOOL_render_qa import qa_report, qa_batch
from LTG_TOOL_color_verify import verify_canonical_colors, get_canonical_palette
from LTG_TOOL_stub_linter import lint_directory as stub_lint_directory, format_report as stub_format_report
from LTG_TOOL_palette_warmth_lint import lint_palette_file, format_report as palette_format_report
from LTG_TOOL_glitch_spec_lint import lint_directory as glitch_lint_directory, format_report as glitch_format_report
from LTG_TOOL_readme_sync import audit as readme_sync_audit, format_report as readme_sync_format_report
from LTG_TOOL_motion_spec_lint import lint_motion_spec, format_report as motion_lint_format_report
import importlib.util as _importlib_util

from PIL import Image

# Arc-diff tool: loaded lazily to avoid import errors if Pillow not installed yet
_arc_diff_mod = None

def _load_arc_diff():
    """Lazily import LTG_TOOL_contact_sheet_arc_diff. Returns module or None."""
    global _arc_diff_mod
    if _arc_diff_mod is not None:
        return _arc_diff_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_contact_sheet_arc_diff",
            str(TOOLS_DIR / "LTG_TOOL_contact_sheet_arc_diff.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _arc_diff_mod = mod
        return mod
    except Exception:
        return None

# ---------------------------------------------------------------------------
# Target file collections
# ---------------------------------------------------------------------------

# Pitch PNGs: style frames (current versions as of C36) + brand logo + storyboard export
PITCH_PNGS = [
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_discovery.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_glitch_storm.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_otherside.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_luma_byte.png",
    PROD_DIR / "LTG_BRAND_logo.png",
    PROD_DIR / "storyboard_pitch_export.png",
]

# Style frames for color verification
STYLE_FRAMES = [
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_discovery.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_glitch_storm.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_otherside.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_luma_byte.png",
]

# Character sheets for proportion verification
# Each entry: (png_path, approximate_bbox as (x, y, w, h) or None for auto)
CHARACTER_SHEETS = [
    (OUTPUT_DIR / "characters" / "main" / "turnarounds" / "LTG_CHAR_luma_turnaround.png", None),
    (OUTPUT_DIR / "characters" / "main" / "turnarounds" / "LTG_CHAR_cosmo_turnaround.png", None),
    (OUTPUT_DIR / "characters" / "main" / "turnarounds" / "LTG_CHAR_miri_turnaround.png", None),
    (OUTPUT_DIR / "characters" / "main" / "turnarounds" / "LTG_CHAR_glitch_turnaround.png", None),
]

# Glitch generator scripts for spec lint
GLITCH_GENERATORS = list(TOOLS_DIR.glob("LTG_TOOL_glitch_*.py")) + \
                    list(TOOLS_DIR.glob("LTG_TOOL_style_frame_03_*.py")) + \
                    list(TOOLS_DIR.glob("LTG_TOOL_character_lineup_*.py"))

# Motion spec sheets for Section 8 lint (add new versions here each cycle)
MOTION_DIR = OUTPUT_DIR / "characters" / "motion"
MOTION_SHEETS = [
    # (path, expected_panel_count)
    (MOTION_DIR / "LTG_CHAR_luma_motion.png",  3),
    (MOTION_DIR / "LTG_CHAR_byte_motion.png",  4),
]

# Contact sheet pairs for arc-diff gate (Section 10).
# Each entry: (label, old_sheet_path, new_sheet_path)
# old = previous version, new = current version.
# Arc-diff output PNG saves to output/production/.
SB_DIR = OUTPUT_DIR / "storyboards"
ARC_DIFF_PAIRS = [
    (
        "Act 2 contact sheet v005→v006",
        SB_DIR / "act2" / "LTG_SB_act2_contact_sheet.png",
        SB_DIR / "act2" / "LTG_SB_act2_contact_sheet.png",
        PROD_DIR / "arc_diff_act2_c39.png",
    ),
    (
        "Act 1 cold open contact sheet v001→v002",
        SB_DIR / "LTG_SB_act1_coldopen_contact_sheet.png",
        SB_DIR / "LTG_SB_act1_coldopen_contact_sheet.png",
        PROD_DIR / "arc_diff_act1_c39.png",
    ),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _grade_line(grade: str) -> str:
    """Return a markdown badge for a grade string."""
    mapping = {
        "PASS":  "**PASS**",
        "WARN":  "**WARN**",
        "FAIL":  "**FAIL**",
        "ERROR": "**ERROR**",
        "SKIP":  "*SKIP*",
    }
    return mapping.get(grade.upper(), grade)


def _worst_grade(*grades) -> str:
    """Return the worst of several grade strings."""
    order = {"ERROR": 3, "FAIL": 2, "WARN": 1, "PASS": 0, "SKIP": -1}
    worst = max(grades, key=lambda g: order.get(g.upper(), -1))
    return worst.upper()


# ---------------------------------------------------------------------------
# Baseline I/O
# ---------------------------------------------------------------------------

def load_baseline() -> dict:
    """Load the previous run's QA baseline from qa_baseline_last.json.
    Returns an empty dict if no baseline exists."""
    if not BASELINE_JSON.exists():
        return {}
    try:
        return json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_baseline(snapshot: dict) -> None:
    """Write the current run's QA snapshot to qa_baseline_last.json."""
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    BASELINE_JSON.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")


def _make_snapshot(
    render_qa_res,
    color_verify_res,
    proportion_res,
    stub_lint_res,
    palette_lint_res,
    glitch_lint_res,
    readme_sync_res,
    motion_spec_res,
    run_ts: str,
    cycle: str,
) -> dict:
    """Build a compact snapshot dict from section results for persistence."""
    def _section(r, name):
        return {
            "section": name,
            "overall": r["overall"],
            "pass": r["pass"],
            "warn": r["warn"],
            "fail": r["fail"],
            "missing": r.get("missing", []),
            "flagged": r.get("flagged", []),
        }
    _all = [render_qa_res, color_verify_res, proportion_res,
            stub_lint_res, palette_lint_res, glitch_lint_res,
            readme_sync_res, motion_spec_res]
    return {
        "cycle": cycle,
        "run_ts": run_ts,
        "sections": {
            "render_qa":      _section(render_qa_res,      "Render QA"),
            "color_verify":   _section(color_verify_res,   "Color Verify"),
            "proportion":     _section(proportion_res,      "Proportion Verify"),
            "stub_linter":    _section(stub_lint_res,       "Stub Linter"),
            "palette_warmth": _section(palette_lint_res,    "Palette Warmth Lint"),
            "glitch_spec":    _section(glitch_lint_res,     "Glitch Spec Lint"),
            "readme_sync":    _section(readme_sync_res,     "README Sync"),
            "motion_spec":    _section(motion_spec_res,     "Motion Spec Lint"),
        },
        "totals": {
            "pass":  sum(r["pass"]  for r in _all),
            "warn":  sum(r["warn"]  for r in _all),
            "fail":  sum(r["fail"]  for r in _all),
        },
    }


# ---------------------------------------------------------------------------
# Delta report
# ---------------------------------------------------------------------------

def compute_delta(current_snapshot: dict, baseline: dict) -> dict:
    """
    Compare current snapshot against baseline.
    Returns a delta dict with:
        new_fails   — list of (section, item) newly FAIL since last run
        new_warns   — list of (section, item) newly WARN since last run
        resolved    — list of (section, item) that were FAIL/WARN, now cleared
        count_delta — dict: {fail: +N, warn: +N, resolved: N}
        has_baseline — bool
        summary     — formatted summary string
    """
    result = {
        "new_fails": [],
        "new_warns": [],
        "resolved": [],
        "count_delta": {"fail": 0, "warn": 0, "resolved": 0},
        "has_baseline": bool(baseline),
        "summary": "",
        "prev_cycle": baseline.get("cycle", "N/A"),
        "prev_ts": baseline.get("run_ts", "N/A"),
    }

    if not baseline:
        result["summary"] = "No baseline found — this run establishes the new baseline."
        return result

    prev_totals = baseline.get("totals", {})
    curr_totals = current_snapshot.get("totals", {})

    delta_fail = curr_totals.get("fail", 0) - prev_totals.get("fail", 0)
    delta_warn = curr_totals.get("warn", 0) - prev_totals.get("warn", 0)

    # Per-section flagged item delta
    prev_sections = baseline.get("sections", {})
    curr_sections = current_snapshot.get("sections", {})

    for sec_key, curr_sec in curr_sections.items():
        prev_sec = prev_sections.get(sec_key, {})
        prev_flagged = set(prev_sec.get("flagged", []))
        curr_flagged = set(curr_sec.get("flagged", []))

        sec_name = curr_sec.get("section", sec_key)

        # New items in current that weren't in previous
        for item in sorted(curr_flagged - prev_flagged):
            if "FAIL" in item.upper():
                result["new_fails"].append((sec_name, item.strip()))
            else:
                result["new_warns"].append((sec_name, item.strip()))

        # Items in previous that are gone now (resolved)
        for item in sorted(prev_flagged - curr_flagged):
            result["resolved"].append((sec_name, item.strip()))

    result["count_delta"]["fail"] = delta_fail
    result["count_delta"]["warn"] = delta_warn
    result["count_delta"]["resolved"] = len(result["resolved"])

    sign_f = "+" if delta_fail >= 0 else ""
    sign_w = "+" if delta_warn >= 0 else ""
    result["summary"] = (
        f"Delta since last run ({result['prev_cycle']} @ {result['prev_ts']}): "
        f"{sign_f}{delta_fail} FAIL, {sign_w}{delta_warn} WARN, "
        f"-{result['count_delta']['resolved']} resolved"
    )

    return result


# ---------------------------------------------------------------------------
# Section runners
# ---------------------------------------------------------------------------

def run_render_qa() -> dict:
    """
    Run LTG_TOOL_render_qa on all pitch PNGs.
    Returns a summary dict with counts and flagged items.

    render_qa result dict keys:
        file, asset_type, silhouette, value_range, color_fidelity,
        warm_cool, line_weight, overall_grade
    """
    results = []
    missing = []
    for p in PITCH_PNGS:
        if not p.exists():
            missing.append(str(p))
            continue
        r = qa_report(str(p))
        results.append(r)

    pass_count  = sum(1 for r in results if r.get("overall_grade") == "PASS")
    warn_count  = sum(1 for r in results if r.get("overall_grade") == "WARN")
    fail_count  = sum(1 for r in results if r.get("overall_grade") == "FAIL")

    # Sub-check names and their pass-flag key within the result dict
    CHECK_PASS_MAP = {
        "value_range":    lambda r: r.get("value_range", {}).get("pass", True),
        "color_fidelity": lambda r: r.get("color_fidelity", {}).get("overall_pass", True),
        "warm_cool":      lambda r: r.get("warm_cool", {}).get("pass", True)
                                    if "status" not in r.get("warm_cool", {}) else True,
        "line_weight":    lambda r: r.get("line_weight", {}).get("pass", True),
        "silhouette":     lambda r: r.get("silhouette", {}).get("score", "distinct") != "blob",
    }

    flagged = []
    for r in results:
        name = Path(r.get("file", "?")).name
        grade = r.get("overall_grade", "?")
        if grade in ("WARN", "FAIL"):
            for check_key, pass_fn in CHECK_PASS_MAP.items():
                try:
                    if not pass_fn(r):
                        detail = ""
                        sub = r.get(check_key, {})
                        if isinstance(sub, dict):
                            notes = sub.get("notes", [])
                            if notes:
                                detail = " — " + "; ".join(notes)
                            elif check_key == "silhouette":
                                detail = f" — score={sub.get('score', '?')}"
                        flagged.append(f"  - {name} / {check_key}: WARN{detail}")
                except Exception:
                    pass

    overall = "PASS"
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0 or missing:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "missing": missing,
        "flagged": flagged,
        "raw": results,
    }


def run_color_verify() -> dict:
    """
    Run LTG_TOOL_color_verify on all style frames.
    Returns a summary dict.
    """
    palette = get_canonical_palette()
    pass_count = 0
    warn_count = 0
    missing = []
    flagged = []

    for p in STYLE_FRAMES:
        if not p.exists():
            missing.append(str(p))
            continue
        try:
            img = Image.open(str(p)).convert("RGB")
            # Downscale if needed
            img.thumbnail((1280, 1280), Image.LANCZOS)
            result = verify_canonical_colors(img, palette)
            name = p.name
            if result.get("overall_pass"):
                pass_count += 1
            else:
                warn_count += 1
                for color_name, info in result.items():
                    if color_name == "overall_pass":
                        continue
                    if isinstance(info, dict) and not info.get("pass", True) and info.get("found_hue") is not None:
                        flagged.append(
                            f"  - {name} / {color_name}: hue drift {info.get('delta', '?'):.1f}° "
                            f"(target={info.get('target_hue', '?'):.0f}, found={info.get('found_hue', '?'):.0f})"
                        )
        except Exception as e:
            warn_count += 1
            flagged.append(f"  - {p.name}: exception — {e}")

    overall = "PASS" if warn_count == 0 and not missing else "WARN"
    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": 0,
        "missing": missing,
        "flagged": flagged,
    }


def run_proportion_verify() -> dict:
    """
    Run LTG_TOOL_proportion_verify on character turnaround sheets.
    Uses the programmatic API by importing and calling the core functions.
    Returns a summary dict.
    """
    # Import proportion verify internals
    sys.path.insert(0, str(TOOLS_DIR))
    import importlib
    pv = importlib.import_module("LTG_TOOL_proportion_verify")

    pass_count = 0
    warn_count = 0
    fail_count = 0
    missing = []
    flagged = []

    for sheet_path, bbox in CHARACTER_SHEETS:
        if not sheet_path.exists():
            missing.append(str(sheet_path))
            continue
        try:
            img = Image.open(str(sheet_path)).convert("RGBA")
            img.thumbnail((1280, 1280), Image.LANCZOS)
            W, H = img.size

            # Use full image as bounding box if none provided
            if bbox is None:
                x, y, w, h = 0, 0, W, H
            else:
                x, y, w, h = bbox

            # Crop to bounding box
            cropped = img.crop((x, y, x + w, y + h))

            # Detect background and occupied rows
            bg_color = pv.detect_background(cropped)
            occ = pv.occupied_rows(cropped, bg_color)
            extent = pv.find_character_extent(occ)

            if extent is None:
                warn_count += 1
                flagged.append(f"  - {sheet_path.name}: no character pixels detected — WARN")
                continue

            top_row, bottom_row = extent
            total_height = bottom_row - top_row + 1
            head_height, _method = pv.find_head_height(occ, top_row)

            if head_height is None or head_height <= 0:
                # Multi-view turnaround sheets: head gap detection fails on multi-panel layouts
                # (multiple characters side by side confuse the row-occupancy algorithm).
                # Flag as WARN — manual review recommended for turnarounds.
                warn_count += 1
                flagged.append(
                    f"  - {sheet_path.name}: head gap not found ({_method}) — "
                    "multi-panel turnaround may require manual proportion check — WARN"
                )
                continue

            ratio = total_height / head_height
            lo = pv.CANONICAL_RATIO * (1 - pv.RATIO_TOLERANCE)
            hi = pv.CANONICAL_RATIO * (1 + pv.RATIO_TOLERANCE)

            # Glitch uses a non-standard body proportion (diamond body), skip strict ratio
            if "glitch" in sheet_path.name.lower():
                pass_count += 1
                flagged.append(f"  - {sheet_path.name}: SKIP proportion check (Glitch non-humanoid)")
                continue

            if lo <= ratio <= hi:
                pass_count += 1
            else:
                grade = "WARN" if abs(ratio - pv.CANONICAL_RATIO) < 0.5 else "FAIL"
                msg = f"ratio={ratio:.2f} (spec={pv.CANONICAL_RATIO}, tol=±{pv.RATIO_TOLERANCE*100:.0f}%)"
                if grade == "FAIL":
                    fail_count += 1
                else:
                    warn_count += 1
                flagged.append(f"  - {sheet_path.name}: {grade} — {msg}")

        except Exception as e:
            warn_count += 1
            flagged.append(f"  - {sheet_path.name}: exception — {e}")

    overall = "PASS"
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0 or missing:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "missing": missing,
        "flagged": flagged,
    }


def run_stub_linter() -> dict:
    """
    Run LTG_TOOL_stub_linter on output/tools/.
    Returns a summary dict.

    stub_linter result dict keys:
        file, issues (list of dicts with line_no/statement/module/
        target_exists/canonical/canonical_exists), status ("PASS"|"WARN"|"ERROR")
    """
    results = stub_lint_directory(str(TOOLS_DIR), skip_legacy=True)

    pass_count  = sum(1 for r in results if r.get("status") == "PASS")
    warn_count  = sum(1 for r in results if r.get("status") == "WARN")
    error_count = sum(1 for r in results if r.get("status") == "ERROR")

    flagged = []
    for r in results:
        if r.get("status") in ("WARN", "ERROR"):
            name = Path(r.get("file", "?")).name
            for imp in r.get("issues", []):
                flagged.append(
                    f"  - {name}: [{r.get('status')}] `{imp.get('statement', '')}` "
                    f"(target_exists={imp.get('target_exists')}, "
                    f"canonical_exists={imp.get('canonical_exists')})"
                )

    overall = "PASS"
    if error_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": error_count,
        "missing": [],
        "flagged": flagged,
        "raw": results,
    }


def run_palette_warmth_lint() -> dict:
    """
    Run LTG_TOOL_palette_warmth_lint on master_palette.md.
    Checks CHAR-M (all entries) + CHAR-L hoodie entries (CHAR-L-04, -08, -11).
    Upgraded from v001 in C39 (Sam Kowalski) — now covers CHAR-L hoodie warmth guarantee.
    Returns a summary dict.
    """
    if not PALETTE_MD.exists():
        return {
            "overall": "FAIL",
            "pass": 0,
            "warn": 0,
            "fail": 1,
            "missing": [str(PALETTE_MD)],
            "flagged": [f"  - master_palette.md not found at {PALETTE_MD}"],
        }

    result = lint_palette_file(str(PALETTE_MD))
    flagged = []
    for v in result.get("violations", []):
        flagged.append(f"  - {v.get('code')} {v.get('name')} {v.get('hex')}: {v.get('reason')}")

    overall = result.get("result", "PASS")
    return {
        "overall": overall,
        "pass": result.get("total_checked", 0) - result.get("total_violations", 0),
        "warn": result.get("total_violations", 0),
        "fail": 0,
        "missing": [],
        "flagged": flagged,
    }


def run_readme_sync() -> dict:
    """
    Run LTG_TOOL_readme_sync — cross-check LTG_TOOL_*.py on disk vs README Script Index.
    Returns a summary dict.

    readme_sync_audit result dict keys:
        disk_tools, listed, legacy, unlisted, ghost, legacy_ghost, ok, result
    """
    result = readme_sync_audit(TOOLS_DIR)

    unlisted_count = len(result.get("unlisted", []))
    ghost_count    = len(result.get("ghost", []))
    legacy_ghost_count = len(result.get("legacy_ghost", []))
    ok_count       = len(result.get("ok", []))

    flagged = []
    for name in result.get("unlisted", []):
        flagged.append(f"  - UNLISTED: `{name}` (on disk, not in README Script Index)")
    for name in result.get("ghost", []):
        flagged.append(f"  - GHOST: `{name}` (in README, not on disk)")
    for name in result.get("legacy_ghost", []):
        flagged.append(f"  - LEGACY GHOST: `{name}` (marked retired, not in legacy/)")

    overall = "PASS" if result.get("result") == "PASS" else "WARN"
    total_discrepancies = unlisted_count + ghost_count + legacy_ghost_count

    return {
        "overall": overall,
        "pass": ok_count,
        "warn": total_discrepancies,
        "fail": 0,
        "missing": [],
        "flagged": flagged,
        "disk_total": len(result.get("disk_tools", [])),
        "listed_total": len(result.get("listed", [])),
        "unlisted_count": unlisted_count,
        "ghost_count": ghost_count,
        "legacy_ghost_count": legacy_ghost_count,
    }


def run_glitch_spec_lint() -> dict:
    """
    Run LTG_TOOL_glitch_spec_lint on all generators in output/tools/.
    Returns a summary dict.

    Note: lint_directory() in glitch_spec_lint only returns non-SKIP results
    (SKIP files are filtered internally). PASS/WARN counts are over Glitch
    generators only. Non-Glitch files are silently excluded.

    glitch_spec_lint result dict keys:
        file, is_glitch (bool), issues (list of str), status ("PASS"|"WARN")
    """
    results = glitch_lint_directory(str(TOOLS_DIR))

    pass_count  = sum(1 for r in results if r.get("status") == "PASS")
    warn_count  = sum(1 for r in results if r.get("status") == "WARN")
    fail_count  = 0  # glitch linter uses WARN for issues, not FAIL

    # Count total .py files to infer skipped count
    total_py = len([f for f in TOOLS_DIR.iterdir()
                    if f.suffix == ".py" and f.parent.name != "legacy"])
    skip_count = total_py - len(results)

    flagged = []
    for r in results:
        if r.get("status") == "WARN":
            name = Path(r.get("file", "?")).name
            for issue_str in r.get("issues", []):
                flagged.append(f"  - {name}: {issue_str}")

    overall = "PASS"
    if warn_count > 0:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "skip": skip_count,
        "missing": [],
        "flagged": flagged,
    }


def run_motion_spec_lint() -> dict:
    """
    Run LTG_TOOL_motion_spec_lint on all motion spec sheets.
    Returns a summary dict compatible with precritique_qa section format.

    Section 8 — Ryo Hasegawa / Cycle 39.
    """
    results = []
    missing = []
    for path, expected_panels in MOTION_SHEETS:
        if not path.exists():
            missing.append(str(path))
            continue
        r = lint_motion_spec(str(path), expected_panels=expected_panels)
        results.append(r)

    pass_count = sum(r["pass"] for r in results)
    warn_count = sum(r["warn"] for r in results)
    fail_count = sum(r["fail"] for r in results)

    flagged = []
    for r in results:
        fname = Path(r["file"]).name
        for item in r.get("flagged", []):
            flagged.append(f"  - {fname}: {item}")
        for m in r.get("missing", []):
            flagged.append(f"  - MISSING: {m}")

    overall = "PASS"
    if fail_count > 0 or missing:
        overall = "WARN"  # missing motion sheets → WARN (advisory, not block)
    elif warn_count > 0:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "missing": missing,
        "flagged": flagged,
    }


def run_arc_diff_gate() -> list:
    """
    Section 10 — Arc-Diff Gate (informational, not scored).

    For each contact sheet pair in ARC_DIFF_PAIRS:
      - If both files exist: run compare_contact_sheets() from arc-diff tool.
      - If CHANGED > 3: add NOTE listing changed panel slot indices.
      - If REMOVED > 0: add WARN (panel removal = story continuity risk).
      - If one/both files missing: skip with NOTE.

    Returns a list of result dicts, one per pair:
        {
            label       : str   — human-readable pair label
            old_path    : str
            new_path    : str
            diff_output : str | None — path to arc-diff PNG (if generated)
            skipped     : bool  — True if files were missing
            skip_reason : str | None
            ok          : bool  — comparison succeeded
            n_old       : int
            n_new       : int
            same        : int
            changed     : int
            added       : int
            removed     : int
            changed_slots : list[int]
            severity    : "PASS" | "NOTE" | "WARN"
            messages    : list[str]
        }
    """
    arc_mod = _load_arc_diff()
    results = []

    for label, old_path, new_path, diff_out in ARC_DIFF_PAIRS:
        entry = {
            "label": label,
            "old_path": str(old_path),
            "new_path": str(new_path),
            "diff_output": None,
            "skipped": False,
            "skip_reason": None,
            "ok": False,
            "n_old": 0, "n_new": 0,
            "same": 0, "changed": 0, "added": 0, "removed": 0,
            "changed_slots": [],
            "severity": "PASS",
            "messages": [],
        }

        # Check file availability
        old_exists = old_path.exists()
        new_exists = new_path.exists()
        if not old_exists or not new_exists:
            missing = []
            if not old_exists:
                missing.append(f"OLD: {old_path.name}")
            if not new_exists:
                missing.append(f"NEW: {new_path.name}")
            entry["skipped"] = True
            entry["skip_reason"] = "Missing: " + ", ".join(missing)
            entry["severity"] = "PASS"   # skipped ≠ failure
            entry["messages"].append(f"NOTE: Skipped — {entry['skip_reason']}")
            results.append(entry)
            continue

        if arc_mod is None:
            entry["skipped"] = True
            entry["skip_reason"] = "arc-diff module could not be loaded"
            entry["severity"] = "PASS"
            entry["messages"].append("NOTE: arc-diff tool unavailable — skipping")
            results.append(entry)
            continue

        # Run comparison
        try:
            r = arc_mod.compare_contact_sheets(str(old_path), str(new_path), str(diff_out))
            entry.update({
                "ok":           r["ok"],
                "n_old":        r["n_old"],
                "n_new":        r["n_new"],
                "same":         r["same"],
                "changed":      r["changed"],
                "added":        r["added"],
                "removed":      r["removed"],
                "changed_slots": r["changed_slots"],
                "diff_output":  r.get("diff_output"),
            })

            if not r["ok"]:
                entry["severity"] = "PASS"
                entry["messages"].append(f"NOTE: comparison error — {r.get('error', 'unknown')}")
            else:
                # Gate logic per spec
                severity = "PASS"
                if r["removed"] > 0:
                    severity = "WARN"
                    entry["messages"].append(
                        f"WARN: {r['removed']} panel(s) REMOVED — story continuity risk. "
                        f"Removed slots: {r['removed_slots']}"
                    )
                if r["changed"] > 3:
                    if severity == "PASS":
                        severity = "NOTE"
                    slots_str = ", ".join(str(s) for s in r["changed_slots"])
                    entry["messages"].append(
                        f"NOTE: {r['changed']} panel(s) CHANGED this cycle "
                        f"(slots: {slots_str}) — critics: focus review on these panels."
                    )
                if r["added"] > 0:
                    entry["messages"].append(
                        f"NOTE: {r['added']} panel(s) ADDED (new panels, not in prior version)."
                    )
                if not entry["messages"]:
                    entry["messages"].append(
                        f"PASS: {r['same']} panel(s) unchanged, "
                        f"{r['changed']} changed, {r['added']} added, {r['removed']} removed."
                    )
                entry["severity"] = severity
        except Exception as exc:
            entry["severity"] = "PASS"
            entry["messages"].append(f"NOTE: arc-diff exception — {exc}")

        results.append(entry)

    return results


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def build_report(
    render_qa_res,
    color_verify_res,
    proportion_res,
    stub_lint_res,
    palette_lint_res,
    glitch_lint_res,
    readme_sync_res,
    motion_spec_res,
    arc_diff_results: list,
    delta: dict,
    run_ts: str,
) -> str:
    """Compose the final Markdown report."""

    def section_header(title: str, result: dict) -> str:
        badge = _grade_line(result["overall"])
        return (
            f"## {title} — {badge}\n\n"
            f"PASS: {result['pass']}  WARN: {result['warn']}  FAIL: {result['fail']}  "
            f"Missing: {len(result.get('missing', []))}\n"
        )

    def flagged_block(result: dict) -> str:
        lines = []
        if result.get("missing"):
            lines.append("**Missing files:**")
            for m in result["missing"]:
                lines.append(f"  - {Path(m).name} (not found)")
        if result.get("flagged"):
            lines.append("**Flagged items:**")
            lines.extend(result["flagged"])
        return ("\n".join(lines) + "\n") if lines else "_No issues found._\n"

    # Overall score
    overall = _worst_grade(
        render_qa_res["overall"],
        color_verify_res["overall"],
        proportion_res["overall"],
        stub_lint_res["overall"],
        palette_lint_res["overall"],
        glitch_lint_res["overall"],
        readme_sync_res["overall"],
        motion_spec_res["overall"],
    )

    _all_sections = [render_qa_res, color_verify_res, proportion_res,
                     stub_lint_res, palette_lint_res, glitch_lint_res,
                     readme_sync_res, motion_spec_res]
    total_pass  = sum(r["pass"] for r in _all_sections)
    total_warn  = sum(r["warn"] for r in _all_sections)
    total_fail  = sum(r["fail"] for r in _all_sections)

    # README sync prominence flag
    readme_discrepancies = readme_sync_res.get("unlisted_count", 0) + readme_sync_res.get("ghost_count", 0)
    readme_warn_line = ""
    if readme_discrepancies > 0:
        readme_warn_line = (
            f"\n> **README SYNC WARNING:** {readme_discrepancies} discrepancy(ies) detected — "
            f"{readme_sync_res.get('unlisted_count', 0)} UNLISTED, "
            f"{readme_sync_res.get('ghost_count', 0)} GHOST. "
            "See Section 7 for details. Update README Script Index before critique.\n"
        )

    lines = [
        f"# Pre-Critique QA Report — {CYCLE_LABEL}",
        "",
        f"**Run date:** {run_ts}",
        f"**Script:** LTG_TOOL_precritique_qa.py v2.4.0",
        "",
        "---",
        "",
        "## Overall Result",
        "",
        f"**{overall}** — PASS: {total_pass}  WARN: {total_warn}  FAIL: {total_fail}",
    ]

    if readme_warn_line:
        lines.append(readme_warn_line)

    lines += [
        "",
        "| Section | Result | PASS | WARN | FAIL |",
        "|---|---|---|---|---|",
        f"| Render QA (pitch PNGs)         | {render_qa_res['overall']}   | {render_qa_res['pass']}  | {render_qa_res['warn']}  | {render_qa_res['fail']}  |",
        f"| Color Verify (style frames)    | {color_verify_res['overall']} | {color_verify_res['pass']} | {color_verify_res['warn']} | {color_verify_res['fail']} |",
        f"| Proportion Verify (char sheets)| {proportion_res['overall']}  | {proportion_res['pass']}  | {proportion_res['warn']}  | {proportion_res['fail']}  |",
        f"| Stub Linter (tools dir)        | {stub_lint_res['overall']}   | {stub_lint_res['pass']}   | {stub_lint_res['warn']}   | {stub_lint_res['fail']}   |",
        f"| Palette Warmth Lint            | {palette_lint_res['overall']}| {palette_lint_res['pass']}| {palette_lint_res['warn']}| {palette_lint_res['fail']}|",
        f"| Glitch Spec Lint               | {glitch_lint_res['overall']} | {glitch_lint_res['pass']} | {glitch_lint_res['warn']} | {glitch_lint_res['fail']} |",
        f"| README Script Index Sync       | {readme_sync_res['overall']} | {readme_sync_res['pass']} | {readme_sync_res['warn']} | {readme_sync_res['fail']} |",
        f"| Motion Spec Lint               | {motion_spec_res['overall']} | {motion_spec_res['pass']} | {motion_spec_res['warn']} | {motion_spec_res['fail']} |",
        "",
        "---",
        "",
    ]

    # Delta report section (prominent, before section details)
    lines.append("## 0. Delta Report")
    lines.append("")
    if delta["has_baseline"]:
        lines.append(f"**{delta['summary']}**")
        lines.append("")
        lines.append(f"_Compared against: {delta['prev_cycle']} run @ {delta['prev_ts']}_")
        lines.append("")

        if delta["new_fails"]:
            lines.append("**New FAILs since last run:**")
            for sec, item in delta["new_fails"]:
                lines.append(f"  - [{sec}] {item}")
            lines.append("")

        if delta["new_warns"]:
            lines.append("**New WARNs since last run:**")
            for sec, item in delta["new_warns"]:
                lines.append(f"  - [{sec}] {item}")
            lines.append("")

        if delta["resolved"]:
            lines.append("**Resolved since last run (previously WARN/FAIL, now PASS):**")
            for sec, item in delta["resolved"]:
                lines.append(f"  - [{sec}] {item}")
            lines.append("")

        if not delta["new_fails"] and not delta["new_warns"] and not delta["resolved"]:
            lines.append("_No changes in flagged items since last run._")
            lines.append("")
    else:
        lines.append("_No baseline found — this run establishes the initial baseline._")
        lines.append(f"_Baseline saved to: `{BASELINE_JSON.name}`_")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 1: Render QA
    lines.append(section_header("1. Render QA — Pitch PNGs", render_qa_res))
    lines.append("")
    lines.append("Target files:")
    for p in PITCH_PNGS:
        exists = "found" if p.exists() else "MISSING"
        lines.append(f"  - `{p.name}` ({exists})")
    lines.append("")
    lines.append(flagged_block(render_qa_res))
    lines.append("")

    # Section 2: Color Verify
    lines.append(section_header("2. Color Verify — Style Frames", color_verify_res))
    lines.append("")
    lines.append(flagged_block(color_verify_res))
    lines.append("")

    # Section 3: Proportion Verify
    lines.append(section_header("3. Proportion Verify — Character Sheets", proportion_res))
    lines.append("")
    lines.append(flagged_block(proportion_res))
    lines.append("")

    # Section 4: Stub Linter
    lines.append(section_header("4. Stub Linter — output/tools/", stub_lint_res))
    lines.append("")
    lines.append(flagged_block(stub_lint_res))
    lines.append("")

    # Section 5: Palette Warmth Lint
    lines.append(section_header("5. Palette Warmth Lint — master_palette.md", palette_lint_res))
    lines.append("")
    lines.append(flagged_block(palette_lint_res))
    lines.append("")

    # Section 6: Glitch Spec Lint
    lines.append(section_header("6. Glitch Spec Lint — Generators", glitch_lint_res))
    lines.append("")
    skip_n = glitch_lint_res.get("skip", 0)
    if skip_n:
        lines.append(f"_(Non-Glitch files: {skip_n} skipped)_")
        lines.append("")
    lines.append(flagged_block(glitch_lint_res))
    lines.append("")

    # Section 7: README Script Index Sync
    lines.append(section_header("7. README Script Index Sync", readme_sync_res))
    lines.append("")
    disk_total   = readme_sync_res.get("disk_total", "?")
    listed_total = readme_sync_res.get("listed_total", "?")
    lines.append(f"_(Tools on disk: {disk_total}  |  Tools listed in README: {listed_total})_")
    lines.append("")
    if readme_discrepancies > 0:
        lines.append(
            f"> **ACTION REQUIRED:** {readme_sync_res.get('unlisted_count', 0)} tool(s) on disk not listed in README "
            f"and {readme_sync_res.get('ghost_count', 0)} README entry(ies) with no corresponding file. "
            "Update `output/tools/README.md` Script Index before next critique cycle."
        )
        lines.append("")
    lines.append(flagged_block(readme_sync_res))
    lines.append("")

    # Section 8: Motion Spec Lint
    lines.append(section_header("8. Motion Spec Lint — motion sheets", motion_spec_res))
    lines.append("")
    lines.append("Target sheets:")
    for path, panels in MOTION_SHEETS:
        exists = "found" if path.exists() else "MISSING"
        lines.append(f"  - `{path.name}` (expected {panels} panels, {exists})")
    lines.append("")
    lines.append(flagged_block(motion_spec_res))
    lines.append("")

    # Section 9: Arc-Diff Gate (informational)
    lines.append("## 9. Arc-Diff Gate — Contact Sheet Changelog")
    lines.append("")
    lines.append("_Informational only — does not affect overall PASS/WARN/FAIL score._")
    lines.append("_WARN = panel removed (story continuity risk). NOTE = changed panels (critics: prioritize review of these)._")
    lines.append("")

    if not arc_diff_results:
        lines.append("_No contact sheet pairs configured._")
        lines.append("")
    else:
        for entry in arc_diff_results:
            label = entry["label"]
            severity = entry["severity"]
            lines.append(f"### {label}")
            if entry.get("skipped"):
                lines.append(f"  - *{entry.get('skip_reason', 'skipped')}*")
            else:
                lines.append(
                    f"  - OLD panels: {entry['n_old']}  "
                    f"NEW panels: {entry['n_new']}  "
                    f"SAME: {entry['same']}  "
                    f"CHANGED: {entry['changed']}  "
                    f"ADDED: {entry['added']}  "
                    f"REMOVED: {entry['removed']}"
                )
                if entry.get("diff_output"):
                    lines.append(f"  - Arc-diff PNG: `{Path(entry['diff_output']).name}`")
            for msg in entry.get("messages", []):
                prefix = "> **WARN:**" if msg.startswith("WARN:") else "_"
                suffix = "_" if msg.startswith("NOTE:") or msg.startswith("PASS:") else ""
                if msg.startswith("WARN:"):
                    lines.append(f"\n> **{msg}**\n")
                elif msg.startswith("NOTE:") or msg.startswith("PASS:"):
                    lines.append(f"  - _{msg}_")
                else:
                    lines.append(f"  - {msg}")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by LTG_TOOL_precritique_qa.py v2.6.0 — Morgan Walsh (arc-diff gate S9 + lineup suppression expansion C39)*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    run_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[precritique_qa] Starting {CYCLE_LABEL} QA pipeline — {run_ts}")
    print(f"[precritique_qa] Repo root: {REPO_ROOT}")

    # Load previous baseline before running
    baseline = load_baseline()
    if baseline:
        print(f"[precritique_qa] Loaded baseline from {baseline.get('cycle', '?')} run @ {baseline.get('run_ts', '?')}")
    else:
        print("[precritique_qa] No baseline found — this run will establish the baseline.")

    print("[1/8] Running Render QA on pitch PNGs...")
    render_qa_res = run_render_qa()
    print(f"      → {render_qa_res['overall']} (PASS={render_qa_res['pass']}, WARN={render_qa_res['warn']}, FAIL={render_qa_res['fail']}, MISSING={len(render_qa_res['missing'])})")

    print("[2/8] Running Color Verify on style frames...")
    color_verify_res = run_color_verify()
    print(f"      → {color_verify_res['overall']} (PASS={color_verify_res['pass']}, WARN={color_verify_res['warn']})")

    print("[3/8] Running Proportion Verify on character turnarounds...")
    proportion_res = run_proportion_verify()
    print(f"      → {proportion_res['overall']} (PASS={proportion_res['pass']}, WARN={proportion_res['warn']}, FAIL={proportion_res['fail']})")

    print("[4/8] Running Stub Linter on output/tools/...")
    stub_lint_res = run_stub_linter()
    print(f"      → {stub_lint_res['overall']} (PASS={stub_lint_res['pass']}, WARN={stub_lint_res['warn']}, ERROR={stub_lint_res['fail']})")

    print("[5/8] Running Palette Warmth Lint on master_palette.md...")
    palette_lint_res = run_palette_warmth_lint()
    print(f"      → {palette_lint_res['overall']} (checked={palette_lint_res['pass'] + palette_lint_res['warn']}, violations={palette_lint_res['warn']})")

    print("[6/8] Running Glitch Spec Lint on generators...")
    glitch_lint_res = run_glitch_spec_lint()
    print(f"      → {glitch_lint_res['overall']} (PASS={glitch_lint_res['pass']}, WARN={glitch_lint_res['warn']}, FAIL={glitch_lint_res['fail']}, SKIP={glitch_lint_res.get('skip',0)})")

    print("[7/8] Running README Script Index Sync audit...")
    readme_sync_res = run_readme_sync()
    # Prominently report README WARN to console
    if readme_sync_res["warn"] > 0:
        print(f"      → {readme_sync_res['overall']} *** README SYNC WARN: {readme_sync_res.get('unlisted_count',0)} UNLISTED, {readme_sync_res.get('ghost_count',0)} GHOST — update README before critique! ***")
    else:
        print(f"      → {readme_sync_res['overall']} (OK={readme_sync_res['pass']}, UNLISTED/GHOST={readme_sync_res['warn']}, disk={readme_sync_res.get('disk_total','?')}, listed={readme_sync_res.get('listed_total','?')})")

    print("[8/9] Running Motion Spec Lint on motion sheets...")
    motion_spec_res = run_motion_spec_lint()
    print(f"      → {motion_spec_res['overall']} (PASS={motion_spec_res['pass']}, WARN={motion_spec_res['warn']}, FAIL={motion_spec_res['fail']}, MISSING={len(motion_spec_res['missing'])})")

    print("[9/9] Running Arc-Diff Gate on contact sheet pairs...")
    arc_diff_results = run_arc_diff_gate()
    for ad in arc_diff_results:
        sev = ad["severity"]
        if ad.get("skipped"):
            print(f"      → {ad['label']}: SKIP ({ad.get('skip_reason', '')})")
        else:
            msgs = "; ".join(m[:80] for m in ad.get("messages", [])[:2])
            print(f"      → {ad['label']}: {sev} — {msgs}")

    # Build snapshot and compute delta
    current_snapshot = _make_snapshot(
        render_qa_res, color_verify_res, proportion_res,
        stub_lint_res, palette_lint_res, glitch_lint_res, readme_sync_res,
        motion_spec_res,
        run_ts, CYCLE_LABEL,
    )
    delta = compute_delta(current_snapshot, baseline)
    print(f"\n[delta] {delta['summary']}")

    # Save new baseline
    save_baseline(current_snapshot)
    print(f"[precritique_qa] Baseline saved to: {BASELINE_JSON}")

    report_md = build_report(
        render_qa_res,
        color_verify_res,
        proportion_res,
        stub_lint_res,
        palette_lint_res,
        glitch_lint_res,
        readme_sync_res,
        motion_spec_res,
        arc_diff_results,
        delta,
        run_ts,
    )

    PROD_DIR.mkdir(parents=True, exist_ok=True)
    report_path = PROD_DIR / f"precritique_qa_{CYCLE_LABEL.lower()}.md"
    report_path.write_text(report_md, encoding="utf-8")
    print(f"\n[precritique_qa] Report written to: {report_path}")

    # Determine exit code
    overall = _worst_grade(
        render_qa_res["overall"],
        color_verify_res["overall"],
        proportion_res["overall"],
        stub_lint_res["overall"],
        palette_lint_res["overall"],
        glitch_lint_res["overall"],
        readme_sync_res["overall"],
        motion_spec_res["overall"],
    )

    print(f"[precritique_qa] OVERALL: {overall}")

    if overall == "PASS":
        return 0
    elif overall == "WARN":
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
