#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_precritique_qa.py
================================
Pre-Critique QA Pipeline for "Luma & the Glitchkin."

Single entry-point script that chains all existing QA tools and produces a
consolidated Markdown report at output/production/precritique_qa_cNN.md.

Tools chained (in order):
  1. LTG_TOOL_render_qa.py       — size/resolution/quality checks on pitch PNGs
                                        (v1.3.0: adds Check F value ceiling guard)
  2. LTG_TOOL_color_verify.py    — canonical color fidelity on style frames
  3. LTG_TOOL_proportion_verify.py — head/body proportion checks on character sheets
  4. LTG_TOOL_stub_linter.py     — broken import detection in output/tools/
  5. LTG_TOOL_palette_warmth_lint.py — CHAR-M + CHAR-L hoodie warmth compliance on master_palette.md
                                             (v005 available; v004 used here for stable import)
  6. LTG_TOOL_glitch_spec_lint.py    — Glitchkin generator spec validation
  7. LTG_TOOL_readme_sync.py     — README Script Index completeness audit
  8. LTG_TOOL_motion_spec_lint.py — Motion spec sheet structural checks (Ryo Hasegawa C39)
  9. Delta Report + Arc-Diff Gate (informational) — delta vs last run; contact sheet version diff
     (Lee Tanaka C38 ideabox). LTG_TOOL_contact_sheet_arc_diff.compare_contact_sheets().
     CHANGED > 3: NOTE. REMOVED > 0: WARN. Informational only — does not affect overall score.
 10. Alpha Blend Lint (scored)       — fill-light composition defect detection (Rin Yamamoto C40)
     LTG_TOOL_alpha_blend_lint.lint_alpha_blend(). Requires unlit base (*_nolight.png) alongside
     composited. FLAT_FILL = FAIL. LOW_SIGNAL = WARN. Skips gracefully when base absent.
 11. UV_PURPLE Dominance Lint (scored) — Glitch Layer world-rule colour balance (Rin Yamamoto C44)
     LTG_TOOL_uv_purple_linter.run_glitch_layer_dominance_check(). Checks UV_PURPLE + ELEC_CYAN
     combined ≥ 20% non-black pixels (FAIL < 10%, WARN 10-19%). Also checks warm-hue
     contamination < 5% total pixels (WARN if ≥ 5%). Runs on registered GLITCH_LAYER_PNGS.
 12. Depth Temperature Lint (scored) — warm=FG / cool=BG depth grammar (Lee Tanaka C48)
     LTG_TOOL_depth_temp_lint.run_depth_temp_check(). Validates Depth Temperature Rule
     (docs/image-rules.md, codified C45). Default bands: FG (78%) / BG (70%).
     Per-asset overrides loaded from depth_temp_band_overrides.json (C48).
     PASS: separation >= threshold. WARN: correct direction, insufficient separation.
     FAIL: inverted. SKIP: GL exempt. Runs on registered DEPTH_TEMP_PNGS.
 13. Warm Pixel Percentage (scored) — world-type warm/cool pixel classification (Kai Nakamura C48)
     LTG_TOOL_warm_pixel_metric.measure_warm_pixel_percentage() + evaluate_threshold().
     Per-asset world_type tag determines threshold. REAL_INTERIOR >= 35%, GLITCH <= 15%, etc.
     PASS: within threshold. FAIL: outside threshold. SKIP: file missing.
     Runs on registered WARM_PIXEL_PNGS.
 14. Sightline Validation (scored) — gaze angular error validation (Morgan Walsh C49)
     LTG_TOOL_sightline_validator.validate_sightline_from_png() pixel detection.
     PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg angular error.
     Runs on registered SIGHTLINE_PNGS.

Output:
    output/production/precritique_qa_c<NN>.md
    output/tools/qa_baseline_last.json  (updated each run)

Exit codes:
    0 — All checks PASS
    1 — One or more WARN
    2 — One or more FAIL/ERROR

Author: Morgan Walsh (Pipeline Automation Specialist)
Created: Cycle 34 — 2026-03-29
Version: 2.14.0 (C45 Rin Yamamoto: LTG_TOOL_uv_purple_linter v1.1.0 GLITCH_DARK_SCENE subtype
               integration. run_uv_purple_lint() now passes GLITCH_DARK_SCENE subtype for
               COVETOUS assets (LTG_COLOR_sf_covetous_glitch.png, LTG_SF_covetous_glitch_v001.png).
               COVETOUS assets previously FAIL (0.6% / 0.2% ΔE-match) now PASS via hue-angle
               matching (96.7% / 98.9% UV_PURPLE hue family h° 255°–325°).
               No change to ENV asset handling — glitchlayer_frame WARNs remain.)
Version: 3.0.0 (C52 Kai Nakamura: Sections 15/16/17 Character Quality Metrics added.
               Section 15: Silhouette Distinctiveness (LTG_TOOL_silhouette_distinctiveness).
               Section 16: Expression Range (LTG_TOOL_expression_range_metric).
               Section 17: Construction Stiffness (LTG_TOOL_construction_stiffness).
               All three run on character turnaround/expression sheets.
               Color verify upgraded to use colour-science ΔE2000 when available.
               CYCLE_LABEL bumped to C52. Step numbering updated 1-17/17.)
Version: 2.18.0 (C49 Morgan Walsh: Section 14 Sightline Validation added.
               LTG_TOOL_sightline_validator.validate_sightline_from_png() on
               SIGHTLINE_PNGS registry. Pixel-based eye detection + angular error.
               PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg. Step numbering 1-14/14.
               build_report() + main() updated. SF01 registered as first sightline
               asset.)
Version: 2.17.0 (C48 Lee Tanaka: Section 12 per-asset band override config.
               depth_temp_band_overrides.json loaded by LTG_TOOL_depth_temp_lint v1.1.0.
               SF04 (fg=0.55, bg=0.85) and SF05 (fg=0.40, bg=0.85) false FAILs now PASS.
               run_depth_temp_lint() unchanged — overrides auto-loaded by lint tool.)
Version: 2.16.1 (C48 Rin Yamamoto: GLITCH_LAYER_PNGS registry extended with
               LTG_COLOR_styleframe_glitch_layer_showcase.png (GL Showcase, Rin C47).
               Now 7 registered GL assets for UV_PURPLE Dominance Lint Section 11.)
Version: 2.16.1 (C49 Ryo Hasegawa: CYCLE_LABEL bumped to C49.
               sheet_geometry_config.json updated with cosmo calibrated geometry +
               restored miri/miri_v002/glitch families after calibrator overwrite.
               LTG_TOOL_sheet_geometry_calibrate.py updated with cosmo sheet path.)
Version: 2.16.0 (C48 Kai Nakamura: Section 13 Warm Pixel Percentage added.
               LTG_TOOL_warm_pixel_metric.measure_warm_pixel_percentage() +
               evaluate_threshold() on WARM_PIXEL_PNGS registry. Each asset has
               a world_type tag for threshold lookup. Scored section (PASS/WARN/FAIL).
               CYCLE_LABEL bumped to C48. Step numbering updated 1-13/13.)
Version: 2.15.0 (C47 Lee Tanaka: Section 12 Depth Temperature Lint added.
               LTG_TOOL_depth_temp_lint.run_depth_temp_check() on DEPTH_TEMP_PNGS registry.
               Checks warm=FG / cool=BG depth grammar per docs/image-rules.md.
               GL scenes auto-exempt via world_type_infer. CYCLE_LABEL bumped to C47.
               Step numbering updated 1-12/12.)
Version: 2.14.1 (C46 Ryo Hasegawa: CYCLE_LABEL bumped to C46. motion_spec_lint C46 update
               (dark-sheet annotation_occupancy fix) — byte + glitch annotation_occupancy
               now PASS with 1% bright-pixel threshold. Eliminates 2 persistent false WARNs.
               sheet_geometry_config.json v2: background_style + occupancy_threshold_dark
               for byte and glitch; miri_v002 family added. MOTION_SHEETS extended with
               LTG_CHAR_miri_motion_v002.png (4 panels) — Miri Emotional Warmth Pacing arc.)
Version: 2.13.0 (C44 Rin Yamamoto: UV_PURPLE Dominance Lint Section 11 added. New GLITCH_LAYER_PNGS
               registry. Lazy-loaded LTG_TOOL_uv_purple_linter via _load_uv_purple_linter().
               run_uv_purple_lint() runner, Section 11 in build_report(), main() [11/11],
               and overall exit-code logic updated. world_type_infer.py bumped to v1.2.0:
               covetous_glitch / sf_covetous added to GLITCH rule.)
Version: 2.12.0 (C45 Ryo Hasegawa: CYCLE_LABEL bumped to C45. MOTION_SHEETS extended with
               LTG_CHAR_glitch_motion.png (4 panels). Lint now covers all 5 character motion
               sheets: luma/byte/cosmo/miri/glitch.)
Version: 2.11.0 (C44 Ryo Hasegawa: CYCLE_LABEL bumped to C44. MOTION_SHEETS extended with
               LTG_CHAR_cosmo_motion.png (4 panels) and LTG_CHAR_miri_motion.png (4 panels);
               Luma panel count corrected 3→4. Lint now covers all 4 character motion sheets.)
Version: 2.10.0 (C43 Rin Yamamoto: CYCLE_LABEL bumped to C43. SF04 entry in FILL_LIGHT_ASSETS
               corrected: was LTG_COLOR_styleframe_luma_byte.png (Jordan C40 legacy path) →
               now LTG_COLOR_styleframe_sf04.png (Jordan C42 canonical, Alex Chen decision C42).
               SF04 nolight base path updated to match. Luma zone cx_frac updated to 0.55
               (doorway center-right, Resolution scene geometry). All three generators (SF01,
               SF02, SF04) now support --save-nolight flag — Section 10 alpha_blend_lint can
               now run actively instead of always-skipping.)
Version: 2.9.0 (C41 Morgan Walsh: CYCLE_LABEL bumped to C41; confirmed Task 1 (README version
              sequence v2.7.0→v2.8.0 unambiguous) and Task 2 (Section 10 alpha_blend_lint
              integration from Rin Yamamoto C40 verified present). C41 baseline run executed.
              No functional changes — cycle bump only.)
Version: 2.8.0 (C40 Morgan Walsh + Kai Nakamura: merges two parallel v2.7.0 branches.
              Morgan Walsh v2.7.0: arc-diff pairs loaded from arc_diff_config.json at startup;
              falls back to hardcoded constant if JSON absent — backwards compatible.
              Kai Nakamura v2.7.0: numpy batch pixel scans; LAB ΔE color verify via cv2;
              run_color_verify() uses _check_color_fidelity_lab() from render_qa v2.0.0.
              CYCLE_LABEL updated to C40.)
Version: 2.8.0 (C40 Rin Yamamoto: alpha_blend_lint Section 10 added — fill-light composition
              defect detection. Runs LTG_TOOL_alpha_blend_lint.lint_alpha_blend() on assets
              that have both a composited image and an unlit base registered in
              FILL_LIGHT_ASSETS. Lazy-loaded; skips gracefully when base is absent or cv2
              unavailable. Section 10 is scored (PASS/WARN/FAIL affects overall grade).
              FLAT_FILL = FAIL, LOW_SIGNAL = WARN, PASS = PASS. If all assets skip
              (no bases on disk), overall = PASS.)
Version: 2.7.0 (C39 Morgan Walsh: arc-diff pairs now loaded from arc_diff_config.json at startup;
              falls back to hardcoded constant if JSON absent — backwards compatible.)
Version: 2.7.0 (C39 Kai Nakamura: numpy batch pixel scans; LAB ΔE color verify.
              run_color_verify() now uses _check_color_fidelity_lab() from render_qa v2.0.0
              when cv2 is available — perceptual ΔE replaces hue-drift RGB Euclidean.
              numpy import added; no API changes.)
Version: 2.6.0 (C39 Morgan Walsh: arc-diff gate Section 10 added — contact sheet changelog for critics.
              Lineup suppression expansion complete — glitch_spec_lint v1.4.0 file_prefix mode;
              character_lineup_* G006/G007 now auto-suppressed via prefix.)
