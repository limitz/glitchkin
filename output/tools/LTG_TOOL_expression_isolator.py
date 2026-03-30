#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_expression_isolator.py
Hero Expression Isolator — v001
"Luma & the Glitchkin" — Cycle 39 / Maya Santos

PURPOSE:
  Renders a single named expression from any character expression sheet at
  2x panel size (800×800px) for critic review and pitch materials.

  When critics say an expression "doesn't land," the problem may be thumbnail
  scale evaluation surrounded by competing panels. A standalone large-render
  tool lets critics and team evaluate an anchor expression at a size where
  face detail, eye asymmetry, and hand gesture are legible — giving more
  actionable critique data.

USAGE:
  python3 LTG_TOOL_expression_isolator.py \\
      --char luma --expr "THE NOTICING" [--output path.png]

  --char      Character name: luma, byte, cosmo
  --expr      Expression name (as printed on the sheet, case-insensitive)
  --output    Output PNG path (default: auto-generated in output/characters/extras/)
  --size      Output size in pixels (default: 800, max: 1280)
  --list      List available expressions for the named character

STRATEGY:
  Each character has a registered generator module. This tool imports that
  module and calls its render_character() function to produce a single panel
  at the requested size. The panel is then composited on a clean white/neutral
  background with labeling for critic context.

OUTPUT:
  Standalone PNG at requested size (≤1280px). Contains:
  - Character expression rendered at large scale
  - Expression name label (ALL CAPS, bottom strip)
  - Character name and cycle version watermark
  - Panel BG from character's canonical BG color for that expression

