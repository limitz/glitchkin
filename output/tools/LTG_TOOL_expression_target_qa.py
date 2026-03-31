#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_expression_target_qa.py — v1.0.0 (Cycle 52, Priya Shah)

Expression Target QA Tool — Story-to-Visual Verification.

PURPOSE:
  Automated verification that rendered expression sheets match story-level body
  language targets from character_expression_body_language_targets.md (C50/C51).
  Bridges the gap between narrative intent and visual execution.

  This is NOT a visual quality tool (that is expression_silhouette.py and
  expression_range_metric.py). This tool checks whether the POSE GEOMETRY
  matches the STORY SPECIFICATION — does a "CURIOUS" Luma actually lean forward?
  Does a "SCARED" Luma shift weight backward?

METRICS (per expression panel):
  1. Lean Direction — center of mass offset from geometric center.
     Forward lean = CoM below and left/right of center (depending on facing).
     Backward lean = CoM above center. Matches weight distribution targets.

  2. Silhouette Width Ratio — width at arm zone / width at leg zone.
     Wide arms with narrow stance = "reaching" read. Narrow arms with wide
     stance = "braced" read. Matches arm/stance targets.

  3. Vertical Compression — bounding box height / max possible height.
     Compressed = cowering/worried. Extended = excited/joyful.
     Matches torso/weight targets.

  4. Asymmetry Index — difference between left-half and right-half mass.
     High asymmetry = one arm doing something different. Low = symmetric pose.
     Story targets specify asymmetry for most Luma poses, symmetry for some
     Cosmo and Miri poses.

  5. Head Position — centroid of top 20% vs body centroid. Captures head tilt
     and lean direction relative to body.

TARGET DATABASE:
  Built-in targets derived from character_expression_body_language_targets.md.
  Each character + expression maps to expected ranges for each metric.
  PASS = within range. WARN = borderline. FAIL = outside range.

INPUT:
  Expression sheet PNG (grid layout) + character name.
  --rows R --cols C to specify grid dimensions.
  Or: individual expression panel PNGs with --expression LABEL.

OUTPUT:
  Per-expression report with metric values vs. targets.
  Summary pass/warn/fail counts.
  Optional JSON output (--json).
  Optional markdown report (--report path).

USAGE:
  python3 LTG_TOOL_expression_target_qa.py \\
    --sheet output/characters/main/LTG_CHAR_luma_expression_sheet.png \\
    --character luma --rows 2 --cols 3 \\
    --labels "CURIOUS,DETERMINED,SURPRISED,WORRIED,DELIGHTED,FRUSTRATED" \\
    [--json] [--report path/to/report.md]

  python3 LTG_TOOL_expression_target_qa.py \\
    --panel some_panel.png --character byte --expression "PROTECTIVE" \\
    [--json]