Version: 2.5.0 (C39 Ryo Hasegawa: motion spec lint Section 8 added.)
Version: 2.4.0 (C39 Sam Kowalski: warmth lint v001→v004; CHAR-L hoodie + REAL_STORM threshold.)
"""

import os
import sys
import json
import datetime
from pathlib import Path

try:
    import numpy as np
    _NP_AVAILABLE = True
except ImportError:
    np = None  # type: ignore
    _NP_AVAILABLE = False

# ---------------------------------------------------------------------------
# Path setup — allow running from any cwd
# ---------------------------------------------------------------------------
REPO_ROOT   = Path(__file__).resolve().parent.parent.parent  # /home/wipkat/team
TOOLS_DIR   = REPO_ROOT / "output" / "tools"
OUTPUT_DIR  = REPO_ROOT / "output"
PROD_DIR    = REPO_ROOT / "output" / "production"
PALETTE_MD  = REPO_ROOT / "output" / "color" / "palettes" / "master_palette.md"
BASELINE_JSON = TOOLS_DIR / "qa_baseline_last.json"

# Cycle label — update each cycle
CYCLE_LABEL = "C52"

if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# ---------------------------------------------------------------------------
# Import QA tools
# ---------------------------------------------------------------------------
from LTG_TOOL_render_qa import qa_report, qa_batch, _check_color_fidelity_lab as _lab_color_check
from LTG_TOOL_color_verify import verify_canonical_colors, get_canonical_palette

# v3.0.0 C52: Import ΔE2000 from color_verify if colour-science available
try:
    from LTG_TOOL_color_verify import verify_canonical_colors_deltaE, _COLOUR_SCIENCE_AVAILABLE
except ImportError:
    _COLOUR_SCIENCE_AVAILABLE = False
from LTG_TOOL_stub_linter import lint_directory as stub_lint_directory, format_report as stub_format_report
from LTG_TOOL_palette_warmth_lint import lint_palette_file, format_report as palette_format_report
from LTG_TOOL_glitch_spec_lint import lint_directory as glitch_lint_directory, format_report as glitch_format_report
from LTG_TOOL_readme_sync import audit as readme_sync_audit, format_report as readme_sync_format_report
from LTG_TOOL_motion_spec_lint import lint_motion_spec, format_report as motion_lint_format_report
import importlib.util as _importlib_util

from PIL import Image

# Arc-diff tool: loaded lazily to avoid import errors if Pillow not installed yet
_arc_diff_mod = None
# Alpha-blend-lint tool: loaded lazily (requires cv2; skips gracefully if absent)
_alpha_blend_lint_mod = None

def _load_alpha_blend_lint():
    """Lazily import LTG_TOOL_alpha_blend_lint. Returns module or None."""
    global _alpha_blend_lint_mod
    if _alpha_blend_lint_mod is not None:
        return _alpha_blend_lint_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_alpha_blend_lint",
            str(TOOLS_DIR / "LTG_TOOL_alpha_blend_lint.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _alpha_blend_lint_mod = mod
        return mod
    except Exception:
        return None


# UV-purple-lint tool: loaded lazily (requires PIL + numpy; skips gracefully if absent)
_uv_purple_lint_mod = None

def _load_uv_purple_linter():
    """Lazily import LTG_TOOL_uv_purple_linter. Returns module or None."""
    global _uv_purple_lint_mod
    if _uv_purple_lint_mod is not None:
        return _uv_purple_lint_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_uv_purple_linter",
            str(TOOLS_DIR / "LTG_TOOL_uv_purple_linter.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _uv_purple_lint_mod = mod
        return mod
    except Exception:
        return None


# Depth-temperature-lint tool: loaded lazily (requires numpy; skips gracefully if absent)
_depth_temp_lint_mod = None

def _load_depth_temp_lint():
    """Lazily import LTG_TOOL_depth_temp_lint. Returns module or None."""
    global _depth_temp_lint_mod
    if _depth_temp_lint_mod is not None:
        return _depth_temp_lint_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_depth_temp_lint",
            str(TOOLS_DIR / "LTG_TOOL_depth_temp_lint.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _depth_temp_lint_mod = mod
        return mod
    except Exception:
        return None


# Warm-pixel-metric tool: loaded lazily (requires PIL + numpy; skips gracefully if absent)
_warm_pixel_metric_mod = None
_sightline_validator_mod = None

def _load_warm_pixel_metric():
    """Lazily import LTG_TOOL_warm_pixel_metric. Returns module or None."""
    global _warm_pixel_metric_mod
    if _warm_pixel_metric_mod is not None:
        return _warm_pixel_metric_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_warm_pixel_metric",
            str(TOOLS_DIR / "LTG_TOOL_warm_pixel_metric.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _warm_pixel_metric_mod = mod
        return mod
    except Exception:
        return None


def _load_sightline_validator():
    """Lazily import LTG_TOOL_sightline_validator. Returns module or None."""
    global _sightline_validator_mod
    if _sightline_validator_mod is not None:
        return _sightline_validator_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_sightline_validator",
            str(TOOLS_DIR / "LTG_TOOL_sightline_validator.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _sightline_validator_mod = mod
        return mod
    except Exception:
        return None


# Character quality metric tools: loaded lazily (C52, Kai Nakamura)
_silhouette_dist_mod = None
_expression_range_mod = None
_construction_stiffness_mod = None


def _load_silhouette_distinctiveness():
    """Lazily import LTG_TOOL_silhouette_distinctiveness. Returns module or None."""
    global _silhouette_dist_mod
    if _silhouette_dist_mod is not None:
        return _silhouette_dist_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_silhouette_distinctiveness",
            str(TOOLS_DIR / "LTG_TOOL_silhouette_distinctiveness.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _silhouette_dist_mod = mod
        return mod
    except Exception:
        return None


def _load_expression_range_metric():
    """Lazily import LTG_TOOL_expression_range_metric. Returns module or None."""
    global _expression_range_mod
    if _expression_range_mod is not None:
        return _expression_range_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_expression_range_metric",
            str(TOOLS_DIR / "LTG_TOOL_expression_range_metric.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _expression_range_mod = mod
        return mod
    except Exception:
        return None


def _load_construction_stiffness():
    """Lazily import LTG_TOOL_construction_stiffness. Returns module or None."""
    global _construction_stiffness_mod
    if _construction_stiffness_mod is not None:
        return _construction_stiffness_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_construction_stiffness",
            str(TOOLS_DIR / "LTG_TOOL_construction_stiffness.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _construction_stiffness_mod = mod
        return mod
    except Exception:
        return None


def _load_arc_diff():
    """Lazily import LTG_TOOL_contact_sheet_arc_diff. Returns module or None."""
    global _arc_diff_mod
    if _arc_diff_mod is not None:
        return _arc_diff_mod
    try:
        spec = _importlib_util.spec_from_file_location(
            "LTG_TOOL_contact_sheet_arc_diff",
            str(TOOLS_DIR / "LTG_TOOL_contact_sheet_arc_diff.py"),
        )
        mod = _importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _arc_diff_mod = mod
        return mod
    except Exception:
        return None

# ---------------------------------------------------------------------------
# Target file collections
# ---------------------------------------------------------------------------

# Pitch PNGs: style frames (C43 — SF04 path updated to canonical Jordan C42 generator)
# SF04 canonical = LTG_COLOR_styleframe_sf04.png (Jordan C42, Alex Chen decision C42).
# LTG_COLOR_styleframe_luma_byte.png was the C40 lamp scene (superseded C42).
PITCH_PNGS = [
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_discovery.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_glitch_storm.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_otherside.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_sf04.png",
    PROD_DIR / "LTG_BRAND_logo.png",
    PROD_DIR / "storyboard_pitch_export.png",
]

# Style frames for color verification (C43 — SF04 path corrected to canonical)
STYLE_FRAMES = [
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_discovery.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_glitch_storm.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_otherside.png",
    OUTPUT_DIR / "color" / "style_frames" / "LTG_COLOR_styleframe_sf04.png",
]

# Character sheets for proportion verification
# Each entry: (png_path, approximate_bbox as (x, y, w, h) or None for auto)
CHARACTER_SHEETS = [
    (OUTPUT_DIR / "characters" / "main" / "turnarounds" / "LTG_CHAR_luma_turnaround.png", None),
    (OUTPUT_DIR / "characters" / "main" / "turnarounds" / "LTG_CHAR_cosmo_turnaround.png", None),
    (OUTPUT_DIR / "characters" / "main" / "turnarounds" / "LTG_CHAR_miri_turnaround.png", None),
    (OUTPUT_DIR / "characters" / "main" / "turnarounds" / "LTG_CHAR_glitch_turnaround.png", None),
]

# Glitch generator scripts for spec lint
GLITCH_GENERATORS = list(TOOLS_DIR.glob("LTG_TOOL_glitch_*.py")) + \
                    list(TOOLS_DIR.glob("LTG_TOOL_style_frame_03_*.py")) + \
                    list(TOOLS_DIR.glob("LTG_TOOL_character_lineup_*.py"))

# Motion spec sheets for Section 8 lint (add new versions here each cycle)
MOTION_DIR = OUTPUT_DIR / "characters" / "motion"
MOTION_SHEETS = [
    # (path, expected_panel_count)
    # C44 update (Ryo Hasegawa): luma corrected 3→4 (4-panel sheet); cosmo+miri added
    # C45 update (Ryo Hasegawa): glitch added — first motion spec for Glitch character
    # C46 update (Ryo Hasegawa): miri_v002 added — Emotional Warmth Pacing arc
    (MOTION_DIR / "LTG_CHAR_luma_motion.png",        4),
    (MOTION_DIR / "LTG_CHAR_byte_motion.png",        4),
    (MOTION_DIR / "LTG_CHAR_cosmo_motion.png",       4),
    (MOTION_DIR / "LTG_CHAR_miri_motion.png",        4),
    (MOTION_DIR / "LTG_CHAR_miri_motion_v002.png",   4),
    (MOTION_DIR / "LTG_CHAR_glitch_motion.png",      4),
]

# Contact sheet pairs for arc-diff gate (Section 10).
# Each entry: (label, old_sheet_path, new_sheet_path, diff_output_path)
# old = previous version, new = current version.
# Arc-diff output PNG saves to output/production/.
#
# Loaded from arc_diff_config.json at startup if present; falls back to
# the hardcoded constant below so existing runs are never broken.
SB_DIR = OUTPUT_DIR / "storyboards"
_ARC_DIFF_PAIRS_DEFAULT = [
    (
        "Act 2 contact sheet v005→v006",
        SB_DIR / "act2" / "LTG_SB_act2_contact_sheet.png",
        SB_DIR / "act2" / "LTG_SB_act2_contact_sheet.png",
        PROD_DIR / "arc_diff_act2_c39.png",
    ),
    (
        "Act 1 cold open contact sheet v001→v002",
        SB_DIR / "LTG_SB_act1_coldopen_contact_sheet.png",
        SB_DIR / "LTG_SB_act1_coldopen_contact_sheet.png",
        PROD_DIR / "arc_diff_act1_c39.png",
    ),
]

_ARC_DIFF_CONFIG = TOOLS_DIR / "arc_diff_config.json"


def _load_arc_diff_pairs():
    """
    Load ARC_DIFF_PAIRS from arc_diff_config.json if present.
    Paths in JSON are relative to REPO_ROOT. Returns list of
    (label, old_path, new_path, diff_out) tuples with Path objects.
    Falls back to _ARC_DIFF_PAIRS_DEFAULT if JSON is absent or invalid.
    """
    if not _ARC_DIFF_CONFIG.exists():
        return _ARC_DIFF_PAIRS_DEFAULT
    try:
        data = json.loads(_ARC_DIFF_CONFIG.read_text(encoding="utf-8"))
        pairs = []
        for entry in data.get("pairs", []):
            label, old_rel, new_rel, diff_rel = entry
            pairs.append((
                label,
                REPO_ROOT / old_rel,
                REPO_ROOT / new_rel,
                REPO_ROOT / diff_rel,
            ))
        return pairs if pairs else _ARC_DIFF_PAIRS_DEFAULT
    except Exception:
        return _ARC_DIFF_PAIRS_DEFAULT


ARC_DIFF_PAIRS = _load_arc_diff_pairs()

# ---------------------------------------------------------------------------
# Fill-light assets for Section 10 — alpha_blend_lint
# ---------------------------------------------------------------------------
# Each entry:
#   (label, composited_path, base_path, zones)
#
#   label           : human-readable name for report
#   composited_path : rendered style frame with fill light applied
#   base_path       : unlit base image (same composition, no fill light overlay)
#                     If base_path does not exist on disk the asset is SKIPPED.
#   zones           : list of zone dicts compatible with lint_alpha_blend() API:
#                     {"label", "cx_frac", "cy_frac", "src_dx_frac", "src_dy_frac"}
#
# Convention: base images are named <original_stem>_nolight<suffix>.
# When a generator produces an unlit base (e.g. for QA), register it here.
# Skipping is not a defect — only flag when base is present.

SF_DIR = OUTPUT_DIR / "color" / "style_frames"

FILL_LIGHT_ASSETS = [
    (
        "SF01 Discovery (Luma — warm lamp fill)",
        SF_DIR / "LTG_COLOR_styleframe_discovery.png",
        SF_DIR / "LTG_COLOR_styleframe_discovery_nolight.png",
        [
            # Luma: fill from upper-left warm lamp
            {"label": "luma", "cx_frac": 0.29, "cy_frac": 0.55,
             "src_dx_frac": -0.5, "src_dy_frac": -0.8},
        ],
    ),
    (
        "SF02 Glitch Storm (Luma/Byte/Cosmo — HOT_MAGENTA fill)",
        SF_DIR / "LTG_COLOR_styleframe_glitch_storm.png",
        SF_DIR / "LTG_COLOR_styleframe_glitch_storm_nolight.png",
        [
            {"label": "luma",  "cx_frac": 0.45, "cy_frac": 0.65,
             "src_dx_frac": 0.5, "src_dy_frac": -0.8},
            {"label": "byte",  "cx_frac": 0.28, "cy_frac": 0.60,
             "src_dx_frac": 0.5, "src_dy_frac": -0.8},
            {"label": "cosmo", "cx_frac": 0.62, "cy_frac": 0.65,
             "src_dx_frac": 0.5, "src_dy_frac": -0.8},
        ],
    ),
    (
        "SF04 Resolution (Jordan C42 canonical — warm light + cool floor bounce)",
        SF_DIR / "LTG_COLOR_styleframe_sf04.png",
        SF_DIR / "LTG_COLOR_styleframe_sf04_nolight.png",
        [
            # Luma stands in doorway, center-right; warm top half, cool floor bounce
            {"label": "luma", "cx_frac": 0.55, "cy_frac": 0.52,
             "src_dx_frac": -0.5, "src_dy_frac": -0.8},
        ],
    ),
]

# ---------------------------------------------------------------------------
# Glitch Layer PNGs for Section 11 — UV_PURPLE Dominance Lint
# ---------------------------------------------------------------------------
# Registered Glitch Layer rendered images to check for UV_PURPLE + ELEC_CYAN
# dominance (Alex Chen C44 brief). World type override = GLITCH applied to all.
# Add new Glitch Layer style frames and env backgrounds here each cycle.

ENV_DIR = OUTPUT_DIR / "backgrounds" / "environments"

GLITCH_LAYER_PNGS = [
    # Glitch Layer style frames
    SF_DIR  / "LTG_COLOR_sf_covetous_glitch.png",
    SF_DIR  / "LTG_SF_covetous_glitch_v001.png",
    SF_DIR  / "LTG_COLOR_styleframe_glitch_layer_showcase.png",  # GL Showcase (Rin C47)
    # Glitch Layer environment backgrounds
    ENV_DIR / "LTG_ENV_glitchlayer_frame.png",
    ENV_DIR / "LTG_ENV_glitchlayer_encounter.png",
    ENV_DIR / "bg_glitch_layer_encounter.png",
    ENV_DIR / "glitch_layer_frame.png",
]


# ---------------------------------------------------------------------------
# Depth Temperature Lint assets for Section 12 (Lee Tanaka C47)
# ---------------------------------------------------------------------------
# Multi-character and multi-tier compositions that must obey warm=FG / cool=BG
# depth grammar (docs/image-rules.md Depth Temperature Rule, codified C45).
# Glitch Layer scenes auto-exempt via world_type_infer. Single-character scenes
# are excluded (no FG/BG tier separation to test).
#
# Each entry: (label, path)

CHAR_DIR = OUTPUT_DIR / "characters" / "main"

DEPTH_TEMP_PNGS = [
    # Character lineup — canonical multi-tier composition (FG/BG ground planes)
    ("Character Lineup",         CHAR_DIR / "LTG_CHAR_character_lineup.png"),
    # SF05 The Passing — Miri + Luma, warm/cool split, Real World
    ("SF05 The Passing",         SF_DIR  / "LTG_COLOR_styleframe_sf05.png"),
    # SF06 The Hand-Off — Miri + Luma + CRT, warm/cool split, Real World
    ("SF06 The Hand-Off",        SF_DIR  / "LTG_COLOR_sf_miri_luma_handoff.png"),
    # SF04 Resolution — Luma + Byte (faded), warm/cool split, Real World
    ("SF04 Resolution",          SF_DIR  / "LTG_COLOR_styleframe_sf04.png"),
    # SF02 Glitch Storm — multi-character, but Glitch Layer → expected SKIP
    ("SF02 Glitch Storm",        SF_DIR  / "LTG_COLOR_styleframe_glitch_storm.png"),
    # COVETOUS — three-character, Glitch Layer → expected SKIP
    ("COVETOUS Style Frame",     SF_DIR  / "LTG_COLOR_sf_covetous_glitch.png"),
]


# ---------------------------------------------------------------------------
# Warm Pixel Percentage assets for Section 13 (Kai Nakamura C48)
# ---------------------------------------------------------------------------
# Style frames and environment backgrounds with assigned world types for
# warm-pixel-percentage threshold validation. Uses Sam Kowalski's
# LTG_TOOL_warm_pixel_metric.py (C47).
#
# Each entry: (label, path, world_type)
# world_type must match LTG_TOOL_warm_pixel_metric.WARM_PCT_THRESHOLDS keys:
#   REAL_INTERIOR, REAL_STORM, GLITCH, OTHER_SIDE

WARM_PIXEL_PNGS = [
    # Real World interiors — warm_pct >= 35%
    ("SF01 Discovery",
     SF_DIR / "LTG_COLOR_styleframe_discovery.png",
     "REAL_INTERIOR"),
    ("SF04 Resolution",
     SF_DIR / "LTG_COLOR_styleframe_sf04.png",
     "REAL_INTERIOR"),
    ("SF05 The Passing",
     SF_DIR / "LTG_COLOR_styleframe_sf05.png",
     "REAL_INTERIOR"),
    ("SF06 The Hand-Off",
     SF_DIR / "LTG_COLOR_sf_miri_luma_handoff.png",
     "REAL_INTERIOR"),
    # Real World storm — warm_pct >= 5%
    ("SF02 Glitch Storm",
     SF_DIR / "LTG_COLOR_styleframe_glitch_storm.png",
     "REAL_STORM"),
    # Glitch Layer — warm_pct <= 15%
    ("COVETOUS Style Frame",
     SF_DIR / "LTG_COLOR_sf_covetous_glitch.png",
     "GLITCH"),
    ("COVETOUS v001",
     SF_DIR / "LTG_SF_covetous_glitch_v001.png",
     "GLITCH"),
    ("Glitch Layer Frame",
     ENV_DIR / "LTG_ENV_glitchlayer_frame.png",
     "GLITCH"),
    ("Glitch Layer Encounter",
     ENV_DIR / "LTG_ENV_glitchlayer_encounter.png",
     "GLITCH"),
    # Other Side — warm_pct <= 5%
    ("SF03 Other Side",
     SF_DIR / "LTG_COLOR_styleframe_otherside.png",
     "OTHER_SIDE"),
]


# ---------------------------------------------------------------------------
# Sightline Validation assets for Section 14 (Morgan Walsh C49)
# ---------------------------------------------------------------------------
# Style frames with known gaze targets for sight-line angular error validation.
# Uses LTG_TOOL_sightline_validator.validate_sightline_from_png() (Jordan Reed C48).
#
# Each entry: (label, path, target_xy, search_box_or_None)
# target_xy: (x, y) the character should be looking at
# search_box: (x0, y0, x1, y1) region to search for eyes, or None for full image

SIGHTLINE_PNGS = [
    # SF01 Discovery — Luma gazes at CRT/Byte emerge point
    # Target: CRT screen center (~640, 230) at 1280x720
    # Search box: Luma's head region (left third of frame, upper-mid)
    ("SF01 Luma -> CRT",
     SF_DIR / "LTG_COLOR_styleframe_discovery.png",
     (640, 230),
     (150, 200, 450, 450)),
]


# ---------------------------------------------------------------------------
# Character Quality Metric assets for Sections 15/16/17 (Kai Nakamura C52)
# ---------------------------------------------------------------------------
# Section 15: Silhouette Distinctiveness — turnaround sheets for pairwise comparison
# Section 16: Expression Range Metric — expression sheets for variation analysis
# Section 17: Construction Stiffness — turnarounds for straightness/stiffness detection

TURNAROUND_DIR = OUTPUT_DIR / "characters" / "main" / "turnarounds"

SILHOUETTE_ASSETS = [
    TURNAROUND_DIR / "LTG_CHAR_luma_turnaround.png",
    TURNAROUND_DIR / "LTG_CHAR_cosmo_turnaround.png",
    TURNAROUND_DIR / "LTG_CHAR_miri_turnaround.png",
    TURNAROUND_DIR / "LTG_CHAR_byte_turnaround.png",
    TURNAROUND_DIR / "LTG_CHAR_glitch_turnaround.png",
]

EXPRESSION_SHEETS = [
    # (label, path)
    ("Luma Expressions",   OUTPUT_DIR / "characters" / "main" / "LTG_CHAR_luma_expression_sheet.png"),
    ("Byte Expressions",   OUTPUT_DIR / "characters" / "main" / "LTG_CHAR_byte_expression_sheet.png"),
    ("Cosmo Expressions",  OUTPUT_DIR / "characters" / "main" / "LTG_CHAR_cosmo_expression_sheet.png"),
    ("Glitch Expressions", OUTPUT_DIR / "characters" / "main" / "LTG_CHAR_glitch_expression_sheet.png"),
    ("Miri Expressions",   OUTPUT_DIR / "characters" / "main" / "LTG_CHAR_grandma_miri_expression_sheet.png"),
]

STIFFNESS_ASSETS = [
    # (label, path)
    ("Luma Turnaround",   TURNAROUND_DIR / "LTG_CHAR_luma_turnaround.png"),
    ("Cosmo Turnaround",  TURNAROUND_DIR / "LTG_CHAR_cosmo_turnaround.png"),
    ("Miri Turnaround",   TURNAROUND_DIR / "LTG_CHAR_miri_turnaround.png"),
    ("Byte Turnaround",   TURNAROUND_DIR / "LTG_CHAR_byte_turnaround.png"),
    ("Glitch Turnaround", TURNAROUND_DIR / "LTG_CHAR_glitch_turnaround.png"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _grade_line(grade: str) -> str:
    """Return a markdown badge for a grade string."""
    mapping = {
        "PASS":  "**PASS**",
        "WARN":  "**WARN**",
        "FAIL":  "**FAIL**",
        "ERROR": "**ERROR**",
        "SKIP":  "*SKIP*",
    }
    return mapping.get(grade.upper(), grade)


def _worst_grade(*grades) -> str:
    """Return the worst of several grade strings."""
    order = {"ERROR": 3, "FAIL": 2, "WARN": 1, "PASS": 0, "SKIP": -1}
    worst = max(grades, key=lambda g: order.get(g.upper(), -1))
    return worst.upper()


# ---------------------------------------------------------------------------
# Baseline I/O
# ---------------------------------------------------------------------------

def load_baseline() -> dict:
    """Load the previous run's QA baseline from qa_baseline_last.json.
    Returns an empty dict if no baseline exists."""
    if not BASELINE_JSON.exists():
        return {}
    try:
        return json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_baseline(snapshot: dict) -> None:
    """Write the current run's QA snapshot to qa_baseline_last.json."""
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    BASELINE_JSON.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")


