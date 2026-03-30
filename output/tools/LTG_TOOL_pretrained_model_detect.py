# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_pretrained_model_detect.py
====================================
Pretrained Model Detection Tool for "Luma & the Glitchkin."

Scans Python source files in output/tools/ for imports, function calls, or
patterns that pull pretrained model weights from torchvision, torch.hub,
timm, or any external model repository. The project must remain open-source
and self-contained — no external model weight downloads.

Checks:
  PM001  torchvision.models import or pretrained=True / weights= usage
  PM002  torch.hub.load() or torch.hub.download_url_to_file()
  PM003  timm.create_model() import
  PM004  keras.applications or tf.keras.applications import
  PM005  load_state_dict() from URL or remote path
  PM006  model_zoo / model_urls patterns
  PM007  huggingface transformers / diffusers import
  PM008  onnxruntime / onnx model loading

Author: Kai Nakamura (Technical Art Engineer)
Created: Cycle 47 — 2026-03-30
Version: 1.0.0

Usage:
  # Scan output/tools/ (default)
  python3 LTG_TOOL_pretrained_model_detect.py

  # Scan a specific directory
  python3 LTG_TOOL_pretrained_model_detect.py /path/to/dir

  # Pre-commit mode (exit 1 on any finding)
  python3 LTG_TOOL_pretrained_model_detect.py --pre-commit

  # Save report
  python3 LTG_TOOL_pretrained_model_detect.py --save-report report.txt

Dependencies: None (stdlib only — re, pathlib, argparse)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Detection patterns
# ---------------------------------------------------------------------------

_PATTERNS: List[Tuple[str, str, re.Pattern]] = [
    # PM001: torchvision pretrained models
    ("PM001", "torchvision pretrained model import",
     re.compile(r"""
        (?:from\s+torchvision(?:\.models)?\s+import)|
        (?:import\s+torchvision\.models)|
        (?:torchvision\.models\.\w+\s*\()|
        (?:pretrained\s*=\s*True)|
        (?:weights\s*=\s*(?!None)\w+)
     """, re.VERBOSE)),

    # PM002: torch.hub
    ("PM002", "torch.hub model loading",
     re.compile(r"""
        (?:torch\.hub\.load\s*\()|
        (?:torch\.hub\.download_url_to_file\s*\()|
        (?:torch\.hub\.load_state_dict_from_url\s*\()
     """, re.VERBOSE)),

    # PM003: timm (PyTorch Image Models)
    ("PM003", "timm pretrained model",
     re.compile(r"""
        (?:import\s+timm)|
        (?:from\s+timm\s+import)|
        (?:timm\.create_model\s*\()
     """, re.VERBOSE)),

    # PM004: Keras/TF pretrained
    ("PM004", "keras/tensorflow pretrained model",
     re.compile(r"""
        (?:from\s+(?:keras|tensorflow)\.(?:keras\.)?applications\s+import)|
        (?:(?:keras|tf)\.applications\.\w+\s*\()
     """, re.VERBOSE)),

    # PM005: load_state_dict from URL
    ("PM005", "load_state_dict from remote source",
     re.compile(r"""
        (?:load_state_dict_from_url\s*\()|
        (?:load_state_dict\s*\(\s*(?:torch\.)?(?:hub\.)?(?:download|load))
     """, re.VERBOSE)),

    # PM006: model_zoo / model_urls patterns
    ("PM006", "model_zoo or model_urls registry",
     re.compile(r"""
        (?:from\s+torch\.utils\.model_zoo\s+import)|
        (?:import\s+torch\.utils\.model_zoo)|
        (?:model_urls\s*=\s*\{)|
        (?:model_zoo\.load_url\s*\()
     """, re.VERBOSE)),

    # PM007: HuggingFace transformers / diffusers
    ("PM007", "huggingface transformers/diffusers import",
     re.compile(r"""
        (?:from\s+transformers\s+import)|
        (?:import\s+transformers)|
        (?:from\s+diffusers\s+import)|
        (?:import\s+diffusers)|
        (?:AutoModel\.from_pretrained\s*\()|
        (?:pipeline\s*\(\s*['\"])
     """, re.VERBOSE)),

    # PM008: ONNX runtime model loading
    ("PM008", "onnxruntime model loading",
     re.compile(r"""
        (?:import\s+onnxruntime)|
        (?:from\s+onnxruntime\s+import)|
        (?:onnxruntime\.InferenceSession\s*\()
     """, re.VERBOSE)),
]

# Lines starting with # are comments — skip them
_COMMENT_RE = re.compile(r"^\s*#")
# Docstring detection (triple-quote)
_TRIPLE_QUOTE_RE = re.compile(r'("""|\'\'\')')


# ---------------------------------------------------------------------------
# Core scanning
# ---------------------------------------------------------------------------

