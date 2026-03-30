#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_batch_stylize_v001.py — Batch Stylization Runner
"Luma & the Glitchkin" — Technical Art / Kai Nakamura / Cycle 24
Updated Cycle 25: calls LTG_TOOL_stylize_handdrawn_v002; adds color verification.

Runs LTG_TOOL_stylize_handdrawn_v002.stylize() on a list of images in a
single command. Supports both a programmatic API (pass a list of job tuples)
and a CLI interface (pass a JSON job list or a glob pattern).

Color verification (Cycle 25): after each job, verify_canonical_colors() is
called on the output PNG and the result is included in the per-job report under
the "color_verify" key. A failed color verification is logged as a warning but
does NOT set status="error" — the file is still written. This allows Rin or the
Art Director to review color drift without blocking the batch.

Usage (module):
    import sys, os
    sys.path.insert(0, "/home/wipkat/team/output/tools")
    from LTG_TOOL_batch_stylize_v001 import batch_stylize

    jobs = [
        ("output/backgrounds/environments/LTG_ENV_tech_den_v003.png",
         "output/stylized/LTG_ENV_tech_den_v003_styled.png",
         "realworld", 1.0),
        ("output/backgrounds/environments/LTG_ENV_other_side_bg_v002.png",
         "output/stylized/LTG_ENV_other_side_bg_v002_styled.png",
         "glitch", 1.0),
    ]
    results = batch_stylize(jobs, seed=42, stop_on_error=False)

Usage (CLI — explicit JSON list):
    python output/tools/LTG_TOOL_batch_stylize_v001.py \\
        --jobs '[["input.png","output.png","realworld",1.0]]'

Usage (CLI — glob all PNGs through one mode):
    python output/tools/LTG_TOOL_batch_stylize_v001.py \\
        --glob "output/backgrounds/**/*.png" \\
        --out-dir output/stylized \\
        --mode realworld \\
        --intensity 1.0

Dependencies: Python 3.8+, Pillow, LTG_TOOL_stylize_handdrawn_v002,
              LTG_TOOL_color_verify_v001
Runnable from: /home/wipkat/team (project root)

Each job tuple: (input_path, output_path, mode, intensity)
  - input_path  : str — source PNG
  - output_path : str — destination PNG (directories created automatically)
  - mode        : str — "realworld" | "glitch" | "mixed"
  - intensity   : float — 0.0–2.0

Cycle 25 changes:
  - Switched stylize() import from v001 → v002 (full canonical color protection)
  - Added post-processing color verification via LTG_TOOL_color_verify_v001
  - Per-job result dict gains "color_verify" key (see batch_stylize() docstring)
