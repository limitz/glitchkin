"""
LTG_TOOL_draw_order_lint_v001.py
=================================
Static draw-order linter for "Luma & the Glitchkin" generator scripts.

Parses .py generator files using regex/string pattern matching (no AST,
no execution) and flags dangerous painter's-algorithm violations:

  1. HEAD / FACE drawn before BODY
  2. OUTLINE drawn before FILL for the same element
  3. SHADOW drawn after the element it should darken
  4. img.paste() / alpha_composite() NOT followed by draw = ImageDraw.Draw(img) refresh

Author: Kai Nakamura (Technical Art Engineer)
Created: Cycle 31 — 2026-03-29
Version: 1.0.0

Usage (standalone):
    python LTG_TOOL_draw_order_lint_v001.py [files_or_glob ...]
    python LTG_TOOL_draw_order_lint_v001.py output/tools/LTG_TOOL_*.py

    When run with no arguments from within output/tools/, lints all
    LTG_TOOL_*.py files in the current directory.

Programmatic:
    from LTG_TOOL_draw_order_lint_v001 import lint_file, lint_directory
    report = lint_file("path/to/generator.py")
    # report["result"] in ("PASS", "WARN")
    # report["warnings"] is a list of {"line": int, "code": str, "message": str}
"""

import os
import re
import sys
import glob as _glob


# ---------------------------------------------------------------------------
# Draw-call keyword tables
# ---------------------------------------------------------------------------

# Keywords that strongly indicate a "body/torso fill" draw call
_BODY_KEYWORDS = re.compile(
    r'\b(body|torso|trunk|chest|abdomen|belly|hull|shell|carapace)\b',
    re.IGNORECASE,
)

# Keywords that strongly indicate a "head/face fill" draw call
_HEAD_KEYWORDS = re.compile(
    r'\b(head|face|skull|cranium|muzzle|snout)\b',
    re.IGNORECASE,
)

# Keywords indicating a fill draw call (must precede outline of same element)
_FILL_KEYWORDS = re.compile(
    r'\b(fill|filled|solid|base|bg|background)\b',
    re.IGNORECASE,
)

# Keywords indicating an outline/stroke call
_OUTLINE_KEYWORDS = re.compile(
    r'\b(outline|stroke|border|contour|edge)\b',
    re.IGNORECASE,
)

# Keywords indicating a shadow call
_SHADOW_KEYWORDS = re.compile(
    r'\b(shadow|drop_shadow|dropshadow|shade|cast)\b',
    re.IGNORECASE,
)

# Actual PIL draw calls — lines that contain a draw primitive on an identified layer
_DRAW_CALL_RE = re.compile(
    r'\b(draw\.|img\.paste|alpha_composite|ImageDraw\.Draw)\b',
)

# img.paste() or alpha_composite() call
_COMPOSITE_RE = re.compile(
    r'\b(img\.paste\s*\(|alpha_composite\s*\()',
)

# draw = ImageDraw.Draw(img)  — refresh pattern (any assignment form)
_DRAW_REFRESH_RE = re.compile(
    r'\bdraw\s*=\s*ImageDraw\.Draw\s*\(',
)


# ---------------------------------------------------------------------------
# Warning codes
# ---------------------------------------------------------------------------

