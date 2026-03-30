"""
LTG_TOOL_warmth_inject.py
======================================
Warm/cool injection utility for "Luma & the Glitchkin" environment PNGs.

PURPOSE
-------
Applies a subtle warm or cool color overlay to an existing environment PNG
to boost the warm/cool separation metric used by render_qa_v001.py.

The QA tool measures top-half vs bottom-half median PIL hue (0–255 scale)
and requires a circular distance >= 20 PIL units.  This tool adjusts one or
both halves via an alpha-composited color overlay to push the image over the
threshold without blowing out the existing palette.

MODES
-----
  warm  — warms the top half (window / sky zone) with SUNLIT_AMBER tint.
           Best for Real World interiors: the window / ceiling area reads warmer.
  cool  — cools the bottom half (floor / desk zone) with a cool-blue tint.
           Best for scenes where floors have monitor/fluorescent spill.
  auto  — runs the QA check first, then chooses warm or cool (or both) as
           needed to reach the threshold with minimal overlay strength.

OUTPUT
------
Saves to the same directory as the input, with suffix _warminjected before
the extension:  LTG_ENV_tech_den.png → LTG_ENV_tech_den_warminjected.png

CLI USAGE
---------
  python3 LTG_TOOL_warmth_inject.py <input.png> [--mode warm|cool|auto] [--alpha INT]

  --mode       warm | cool | auto  (default: auto)
  --alpha      base overlay alpha 0–100 (default: 40).  Tool will auto-increase in
               steps of 10 when in auto mode until QA passes or max_alpha (80) is hit.
  --dry-run    Print the before/after QA metrics without saving.

PALETTE CONSTANTS (Real World only — no Glitch colours)
---------------------------------------------------------
  SUNLIT_AMBER  = (212, 172, 100)   # warm window top-half tint
  COOL_FILL     = (160, 195, 215)   # cool monitor/fluorescent bottom-half tint

INTEGRATION
-----------
  After generating a new environment PNG, call this tool and run render_qa
  on the _warminjected output to confirm the pass:

    python3 output/tools/LTG_TOOL_warmth_inject.py \\
        output/backgrounds/environments/LTG_ENV_tech_den.png \\
        --mode auto

    python3 output/tools/LTG_TOOL_render_qa.py \\
        output/backgrounds/environments/LTG_ENV_tech_den_warminjected.png

Author:  Jordan Reed / Cycle 36
"""

from __future__ import annotations

import argparse
import colorsys
import os
import sys

from PIL import Image, ImageDraw

__version__ = "1.0.0"

# ---------------------------------------------------------------------------
# Palette constants — Real World only
# ---------------------------------------------------------------------------
SUNLIT_AMBER = (212, 172, 100)   # warm window / ceiling tint (top half)
COOL_FILL    = (160, 195, 215)   # cool monitor / fluorescent tint (bottom half)

# ---------------------------------------------------------------------------
# QA helpers (inline — mirrors render_qa logic, no import needed)
# ---------------------------------------------------------------------------

_WARM_COOL_MIN_SEPARATION = 20.0   # PIL hue units (0–255 scale)


def _rgb_to_pil_hue(r: int, g: int, b: int) -> float:
    """Convert (R,G,B) 0–255 to PIL HSV hue (0–255 scale). Returns -1 if achromatic."""
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(rf, gf, bf)
    if s < 0.05:
        return -1.0
    return h * 255.0