"""

__version__ = "1.1.0"
__author__ = "Kai Nakamura"
__cycle__ = 25

import sys
import os
import json
import argparse
import glob as _glob_module
import time
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------------
# Bootstrap: ensure output/tools is on sys.path so stylize tool can be found
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from LTG_TOOL_stylize_handdrawn_v002 import stylize  # noqa: E402 — C25: upgraded to v002
from LTG_TOOL_color_verify_v001 import (              # noqa: E402 — C25: color verification
    verify_canonical_colors, get_canonical_palette
)

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------
# A job is a 4-tuple: (input_path, output_path, mode, intensity)
Job = Tuple[str, str, str, float]

VALID_MODES = ("realworld", "glitch", "mixed")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def batch_stylize(
    jobs: List[Job],
    seed: int = 42,
    stop_on_error: bool = False,
    verbose: bool = True,
    verify_colors: bool = True,
    color_max_delta_hue: float = 5.0,
) -> List[dict]:
    """Run stylize() on a list of (input_path, output_path, mode, intensity) jobs.

    Args:
        jobs                (list):  List of 4-tuples:
                                     (input_path: str, output_path: str, mode: str, intensity: float)
                                     - input_path:  path to source PNG
                                     - output_path: path for stylized output PNG
                                     - mode:        "realworld" | "glitch" | "mixed"
                                     - intensity:   0.0–2.0 global effect multiplier
        seed                (int):   RNG seed applied to every job for reproducibility.
        stop_on_error       (bool):  If True, raise on first failure; if False, log and continue.
        verbose             (bool):  Print per-job progress to stdout.
        verify_colors       (bool):  If True (default), run verify_canonical_colors() on each
                                     output PNG and include the result in the report. A failed
                                     color check is logged as a warning but does NOT set
                                     status="error". (C25)
        color_max_delta_hue (float): Hue drift threshold in degrees for color verification.
                                     Default: 5.0 (matches LTG_TOOL_color_verify_v001 default).

    Returns:
        list of dicts, one per job:
        {
            "input":         str,
            "output":        str,
            "mode":          str,
            "intensity":     float,
            "status":        "ok" | "error",
            "error":         str | None,
            "elapsed":       float  (seconds),
            "color_verify":  dict | None  — result from verify_canonical_colors(), or None
                                           if verify_colors=False or job failed before output.
                                           overall_pass=False means hue drift detected.
        }
    """
    if not jobs:
        if verbose:
            print("[batch_stylize] No jobs provided — nothing to do.")
        return []

    results = []
    total = len(jobs)

    if verbose:
        print(f"[LTG_TOOL_batch_stylize_v001] Starting batch: {total} job(s), seed={seed}")
        print("-" * 70)

    for idx, job in enumerate(jobs, start=1):
        if len(job) != 4:
            msg = f"Job {idx}: Expected 4-tuple, got {len(job)} elements: {job!r}"
            if stop_on_error:
                raise ValueError(msg)
            results.append({
                "input": str(job[0]) if job else "",
                "output": str(job[1]) if len(job) > 1 else "",
                "mode": str(job[2]) if len(job) > 2 else "",
                "intensity": float(job[3]) if len(job) > 3 else 1.0,
                "status": "error",
                "error": msg,
                "elapsed": 0.0,
            })
            if verbose:
                print(f"  [{idx}/{total}] ERROR — {msg}")
            continue

        input_path, output_path, mode, intensity = job
        input_path = str(input_path)
        output_path = str(output_path)
        mode = str(mode)
        intensity = float(intensity)

        record = {
            "input": input_path,
            "output": output_path,
            "mode": mode,
            "intensity": intensity,
            "status": "ok",
            "error": None,
            "elapsed": 0.0,
            "color_verify": None,
        }

        if verbose:
            print(f"  [{idx}/{total}] {os.path.basename(input_path)} → "
                  f"{os.path.basename(output_path)}  mode={mode}  intensity={intensity}")

        t0 = time.time()
        try:
            _validate_job(input_path, output_path, mode, intensity)
            stylize(input_path, output_path, mode=mode, intensity=intensity, seed=seed)
            record["elapsed"] = round(time.time() - t0, 2)
            if verbose:
                print(f"         done in {record['elapsed']}s")

            # --- Color verification (C25) ---
            if verify_colors and os.path.exists(output_path):
                try:
                    from PIL import Image as _Image
                    _palette = get_canonical_palette()
                    _out_img = _Image.open(output_path)
                    cv_result = verify_canonical_colors(
                        _out_img, _palette,
                        max_delta_hue=color_max_delta_hue,
                    )
                    record["color_verify"] = cv_result
                    if not cv_result.get("overall_pass", True):
                        _drifted = [
                            k for k, v in cv_result.items()
                            if k != "overall_pass"
                            and isinstance(v, dict)
                            and not v.get("pass", True)
                        ]
                        if verbose:
                            print(f"         WARNING: color drift detected — {_drifted}")
                    else:
                        if verbose:
                            print(f"         color verify: PASS")
                except Exception as cv_exc:
                    if verbose:
                        print(f"         color verify ERROR — {cv_exc}")
                    record["color_verify"] = {"overall_pass": None, "error": str(cv_exc)}

        except Exception as exc:
            record["status"] = "error"
            record["error"] = str(exc)
            record["elapsed"] = round(time.time() - t0, 2)
            if verbose:
                print(f"         ERROR — {exc}")
            if stop_on_error:
                raise

        results.append(record)

    # Summary
    if verbose:
        ok_count = sum(1 for r in results if r["status"] == "ok")
        err_count = total - ok_count
        # Color verification summary
        cv_results = [r["color_verify"] for r in results if r.get("color_verify") is not None]
        cv_pass = sum(1 for cv in cv_results if cv.get("overall_pass") is True)
        cv_warn = sum(1 for cv in cv_results if cv.get("overall_pass") is False)
        cv_skip = total - len(cv_results)
        print("-" * 70)
        print(f"[batch_stylize] Complete — {ok_count}/{total} succeeded"
              + (f", {err_count} error(s)" if err_count else ""))
        if verify_colors:
            print(f"[batch_stylize] Color verify — {cv_pass} pass"
                  + (f", {cv_warn} WARNING(s) (hue drift)" if cv_warn else "")
                  + (f", {cv_skip} skipped" if cv_skip else ""))

    return results


def batch_stylize_from_glob(
    pattern: str,
    out_dir: str,
    mode: str = "realworld",
    intensity: float = 1.0,
    seed: int = 42,
    suffix: str = "_styled",
    stop_on_error: bool = False,
    verbose: bool = True,
) -> List[dict]:
    """Build a job list from a glob pattern and run batch_stylize().

    Output filenames are derived by appending `suffix` before the extension,
    e.g. "LTG_ENV_tech_den_v003.png" → "LTG_ENV_tech_den_v003_styled.png"
    placed under out_dir (flat — no subdirectory hierarchy preserved).

    Args:
        pattern       (str): Glob pattern for source PNGs. Relative to cwd.
        out_dir       (str): Directory to write stylized outputs.
        mode          (str): Stylization mode for all matched images.
        intensity     (float): Intensity for all matched images.
        seed          (int): RNG seed.
        suffix        (str): Suffix appended to each filename before extension.
        stop_on_error (bool): Whether to abort on first failure.
        verbose       (bool): Print progress.

    Returns:
        Same list-of-dicts as batch_stylize().
    """
    matched = sorted(_glob_module.glob(pattern, recursive=True))
    if not matched:
        if verbose:
            print(f"[batch_stylize_from_glob] No files matched: {pattern}")
        return []

    os.makedirs(out_dir, exist_ok=True)

    jobs: List[Job] = []
    for src in matched:
        basename = os.path.basename(src)
        stem, ext = os.path.splitext(basename)
        dest_name = f"{stem}{suffix}{ext}"
        dest = os.path.join(out_dir, dest_name)
        jobs.append((src, dest, mode, intensity))

    return batch_stylize(jobs, seed=seed, stop_on_error=stop_on_error, verbose=verbose)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _validate_job(input_path: str, output_path: str, mode: str, intensity: float) -> None:
    """Raise ValueError or FileNotFoundError for invalid job parameters."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input not found: {input_path}")
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid mode '{mode}'. Must be one of: {VALID_MODES}")
    if not (0.0 <= intensity <= 2.0):
        raise ValueError(f"intensity must be 0.0–2.0, got {intensity}")
    if not output_path:
        raise ValueError("output_path must not be empty")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli():
    parser = argparse.ArgumentParser(
        description=(
            "LTG Batch Stylization Runner v001 (C25: v1.1.0) — Luma & the Glitchkin\n"
            "Runs stylize() from LTG_TOOL_stylize_handdrawn_v002 on multiple images.\n"
            "Color verification (LTG_TOOL_color_verify_v001) is run on each output."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run from project root with explicit JSON job list
  python output/tools/LTG_TOOL_batch_stylize_v001.py \\
      --jobs '[["output/backgrounds/environments/LTG_ENV_tech_den_v003.png",
               "output/stylized/LTG_ENV_tech_den_v003_styled.png",
               "realworld", 1.0]]'

  # Glob all environment PNGs, write to output/stylized/
  python output/tools/LTG_TOOL_batch_stylize_v001.py \\
      --glob "output/backgrounds/**/*.png" \\
      --out-dir output/stylized \\
      --mode realworld \\
      --intensity 1.0

  # Dump results JSON to file
  python output/tools/LTG_TOOL_batch_stylize_v001.py \\
      --glob "output/backgrounds/**/*.png" \\
      --out-dir output/stylized \\
      --mode glitch \\
      --results-json output/stylized/batch_results.json
        """,
    )

    # Mutually exclusive: --jobs JSON vs --glob pattern
    src_group = parser.add_mutually_exclusive_group(required=True)
    src_group.add_argument(
        "--jobs",
        type=str,
        metavar="JSON",
        help=(
            "JSON array of job tuples: "
            '[[\"in.png\",\"out.png\",\"realworld\",1.0], ...]'
        ),
    )
    src_group.add_argument(
        "--glob",
        type=str,
        metavar="PATTERN",
        help="Glob pattern for source PNGs (relative to cwd). Use with --out-dir.",
    )

    parser.add_argument(
        "--out-dir",
        type=str,
        default="output/stylized",
        help="Output directory when using --glob (default: output/stylized)",
    )
    parser.add_argument(
        "--mode",
        choices=list(VALID_MODES),
        default="realworld",
        help="Stylization mode — used when --glob is set (default: realworld)",
    )
    parser.add_argument(
        "--intensity",
        type=float,
        default=1.0,
        help="Intensity 0.0–2.0 — used when --glob is set (default: 1.0)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="RNG seed for all jobs (default: 42)",
    )
    parser.add_argument(
        "--suffix",
        type=str,
        default="_styled",
        help="Filename suffix appended when using --glob (default: _styled)",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        default=False,
        help="Abort on first failure (default: log and continue)",
    )
    parser.add_argument(
        "--results-json",
        type=str,
        default=None,
        metavar="PATH",
        help="Optional: write batch results summary as JSON to this path",
    )

    args = parser.parse_args()

    if args.jobs:
        try:
            raw = json.loads(args.jobs)
        except json.JSONDecodeError as e:
            parser.error(f"--jobs: invalid JSON — {e}")

        if not isinstance(raw, list):
            parser.error("--jobs: must be a JSON array")

        jobs = []
        for i, item in enumerate(raw):
            if not isinstance(item, (list, tuple)) or len(item) != 4:
                parser.error(f"--jobs: item {i} must be a 4-element array")
            jobs.append(tuple(item))

        results = batch_stylize(
            jobs,
            seed=args.seed,
            stop_on_error=args.stop_on_error,
            verbose=True,
        )
    else:
        results = batch_stylize_from_glob(
            pattern=args.glob,
            out_dir=args.out_dir,
            mode=args.mode,
            intensity=args.intensity,
            seed=args.seed,
            suffix=args.suffix,
            stop_on_error=args.stop_on_error,
            verbose=True,
        )

    # Optionally dump results JSON
    if args.results_json and results:
        results_path = args.results_json
        out_dir = os.path.dirname(results_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(results_path, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2)
        print(f"[batch_stylize] Results written to: {results_path}")

    # Exit with error code if any job failed
    any_error = any(r["status"] == "error" for r in results)
    sys.exit(1 if any_error else 0)


if __name__ == "__main__":
    _cli()
