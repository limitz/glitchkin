# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_warmth_inject_hook.py
=====================================
Shared hook that environment generators call when the ``--check-warmth`` flag
is passed.  Encapsulates the 2-step generate → warmth-inject pipeline so that
every generator can gain the feature with a 3-line import + call.

USAGE (in a generator)
----------------------
Add a CLI flag:

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-warmth", action="store_true",
                        help="Run warmth-inject if render_qa warm/cool check fails")
    args = parser.parse_args()

After saving the PNG, call:

    from LTG_TOOL_warmth_inject_hook import run_warmth_hook
    run_warmth_hook(out_path, enabled=args.check_warmth)

WHAT IT DOES
------------
1. If enabled=False  → no-op (original behaviour preserved).
2. If enabled=True   → loads the generated PNG and runs inject_warmth(mode="auto").
   - If the image already passes warm/cool QA → prints status, does nothing.
   - If injection is needed → saves <name>_warminjected.png to the same directory
     and prints the before/after metrics.

NOTES FOR HANA OKONKWO
-----------------------
To apply this pattern to a new generator:
  1. Import run_warmth_hook at the top of your generator.
  2. Add --check-warmth to your argparse block.
  3. Call run_warmth_hook(out_path, enabled=args.check_warmth) after the final .save().
  4. Register your generator in output/tools/README.md noting --check-warmth support.

Author: Jordan Reed / Cycle 37
"""

from __future__ import annotations

import os
import sys

from PIL import Image


def run_warmth_hook(out_path: str, enabled: bool = True) -> str | None:
    """
    Optionally run the warmth-inject post-process on a freshly generated PNG.

    Parameters
    ----------
    out_path : str
        Absolute path to the generated PNG.
    enabled  : bool
        If False, this is a no-op.  Pass ``args.check_warmth`` here.

    Returns
    -------
    str | None
        Path to the _warminjected PNG if injection was applied, otherwise None.
    """
    if not enabled:
        return None

    if not os.path.isfile(out_path):
        print(f"[warmth_hook] WARNING: output PNG not found: {out_path}", file=sys.stderr)
        return None

    # Locate the inject tool relative to this file's directory
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    inject_module_path = os.path.join(tools_dir, "LTG_TOOL_warmth_inject.py")

    if not os.path.isfile(inject_module_path):
        print(
            f"[warmth_hook] ERROR: LTG_TOOL_warmth_inject.py not found in {tools_dir}",
            file=sys.stderr,
        )
        return None

    # Dynamically import inject_warmth so we don't hard-code a sys.path manipulation
    import importlib.util

    spec = importlib.util.spec_from_file_location("LTG_TOOL_warmth_inject", inject_module_path)
    inject_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inject_mod)

    print(f"\n[warmth_hook] --check-warmth: evaluating {os.path.basename(out_path)} ...")

    img = Image.open(out_path)
    result_img, report = inject_mod.inject_warmth(img, mode="auto", base_alpha=40, dry_run=False)

    before = report["before"]
    after = report["after"]

    print(
        f"[warmth_hook] Before: separation={before['separation']:.1f} "
        f"(zone_a={before['zone_a_hue']:.1f}, zone_b={before['zone_b_hue']:.1f})"
    )

    if report["before"]["pass"]:
        print(f"[warmth_hook] Already passing — no injection applied.")
        return None

    # Save injected output
    base, ext = os.path.splitext(out_path)
    injected_path = base + "_warminjected" + ext

    result_img.thumbnail((1280, 1280), Image.LANCZOS)
    result_img.convert("RGB").save(injected_path, format="PNG")

    print(
        f"[warmth_hook] After:  separation={after['separation']:.1f} "
        f"({'PASS' if after['pass'] else 'FAIL/WARN'})"
    )
    print(f"[warmth_hook] Mode: {report['mode_applied']}, alpha: {report['alpha_used']}")
    print(f"[warmth_hook] Saved injected PNG: {injected_path}")

    if not after["pass"]:
        print(
            "[warmth_hook] WARNING: Injection could not push separation to threshold. "
            "Manual warm/cool pass may be needed.",
            file=sys.stderr,
        )

    return injected_path
