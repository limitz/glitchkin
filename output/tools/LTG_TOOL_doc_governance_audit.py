# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_doc_governance_audit.py
Doc Governance Audit — "Luma & the Glitchkin"
Author: Morgan Walsh / Cycle 47
v1.0.0

Scans all .md documentation files under docs/ and output/ for cycle
references (C<number>). Reports the highest cycle referenced in each file
and flags files that haven't been updated in N+ cycles as STALE.

Files with no cycle reference are listed separately — they may be
specification docs that don't track cycles, or they may be forgotten.

Usage
-----
    python LTG_TOOL_doc_governance_audit.py
    python LTG_TOOL_doc_governance_audit.py --stale-threshold 10
    python LTG_TOOL_doc_governance_audit.py --current-cycle 47
    python LTG_TOOL_doc_governance_audit.py --save-report PATH

API
---
    from LTG_TOOL_doc_governance_audit import audit_docs, format_audit_report

    result = audit_docs(current_cycle=47, stale_threshold=10)
    print(format_audit_report(result))

Changelog
---------
v1.0.0 (C47): Initial implementation. Scans docs/ and output/ for .md files.
              Reports STALE / NO_CYCLE_REF / RECENT per file.
              (Morgan Walsh)
"""

__version__ = "1.0.0"

import os
import re
import sys
import argparse

_HERE = os.path.dirname(os.path.abspath(__file__))

# Pattern to match cycle references like C47, C10, C8 etc.
_CYCLE_PATTERN = re.compile(r'\bC(\d{1,3})\b')


def _find_project_root():
    """Walk up from _HERE to find CLAUDE.md sentinel."""
    d = _HERE
    for _ in range(10):
        if os.path.exists(os.path.join(d, "CLAUDE.md")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.dirname(_HERE))


def _get_max_cycle(filepath):
    """Read a file and return the highest C<number> referenced, or None."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        cycles = [int(m) for m in _CYCLE_PATTERN.findall(text)]
        return max(cycles) if cycles else None
    except OSError:
        return None


def audit_docs(current_cycle=48, stale_threshold=10, project_root=None):
    """
    Scan all .md files under docs/ and output/ for cycle references.

    Parameters
    ----------
    current_cycle : int
        Current cycle number (e.g. 47).
    stale_threshold : int
        Number of cycles after which a doc is considered stale (default 10).
    project_root : str | None
        Project root directory. Auto-detected if None.

    Returns
    -------
    dict
        {
          "current_cycle": int,
          "stale_threshold": int,
          "stale": list[dict],       # {path, max_cycle, age}
          "no_cycle_ref": list[dict], # {path}
          "recent": list[dict],       # {path, max_cycle, age}
          "total_scanned": int,
        }
    """
    root = project_root or _find_project_root()

    scan_roots = [
        os.path.join(root, "docs"),
        os.path.join(root, "output"),
    ]

    # Skip patterns
    skip_dirs = {"__pycache__", ".git", "node_modules", "deprecated", "legacy"}
    skip_files = {"README.md"}  # tools README is huge and always current

    scanned = set()
    stale = []
    no_cycle_ref = []
    recent = []

    for scan_root in scan_roots:
        if not os.path.isdir(scan_root):
            continue
        for dirpath, dirnames, filenames in os.walk(scan_root):
            # Prune skip dirs
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]

            # Skip tools/README.md specifically
            rel_dir = os.path.relpath(dirpath, root)

            for fname in sorted(filenames):
                if not fname.endswith(".md"):
                    continue
                # Skip tools/README.md (it's always current, very large)
                if fname == "README.md" and "tools" in rel_dir:
                    continue

                fpath = os.path.join(dirpath, fname)
                if fpath in scanned:
                    continue
                scanned.add(fpath)

                rel_path = os.path.relpath(fpath, root)
                max_c = _get_max_cycle(fpath)

                if max_c is not None:
                    age = current_cycle - max_c
                    entry = {"path": rel_path, "max_cycle": max_c, "age": age}
                    if age >= stale_threshold:
                        stale.append(entry)
                    else:
                        recent.append(entry)
                else:
                    no_cycle_ref.append({"path": rel_path})

    # Sort stale by age descending
    stale.sort(key=lambda x: -x["age"])
    # Sort recent by age descending
    recent.sort(key=lambda x: -x["age"])
    # Sort no_cycle_ref alphabetically
    no_cycle_ref.sort(key=lambda x: x["path"])

    return {
        "current_cycle": current_cycle,
        "stale_threshold": stale_threshold,
        "stale": stale,
        "no_cycle_ref": no_cycle_ref,
        "recent": recent,
        "total_scanned": len(scanned),
    }


def format_audit_report(result):
    """
    Format the audit result dict as a human-readable report.

    Parameters
    ----------
    result : dict
        From audit_docs().

    Returns
    -------
    str
    """
    lines = []
    lines.append("=" * 72)
    lines.append(f"DOC GOVERNANCE AUDIT — C{result['current_cycle']}")
    lines.append(f"Stale threshold: {result['stale_threshold']}+ cycles")
    lines.append(f"Total scanned: {result['total_scanned']} .md files")
    lines.append("=" * 72)

    stale = result["stale"]
    no_ref = result["no_cycle_ref"]
    recent = result["recent"]

    lines.append(f"\nSTALE ({result['stale_threshold']}+ cycles old): {len(stale)} files")
    lines.append("-" * 72)
    if stale:
        for entry in stale:
            lines.append(
                f"  C{entry['max_cycle']:<3d}  (age {entry['age']:>2d})  {entry['path']}"
            )
    else:
        lines.append("  (none)")

    lines.append(f"\nNO CYCLE REFERENCE: {len(no_ref)} files")
    lines.append("-" * 72)
    if no_ref:
        for entry in no_ref:
            lines.append(f"  --          {entry['path']}")
    else:
        lines.append("  (none)")

    lines.append(f"\nRECENT (<{result['stale_threshold']} cycles): {len(recent)} files")
    lines.append("-" * 72)
    if recent:
        for entry in recent:
            lines.append(
                f"  C{entry['max_cycle']:<3d}  (age {entry['age']:>2d})  {entry['path']}"
            )
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("=" * 72)
    lines.append(f"SUMMARY: {len(stale)} STALE | {len(no_ref)} NO_REF | {len(recent)} RECENT")
    lines.append("=" * 72)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description=f"LTG Doc Governance Audit v{__version__}"
    )
    parser.add_argument(
        "--current-cycle",
        type=int,
        default=48,
        help="Current cycle number (default: 48)",
    )
    parser.add_argument(
        "--stale-threshold",
        type=int,
        default=10,
        help="Cycles after which a doc is stale (default: 10)",
    )
    parser.add_argument(
        "--save-report",
        default=None,
        metavar="PATH",
        help="Save report to this file",
    )
    args = parser.parse_args()

    result = audit_docs(
        current_cycle=args.current_cycle,
        stale_threshold=args.stale_threshold,
    )
    report = format_audit_report(result)

    if args.save_report:
        with open(args.save_report, "w", encoding="utf-8") as fh:
            fh.write(report)
            fh.write("\n")
        print(f"Report saved to: {args.save_report}")
    else:
        print(report)


if __name__ == "__main__":
    main()
