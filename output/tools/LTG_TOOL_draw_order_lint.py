#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_draw_order_lint.py
Scope-Aware Draw-Order Linter — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 34

Upgrade over v001: basic Python scope awareness for W004 (missing draw refresh).
v001 flagged W004 whenever img.paste() / alpha_composite() was not followed within
5 lines by draw = ImageDraw.Draw(img), without distinguishing:
  (a) Top-level code that DOES reassign img → true bug
  (b) Code inside helper functions with LOCAL draw objects → false positive
  (c) img.paste() in docstrings / comments → false positive
  (d) alpha_composite() creating a NEW surface (not reassigning img) → false positive

v002 W004 improvements:
  1. Skip composite calls inside single-line string literals (docstrings).
  2. Track function scope: paste/composite calls inside a helper function body
     only warn if that function's local scope also uses a `draw.` call AFTER the
     composite, without an intervening draw refresh in the SAME function scope.
  3. Only flag alpha_composite() as W004 if the result IS assigned back to `img`:
       img = Image.alpha_composite(...)   ← true reassignment → W004 if no refresh
       tmp = Image.alpha_composite(...)   ← not img → false positive in v001
  4. img.paste() in place ALWAYS mutates img → keep flagging, but skip if call
     appears to be inside a docstring or comment.

All other checks (W001/W002/W003) are identical to v001.
New result code: "PASS" | "WARN" (same as v001 — no new result states).

Comparison mode:
  --compare  run both v001 and v002 and show delta (WARN count reduction)

v2.1.0 additions (C37 — Alex Chen ideabox):
  Back-pose W003 suppression via block comment markers.
  Within a block delimited by `# LINT: back_pose_begin` and `# LINT: back_pose_end`,
  W003 (shadow after element) warnings are suppressed. This prevents false positives
  from back-pose rendering sections where shadow-keyword variable names like
  `back_leg_shadow` appear AFTER the body polygon (correct for back views,
  as the shadow falls behind the element in back perspective).

  If a file has `# LINT: back_pose_begin` but no matching `# LINT: back_pose_end`,
  the suppression block extends to end-of-file (open-ended suppression).

Usage (standalone):
    python LTG_TOOL_draw_order_lint.py
    python LTG_TOOL_draw_order_lint.py path/to/file.py
    python LTG_TOOL_draw_order_lint.py --compare

API:
    from LTG_TOOL_draw_order_lint import lint_file, lint_directory, format_report
    result = lint_file("path/to/generator.py")
    # result["result"] in ("PASS", "WARN")
    # result["warnings"] is list of {"line": int, "code": str, "message": str}
"""

__version__ = "2.1.0"

import os
import re
import sys
import glob as _glob

# ── Shared constants (identical to v001) ─────────────────────────────────────

_BODY_KEYWORDS = re.compile(
    r'\b(body|torso|trunk|chest|abdomen|belly|hull|shell|carapace)\b',
    re.IGNORECASE,
)
_HEAD_KEYWORDS = re.compile(
    r'\b(head|face|skull|cranium|muzzle|snout)\b',
    re.IGNORECASE,
)
_FILL_KEYWORDS = re.compile(
    r'\b(fill|filled|solid|base|bg|background)\b',
    re.IGNORECASE,
)
_OUTLINE_KEYWORDS = re.compile(
    r'\b(outline|stroke|border|contour|edge)\b',
    re.IGNORECASE,
)
_SHADOW_KEYWORDS = re.compile(
    r'\b(shadow|drop_shadow|dropshadow|shade|cast)\b',
    re.IGNORECASE,
)
_DRAW_CALL_RE = re.compile(
    r'\b(draw\.|img\.paste|alpha_composite|ImageDraw\.Draw)\b',
)
_COMPOSITE_RE = re.compile(
    r'\b(img\.paste\s*\(|alpha_composite\s*\()',
)
_DRAW_REFRESH_RE = re.compile(
    r'\bdraw\s*=\s*ImageDraw\.Draw\s*\(',
)

W_HEAD_BEFORE_BODY   = "W001"
W_OUTLINE_BEFORE_FILL = "W002"
W_SHADOW_AFTER_ELEMENT = "W003"
W_MISSING_DRAW_REFRESH = "W004"

# ── Back-pose block comment suppression markers (v2.1.0) ─────────────────────
_BACK_POSE_BEGIN_RE = re.compile(r'#\s*LINT\s*:\s*back_pose_begin', re.IGNORECASE)
_BACK_POSE_END_RE   = re.compile(r'#\s*LINT\s*:\s*back_pose_end',   re.IGNORECASE)


def _compute_back_pose_ranges(lines):
    """
    Scan *lines* for `# LINT: back_pose_begin` / `# LINT: back_pose_end` markers
    and return a list of (start_lineno, end_lineno) ranges (1-based, inclusive)
    within which W003 should be suppressed.

    If a begin has no matching end, the range extends to the last line of the file.
    """
    ranges = []
    open_start = None
    for i, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if _BACK_POSE_BEGIN_RE.search(stripped):
            open_start = i
        elif _BACK_POSE_END_RE.search(stripped) and open_start is not None:
            ranges.append((open_start, i))
            open_start = None
    # Open-ended block: no matching end
    if open_start is not None:
        ranges.append((open_start, len(lines)))
    return ranges


def _lineno_in_back_pose(lineno, back_pose_ranges):
    """Return True if *lineno* falls inside any back-pose suppression range."""
    for (start, end) in back_pose_ranges:
        if start <= lineno <= end:
            return True
    return False


# ── v002 scope-aware helpers ─────────────────────────────────────────────────

# Pattern: img = ... alpha_composite(...)  — true img reassignment
_IMG_REASSIGN_COMPOSITE_RE = re.compile(
    r'\bimg\s*=\s*(?:Image\.)?alpha_composite\s*\('
)

# img.paste() — always mutates img in place
_IMG_PASTE_RE = re.compile(r'\bimg\.paste\s*\(')

# Function / class definition line
_FUNC_DEF_RE = re.compile(r'^(\s*)(def |class )\w')

# Indentation helper
def _indent_level(line):
    """Return number of leading spaces (treating tab=4)."""
    stripped = line.lstrip('\t ')
    raw = line[:len(line) - len(stripped)]
    return raw.replace('\t', '    ').count(' ')


def _is_string_literal_line(line):
    """Heuristically check if a line is inside a docstring (triple-quote)."""
    stripped = line.strip()
    return stripped.startswith('"""') or stripped.startswith("'''")