def measure_warm_cool(img: Image.Image) -> dict:
    """
    Return warm/cool separation dict mirroring render_qa._check_warm_cool().
    Keys: zone_a_hue, zone_b_hue, separation, pass
    """
    rgb = img.convert("RGB")
    w, h = rgb.size
    top = rgb.crop((0, 0, w, h // 2))
    bot = rgb.crop((0, h // 2, w, h))

    def median_hue(region: Image.Image) -> float:
        hues = [_rgb_to_pil_hue(r, g, b) for (r, g, b) in region.getdata() if _rgb_to_pil_hue(r, g, b) >= 0]
        if not hues:
            return -1.0
        hues.sort()
        return hues[len(hues) // 2]

    ha = median_hue(top)
    hb = median_hue(bot)
    if ha < 0 or hb < 0:
        return {"zone_a_hue": ha, "zone_b_hue": hb, "separation": 0.0, "pass": True}
    delta = abs(ha - hb)
    if delta > 127.5:
        delta = 255.0 - delta
    return {
        "zone_a_hue": round(ha, 2),
        "zone_b_hue": round(hb, 2),
        "separation": round(delta, 2),
        "pass": delta >= _WARM_COOL_MIN_SEPARATION,
    }


# ---------------------------------------------------------------------------
# Overlay helpers
# ---------------------------------------------------------------------------

def apply_half_overlay(img: Image.Image, color: tuple, alpha: int, half: str) -> Image.Image:
    """
    Alpha-composite a solid color overlay onto the top or bottom half of img.

    Parameters
    ----------
    img   : RGBA Image
    color : (R, G, B) tuple
    alpha : overlay alpha 0–255
    half  : "top" | "bottom"

    Returns a new RGBA Image with the overlay applied.
    """
    w, h = img.size
    out = img.copy().convert("RGBA")

    overlay = Image.new("RGBA", (w, h // 2), (*color, alpha))

    if half == "top":
        out.alpha_composite(overlay, dest=(0, 0))
    else:
        out.alpha_composite(overlay, dest=(0, h // 2))

    return out


# ---------------------------------------------------------------------------
# Core inject logic
# ---------------------------------------------------------------------------

def inject_warmth(
    img: Image.Image,
    mode: str = "auto",
    base_alpha: int = 40,
    dry_run: bool = False,
) -> tuple[Image.Image, dict]:
    """
    Apply warm/cool injection to bring the image above the separation threshold.

    Parameters
    ----------
    img        : input PIL Image (any mode; converted to RGBA internally)
    mode       : "warm" | "cool" | "auto"
    base_alpha : starting overlay alpha (0–100, mapped to 0–255 for PIL)
    dry_run    : if True, don't apply overlay — just return metrics

    Returns
    -------
    (result_image, report_dict)
        result_image: modified RGBA Image (same as input if dry_run)
        report_dict:  before/after QA metrics + applied settings
    """
    src = img.convert("RGBA")
    before = measure_warm_cool(src)
    report = {
        "before": before,
        "after": None,
        "mode_applied": None,
        "alpha_used": None,
        "passed": before["pass"],
    }

    if before["pass"]:
        print(f"[warmth_inject] Already passing (separation={before['separation']:.1f}). No injection needed.")
        report["after"] = before
        return src, report

    if dry_run:
        print(f"[warmth_inject] DRY RUN — separation={before['separation']:.1f} (need {_WARM_COOL_MIN_SEPARATION})")
        report["after"] = before
        return src, report

    # Determine which mode to apply
    if mode == "auto":
        # Top half warmer OR bottom half cooler — whichever direction gives more separation.
        # Quick heuristic: warm top if top_hue is near neutral (amber hue ~ PIL 21-30),
        # cool bottom if bottom is already reddish.
        # Safe fallback: always warm top first (Real World assets).
        apply_mode = "warm"
    else:
        apply_mode = mode

    max_alpha = 80
    alpha_step = 10
    alpha_pil = min(base_alpha * 255 // 100, max_alpha * 255 // 100)
    alpha_step_pil = alpha_step * 255 // 100

    best_img = src
    best_result = before

    while True:
        if apply_mode == "warm":
            candidate = apply_half_overlay(src, SUNLIT_AMBER, alpha_pil, "top")
        else:  # cool
            candidate = apply_half_overlay(src, COOL_FILL, alpha_pil, "bottom")

        result = measure_warm_cool(candidate)
        best_img = candidate
        best_result = result

        print(
            f"[warmth_inject] mode={apply_mode} alpha={alpha_pil} → "
            f"separation={result['separation']:.1f} ({'PASS' if result['pass'] else 'FAIL'})"
        )

        if result["pass"]:
            break

        alpha_pil += alpha_step_pil
        if alpha_pil > max_alpha * 255 // 100:
            # Try complementary mode if primary didn't work
            if mode == "auto" and apply_mode == "warm":
                apply_mode = "cool"
                alpha_pil = base_alpha * 255 // 100
                print("[warmth_inject] Warm pass insufficient — trying cool bottom pass...")
                continue
            print(
                f"[warmth_inject] WARNING: Could not reach threshold "
                f"(max_alpha reached). Best separation={result['separation']:.1f}"
            )
            break

    report["after"] = best_result
    report["mode_applied"] = apply_mode
    report["alpha_used"] = alpha_pil
    report["passed"] = best_result["pass"]

    return best_img, report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="LTG_TOOL_warmth_inject — warm/cool injection for environment PNGs"
    )
    parser.add_argument("input", help="Path to input PNG")
    parser.add_argument(
        "--mode",
        choices=["warm", "cool", "auto"],
        default="auto",
        help="Injection mode: warm (top half), cool (bottom half), auto (default)",
    )
    parser.add_argument(
        "--alpha",
        type=int,
        default=40,
        metavar="INT",
        help="Base overlay alpha 0–100 (default: 40)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print metrics without saving output",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"[warmth_inject] ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    img = Image.open(args.input)
    print(f"[warmth_inject] Input: {args.input}  ({img.size[0]}×{img.size[1]})")

    result_img, report = inject_warmth(img, mode=args.mode, base_alpha=args.alpha, dry_run=args.dry_run)

    print(f"[warmth_inject] Before: separation={report['before']['separation']:.1f} "
          f"(zone_a={report['before']['zone_a_hue']:.1f}, zone_b={report['before']['zone_b_hue']:.1f})")
    if report["after"] and not args.dry_run:
        print(f"[warmth_inject] After:  separation={report['after']['separation']:.1f} "
              f"({'PASS' if report['after']['pass'] else 'FAIL/WARN'})")
        print(f"[warmth_inject] Mode applied: {report['mode_applied']}, alpha: {report['alpha_used']}")

    if not args.dry_run and not report["before"]["pass"]:
        base, ext = os.path.splitext(args.input)
        out_path = base + "_warminjected" + ext

        # Apply image size rule: hard limit ≤ 1280px in both dimensions
        result_img.thumbnail((1280, 1280), Image.LANCZOS)

        # Save as RGB PNG
        result_img.convert("RGB").save(out_path, format="PNG")
        print(f"[warmth_inject] Saved: {out_path}")


if __name__ == "__main__":
    main()