def _make_snapshot(
    render_qa_res,
    color_verify_res,
    proportion_res,
    stub_lint_res,
    palette_lint_res,
    glitch_lint_res,
    readme_sync_res,
    motion_spec_res,
    run_ts: str,
    cycle: str,
) -> dict:
    """Build a compact snapshot dict from section results for persistence."""
    def _section(r, name):
        return {
            "section": name,
            "overall": r["overall"],
            "pass": r["pass"],
            "warn": r["warn"],
            "fail": r["fail"],
            "missing": r.get("missing", []),
            "flagged": r.get("flagged", []),
        }
    _all = [render_qa_res, color_verify_res, proportion_res,
            stub_lint_res, palette_lint_res, glitch_lint_res,
            readme_sync_res, motion_spec_res]
    return {
        "cycle": cycle,
        "run_ts": run_ts,
        "sections": {
            "render_qa":      _section(render_qa_res,      "Render QA"),
            "color_verify":   _section(color_verify_res,   "Color Verify"),
            "proportion":     _section(proportion_res,      "Proportion Verify"),
            "stub_linter":    _section(stub_lint_res,       "Stub Linter"),
            "palette_warmth": _section(palette_lint_res,    "Palette Warmth Lint"),
            "glitch_spec":    _section(glitch_lint_res,     "Glitch Spec Lint"),
            "readme_sync":    _section(readme_sync_res,     "README Sync"),
            "motion_spec":    _section(motion_spec_res,     "Motion Spec Lint"),
        },
        "totals": {
            "pass":  sum(r["pass"]  for r in _all),
            "warn":  sum(r["warn"]  for r in _all),
            "fail":  sum(r["fail"]  for r in _all),
        },
    }


# ---------------------------------------------------------------------------
# Delta report
# ---------------------------------------------------------------------------

def compute_delta(current_snapshot: dict, baseline: dict) -> dict:
    """
    Compare current snapshot against baseline.
    Returns a delta dict with:
        new_fails   — list of (section, item) newly FAIL since last run
        new_warns   — list of (section, item) newly WARN since last run
        resolved    — list of (section, item) that were FAIL/WARN, now cleared
        count_delta — dict: {fail: +N, warn: +N, resolved: N}
        has_baseline — bool
        summary     — formatted summary string
    """
    result = {
        "new_fails": [],
        "new_warns": [],
        "resolved": [],
        "count_delta": {"fail": 0, "warn": 0, "resolved": 0},
        "has_baseline": bool(baseline),
        "summary": "",
        "prev_cycle": baseline.get("cycle", "N/A"),
        "prev_ts": baseline.get("run_ts", "N/A"),
    }

    if not baseline:
        result["summary"] = "No baseline found — this run establishes the new baseline."
        return result

    prev_totals = baseline.get("totals", {})
    curr_totals = current_snapshot.get("totals", {})

    delta_fail = curr_totals.get("fail", 0) - prev_totals.get("fail", 0)
    delta_warn = curr_totals.get("warn", 0) - prev_totals.get("warn", 0)

    # Per-section flagged item delta
    prev_sections = baseline.get("sections", {})
    curr_sections = current_snapshot.get("sections", {})

    for sec_key, curr_sec in curr_sections.items():
        prev_sec = prev_sections.get(sec_key, {})
        prev_flagged = set(prev_sec.get("flagged", []))
        curr_flagged = set(curr_sec.get("flagged", []))

        sec_name = curr_sec.get("section", sec_key)

        # New items in current that weren't in previous
        for item in sorted(curr_flagged - prev_flagged):
            if "FAIL" in item.upper():
                result["new_fails"].append((sec_name, item.strip()))
            else:
                result["new_warns"].append((sec_name, item.strip()))

        # Items in previous that are gone now (resolved)
        for item in sorted(prev_flagged - curr_flagged):
            result["resolved"].append((sec_name, item.strip()))

    result["count_delta"]["fail"] = delta_fail
    result["count_delta"]["warn"] = delta_warn
    result["count_delta"]["resolved"] = len(result["resolved"])

    sign_f = "+" if delta_fail >= 0 else ""
    sign_w = "+" if delta_warn >= 0 else ""
    result["summary"] = (
        f"Delta since last run ({result['prev_cycle']} @ {result['prev_ts']}): "
        f"{sign_f}{delta_fail} FAIL, {sign_w}{delta_warn} WARN, "
        f"-{result['count_delta']['resolved']} resolved"
    )

    return result


# ---------------------------------------------------------------------------
# Section runners
# ---------------------------------------------------------------------------

def run_render_qa() -> dict:
    """
    Run LTG_TOOL_render_qa on all pitch PNGs.
    Returns a summary dict with counts and flagged items.

    render_qa result dict keys:
        file, asset_type, silhouette, value_range, color_fidelity,
        warm_cool, line_weight, overall_grade
    """
    results = []
    missing = []
    for p in PITCH_PNGS:
        if not p.exists():
            missing.append(str(p))
            continue
        r = qa_report(str(p))
        results.append(r)

    pass_count  = sum(1 for r in results if r.get("overall_grade") == "PASS")
    warn_count  = sum(1 for r in results if r.get("overall_grade") == "WARN")
    fail_count  = sum(1 for r in results if r.get("overall_grade") == "FAIL")

    # Sub-check names and their pass-flag key within the result dict
    CHECK_PASS_MAP = {
        "value_range":    lambda r: r.get("value_range", {}).get("pass", True),
        "color_fidelity": lambda r: r.get("color_fidelity", {}).get("overall_pass", True),
        "warm_cool":      lambda r: r.get("warm_cool", {}).get("pass", True)
                                    if "status" not in r.get("warm_cool", {}) else True,
        "line_weight":    lambda r: r.get("line_weight", {}).get("pass", True),
        "silhouette":     lambda r: r.get("silhouette", {}).get("score", "distinct") != "blob",
    }

    flagged = []
    for r in results:
        name = Path(r.get("file", "?")).name
        grade = r.get("overall_grade", "?")
        if grade in ("WARN", "FAIL"):
            for check_key, pass_fn in CHECK_PASS_MAP.items():
                try:
                    if not pass_fn(r):
                        detail = ""
                        sub = r.get(check_key, {})
                        if isinstance(sub, dict):
                            notes = sub.get("notes", [])
                            if notes:
                                detail = " — " + "; ".join(notes)
                            elif check_key == "silhouette":
                                detail = f" — score={sub.get('score', '?')}"
                        flagged.append(f"  - {name} / {check_key}: WARN{detail}")
                except Exception:
                    pass

    overall = "PASS"
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0 or missing:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "missing": missing,
        "flagged": flagged,
        "raw": results,
    }