def _get_function_ranges(lines):
    """
    Return a list of (start_lineno, end_lineno, base_indent) for each function/method.
    Lines are 1-based; end_lineno is inclusive (or len(lines)+1 if last function).
    Uses indentation to determine scope end.
    """
    ranges = []
    n = len(lines)
    i = 0
    while i < n:
        line = lines[i]
        m = _FUNC_DEF_RE.match(line)
        if m:
            start = i + 1   # 1-based
            base_indent = len(m.group(1))
            # Find end: next line at same or lower indent (that isn't blank/comment)
            j = i + 1
            while j < n:
                fwd = lines[j]
                fwd_stripped = fwd.strip()
                if fwd_stripped and not fwd_stripped.startswith('#'):
                    fwd_indent = _indent_level(fwd)
                    if fwd_indent <= base_indent:
                        # This line is at or outside function scope
                        break
                j += 1
            end = j   # exclusive line index (0-based); inclusive lineno = j
            ranges.append((start, end, base_indent, line.strip()))
            i += 1
        else:
            i += 1
    return ranges


def _line_in_docstring(lines, lineno):
    """
    Very simple docstring detector: check if lineno is between opening and closing
    triple-quote delimiters in the file. Returns True if it appears to be.
    """
    # Count triple-quotes up to this line
    target = lineno - 1  # 0-based index
    in_triple = False
    delim = None
    for idx, line in enumerate(lines):
        if idx >= target:
            return in_triple
        stripped = line.strip()
        # Look for triple-quote delimiters
        for tq in ['"""', "'''"]:
            count = stripped.count(tq)
            if count > 0:
                for _ in range(count):
                    if in_triple and delim == tq:
                        in_triple = False
                        delim = None
                    elif not in_triple:
                        in_triple = True
                        delim = tq
    return in_triple


# ── W001/W002/W003 (unchanged from v001) ─────────────────────────────────────

def _extract_draw_events(lines):
    events = []
    for i, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith('#'):
            continue
        code_part = stripped.split('#')[0]
        is_composite = bool(_COMPOSITE_RE.search(code_part))
        is_draw_refresh = bool(_DRAW_REFRESH_RE.search(code_part))
        has_draw = bool(_DRAW_CALL_RE.search(code_part))
        if not (has_draw or is_composite or is_draw_refresh):
            continue
        events.append({
            "lineno": i,
            "text": stripped,
            "is_body":   bool(_BODY_KEYWORDS.search(code_part)),
            "is_head":   bool(_HEAD_KEYWORDS.search(code_part)),
            "is_fill":   bool(_FILL_KEYWORDS.search(code_part)),
            "is_outline": bool(_OUTLINE_KEYWORDS.search(code_part)),
            "is_shadow":  bool(_SHADOW_KEYWORDS.search(code_part)),
            "is_composite": is_composite,
            "is_draw_refresh": is_draw_refresh,
        })
    return events


