#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_fill_light_adapter.py — Resolution-Aware Fill Light Adapter
"Luma & the Glitchkin"
Author: Rin Yamamoto | Cycle 39 (v1.0.0), Cycle 40 (v1.1.0)

PURPOSE
-------
A resolution-aware fill light adapter for any PIL-based generator. This module
provides a unified interface so fill light effects work correctly at any canvas
size without the caller needing to scale parameters manually.

PROBLEM SOLVED (C36/C37 ideabox — Rin Yamamoto):
  The original fill light fix module (LTG_TOOL_sf02_fill_light_fix_c35.py)
  hardcoded W=1280, H=720. Generators rendering at 1920×1080 triggered PIL
  alpha_composite failures ("images do not match"). The C37 fix added canvas_w/
  canvas_h params to that module. This adapter takes it one step further:
  provides a clean, generator-agnostic interface that accepts:
    - fractional (0.0–1.0) OR absolute (pixel) character positions
    - auto-scales all radii, blur radii, and alpha gradients to canvas size
    - works with any PIL-generated frame regardless of resolution

DESIGN
------
  FillLightConfig  — dataclass-style config for a single fill light effect
  FillLightAdapter — main class; resolves coords, builds overlay, composites

  Supports two position modes:
    - "fractional": cx/cy given as 0.0–1.0 fractions of canvas dimensions
    - "absolute":   cx/cy given as pixel values (for generators that already
                    have exact pixel coords)

v1.1.0 (C40) — Scene Presets Registry:
  load_scene_configs(scene_name, presets_path=None) — loads FillLightConfig list
  from LTG_fill_light_presets.json. Falls back to hardcoded if JSON absent.
  Supported scene names: "SF01", "SF02", "SF03", "SF04".
  char_h_frac for each scene is also returned from the registry.

USAGE
-----
  from LTG_TOOL_fill_light_adapter import FillLightAdapter, FillLightConfig
  from LTG_TOOL_fill_light_adapter import load_scene_configs

  # Registry-based (v1.1.0):
  configs, char_h_frac = load_scene_configs("SF02")
  img = apply_fill_light(img, configs, canvas_w=1280, canvas_h=720,
                         char_h_frac=char_h_frac)

  # Manual config:
  adapter = FillLightAdapter(canvas_w=1280, canvas_h=720)
  configs = [
      FillLightConfig(cx=0.45, cy=0.65, color=(255, 45, 107), alpha_max=35,
                      source_dx=+0.5, source_dy=-0.8, label="luma"),
      FillLightConfig(cx=0.28, cy=0.60, color=(255, 45, 107), alpha_max=35,
                      source_dx=+0.5, source_dy=-0.8, label="byte"),
  ]
  img = adapter.apply(img, configs, char_h_frac=0.18)

  # Absolute pixel mode (pass pos_mode="absolute" per config):
  configs_abs = [
      FillLightConfig(cx=576, cy=468, color=(255, 45, 107), alpha_max=35,
                      source_dx=+0.5, source_dy=-0.8, pos_mode="absolute",
                      label="luma"),
  ]
  img = adapter.apply(img, configs_abs, char_h_frac=0.18)

DEPENDENCIES
------------
  Python 3.8+, Pillow (PIL). No NumPy required.
