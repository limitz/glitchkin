#!/usr/bin/env python3
"""
LTG_TOOL_proportion_audit_v001.py
Proportion Audit Tool — "Luma & the Glitchkin"

Scans all LTG_TOOL_styleframe_*.py files in output/tools/ and
LTG_TOOL_style_frame_*.py files in output/tools/ (and legacy source
locations), extracts the numeric constants for:
  - head_r / HR  (head radius)
  - ew / eye_w   (eye half-width)
then computes ew/HR ratio and reports PASS / WARN / FAIL against
canonical spec:
  CANONICAL: ew = HR × 0.22  (PASS if within ±0.01, i.e. 0.21–0.23)

Usage:
    python3 LTG_TOOL_proportion_audit_v001.py

Output:
    Printed report + writes output/production/proportion_audit_c31.md
"""

import os
import re
import ast
import sys

# ── Config ────────────────────────────────────────────────────────────────────
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
# TOOLS_DIR = .../output/tools; PROJECT_ROOT = .../  (two levels up)
PROJECT_ROOT = os.path.dirname(os.path.dirname(TOOLS_DIR))
REPORT_PATH = os.path.join(PROJECT_ROOT, "output", "production", "proportion_audit_c31.md")

CANONICAL_RATIO = 0.22
PASS_TOLERANCE  = 0.01   # ±0.01 → [0.21, 0.23] passes
WARN_TOLERANCE  = 0.03   # ±0.03 → [0.19, 0.25] warns; outside = FAIL


def _ratio_verdict(ratio):
    """Return PASS / WARN / FAIL string based on ratio proximity to canonical."""
    if ratio is None:
        return "N/A"
    delta = abs(ratio - CANONICAL_RATIO)
    if delta <= PASS_TOLERANCE:
        return "PASS"
    elif delta <= WARN_TOLERANCE:
        return "WARN"
    else:
        return "FAIL"


# ── Regex extractors ──────────────────────────────────────────────────────────

def _extract_head_r(source):
    """
    Return (expr_str, numeric_value_or_None) for head_r or HR assignment.
    Looks for patterns like:
        head_r = p(72)
        head_r = int(h * 0.12)
        HR = 72
        head_r = p(72)  (with scale captured separately)
    Returns the *first* Luma-relevant match (avoids Byte/Cosmo head_r).
    Strategy: find all assignments, return first match with context note.
    """
    patterns = [
        # head_r = p(N)
        (r'\bhead_r\s*=\s*p\((\d+)\)', 'p(N)', lambda m: int(m.group(1))),
        # head_r = int(N)
        (r'\bhead_r\s*=\s*int\((\d+)\)', 'int(N)', lambda m: int(m.group(1))),
        # head_r = N  (bare integer)
        (r'\bhead_r\s*=\s*(\d+)\b', 'bare int', lambda m: int(m.group(1))),
        # head_r = int(h * 0.NN)  — float fraction
        (r'\bhead_r\s*=\s*int\(\s*\w+\s*\*\s*([\d.]+)\s*\)', 'int(h*factor)', None),
        # HR = N
        (r'\bHR\s*=\s*(\d+)\b', 'HR=N', lambda m: int(m.group(1))),
    ]
    for pat, label, extractor in patterns:
        m = re.search(pat, source)
        if m:
            expr = m.group(0).strip()
            val = extractor(m) if extractor else None
            return expr, val
    return None, None


def _extract_ew(source):
    """
    Return (expr_str, numeric_or_formula) for ew / eye_w.
    Looks for:
        ew  = int(head_r * 0.22)
        ew  = p(18)
        eye_w = max(4, head_w // 4)
        eye_w = head_w // N
    """
    patterns = [
        # ew = int(head_r * ratio)
        (r'\bew\s*=\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)', 'int(head_r*ratio)', None),
        # ew = p(N)
        (r'\bew\s*=\s*p\((\d+)\)', 'p(N)', lambda m: int(m.group(1))),
        # ew = int(N)
        (r'\bew\s*=\s*int\((\d+)\)', 'int(N)', lambda m: int(m.group(1))),
        # ew = N  (bare int)
        (r'\bew\s*=\s*(\d+)\b', 'bare int', lambda m: int(m.group(1))),
        # eye_w = max(N, head_w // M)
        (r'\beye_w\s*=\s*max\([^)]+\)', 'max(N,head_w//M)', None),
        # eye_w = head_w // N
        (r'\beye_w\s*=\s*head_w\s*//\s*(\d+)', 'head_w//N', None),
        # eye_w = int(head_r * ratio)
        (r'\beye_w\s*=\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)', 'int(head_r*ratio)', None),
    ]
    for pat, label, extractor in patterns:
        m = re.search(pat, source)
        if m:
            expr = m.group(0).strip()
            val = extractor(m) if extractor else None
            return expr, val
    return None, None


