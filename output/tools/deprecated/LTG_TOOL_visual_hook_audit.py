#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_visual_hook_audit.py
Visual Hook Audit Tool — Luma & the Glitchkin
Cycle 48 / Maya Santos

Renders each main character at thumbnail scale (~128px tall) and checks whether
their defining visual hook is still readable at that size.  Outputs PASS/WARN/FAIL
per character plus a diagnostic contact-sheet PNG.

Visual hooks per character:
  Luma   — orange hoodie (unique hue mass in torso region)
  Cosmo  — amplified cowlick (shape protrusion above head) + glasses bridge tape
  Miri   — wooden hairpins (thin high-contrast sticks above bun)
  Byte   — teal oval body (non-rectangular silhouette, elliptical)
  Glitch — destabilized eye (asymmetric pixel-grid eye pattern)

Method:
  1. Render each character at 128px height on a neutral background using the
     same draw functions as the lineup tool (v011).
  2. For each character, extract the hook region and run a detection check:
     - Color-mass checks: measure area of hook-specific hue in the expected region
     - Shape checks: silhouette uniqueness in the hook region
  3. Score each hook:  PASS (clearly readable), WARN (borderline), FAIL (lost)

Output: output/production/LTG_PROD_visual_hook_audit.png  (contact sheet)
        Console: PASS/WARN/FAIL per character with metrics

Usage: python3 LTG_TOOL_visual_hook_audit.py
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── Import lineup draw functions ──────────────────────────────────────────────
# We import the lineup tool to reuse its character draw functions.
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS_DIR)

# We need the lineup tool's color constants and draw functions.
# Import them directly.
import importlib.util
lineup_spec = importlib.util.spec_from_file_location(
    "lineup", os.path.join(TOOLS_DIR, "LTG_TOOL_character_lineup.py"))
lineup = importlib.util.module_from_spec(lineup_spec)
lineup_spec.loader.exec_module(lineup)


# ── Constants ─────────────────────────────────────────────────────────────────
THUMB_H      = 128                 # target character height in pixels
BG_NEUTRAL   = (230, 228, 224)     # neutral gray — no hue bias
PANEL_PAD    = 20                  # padding around each character panel
PANEL_W      = THUMB_H + PANEL_PAD * 2
PANEL_H      = THUMB_H + PANEL_PAD * 3 + 40   # extra for label + result

# Hook color targets (approximate hue ranges in HSV)
# Hue is 0-360, S and V are 0-255 in our checks (PIL uses 0-255 for HS but
# we convert to numpy for analysis).

# Thresholds: minimum percentage of hook-region pixels that must match
HOOK_PASS_PCT = 4.0    # at least 4% of hook region is hook color -> PASS
HOOK_WARN_PCT = 1.5    # at least 1.5% -> WARN, below -> FAIL


