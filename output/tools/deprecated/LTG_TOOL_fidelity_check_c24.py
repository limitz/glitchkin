#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_fidelity_check_c24.py
Color Fidelity Check Tool — Cycle 24
"Luma & the Glitchkin" — Sam Kowalski

Samples canonical palette colors from each _styled.png and compares to
the original (non-styled) PNG at the same pixel coordinates.

Canonical targets:
  GL-07 CORRUPT_AMBER  = (255, 140,   0)  #FF8C00
  GL-01b BYTE_TEAL     = (  0, 212, 232)  #00D4E8
  UV_PURPLE            = (123,  47, 190)  #7B2FBE
  SUNLIT_AMBER         = (212, 146,  58)  #D4923A  (RW-02 warm variant)
  SOFT_GOLD / RW-02    = (232, 201,  90)  #E8C95A
  ENV-06               = (150, 172, 162)  #96ACA2

Tolerance: 20 per channel (stylization may shift slightly; >20 = FLAG)
"""

from PIL import Image
import os

BASE = "/home/wipkat/team/output"

# ── Asset pairs: (label, original_path, styled_path) ─────────────────────────
ASSETS = [
    (
        "SF02 — Glitch Storm",
        f"{BASE}/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png",
        f"{BASE}/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v005_styled.png",
    ),
    (
        "SF03 — Other Side",
        f"{BASE}/color/style_frames/LTG_COLOR_styleframe_otherside.png",
        f"{BASE}/color/style_frames/LTG_COLOR_styleframe_otherside_v003_styled.png",
    ),
    (
        "SF01 — Discovery",
        f"{BASE}/color/style_frames/LTG_COLOR_styleframe_discovery.png",
        f"{BASE}/color/style_frames/LTG_COLOR_styleframe_discovery_v003_styled.png",
    ),
    (
        "Kitchen — Grandma",
        f"{BASE}/backgrounds/environments/LTG_ENV_grandma_kitchen.png",
        f"{BASE}/backgrounds/environments/LTG_ENV_grandma_kitchen_styled.png",
    ),
]

# ── Canonical target colors ────────────────────────────────────────────────────
TARGETS = {
    "GL-07 CORRUPT_AMBER (#FF8C00)": (255, 140, 0),
    "GL-01b BYTE_TEAL (#00D4E8)":    (0, 212, 232),
    "UV_PURPLE (#7B2FBE)":           (123, 47, 190),
    "SUNLIT_AMBER / RW-02 (#E8C95A)": (232, 201, 90),
}

TOLERANCE = 20          # max per-channel delta before FLAG
SEARCH_RADIUS = 8       # search grid half-size for nearest-match sampling

# ── Helpers ────────────────────────────────────────────────────────────────────

def color_distance(a, b):
    """Max channel difference between two RGB tuples."""
    return max(abs(a[i] - b[i]) for i in range(3))

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def find_nearest_match(img, target_rgb, tolerance=40, max_samples=5):
    """
    Scan the image for pixels close to target_rgb.
    Returns list of (x, y, actual_rgb) for up to max_samples matches,
    or empty list if none found within tolerance.
    """
    w, h = img.size
    pixels = img.load()
    matches = []
    step = max(1, min(w, h) // 120)   # coarse grid scan
    for y in range(0, h, step):
        for x in range(0, w, step):
            px = pixels[x, y][:3]
            if color_distance(px, target_rgb) <= tolerance:
                matches.append((x, y, px))
                if len(matches) >= max_samples:
                    return matches
    return matches

def check_asset(label, orig_path, styled_path):
    """Run fidelity check on one asset pair."""
    results = {"label": label, "checks": []}

    orig_ok = os.path.exists(orig_path)
    styled_ok = os.path.exists(styled_path)
    results["orig_exists"] = orig_ok
    results["styled_exists"] = styled_ok

    if not orig_ok or not styled_ok:
        return results

    orig_img = Image.open(orig_path).convert("RGB")
    styled_img = Image.open(styled_path).convert("RGB")
    results["orig_size"] = orig_img.size
    results["styled_size"] = styled_img.size

    # Sizes should match for a faithful stylization
    results["size_match"] = (orig_img.size == styled_img.size)

    for target_name, target_rgb in TARGETS.items():
        # Find this color in the ORIGINAL image
        orig_matches = find_nearest_match(orig_img, target_rgb, tolerance=30)

        if not orig_matches:
            results["checks"].append({
                "target": target_name,
                "canonical": rgb_to_hex(target_rgb),
                "status": "SKIP",
                "reason": "Color not found in original — not expected in this scene",
                "samples": [],
            })
            continue

        # Sample the SAME coordinates in the styled image
        check_rows = []
        any_fail = False
        styled_pix = styled_img.load()
        for ox, oy, orig_pix in orig_matches:
            # Clamp coords if styled image is smaller (shouldn't happen)
            sx = min(ox, styled_img.size[0] - 1)
            sy = min(oy, styled_img.size[1] - 1)
            styled_pix_val = styled_pix[sx, sy][:3]
            delta = color_distance(styled_pix_val, orig_pix)
            max_shift = color_distance(styled_pix_val, target_rgb)
            status = "PASS" if max_shift <= TOLERANCE else "FLAG"
            if status == "FLAG":
                any_fail = True
            check_rows.append({
                "coord": (ox, oy),
                "orig_px": rgb_to_hex(orig_pix),
                "styled_px": rgb_to_hex(styled_pix_val),
                "delta_from_orig": delta,
                "delta_from_canonical": max_shift,
                "status": status,
            })

        results["checks"].append({
            "target": target_name,
            "canonical": rgb_to_hex(target_rgb),
            "overall": "FLAG" if any_fail else "PASS",
            "samples": check_rows,
        })

    return results


def print_report(all_results):
    """Print human-readable report and return (report_text, overall_pass)."""
    lines = []
    lines.append("# LTG COLOR Stylization Fidelity Report — Cycle 24")
    lines.append("")
    lines.append("**Author:** Sam Kowalski, Color & Style Artist")
    lines.append("**Date:** 2026-03-29")
    lines.append("**Tool:** LTG_TOOL_fidelity_check_c24.py")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("Pixel-level color fidelity check on all `_styled.png` outputs produced by")
    lines.append("Rin Yamamoto in Cycle 24. Samples canonical palette colors at matching")
    lines.append("coordinates in original vs. styled versions. Tolerance: ±20 per channel.")
    lines.append("")
    lines.append(f"Canonical targets checked per asset:")
    for name in TARGETS:
        lines.append(f"  - {name}")
    lines.append("")

    asset_verdicts = []

    for res in all_results:
        label = res["label"]
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## Asset: {label}")
        lines.append("")

        if not res.get("styled_exists"):
            lines.append(f"**MISSING** — Styled PNG not found at expected path.")
            asset_verdicts.append((label, "MISSING"))
            continue
        if not res.get("orig_exists"):
            lines.append(f"**MISSING** — Original PNG not found.")
            asset_verdicts.append((label, "MISSING"))
            continue

        o_w, o_h = res["orig_size"]
        s_w, s_h = res["styled_size"]
        size_note = "MATCH" if res["size_match"] else f"MISMATCH (orig {o_w}×{o_h}, styled {s_w}×{s_h})"
        lines.append(f"- **Original:** {o_w}×{o_h}px")
        lines.append(f"- **Styled:** {s_w}×{s_h}px  ({size_note})")
        lines.append("")

        asset_fail = False
        for chk in res["checks"]:
            tname = chk["target"]
            canonical = chk["canonical"]
            status = chk.get("overall") or chk["status"]

            if status == "SKIP":
                lines.append(f"### {tname}")
                lines.append(f"  - Status: SKIP — {chk['reason']}")
                lines.append("")
                continue

            if status == "FLAG":
                asset_fail = True

            lines.append(f"### {tname}  →  **{status}**")
            lines.append(f"  Canonical: `{canonical}`  |  Tolerance: ±20 per channel")
            lines.append("")
            for s in chk["samples"]:
                coord_str = f"({s['coord'][0]}, {s['coord'][1]})"
                delta_c = s["delta_from_canonical"]
                delta_o = s["delta_from_orig"]
                px_status = s["status"]
                lines.append(f"  | Coord {coord_str} | orig `{s['orig_px']}` | styled `{s['styled_px']}` | Δcanonical={delta_c} | Δorig={delta_o} | {px_status} |")
            lines.append("")

        verdict = "FLAG" if asset_fail else "PASS"
        asset_verdicts.append((label, verdict))
        lines.append(f"**Asset Verdict: {verdict}**")
        lines.append("")

    # Overall summary table
    lines.append("---")
    lines.append("")
    lines.append("## Overall Results")
    lines.append("")
    lines.append("| Asset | Verdict |")
    lines.append("|-------|---------|")
    all_pass = True
    for av_label, av_verdict in asset_verdicts:
        lines.append(f"| {av_label} | **{av_verdict}** |")
        if av_verdict != "PASS":
            all_pass = False
    lines.append("")
    overall = "ALL PASS" if all_pass else "ISSUES FOUND — see flagged assets above"
    lines.append(f"**Overall: {overall}**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Report generated by LTG_TOOL_fidelity_check_c24.py*")

    return "\n".join(lines), all_pass


def main():
    all_results = []
    for label, orig, styled in ASSETS:
        print(f"Checking: {label}...")
        res = check_asset(label, orig, styled)
        all_results.append(res)

    report_text, all_pass = print_report(all_results)

    out_path = f"{BASE}/color/LTG_COLOR_stylization_fidelity_report_c24.md"
    with open(out_path, "w") as f:
        f.write(report_text)

    print(f"\nReport saved: {out_path}")
    print(f"Overall: {'ALL PASS' if all_pass else 'ISSUES FOUND'}")
    print()
    print(report_text)


if __name__ == "__main__":
    main()