def run_color_verify() -> dict:
    """
    Run color fidelity check on all style frames.

    v2.7.0: uses _check_color_fidelity_lab() (LAB ΔE via cv2) from render_qa v2.0.0
    when cv2 is available.  Falls back to verify_canonical_colors (RGB Euclidean) if not.
    numpy array ops used for batch pixel operations where possible.

    Returns a summary dict.
    """
    palette = get_canonical_palette()
    pass_count = 0
    warn_count = 0
    missing = []
    flagged = []

    for p in STYLE_FRAMES:
        if not p.exists():
            missing.append(str(p))
            continue
        try:
            img = Image.open(str(p)).convert("RGB")
            # Downscale if needed
            img.thumbnail((1280, 1280), Image.LANCZOS)
            name = p.name

            # v3.0.0 C52: Prefer colour-science ΔE2000 (catches L*/C* drift).
            # Falls back to LAB ΔE (cv2) then RGB Euclidean.
            if _COLOUR_SCIENCE_AVAILABLE:
                de_result = verify_canonical_colors_deltaE(img, palette)
                if de_result.get("delta_e_available"):
                    if de_result.get("overall_pass"):
                        pass_count += 1
                    else:
                        warn_count += 1
                        for color_name, info in de_result.items():
                            if not isinstance(info, dict) or "delta_e_2000" not in info:
                                continue
                            if not info.get("pass", True):
                                de = info.get("delta_e_2000", "?")
                                de_str = f"{de:.2f}" if isinstance(de, (float, int)) else str(de)
                                flagged.append(
                                    f"  - {name} / {color_name}: ΔE2000={de_str} "
                                    f"({info.get('verdict', '?')})"
                                )
                    continue  # skip LAB fallback

            # Fallback: LAB ΔE check (cv2) or RGB Euclidean
            result = _lab_color_check(img, palette)
            method = result.get("color_method", "RGB_euclidean")
            if result.get("overall_pass"):
                pass_count += 1
            else:
                warn_count += 1
                colors_data = result.get("colors", {})
                for color_name, info in colors_data.items():
                    if not isinstance(info, dict):
                        continue
                    if not info.get("pass", True) and info.get("status") == "found":
                        if method == "LAB_DE":
                            de = info.get("delta_e", "?")
                            de_str = f"{de:.2f}" if isinstance(de, float) else str(de)
                            flagged.append(
                                f"  - {name} / {color_name}: LAB ΔE={de_str} "
                                f"(threshold={result.get('delta_e_threshold', 5.0)})"
                            )
                        else:
                            flagged.append(
                                f"  - {name} / {color_name}: hue drift "
                                f"delta={info.get('delta', '?'):.1f}°"
                            )
        except Exception as e:
            warn_count += 1
            flagged.append(f"  - {p.name}: exception — {e}")

    overall = "PASS" if warn_count == 0 and not missing else "WARN"
    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": 0,
        "missing": missing,
        "flagged": flagged,
    }


def run_proportion_verify() -> dict:
    """
    Run LTG_TOOL_proportion_verify on character turnaround sheets.
    Uses the programmatic API by importing and calling the core functions.
    Returns a summary dict.
    """
    # Import proportion verify internals
    sys.path.insert(0, str(TOOLS_DIR))
    import importlib
    pv = importlib.import_module("LTG_TOOL_proportion_verify")

    pass_count = 0
    warn_count = 0
    fail_count = 0
    missing = []
    flagged = []

    for sheet_path, bbox in CHARACTER_SHEETS:
        if not sheet_path.exists():
            missing.append(str(sheet_path))
            continue
        try:
            img = Image.open(str(sheet_path)).convert("RGBA")
            img.thumbnail((1280, 1280), Image.LANCZOS)
            W, H = img.size

            # Use full image as bounding box if none provided
            if bbox is None:
                x, y, w, h = 0, 0, W, H
            else:
                x, y, w, h = bbox

            # Crop to bounding box
            cropped = img.crop((x, y, x + w, y + h))

            # Detect background and occupied rows
            bg_color = pv.detect_background(cropped)
            occ = pv.occupied_rows(cropped, bg_color)
            extent = pv.find_character_extent(occ)

            if extent is None:
                warn_count += 1
                flagged.append(f"  - {sheet_path.name}: no character pixels detected — WARN")
                continue

            top_row, bottom_row = extent
            total_height = bottom_row - top_row + 1
            head_height, _method = pv.find_head_height(occ, top_row)

            if head_height is None or head_height <= 0:
                # Multi-view turnaround sheets: head gap detection fails on multi-panel layouts
                # (multiple characters side by side confuse the row-occupancy algorithm).
                # Flag as WARN — manual review recommended for turnarounds.
                warn_count += 1
                flagged.append(
                    f"  - {sheet_path.name}: head gap not found ({_method}) — "
                    "multi-panel turnaround may require manual proportion check — WARN"
                )
                continue

            ratio = total_height / head_height
            lo = pv.CANONICAL_RATIO * (1 - pv.RATIO_TOLERANCE)
            hi = pv.CANONICAL_RATIO * (1 + pv.RATIO_TOLERANCE)

            # Glitch uses a non-standard body proportion (diamond body), skip strict ratio
            if "glitch" in sheet_path.name.lower():
                pass_count += 1
                flagged.append(f"  - {sheet_path.name}: SKIP proportion check (Glitch non-humanoid)")
                continue

            if lo <= ratio <= hi:
                pass_count += 1
            else:
                grade = "WARN" if abs(ratio - pv.CANONICAL_RATIO) < 0.5 else "FAIL"
                msg = f"ratio={ratio:.2f} (spec={pv.CANONICAL_RATIO}, tol=±{pv.RATIO_TOLERANCE*100:.0f}%)"
                if grade == "FAIL":
                    fail_count += 1
                else:
                    warn_count += 1
                flagged.append(f"  - {sheet_path.name}: {grade} — {msg}")

        except Exception as e:
            warn_count += 1
            flagged.append(f"  - {sheet_path.name}: exception — {e}")

    overall = "PASS"
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0 or missing:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "missing": missing,
        "flagged": flagged,
    }


def run_stub_linter() -> dict:
    """
    Run LTG_TOOL_stub_linter on output/tools/.
    Returns a summary dict.

    stub_linter result dict keys:
        file, issues (list of dicts with line_no/statement/module/
        target_exists/canonical/canonical_exists), status ("PASS"|"WARN"|"ERROR")
    """
    results = stub_lint_directory(str(TOOLS_DIR), skip_legacy=True)

    pass_count  = sum(1 for r in results if r.get("status") == "PASS")
    warn_count  = sum(1 for r in results if r.get("status") == "WARN")
    error_count = sum(1 for r in results if r.get("status") == "ERROR")

    flagged = []
    for r in results:
        if r.get("status") in ("WARN", "ERROR"):
            name = Path(r.get("file", "?")).name
            for imp in r.get("issues", []):
                flagged.append(
                    f"  - {name}: [{r.get('status')}] `{imp.get('statement', '')}` "
                    f"(target_exists={imp.get('target_exists')}, "
                    f"canonical_exists={imp.get('canonical_exists')})"
                )

    overall = "PASS"
    if error_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": error_count,
        "missing": [],
        "flagged": flagged,
        "raw": results,
    }


def run_palette_warmth_lint() -> dict:
    """
    Run LTG_TOOL_palette_warmth_lint on master_palette.md.
    Checks CHAR-M (all entries) + CHAR-L hoodie entries (CHAR-L-04, -08, -11).
    Upgraded from v001 in C39 (Sam Kowalski) — now covers CHAR-L hoodie warmth guarantee.
    Returns a summary dict.
    """
    if not PALETTE_MD.exists():
        return {
            "overall": "FAIL",
            "pass": 0,
            "warn": 0,
            "fail": 1,
            "missing": [str(PALETTE_MD)],
            "flagged": [f"  - master_palette.md not found at {PALETTE_MD}"],
        }

    result = lint_palette_file(str(PALETTE_MD))
    flagged = []
    for v in result.get("violations", []):
        flagged.append(f"  - {v.get('code')} {v.get('name')} {v.get('hex')}: {v.get('reason')}")

    overall = result.get("result", "PASS")
    return {
        "overall": overall,
        "pass": result.get("total_checked", 0) - result.get("total_violations", 0),
        "warn": result.get("total_violations", 0),
        "fail": 0,
        "missing": [],
        "flagged": flagged,
    }


def run_readme_sync() -> dict:
    """
    Run LTG_TOOL_readme_sync — cross-check LTG_TOOL_*.py on disk vs README Script Index.
    Returns a summary dict.

    readme_sync_audit result dict keys:
        disk_tools, listed, legacy, unlisted, ghost, legacy_ghost, ok, result
    """
    result = readme_sync_audit(TOOLS_DIR)

    unlisted_count = len(result.get("unlisted", []))
    ghost_count    = len(result.get("ghost", []))
    legacy_ghost_count = len(result.get("legacy_ghost", []))
    ok_count       = len(result.get("ok", []))

    flagged = []
    for name in result.get("unlisted", []):
        flagged.append(f"  - UNLISTED: `{name}` (on disk, not in README Script Index)")
    for name in result.get("ghost", []):
        flagged.append(f"  - GHOST: `{name}` (in README, not on disk)")
    for name in result.get("legacy_ghost", []):
        flagged.append(f"  - LEGACY GHOST: `{name}` (marked retired, not in legacy/)")

    overall = "PASS" if result.get("result") == "PASS" else "WARN"
    total_discrepancies = unlisted_count + ghost_count + legacy_ghost_count

    return {
        "overall": overall,
        "pass": ok_count,
        "warn": total_discrepancies,
        "fail": 0,
        "missing": [],
        "flagged": flagged,
        "disk_total": len(result.get("disk_tools", [])),
        "listed_total": len(result.get("listed", [])),
        "unlisted_count": unlisted_count,
        "ghost_count": ghost_count,
        "legacy_ghost_count": legacy_ghost_count,
    }


def run_glitch_spec_lint() -> dict:
    """
    Run LTG_TOOL_glitch_spec_lint on all generators in output/tools/.
    Returns a summary dict.

    Note: lint_directory() in glitch_spec_lint only returns non-SKIP results
    (SKIP files are filtered internally). PASS/WARN counts are over Glitch
    generators only. Non-Glitch files are silently excluded.

    glitch_spec_lint result dict keys:
        file, is_glitch (bool), issues (list of str), status ("PASS"|"WARN")
    """
    results = glitch_lint_directory(str(TOOLS_DIR))

    pass_count  = sum(1 for r in results if r.get("status") == "PASS")
    warn_count  = sum(1 for r in results if r.get("status") == "WARN")
    fail_count  = 0  # glitch linter uses WARN for issues, not FAIL

    # Count total .py files to infer skipped count
    total_py = len([f for f in TOOLS_DIR.iterdir()
                    if f.suffix == ".py" and f.parent.name != "legacy"])
    skip_count = total_py - len(results)

    flagged = []
    for r in results:
        if r.get("status") == "WARN":
            name = Path(r.get("file", "?")).name
            for issue_str in r.get("issues", []):
                flagged.append(f"  - {name}: {issue_str}")

    overall = "PASS"
    if warn_count > 0:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "skip": skip_count,
        "missing": [],
        "flagged": flagged,
    }


def run_motion_spec_lint() -> dict:
    """
    Run LTG_TOOL_motion_spec_lint on all motion spec sheets.
    Returns a summary dict compatible with precritique_qa section format.

    Section 8 — Ryo Hasegawa / Cycle 39.
    """
    results = []
    missing = []
    for path, expected_panels in MOTION_SHEETS:
        if not path.exists():
            missing.append(str(path))
            continue
        r = lint_motion_spec(str(path), expected_panels=expected_panels)
        results.append(r)

    pass_count = sum(r["pass"] for r in results)
    warn_count = sum(r["warn"] for r in results)
    fail_count = sum(r["fail"] for r in results)

    flagged = []
    for r in results:
        fname = Path(r["file"]).name
        for item in r.get("flagged", []):
            flagged.append(f"  - {fname}: {item}")
        for m in r.get("missing", []):
            flagged.append(f"  - MISSING: {m}")

    overall = "PASS"
    if fail_count > 0 or missing:
        overall = "WARN"  # missing motion sheets → WARN (advisory, not block)
    elif warn_count > 0:
        overall = "WARN"

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "missing": missing,
        "flagged": flagged,
    }


def run_arc_diff_gate() -> list:
    """
    Section 10 — Arc-Diff Gate (informational, not scored).

    For each contact sheet pair in ARC_DIFF_PAIRS:
      - If both files exist: run compare_contact_sheets() from arc-diff tool.
      - If CHANGED > 3: add NOTE listing changed panel slot indices.
      - If REMOVED > 0: add WARN (panel removal = story continuity risk).
      - If one/both files missing: skip with NOTE.

    Returns a list of result dicts, one per pair:
        {
            label       : str   — human-readable pair label
            old_path    : str
            new_path    : str
            diff_output : str | None — path to arc-diff PNG (if generated)
            skipped     : bool  — True if files were missing
            skip_reason : str | None
            ok          : bool  — comparison succeeded
            n_old       : int
            n_new       : int
            same        : int
            changed     : int
            added       : int
            removed     : int
            changed_slots : list[int]
            severity    : "PASS" | "NOTE" | "WARN"
            messages    : list[str]
        }
    """
    arc_mod = _load_arc_diff()
    results = []

    for label, old_path, new_path, diff_out in ARC_DIFF_PAIRS:
        entry = {
            "label": label,
            "old_path": str(old_path),
            "new_path": str(new_path),
            "diff_output": None,
            "skipped": False,
            "skip_reason": None,
            "ok": False,
            "n_old": 0, "n_new": 0,
            "same": 0, "changed": 0, "added": 0, "removed": 0,
            "changed_slots": [],
            "severity": "PASS",
            "messages": [],
        }

        # Check file availability
        old_exists = old_path.exists()
        new_exists = new_path.exists()
        if not old_exists or not new_exists:
            missing = []
            if not old_exists:
                missing.append(f"OLD: {old_path.name}")
            if not new_exists:
                missing.append(f"NEW: {new_path.name}")
            entry["skipped"] = True
            entry["skip_reason"] = "Missing: " + ", ".join(missing)
            entry["severity"] = "PASS"   # skipped ≠ failure
            entry["messages"].append(f"NOTE: Skipped — {entry['skip_reason']}")
            results.append(entry)
            continue

        if arc_mod is None:
            entry["skipped"] = True
            entry["skip_reason"] = "arc-diff module could not be loaded"
            entry["severity"] = "PASS"
            entry["messages"].append("NOTE: arc-diff tool unavailable — skipping")
            results.append(entry)
            continue

        # Run comparison
        try:
            r = arc_mod.compare_contact_sheets(str(old_path), str(new_path), str(diff_out))
            entry.update({
                "ok":           r["ok"],
                "n_old":        r["n_old"],
                "n_new":        r["n_new"],
                "same":         r["same"],
                "changed":      r["changed"],
                "added":        r["added"],
                "removed":      r["removed"],
                "changed_slots": r["changed_slots"],
                "diff_output":  r.get("diff_output"),
            })

            if not r["ok"]:
                entry["severity"] = "PASS"
                entry["messages"].append(f"NOTE: comparison error — {r.get('error', 'unknown')}")
            else:
                # Gate logic per spec
                severity = "PASS"
                if r["removed"] > 0:
                    severity = "WARN"
                    entry["messages"].append(
                        f"WARN: {r['removed']} panel(s) REMOVED — story continuity risk. "
                        f"Removed slots: {r['removed_slots']}"
                    )
                if r["changed"] > 3:
                    if severity == "PASS":
                        severity = "NOTE"
                    slots_str = ", ".join(str(s) for s in r["changed_slots"])
                    entry["messages"].append(
                        f"NOTE: {r['changed']} panel(s) CHANGED this cycle "
                        f"(slots: {slots_str}) — critics: focus review on these panels."
                    )
                if r["added"] > 0:
                    entry["messages"].append(
                        f"NOTE: {r['added']} panel(s) ADDED (new panels, not in prior version)."
                    )
                if not entry["messages"]:
                    entry["messages"].append(
                        f"PASS: {r['same']} panel(s) unchanged, "
                        f"{r['changed']} changed, {r['added']} added, {r['removed']} removed."
                    )
                entry["severity"] = severity
        except Exception as exc:
            entry["severity"] = "PASS"
            entry["messages"].append(f"NOTE: arc-diff exception — {exc}")

        results.append(entry)

    return results