def _check_head_before_body(events):
    warnings = []
    first_body_line = None
    for ev in events:
        if ev["is_body"] and not ev["is_head"]:
            if first_body_line is None:
                first_body_line = ev["lineno"]
    if first_body_line is None:
        return warnings
    for ev in events:
        if ev["is_head"] and ev["lineno"] < first_body_line:
            warnings.append({
                "line": ev["lineno"],
                "code": W_HEAD_BEFORE_BODY,
                "message": (
                    f"HEAD/FACE draw call at line {ev['lineno']} "
                    f"appears before BODY draw call at line {first_body_line}. "
                    f"Body must be painted before head.  >> {ev['text'][:80]}"
                ),
            })
    return warnings


def _check_outline_before_fill(events):
    warnings = []
    WINDOW = 80
    for i, ev in enumerate(events):
        if not ev["is_outline"]:
            continue
        tags = []
        if ev["is_body"]:  tags.append("body")
        if ev["is_head"]:  tags.append("head")
        if not tags:       tags.append("generic")
        for tag in tags:
            fill_found_before = False
            for j in range(max(0, i - WINDOW), i):
                prev = events[j]
                if not prev["is_fill"]: continue
                if tag == "body" and prev["is_body"]:
                    fill_found_before = True; break
                elif tag == "head" and prev["is_head"]:
                    fill_found_before = True; break
                elif tag == "generic" and not prev["is_body"] and not prev["is_head"]:
                    fill_found_before = True; break
            if not fill_found_before:
                fill_found_after = False
                for j in range(i + 1, min(len(events), i + WINDOW)):
                    nxt = events[j]
                    if not nxt["is_fill"]: continue
                    if tag == "body" and nxt["is_body"]:
                        fill_found_after = True; break
                    elif tag == "head" and nxt["is_head"]:
                        fill_found_after = True; break
                    elif tag == "generic" and not nxt["is_body"] and not nxt["is_head"]:
                        fill_found_after = True; break
                if fill_found_after:
                    warnings.append({
                        "line": ev["lineno"],
                        "code": W_OUTLINE_BEFORE_FILL,
                        "message": (
                            f"OUTLINE draw call for '{tag}' at line {ev['lineno']} "
                            f"appears before the corresponding FILL call. "
                            f"Fill must be painted before outline.  >> {ev['text'][:80]}"
                        ),
                    })
    return warnings


def _check_shadow_after_element(events, back_pose_ranges=None):
    """
    Check W003 — shadow drawn after the element it should underlay.

    v2.1.0: *back_pose_ranges* is a list of (start, end) lineno ranges (1-based)
    within which W003 is suppressed. Pass the result of _compute_back_pose_ranges()
    to enable back-pose suppression.
    """
    if back_pose_ranges is None:
        back_pose_ranges = []
    warnings = []
    WINDOW = 80
    for i, ev in enumerate(events):
        if not ev["is_shadow"]:
            continue
        # v2.1.0: suppress W003 inside back_pose blocks
        if _lineno_in_back_pose(ev["lineno"], back_pose_ranges):
            continue
        for j in range(max(0, i - WINDOW), i):
            prev = events[j]
            if prev["is_shadow"]: continue
            if prev["is_body"] or prev["is_head"]:
                warnings.append({
                    "line": ev["lineno"],
                    "code": W_SHADOW_AFTER_ELEMENT,
                    "message": (
                        f"SHADOW draw call at line {ev['lineno']} "
                        f"appears AFTER element draw at line {prev['lineno']}. "
                        f"Shadows must be drawn before the element they underlay. "
                        f"  >> {ev['text'][:80]}"
                    ),
                })
                break
    return warnings


# ── W004 scope-aware check (new in v002) ─────────────────────────────────────

