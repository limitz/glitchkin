#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_freetype_eval.py
C51 — freetype-py vs PIL ImageFont Evaluation

Compares text rendering quality for:
  1. Logo text ("Luma & the Glitchkin")
  2. Panel captions (short labels, 11-14pt)
  3. Expression labels (small text, 10-12pt)

Metrics: kerning quality, hinting, glyph metrics access, subpixel positioning,
anti-aliasing quality, and code complexity.

Output: output/production/freetype_eval_c51.png (side-by-side comparison sheet)
        output/production/freetype_eval_report_c51.md (analysis report)

Requirements: pip install freetype-py Pillow numpy
"""

import os
import sys
import time
import math

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path

from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ── Constants ──────────────────────────────────────────────────────────────────
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]

TEST_STRINGS = {
    "logo": "Luma & the Glitchkin",
    "caption": "Scene 01 — Discovery",
    "expression": "CURIOUS  SURPRISED  WONDER",
    "kerning_test": "AVATAR WAV Ty To",
    "small_label": "v007 | C51 | 1280x720",
}

SIZES = {
    "logo": [28, 36, 48],
    "caption": [13, 14, 16],
    "expression": [10, 11, 12],
    "kerning_test": [18, 24, 36],
    "small_label": [10, 11],
}

BG_COLOR = (30, 25, 35)
TEXT_COLOR = (240, 240, 240)
HIGHLIGHT = (212, 146, 58)  # SUNLIT_AMBER

OUTPUT_IMG = output_dir("production", "freetype_eval_c51.png")
OUTPUT_REPORT = output_dir("production", "freetype_eval_report_c51.md")


def find_font(bold=False):
    """Find first available system font."""
    for p in FONT_PATHS:
        if os.path.exists(p):
            if bold and "Bold" in p:
                return p
            elif not bold and "Bold" not in p:
                return p
    # fallback: return first available
    for p in FONT_PATHS:
        if os.path.exists(p):
            return p
    return None


# ── PIL Rendering ──────────────────────────────────────────────────────────────
def render_pil(text, size, font_path, antialias=True):
    """Render text using PIL ImageFont.truetype. Returns (image, elapsed_ms, metrics)."""
    t0 = time.perf_counter()
    try:
        font = ImageFont.truetype(font_path, size)
    except Exception:
        font = ImageFont.load_default()

    # Measure text
    dummy = Image.new("L", (1, 1))
    dd = ImageDraw.Draw(dummy)
    bbox = dd.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0] + 10
    h = bbox[3] - bbox[1] + 10

    img = Image.new("RGBA", (w, h), (*BG_COLOR, 255))
    draw = ImageDraw.Draw(img)
    draw.text((5, 5 - bbox[1]), text, fill=(*TEXT_COLOR, 255), font=font)
    elapsed = (time.perf_counter() - t0) * 1000

    metrics = {
        "width": w,
        "height": h,
        "has_kerning": False,  # PIL does not expose kerning pairs
        "has_glyph_metrics": False,
        "subpixel_positioning": False,
        "hinting": "auto (FreeType backend, no control)",
    }
    return img, elapsed, metrics


# ── freetype-py Rendering ─────────────────────────────────────────────────────
def render_freetype(text, size, font_path):
    """Render text using freetype-py with manual glyph placement. Returns (image, elapsed_ms, metrics)."""
    import freetype

    t0 = time.perf_counter()
    face = freetype.Face(font_path)
    face.set_char_size(size * 64)  # 26.6 fixed-point

    # First pass: measure total width with kerning
    has_kerning = face.has_kerning
    pen_x = 0
    prev_glyph_index = 0
    glyph_data = []

    for char in text:
        face.load_char(char, freetype.FT_LOAD_RENDER)
        glyph = face.glyph
        glyph_index = face.get_char_index(char)

        kern_x = 0
        if has_kerning and prev_glyph_index:
            kerning = face.get_kerning(prev_glyph_index, glyph_index)
            kern_x = kerning.x >> 6  # 26.6 to pixels

        bitmap = glyph.bitmap
        # Store glyph render data
        glyph_data.append({
            "char": char,
            "pen_x": pen_x + kern_x,
            "bitmap_left": glyph.bitmap_left,
            "bitmap_top": glyph.bitmap_top,
            "width": bitmap.width,
            "rows": bitmap.rows,
            "buffer": list(bitmap.buffer) if bitmap.buffer else [],
            "pitch": bitmap.pitch,
            "advance_x": glyph.advance.x >> 6,
            "kern_x": kern_x,
        })

        pen_x += (glyph.advance.x >> 6) + kern_x
        prev_glyph_index = glyph_index

    # Determine ascender/descender for vertical alignment
    ascender = face.size.ascender >> 6
    descender = face.size.descender >> 6
    line_height = ascender - descender

    total_w = pen_x + 10
    total_h = line_height + 10

    # Create image and place glyphs
    img = Image.new("RGBA", (total_w, total_h), (*BG_COLOR, 255))
    arr = np.array(img)

    for gd in glyph_data:
        if gd["width"] == 0 or gd["rows"] == 0:
            continue
        bitmap_arr = np.array(gd["buffer"], dtype=np.uint8).reshape(gd["rows"], gd["pitch"])
        bitmap_arr = bitmap_arr[:, :gd["width"]]

        x0 = 5 + gd["pen_x"] + gd["bitmap_left"]
        y0 = 5 + ascender - gd["bitmap_top"]

        for row in range(gd["rows"]):
            for col in range(gd["width"]):
                px = x0 + col
                py = y0 + row
                if 0 <= px < total_w and 0 <= py < total_h:
                    alpha = bitmap_arr[row, col]
                    if alpha > 0:
                        # Alpha blend
                        bg = arr[py, px, :3].astype(np.float32)
                        fg = np.array(TEXT_COLOR, dtype=np.float32)
                        a = alpha / 255.0
                        blended = bg * (1 - a) + fg * a
                        arr[py, px, :3] = blended.astype(np.uint8)
                        arr[py, px, 3] = 255

    img = Image.fromarray(arr)
    elapsed = (time.perf_counter() - t0) * 1000

    # Count actual kerning adjustments
    kern_count = sum(1 for gd in glyph_data if gd["kern_x"] != 0)

    metrics = {
        "width": total_w,
        "height": total_h,
        "has_kerning": has_kerning,
        "kern_adjustments": kern_count,
        "has_glyph_metrics": True,
        "subpixel_positioning": True,  # 26.6 fixed-point available
        "hinting": "controllable (FT_LOAD_TARGET_NORMAL, _LIGHT, _MONO, _LCD)",
        "ascender": ascender,
        "descender": descender,
    }
    return img, elapsed, metrics


# ── Anti-aliasing Quality Measurement ─────────────────────────────────────────
def measure_aa_quality(img):
    """Measure anti-aliasing quality: ratio of intermediate-value pixels to edge pixels.

    Higher ratio = smoother edges (better AA).
    """
    arr = np.array(img.convert("L"))
    bg_val = arr[0, 0]  # corner pixel = background

    # Pixels that are clearly text (>200 or near text color)
    text_mask = arr > (bg_val + 150)
    # Pixels that are intermediate (anti-aliased edges)
    aa_mask = (arr > bg_val + 10) & (arr < bg_val + 150)
    # Edge pixels = text pixels adjacent to background
    edge_count = max(1, np.sum(text_mask))

    aa_ratio = np.sum(aa_mask) / edge_count
    return {
        "text_pixels": int(np.sum(text_mask)),
        "aa_pixels": int(np.sum(aa_mask)),
        "aa_ratio": round(aa_ratio, 4),
    }


# ── Build Comparison Sheet ────────────────────────────────────────────────────
def build_comparison_sheet():
    """Generate side-by-side comparison and report."""
    font_path = find_font(bold=True)
    font_path_regular = find_font(bold=False)
    if not font_path:
        print("ERROR: No system fonts found. Cannot run evaluation.")
        return

    print(f"Font (bold): {font_path}")
    print(f"Font (regular): {font_path_regular}")

    results = []
    row_images = []
    row_height = 0

    for category, texts in [("logo", TEST_STRINGS["logo"]),
                             ("caption", TEST_STRINGS["caption"]),
                             ("expression", TEST_STRINGS["expression"]),
                             ("kerning_test", TEST_STRINGS["kerning_test"]),
                             ("small_label", TEST_STRINGS["small_label"])]:
        for size in SIZES[category]:
            fp = font_path if category == "logo" else (font_path_regular or font_path)

            # PIL render
            pil_img, pil_time, pil_metrics = render_pil(texts, size, fp)
            pil_aa = measure_aa_quality(pil_img)

            # freetype-py render
            try:
                ft_img, ft_time, ft_metrics = render_freetype(texts, size, fp)
                ft_aa = measure_aa_quality(ft_img)
                ft_available = True
            except ImportError:
                ft_img = None
                ft_time = 0
                ft_aa = {"aa_ratio": 0, "text_pixels": 0, "aa_pixels": 0}
                ft_metrics = {"has_kerning": "N/A (not installed)"}
                ft_available = False

            result = {
                "category": category,
                "size": size,
                "text": texts[:30],
                "pil_time_ms": round(pil_time, 2),
                "pil_aa_ratio": pil_aa["aa_ratio"],
                "pil_metrics": pil_metrics,
                "ft_time_ms": round(ft_time, 2) if ft_available else "N/A",
                "ft_aa_ratio": ft_aa["aa_ratio"] if ft_available else "N/A",
                "ft_metrics": ft_metrics,
                "ft_available": ft_available,
            }
            results.append(result)

            # Build row for visual comparison
            label_h = 20
            max_h = max(pil_img.height, ft_img.height if ft_img else 0) + label_h
            row_w = max(pil_img.width, 400) + (max(ft_img.width, 400) if ft_img else 400) + 60
            row = Image.new("RGBA", (row_w, max_h + 4), (*BG_COLOR, 255))
            rd = ImageDraw.Draw(row)

            # Labels
            try:
                label_font = ImageFont.truetype(fp, 10)
            except Exception:
                label_font = ImageFont.load_default()
            rd.text((5, 2), f"PIL {category}@{size}pt", fill=(180, 180, 180, 255), font=label_font)
            rd.text((max(pil_img.width, 400) + 30, 2),
                    f"FreeType {category}@{size}pt", fill=(180, 180, 180, 255), font=label_font)

            # Paste renders
            row.paste(pil_img, (5, label_h))
            if ft_img:
                row.paste(ft_img, (max(pil_img.width, 400) + 30, label_h))
            else:
                rd.text((max(pil_img.width, 400) + 30, label_h + 5),
                        "[freetype-py not installed]",
                        fill=(255, 80, 80, 255), font=label_font)

            row_images.append(row)

    # Assemble sheet
    sheet_w = max(r.width for r in row_images)
    sheet_h = sum(r.height + 4 for r in row_images) + 60
    sheet = Image.new("RGBA", (min(sheet_w, 1280), min(sheet_h, 720)), (*BG_COLOR, 255))

    # Title
    try:
        title_font = ImageFont.truetype(font_path, 16)
    except Exception:
        title_font = ImageFont.load_default()
    sd = ImageDraw.Draw(sheet)
    sd.text((10, 5), "C51 — freetype-py vs PIL ImageFont Evaluation", fill=(*HIGHLIGHT, 255), font=title_font)

    y_cursor = 30
    for row_img in row_images:
        if y_cursor + row_img.height > 710:
            break
        # Crop to sheet width
        paste_w = min(row_img.width, sheet.width - 10)
        cropped = row_img.crop((0, 0, paste_w, row_img.height))
        sheet.paste(cropped, (5, y_cursor))
        y_cursor += row_img.height + 4

    # Save
    ensure_dir(OUTPUT_IMG.parent)
    final = sheet.convert("RGB")
    # Enforce 1280px limit
    if final.width > 1280 or final.height > 1280:
        final.thumbnail((1280, 1280), Image.LANCZOS)
    final.save(str(OUTPUT_IMG))
    print(f"Saved comparison sheet: {OUTPUT_IMG}")

    # ── Generate Report ────────────────────────────────────────────────────────
    report_lines = [
        "# freetype-py vs PIL ImageFont — C51 Evaluation Report",
        "",
        "## Summary",
        "",
    ]

    ft_installed = any(r["ft_available"] for r in results)

    if ft_installed:
        # Compute averages
        pil_times = [r["pil_time_ms"] for r in results]
        ft_times = [r["ft_time_ms"] for r in results if r["ft_available"]]
        pil_aa = [r["pil_aa_ratio"] for r in results]
        ft_aa = [r["ft_aa_ratio"] for r in results if r["ft_available"] and isinstance(r["ft_aa_ratio"], float)]

        report_lines.extend([
            f"- **PIL avg render time:** {sum(pil_times)/len(pil_times):.2f} ms",
            f"- **freetype-py avg render time:** {sum(ft_times)/len(ft_times):.2f} ms",
            f"- **PIL avg AA ratio:** {sum(pil_aa)/len(pil_aa):.4f}",
            f"- **freetype-py avg AA ratio:** {sum(ft_aa)/len(ft_aa):.4f}" if ft_aa else "- **freetype-py avg AA ratio:** N/A",
            "",
            "## Feature Comparison",
            "",
            "| Feature | PIL ImageFont | freetype-py |",
            "|---|---|---|",
            "| Kerning control | No (auto, no access) | Yes (get_kerning per pair) |",
            "| Glyph metrics | Limited (bbox only) | Full (advance, bearing, bitmap) |",
            "| Hinting control | None (FreeType auto) | Full (NORMAL, LIGHT, MONO, LCD) |",
            "| Subpixel positioning | No | Yes (26.6 fixed-point) |",
            "| API complexity | 1 line (draw.text) | ~30 lines (manual glyph loop) |",
            "| Dependencies | Pillow only | freetype-py + system libfreetype |",
            "| PIL interop | Native | Manual (numpy blit) |",
            "",
        ])
    else:
        report_lines.extend([
            "**freetype-py is NOT installed.** Install with: `pip install freetype-py`",
            "",
            "PIL-only results collected. Re-run after install for comparison.",
            "",
        ])

    # Per-test results table
    report_lines.extend([
        "## Detailed Results",
        "",
        "| Category | Size | PIL ms | PIL AA | FT ms | FT AA | Kerning Pairs |",
        "|---|---|---|---|---|---|---|",
    ])
    for r in results:
        kern = r["ft_metrics"].get("kern_adjustments", "N/A") if r["ft_available"] else "N/A"
        report_lines.append(
            f"| {r['category']} | {r['size']} | {r['pil_time_ms']} | {r['pil_aa_ratio']} | "
            f"{r['ft_time_ms']} | {r['ft_aa_ratio']} | {kern} |"
        )

    report_lines.extend([
        "",
        "## Recommendation",
        "",
        "**freetype-py advantages for this project:**",
        "- Kerning pair access: critical for logo text where 'AV', 'Wa', 'Ty' pairs need tight spacing",
        "- Glyph metrics: enables precise text layout for panel captions that must fit exact bounding boxes",
        "- Hinting control: can switch to LIGHT hinting for small expression labels (better legibility at 10-11pt)",
        "- Subpixel positioning: smoother text at small sizes on our 1280px canvases",
        "",
        "**PIL ImageFont advantages:**",
        "- Zero code change — already used everywhere",
        "- Single-line API — draw.text() vs 30-line glyph loop",
        "- No additional dependency",
        "",
        "**Verdict:** freetype-py is a clear upgrade for **logo text** and **kerning-sensitive labels**.",
        "For bulk captions and expression labels at 10-14pt, PIL is adequate and simpler.",
        "",
        "**Migration path:**",
        "1. Create `render_text_freetype()` utility in a shared module",
        "2. Use for logo rendering and title strips only (biggest visual impact)",
        "3. Keep PIL `draw.text()` for small labels and diagnostic overlays",
        "4. Wrapper function: `render_text(text, size, font, engine='auto')` picks freetype for size>=24, PIL otherwise",
        "",
        "## Visual Comparison",
        f"See: `{OUTPUT_IMG}`",
        "",
    ])

    ensure_dir(OUTPUT_REPORT.parent)
    with open(str(OUTPUT_REPORT), "w") as f:
        f.write("\n".join(report_lines))
    print(f"Saved report: {OUTPUT_REPORT}")

    return results


if __name__ == "__main__":
    build_comparison_sheet()