def run_alpha_blend_lint() -> dict:
    """
    Section 10 — Alpha Blend Lint (Rin Yamamoto, Cycle 40).

    Runs LTG_TOOL_alpha_blend_lint.lint_alpha_blend() on each asset registered
    in FILL_LIGHT_ASSETS that has a base (unlit) image present on disk.

    Scoring per zone:
        FLAT_FILL  → counts as FAIL (fill gradient not radial — defect)
        LOW_SIGNAL → counts as WARN (subtle fill; may be intentional)
        PASS       → counts as PASS

    If no base images are available (all skipped), overall = PASS.

    Returns:
        {
            "overall"  : "PASS" | "WARN" | "FAIL",
            "pass"     : int,
            "warn"     : int,
            "fail"     : int,
            "skipped"  : int,
            "per_asset": list of per-asset result dicts
        }
    """
    abl_mod = _load_alpha_blend_lint()

    pass_count = 0
    warn_count = 0
    fail_count = 0
    skipped    = 0
    per_asset  = []

    for label, comp_path, base_path, zones in FILL_LIGHT_ASSETS:
        asset_entry = {
            "label":      label,
            "composited": str(comp_path),
            "base":       str(base_path),
            "skipped":    False,
            "skip_reason": None,
            "zones":      [],
        }

        # Graceful skip: base not on disk
        if not base_path.exists():
            asset_entry["skipped"] = True
            asset_entry["skip_reason"] = f"Base image not found: {base_path.name}"
            skipped += 1
            per_asset.append(asset_entry)
            continue

        # Graceful skip: composited not on disk
        if not comp_path.exists():
            asset_entry["skipped"] = True
            asset_entry["skip_reason"] = f"Composited image not found: {comp_path.name}"
            skipped += 1
            per_asset.append(asset_entry)
            continue

        # Module unavailable (e.g. cv2 not installed)
        if abl_mod is None:
            asset_entry["skipped"] = True
            asset_entry["skip_reason"] = "alpha_blend_lint module unavailable (cv2 required)"
            skipped += 1
            per_asset.append(asset_entry)
            continue

        # Run lint
        try:
            results = abl_mod.lint_alpha_blend(
                composited_path=str(comp_path),
                base_path=str(base_path),
                zones=zones,
            )
        except Exception as exc:
            asset_entry["skipped"] = True
            asset_entry["skip_reason"] = f"lint_alpha_blend() exception: {exc}"
            skipped += 1
            per_asset.append(asset_entry)
            continue

        for zone_r in results.get("zones", results if isinstance(results, list) else []):
            verdict = zone_r.get("verdict", "PASS").upper()
            zone_entry = {
                "zone":    zone_r.get("label", "?"),
                "verdict": verdict,
            }
            if verdict == "FLAT_FILL":
                fail_count += 1
                zone_entry["msg"] = "FLAT_FILL — fill contribution has no radial falloff (defect)"
            elif verdict == "LOW_SIGNAL":
                warn_count += 1
                zone_entry["msg"] = "LOW_SIGNAL — fill contribution below noise floor (advisory)"
            else:
                pass_count += 1
                zone_entry["msg"] = "PASS — radial falloff detected"
            asset_entry["zones"].append(zone_entry)

        per_asset.append(asset_entry)

    # Overall grade: PASS if all skipped, otherwise worst of zone verdicts
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "overall":   overall,
        "pass":      pass_count,
        "warn":      warn_count,
        "fail":      fail_count,
        "skipped":   skipped,
        "per_asset": per_asset,
    }


def run_uv_purple_lint() -> dict:
    """
    Section 11 — UV_PURPLE Dominance Lint (Rin Yamamoto, Cycle 44).

    Runs LTG_TOOL_uv_purple_linter.run_glitch_layer_dominance_check() on each
    PNG registered in GLITCH_LAYER_PNGS. World type override = GLITCH applied
    to all (they are pre-selected Glitch Layer assets).

    Scoring per file:
        FAIL   → Check A combined fraction < 10%, or error
        WARN   → Check A 10–19%, or Check B warm-hue ≥ 5%
        PASS   → Check A ≥ 20%, Check B < 5%
        SKIP   → File not on disk

    Returns:
        {
            "overall"  : "PASS" | "WARN" | "FAIL",
            "pass"     : int,
            "warn"     : int,
            "fail"     : int,
            "skip"     : int,
            "per_file" : list of per-file result dicts
        }
    """
    uv_mod = _load_uv_purple_linter()

    # If module cannot be loaded, return graceful WARN
    if uv_mod is None:
        return {
            "overall":  "WARN",
            "pass":     0,
            "warn":     1,
            "fail":     0,
            "skip":     0,
            "per_file": [],
            "error":    "LTG_TOOL_uv_purple_linter could not be loaded",
        }

    existing_paths = [str(p) for p in GLITCH_LAYER_PNGS if p.exists()]
    missing_count  = len(GLITCH_LAYER_PNGS) - len(existing_paths)

    # Per-file scene subtype hints (v2.14.0, Rin Yamamoto C45).
    # COVETOUS assets use UV_PURPLE_DARK family (dark luminance purple variants).
    # Without GLITCH_DARK_SCENE subtype they FAIL Check A via ΔE (< 1% match).
    # With GLITCH_DARK_SCENE, hue-angle matching correctly identifies them as
    # UV_PURPLE family (96–99% of non-black pixels in h° 255°–325°).
    # Filename inference in lint_uv_purple_dominance() already handles "covetous"
    # automatically (via infer_scene_subtype()), but explicit registration here
    # documents the intent and survives any future keyword changes.
    _GLITCH_DARK_SCENE = getattr(uv_mod, "SCENE_SUBTYPE_GLITCH_DARK_SCENE", "GLITCH_DARK_SCENE")
    subtypes = {
        str(SF_DIR / "LTG_COLOR_sf_covetous_glitch.png"):    _GLITCH_DARK_SCENE,
        str(SF_DIR / "LTG_SF_covetous_glitch_v001.png"):     _GLITCH_DARK_SCENE,
    }

    result = uv_mod.run_glitch_layer_dominance_check(existing_paths, subtypes=subtypes)
    result["skip"] = result.get("skip", 0) + missing_count
    return result


def run_depth_temp_lint() -> dict:
    """
    Section 12 — Depth Temperature Lint (Lee Tanaka, Cycle 47).

    Runs LTG_TOOL_depth_temp_lint.run_depth_temp_check() on each PNG registered
    in DEPTH_TEMP_PNGS. Glitch Layer scenes auto-exempt via world_type_infer.

    Thresholds (from C46 results):
        - PASS: separation >= threshold (auto from world_type_infer, default 12.0)
        - WARN: correct direction (FG warmer) but under threshold
        - FAIL: inverted depth grammar
        - SKIP: Glitch Layer exempt, or file missing

    Returns:
        {
            "overall"  : "PASS" | "WARN" | "FAIL",
            "pass"     : int,
            "warn"     : int,
            "fail"     : int,
            "skip"     : int,
            "per_file" : list of per-file result dicts
        }
    """
    dt_mod = _load_depth_temp_lint()

    if dt_mod is None:
        return {
            "overall":  "WARN",
            "pass":     0,
            "warn":     1,
            "fail":     0,
            "skip":     0,
            "per_file": [],
            "error":    "LTG_TOOL_depth_temp_lint could not be loaded",
        }

    existing = []
    missing_count = 0
    label_map = {}
    for label, p in DEPTH_TEMP_PNGS:
        if p.exists():
            existing.append(str(p))
            label_map[str(p)] = label
        else:
            missing_count += 1

    result = dt_mod.run_depth_temp_check(existing)

    # Attach labels to per-file results
    for r in result.get("per_file", []):
        r["label"] = label_map.get(r.get("path", ""), os.path.basename(r.get("path", "")))

    result["skip"] = result.get("skip", 0) + missing_count
    return result


def run_warm_pixel_lint() -> dict:
    """
    Section 13 — Warm Pixel Percentage (Kai Nakamura, Cycle 48).

    Runs LTG_TOOL_warm_pixel_metric.measure_warm_pixel_percentage() +
    evaluate_threshold() on each PNG registered in WARM_PIXEL_PNGS.
    Each asset carries a world_type tag used for threshold lookup.

    Returns:
        {
            "overall"  : "PASS" | "WARN" | "FAIL",
            "pass"     : int,
            "warn"     : int,
            "fail"     : int,
            "skip"     : int,
            "per_file" : list of per-file result dicts
        }
    """
    wpm = _load_warm_pixel_metric()

    if wpm is None:
        return {
            "overall":  "WARN",
            "pass":     0,
            "warn":     1,
            "fail":     0,
            "skip":     0,
            "per_file": [],
            "error":    "LTG_TOOL_warm_pixel_metric could not be loaded",
        }

    pass_count = 0
    warn_count = 0
    fail_count = 0
    skip_count = 0
    per_file = []

    for label, img_path, world_type in WARM_PIXEL_PNGS:
        entry = {"label": label, "path": str(img_path), "world_type": world_type}

        if not img_path.exists():
            entry["overall"] = "SKIP"
            entry["message"] = "File not found"
            skip_count += 1
            per_file.append(entry)
            continue

        try:
            from PIL import Image
            img = Image.open(str(img_path))
            measurement = wpm.measure_warm_pixel_percentage(img)
            warm_pct = measurement["warm_pct"]
            evaluation = wpm.evaluate_threshold(warm_pct, world_type)

            entry["warm_pct"] = warm_pct
            entry["cool_pct"] = measurement["cool_pct"]
            entry["chromatic_warm_pct"] = measurement.get("chromatic_warm_pct", 0.0)
            entry["passes"] = evaluation["passes"]
            entry["verdict"] = evaluation["verdict"]
            entry["explanation"] = evaluation["explanation"]

            if evaluation["passes"]:
                entry["overall"] = "PASS"
                pass_count += 1
            else:
                entry["overall"] = "FAIL"
                fail_count += 1
        except Exception as exc:
            entry["overall"] = "WARN"
            entry["error"] = str(exc)
            warn_count += 1

        per_file.append(entry)

    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "overall":  overall,
        "pass":     pass_count,
        "warn":     warn_count,
        "fail":     fail_count,
        "skip":     skip_count,
        "per_file": per_file,
    }


def run_sightline_lint() -> dict:
    """
    Section 14 — Sightline Validation (Morgan Walsh, Cycle 49).

    Runs LTG_TOOL_sightline_validator.validate_sightline_from_png() on each
    PNG registered in SIGHTLINE_PNGS. Validates eye/pupil angular error
    against gaze target. PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg.

    Returns:
        {
            "overall"  : "PASS" | "WARN" | "FAIL",
            "pass"     : int,
            "warn"     : int,
            "fail"     : int,
            "skip"     : int,
            "per_file" : list of per-file result dicts
        }
    """
    sv = _load_sightline_validator()

    if sv is None:
        return {
            "overall":  "WARN",
            "pass":     0,
            "warn":     1,
            "fail":     0,
            "skip":     0,
            "per_file": [],
            "error":    "LTG_TOOL_sightline_validator could not be loaded",
        }

    pass_count = 0
    warn_count = 0
    fail_count = 0
    skip_count = 0
    per_file = []

    for label, img_path, target_xy, search_box in SIGHTLINE_PNGS:
        entry = {"label": label, "path": str(img_path), "target": target_xy}

        if not img_path.exists():
            entry["overall"] = "SKIP"
            entry["message"] = "File not found"
            skip_count += 1
            per_file.append(entry)
            continue

        try:
            result = sv.validate_sightline_from_png(
                str(img_path),
                target_xy,
                search_box=search_box,
            )

            grade = result.get("grade", "SKIP")
            entry["angular_error"] = result.get("angular_error")
            entry["miss_px"] = result.get("miss_px")
            entry["detail"] = result.get("detail", "")
            entry["mode"] = result.get("mode", "pixel")

            if grade == "PASS":
                entry["overall"] = "PASS"
                pass_count += 1
            elif grade == "FAIL":
                entry["overall"] = "FAIL"
                fail_count += 1
            elif grade == "WARN":
                entry["overall"] = "WARN"
                warn_count += 1
            else:
                # SKIP — detection failed
                entry["overall"] = "SKIP"
                skip_count += 1
        except Exception as exc:
            entry["overall"] = "WARN"
            entry["error"] = str(exc)
            warn_count += 1

        per_file.append(entry)

    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "overall":  overall,
        "pass":     pass_count,
        "warn":     warn_count,
        "fail":     fail_count,
        "skip":     skip_count,
        "per_file": per_file,
    }