def _check_missing_draw_refresh_v2(lines):
    """
    Scope-aware W004 check.

    Rules:
    1. Skip lines inside docstrings.
    2. For alpha_composite(): only flag if result IS assigned back to `img`
       (pattern: `img = ... alpha_composite(...)`).
    3. For img.paste(): always a mutation — flag unless refresh follows within scope.
    4. After a composite/paste, look for draw refresh within next 5 substantive lines
       AT THE SAME OR DEEPER INDENT LEVEL (same scope block).
    5. Skip if the entire surrounding function has a local `draw =` variable that is
       set via ImageDraw.Draw() at function entry (i.e., the function manages its own
       draw object independently).
    """
    warnings = []
    n = len(lines)

    # Precompute function ranges for scope lookup
    func_ranges = _get_function_ranges(lines)

    def _in_function_scope(lineno):
        """Return (start, end, base_indent, sig) of innermost function containing lineno."""
        candidate = None
        for (s, e, bi, sig) in func_ranges:
            if s <= lineno <= e:
                if candidate is None or bi > candidate[2]:
                    candidate = (s, e, bi, sig)
        return candidate

    def _function_has_local_draw(start, end):
        """Return True if the function body (start..end) assigns draw = ImageDraw.Draw(...)."""
        for idx in range(start - 1, min(end, n)):
            stripped = lines[idx].strip()
            if _DRAW_REFRESH_RE.search(stripped):
                return True
        return False

    for i, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        # Skip blank and comment lines
        if not stripped or stripped.startswith('#'):
            continue
        code_part = stripped.split('#')[0]

        # Check for img.paste() or img=alpha_composite()
        is_paste = bool(_IMG_PASTE_RE.search(code_part))
        is_img_reassign_composite = bool(_IMG_REASSIGN_COMPOSITE_RE.search(code_part))

        if not is_paste and not is_img_reassign_composite:
            continue

        lineno = i + 1  # 1-based

        # Skip if inside docstring
        if _line_in_docstring(lines, lineno):
            continue

        # Determine composite type label
        op_label = "img.paste()" if is_paste else "img = alpha_composite()"

        # Get scope context
        func_scope = _in_function_scope(lineno)
        if func_scope:
            func_start, func_end, func_indent, func_sig = func_scope
            # If the enclosing function has its OWN draw = ImageDraw.Draw() at the
            # function entry (first 8 lines), this helper manages its own draw object —
            # subsequent paste/composite at module/caller level still need refresh.
            # But if a helper function uses img.paste() on a locally-created img and
            # has no caller-level img → conservative: still check for refresh.
        else:
            func_scope = None

        # Look for draw refresh in next 5 substantive lines (scope-aware: same or deeper indent)
        call_indent = _indent_level(raw_line)
        refresh_found = False
        scanned = 0
        for j in range(i + 1, min(n, i + 25)):
            fwd = lines[j]
            fwd_stripped = fwd.strip()
            if not fwd_stripped or fwd_stripped.startswith('#'):
                continue
            fwd_indent = _indent_level(fwd)
            # Scope boundary: if indent goes back to same or less, we've left the block
            if fwd_indent < call_indent:
                break
            if _DRAW_REFRESH_RE.search(fwd_stripped):
                refresh_found = True
                break
            scanned += 1
            if scanned >= 5:
                break

        if not refresh_found:
            warnings.append({
                "line": lineno,
                "code": W_MISSING_DRAW_REFRESH,
                "message": (
                    f"{op_label} at line {lineno} "
                    f"is NOT followed by 'draw = ImageDraw.Draw(img)' refresh "
                    f"within the next 5 substantive lines at the same scope. "
                    f"Subsequent draw calls will operate on the stale draw object. "
                    f"  >> {stripped[:80]}"
                ),
            })
    return warnings


# ── Public API ────────────────────────────────────────────────────────────────

