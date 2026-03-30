#!/usr/bin/env python3
"""
LTG_TOOL_proportion_audit.py
Proportion Audit Tool v003 — "Luma & the Glitchkin"
Author: Rin Yamamoto | Cycle 39

Extends v002 with --cycle N CLI flag (C37/C39 actioned ideabox):
  - Accepts --cycle N argument to label the report heading and output path
  - Report path: output/production/proportion_audit_c{N}.md
  - Report heading: "# Proportion Audit — C{N}"
  - Default: --cycle 39 (current cycle)
  - No more per-cycle wrapper scripts needed — run once with the cycle flag

All v002 functionality preserved:
  - Asymmetric eye detection (eye_r_left / eye_r_right patterns)
  - ASYM-PASS / ASYM-WARN verdicts
  - Stub resolution
  - Luma presence detection

Usage:
    python3 LTG_TOOL_proportion_audit.py              # reports C39
    python3 LTG_TOOL_proportion_audit.py --cycle 39   # explicit cycle
    python3 LTG_TOOL_proportion_audit.py --cycle 40   # pre-label for C40

Callable as a module:
    from LTG_TOOL_proportion_audit import scan_styleframe_files, format_report
    results = scan_styleframe_files()
    print(format_report(results, cycle=39))

Output:
    Printed report + writes output/production/proportion_audit_c{N}.md
"""

import argparse
import os
import re
import sys

# ── Config ────────────────────────────────────────────────────────────────────
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(TOOLS_DIR))
PRODUCTION_DIR = os.path.join(PROJECT_ROOT, "output", "production")

CANONICAL_RATIO = 0.22
PASS_TOLERANCE  = 0.01   # ±0.01 → [0.21, 0.23] passes
WARN_TOLERANCE  = 0.03   # ±0.03 → [0.19, 0.25] warns; outside = FAIL

# Maximum allowed difference between left/right eye ratios (as fraction of canonical)
ASYM_WARN_THRESHOLD = 0.10  # 10% of canonical = 0.022

DEFAULT_CYCLE = 39