W_HEAD_BEFORE_BODY = "W001"
W_OUTLINE_BEFORE_FILL = "W002"
W_SHADOW_AFTER_ELEMENT = "W003"
W_MISSING_DRAW_REFRESH = "W004"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_draw_events(lines):
    """
    Walk *lines* (list of str) and emit a sequence of draw events.

    Each event is a dict:
        {
            "lineno":    int,         # 1-based
            "text":      str,         # stripped line text
            "is_body":   bool,
            "is_head":   bool,
            "is_fill":   bool,
            "is_outline": bool,
            "is_shadow":  bool,
            "is_composite": bool,     # img.paste / alpha_composite
            "is_draw_refresh": bool,  # draw = ImageDraw.Draw(img)
        }

    Only lines that contain actual PIL draw calls or compositing calls are
    included; purely comment / assignment / import lines are skipped unless
    they match a draw pattern.
    """
    events = []
    for i, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()

        # Skip pure comments
        if stripped.startswith('#'):
            continue

        # Remove inline comment for matching purposes
        code_part = stripped.split('#')[0]

        is_composite = bool(_COMPOSITE_RE.search(code_part))
        is_draw_refresh = bool(_DRAW_REFRESH_RE.search(code_part))

        # Only record draw-relevant lines
        has_draw = bool(_DRAW_CALL_RE.search(code_part))
        if not (has_draw or is_composite or is_draw_refresh):
            continue

        events.append({
            "lineno": i,
            "text": stripped,
            "is_body": bool(_BODY_KEYWORDS.search(code_part)),
            "is_head": bool(_HEAD_KEYWORDS.search(code_part)),
            "is_fill": bool(_FILL_KEYWORDS.search(code_part)),
            "is_outline": bool(_OUTLINE_KEYWORDS.search(code_part)),
            "is_shadow": bool(_SHADOW_KEYWORDS.search(code_part)),
            "is_composite": is_composite,
            "is_draw_refresh": is_draw_refresh,
        })
    return events


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def _check_head_before_body(events):
    """
    Flag any head/face draw call that appears before the first body draw call.

    Returns list of warning dicts.
    """
    warnings = []
    first_body_line = None
    for ev in events:
        if ev["is_body"] and not ev["is_head"]:
            if first_body_line is None:
                first_body_line = ev["lineno"]

    if first_body_line is None:
        # No body draw found — can't determine order; skip
        return warnings

    for ev in events:
        if ev["is_head"] and ev["lineno"] < first_body_line:
            warnings.append({
                "line": ev["lineno"],
                "code": W_HEAD_BEFORE_BODY,
                "message": (
                    f"HEAD/FACE draw call at line {ev['lineno']} "
                    f"appears before BODY draw call at line {first_body_line}. "
                    f"Body must be painted before head. "
                    f"  >> {ev['text'][:80]}"
                ),
            })
    return warnings


def _check_outline_before_fill(events):
    """
    For each semantic element (body/head/shadow), flag outline calls that
    appear before a fill call for the same element.

    Strategy: within a contiguous block (up to 80 lines), detect outline
    preceding fill for the same element category.
    """
    warnings = []
    # We look for (outline + element tag) preceding (fill + same element tag)
    # within a proximity window to reduce false positives.
    WINDOW = 80

    for i, ev in enumerate(events):
        if not ev["is_outline"]:
            continue
        # Determine which element categories this outline applies to
        tags = []
        if ev["is_body"]:
            tags.append("body")
        if ev["is_head"]:
            tags.append("head")
        if not tags:
            # Generic outline — look for a generic fill that should precede it
            tags.append("generic")

        # Search backward (within WINDOW events) for a fill of the same tag
        # that has NOT yet appeared — i.e., fill comes AFTER this outline
        for tag in tags:
            fill_found_before = False
            for j in range(max(0, i - WINDOW), i):
                prev = events[j]
                if not prev["is_fill"]:
                    continue
                if tag == "body" and prev["is_body"]:
                    fill_found_before = True
                    break
                elif tag == "head" and prev["is_head"]:
                    fill_found_before = True
                    break
                elif tag == "generic" and not prev["is_body"] and not prev["is_head"]:
                    fill_found_before = True
                    break

            if not fill_found_before:
                # Check that a fill of matching tag actually exists AFTER this outline
                fill_found_after = False
                for j in range(i + 1, min(len(events), i + WINDOW)):
                    nxt = events[j]
                    if not nxt["is_fill"]:
                        continue
                    if tag == "body" and nxt["is_body"]:
                        fill_found_after = True
                        break
                    elif tag == "head" and nxt["is_head"]:
                        fill_found_after = True
                        break
                    elif tag == "generic" and not nxt["is_body"] and not nxt["is_head"]:
                        fill_found_after = True
                        break

                if fill_found_after:
                    warnings.append({
                        "line": ev["lineno"],
                        "code": W_OUTLINE_BEFORE_FILL,
                        "message": (
                            f"OUTLINE draw call for '{tag}' at line {ev['lineno']} "
                            f"appears before the corresponding FILL call. "
                            f"Fill must be painted before outline. "
                            f"  >> {ev['text'][:80]}"
                        ),
                    })
    return warnings


def _check_shadow_after_element(events):
    """
    Flag shadow draw calls that appear AFTER the main element they should underlay.

    A shadow should be drawn BEFORE the element it darkens. If a shadow call
    appears after a non-shadow body/head draw call within the same block (≤80
    events), it is suspicious.
    """
    warnings = []
    WINDOW = 80

    for i, ev in enumerate(events):
        if not ev["is_shadow"]:
            continue

        # Look backward for a non-shadow body/head draw call
        for j in range(max(0, i - WINDOW), i):
            prev = events[j]
            if prev["is_shadow"]:
                continue
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
                break  # one warning per shadow call is enough
    return warnings


