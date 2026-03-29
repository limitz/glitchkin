#!/usr/bin/env python3
"""
LTG_TOOL_readme_sync_v001.py
============================
README Script Index audit/sync tool for "Luma & the Glitchkin."

Enumerates all LTG_TOOL_*.py files in output/tools/ (excluding legacy/)
and cross-checks against the Script Index table in README.md.

Reports:
  - UNLISTED tools: on disk but not in README Script Index table
  - GHOST entries: in README table but no .py file on disk
  - LEGACY entries: marked with ~~ strikethrough in README (correctly archived)

This tool does NOT modify any files — it only reports.

Author: Morgan Walsh (Pipeline Automation Specialist)
Created: Cycle 35 — 2026-03-29
Version: 1.0.0

Usage:
    python LTG_TOOL_readme_sync_v001.py [--save-report PATH]
    python LTG_TOOL_readme_sync_v001.py --json

Exit codes:
    0 — All tools listed in README and all entries have files on disk
    1 — One or more UNLISTED or GHOST tools found
"""

import sys
import re
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_TOOLS_DIR  = Path(__file__).resolve().parent
_README     = _TOOLS_DIR / "README.md"
_LEGACY_DIR = _TOOLS_DIR / "legacy"

__version__ = "1.0.0"


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def enumerate_disk_tools(tools_dir: Path = _TOOLS_DIR) -> list:
    """
    Return sorted list of LTG_TOOL_*.py filenames present in tools_dir
    (not in legacy/ subdirectory).
    """
    results = []
    for p in tools_dir.iterdir():
        if p.is_file() and p.suffix == ".py" and p.stem.startswith("LTG_TOOL_"):
            results.append(p.name)
    return sorted(results)


def parse_readme_index(readme_path: Path = _README) -> dict:
    """
    Parse the Script Index table in README.md and return a dict:
    {
        "listed":  list[str]  # tool names with a live table row (backtick name)
        "legacy":  list[str]  # tool names marked ~~strikethrough~~ (retired)
    }

    Table rows have the form:
      | `LTG_TOOL_name.py` | ... |
    Legacy (retired) rows:
      | ~~`LTG_TOOL_name.py`~~ | ... |
    """
    if not readme_path.exists():
        return {"listed": [], "legacy": []}

    text = readme_path.read_text(encoding="utf-8")

    listed = []
    legacy = []

    # Match table rows: | `LTG_TOOL_*.py` | ... |
    # Also match legacy rows: | ~~`LTG_TOOL_*.py`~~ | ... |
    row_re = re.compile(r"^\|\s*(~~)?`?(LTG_TOOL_\S+\.py)`?(~~)?\s*\|", re.MULTILINE)
    for m in row_re.finditer(text):
        name = m.group(2)
        is_legacy = bool(m.group(1)) or bool(m.group(3))
        if is_legacy:
            legacy.append(name)
        else:
            listed.append(name)

    return {"listed": listed, "legacy": legacy}


def audit(tools_dir: Path = _TOOLS_DIR, readme_path: Path = _README) -> dict:
    """
    Cross-check disk tools vs README Script Index.

    Returns:
    {
        "disk_tools":  list[str],   # all LTG_TOOL_*.py on disk (non-legacy)
        "listed":      list[str],   # tools listed in README (non-legacy rows)
        "legacy":      list[str],   # tools listed in README as retired
        "unlisted":    list[str],   # on disk but NOT in README
        "ghost":       list[str],   # in README but NOT on disk
        "ok":          list[str],   # in both disk and README
        "result":      "PASS"|"WARN"
    }
    """
    disk_tools  = enumerate_disk_tools(tools_dir)
    index       = parse_readme_index(readme_path)
    listed      = index["listed"]
    legacy      = index["legacy"]

    listed_set = set(listed)
    legacy_set = set(legacy)
    disk_set   = set(disk_tools)

    # Unlisted: on disk, not in README (ignore legacy dir files — they won't appear here)
    unlisted = sorted(disk_set - listed_set - legacy_set)

    # Ghost: in README table but not on disk
    # Check both tools_dir and legacy_dir for legacy entries
    ghost = []
    for name in listed:
        if (tools_dir / name).exists():
            continue
        # Not found in main dir
        ghost.append(name)

    # Legacy ghost: in README legacy rows but not in legacy/ dir
    legacy_ghost = []
    for name in legacy:
        if not (_legacy_dir := tools_dir / "legacy" / name).exists():
            # Check if it's in main dir (not yet moved)
            if not (tools_dir / name).exists():
                legacy_ghost.append(name)

    ok = sorted(disk_set & listed_set)

    result = "PASS"
    if unlisted or ghost or legacy_ghost:
        result = "WARN"

    return {
        "disk_tools":     disk_tools,
        "listed":         listed,
        "legacy":         legacy,
        "unlisted":       unlisted,
        "ghost":          ghost,
        "legacy_ghost":   legacy_ghost,
        "ok":             ok,
        "result":         result,
    }


def format_report(audit_result: dict) -> str:
    """Format audit result as a compact Markdown/text report."""
    lines = [
        f"# README Script Index Audit — LTG_TOOL_readme_sync_v001.py v{__version__}",
        "",
        f"**Result:** {audit_result['result']}",
        "",
        f"- Tools on disk (non-legacy):  {len(audit_result['disk_tools'])}",
        f"- Tools listed in README:       {len(audit_result['listed'])}",
        f"- Tools retired (~~struck~~):   {len(audit_result['legacy'])}",
        f"- OK (both disk + README):      {len(audit_result['ok'])}",
        f"- UNLISTED (disk, not README):  {len(audit_result['unlisted'])}",
        f"- GHOST (README, not disk):     {len(audit_result['ghost'])}",
        "",
    ]

    if audit_result["unlisted"]:
        lines.append("## UNLISTED tools (on disk, not in README Script Index)")
        lines.append("_Action required: add a row to the Script Index table in README.md_")
        lines.append("")
        for name in audit_result["unlisted"]:
            lines.append(f"  - `{name}`")
        lines.append("")

    if audit_result["ghost"]:
        lines.append("## GHOST entries (in README, not on disk)")
        lines.append("_Action required: restore the file or remove the README row_")
        lines.append("")
        for name in audit_result["ghost"]:
            lines.append(f"  - `{name}`")
        lines.append("")

    if audit_result["legacy_ghost"]:
        lines.append("## LEGACY GHOST entries (marked retired in README, not in legacy/)")
        lines.append("_Action required: move file to output/tools/legacy/ or update README_")
        lines.append("")
        for name in audit_result["legacy_ghost"]:
            lines.append(f"  - `{name}`")
        lines.append("")

    if audit_result["result"] == "PASS":
        lines.append("_All tools on disk are listed in the README Script Index. No ghosts._")
        lines.append("")

    lines.append("---")
    lines.append(f"*Generated by LTG_TOOL_readme_sync_v001.py v{__version__} — Morgan Walsh, Pipeline Automation*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    save_path = None
    as_json = False

    i = 0
    while i < len(args):
        if args[i] == "--save-report" and i + 1 < len(args):
            save_path = args[i + 1]
            i += 2
        elif args[i] == "--json":
            as_json = True
            i += 1
        else:
            i += 1

    result = audit()

    if as_json:
        # Remove non-serialisable items if any
        out = {k: v for k, v in result.items()}
        print(json.dumps(out, indent=2))
    else:
        report = format_report(result)
        print(report)
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            Path(save_path).write_text(report, encoding="utf-8")
            print(f"\nReport saved to: {save_path}")

    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