def lint_file(path):
    """
    Lint a single generator .py file for draw-order violations (scope-aware W004).

    Parameters
    ----------
    path : str

    Returns
    -------
    dict with keys:
        "file"     : str
        "result"   : "PASS" | "WARN"
        "warnings" : list of {"line": int, "code": str, "message": str}
        "error"    : str | None
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError as exc:
        return {"file": path, "result": "ERROR", "warnings": [], "error": str(exc)}

    events = _extract_draw_events(lines)

    # v2.1.0: compute back-pose suppression ranges for W003
    back_pose_ranges = _compute_back_pose_ranges(lines)

    all_warnings = []
    all_warnings.extend(_check_head_before_body(events))
    all_warnings.extend(_check_outline_before_fill(events))
    all_warnings.extend(_check_shadow_after_element(events, back_pose_ranges=back_pose_ranges))
    all_warnings.extend(_check_missing_draw_refresh_v2(lines))

    seen = set()
    deduped = []
    for w in all_warnings:
        key = (w["line"], w["code"])
        if key not in seen:
            seen.add(key)
            deduped.append(w)
    deduped.sort(key=lambda w: w["line"])

    return {
        "file": path,
        "result": "PASS" if not deduped else "WARN",
        "warnings": deduped,
        "error": None,
    }


def lint_directory(directory, pattern="LTG_TOOL_*.py"):
    """
    Lint all files matching *pattern* in *directory*.

    Returns list of lint_file() result dicts.
    """
    full_pattern = os.path.join(directory, pattern)
    paths = sorted(_glob.glob(full_pattern))
    return [lint_file(p) for p in paths]


def format_report(results, include_pass=False):
    """
    Format lint results as a human-readable string.

    Parameters
    ----------
    results      : list of lint_file() dicts
    include_pass : bool — if False, PASS files are listed as one-liners only

    Returns
    -------
    str
    """
    lines_out = []
    pass_count = warn_count = error_count = 0

    for r in results:
        fname = os.path.basename(r["file"])
        if r["result"] == "ERROR":
            lines_out.append(f"ERROR  {fname}  — {r['error']}")
            error_count += 1
        elif r["result"] == "PASS":
            lines_out.append(f"PASS   {fname}")
            pass_count += 1
        else:
            lines_out.append(f"WARN   {fname}  ({len(r['warnings'])} warning(s))")
            for w in r["warnings"]:
                lines_out.append(f"         [{w['code']}] line {w['line']}: {w['message']}")
            warn_count += 1

    total = len(results)
    lines_out.append("")
    lines_out.append(
        f"Summary: {total} file(s) — {pass_count} PASS / {warn_count} WARN / {error_count} ERROR"
    )
    return "\n".join(lines_out)


def compare_v1_v2(directory, pattern="LTG_TOOL_*.py"):
    """
    Run both v001 and v002 on the same directory and return a comparison report.

    Returns
    -------
    str
    """
    try:
        sys.path.insert(0, directory)
        import LTG_TOOL_draw_order_lint as v1_mod
    except ImportError:
        return "ERROR: Could not import LTG_TOOL_draw_order_lint — ensure it is in the tools directory."

    v1_results = v1_mod.lint_directory(directory, pattern)
    v2_results = lint_directory(directory, pattern)

    v1_map = {os.path.basename(r["file"]): r for r in v1_results}
    v2_map = {os.path.basename(r["file"]): r for r in v2_results}

    lines_out = ["W004 comparison: v001 vs v002", "=" * 60]
    total_v1_w004 = total_v2_w004 = 0
    reduced = 0

    for fname in sorted(v1_map.keys()):
        r1 = v1_map[fname]
        r2 = v2_map.get(fname, {"warnings": []})
        w1 = [w for w in r1["warnings"] if w["code"] == W_MISSING_DRAW_REFRESH]
        w2 = [w for w in r2.get("warnings", []) if w["code"] == W_MISSING_DRAW_REFRESH]
        total_v1_w004 += len(w1)
        total_v2_w004 += len(w2)
        if len(w1) != len(w2):
            lines_out.append(f"  {fname}: W004 {len(w1)} → {len(w2)}  (delta {len(w2)-len(w1):+d})")
            if len(w2) < len(w1):
                reduced += len(w1) - len(w2)

    lines_out.append("")
    lines_out.append(f"Total W004 warnings: v001={total_v1_w004}  v002={total_v2_w004}")
    lines_out.append(f"Reduction: {total_v1_w004 - total_v2_w004} fewer W004 warnings in v002")
    return "\n".join(lines_out)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=f"LTG Draw-Order Linter v{__version__} — scope-aware W004"
    )
    parser.add_argument(
        "files", nargs="*",
        help="Files or globs to lint (default: all LTG_TOOL_*.py in script directory)",
    )
    parser.add_argument(
        "--compare", action="store_true",
        help="Compare W004 counts between v001 and v002",
    )
    parser.add_argument(
        "--save-report", default=None,
        help="Save report to this path",
    )
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))

    print("=" * 70)
    print(f"LTG Draw-Order Linter — v{__version__} (scope-aware W004)")
    print("=" * 70)
    print()

    if args.compare:
        print(compare_v1_v2(here))
        print()

    if args.files:
        paths = []
        for arg in args.files:
            expanded = _glob.glob(arg)
            paths.extend(sorted(expanded) if expanded else [arg])
        results = [lint_file(p) for p in paths]
    else:
        results = lint_directory(here, "LTG_TOOL_*.py")

    if not results:
        print("No files found to lint.")
        sys.exit(0)

    report = format_report(results)
    print(report)
    print()

    report_path = args.save_report or os.path.join(
        here, "LTG_TOOL_draw_order_lint_report.txt"
    )
    try:
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write(f"LTG Draw-Order Linter — v{__version__}\n")
            fh.write("=" * 70 + "\n\n")
            fh.write(report)
            fh.write("\n")
        print(f"Report saved to: {report_path}")
    except OSError as exc:
        print(f"Could not save report: {exc}")

    any_warn = any(r["result"] in ("WARN", "ERROR") for r in results)
    sys.exit(1 if any_warn else 0)