def _check_missing_draw_refresh(lines):
    """
    Scan raw lines for img.paste() / alpha_composite() calls not followed
    (within the next 5 non-blank, non-comment lines) by
    draw = ImageDraw.Draw(img).

    Returns list of warning dicts.
    """
    warnings = []
    n = len(lines)

    for i, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        if stripped.startswith('#'):
            continue
        code_part = stripped.split('#')[0]

        if not _COMPOSITE_RE.search(code_part):
            continue

        # Found a paste/composite call — scan ahead for refresh
        refresh_found = False
        scanned = 0
        for j in range(i + 1, min(n, i + 20)):
            fwd = lines[j].strip()
            if not fwd or fwd.startswith('#'):
                continue
            if _DRAW_REFRESH_RE.search(fwd):
                refresh_found = True
                break
            scanned += 1
            if scanned >= 5:
                break

        if not refresh_found:
            warnings.append({
                "line": i + 1,  # 1-based
                "code": W_MISSING_DRAW_REFRESH,
                "message": (
                    f"img.paste() / alpha_composite() at line {i + 1} "
                    f"is NOT followed by 'draw = ImageDraw.Draw(img)' refresh "
                    f"within the next 5 substantive lines. "
                    f"Subsequent draw calls will operate on the stale draw object. "
                    f"  >> {stripped[:80]}"
                ),
            })
    return warnings


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def lint_file(path):
    """
    Lint a single generator .py file for draw-order violations.

    Parameters
    ----------
    path : str
        Absolute or relative path to the .py file.

    Returns
    -------
    dict with keys:
        "file"     : str — path as provided
        "result"   : "PASS" | "WARN"
        "warnings" : list of {"line": int, "code": str, "message": str}
        "error"    : str | None — populated if file could not be read
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError as exc:
        return {
            "file": path,
            "result": "ERROR",
            "warnings": [],
            "error": str(exc),
        }

    events = _extract_draw_events(lines)

    all_warnings = []
    all_warnings.extend(_check_head_before_body(events))
    all_warnings.extend(_check_outline_before_fill(events))
    all_warnings.extend(_check_shadow_after_element(events))
    all_warnings.extend(_check_missing_draw_refresh(lines))

    # De-duplicate warnings at the same line with the same code
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

    Parameters
    ----------
    directory : str
    pattern   : str — glob pattern relative to directory

    Returns
    -------
    list of lint_file() result dicts, sorted by filename.
    """
    full_pattern = os.path.join(directory, pattern)
    paths = sorted(_glob.glob(full_pattern))
    return [lint_file(p) for p in paths]


def format_report(results):
    """
    Format a list of lint_file() results as a human-readable string.

    Parameters
    ----------
    results : list of dicts (output of lint_file / lint_directory)

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


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    args = sys.argv[1:]

    if args:
        # Expand any globs provided on the command line
        paths = []
        for arg in args:
            expanded = _glob.glob(arg)
            if expanded:
                paths.extend(sorted(expanded))
            else:
                paths.append(arg)  # let lint_file report the missing-file error
        results = [lint_file(p) for p in paths]
    else:
        # Default: lint all LTG_TOOL_*.py in current directory
        here = os.path.dirname(os.path.abspath(__file__))
        results = lint_directory(here, "LTG_TOOL_*.py")

    if not results:
        print("No files found to lint.")
        sys.exit(0)

    print("=" * 70)
    print("LTG Draw-Order Linter — v1.0.0")
    print("=" * 70)
    print()
    print(format_report(results))
    print()

    # Save results to a report file alongside this script
    report_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "LTG_TOOL_draw_order_lint_v001_report.txt",
    )
    try:
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write("LTG Draw-Order Linter — v1.0.0\n")
            fh.write("=" * 70 + "\n\n")
            fh.write(format_report(results))
            fh.write("\n")
        print(f"Report saved to: {report_path}")
    except OSError as exc:
        print(f"Could not save report: {exc}")

    any_warn = any(r["result"] in ("WARN", "ERROR") for r in results)
    sys.exit(1 if any_warn else 0)