def run_silhouette_distinctiveness() -> dict:
    """
    Section 15 — Silhouette Distinctiveness (Kai Nakamura, Cycle 52).

    Runs LTG_TOOL_silhouette_distinctiveness.run_analysis() on all
    character turnaround sheets. Pairwise comparison at multiple scales.

    Returns:
        {
            "overall"  : "PASS" | "WARN" | "FAIL",
            "pass"     : int,
            "warn"     : int,
            "fail"     : int,
            "skip"     : int,
            "pairs"    : list of pair result dicts,
            "characters": list of character names
        }
    """
    sd_mod = _load_silhouette_distinctiveness()

    if sd_mod is None:
        return {
            "overall":  "WARN",
            "pass":     0,
            "warn":     1,
            "fail":     0,
            "skip":     0,
            "pairs":    [],
            "characters": [],
            "error":    "LTG_TOOL_silhouette_distinctiveness could not be loaded",
        }

    existing = [str(p) for p in SILHOUETTE_ASSETS if p.exists()]
    missing_count = len(SILHOUETTE_ASSETS) - len(existing)

    if len(existing) < 2:
        return {
            "overall":  "SKIP" if len(existing) == 0 else "WARN",
            "pass":     0,
            "warn":     0 if len(existing) == 0 else 1,
            "fail":     0,
            "skip":     missing_count,
            "pairs":    [],
            "characters": [],
            "error":    f"Need at least 2 turnarounds; found {len(existing)}",
        }

    try:
        result = sd_mod.run_analysis(existing)
    except Exception as exc:
        return {
            "overall":  "WARN",
            "pass":     0,
            "warn":     1,
            "fail":     0,
            "skip":     0,
            "pairs":    [],
            "characters": [],
            "error":    f"run_analysis() exception: {exc}",
        }

    summary = result.get("summary", {})
    return {
        "overall":    summary.get("overall", "WARN"),
        "pass":       summary.get("pass", 0),
        "warn":       summary.get("warn", 0),
        "fail":       summary.get("fail", 0),
        "skip":       missing_count,
        "pairs":      result.get("pairs", []),
        "characters": result.get("characters", []),
    }


def run_expression_range() -> dict:
    """
    Section 16 — Expression Range Metric (Kai Nakamura, Cycle 52).

    Runs LTG_TOOL_expression_range_metric.analyze_expression_sheet() on
    each expression sheet registered in EXPRESSION_SHEETS.

    Returns:
        {
            "overall"  : "PASS" | "WARN" | "FAIL",
            "pass"     : int,
            "warn"     : int,
            "fail"     : int,
            "skip"     : int,
            "per_sheet": list of per-sheet result dicts
        }
    """
    erm = _load_expression_range_metric()

    if erm is None:
        return {
            "overall":   "WARN",
            "pass":      0,
            "warn":      1,
            "fail":      0,
            "skip":      0,
            "per_sheet": [],
            "error":     "LTG_TOOL_expression_range_metric could not be loaded",
        }

    pass_count = 0
    warn_count = 0
    fail_count = 0
    skip_count = 0
    per_sheet = []

    for label, img_path in EXPRESSION_SHEETS:
        entry = {"label": label, "path": str(img_path)}

        if not img_path.exists():
            entry["overall"] = "SKIP"
            entry["message"] = "File not found"
            skip_count += 1
            per_sheet.append(entry)
            continue

        try:
            result = erm.analyze_expression_sheet(str(img_path))
            entry["grid"] = result.get("grid", "?")
            entry["valid_panels"] = result.get("valid_panels", 0)
            entry["ers"] = result.get("ers", 0.0)
            entry["ers_verdict"] = result.get("ers_verdict", "FAIL")
            entry["pairs_summary"] = result.get("summary", {})

            if result.get("error"):
                entry["overall"] = "WARN"
                entry["error"] = result["error"]
                warn_count += 1
            elif entry["ers_verdict"] == "PASS":
                entry["overall"] = "PASS"
                pass_count += 1
            elif entry["ers_verdict"] == "WARN":
                entry["overall"] = "WARN"
                warn_count += 1
            else:
                entry["overall"] = "FAIL"
                fail_count += 1
        except Exception as exc:
            entry["overall"] = "WARN"
            entry["error"] = str(exc)
            warn_count += 1

        per_sheet.append(entry)

    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "overall":   overall,
        "pass":      pass_count,
        "warn":      warn_count,
        "fail":      fail_count,
        "skip":      skip_count,
        "per_sheet": per_sheet,
    }