def _compute_ratio(head_r_expr, head_r_val, ew_expr, ew_val, source):
    """
    Attempt to compute numeric ew/HR ratio.
    Strategy:
      1. If ew = int(head_r * N): ratio = N directly
      2. If ew = p(N) and head_r = p(M): ratio = N/M
      3. If ew = int(head_r * ratio): parse ratio from ew_expr
      4. If eye_w = max(4, head_w // 4): try head_w//4 logic:
           head_w = int(head_h * 0.85) typically; head_h = h//5
           head_r ≈ head_h/2 → ratio ≈ (head_w/4)/(head_r) ≈ complex
         → mark as N/A (pixel-art style, canonical spec N/A)
    """
    if ew_expr is None:
        return None, "no ew found"

    # Case 1: ew = int(head_r * N) — extract ratio directly
    m = re.match(r'\bew\s*=\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)', ew_expr)
    if m:
        return float(m.group(1)), "direct ratio"

    # Case 2: ew = p(N) and head_r = p(M)
    if ew_val is not None and head_r_val is not None:
        # ew = p(N) with N pixels, head_r = p(M) with M pixels
        # ratio = N/M
        m_ew = re.match(r'\bew\s*=\s*p\((\d+)\)', ew_expr)
        m_hr = re.match(r'\bhead_r\s*=\s*p\((\d+)\)', head_r_expr) if head_r_expr else None
        if m_ew and m_hr:
            return int(m_ew.group(1)) / int(m_hr.group(1)), "p(N)/p(M)"
        # bare integer case
        if ew_val and head_r_val:
            return ew_val / head_r_val, "N/M"

    # Case 3: ew = int(HR * N)
    m = re.match(r'\bew\s*=\s*int\(\s*HR\s*\*\s*([\d.]+)\s*\)', ew_expr)
    if m:
        return float(m.group(1)), "HR ratio"

    # Case 4: pixel-art / head_w//N style — not organic spec
    if 'head_w' in ew_expr or 'eye_w' in ew_expr:
        return None, "pixel-art style (N/A)"

    # Case 5: ew = p(N) but no head_r = p(M) found (scale-relative)
    m_ew = re.match(r'\bew\s*=\s*p\((\d+)\)', ew_expr)
    m_hr_p = re.search(r'\bhead_r\s*=\s*p\((\d+)\)', source)
    if m_ew and m_hr_p:
        return int(m_ew.group(1)) / int(m_hr_p.group(1)), "p(N)/p(M)"

    return None, "could not resolve"


# ── Stub detection ────────────────────────────────────────────────────────────

def _is_stub(source):
    """Return True if the file is a naming stub (re-exports from another module)."""
    return 'import *' in source and ('from LTG_COLOR_' in source or
                                      'from LTG_TOOL_style_frame_' in source)


def _stub_source_path(source, stub_dir):
    """For a stub file, return the path to the real source module."""
    # Pattern: from LTG_COLOR_xxx import *
    m = re.search(r'from\s+(LTG_COLOR_\S+|LTG_TOOL_style_frame_\S+)\s+import', source)
    if not m:
        return None
    modname = m.group(1)
    # Try tools dir first
    candidate = os.path.join(stub_dir, modname + '.py')
    if os.path.exists(candidate):
        return candidate
    # Try color/style_frames dir (stub_dir = .../output/tools; go up two levels for project root)
    sf_dir = os.path.join(os.path.dirname(os.path.dirname(stub_dir)), 'output', 'color', 'style_frames')
    candidate2 = os.path.join(sf_dir, modname + '.py')
    if os.path.exists(candidate2):
        return candidate2
    return None