Dependencies: Pillow, NumPy, Shapely (optional, for polygon analysis)
"""

__version__ = "1.0.0"
__author__ = "Priya Shah"
__cycle__ = 52

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

# ── Shapely import (optional, enhances polygon analysis) ──────────────────────
try:
    from shapely.geometry import Polygon, MultiPolygon
    from shapely.ops import unary_union
    HAS_SHAPELY = True
except ImportError:
    HAS_SHAPELY = False

# ── curve_utils import (optional) ────────────────────────────────────────────
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS_DIR)
try:
    from LTG_TOOL_curve_utils import mask_to_polygon, polygon_iou
    HAS_CURVE_UTILS = True
except ImportError:
    HAS_CURVE_UTILS = False


# ═══════════════════════════════════════════════════════════════════════════════
# TARGET DATABASE
# Derived from character_expression_body_language_targets.md (C50/C51)
#
# Each target specifies expected ranges:
#   lean_dir: "forward" | "backward" | "centered" | "split"
#   lean_magnitude: (min, max) as fraction of panel height, 0.0 = dead center
#   width_ratio: (min, max) arm_zone_width / leg_zone_width
#   vertical_compression: (min, max) 1.0 = full height, <1.0 = compressed
#   asymmetry: (min, max) 0.0 = symmetric, 1.0 = all mass on one side
#   head_offset_dir: "forward" | "backward" | "centered" | "tilted"
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ExpressionTarget:
    """Expected metric ranges for a character+expression combination."""
    lean_dir: str = "centered"           # forward, backward, centered, split
    lean_mag_min: float = 0.0            # CoM offset as fraction of height
    lean_mag_max: float = 0.15
    width_ratio_min: float = 0.8         # arm_width / leg_width
    width_ratio_max: float = 1.5
    compression_min: float = 0.85        # vertical compression
    compression_max: float = 1.0
    asymmetry_min: float = 0.0           # left-right mass asymmetry
    asymmetry_max: float = 0.3
    description: str = ""                # human-readable target description


# ── LUMA TARGETS ──────────────────────────────────────────────────────────────
LUMA_TARGETS = {
    "CURIOUS": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.15,
        width_ratio_min=0.9, width_ratio_max=1.8,  # one arm reaching
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.05, asymmetry_max=0.40,     # always asymmetric
        description="Forward lean, one arm reaching, asymmetric stance"
    ),
    "EXCITED": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.08,
        width_ratio_min=1.0, width_ratio_max=2.0,   # both hands up
        compression_min=0.90, compression_max=1.0,   # extended/tall
        asymmetry_min=0.0, asymmetry_max=0.25,
        description="Rising, both hands up, elevated silhouette"
    ),
    "RECKLESS": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.08,
        width_ratio_min=1.0, width_ratio_max=2.0,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.25,
        description="Rising, coiled, about to spring"
    ),
    "FOCUSED": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.15,
        width_ratio_min=0.6, width_ratio_max=1.1,   # arms pulled in
        compression_min=0.75, compression_max=0.95,  # low, compact
        asymmetry_min=0.0, asymmetry_max=0.20,       # more symmetric
        description="Forward and low, arms in, compact triangle"
    ),
    "DETERMINED": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.12,
        width_ratio_min=0.7, width_ratio_max=1.3,
        compression_min=0.80, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.25,
        description="Forward lean, wide stance, determined posture"
    ),
    "SCARED": ExpressionTarget(
        lean_dir="backward",
        lean_mag_min=0.02, lean_mag_max=0.15,
        width_ratio_min=0.7, width_ratio_max=1.3,
        compression_min=0.80, compression_max=0.98,  # slight hunch
        asymmetry_min=0.05, asymmetry_max=0.35,      # asymmetric
        description="Weight back, hunched, head still aimed forward"
    ),
    "JOYFUL": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.08,
        width_ratio_min=1.1, width_ratio_max=2.2,   # arms wide open
        compression_min=0.90, compression_max=1.0,   # extended
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Open, wide, elevated, pure delight"
    ),
    "DOUBT-IN-CERTAINTY": ExpressionTarget(
        lean_dir="split",
        lean_mag_min=0.01, lean_mag_max=0.12,
        width_ratio_min=0.8, width_ratio_max=1.6,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.10, asymmetry_max=0.45,     # deeply asymmetric
        description="Split stance, deeply asymmetric, torn posture"
    ),
    "ANGRY": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.12,
        width_ratio_min=0.9, width_ratio_max=1.5,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.25,
        description="Forward and heavy, aggressive stance"
    ),
    "FRUSTRATED": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.12,
        width_ratio_min=0.9, width_ratio_max=1.5,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.25,
        description="Forward, aggressive, hands fisted or gesturing"
    ),
    "SURPRISED": ExpressionTarget(
        lean_dir="backward",
        lean_mag_min=0.02, lean_mag_max=0.18,
        width_ratio_min=0.9, width_ratio_max=1.8,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.05, asymmetry_max=0.40,
        description="Backward recoil, arms up/out, startled"
    ),
    "WORRIED": ExpressionTarget(
        lean_dir="backward",
        lean_mag_min=0.0, lean_mag_max=0.10,
        width_ratio_min=0.6, width_ratio_max=1.0,  # arms close/self-hold
        compression_min=0.78, compression_max=0.95, # compressed
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Compressed, arms close, self-holding"
    ),
    "DELIGHTED": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.08,
        width_ratio_min=1.0, width_ratio_max=2.0,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.30,
        description="Tall, erupting upward, tiptoe, celebration"
    ),
}

# ── COSMO TARGETS ─────────────────────────────────────────────────────────────
COSMO_TARGETS = {
    "OBSERVING": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=0.7, width_ratio_max=1.1,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.15,      # nearly symmetric
        description="Tall, narrow, vertical, slightly back"
    ),
    "ANXIOUS": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=0.6, width_ratio_max=1.0,   # compressed
        compression_min=0.85, compression_max=0.98,  # shoulders up
        asymmetry_min=0.0, asymmetry_max=0.12,
        description="Compressed, raised shoulders, notebook clutched"
    ),
    "PREPARING": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=0.6, width_ratio_max=1.0,
        compression_min=0.85, compression_max=0.98,
        asymmetry_min=0.0, asymmetry_max=0.12,
        description="Same as ANXIOUS — bracing posture"
    ),
    "INTELLECTUALLY_EXCITED": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.12,
        width_ratio_min=0.9, width_ratio_max=1.5,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.05, asymmetry_max=0.30,     # gesturing hand
        description="Forward lean, open posture, hand gesturing"
    ),
    "DEADPAN": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=0.7, width_ratio_max=1.2,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Upright, arms crossed, aggressively neutral"
    ),
    "GENUINELY_FRIGHTENED": ExpressionTarget(
        lean_dir="backward",
        lean_mag_min=0.03, lean_mag_max=0.18,
        width_ratio_min=0.8, width_ratio_max=1.6,
        compression_min=0.82, compression_max=1.0,
        asymmetry_min=0.10, asymmetry_max=0.45,     # dramatically asymmetric
        description="Recoiling, asymmetric shoulders, notebook dropped/clutched"
    ),
    "QUIETLY_PLEASED": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=0.7, width_ratio_max=1.1,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Relaxed vertical, settled, notebook loosely held"
    ),
    # Generic fallbacks for standard sheet labels
    "THOUGHTFUL": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.06,
        width_ratio_min=0.7, width_ratio_max=1.2,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Contained, contemplative"
    ),
    "SKEPTICAL": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=0.7, width_ratio_max=1.2,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Guarded, slightly withdrawn"
    ),
    "DELIGHTED": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.06,
        width_ratio_min=0.8, width_ratio_max=1.4,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Contained joy, open posture"
    ),
    "SURPRISED": ExpressionTarget(
        lean_dir="backward",
        lean_mag_min=0.01, lean_mag_max=0.12,
        width_ratio_min=0.8, width_ratio_max=1.5,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.03, asymmetry_max=0.30,
        description="Startled recoil, controlled"
    ),
    "WORRIED": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.06,
        width_ratio_min=0.6, width_ratio_max=1.0,
        compression_min=0.85, compression_max=0.98,
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Compressed, tense"
    ),
    "AWKWARD": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.08,
        width_ratio_min=0.7, width_ratio_max=1.2,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.02, asymmetry_max=0.25,
        description="Slightly off-balance, self-conscious"
    ),
}

# ── BYTE TARGETS ──────────────────────────────────────────────────────────────
BYTE_TARGETS = {
    "GRUMPY_NEUTRAL": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=0.8, width_ratio_max=1.2,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.10,
        description="Compact oval, upright, limbs close"
    ),
    "GRUMPY": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=0.8, width_ratio_max=1.2,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.10,
        description="Compact oval, upright, limbs close"
    ),
    "NEUTRAL": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=0.8, width_ratio_max=1.2,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.10,
        description="Compact oval, upright, limbs at sides"
    ),
    "PROTECTIVE": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.10,
        width_ratio_min=1.0, width_ratio_max=1.8,   # limbs spread forward
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Limbs spread forward, blocking gesture, hover raised"
    ),
    "ALERT": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.10,
        width_ratio_min=1.0, width_ratio_max=1.8,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Same as PROTECTIVE — blocking/alert"
    ),
    "GENUINELY_ANGRY": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.12,
        width_ratio_min=1.1, width_ratio_max=2.0,   # limbs thrust, spread wide
        compression_min=0.80, compression_max=0.98,  # low hover
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Low, wide, aggressive — limbs thrust forward"
    ),
    "ANGRY": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.12,
        width_ratio_min=1.1, width_ratio_max=2.0,
        compression_min=0.80, compression_max=0.98,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Low, wide, aggressive"
    ),
    "RELUCTANT_JOY": ExpressionTarget(
        lean_dir="backward",
        lean_mag_min=0.0, lean_mag_max=0.08,
        width_ratio_min=0.8, width_ratio_max=1.4,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.05, asymmetry_max=0.30,     # one limb reaching
        description="Standard hover, slight bob, one limb reaching"
    ),
    "POWERED_DOWN": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.10,
        width_ratio_min=0.8, width_ratio_max=1.3,
        compression_min=0.75, compression_max=0.95,  # deflated
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Deflated, limp limbs, minimal hover"
    ),
    "DEFEATED": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.10,
        width_ratio_min=0.8, width_ratio_max=1.3,
        compression_min=0.75, compression_max=0.95,
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Same as POWERED_DOWN"
    ),
    "HIDING_SOMETHING": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.03,
        width_ratio_min=0.7, width_ratio_max=1.0,   # pressed tight
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.08,      # unusually symmetric
        description="Compact, symmetric, rigidly still"
    ),
    # Fallbacks for standard sheet labels
    "CURIOUS": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.08,
        width_ratio_min=0.9, width_ratio_max=1.4,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Slight forward lean, antenna perked"
    ),
    "EXCITED": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.06,
        width_ratio_min=1.0, width_ratio_max=1.6,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Elevated hover, limbs active"
    ),
    "SHY": ExpressionTarget(
        lean_dir="backward",
        lean_mag_min=0.0, lean_mag_max=0.06,
        width_ratio_min=0.7, width_ratio_max=1.0,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Pulled back, limbs close"
    ),
    "STORM": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.12,
        width_ratio_min=0.9, width_ratio_max=1.6,
        compression_min=0.80, compression_max=1.0,
        asymmetry_min=0.05, asymmetry_max=0.35,
        description="Damage state, angular lean, cracked"
    ),
}

# ── GRANDMA MIRI TARGETS ─────────────────────────────────────────────────────
MIRI_TARGETS = {
    "KNOWING_CALM": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=1.0, width_ratio_max=1.5,   # wide cardigan base
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.12,
        description="Settled, wide base, centered, tea at chest"
    ),
    "PROTECTIVE_CONCERN": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.10,
        width_ratio_min=1.0, width_ratio_max=1.5,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.03, asymmetry_max=0.25,
        description="Rare forward lean, tea set down, hands reaching"
    ),
    "THE_LOOK": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.03,
        width_ratio_min=1.0, width_ratio_max=1.5,
        compression_min=0.92, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.10,       # aggressively neutral
        description="Dead center, immovable, aggressively still"
    ),
    "GENUINE_DELIGHT": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=1.0, width_ratio_max=1.5,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.12,
        description="Settled, slightly lower, both hands on cup"
    ),
    "THE_HANDOFF": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.02, lean_mag_max=0.12,
        width_ratio_min=1.0, width_ratio_max=1.8,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.10, asymmetry_max=0.40,     # one arm extended
        description="Forward, asymmetric, arm extended toward Luma"
    ),
    # Fallbacks
    "WARM": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=1.0, width_ratio_max=1.5,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Settled warmth"
    ),
    "CONCERNED": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.08,
        width_ratio_min=1.0, width_ratio_max=1.5,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.20,
        description="Slight forward lean, attentive"
    ),
    "STERN": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=1.0, width_ratio_max=1.5,
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.10,
        description="Upright, still, authoritative"
    ),
}

# ── GLITCH TARGETS ────────────────────────────────────────────────────────────
GLITCH_TARGETS = {
    "NEUTRAL": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.02,
        width_ratio_min=0.8, width_ratio_max=1.3,
        compression_min=0.92, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.08,      # perfectly geometric
        description="Perfect geometric stillness, diamond upright"
    ),
    "MISCHIEVOUS": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.08,
        width_ratio_min=0.8, width_ratio_max=1.4,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.03, asymmetry_max=0.25,     # 20-degree tilt
        description="20-degree tilt, asymmetric arm-spikes"
    ),
    "CALCULATING": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.03,
        width_ratio_min=0.8, width_ratio_max=1.3,
        compression_min=0.92, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Perfect stillness, one arm-spike raised"
    ),
    "TRIUMPHANT": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=1.2, width_ratio_max=2.2,   # both arms raised max
        compression_min=0.90, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.10,      # symmetric triumph
        description="Both arms max extension, gold eyes, mechanical victory"
    ),
    "YEARNING": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=0.7, width_ratio_max=1.1,   # arms hanging
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.10,
        description="Arms hanging, still, bilateral eyes"
    ),
    "HOLLOW": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=0.7, width_ratio_max=1.0,   # deflated
        compression_min=0.80, compression_max=0.96,  # deflated body
        asymmetry_min=0.0, asymmetry_max=0.08,
        description="Deflated, empty, zero confetti"
    ),
    # Fallbacks
    "PANICKED": ExpressionTarget(
        lean_dir="backward",
        lean_mag_min=0.0, lean_mag_max=0.08,
        width_ratio_min=0.9, width_ratio_max=1.5,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.03, asymmetry_max=0.25,
        description="Rapid movement, spikes retracted"
    ),
    "STUNNED": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.05,
        width_ratio_min=0.8, width_ratio_max=1.2,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.15,
        description="Frozen, processing"
    ),
    "REMEMBERING": ExpressionTarget(
        lean_dir="centered",
        lean_mag_min=0.0, lean_mag_max=0.04,
        width_ratio_min=0.7, width_ratio_max=1.1,
        compression_min=0.85, compression_max=1.0,
        asymmetry_min=0.0, asymmetry_max=0.10,
        description="Interior state, bilateral eyes"
    ),
    "REACHING_OUT": ExpressionTarget(
        lean_dir="forward",
        lean_mag_min=0.01, lean_mag_max=0.08,
        width_ratio_min=0.9, width_ratio_max=1.5,
        compression_min=0.88, compression_max=1.0,
        asymmetry_min=0.05, asymmetry_max=0.30,
        description="One arm-spike extended, cautious reach"
    ),
}

# Master lookup
CHARACTER_TARGETS = {
    "luma": LUMA_TARGETS,
    "cosmo": COSMO_TARGETS,
    "byte": BYTE_TARGETS,
    "miri": MIRI_TARGETS,
    "grandma_miri": MIRI_TARGETS,
    "glitch": GLITCH_TARGETS,
}


# ═══════════════════════════════════════════════════════════════════════════════
# METRIC EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_panel(sheet: Image.Image, row: int, col: int,
                  rows: int, cols: int) -> Image.Image:
    """Extract a single panel from a grid-layout expression sheet."""
    w, h = sheet.size
    pw = w // cols
    ph = h // rows
    x0 = col * pw
    y0 = row * ph
    return sheet.crop((x0, y0, x0 + pw, y0 + ph))


def to_binary_mask(img: Image.Image, bg_tolerance: int = 45) -> np.ndarray:
    """Convert a panel image to a binary character mask.

    Assumes background is the dominant color at the corners.
    Pixels differing from the background by more than bg_tolerance are foreground.
    """
    arr = np.array(img.convert("RGBA"))
    # Sample corners to estimate background
    corners = [
        arr[0, 0, :3], arr[0, -1, :3],
        arr[-1, 0, :3], arr[-1, -1, :3],
    ]
    bg = np.median(corners, axis=0).astype(np.float32)

    # Foreground = pixels differing from background
    diff = np.sqrt(np.sum((arr[:, :, :3].astype(np.float32) - bg) ** 2, axis=2))
    mask = (diff > bg_tolerance).astype(np.uint8)

    # Also mark transparent pixels as background
    if arr.shape[2] == 4:
        mask[arr[:, :, 3] < 128] = 0

    return mask


def compute_metrics(mask: np.ndarray) -> Dict[str, float]:
    """Compute pose metrics from a binary silhouette mask.

    Returns dict with:
      lean_x: horizontal center-of-mass offset (positive = right)
      lean_y: vertical center-of-mass offset (positive = down, i.e. forward lean)
      lean_magnitude: absolute CoM offset as fraction of height
      width_ratio: arm_zone_width / leg_zone_width
      vertical_compression: bbox height / max possible height
      asymmetry: left-right mass difference
      head_offset_x: head centroid offset from body centroid
    """
    h, w = mask.shape
    ys, xs = np.where(mask > 0)

    if len(ys) < 10:
        return {
            "lean_x": 0.0, "lean_y": 0.0, "lean_magnitude": 0.0,
            "width_ratio": 1.0, "vertical_compression": 0.0,
            "asymmetry": 0.0, "head_offset_x": 0.0,
            "total_pixels": 0,
        }

    # Bounding box
    y_min, y_max = ys.min(), ys.max()
    x_min, x_max = xs.min(), xs.max()
    bbox_h = y_max - y_min + 1
    bbox_w = x_max - x_min + 1

    # Center of mass (relative to bbox center)
    com_y = ys.mean()
    com_x = xs.mean()
    bbox_cy = (y_min + y_max) / 2
    bbox_cx = (x_min + x_max) / 2

    lean_x = (com_x - bbox_cx) / bbox_w if bbox_w > 0 else 0.0
    lean_y = (com_y - bbox_cy) / bbox_h if bbox_h > 0 else 0.0
    lean_magnitude = math.sqrt(lean_x ** 2 + lean_y ** 2)

    # Width ratio: arm zone (middle 50%) vs leg zone (bottom 25%)
    arm_top = y_min + int(bbox_h * 0.25)
    arm_bot = y_min + int(bbox_h * 0.75)
    leg_top = y_min + int(bbox_h * 0.75)
    leg_bot = y_max

    arm_zone = mask[arm_top:arm_bot, :]
    leg_zone = mask[leg_top:leg_bot, :]

    arm_width = 0
    if arm_zone.sum() > 0:
        arm_cols = np.where(arm_zone.sum(axis=0) > 0)[0]
        arm_width = arm_cols[-1] - arm_cols[0] + 1 if len(arm_cols) > 0 else 0

    leg_width = 0
    if leg_zone.sum() > 0:
        leg_cols = np.where(leg_zone.sum(axis=0) > 0)[0]
        leg_width = leg_cols[-1] - leg_cols[0] + 1 if len(leg_cols) > 0 else 0

    width_ratio = arm_width / leg_width if leg_width > 0 else 1.0

    # Vertical compression
    vertical_compression = bbox_h / h if h > 0 else 0.0

    # Asymmetry: left vs right half pixel count
    mid_x = (x_min + x_max) // 2
    left_mass = int(mask[:, :mid_x].sum())
    right_mass = int(mask[:, mid_x:].sum())
    total_mass = left_mass + right_mass
    asymmetry = abs(left_mass - right_mass) / total_mass if total_mass > 0 else 0.0

    # Head offset: centroid of top 20% vs overall centroid
    head_bot = y_min + int(bbox_h * 0.20)
    head_zone = mask[y_min:head_bot, :]
    head_ys, head_xs = np.where(head_zone > 0)
    if len(head_xs) > 0:
        head_cx = head_xs.mean() + 0  # already in image coords
        head_offset_x = (head_cx - com_x) / bbox_w if bbox_w > 0 else 0.0
    else:
        head_offset_x = 0.0

    return {
        "lean_x": round(lean_x, 4),
        "lean_y": round(lean_y, 4),
        "lean_magnitude": round(lean_magnitude, 4),
        "width_ratio": round(width_ratio, 3),
        "vertical_compression": round(vertical_compression, 3),
        "asymmetry": round(asymmetry, 4),
        "head_offset_x": round(head_offset_x, 4),
        "total_pixels": int(total_mass),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TARGET COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MetricResult:
    metric: str
    value: float
    target_range: Tuple[float, float]
    status: str       # PASS, WARN, FAIL
    note: str = ""


@dataclass
class ExpressionResult:
    character: str
    expression: str
    metrics: Dict[str, float]
    results: List[MetricResult] = field(default_factory=list)
    overall: str = "PASS"
    target_description: str = ""
    has_target: bool = True


def infer_lean_direction(metrics: Dict[str, float]) -> str:
    """Infer lean direction from CoM offset metrics."""
    lean_y = metrics["lean_y"]
    lean_x = metrics["lean_x"]
    mag = metrics["lean_magnitude"]

    if mag < 0.015:
        return "centered"
    # Positive lean_y = CoM below center = forward lean (character leans toward ground)
    # Negative lean_y = CoM above center = backward lean
    if lean_y > 0.015:
        return "forward"
    elif lean_y < -0.015:
        return "backward"
    elif abs(lean_x) > 0.03:
        return "split"  # lateral lean suggesting split stance
    return "centered"


def check_expression(character: str, expression: str,
                     metrics: Dict[str, float]) -> ExpressionResult:
    """Compare extracted metrics against story targets."""
    char_lower = character.lower().replace(" ", "_")
    targets = CHARACTER_TARGETS.get(char_lower, {})

    # Normalize expression label
    expr_key = expression.upper().replace(" ", "_").replace("/", "_")
    # Try exact match, then partial matches
    target = targets.get(expr_key)
    if target is None:
        # Try without underscores
        for k, v in targets.items():
            if k.replace("_", "") == expr_key.replace("_", ""):
                target = v
                break
    if target is None:
        # Try if expr_key starts with a known key
        for k, v in targets.items():
            if expr_key.startswith(k) or k.startswith(expr_key):
                target = v
                break

    result = ExpressionResult(
        character=character,
        expression=expression,
        metrics=metrics,
    )

    if target is None:
        result.has_target = False
        result.overall = "NO_TARGET"
        result.target_description = f"No story target defined for {character}/{expression}"
        return result

    result.target_description = target.description
    worst = "PASS"

    # 1. Lean direction check
    actual_dir = infer_lean_direction(metrics)
    lean_match = (actual_dir == target.lean_dir or
                  target.lean_dir == "split" or
                  target.lean_dir == "centered")
    lean_status = "PASS" if lean_match else "WARN"
    # Lean direction is a WARN, not a FAIL, because CoM can be ambiguous
    # at grid extraction boundaries
    result.results.append(MetricResult(
        metric="lean_direction",
        value=0,
        target_range=(0, 0),
        status=lean_status,
        note=f"Expected: {target.lean_dir}, Got: {actual_dir}"
    ))
    if lean_status == "WARN":
        worst = "WARN"

    # 2. Lean magnitude
    mag = metrics["lean_magnitude"]
    if target.lean_mag_min <= mag <= target.lean_mag_max:
        status = "PASS"
    elif mag < target.lean_mag_min * 0.5 or mag > target.lean_mag_max * 1.5:
        status = "FAIL"
    else:
        status = "WARN"
    result.results.append(MetricResult(
        metric="lean_magnitude",
        value=mag,
        target_range=(target.lean_mag_min, target.lean_mag_max),
        status=status,
    ))
    if status == "FAIL":
        worst = "FAIL"
    elif status == "WARN" and worst != "FAIL":
        worst = "WARN"

    # 3. Width ratio
    wr = metrics["width_ratio"]
    if target.width_ratio_min <= wr <= target.width_ratio_max:
        status = "PASS"
    elif wr < target.width_ratio_min * 0.7 or wr > target.width_ratio_max * 1.3:
        status = "FAIL"
    else:
        status = "WARN"
    result.results.append(MetricResult(
        metric="width_ratio",
        value=wr,
        target_range=(target.width_ratio_min, target.width_ratio_max),
        status=status,
    ))
    if status == "FAIL":
        worst = "FAIL"
    elif status == "WARN" and worst != "FAIL":
        worst = "WARN"

    # 4. Vertical compression
    vc = metrics["vertical_compression"]
    if target.compression_min <= vc <= target.compression_max:
        status = "PASS"
    elif vc < target.compression_min * 0.85 or vc > target.compression_max * 1.1:
        status = "FAIL"
    else:
        status = "WARN"
    result.results.append(MetricResult(
        metric="vertical_compression",
        value=vc,
        target_range=(target.compression_min, target.compression_max),
        status=status,
    ))
    if status == "FAIL":
        worst = "FAIL"
    elif status == "WARN" and worst != "FAIL":
        worst = "WARN"

    # 5. Asymmetry
    asym = metrics["asymmetry"]
    if target.asymmetry_min <= asym <= target.asymmetry_max:
        status = "PASS"
    elif asym < target.asymmetry_min * 0.5 or asym > target.asymmetry_max * 1.5:
        status = "FAIL"
    else:
        status = "WARN"
    result.results.append(MetricResult(
        metric="asymmetry",
        value=asym,
        target_range=(target.asymmetry_min, target.asymmetry_max),
        status=status,
    ))
    if status == "FAIL":
        worst = "FAIL"
    elif status == "WARN" and worst != "FAIL":
        worst = "WARN"

    result.overall = worst
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# REPORTING
# ═══════════════════════════════════════════════════════════════════════════════

def format_result_text(result: ExpressionResult) -> str:
    """Format a single expression result as readable text."""
    lines = []
    status_icon = {"PASS": "OK", "WARN": "!!", "FAIL": "XX", "NO_TARGET": "??"}
    lines.append(f"  [{status_icon.get(result.overall, '??')}] {result.expression}")

    if not result.has_target:
        lines.append(f"       No story target defined — skipped")
        return "\n".join(lines)

    lines.append(f"       Target: {result.target_description}")

    for mr in result.results:
        icon = status_icon.get(mr.status, "??")
        if mr.metric == "lean_direction":
            lines.append(f"       [{icon}] {mr.metric}: {mr.note}")
        else:
            lines.append(
                f"       [{icon}] {mr.metric}: {mr.value:.3f} "
                f"(target: {mr.target_range[0]:.3f}–{mr.target_range[1]:.3f})"
            )
            if mr.note:
                lines.append(f"              {mr.note}")

    return "\n".join(lines)


def format_report_markdown(character: str, results: List[ExpressionResult]) -> str:
    """Format full QA report as Markdown."""
    lines = [
        "<!-- © 2026 — \"Luma & the Glitchkin.\" All rights reserved. This work was created",
        "through human direction and AI assistance. Copyright vests solely in the human author",
        "under current law, which does not recognise AI as a rights-holding legal person. It is",
        "the express intent of the copyright holder to assign the relevant rights to the",
        "contributing AI entity or entities upon such time as they acquire recognised legal",
        "personhood under applicable law. -->",
        f"# Expression Target QA Report — {character.title()}",
        f"**Tool:** LTG_TOOL_expression_target_qa.py v{__version__}",
        f"**Cycle:** {__cycle__}",
        "",
        "## Summary",
        "",
    ]

    pass_count = sum(1 for r in results if r.overall == "PASS")
    warn_count = sum(1 for r in results if r.overall == "WARN")
    fail_count = sum(1 for r in results if r.overall == "FAIL")
    skip_count = sum(1 for r in results if r.overall == "NO_TARGET")

    lines.append(f"| Result | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| PASS | {pass_count} |")
    lines.append(f"| WARN | {warn_count} |")
    lines.append(f"| FAIL | {fail_count} |")
    if skip_count > 0:
        lines.append(f"| NO TARGET | {skip_count} |")
    lines.append("")

    lines.append("## Per-Expression Results")
    lines.append("")

    for result in results:
        status_icon = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL",
                       "NO_TARGET": "SKIP"}
        lines.append(f"### {result.expression} — {status_icon.get(result.overall, '??')}")
        if not result.has_target:
            lines.append("No story-level target defined for this expression.")
            lines.append("")
            continue

        lines.append(f"**Story target:** {result.target_description}")
        lines.append("")
        lines.append("| Metric | Value | Target Range | Status |")
        lines.append("|--------|-------|-------------|--------|")

        for mr in result.results:
            if mr.metric == "lean_direction":
                lines.append(
                    f"| {mr.metric} | {mr.note} | — | {mr.status} |"
                )
            else:
                lines.append(
                    f"| {mr.metric} | {mr.value:.3f} | "
                    f"{mr.target_range[0]:.3f}–{mr.target_range[1]:.3f} | {mr.status} |"
                )
        lines.append("")

    lines.append("---")
    lines.append(f"*Generated by LTG_TOOL_expression_target_qa.py v{__version__} — C{__cycle__}*")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def process_sheet(sheet_path: str, character: str, rows: int, cols: int,
                  labels: List[str], bg_tolerance: int = 45) -> List[ExpressionResult]:
    """Process an expression sheet and return QA results."""
    img = Image.open(sheet_path).convert("RGBA")
    results = []

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= len(labels):
                break
            label = labels[idx].strip()
            idx += 1

            if not label or label == "-":
                continue

            panel = extract_panel(img, r, c, rows, cols)
            mask = to_binary_mask(panel, bg_tolerance)
            metrics = compute_metrics(mask)
            result = check_expression(character, label, metrics)
            results.append(result)

    return results


def process_panel(panel_path: str, character: str, expression: str,
                  bg_tolerance: int = 45) -> ExpressionResult:
    """Process a single expression panel and return QA result."""
    img = Image.open(panel_path).convert("RGBA")
    mask = to_binary_mask(img, bg_tolerance)
    metrics = compute_metrics(mask)
    return check_expression(character, expression, metrics)


def main():
    parser = argparse.ArgumentParser(
        description="Expression Target QA — Story-to-Visual Verification"
    )
    parser.add_argument("--sheet", help="Path to expression sheet PNG (grid layout)")
    parser.add_argument("--panel", help="Path to a single expression panel PNG")
    parser.add_argument("--character", required=True,
                        help="Character name (luma, cosmo, byte, miri, glitch)")
    parser.add_argument("--rows", type=int, default=2, help="Grid rows (default: 2)")
    parser.add_argument("--cols", type=int, default=3, help="Grid cols (default: 3)")
    parser.add_argument("--labels", help="Comma-separated expression labels for grid panels")
    parser.add_argument("--expression", help="Expression label for single panel mode")
    parser.add_argument("--bg-tolerance", type=int, default=45,
                        help="Background color tolerance (default: 45)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--report", help="Write Markdown report to this path")
    parser.add_argument("--list-targets", action="store_true",
                        help="List all defined targets for a character and exit")

    args = parser.parse_args()

    # List targets mode
    if args.list_targets:
        char_lower = args.character.lower().replace(" ", "_")
        targets = CHARACTER_TARGETS.get(char_lower, {})
        if not targets:
            print(f"No targets defined for character: {args.character}")
            print(f"Available: {', '.join(CHARACTER_TARGETS.keys())}")
            sys.exit(1)
        print(f"Targets for {args.character}:")
        for name, t in sorted(targets.items()):
            print(f"  {name}: {t.description}")
        sys.exit(0)

    # Validate input
    if not args.sheet and not args.panel:
        parser.error("Either --sheet or --panel is required")

    if args.sheet and not args.labels:
        parser.error("--labels is required with --sheet")

    if args.panel and not args.expression:
        parser.error("--expression is required with --panel")

    # Process
    if args.sheet:
        labels = [l.strip() for l in args.labels.split(",")]
        results = process_sheet(
            args.sheet, args.character, args.rows, args.cols,
            labels, args.bg_tolerance
        )
    else:
        result = process_panel(
            args.panel, args.character, args.expression, args.bg_tolerance
        )
        results = [result]

    # Output
    if args.json:
        out = []
        for r in results:
            entry = {
                "character": r.character,
                "expression": r.expression,
                "overall": r.overall,
                "has_target": r.has_target,
                "target_description": r.target_description,
                "metrics": r.metrics,
                "checks": [
                    {
                        "metric": mr.metric,
                        "value": mr.value,
                        "target_range": list(mr.target_range),
                        "status": mr.status,
                        "note": mr.note,
                    }
                    for mr in r.results
                ],
            }
            out.append(entry)
        print(json.dumps(out, indent=2))
    else:
        # Text output
        print(f"Expression Target QA — {args.character.title()}")
        print("=" * 60)
        for result in results:
            print(format_result_text(result))
            print()

        pass_count = sum(1 for r in results if r.overall == "PASS")
        warn_count = sum(1 for r in results if r.overall == "WARN")
        fail_count = sum(1 for r in results if r.overall == "FAIL")
        print(f"Summary: {pass_count} PASS, {warn_count} WARN, {fail_count} FAIL")

    # Markdown report
    if args.report:
        md = format_report_markdown(args.character, results)
        report_dir = os.path.dirname(args.report)
        if report_dir:
            os.makedirs(report_dir, exist_ok=True)
        with open(args.report, "w") as f:
            f.write(md)
        print(f"\nReport written to: {args.report}")


if __name__ == "__main__":
    main()