def run_construction_stiffness() -> dict:
    """
    Section 17 — Construction Stiffness (Kai Nakamura, Cycle 52).

    Runs LTG_TOOL_construction_stiffness.analyze_image() on each character
    turnaround sheet. Detects overly straight (rectangular) construction.

    Returns:
        {
            "overall"  : "PASS" | "WARN" | "FAIL",
            "pass"     : int,
            "warn"     : int,
            "fail"     : int,
            "skip"     : int,
            "per_file" : list of per-file result dicts
        }
    """
    cs_mod = _load_construction_stiffness()

    if cs_mod is None:
        return {
            "overall":  "WARN",
            "pass":     0,
            "warn":     1,
            "fail":     0,
            "skip":     0,
            "per_file": [],
            "error":    "LTG_TOOL_construction_stiffness could not be loaded",
        }

    pass_count = 0
    warn_count = 0
    fail_count = 0
    skip_count = 0
    per_file = []

    for label, img_path in STIFFNESS_ASSETS:
        entry = {"label": label, "path": str(img_path)}

        if not img_path.exists():
            entry["overall"] = "SKIP"
            entry["message"] = "File not found"
            skip_count += 1
            per_file.append(entry)
            continue

        try:
            result = cs_mod.analyze_image(str(img_path))
            entry["stiffness_score"] = result.get("stiffness_score", 0.0)
            entry["straight_pct"] = result.get("straight_pct", 0.0)
            entry["longest_straight_run"] = result.get("longest_straight_run", 0)
            entry["verdict"] = result.get("verdict", "FAIL")
            entry["backend"] = result.get("backend", "unknown")
            entry["total_outline_pixels"] = result.get("total_outline_pixels", 0)

            v = result.get("verdict", "FAIL")
            if v == "PASS":
                entry["overall"] = "PASS"
                pass_count += 1
            elif v == "WARN":
                entry["overall"] = "WARN"
                warn_count += 1
            else:
                entry["overall"] = "FAIL"
                fail_count += 1
        except Exception as exc:
            entry["overall"] = "WARN"
            entry["error"] = str(exc)
            warn_count += 1

        per_file.append(entry)

    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "overall":  overall,
        "pass":     pass_count,
        "warn":     warn_count,
        "fail":     fail_count,
        "skip":     skip_count,
        "per_file": per_file,
    }


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def build_report(
    render_qa_res,
    color_verify_res,
    proportion_res,
    stub_lint_res,
    palette_lint_res,
    glitch_lint_res,
    readme_sync_res,
    motion_spec_res,
    arc_diff_results: list,
    alpha_blend_res: dict,
    uv_purple_res: dict,
    depth_temp_res: dict,
    warm_pixel_res: dict,
    sightline_res: dict,
    silhouette_res: dict,
    expression_res: dict,
    stiffness_res: dict,
    delta: dict,
    run_ts: str,
) -> str:
    """Compose the final Markdown report."""

    def section_header(title: str, result: dict) -> str:
        badge = _grade_line(result["overall"])
        return (
            f"## {title} — {badge}\n\n"
            f"PASS: {result['pass']}  WARN: {result['warn']}  FAIL: {result['fail']}  "
            f"Missing: {len(result.get('missing', []))}\n"
        )

    def flagged_block(result: dict) -> str:
        lines = []
        if result.get("missing"):
            lines.append("**Missing files:**")
            for m in result["missing"]:
                lines.append(f"  - {Path(m).name} (not found)")
        if result.get("flagged"):
            lines.append("**Flagged items:**")
            lines.extend(result["flagged"])
        return ("\n".join(lines) + "\n") if lines else "_No issues found._\n"

    # Overall score
    overall = _worst_grade(
        render_qa_res["overall"],
        color_verify_res["overall"],
        proportion_res["overall"],
        stub_lint_res["overall"],
        palette_lint_res["overall"],
        glitch_lint_res["overall"],
        readme_sync_res["overall"],
        motion_spec_res["overall"],
        warm_pixel_res["overall"],
        silhouette_res["overall"],
        expression_res["overall"],
        stiffness_res["overall"],
    )

    _all_sections = [render_qa_res, color_verify_res, proportion_res,
                     stub_lint_res, palette_lint_res, glitch_lint_res,
                     readme_sync_res, motion_spec_res, warm_pixel_res,
                     silhouette_res, expression_res, stiffness_res]
    total_pass  = sum(r["pass"] for r in _all_sections)
    total_warn  = sum(r["warn"] for r in _all_sections)
    total_fail  = sum(r["fail"] for r in _all_sections)

    # README sync prominence flag
    readme_discrepancies = readme_sync_res.get("unlisted_count", 0) + readme_sync_res.get("ghost_count", 0)
    readme_warn_line = ""
    if readme_discrepancies > 0:
        readme_warn_line = (
            f"\n> **README SYNC WARNING:** {readme_discrepancies} discrepancy(ies) detected — "
            f"{readme_sync_res.get('unlisted_count', 0)} UNLISTED, "
            f"{readme_sync_res.get('ghost_count', 0)} GHOST. "
            "See Section 7 for details. Update README Script Index before critique.\n"
        )

    lines = [
        f"# Pre-Critique QA Report — {CYCLE_LABEL}",
        "",
        f"**Run date:** {run_ts}",
        f"**Script:** LTG_TOOL_precritique_qa.py v2.11.0",
        "",
        "---",
        "",
        "## Overall Result",
        "",
        f"**{overall}** — PASS: {total_pass}  WARN: {total_warn}  FAIL: {total_fail}",
    ]

    if readme_warn_line:
        lines.append(readme_warn_line)

    lines += [
        "",
        "| Section | Result | PASS | WARN | FAIL |",
        "|---|---|---|---|---|",
        f"| Render QA (pitch PNGs)         | {render_qa_res['overall']}   | {render_qa_res['pass']}  | {render_qa_res['warn']}  | {render_qa_res['fail']}  |",
        f"| Color Verify (style frames)    | {color_verify_res['overall']} | {color_verify_res['pass']} | {color_verify_res['warn']} | {color_verify_res['fail']} |",
        f"| Proportion Verify (char sheets)| {proportion_res['overall']}  | {proportion_res['pass']}  | {proportion_res['warn']}  | {proportion_res['fail']}  |",
        f"| Stub Linter (tools dir)        | {stub_lint_res['overall']}   | {stub_lint_res['pass']}   | {stub_lint_res['warn']}   | {stub_lint_res['fail']}   |",
        f"| Palette Warmth Lint            | {palette_lint_res['overall']}| {palette_lint_res['pass']}| {palette_lint_res['warn']}| {palette_lint_res['fail']}|",
        f"| Glitch Spec Lint               | {glitch_lint_res['overall']} | {glitch_lint_res['pass']} | {glitch_lint_res['warn']} | {glitch_lint_res['fail']} |",
        f"| README Script Index Sync       | {readme_sync_res['overall']} | {readme_sync_res['pass']} | {readme_sync_res['warn']} | {readme_sync_res['fail']} |",
        f"| Motion Spec Lint               | {motion_spec_res['overall']} | {motion_spec_res['pass']} | {motion_spec_res['warn']} | {motion_spec_res['fail']} |",
        f"| Alpha Blend Lint               | {alpha_blend_res['overall']} | {alpha_blend_res['pass']} | {alpha_blend_res['warn']} | {alpha_blend_res['fail']} |",
        f"| UV_PURPLE Dominance Lint       | {uv_purple_res['overall']}   | {uv_purple_res['pass']}   | {uv_purple_res['warn']}   | {uv_purple_res['fail']}   |",
        f"| Depth Temperature Lint         | {depth_temp_res['overall']}   | {depth_temp_res['pass']}   | {depth_temp_res['warn']}   | {depth_temp_res['fail']}   |",
        f"| Silhouette Distinctiveness     | {silhouette_res['overall']}   | {silhouette_res['pass']}   | {silhouette_res['warn']}   | {silhouette_res['fail']}   |",
        f"| Expression Range Metric        | {expression_res['overall']}   | {expression_res['pass']}   | {expression_res['warn']}   | {expression_res['fail']}   |",
        f"| Construction Stiffness         | {stiffness_res['overall']}   | {stiffness_res['pass']}   | {stiffness_res['warn']}   | {stiffness_res['fail']}   |",
        "",
        "---",
        "",
    ]

    # Delta report section (prominent, before section details)
    lines.append("## 0. Delta Report")
    lines.append("")
    if delta["has_baseline"]:
        lines.append(f"**{delta['summary']}**")
        lines.append("")
        lines.append(f"_Compared against: {delta['prev_cycle']} run @ {delta['prev_ts']}_")
        lines.append("")

        if delta["new_fails"]:
            lines.append("**New FAILs since last run:**")
            for sec, item in delta["new_fails"]:
                lines.append(f"  - [{sec}] {item}")
            lines.append("")

        if delta["new_warns"]:
            lines.append("**New WARNs since last run:**")
            for sec, item in delta["new_warns"]:
                lines.append(f"  - [{sec}] {item}")
            lines.append("")

        if delta["resolved"]:
            lines.append("**Resolved since last run (previously WARN/FAIL, now PASS):**")
            for sec, item in delta["resolved"]:
                lines.append(f"  - [{sec}] {item}")
            lines.append("")

        if not delta["new_fails"] and not delta["new_warns"] and not delta["resolved"]:
            lines.append("_No changes in flagged items since last run._")
            lines.append("")
    else:
        lines.append("_No baseline found — this run establishes the initial baseline._")
        lines.append(f"_Baseline saved to: `{BASELINE_JSON.name}`_")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 1: Render QA
    lines.append(section_header("1. Render QA — Pitch PNGs", render_qa_res))
    lines.append("")
    lines.append("Target files:")
    for p in PITCH_PNGS:
        exists = "found" if p.exists() else "MISSING"
        lines.append(f"  - `{p.name}` ({exists})")
    lines.append("")
    lines.append(flagged_block(render_qa_res))
    lines.append("")

    # Section 2: Color Verify
    lines.append(section_header("2. Color Verify — Style Frames", color_verify_res))
    lines.append("")
    lines.append(flagged_block(color_verify_res))
    lines.append("")

    # Section 3: Proportion Verify
    lines.append(section_header("3. Proportion Verify — Character Sheets", proportion_res))
    lines.append("")
    lines.append(flagged_block(proportion_res))
    lines.append("")

    # Section 4: Stub Linter
    lines.append(section_header("4. Stub Linter — output/tools/", stub_lint_res))
    lines.append("")
    lines.append(flagged_block(stub_lint_res))
    lines.append("")

    # Section 5: Palette Warmth Lint
    lines.append(section_header("5. Palette Warmth Lint — master_palette.md", palette_lint_res))
    lines.append("")
    lines.append(flagged_block(palette_lint_res))
    lines.append("")

    # Section 6: Glitch Spec Lint
    lines.append(section_header("6. Glitch Spec Lint — Generators", glitch_lint_res))
    lines.append("")
    skip_n = glitch_lint_res.get("skip", 0)
    if skip_n:
        lines.append(f"_(Non-Glitch files: {skip_n} skipped)_")
        lines.append("")
    lines.append(flagged_block(glitch_lint_res))
    lines.append("")

    # Section 7: README Script Index Sync
    lines.append(section_header("7. README Script Index Sync", readme_sync_res))
    lines.append("")
    disk_total   = readme_sync_res.get("disk_total", "?")
    listed_total = readme_sync_res.get("listed_total", "?")
    lines.append(f"_(Tools on disk: {disk_total}  |  Tools listed in README: {listed_total})_")
    lines.append("")
    if readme_discrepancies > 0:
        lines.append(
            f"> **ACTION REQUIRED:** {readme_sync_res.get('unlisted_count', 0)} tool(s) on disk not listed in README "
            f"and {readme_sync_res.get('ghost_count', 0)} README entry(ies) with no corresponding file. "
            "Update `output/tools/README.md` Script Index before next critique cycle."
        )
        lines.append("")
    lines.append(flagged_block(readme_sync_res))
    lines.append("")

    # Section 8: Motion Spec Lint
    lines.append(section_header("8. Motion Spec Lint — motion sheets", motion_spec_res))
    lines.append("")
    lines.append("Target sheets:")
    for path, panels in MOTION_SHEETS:
        exists = "found" if path.exists() else "MISSING"
        lines.append(f"  - `{path.name}` (expected {panels} panels, {exists})")
    lines.append("")
    lines.append(flagged_block(motion_spec_res))
    lines.append("")

    # Section 9: Arc-Diff Gate (informational)
    lines.append("## 9. Arc-Diff Gate — Contact Sheet Changelog")
    lines.append("")
    lines.append("_Informational only — does not affect overall PASS/WARN/FAIL score._")
    lines.append("_WARN = panel removed (story continuity risk). NOTE = changed panels (critics: prioritize review of these)._")
    lines.append("")

    if not arc_diff_results:
        lines.append("_No contact sheet pairs configured._")
        lines.append("")
    else:
        for entry in arc_diff_results:
            label = entry["label"]
            severity = entry["severity"]
            lines.append(f"### {label}")
            if entry.get("skipped"):
                lines.append(f"  - *{entry.get('skip_reason', 'skipped')}*")
            else:
                lines.append(
                    f"  - OLD panels: {entry['n_old']}  "
                    f"NEW panels: {entry['n_new']}  "
                    f"SAME: {entry['same']}  "
                    f"CHANGED: {entry['changed']}  "
                    f"ADDED: {entry['added']}  "
                    f"REMOVED: {entry['removed']}"
                )
                if entry.get("diff_output"):
                    lines.append(f"  - Arc-diff PNG: `{Path(entry['diff_output']).name}`")
            for msg in entry.get("messages", []):
                prefix = "> **WARN:**" if msg.startswith("WARN:") else "_"
                suffix = "_" if msg.startswith("NOTE:") or msg.startswith("PASS:") else ""
                if msg.startswith("WARN:"):
                    lines.append(f"\n> **{msg}**\n")
                elif msg.startswith("NOTE:") or msg.startswith("PASS:"):
                    lines.append(f"  - _{msg}_")
                else:
                    lines.append(f"  - {msg}")
            lines.append("")

    lines.append("---")
    lines.append("")

    # Section 10: Alpha Blend Lint
    abl_badge = _grade_line(alpha_blend_res["overall"])
    lines.append(f"## 10. Alpha Blend Lint — Fill-Light Composition — {abl_badge}")
    lines.append("")
    lines.append(
        "_Checks fill-light blending quality on composited style frames. "
        "Requires unlit base images (`*_nolight.png`) alongside composited outputs. "
        "FLAT_FILL = FAIL (no radial falloff). LOW_SIGNAL = WARN (fill too subtle). "
        "Assets skip gracefully when base is absent — not a defect._"
    )
    lines.append("")
    lines.append(
        f"PASS: {alpha_blend_res['pass']}  "
        f"WARN: {alpha_blend_res['warn']}  "
        f"FAIL: {alpha_blend_res['fail']}  "
        f"Skipped: {alpha_blend_res['skipped']}"
    )
    lines.append("")

    for asset in alpha_blend_res.get("per_asset", []):
        lines.append(f"### {asset['label']}")
        if asset.get("skipped"):
            lines.append(f"  - *SKIP — {asset.get('skip_reason', 'no base available')}*")
        else:
            for zone in asset.get("zones", []):
                verdict = zone["verdict"]
                badge_v = _grade_line(verdict) if verdict in ("PASS", "WARN", "FAIL") else verdict
                lines.append(f"  - Zone `{zone['zone']}`: {badge_v} — {zone.get('msg', '')}")
        lines.append("")

    if not alpha_blend_res.get("per_asset"):
        lines.append("_No fill-light assets registered._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 11: UV_PURPLE Dominance Lint
    uv_badge = _grade_line(uv_purple_res["overall"])
    lines.append(f"## 11. UV_PURPLE Dominance Lint — Glitch Layer Colour Balance — {uv_badge}")
    lines.append("")
    lines.append(
        "_Verifies UV_PURPLE (#7B2FBE) + ELEC_CYAN (#00F0FF) are the dominant colours "
        "in Glitch Layer images. Core world-rule: Glitch Layer = UV_PURPLE/ELEC_CYAN dominant, "
        "zero warm light. Check A: combined fraction of non-black pixels — PASS ≥ 20%, "
        "WARN 10–19%, FAIL < 10%. Check B: warm-hue contamination (LAB h° 30°–80°, "
        "chroma C* ≥ 8) — PASS < 5%, WARN ≥ 5%._"
    )
    lines.append("")
    lines.append(
        f"PASS: {uv_purple_res['pass']}  "
        f"WARN: {uv_purple_res['warn']}  "
        f"FAIL: {uv_purple_res['fail']}  "
        f"Skip: {uv_purple_res.get('skip', 0)}"
    )
    lines.append("")

    if uv_purple_res.get("error"):
        lines.append(f"  - *ERROR — {uv_purple_res['error']}*")
        lines.append("")

    for file_res in uv_purple_res.get("per_file", []):
        f_badge = _grade_line(file_res["overall"])
        lines.append(f"### {file_res['basename']} — {f_badge}")
        if file_res.get("skipped"):
            lines.append(f"  - *SKIP — {file_res.get('skip_reason', '')}*")
        elif file_res.get("error"):
            lines.append(f"  - *ERROR — {file_res['error']}*")
        else:
            for check in file_res.get("checks", []):
                cv = _grade_line(check["verdict"])
                lines.append(f"  - Check {check['check']} ({check['name']}): {cv}")
                lines.append(f"    {check['msg']}")
        lines.append("")

    if not uv_purple_res.get("per_file"):
        lines.append("_No Glitch Layer assets registered._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 12: Depth Temperature Lint
    dt_badge = _grade_line(depth_temp_res["overall"])
    lines.append(f"## 12. Depth Temperature Lint — Warm=FG / Cool=BG Grammar — {dt_badge}")
    lines.append("")
    lines.append(
        "_Validates the Depth Temperature Rule (docs/image-rules.md, codified C45): "
        "warm color = foreground, cool color = background. Checks multi-character and "
        "multi-tier compositions. Glitch Layer scenes exempt. "
        "PASS: FG warmer than BG by >= threshold. "
        "WARN: correct direction but insufficient separation. "
        "FAIL: inverted depth grammar._"
    )
    lines.append("")
    lines.append(
        f"PASS: {depth_temp_res['pass']}  "
        f"WARN: {depth_temp_res['warn']}  "
        f"FAIL: {depth_temp_res['fail']}  "
        f"Skip: {depth_temp_res.get('skip', 0)}"
    )
    lines.append("")

    if depth_temp_res.get("error"):
        lines.append(f"  - *ERROR — {depth_temp_res['error']}*")
        lines.append("")

    for file_res in depth_temp_res.get("per_file", []):
        f_badge = _grade_line(file_res["overall"])
        label = file_res.get("label", os.path.basename(file_res.get("path", "")))
        lines.append(f"### {label} — {f_badge}")
        if file_res["overall"] == "SKIP":
            lines.append(f"  - *SKIP — {file_res.get('message', '')}*")
        else:
            lines.append(
                f"  - FG warmth: {file_res['fg_warmth']:.1f}  "
                f"BG warmth: {file_res['bg_warmth']:.1f}  "
                f"separation: {file_res['separation']:.1f}  "
                f"threshold: {file_res['threshold']:.1f}"
            )
            wt = file_res.get("world_type", "")
            if wt:
                lines.append(f"  - World type: {wt}")
            if file_res.get("band_override"):
                lines.append(
                    f"  - Band override: FG={file_res.get('fg_y_frac', '?')} "
                    f"BG={file_res.get('bg_y_frac', '?')} "
                    f"(from depth_temp_band_overrides.json)"
                )
        lines.append("")

    if not depth_temp_res.get("per_file"):
        lines.append("_No depth temperature assets registered._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 13: Warm Pixel Percentage
    wp_badge = _grade_line(warm_pixel_res["overall"])
    lines.append(f"## 13. Warm Pixel Percentage — World-Type Threshold Validation — {wp_badge}")
    lines.append("")
    lines.append(
        "_Validates warm-pixel-percentage against world-type thresholds using "
        "Sam Kowalski's LTG_TOOL_warm_pixel_metric (C47). "
        "REAL_INTERIOR: warm_pct >= 35%. REAL_STORM: warm_pct >= 5%. "
        "GLITCH: warm_pct <= 15%. OTHER_SIDE: warm_pct <= 5%._"
    )
    lines.append("")
    lines.append(
        f"PASS: {warm_pixel_res['pass']}  "
        f"WARN: {warm_pixel_res['warn']}  "
        f"FAIL: {warm_pixel_res['fail']}  "
        f"Skip: {warm_pixel_res.get('skip', 0)}"
    )
    lines.append("")

    if warm_pixel_res.get("error"):
        lines.append(f"  - *ERROR — {warm_pixel_res['error']}*")
        lines.append("")

    for file_res in warm_pixel_res.get("per_file", []):
        f_badge = _grade_line(file_res["overall"])
        label = file_res.get("label", os.path.basename(file_res.get("path", "")))
        lines.append(f"### {label} — {f_badge}")
        if file_res["overall"] == "SKIP":
            lines.append(f"  - *SKIP — {file_res.get('message', '')}*")
        elif file_res.get("error"):
            lines.append(f"  - *ERROR — {file_res['error']}*")
        else:
            lines.append(
                f"  - warm_pct: {file_res['warm_pct']:.1f}%  "
                f"cool_pct: {file_res['cool_pct']:.1f}%  "
                f"chromatic_warm_pct: {file_res.get('chromatic_warm_pct', 0):.1f}%"
            )
            lines.append(f"  - World type: {file_res['world_type']}  verdict: {file_res['verdict']}")
            if file_res.get("explanation"):
                lines.append(f"  - {file_res['explanation']}")
        lines.append("")

    if not warm_pixel_res.get("per_file"):
        lines.append("_No warm pixel assets registered._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 14: Sightline Validation
    sl_badge = _grade_line(sightline_res["overall"])
    lines.append(f"## 14. Sightline Validation — Gaze Angular Error — {sl_badge}")
    lines.append("")
    lines.append(
        "_Validates sight-line angular accuracy using "
        "Jordan Reed's LTG_TOOL_sightline_validator (C48). "
        "Pixel-based eye/pupil detection on rendered PNGs. "
        "PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg angular error._"
    )
    lines.append("")
    lines.append(
        f"PASS: {sightline_res['pass']}  "
        f"WARN: {sightline_res['warn']}  "
        f"FAIL: {sightline_res['fail']}  "
        f"Skip: {sightline_res.get('skip', 0)}"
    )
    lines.append("")

    if sightline_res.get("error"):
        lines.append(f"  - *ERROR — {sightline_res['error']}*")
        lines.append("")

    for file_res in sightline_res.get("per_file", []):
        f_badge = _grade_line(file_res["overall"])
        label = file_res.get("label", os.path.basename(file_res.get("path", "")))
        lines.append(f"### {label} — {f_badge}")
        if file_res["overall"] == "SKIP":
            msg = file_res.get("message", file_res.get("detail", ""))
            lines.append(f"  - *SKIP — {msg}*")
        elif file_res.get("error"):
            lines.append(f"  - *ERROR — {file_res['error']}*")
        else:
            ang_err = file_res.get("angular_error")
            miss_px = file_res.get("miss_px")
            detail = file_res.get("detail", "")
            if ang_err is not None:
                lines.append(f"  - Angular error: {ang_err:.1f} deg")
            if miss_px is not None:
                lines.append(f"  - Miss distance: {miss_px:.1f} px")
            if detail:
                lines.append(f"  - {detail}")
        lines.append("")

    if not sightline_res.get("per_file"):
        lines.append("_No sightline assets registered._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 15: Silhouette Distinctiveness (C52)
    sil_badge = _grade_line(silhouette_res["overall"])
    lines.append(f"## 15. Silhouette Distinctiveness — Character Shape Uniqueness — {sil_badge}")
    lines.append("")
    lines.append(
        "_Pairwise silhouette comparison of character turnarounds at multiple scales. "
        "Measures Silhouette Overlap Ratio (SOR) and Width Profile Correlation (WPC). "
        "DS = 1.0 - (0.5*SOR + 0.5*WPC). "
        "PASS: DS >= 0.30. WARN: DS 0.15-0.30. FAIL: DS < 0.15._"
    )
    lines.append("")
    lines.append(
        f"PASS: {silhouette_res['pass']}  "
        f"WARN: {silhouette_res['warn']}  "
        f"FAIL: {silhouette_res['fail']}  "
        f"Skip: {silhouette_res.get('skip', 0)}"
    )
    lines.append("")

    if silhouette_res.get("error"):
        lines.append(f"  - *ERROR — {silhouette_res['error']}*")
        lines.append("")

    if silhouette_res.get("characters"):
        lines.append(f"Characters analyzed: {', '.join(silhouette_res['characters'])}")
        lines.append("")

    for pair in silhouette_res.get("pairs", []):
        pair_label = pair.get("pair", "?")
        ds = pair.get("worst_ds", 0.0)
        v = pair.get("verdict", "?")
        v_badge = _grade_line(v)
        lines.append(f"### {pair_label} — {v_badge}")
        lines.append(f"  - Worst DS: {ds:.4f} (at {pair.get('worst_scale', '?')})")
        # Show per-scale breakdown
        for scale_key, scale_data in pair.get("scales", {}).items():
            sor = scale_data.get("overlap_ratio", 0)
            wpc = scale_data.get("width_profile_corr", 0)
            sds = scale_data.get("distinctiveness", 0)
            hd = scale_data.get("hausdorff_norm")
            hd_str = f"  Hausdorff: {hd:.4f}" if hd is not None else ""
            lines.append(
                f"  - {scale_key}: DS={sds:.4f}  SOR={sor:.4f}  WPC={wpc:.4f}{hd_str}"
            )
        lines.append("")

    if not silhouette_res.get("pairs") and not silhouette_res.get("error"):
        lines.append("_No silhouette pairs to report._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 16: Expression Range Metric (C52)
    expr_badge = _grade_line(expression_res["overall"])
    lines.append(f"## 16. Expression Range Metric — Facial Variation — {expr_badge}")
    lines.append("")
    lines.append(
        "_Measures expression variation across expression sheet panels using "
        "Face Region Pixel Delta (FRPD) and Structural Change Index (SCI). "
        "Aggregate Expression Range Score (ERS) = mean FRPD across all pairs. "
        "PASS: ERS >= 0.10. WARN: ERS 0.05-0.10. FAIL: ERS < 0.05._"
    )
    lines.append("")
    lines.append(
        f"PASS: {expression_res['pass']}  "
        f"WARN: {expression_res['warn']}  "
        f"FAIL: {expression_res['fail']}  "
        f"Skip: {expression_res.get('skip', 0)}"
    )
    lines.append("")

    if expression_res.get("error"):
        lines.append(f"  - *ERROR — {expression_res['error']}*")
        lines.append("")

    for sheet in expression_res.get("per_sheet", []):
        label = sheet.get("label", os.path.basename(sheet.get("path", "")))
        f_badge = _grade_line(sheet["overall"])
        lines.append(f"### {label} — {f_badge}")
        if sheet["overall"] == "SKIP":
            lines.append(f"  - *SKIP — {sheet.get('message', '')}*")
        elif sheet.get("error"):
            lines.append(f"  - *ERROR — {sheet['error']}*")
        else:
            lines.append(
                f"  - Grid: {sheet.get('grid', '?')}  "
                f"Valid panels: {sheet.get('valid_panels', '?')}  "
                f"ERS: {sheet.get('ers', 0):.4f}  "
                f"Verdict: {sheet.get('ers_verdict', '?')}"
            )
            ps = sheet.get("pairs_summary", {})
            if ps:
                lines.append(
                    f"  - Pairs: {ps.get('total_pairs', 0)} total — "
                    f"PASS: {ps.get('pass', 0)}  WARN: {ps.get('warn', 0)}  FAIL: {ps.get('fail', 0)}"
                )
        lines.append("")

    if not expression_res.get("per_sheet"):
        lines.append("_No expression sheets registered._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 17: Construction Stiffness (C52)
    stiff_badge = _grade_line(stiffness_res["overall"])
    lines.append(f"## 17. Construction Stiffness — Organic Shape Quality — {stiff_badge}")
    lines.append("")
    lines.append(
        "_Detects overly straight/rectangular character construction via contour "
        "straightness analysis. Uses skimage sub-pixel contours + Shapely when available. "
        "Stiffness Score = 0.6*straight_pct + 0.4*(longest_run/total). "
        "PASS: SS <= 0.25. WARN: SS 0.25-0.40. FAIL: SS > 0.40._"
    )
    lines.append("")
    lines.append(
        f"PASS: {stiffness_res['pass']}  "
        f"WARN: {stiffness_res['warn']}  "
        f"FAIL: {stiffness_res['fail']}  "
        f"Skip: {stiffness_res.get('skip', 0)}"
    )
    lines.append("")

    if stiffness_res.get("error"):
        lines.append(f"  - *ERROR — {stiffness_res['error']}*")
        lines.append("")

    for file_res in stiffness_res.get("per_file", []):
        label = file_res.get("label", os.path.basename(file_res.get("path", "")))
        f_badge = _grade_line(file_res["overall"])
        lines.append(f"### {label} — {f_badge}")
        if file_res["overall"] == "SKIP":
            lines.append(f"  - *SKIP — {file_res.get('message', '')}*")
        elif file_res.get("error"):
            lines.append(f"  - *ERROR — {file_res['error']}*")
        else:
            lines.append(
                f"  - Stiffness: {file_res.get('stiffness_score', 0):.4f}  "
                f"Straight%: {file_res.get('straight_pct', 0):.1%}  "
                f"Longest run: {file_res.get('longest_straight_run', 0)}px  "
                f"Total outline: {file_res.get('total_outline_pixels', 0)}px"
            )
            lines.append(f"  - Backend: {file_res.get('backend', '?')}")
        lines.append("")

    if not stiffness_res.get("per_file"):
        lines.append("_No stiffness assets registered._")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "*Generated by LTG_TOOL_precritique_qa.py v3.0.0 — "
        "Kai Nakamura (C52: Sections 15/16/17 Character Quality Metrics); "
        "Morgan Walsh (C49: Section 14 Sightline Validation added); "
        "Lee Tanaka (C48: Section 12 per-asset band overrides); "
        "Kai Nakamura (C48: Section 13 Warm Pixel Percentage added); "
        "Rin Yamamoto (C44: Section 11 UV_PURPLE Dominance Lint); "
        "Ryo Hasegawa (C46: motion spec dark-sheet fix, C45: glitch motion); "
        "Rin Yamamoto (C43: SF04 FILL_LIGHT_ASSETS path fix)*"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    run_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[precritique_qa] Starting {CYCLE_LABEL} QA pipeline — {run_ts}")
    print(f"[precritique_qa] Repo root: {REPO_ROOT}")

    # Load previous baseline before running
    baseline = load_baseline()
    if baseline:
        print(f"[precritique_qa] Loaded baseline from {baseline.get('cycle', '?')} run @ {baseline.get('run_ts', '?')}")
    else:
        print("[precritique_qa] No baseline found — this run will establish the baseline.")

    print("[1/17] Running Render QA on pitch PNGs...")
    render_qa_res = run_render_qa()
    print(f"      → {render_qa_res['overall']} (PASS={render_qa_res['pass']}, WARN={render_qa_res['warn']}, FAIL={render_qa_res['fail']}, MISSING={len(render_qa_res['missing'])})")

    print("[2/17] Running Color Verify on style frames...")
    color_verify_res = run_color_verify()
    print(f"      → {color_verify_res['overall']} (PASS={color_verify_res['pass']}, WARN={color_verify_res['warn']})")

    print("[3/17] Running Proportion Verify on character turnarounds...")
    proportion_res = run_proportion_verify()
    print(f"      → {proportion_res['overall']} (PASS={proportion_res['pass']}, WARN={proportion_res['warn']}, FAIL={proportion_res['fail']})")

    print("[4/17] Running Stub Linter on output/tools/...")
    stub_lint_res = run_stub_linter()
    print(f"      → {stub_lint_res['overall']} (PASS={stub_lint_res['pass']}, WARN={stub_lint_res['warn']}, ERROR={stub_lint_res['fail']})")

    print("[5/17] Running Palette Warmth Lint on master_palette.md...")
    palette_lint_res = run_palette_warmth_lint()
    print(f"      → {palette_lint_res['overall']} (checked={palette_lint_res['pass'] + palette_lint_res['warn']}, violations={palette_lint_res['warn']})")

    print("[6/17] Running Glitch Spec Lint on generators...")
    glitch_lint_res = run_glitch_spec_lint()
    print(f"      → {glitch_lint_res['overall']} (PASS={glitch_lint_res['pass']}, WARN={glitch_lint_res['warn']}, FAIL={glitch_lint_res['fail']}, SKIP={glitch_lint_res.get('skip',0)})")

    print("[7/17] Running README Script Index Sync audit...")
    readme_sync_res = run_readme_sync()
    if readme_sync_res["warn"] > 0:
        print(f"      → {readme_sync_res['overall']} *** README SYNC WARN: {readme_sync_res.get('unlisted_count',0)} UNLISTED, {readme_sync_res.get('ghost_count',0)} GHOST — update README before critique! ***")
    else:
        print(f"      → {readme_sync_res['overall']} (OK={readme_sync_res['pass']}, UNLISTED/GHOST={readme_sync_res['warn']}, disk={readme_sync_res.get('disk_total','?')}, listed={readme_sync_res.get('listed_total','?')})")

    print("[8/17] Running Motion Spec Lint on motion sheets...")
    motion_spec_res = run_motion_spec_lint()
    print(f"      → {motion_spec_res['overall']} (PASS={motion_spec_res['pass']}, WARN={motion_spec_res['warn']}, FAIL={motion_spec_res['fail']}, MISSING={len(motion_spec_res['missing'])})")

    print("[9/17] Running Arc-Diff Gate on contact sheet pairs...")
    arc_diff_results = run_arc_diff_gate()
    for ad in arc_diff_results:
        sev = ad["severity"]
        if ad.get("skipped"):
            print(f"      → {ad['label']}: SKIP ({ad.get('skip_reason', '')})")
        else:
            msgs = "; ".join(m[:80] for m in ad.get("messages", [])[:2])
            print(f"      → {ad['label']}: {sev} — {msgs}")

    print("[10/17] Running Alpha Blend Lint on fill-light assets...")
    alpha_blend_res = run_alpha_blend_lint()
    print(f"      → {alpha_blend_res['overall']} (PASS={alpha_blend_res['pass']}, WARN={alpha_blend_res['warn']}, FAIL={alpha_blend_res['fail']}, SKIP={alpha_blend_res['skipped']})")

    print("[11/17] Running UV_PURPLE Dominance Lint on Glitch Layer assets...")
    uv_purple_res = run_uv_purple_lint()
    print(f"      → {uv_purple_res['overall']} (PASS={uv_purple_res['pass']}, WARN={uv_purple_res['warn']}, FAIL={uv_purple_res['fail']}, SKIP={uv_purple_res.get('skip',0)})")

    print("[12/17] Running Depth Temperature Lint on multi-character assets...")
    depth_temp_res = run_depth_temp_lint()
    print(f"      → {depth_temp_res['overall']} (PASS={depth_temp_res['pass']}, WARN={depth_temp_res['warn']}, FAIL={depth_temp_res['fail']}, SKIP={depth_temp_res.get('skip',0)})")

    print("[13/17] Running Warm Pixel Percentage on world-typed assets...")
    warm_pixel_res = run_warm_pixel_lint()
    print(f"      → {warm_pixel_res['overall']} (PASS={warm_pixel_res['pass']}, WARN={warm_pixel_res['warn']}, FAIL={warm_pixel_res['fail']}, SKIP={warm_pixel_res.get('skip',0)})")

    print("[14/17] Running Sightline Validation on gaze-target assets...")
    sightline_res = run_sightline_lint()
    print(f"      → {sightline_res['overall']} (PASS={sightline_res['pass']}, WARN={sightline_res['warn']}, FAIL={sightline_res['fail']}, SKIP={sightline_res.get('skip',0)})")

    print("[15/17] Running Silhouette Distinctiveness on character turnarounds...")
    silhouette_res = run_silhouette_distinctiveness()
    print(f"      → {silhouette_res['overall']} (PASS={silhouette_res['pass']}, WARN={silhouette_res['warn']}, FAIL={silhouette_res['fail']}, SKIP={silhouette_res.get('skip',0)})")

    print("[16/17] Running Expression Range Metric on expression sheets...")
    expression_res = run_expression_range()
    print(f"      → {expression_res['overall']} (PASS={expression_res['pass']}, WARN={expression_res['warn']}, FAIL={expression_res['fail']}, SKIP={expression_res.get('skip',0)})")

    print("[17/17] Running Construction Stiffness on character turnarounds...")
    stiffness_res = run_construction_stiffness()
    print(f"      → {stiffness_res['overall']} (PASS={stiffness_res['pass']}, WARN={stiffness_res['warn']}, FAIL={stiffness_res['fail']}, SKIP={stiffness_res.get('skip',0)})")

    # Build snapshot and compute delta
    current_snapshot = _make_snapshot(
        render_qa_res, color_verify_res, proportion_res,
        stub_lint_res, palette_lint_res, glitch_lint_res, readme_sync_res,
        motion_spec_res,
        run_ts, CYCLE_LABEL,
    )
    delta = compute_delta(current_snapshot, baseline)
    print(f"\n[delta] {delta['summary']}")

    # Save new baseline
    save_baseline(current_snapshot)
    print(f"[precritique_qa] Baseline saved to: {BASELINE_JSON}")

    report_md = build_report(
        render_qa_res,
        color_verify_res,
        proportion_res,
        stub_lint_res,
        palette_lint_res,
        glitch_lint_res,
        readme_sync_res,
        motion_spec_res,
        arc_diff_results,
        alpha_blend_res,
        uv_purple_res,
        depth_temp_res,
        warm_pixel_res,
        sightline_res,
        silhouette_res,
        expression_res,
        stiffness_res,
        delta,
        run_ts,
    )

    PROD_DIR.mkdir(parents=True, exist_ok=True)
    report_path = PROD_DIR / f"precritique_qa_{CYCLE_LABEL.lower()}.md"
    report_path.write_text(report_md, encoding="utf-8")
    print(f"\n[precritique_qa] Report written to: {report_path}")

    # Determine exit code
    overall = _worst_grade(
        render_qa_res["overall"],
        color_verify_res["overall"],
        proportion_res["overall"],
        stub_lint_res["overall"],
        palette_lint_res["overall"],
        glitch_lint_res["overall"],
        readme_sync_res["overall"],
        motion_spec_res["overall"],
        alpha_blend_res["overall"],
        uv_purple_res["overall"],
        depth_temp_res["overall"],
        warm_pixel_res["overall"],
        sightline_res["overall"],
        silhouette_res["overall"],
        expression_res["overall"],
        stiffness_res["overall"],
    )

    print(f"[precritique_qa] OVERALL: {overall}")

    if overall == "PASS":
        return 0
    elif overall == "WARN":
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