Author: Maya Santos
Cycle: 39
Date: 2026-03-29
"""

import argparse
import importlib.util
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ── Paths ──────────────────────────────────────────────────────────────────────
TOOLS_DIR  = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT  = os.path.abspath(os.path.join(TOOLS_DIR, "..", ".."))
OUTPUT_DIR = os.path.join(PROJ_ROOT, "output", "characters", "extras")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Character registry ─────────────────────────────────────────────────────────
# Maps char slug → (module filename, render_function, expr_list_attr, bg_dict_attr, version_label)
# render_fn signature: render_fn(expr_name, panel_w, panel_h, panel_bg=None) → RGBA Image
CHAR_REGISTRY = {
    "luma": {
        "module":      "LTG_TOOL_luma_expression_sheet.py",
        "render_fn":   "render_character",
        "exprs_attr":  "EXPRESSIONS",    # list of expression name strings in slot order
        "bg_attr":     "BG",             # dict: expr_name → (r,g,b) tuple
        "version":     "v011",
        "char_label":  "LUMA",
    },
    "byte": {
        "module":      "LTG_TOOL_byte_expression_sheet.py",
        "render_fn":   "render_expression",  # byte uses a different internal fn name
        "exprs_attr":  "EXPRESSIONS",        # list of tuples; name is index 0
        "bg_attr":     None,                 # byte BG is embedded in expr tuple (index 5)
        "version":     "v006",
        "char_label":  "BYTE",
    },
    "cosmo": {
        "module":      "LTG_TOOL_cosmo_expression_sheet.py",
        "render_fn":   "render_character",
        "exprs_attr":  "EXPRESSIONS",
        "bg_attr":     "BG",
        "version":     "v007",
        "char_label":  "COSMO",
    },
}


def load_module(module_path):
    """Dynamically load a Python module from an absolute path."""
    spec   = importlib.util.spec_from_file_location("_ltg_char_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_expr_names(module, char_cfg):
    """Extract list of expression name strings from the loaded module."""
    exprs_raw = getattr(module, char_cfg["exprs_attr"])
    names = []
    for e in exprs_raw:
        if isinstance(e, str):
            names.append(e)
        elif isinstance(e, (list, tuple)):
            # Byte style: (name, symbol, emotion, body, right_eye, bg, ...)
            names.append(e[0])
    return names


def find_expr(expr_arg, expr_names):
    """Case-insensitive match of expr_arg against available expression names.
    Returns the canonical name or raises ValueError."""
    needle = expr_arg.strip().upper()
    for name in expr_names:
        if name.upper() == needle:
            return name
    # Partial match fallback
    matches = [n for n in expr_names if needle in n.upper()]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        raise ValueError(
            f"Ambiguous expression '{expr_arg}'. Matches: {matches}\n"
            f"Use the full name."
        )
    raise ValueError(
        f"Expression '{expr_arg}' not found. Available: {expr_names}"
    )


def get_panel_bg(module, char_cfg, expr_name):
    """Retrieve the panel background color for the given expression."""
    if char_cfg["bg_attr"] is not None:
        bg_dict = getattr(module, char_cfg["bg_attr"], {})
        if expr_name in bg_dict:
            return bg_dict[expr_name]
        return (230, 225, 215)  # fallback neutral
    else:
        # Byte: bg embedded in EXPRESSIONS tuple at index 5
        exprs_raw = getattr(module, char_cfg["exprs_attr"])
        for e in exprs_raw:
            if isinstance(e, (list, tuple)) and e[0] == expr_name:
                if len(e) > 5:
                    return e[5]
        return (28, 34, 42)  # Byte dark default


def render_isolated_byte(module, expr_name, char_area, panel_bg):
    """
    Special-case renderer for Byte, whose module does not expose a
    render_character(name, w, h) API. Instead it exposes draw_byte().
    We build a clean panel, find the matching expression tuple, and call draw_byte().
    """
    # Find the expression tuple in EXPRESSIONS
    exprs_raw = getattr(module, "EXPRESSIONS")
    expr_tuple = None
    for e in exprs_raw:
        if isinstance(e, (list, tuple)) and e[0] == expr_name:
            expr_tuple = e
            break
    if expr_tuple is None:
        raise ValueError(f"Byte expression '{expr_name}' not found in EXPRESSIONS.")

    name, symbol, emotion, body_data, right_eye_style, bg_col = (
        expr_tuple[0], expr_tuple[1], expr_tuple[2],
        expr_tuple[3], expr_tuple[4], expr_tuple[5]
    )

    img  = Image.new("RGB", (char_area, char_area), bg_col)
    draw = ImageDraw.Draw(img)

    # Special backgrounds
    draw_storm_bg = getattr(module, "draw_storm_bg_texture", None)
    draw_warmth   = getattr(module, "draw_warmth_bg", None)
    if emotion == "storm" and draw_storm_bg:
        draw_storm_bg(draw, 0, 0, char_area, char_area, bg_col)
        draw = ImageDraw.Draw(img)
    if name == "UNGUARDED WARMTH" and draw_warmth:
        draw_warmth(draw, 0, 0, char_area, char_area)
        draw = ImageDraw.Draw(img)

    draw_byte = getattr(module, "draw_byte")
    byte_size = min(88, int(char_area * 0.30))   # scale up proportionally
    bcx = char_area // 2
    bcy = char_area // 2 - int(char_area * 0.08)

    draw_byte(draw, bcx, bcy, byte_size, name, symbol, emotion, body_data, right_eye_style, img)
    return img.convert("RGB")


def render_isolated(module, char_cfg, expr_name, out_size):
    """
    Render the expression at out_size × out_size using the character's
    render_character() function.

    Returns an RGB Image at out_size×out_size with label strip.
    """
    LABEL_STRIP = 48      # px for label at bottom
    char_area   = out_size - LABEL_STRIP
    panel_bg    = get_panel_bg(module, char_cfg, expr_name)

    char_img = None

    # Byte special case: no render_character() API
    if char_cfg.get("render_fn") == "render_expression" or char_cfg.get("char_label") == "BYTE":
        char_img = render_isolated_byte(module, expr_name, char_area, panel_bg)
    else:
        # Try to call render_character
        render_fn_name = char_cfg["render_fn"]
        render_fn = getattr(module, render_fn_name, None)
        if render_fn is None:
            render_fn = getattr(module, "render_character", None)
        if render_fn is None:
            raise RuntimeError(
                f"Cannot find render function '{render_fn_name}' in module."
            )

        # Call the render function.
        #   render_character(expr_name, panel_w, panel_h, panel_bg=bg)  ← luma/cosmo
        try:
            char_img = render_fn(expr_name, char_area, char_area, panel_bg=panel_bg)
        except TypeError:
            try:
                char_img = render_fn(expr_name, char_area, char_area)
            except TypeError:
                raise RuntimeError(
                    f"Cannot call render function with expected signature. "
                    f"Check module API for '{render_fn_name}'."
                )

    # If char_img is RGBA, composite onto panel_bg
    if char_img.mode == "RGBA":
        bg_img = Image.new("RGB", (char_area, char_area), panel_bg)
        bg_img.paste(char_img, (0, 0), char_img)
        char_img = bg_img
    else:
        char_img = char_img.convert("RGB")

    # Build final image: character area + label strip
    final = Image.new("RGB", (out_size, out_size), panel_bg)
    final.paste(char_img, (0, 0))

    # Draw label strip
    draw = ImageDraw.Draw(final)
    strip_y = char_area
    draw.rectangle([0, strip_y, out_size - 1, out_size - 1], fill=(30, 26, 22))

    try:
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_label = ImageFont.load_default()
        font_sub   = font_label

    # Expression name centered
    label = expr_name.upper()
    bbox  = draw.textbbox((0, 0), label, font=font_label)
    tw    = bbox[2] - bbox[0]
    tx    = (out_size - tw) // 2
    ty    = strip_y + (LABEL_STRIP - (bbox[3] - bbox[1])) // 2 - 8
    draw.text((tx, ty), label, fill=(230, 215, 195), font=font_label)

    # Sub-label: character name + version + LTG
    sub = (f"{char_cfg['char_label']}  |  {char_cfg['version']}  |  "
           f"Luma & the Glitchkin  |  Maya Santos C39")
    bbox2 = draw.textbbox((0, 0), sub, font=font_sub)
    sx    = (out_size - (bbox2[2] - bbox2[0])) // 2
    sy    = ty + (bbox[3] - bbox[1]) + 4
    draw.text((sx, sy), sub, fill=(140, 130, 118), font=font_sub)

    return final


def main():
    parser = argparse.ArgumentParser(
        description="LTG Hero Expression Isolator — renders a single expression at large scale."
    )
    parser.add_argument("--char",   required=False, default="luma",
                        help="Character slug: luma, byte, cosmo (default: luma)")
    parser.add_argument("--expr",   required=False,
                        help="Expression name (case-insensitive). Use --list to see options.")
    parser.add_argument("--output", required=False, default=None,
                        help="Output PNG path (default: auto-generated in output/characters/extras/)")
    parser.add_argument("--size",   required=False, type=int, default=800,
                        help="Output size in pixels, square (default: 800, max: 1280)")
    parser.add_argument("--list",   action="store_true",
                        help="List available expressions for the named character and exit.")
    args = parser.parse_args()

    char_slug = args.char.strip().lower()
    if char_slug not in CHAR_REGISTRY:
        print(f"ERROR: unknown character '{char_slug}'. Available: {list(CHAR_REGISTRY.keys())}")
        sys.exit(1)

    char_cfg    = CHAR_REGISTRY[char_slug]
    module_path = os.path.join(TOOLS_DIR, char_cfg["module"])
    if not os.path.exists(module_path):
        print(f"ERROR: character module not found: {module_path}")
        sys.exit(1)

    module     = load_module(module_path)
    expr_names = get_expr_names(module, char_cfg)

    if args.list:
        print(f"\nAvailable expressions for {char_cfg['char_label']} ({char_cfg['version']}):")
        for i, name in enumerate(expr_names):
            if name:
                print(f"  [{i:02d}]  {name}")
        return

    if not args.expr:
        print("ERROR: --expr is required (or use --list to see available expressions).")
        sys.exit(1)

    # Resolve expression
    try:
        expr_name = find_expr(args.expr, expr_names)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Validate and clamp size
    out_size = min(max(args.size, 100), 1280)
    if args.size > 1280:
        print(f"WARNING: size {args.size} exceeds 1280px hard limit — clamped to 1280.")

    print(f"Isolating: {char_cfg['char_label']} / {expr_name} at {out_size}×{out_size}px")

    # Render
    img = render_isolated(module, char_cfg, expr_name, out_size)

    # Enforce size limit (belt-and-suspenders)
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    # Output path
    if args.output:
        out_path = args.output
    else:
        safe_expr = expr_name.upper().replace(" ", "_").replace("/", "_").replace("—", "")
        safe_expr = "".join(c if c.isalnum() or c == "_" else "" for c in safe_expr)
        fname     = (f"LTG_CHAR_{char_slug}_isolated_{safe_expr}_"
                     f"{char_cfg['version']}_{out_size}px.png")
        out_path  = os.path.join(OUTPUT_DIR, fname)

    img.save(out_path)
    print(f"Saved: {out_path}")
    print(f"Size:  {img.width}×{img.height}px")


if __name__ == "__main__":
    main()