def scan_file(filepath: str) -> Dict:
    """
    Scan a single Python file for pretrained model usage patterns.

    Returns
    -------
    dict
        {
          "file": str,
          "status": "PASS" | "WARN",
          "findings": list[dict],  # each: {code, description, line_no, line_text}
        }
    """
    path = Path(filepath)
    if not path.is_file() or path.suffix != ".py":
        return {
            "file": str(path),
            "status": "SKIP",
            "findings": [],
            "reason": "not a .py file",
        }

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {
            "file": str(path),
            "status": "ERROR",
            "findings": [],
            "reason": str(e),
        }

    lines = text.split("\n")
    findings = []

    # Track whether we're inside a docstring
    in_docstring = False
    docstring_char = None

    for line_no, line in enumerate(lines, start=1):
        # Simple docstring tracking
        quotes = _TRIPLE_QUOTE_RE.findall(line)
        for q in quotes:
            if not in_docstring:
                in_docstring = True
                docstring_char = q
            elif q == docstring_char:
                in_docstring = False
                docstring_char = None

        # Skip comments and docstrings
        if _COMMENT_RE.match(line):
            continue
        if in_docstring:
            continue

        stripped = line.strip()
        if not stripped:
            continue

        for code, description, pattern in _PATTERNS:
            if pattern.search(stripped):
                findings.append({
                    "code": code,
                    "description": description,
                    "line_no": line_no,
                    "line_text": stripped[:120],
                })

    return {
        "file": str(path),
        "status": "WARN" if findings else "PASS",
        "findings": findings,
    }


def scan_directory(
    directory: str,
    pattern: str = "*.py",
    skip_legacy: bool = True,
) -> List[Dict]:
    """
    Scan all Python files in a directory for pretrained model patterns.

    Parameters
    ----------
    directory : str
        Path to scan.
    pattern : str
        Glob pattern for files. Default "*.py".
    skip_legacy : bool
        Skip files in legacy/ subdirectory.

    Returns
    -------
    list[dict]
        One result per file (same structure as scan_file).
    """
    dirpath = Path(directory)
    if not dirpath.is_dir():
        return [{
            "file": str(dirpath),
            "status": "ERROR",
            "findings": [],
            "reason": "not a directory",
        }]

    results = []
    for pyfile in sorted(dirpath.glob(pattern)):
        if not pyfile.is_file():
            continue
        if skip_legacy and "legacy" in pyfile.parts:
            continue
        results.append(scan_file(str(pyfile)))

    return results


def format_report(results: List[Dict], include_pass: bool = False) -> str:
    """
    Format scan results as a human-readable report.

    Parameters
    ----------
    results : list[dict]
        Output from scan_directory().
    include_pass : bool
        Include PASS files in the report.

    Returns
    -------
    str
        Formatted report text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("Pretrained Model Detection Report")
    lines.append("Tool: LTG_TOOL_pretrained_model_detect.py v1.0.0")
    lines.append("=" * 60)
    lines.append("")

    total = len(results)
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    warn_count = sum(1 for r in results if r["status"] == "WARN")
    error_count = sum(1 for r in results if r["status"] == "ERROR")
    skip_count = sum(1 for r in results if r["status"] == "SKIP")

    lines.append(f"Files scanned: {total}")
    lines.append(f"PASS: {pass_count}  WARN: {warn_count}  ERROR: {error_count}  SKIP: {skip_count}")
    lines.append("")

    if warn_count == 0:
        lines.append("No pretrained model usage detected. Pipeline is self-contained.")
        lines.append("")
    else:
        lines.append(f"*** {warn_count} file(s) with pretrained model patterns detected ***")
        lines.append("")

    for r in results:
        if r["status"] == "PASS" and not include_pass:
            continue
        if r["status"] == "SKIP":
            continue

        fname = Path(r["file"]).name
        lines.append(f"--- {fname} [{r['status']}] ---")

        if r["status"] == "ERROR":
            lines.append(f"  Error: {r.get('reason', 'unknown')}")
        elif r["findings"]:
            for f in r["findings"]:
                lines.append(f"  [{f['code']}] L{f['line_no']}: {f['description']}")
                lines.append(f"         {f['line_text']}")
        else:
            lines.append("  No findings.")

        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Detect pretrained model usage (torchvision, torch.hub, etc.) in project Python files."
    )
    parser.add_argument(
        "directory", nargs="?", default=None,
        help="Directory to scan (default: output/tools/ from project root)"
    )
    parser.add_argument(
        "--pre-commit", action="store_true",
        help="Exit code 1 if any findings (for CI gate)"
    )
    parser.add_argument(
        "--include-pass", action="store_true",
        help="Include PASS files in report"
    )
    parser.add_argument(
        "--include-legacy", action="store_true",
        help="Include files in legacy/ subdirectory"
    )
    parser.add_argument(
        "--save-report", default=None,
        help="Save report to file"
    )

    args = parser.parse_args()

    # Resolve directory
    if args.directory:
        scan_dir = args.directory
    else:
        # Default: output/tools/ relative to this file's location
        scan_dir = str(Path(__file__).parent)

    results = scan_directory(
        scan_dir,
        skip_legacy=not args.include_legacy,
    )

    report = format_report(results, include_pass=args.include_pass)
    print(report)

    if args.save_report:
        rp = Path(args.save_report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(report, encoding="utf-8")
        print(f"Report saved to: {args.save_report}")

    # Exit code
    warn_count = sum(1 for r in results if r["status"] == "WARN")
    if args.pre_commit and warn_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