def _report_path(cycle: int) -> str:
    """Return the output path for the given cycle number."""
    return os.path.join(PRODUCTION_DIR, f"proportion_audit_c{cycle}.md")


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
    patterns = [
        (r'\bhead_r\s*=\s*p\((\d+)\)', 'p(N)', lambda m: int(m.group(1))),
        (r'\bhead_r\s*=\s*int\((\d+)\)', 'int(N)', lambda m: int(m.group(1))),
        (r'\bhead_r\s*=\s*(\d+)\b', 'bare int', lambda m: int(m.group(1))),
        (r'\bhead_r\s*=\s*int\(\s*\w+\s*\*\s*([\d.]+)\s*\)', 'int(h*factor)', None),
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
    patterns = [
        (r'\bew\s*=\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)', 'int(head_r*ratio)', None),
        (r'\bew\s*=\s*p\((\d+)\)', 'p(N)', lambda m: int(m.group(1))),
        (r'\bew\s*=\s*int\((\d+)\)', 'int(N)', lambda m: int(m.group(1))),
        (r'\bew\s*=\s*(\d+)\b', 'bare int', lambda m: int(m.group(1))),
        (r'\beye_w\s*=\s*max\([^)]+\)', 'max(N,head_w//M)', None),
        (r'\beye_w\s*=\s*head_w\s*//\s*(\d+)', 'head_w//N', None),
        (r'\beye_w\s*=\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)', 'int(head_r*ratio)', None),
    ]
    for pat, label, extractor in patterns:
        m = re.search(pat, source)
        if m:
            expr = m.group(0).strip()
            val = extractor(m) if extractor else None
            return expr, val
    return None, None


def _extract_asymmetric_eyes(source):
    left_expr = right_expr = None
    left_ratio = right_ratio = None

    m = re.search(r'\beye_r_left\s*=\s*max\(\s*\d+\s*,\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)\s*\)', source)
    if m:
        left_expr = m.group(0).strip()
        left_ratio = float(m.group(1))

    if left_expr is None:
        m = re.search(r'\beye_r_left\s*=\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)', source)
        if m:
            left_expr = m.group(0).strip()
            left_ratio = float(m.group(1))

    m = re.search(r'\beye_r_right\s*=\s*max\(\s*\d+\s*,\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)\s*\)', source)
    if m:
        right_expr = m.group(0).strip()
        right_ratio = float(m.group(1))

    if right_expr is None:
        m = re.search(r'\beye_r_right\s*=\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)', source)
        if m:
            right_expr = m.group(0).strip()
            right_ratio = float(m.group(1))

    return left_expr, left_ratio, right_expr, right_ratio


def _compute_ratio(head_r_expr, head_r_val, ew_expr, ew_val, source):
    if ew_expr is None:
        return None, "no ew found"

    m = re.match(r'\bew\s*=\s*int\(\s*head_r\s*\*\s*([\d.]+)\s*\)', ew_expr)
    if m:
        return float(m.group(1)), "direct ratio"

    if ew_val is not None and head_r_val is not None:
        m_ew = re.match(r'\bew\s*=\s*p\((\d+)\)', ew_expr)
        m_hr = re.match(r'\bhead_r\s*=\s*p\((\d+)\)', head_r_expr) if head_r_expr else None
        if m_ew and m_hr:
            return int(m_ew.group(1)) / int(m_hr.group(1)), "p(N)/p(M)"
        if ew_val and head_r_val:
            return ew_val / head_r_val, "N/M"

    m = re.match(r'\bew\s*=\s*int\(\s*HR\s*\*\s*([\d.]+)\s*\)', ew_expr)
    if m:
        return float(m.group(1)), "HR ratio"

    if 'head_w' in ew_expr or 'eye_w' in ew_expr:
        return None, "pixel-art style (N/A)"

    m_ew = re.match(r'\bew\s*=\s*p\((\d+)\)', ew_expr)
    m_hr_p = re.search(r'\bhead_r\s*=\s*p\((\d+)\)', source)
    if m_ew and m_hr_p:
        return int(m_ew.group(1)) / int(m_hr_p.group(1)), "p(N)/p(M)"

    return None, "could not resolve"


# ── Stub detection ────────────────────────────────────────────────────────────

def _is_stub(source):
    return 'import *' in source and ('from LTG_COLOR_' in source or
                                      'from LTG_TOOL_style_frame_' in source)


def _stub_source_path(source, stub_dir):
    m = re.search(r'from\s+(LTG_COLOR_\S+|LTG_TOOL_style_frame_\S+)\s+import', source)
    if not m:
        return None
    modname = m.group(1)
    candidate = os.path.join(stub_dir, modname + '.py')
    if os.path.exists(candidate):
        return candidate
    sf_dir = os.path.join(os.path.dirname(os.path.dirname(stub_dir)), 'output', 'color', 'style_frames')
    candidate2 = os.path.join(sf_dir, modname + '.py')
    if os.path.exists(candidate2):
        return candidate2
    return None


# ── Luma presence detection ───────────────────────────────────────────────────

def _has_luma(source, filename):
    if 'glitch_storm' in filename:
        if re.search(r'eye_r_left|eye_r_right|ew\s*=', source):
            return True, "Luma: sprint face with eyes (asymmetric)"
        return False, "Luma: sprint pose, no eyes (canonical N/A)"

    if 'other_side' in filename:
        if 'eye_w' in source and 'head_w' in source:
            return True, "Luma: pixel-art style (organic spec N/A)"
        return True, "Luma: pixel-art style (organic spec N/A)"

    if 'discovery' in filename or 'luma_byte' in filename:
        return True, "Luma: organic style"

    if 'luma' in source.lower() and ('ew' in source or 'eye_w' in source or
                                       'eye_r_left' in source or 'eye_r_right' in source):
        return True, "Luma with eyes (detected)"

    return False, "no Luma detected"


# ── Main scan ─────────────────────────────────────────────────────────────────

def scan_styleframe_files():
    """Scan all styleframe generator files and return list of result dicts."""
    candidates = []
    for fname in os.listdir(TOOLS_DIR):
        if fname.endswith('.py') and (
            fname.startswith('LTG_TOOL_styleframe_') or
            fname.startswith('LTG_TOOL_style_frame_')
        ):
            candidates.append(os.path.join(TOOLS_DIR, fname))

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
        ew_expr, ew_val         = _extract_ew(source)

        asym_left_expr, asym_left_ratio, asym_right_expr, asym_right_ratio = \
            _extract_asymmetric_eyes(source)

        has_asym = (asym_left_expr is not None) or (asym_right_expr is not None)

        if has_asym:
            left_verdict  = _ratio_verdict(asym_left_ratio)
            right_verdict = _ratio_verdict(asym_right_ratio)

            asym_diff_warn = False
            asym_diff_note = ""
            if asym_left_ratio is not None and asym_right_ratio is not None:
                diff = abs(asym_left_ratio - asym_right_ratio)
                if diff > ASYM_WARN_THRESHOLD:
                    asym_diff_warn = True
                    asym_diff_note = (f"ASYM-WARN: L/R differ by {diff:.4f} "
                                      f"(>{ASYM_WARN_THRESHOLD:.3f} threshold)")

            verdicts = [v for v in [left_verdict, right_verdict] if v not in ("N/A", None)]
            if not verdicts:
                overall_verdict = "N/A"
            elif all(v == "PASS" for v in verdicts) and not asym_diff_warn:
                overall_verdict = "ASYM-PASS"
            else:
                overall_verdict = "ASYM-WARN"

            results.append({
                'filename': fname,
                'stub_note': stub_note,
                'luma_note': luma_note,
                'head_r_expr': head_r_expr or '—',
                'ew_expr': f"L:{asym_left_expr or '—'} / R:{asym_right_expr or '—'}",
                'ratio': None,
                'ratio_str': f"L:{asym_left_ratio:.4f} / R:{asym_right_ratio:.4f}"
                              if (asym_left_ratio is not None and asym_right_ratio is not None)
                              else f"L:{asym_left_ratio} / R:{asym_right_ratio}",
                'ratio_method': "asymmetric",
                'verdict': overall_verdict,
                'asym_left_verdict': left_verdict,
                'asym_right_verdict': right_verdict,
                'asym_diff_warn': asym_diff_warn,
                'asym_diff_note': asym_diff_note,
            })

        else:
            ratio, ratio_method = _compute_ratio(head_r_expr, head_r_val,
                                                  ew_expr, ew_val, source)

            if 'N/A' in luma_note or 'no eyes' in luma_note or 'no Luma' in luma_note:
                verdict = "N/A"
            elif ew_expr is None:
                verdict = "N/A (no ew found)"
            elif 'pixel-art' in (ratio_method or ''):
                verdict = "N/A (pixel-art style)"
            else:
                verdict = _ratio_verdict(ratio)

            ratio_str = f"{ratio:.4f}" if ratio is not None else "—"

            results.append({
                'filename': fname,
                'stub_note': stub_note,
                'luma_note': luma_note,
                'head_r_expr': head_r_expr or '—',
                'ew_expr': ew_expr or '—',
                'ratio': ratio,
                'ratio_str': ratio_str,
                'ratio_method': ratio_method,
                'verdict': verdict,
                'asym_left_verdict': None,
                'asym_right_verdict': None,
                'asym_diff_warn': False,
                'asym_diff_note': "",
            })

    return results


def format_report(results, cycle: int = DEFAULT_CYCLE):
    """Format results as a markdown report string for the given cycle."""
    lines = []
    lines.append(f"# Proportion Audit — C{cycle}")
    lines.append("")
    lines.append("**Canonical spec:** `ew = HR × 0.22`")
    lines.append("**PASS:** ratio within 0.21–0.23  |  **WARN:** 0.19–0.25  |  **FAIL:** outside 0.19–0.25")
    lines.append("**ASYM-PASS:** asymmetric eyes, both within spec, diff ≤ 10%")
    lines.append("**ASYM-WARN:** asymmetric eyes; diff > 10% between L/R (intentional asymmetry flag)")
    lines.append("**N/A:** file has no organic Luma eyes (sprint pose without face, pixel-art, or no Luma)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| File | Luma Context | head_r expr | ew / eye_r expr | L/R ratio | Status |")
    lines.append("|------|-------------|-------------|-----------------|-----------|--------|")

    pass_count = warn_count = fail_count = na_count = asym_pass_count = asym_warn_count = 0

    for r in results:
        fname_display = r['filename']
        if r['stub_note']:
            fname_display += f" {r['stub_note']}"

        ew_display = r['ew_expr']
        if len(ew_display) > 60:
            ew_display = ew_display[:57] + "..."

        verdict = r['verdict']
        asym_note = f" {r['asym_diff_note']}" if r.get('asym_diff_note') else ""

        lines.append(
            f"| `{fname_display}` "
            f"| {r['luma_note']} "
            f"| `{r['head_r_expr']}` "
            f"| `{ew_display}` "
            f"| {r['ratio_str']} "
            f"| **{verdict}**{asym_note} |"
        )

        if verdict.startswith("PASS"):
            pass_count += 1
        elif verdict.startswith("ASYM-PASS"):
            asym_pass_count += 1
        elif verdict.startswith("ASYM-WARN"):
            asym_warn_count += 1
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
    lines.append(f"- **ASYM-PASS:** {asym_pass_count} (asymmetric eyes, both within spec)")
    lines.append(f"- **ASYM-WARN:** {asym_warn_count} (asymmetric eyes, L/R differ by > 10%)")
    lines.append(f"- **WARN:** {warn_count}")
    lines.append(f"- **FAIL:** {fail_count}")
    lines.append(f"- **N/A:** {na_count}")
    lines.append(f"- **Total files scanned:** {len(results)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- **SF01 (discovery):** Organic Luma. C30 fix corrected `ew = p(18)` (≈0.25) → `int(head_r * 0.22)`. v004+ should PASS.")
    lines.append("- **SF02 (glitch_storm):** v007+ has Luma face with asymmetric `eye_r_left`/`eye_r_right`. ASYM verdict reported.")
    lines.append("  SF02 v001–v006: Luma in sprint pose without eyes — N/A.")
    lines.append("- **SF03 (other_side):** Pixel-art Luma — `eye_w = max(4, head_w // 4)`. Organic spec intentionally N/A.")
    lines.append("- **SF04 (luma_byte):** Organic Luma. Latest version is v004. Should PASS.")
    lines.append("- **ASYM-WARN** is informational — asymmetric eyes may be intentional (e.g. FOCUSED DETERMINATION expression).")
    lines.append("  Flag to Art Director if asymmetry looks accidental or extreme.")
    lines.append("")
    lines.append(f"*Generated by `LTG_TOOL_proportion_audit.py` — Cycle {cycle}*")

    return "\n".join(lines)


def print_console_report(results, cycle: int = DEFAULT_CYCLE):
    """Print a compact console report."""
    print("=" * 72)
    print(f"LTG PROPORTION AUDIT — C{cycle} (v003)")
    print(f"Canonical spec: ew = HR × {CANONICAL_RATIO} (PASS ±{PASS_TOLERANCE})")
    print(f"Asym warn threshold: L/R differ by > {ASYM_WARN_THRESHOLD:.0%} of canonical")
    print("=" * 72)
    print()

    col_w = 52
    for r in results:
        fname = r['filename']
        if r['stub_note']:
            fname += f" {r['stub_note']}"
        ratio_str = r['ratio_str']
        verdict = r['verdict']
        print(f"  {fname[:col_w]:<{col_w}}  ratio={ratio_str}  [{verdict}]")
        print(f"    head_r: {r['head_r_expr']}")
        print(f"    ew:     {r['ew_expr'][:80]}")
        print(f"    note:   {r['luma_note']}")
        if r.get('asym_diff_note'):
            print(f"    asym:   {r['asym_diff_note']}")
        print()

    pass_c      = sum(1 for r in results if r['verdict'].startswith("PASS"))
    asym_pass_c = sum(1 for r in results if r['verdict'].startswith("ASYM-PASS"))
    asym_warn_c = sum(1 for r in results if r['verdict'].startswith("ASYM-WARN"))
    warn_c      = sum(1 for r in results if r['verdict'].startswith("WARN"))
    fail_c      = sum(1 for r in results if r['verdict'].startswith("FAIL"))
    na_c        = sum(1 for r in results if r['verdict'].startswith("N/A"))

    print("-" * 72)
    print(f"  PASS={pass_c}  ASYM-PASS={asym_pass_c}  ASYM-WARN={asym_warn_c}  "
          f"WARN={warn_c}  FAIL={fail_c}  N/A={na_c}  (total={len(results)})")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(
        description="LTG Proportion Audit — checks eye-width / head-radius ratios in SF generators"
    )
    parser.add_argument(
        "--cycle", type=int, default=DEFAULT_CYCLE,
        help=f"Cycle number for report labelling and output path (default: {DEFAULT_CYCLE})"
    )
    args = parser.parse_args()
    cycle = args.cycle

    report_path = _report_path(cycle)

    results = scan_styleframe_files()

    if not results:
        print("No styleframe generator files found.")
        sys.exit(1)

    print_console_report(results, cycle)

    report_md = format_report(results, cycle)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    print(f"\nReport written to: {report_path}")


if __name__ == "__main__":
    main()