"""

__version__ = "1.1.0"
__author__ = "Rin Yamamoto"
__cycle__ = 40

import json
import math
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageChops

# Default path to the presets registry (same directory as this module)
_DEFAULT_PRESETS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "LTG_fill_light_presets.json"
)


# ── FillLightConfig ────────────────────────────────────────────────────────────

@dataclass
class FillLightConfig:
    """
    Configuration for a single character fill light effect.

    Attributes
    ----------
    cx : float
        Character horizontal center.
        If pos_mode="fractional" (default): 0.0–1.0 fraction of canvas width.
        If pos_mode="absolute": pixel x coordinate.
    cy : float
        Character vertical center.
        If pos_mode="fractional": 0.0–1.0 fraction of canvas height.
        If pos_mode="absolute": pixel y coordinate.
    color : tuple
        RGB fill light color, e.g. (255, 45, 107) for HOT_MAGENTA.
    alpha_max : int
        Maximum alpha for the fill gradient (0–255).
        Typical values: 30–45 for subtle fill, 50–80 for strong bounce light.
    source_dx : float
        Fill source offset in x as a fraction of char_h (character height).
        Positive = source to the right of character center.
        e.g. +0.5 → source 0.5×char_h to the right (upper-right storm crack).
    source_dy : float
        Fill source offset in y as a fraction of char_h.
        Negative = source ABOVE character center.
        e.g. -0.8 → source 0.8×char_h above the character.
    radius_scale : float
        Fill gradient radius as a multiple of char_h. Default 1.6.
    alpha_exponent : float
        Controls falloff shape: 1.0 = linear, 1.3 = slightly concentrated,
        2.0 = strongly peaked at source. Default 1.3.
    mask_threshold : int
        Grayscale threshold for character silhouette masking (0–255).
        Lower values capture more of the character area. Default 60.
    pos_mode : str
        "fractional" (default) — cx/cy are 0.0–1.0 fractions.
        "absolute"             — cx/cy are pixel values.
    label : str
        Optional label for debugging / reporting.
    """
    cx: float
    cy: float
    color: Tuple[int, int, int]
    alpha_max: int = 35
    source_dx: float = +0.5    # fill source: +0.5×char_h right of char center
    source_dy: float = -0.8    # fill source: -0.8×char_h above char center
    radius_scale: float = 1.6
    alpha_exponent: float = 1.3
    mask_threshold: int = 60
    pos_mode: str = "fractional"  # "fractional" or "absolute"
    label: str = ""


# ── FillLightAdapter ───────────────────────────────────────────────────────────

class FillLightAdapter:
    """
    Resolution-aware fill light adapter for PIL image generators.

    Automatically scales all radii, blur radii, and gradient parameters to
    match the canvas resolution. Accepts character positions as fractions
    (portable between 720p and 1080p generators) or as absolute pixels
    (for generators that already compute exact coords).

    Parameters
    ----------
    canvas_w : int
        Target canvas width in pixels.
    canvas_h : int
        Target canvas height in pixels.
    """

    def __init__(self, canvas_w: int, canvas_h: int):
        self.cw = canvas_w
        self.ch = canvas_h
        # Scale factor relative to 1280×720 baseline — used to scale blur radii
        self._scale = min(canvas_w / 1280.0, canvas_h / 720.0)

    def _resolve_coords(self, config: FillLightConfig, char_h: int) -> Tuple[int, int]:
        """Resolve cx/cy to absolute pixel coords from config."""
        if config.pos_mode == "fractional":
            cx = int(config.cx * self.cw)
            cy = int(config.cy * self.ch)
        else:
            cx = int(config.cx)
            cy = int(config.cy)
        return cx, cy

    def _make_silhouette_mask(self, img: Image.Image, char_cx: int, char_cy: int,
                               char_h: int, threshold: int) -> Image.Image:
        """
        Build a character silhouette mask at full canvas resolution.

        Crops a zone around (char_cx, char_cy), thresholds to isolate the
        character, dilates slightly, and returns a full-canvas "L" mask
        (255=character, 0=background).

        Blur radius scales with canvas size.
        """
        cw, ch = self.cw, self.ch
        zone_w = int(char_h * 2.0)
        zone_h = int(char_h * 2.5)
        x0 = max(0, char_cx - zone_w // 2)
        y0 = max(0, char_cy - zone_h // 2)
        x1 = min(cw, char_cx + zone_w // 2)
        y1 = min(ch, char_cy + zone_h)

        crop = img.crop((x0, y0, x1, y1))
        gray = crop.convert("L")
        mask_crop = gray.point(lambda p: 255 if p > threshold else 0, mode="L")

        full_mask = Image.new("L", (cw, ch), 0)
        full_mask.paste(mask_crop, (x0, y0))

        # Scale blur radius to canvas size — radius=4 at 1280px baseline
        blur_r = max(2, int(4 * self._scale))
        blurred = full_mask.filter(ImageFilter.GaussianBlur(radius=blur_r))
        dilated = blurred.point(lambda p: 255 if p > 30 else 0, mode="L")
        return dilated

    def _build_fill_overlay(self, config: FillLightConfig, char_cx: int,
                             char_cy: int, char_h: int) -> Image.Image:
        """
        Build a radial gradient fill light overlay (RGBA) for one character.

        The gradient source is positioned relative to the character center
        using source_dx and source_dy fractions of char_h.
        """
        overlay = Image.new("RGBA", (self.cw, self.ch), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)

        src_x = char_cx + int(config.source_dx * char_h)
        src_y = char_cy + int(config.source_dy * char_h)
        fill_r = int(char_h * config.radius_scale)

        step_size = max(1, fill_r // 30)
        for r_step in range(fill_r, 0, -step_size):
            t = 1.0 - (r_step / fill_r)
            a = int(config.alpha_max * (t ** config.alpha_exponent))
            a = max(0, min(255, a))
            if a < 2:
                continue
            od.ellipse(
                [src_x - r_step, src_y - r_step,
                 src_x + r_step, src_y + r_step],
                fill=(*config.color, a)
            )

        return overlay

    def apply_one(self, img: Image.Image, config: FillLightConfig,
                  char_h: int) -> Image.Image:
        """
        Apply a single fill light effect to the image.

        Parameters
        ----------
        img     : PIL.Image in RGB mode.
        config  : FillLightConfig describing this character's fill light.
        char_h  : Character height in pixels (absolute, already scaled to canvas).

        Returns
        -------
        PIL.Image: RGB image with fill light composited.
        """
        char_cx, char_cy = self._resolve_coords(config, char_h)

        # Build silhouette mask
        mask = self._make_silhouette_mask(
            img, char_cx, char_cy, char_h, config.mask_threshold
        )

        # Build gradient overlay
        overlay = self._build_fill_overlay(config, char_cx, char_cy, char_h)

        # Apply silhouette mask to overlay alpha
        r_ch, g_ch, b_ch, a_ch = overlay.split()
        masked_alpha = ImageChops.multiply(a_ch, mask)
        masked_overlay = Image.merge("RGBA", (r_ch, g_ch, b_ch, masked_alpha))

        # Composite onto image
        base_rgba = img.convert("RGBA")
        composited = Image.alpha_composite(base_rgba, masked_overlay)
        return composited.convert("RGB")

    def apply(self, img: Image.Image, configs: List[FillLightConfig],
              char_h_frac: float = 0.18) -> Image.Image:
        """
        Apply fill light effects for all configured characters.

        Parameters
        ----------
        img           : PIL.Image in RGB mode.
        configs       : List of FillLightConfig, one per character.
        char_h_frac   : Character height as a fraction of canvas height.
                        Default 0.18 (18% of canvas height — SF02 standard).
                        Used to derive char_h = int(canvas_h * char_h_frac).

        Returns
        -------
        PIL.Image: RGB image with all fill lights composited.
        """
        char_h = int(self.ch * char_h_frac)
        for config in configs:
            img = self.apply_one(img, config, char_h)
        return img


# ── Convenience factory functions ──────────────────────────────────────────────

def make_glitch_storm_fill_configs(
    luma_cx_frac: float = 0.45,
    byte_cx_frac: float = 0.28,
    cosmo_cx_frac: float = 0.62,
    luma_cy_frac: float = 0.65,
    byte_cy_frac: float = 0.60,
    cosmo_cy_frac: float = 0.65,
) -> List[FillLightConfig]:
    """
    Factory: return the standard 3-character HOT_MAGENTA fill light configs
    for the SF02 Glitch Storm scene.

    Source direction: upper-right (matching storm crack at ~94% x, ~2% y).
    source_dx=+0.5, source_dy=-0.8 → 0.5×char_h right, 0.8×char_h above.

    All positions are fractional — portable to any canvas resolution.
    """
    HOT_MAGENTA = (255, 45, 107)
    return [
        FillLightConfig(cx=luma_cx_frac,  cy=luma_cy_frac,  color=HOT_MAGENTA,
                        alpha_max=35, source_dx=+0.5, source_dy=-0.8, label="luma"),
        FillLightConfig(cx=byte_cx_frac,  cy=byte_cy_frac,  color=HOT_MAGENTA,
                        alpha_max=35, source_dx=+0.5, source_dy=-0.8, label="byte"),
        FillLightConfig(cx=cosmo_cx_frac, cy=cosmo_cy_frac, color=HOT_MAGENTA,
                        alpha_max=35, source_dx=+0.5, source_dy=-0.8, label="cosmo"),
    ]


def apply_fill_light(img: Image.Image, configs: List[FillLightConfig],
                     canvas_w: int, canvas_h: int,
                     char_h_frac: float = 0.18) -> Image.Image:
    """
    Standalone convenience function: create adapter and apply fill lights
    in one call.

    Parameters
    ----------
    img         : PIL.Image in RGB mode.
    configs     : List of FillLightConfig.
    canvas_w    : Canvas width in pixels.
    canvas_h    : Canvas height in pixels.
    char_h_frac : Character height fraction (default 0.18).

    Returns
    -------
    PIL.Image: RGB image with fill lights applied.
    """
    adapter = FillLightAdapter(canvas_w, canvas_h)
    return adapter.apply(img, configs, char_h_frac)


# ── Scene Presets Registry (v1.1.0) ───────────────────────────────────────────

# Hardcoded fallbacks used when the JSON registry is absent.
_HARDCODED_PRESETS = {
    "SF01": {
        "char_h_frac": 0.35,
        "lights": [
            dict(cx=0.29, cy=0.62, color=(212, 146, 58), alpha_max=30,
                 source_dx=-0.6, source_dy=-1.0, radius_scale=1.8,
                 alpha_exponent=1.5, mask_threshold=60, pos_mode="fractional",
                 label="luma_warm_lamp"),
            dict(cx=0.29, cy=0.62, color=(0, 212, 232), alpha_max=22,
                 source_dx=+0.8, source_dy=-0.2, radius_scale=1.4,
                 alpha_exponent=1.3, mask_threshold=60, pos_mode="fractional",
                 label="luma_crt_bounce"),
        ],
    },
    "SF02": {
        "char_h_frac": 0.18,
        "lights": [
            dict(cx=0.45, cy=0.65, color=(255, 45, 107), alpha_max=35,
                 source_dx=+0.5, source_dy=-0.8, radius_scale=1.6,
                 alpha_exponent=1.3, mask_threshold=60, pos_mode="fractional",
                 label="luma"),
            dict(cx=0.28, cy=0.60, color=(255, 45, 107), alpha_max=35,
                 source_dx=+0.5, source_dy=-0.8, radius_scale=1.6,
                 alpha_exponent=1.3, mask_threshold=60, pos_mode="fractional",
                 label="byte"),
            dict(cx=0.62, cy=0.65, color=(255, 45, 107), alpha_max=35,
                 source_dx=+0.5, source_dy=-0.8, radius_scale=1.6,
                 alpha_exponent=1.3, mask_threshold=60, pos_mode="fractional",
                 label="cosmo"),
        ],
    },
    "SF03": {
        "char_h_frac": 0.14,
        "lights": [
            dict(cx=0.38, cy=0.70, color=(123, 47, 190), alpha_max=28,
                 source_dx=0.0, source_dy=-1.2, radius_scale=1.5,
                 alpha_exponent=1.2, mask_threshold=50, pos_mode="fractional",
                 label="luma"),
            dict(cx=0.55, cy=0.68, color=(0, 240, 255), alpha_max=32,
                 source_dx=-0.3, source_dy=-0.5, radius_scale=1.4,
                 alpha_exponent=1.2, mask_threshold=50, pos_mode="fractional",
                 label="byte"),
        ],
    },
    "SF04": {
        "char_h_frac": 0.40,
        "lights": [
            dict(cx=0.35, cy=0.60, color=(0, 212, 232), alpha_max=25,
                 source_dx=+0.7, source_dy=-0.1, radius_scale=1.5,
                 alpha_exponent=1.4, mask_threshold=60, pos_mode="fractional",
                 label="luma_monitor_bounce"),
            dict(cx=0.68, cy=0.58, color=(0, 240, 255), alpha_max=30,
                 source_dx=0.0, source_dy=-0.3, radius_scale=1.3,
                 alpha_exponent=1.0, mask_threshold=55, pos_mode="fractional",
                 label="byte_self_glow"),
        ],
    },
}


def load_scene_configs(
    scene_name: str,
    presets_path: Optional[str] = None,
) -> Tuple[List[FillLightConfig], float]:
    """
    Load FillLightConfig list for a named scene from the JSON registry.
    Falls back to hardcoded defaults if the JSON file is absent or unreadable.

    Parameters
    ----------
    scene_name   : Scene key — one of "SF01", "SF02", "SF03", "SF04".
    presets_path : Optional path to LTG_fill_light_presets.json.
                   Defaults to the file alongside this module.

    Returns
    -------
    (configs, char_h_frac) :
        configs      — list of FillLightConfig, ready to pass to apply_fill_light()
        char_h_frac  — character height as fraction of canvas height for this scene

    Raises
    ------
    KeyError  : if scene_name is not found in either the JSON or hardcoded presets.
    """
    scene_name = scene_name.upper()
    path = presets_path or _DEFAULT_PRESETS_PATH

    scene_data = None

    # Try loading from JSON registry first
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                registry = json.load(f)
            if scene_name in registry:
                scene_data = registry[scene_name]
        except (json.JSONDecodeError, IOError) as exc:
            # Registry unreadable — fall through to hardcoded
            print(f"[fill_light_adapter] WARNING: Could not read presets JSON ({exc}). "
                  f"Falling back to hardcoded presets for {scene_name}.")

    # Fall back to hardcoded if JSON didn't yield data
    if scene_data is None:
        if scene_name not in _HARDCODED_PRESETS:
            raise KeyError(
                f"load_scene_configs: unknown scene '{scene_name}'. "
                f"Valid scenes: {sorted(_HARDCODED_PRESETS.keys())}"
            )
        scene_data = _HARDCODED_PRESETS[scene_name]
        print(f"[fill_light_adapter] INFO: Using hardcoded fallback presets for {scene_name}.")

    char_h_frac = float(scene_data.get("_char_h_frac", scene_data.get("char_h_frac", 0.18)))
    configs = []
    for entry in scene_data.get("lights", []):
        # Strip comment keys (prefixed with _)
        params = {k: v for k, v in entry.items() if not k.startswith("_")}
        # color comes as list from JSON — convert to tuple
        if isinstance(params.get("color"), list):
            params["color"] = tuple(params["color"])
        configs.append(FillLightConfig(**params))

    return configs, char_h_frac


# ── Self-test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    print("LTG_TOOL_fill_light_adapter.py v1.1.0 — Self-test")
    print("=" * 60)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "..", "output", "tools")
    out_dir = os.path.normpath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    # ── Test 1: Legacy factory (make_glitch_storm_fill_configs) ─────────────
    print("\nTest 1: Legacy factory + 720p/1080p resolution portability")
    for (cw, ch, res_label) in [(1280, 720, "720p"), (1920, 1080, "1080p")]:
        test_img = Image.new("RGB", (cw, ch), (15, 10, 25))
        td = ImageDraw.Draw(test_img)
        char_h = int(ch * 0.18)
        for cx_frac, cy_frac in [(0.45, 0.65), (0.28, 0.60), (0.62, 0.65)]:
            cx = int(cx_frac * cw)
            cy = int(cy_frac * ch)
            cw2, ch2 = int(char_h * 0.3), char_h
            td.rectangle([cx - cw2, cy - ch2 // 2, cx + cw2, cy + ch2 // 2],
                         fill=(200, 195, 180))
        configs = make_glitch_storm_fill_configs()
        result = apply_fill_light(test_img, configs, cw, ch, char_h_frac=0.18)
        result.thumbnail((1280, 1280), Image.LANCZOS)
        out_path = os.path.join(out_dir, f"test_fill_light_adapter_{res_label}.png")
        result.save(out_path)
        print(f"  [{res_label}] PASS — saved: {out_path}")

    # ── Test 2: load_scene_configs for all 4 scenes ──────────────────────────
    print("\nTest 2: load_scene_configs() — all scenes")
    all_pass = True
    for scene in ["SF01", "SF02", "SF03", "SF04"]:
        try:
            cfgs, frac = load_scene_configs(scene)
            print(f"  [{scene}] PASS — {len(cfgs)} light(s), char_h_frac={frac}")
        except Exception as exc:
            print(f"  [{scene}] FAIL — {exc}")
            all_pass = False

    # ── Test 3: Registry-based render for SF02 ───────────────────────────────
    print("\nTest 3: Registry-based render — SF02 at 1280×720")
    cw, ch = 1280, 720
    configs_sf02, char_h_frac_sf02 = load_scene_configs("SF02")
    test_img = Image.new("RGB", (cw, ch), (10, 8, 20))
    td = ImageDraw.Draw(test_img)
    char_h = int(ch * char_h_frac_sf02)
    for cfg in configs_sf02:
        cx = int(cfg.cx * cw)
        cy = int(cfg.cy * ch)
        cw2, ch2 = int(char_h * 0.3), char_h
        td.rectangle([cx - cw2, cy - ch2 // 2, cx + cw2, cy + ch2 // 2],
                     fill=(195, 190, 175))
    result_sf02 = apply_fill_light(test_img, configs_sf02, cw, ch,
                                   char_h_frac=char_h_frac_sf02)
    result_sf02.thumbnail((1280, 1280), Image.LANCZOS)
    sf02_path = os.path.join(out_dir, "test_fill_light_adapter_sf02_registry.png")
    result_sf02.save(sf02_path)
    print(f"  [SF02] PASS — registry render saved: {sf02_path}")

    print("\n" + ("SELF-TEST PASS" if all_pass else "SELF-TEST WARN (see above)"))
    print("Done.")