# ── Luma presence detection ───────────────────────────────────────────────────

def _has_luma(source, filename):
    """
    Heuristic: does this file draw Luma with organic eyes?
    Returns (has_luma: bool, note: str)
    """
    # SF02 Glitch Storm: Luma is in full sprint, no eyes drawn
    if 'glitch_storm' in filename:
        # Check if _draw_luma has eye drawing
        if re.search(r'draw.*eye|eye.*draw|ew\s*=', source):
            return True, "Luma with eyes"
        return False, "Luma: sprint pose, no eyes (canonical N/A)"

    # SF03 Other Side: pixel-art Luma
    if 'other_side' in filename:
        if 'eye_w' in source and 'head_w' in source:
            return True, "Luma: pixel-art style (organic spec N/A)"
        return True, "Luma: pixel-art style (organic spec N/A)"

    # SF01/SF04: organic Luma
    if 'discovery' in filename or 'luma_byte' in filename:
        return True, "Luma: organic style"

    # Generic: if source mentions luma and eye
    if 'luma' in source.lower() and ('ew' in source or 'eye_w' in source):
        return True, "Luma with eyes (detected)"

    return False, "no Luma detected"


# ── Main scan ─────────────────────────────────────────────────────────────────

def scan_styleframe_files():
    """Scan all styleframe generator files and return list of result dicts."""
    # Collect candidate files: both naming patterns
    candidates = []
    for fname in os.listdir(TOOLS_DIR):
        if fname.endswith('.py') and (
            fname.startswith('LTG_TOOL_styleframe_') or
            fname.startswith('LTG_TOOL_style_frame_')
        ):
            candidates.append(os.path.join(TOOLS_DIR, fname))

    # Also check output/color/style_frames for source files not covered by stubs
    # Only add if no file with the same filename is already in candidates
    candidate_names = {os.path.basename(p) for p in candidates}
    sf_dir = os.path.join(PROJECT_ROOT, 'output', 'color', 'style_frames')
    if os.path.isdir(sf_dir):
        for fname in os.listdir(sf_dir):
            if fname.endswith('.py') and (
                fname.startswith('LTG_TOOL_styleframe_') or
                fname.startswith('LTG_TOOL_style_frame_')
            ) and fname not in candidate_names:
                fpath = os.path.join(sf_dir, fname)
                candidates.append(fpath)
                candidate_names.add(fname)

    candidates.sort()
    results = []

    for fpath in candidates:
        fname = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            source = f.read()

        is_stub = _is_stub(source)
        resolved_path = fpath
        resolved_fname = fname
        stub_note = ""

        if is_stub:
            real_path = _stub_source_path(source, TOOLS_DIR)
            if real_path and os.path.exists(real_path):
                resolved_path = real_path
                resolved_fname = os.path.basename(real_path)
                stub_note = f"[stub → {resolved_fname}]"
                with open(resolved_path, 'r', encoding='utf-8') as f:
                    source = f.read()
            else:
                stub_note = "[stub → source not found]"

        has_luma, luma_note = _has_luma(source, fname)

        head_r_expr, head_r_val = _extract_head_r(source)
        ew_expr, ew_val = _extract_ew(source)

        ratio, ratio_method = _compute_ratio(head_r_expr, head_r_val,
                                              ew_expr, ew_val, source)

        # Determine verdict
        # Pixel-art and no-eyes cases: mark N/A
        if 'N/A' in luma_note or 'no eyes' in luma_note or 'no Luma' in luma_note:
            verdict = "N/A"
        elif ew_expr is None:
            verdict = "N/A (no ew found)"
        elif 'pixel-art' in (ratio_method or ''):
            verdict = "N/A (pixel-art style)"
        else:
            verdict = _ratio_verdict(ratio)

        results.append({
            'filename': fname,
            'stub_note': stub_note,
            'luma_note': luma_note,
            'head_r_expr': head_r_expr or '—',
            'ew_expr': ew_expr or '—',
            'ratio': ratio,
            'ratio_method': ratio_method,
            'verdict': verdict,
        })

    return results


