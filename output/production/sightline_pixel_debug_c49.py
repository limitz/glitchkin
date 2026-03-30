# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
Debug script: examine pixel values around Luma's eyes in SF01 v007.
Outputs pixel color info to help tune pixel-based sightline detection.
"""
import os, sys
from PIL import Image
import numpy as np

def main():
    sf01 = os.path.join(os.path.dirname(__file__), "..",
                        "color", "style_frames", "LTG_COLOR_styleframe_discovery.png")
    sf01 = os.path.normpath(sf01)
    img = Image.open(sf01).convert("RGB")
    arr = np.array(img)

    # Known geometry
    min_r = min(1280/1920, 720/1080)  # 0.6667
    scale = 0.92
    def p(n): return int(n * scale * min_r)
    hcx, hcy = 411, 433

    lex = hcx + p(4)
    ley = hcy - p(10)
    rex = hcx + p(38)
    rey = hcy - p(8)
    print(f"Left eye center (construction): ({lex}, {ley})")
    print(f"Right eye center (construction): ({rex}, {rey})")

    # Sample pixel colors around eyes
    for name, ecx, ecy in [("LEFT_EYE", lex, ley), ("RIGHT_EYE", rex, rey)]:
        print(f"\n--- {name} at ({ecx}, {ecy}) ---")
        for dy in range(-12, 13, 3):
            row = []
            for dx in range(-12, 13, 3):
                px, py = ecx + dx, ecy + dy
                if 0 <= px < 1280 and 0 <= py < 720:
                    r, g, b = arr[py, px]
                    v = max(r, g, b)
                    mn = min(r, g, b)
                    sat = (v - mn) / v if v > 0 else 0
                    row.append(f"({r:3d},{g:3d},{b:3d}) V={v:3d} S={sat:.2f}")
                else:
                    row.append("(out of bounds)")
            print(f"  dy={dy:+3d}: " + " | ".join(row))

    # Also check what the detection is picking up
    # Eye white mask: V>=200, S<=0.15, close to known whites
    search_box = (291, 313, 531, 553)
    x0, y0, x1, y1 = search_box
    region = arr[y0:y1, x0:x1]
    value = np.max(region, axis=2)
    min_ch = np.min(region, axis=2)
    sat = np.where(value > 0, (value.astype(float) - min_ch.astype(float)) / value.astype(float), 0)

    bright_low_sat = (value >= 200) & (sat <= 0.15)
    ey, ex = np.where(bright_low_sat)
    print(f"\nBright + low-sat pixels in search box: {len(ex)}")

    # Show unique colors of those pixels
    if len(ex) > 0:
        colors = {}
        for i in range(len(ex)):
            c = tuple(region[ey[i], ex[i]])
            colors[c] = colors.get(c, 0) + 1
        print("Top 20 colors:")
        for c, cnt in sorted(colors.items(), key=lambda x: -x[1])[:20]:
            print(f"  RGB{c}: {cnt}px")

    # Now test with tighter tolerance: only match actual sclera, not catch-lights
    # Sclera in SF01: (242, 240, 248) — slight blue tint
    from collections import Counter
    sclera_ref = np.array([242, 240, 248], dtype=float)
    dists = np.sqrt(np.sum((region[ey, ex].astype(float) - sclera_ref) ** 2, axis=1))
    print(f"\nDistance from (242,240,248) for bright/low-sat pixels:")
    bins = [0, 10, 20, 30, 40, 50, 60, 80, 100, 150, 200]
    for i in range(len(bins)-1):
        cnt = np.sum((dists >= bins[i]) & (dists < bins[i+1]))
        print(f"  {bins[i]:3d}-{bins[i+1]:3d}: {cnt}px")


if __name__ == "__main__":
    main()