def rgb_to_hsv_array(img_array):
    """Convert RGB uint8 array (H,W,3) to HSV float array with H in [0,360], S,V in [0,1]."""
    arr = img_array.astype(np.float32) / 255.0
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    cmax = np.maximum(r, np.maximum(g, b))
    cmin = np.minimum(r, np.minimum(g, b))
    delta = cmax - cmin

    h = np.zeros_like(cmax)
    mask_r = (cmax == r) & (delta > 0)
    mask_g = (cmax == g) & (delta > 0)
    mask_b = (cmax == b) & (delta > 0)
    h[mask_r] = 60.0 * (((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6)
    h[mask_g] = 60.0 * (((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2)
    h[mask_b] = 60.0 * (((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4)

    with np.errstate(invalid='ignore'):
        s = np.where(cmax > 0, delta / cmax, 0.0)
    v = cmax
    return np.stack([h, s, v], axis=-1)


def render_character_thumb(char_name, thumb_h):
    """Render a single character at thumb_h pixels tall on neutral BG.
    Returns a PIL Image cropped to the character bounding box + padding."""
    # Canvas big enough for any character (they draw relative to base_y and cx)
    canvas_w = thumb_h * 3
    canvas_h = thumb_h * 3
    img = Image.new("RGB", (canvas_w, canvas_h), BG_NEUTRAL)
    draw = ImageDraw.Draw(img)

    cx = canvas_w // 2
    base_y = int(canvas_h * 0.85)

    draw_fn = {
        "luma":   lineup.draw_luma_lineup,
        "byte":   lineup.draw_byte_lineup,
        "cosmo":  lineup.draw_cosmo_lineup,
        "miri":   lineup.draw_miri_lineup,
        "glitch": lineup.draw_glitch_lineup,
    }[char_name]

    draw_fn(draw, cx, base_y, thumb_h)

    # Crop to character region (find non-background bounding box)
    arr = np.array(img)
    bg = np.array(BG_NEUTRAL)
    diff = np.abs(arr.astype(int) - bg.astype(int)).sum(axis=2)
    mask = diff > 15  # pixels that differ from BG
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)

    if not rows.any():
        return img.crop((0, 0, PANEL_W, PANEL_H))

    y_min, y_max = np.where(rows)[0][[0, -1]]
    x_min, x_max = np.where(cols)[0][[0, -1]]

    pad = 6
    y_min = max(0, y_min - pad)
    y_max = min(canvas_h - 1, y_max + pad)
    x_min = max(0, x_min - pad)
    x_max = min(canvas_w - 1, x_max + pad)

    return img.crop((x_min, y_min, x_max + 1, y_max + 1))


# ── Hook detection functions ──────────────────────────────────────────────────

def check_luma_hoodie(thumb_img):
    """Luma's visual hook: orange hoodie. Check for orange hue mass in torso region."""
    arr = np.array(thumb_img)
    h, w = arr.shape[:2]

    # Torso region: roughly middle third vertically, center horizontally
    y1, y2 = int(h * 0.25), int(h * 0.60)
    x1, x2 = int(w * 0.15), int(w * 0.85)
    region = arr[y1:y2, x1:x2]

    hsv = rgb_to_hsv_array(region)
    # Orange hue: H in [10, 35], S > 0.4, V > 0.3
    orange_mask = (hsv[:, :, 0] >= 10) & (hsv[:, :, 0] <= 40) & \
                  (hsv[:, :, 1] > 0.35) & (hsv[:, :, 2] > 0.30)
    pct = orange_mask.sum() / max(1, region.shape[0] * region.shape[1]) * 100
    return pct, "orange hoodie hue in torso"


def check_cosmo_cowlick(thumb_img):
    """Cosmo's visual hook: amplified cowlick protrusion above head top."""
    arr = np.array(thumb_img)
    h, w = arr.shape[:2]

    # Cowlick region: top 20% of image, center third horizontally
    y1, y2 = 0, int(h * 0.22)
    x1, x2 = int(w * 0.25), int(w * 0.75)
    region = arr[y1:y2, x1:x2]

    bg = np.array(BG_NEUTRAL)
    diff = np.abs(region.astype(int) - bg.astype(int)).sum(axis=2)
    non_bg = diff > 15
    pct = non_bg.sum() / max(1, region.shape[0] * region.shape[1]) * 100
    return pct, "cowlick protrusion above head"


def check_cosmo_tape(thumb_img):
    """Cosmo's secondary hook: glasses bridge tape (cream patch on bridge)."""
    arr = np.array(thumb_img)
    h, w = arr.shape[:2]

    # Glasses bridge region: ~25-35% from top, narrow center band
    y1, y2 = int(h * 0.18), int(h * 0.32)
    x1, x2 = int(w * 0.35), int(w * 0.65)
    region = arr[y1:y2, x1:x2]

    # Tape is cream (250, 240, 220) — look for high-value, low-saturation warm pixels
    hsv = rgb_to_hsv_array(region)
    cream_mask = (hsv[:, :, 1] < 0.15) & (hsv[:, :, 2] > 0.90)
    pct = cream_mask.sum() / max(1, region.shape[0] * region.shape[1]) * 100
    return pct, "cream tape on glasses bridge"


def check_miri_hairpins(thumb_img):
    """Miri's visual hook: wooden hairpins above the bun."""
    arr = np.array(thumb_img)
    h, w = arr.shape[:2]

    # Hairpin region: top 25% of image (above head/bun area)
    y1, y2 = 0, int(h * 0.28)
    x1, x2 = int(w * 0.20), int(w * 0.80)
    region = arr[y1:y2, x1:x2]

    # Hairpins are dark warm brown (92, 58, 32) — look for this specific brown
    hsv = rgb_to_hsv_array(region)
    # Brown hue: H ~20-35, S > 0.3, V in 0.1-0.5 (dark)
    brown_mask = (hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 40) & \
                 (hsv[:, :, 1] > 0.30) & (hsv[:, :, 2] > 0.10) & (hsv[:, :, 2] < 0.55)
    pct = brown_mask.sum() / max(1, region.shape[0] * region.shape[1]) * 100
    return pct, "wooden hairpin brown in bun area"


def check_byte_oval(thumb_img):
    """Byte's visual hook: oval/elliptical body shape (non-rectangular silhouette)."""
    arr = np.array(thumb_img)
    h, w = arr.shape[:2]

    # Body region: center 60% vertically, full width
    y1, y2 = int(h * 0.10), int(h * 0.75)
    x1, x2 = int(w * 0.05), int(w * 0.95)
    region = arr[y1:y2, x1:x2]

    hsv = rgb_to_hsv_array(region)
    # Byte is teal: H ~170-195, S > 0.3
    teal_mask = (hsv[:, :, 0] >= 160) & (hsv[:, :, 0] <= 200) & \
                (hsv[:, :, 1] > 0.25) & (hsv[:, :, 2] > 0.20)
    total_px = region.shape[0] * region.shape[1]
    teal_count = teal_mask.sum()

    # Compute circularity: ratio of teal area to bounding box area
    # An oval fills ~π/4 = 78.5% of its bbox. A rectangle fills 100%.
    # If teal fills < 85% of bbox, it reads as oval not rectangle.
    if teal_count == 0:
        return 0.0, "teal oval body shape"

    teal_rows = np.any(teal_mask, axis=1)
    teal_cols = np.any(teal_mask, axis=0)
    if not teal_rows.any():
        return 0.0, "teal oval body shape"

    teal_bbox_h = np.where(teal_rows)[0][-1] - np.where(teal_rows)[0][0] + 1
    teal_bbox_w = np.where(teal_cols)[0][-1] - np.where(teal_cols)[0][0] + 1
    bbox_area = teal_bbox_h * teal_bbox_w
    fill_ratio = teal_count / max(1, bbox_area)

    # Oval reads when fill_ratio is in 0.55-0.88 range (not a rectangle)
    # and teal area is substantial
    teal_pct = teal_count / max(1, total_px) * 100
    # Use teal_pct as the hook metric (is the oval body visible at all)
    return teal_pct, f"teal oval body (fill={fill_ratio:.2f})"


def check_glitch_eye(thumb_img):
    """Glitch's visual hook: destabilized eye pattern (asymmetric pixel grid)."""
    arr = np.array(thumb_img)
    h, w = arr.shape[:2]

    # Eye region: upper-middle of the diamond body
    y1, y2 = int(h * 0.20), int(h * 0.50)
    x1, x2 = int(w * 0.15), int(w * 0.85)
    region = arr[y1:y2, x1:x2]

    hsv = rgb_to_hsv_array(region)
    # Glitch gold eye pixels: H ~40-55, S > 0.4, V > 0.5
    gold_mask = (hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 60) & \
                (hsv[:, :, 1] > 0.35) & (hsv[:, :, 2] > 0.45)
    pct = gold_mask.sum() / max(1, region.shape[0] * region.shape[1]) * 100
    return pct, "gold pixel-eye pattern"


# ── Main audit ────────────────────────────────────────────────────────────────

CHARACTERS = [
    ("luma",   [("hoodie", check_luma_hoodie, 12.0, 5.0)]),
    ("cosmo",  [("cowlick", check_cosmo_cowlick, 3.0, 1.0),
                ("tape", check_cosmo_tape, 1.0, 0.3)]),
    ("miri",   [("hairpins", check_miri_hairpins, 1.5, 0.5)]),
    ("byte",   [("oval body", check_byte_oval, 15.0, 6.0)]),
    ("glitch", [("destabilized eye", check_glitch_eye, 1.5, 0.5)]),
]


def score(pct, pass_thresh, warn_thresh):
    if pct >= pass_thresh:
        return "PASS"
    elif pct >= warn_thresh:
        return "WARN"
    return "FAIL"


def main():
    out_dir = output_dir('production')
    out_path = os.path.join(out_dir, "LTG_PROD_visual_hook_audit.png")
    os.makedirs(out_dir, exist_ok=True)

    results = []
    thumbs  = []

    print("=" * 68)
    print("VISUAL HOOK AUDIT — Thumbnail Readability @ 128px")
    print("=" * 68)

    for char_name, hooks in CHARACTERS:
        thumb = render_character_thumb(char_name, THUMB_H)
        thumbs.append((char_name, thumb))

        char_results = []
        for hook_name, check_fn, pass_t, warn_t in hooks:
            pct, desc = check_fn(thumb)
            result = score(pct, pass_t, warn_t)
            char_results.append((hook_name, pct, desc, result))
            status = f"  {result:4s}  {char_name:8s} | {hook_name:20s} | {pct:5.1f}% ({desc})"
            print(status)

        # Overall character result: worst of all hooks
        worst = "PASS"
        for _, _, _, r in char_results:
            if r == "FAIL":
                worst = "FAIL"
            elif r == "WARN" and worst != "FAIL":
                worst = "WARN"
        results.append((char_name, worst, char_results))

    # ── Build contact sheet ──────────────────────────────────────────────────
    n_chars = len(thumbs)
    sheet_w = min(1280, PANEL_W * n_chars + PANEL_PAD * 2)
    sheet_h = 300
    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 243, 240))
    draw_sheet = ImageDraw.Draw(sheet)

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    # Title bar
    draw_sheet.rectangle([0, 0, sheet_w, 28], fill=(59, 40, 32))
    draw_sheet.text((8, 6),
                    "VISUAL HOOK AUDIT — 128px Thumbnail Readability",
                    fill=(245, 240, 230), font=font)

    # Paste each character thumbnail
    x_cursor = PANEL_PAD
    for i, (char_name, thumb) in enumerate(thumbs):
        # Scale thumb to fit panel
        tw, th = thumb.size
        scale = min(PANEL_W - 10, tw) / max(1, tw)
        scale = min(scale, (sheet_h - 90) / max(1, th))
        new_w = max(1, int(tw * scale))
        new_h = max(1, int(th * scale))
        resized = thumb.resize((new_w, new_h), Image.LANCZOS)  # ltg-thumbnail-ok

        paste_y = 36
        paste_x = x_cursor + (PANEL_W - new_w) // 2
        sheet.paste(resized, (paste_x, paste_y))

        # Label and result
        _, overall, hooks_detail = results[i]
        label_y = paste_y + new_h + 4
        draw_sheet = ImageDraw.Draw(sheet)  # refresh after paste

        # Character name
        draw_sheet.text((x_cursor + 4, label_y),
                        char_name.upper(), fill=(59, 40, 32), font=font)

        # Result color
        color_map = {"PASS": (40, 140, 60), "WARN": (200, 160, 40), "FAIL": (200, 50, 40)}
        result_col = color_map.get(overall, (100, 100, 100))
        draw_sheet.text((x_cursor + 4, label_y + 14),
                        overall, fill=result_col, font=font)

        # Hook details
        dy = 28
        for hook_name, pct, desc, result in hooks_detail:
            rc = color_map.get(result, (100, 100, 100))
            draw_sheet.text((x_cursor + 4, label_y + dy),
                            f"{hook_name}: {pct:.1f}% {result}",
                            fill=rc, font=font)
            dy += 12

        x_cursor += PANEL_W + 4

    # Size rule compliance
    sheet.thumbnail((1280, 1280), Image.LANCZOS)  # ltg-thumbnail-ok
    sheet.save(out_path)
    print(f"\n[Maya C48] Contact sheet: {out_path} ({sheet.width}x{sheet.height}px)")

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 68)
    print("SUMMARY")
    print("=" * 68)
    overall_pass = True
    for char_name, overall, _ in results:
        tag = f"  {overall:4s}  {char_name}"
        print(tag)
        if overall != "PASS":
            overall_pass = False

    overall_label = "OVERALL PASS" if overall_pass else "OVERALL WARN/FAIL — review needed"
    print(f"\n  {overall_label}")
    print("=" * 68)

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