def format_report(results):
    """Format results as a markdown report string."""
    lines = []
    lines.append("# Proportion Audit — C31")
    lines.append("")
    lines.append("**Canonical spec:** `ew = HR × 0.22`")
    lines.append("**PASS:** ratio within 0.21–0.23  |  **WARN:** 0.19–0.25  |  **FAIL:** outside 0.19–0.25")
    lines.append("**N/A:** file has no organic Luma eyes (sprint pose, pixel-art, or no Luma)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Results")
    lines.append("")

    # Table
    lines.append("| File | Luma Context | head_r expr | ew expr | ew/HR ratio | Status |")
    lines.append("|------|-------------|-------------|---------|-------------|--------|")

    pass_count = warn_count = fail_count = na_count = 0

    for r in results:
        ratio_str = f"{r['ratio']:.4f}" if r['ratio'] is not None else "—"
        verdict = r['verdict']
        fname_display = r['filename']
        if r['stub_note']:
            fname_display += f" {r['stub_note']}"

        lines.append(
            f"| `{fname_display}` "
            f"| {r['luma_note']} "
            f"| `{r['head_r_expr']}` "
            f"| `{r['ew_expr']}` "
            f"| {ratio_str} "
            f"| **{verdict}** |"
        )

        if verdict.startswith("PASS"):
            pass_count += 1
        elif verdict.startswith("WARN"):
            warn_count += 1
        elif verdict.startswith("FAIL"):
            fail_count += 1
        else:
            na_count += 1

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **PASS:** {pass_count}")
    lines.append(f"- **WARN:** {warn_count}")
    lines.append(f"- **FAIL:** {fail_count}")
    lines.append(f"- **N/A:** {na_count}")
    lines.append(f"- **Total files scanned:** {len(results)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- **SF01 (discovery):** Organic Luma. C30 fix corrected `ew = p(18)` (≈0.25) → `int(head_r * 0.22)`. v004 should PASS.")
    lines.append("- **SF02 (glitch_storm):** Luma in sprint pose — no eyes drawn. ew/HR not applicable.")
    lines.append("- **SF03 (other_side):** Pixel-art Luma — `eye_w = max(4, head_w // 4)`. Organic spec intentionally not applied.")
    lines.append("- **SF04 (luma_byte):** Latest version is v003. Stubs redirect to LTG_COLOR_* source files.")
    lines.append("- Files marked as stubs were resolved to their actual source for analysis.")
    lines.append("")
    lines.append(f"*Generated by `LTG_TOOL_proportion_audit_v001.py` — Cycle 31*")

    return "\n".join(lines)


def print_console_report(results):
    """Print a compact console report."""
    print("=" * 72)
    print("LTG PROPORTION AUDIT — C31")
    print(f"Canonical spec: ew = HR × {CANONICAL_RATIO} (PASS ±{PASS_TOLERANCE})")
    print("=" * 72)
    print()

    col_w = 52
    for r in results:
        fname = r['filename']
        if r['stub_note']:
            fname += f" {r['stub_note']}"
        ratio_str = f"{r['ratio']:.4f}" if r['ratio'] is not None else "  N/A "
        print(f"  {fname[:col_w]:<{col_w}}  ratio={ratio_str}  [{r['verdict']}]")
        print(f"    head_r: {r['head_r_expr']}")
        print(f"    ew:     {r['ew_expr']}")
        print(f"    note:   {r['luma_note']}")
        print()

    pass_c  = sum(1 for r in results if r['verdict'].startswith("PASS"))
    warn_c  = sum(1 for r in results if r['verdict'].startswith("WARN"))
    fail_c  = sum(1 for r in results if r['verdict'].startswith("FAIL"))
    na_c    = sum(1 for r in results if r['verdict'].startswith("N/A"))

    print("-" * 72)
    print(f"  PASS={pass_c}  WARN={warn_c}  FAIL={fail_c}  N/A={na_c}  "
          f"(total={len(results)})")
    print("=" * 72)


def main():
    results = scan_styleframe_files()

    if not results:
        print("No styleframe generator files found.")
        sys.exit(1)

    print_console_report(results)

    report_md = format_report(results)
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_md)
    print(f"\nReport written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
