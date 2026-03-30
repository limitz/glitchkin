#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_naming_compliance_copier.py
Tool: Naming Convention Compliance Copier — Cycle 12 pass (ENV gaps)
Cycle: 12
Author: Jordan Reed, Background & Environment Artist
Date: 2026-03-29

Creates LTG-compliant copies of remaining ENV legacy-named files:
- glitch_layer_layout.png  → LTG_ENV_glitchlayer_layout.png
- frame01_house_interior.png → LTG_ENV_lumashome_study_interior_v002.png
  (v001 already exists as LTG_ENV_lumashome_study_interior.png — same source, different name origin)
- bg_glitch_layer_encounter.png → LTG_ENV_glitchlayer_encounter.png

Never overwrites — only creates new files.
"""

import shutil
import os

BASE = "/home/wipkat/team/output"

COMPLIANCE_COPIES = [
    # ── ENV LAYOUTS ───────────────────────────────────────────────────────────
    (
        f"{BASE}/backgrounds/environments/layouts/glitch_layer_layout.png",
        f"{BASE}/backgrounds/environments/layouts/LTG_ENV_glitchlayer_layout.png",
    ),
    # ── ENV BACKGROUNDS ───────────────────────────────────────────────────────
    # frame01_house_interior.png — LTG_ENV_lumashome_study_interior.png
    # already exists as a valid LTG copy; v002 would be identical duplicate.
    # Skip to avoid redundant files; v001 is the canonical LTG copy.
    (
        f"{BASE}/backgrounds/environments/bg_glitch_layer_encounter.png",
        f"{BASE}/backgrounds/environments/LTG_ENV_glitchlayer_encounter.png",
    ),
    (
        f"{BASE}/backgrounds/environments/glitch_layer_frame.png",
        f"{BASE}/backgrounds/environments/LTG_ENV_glitchlayer_frame.png",
    ),
]


def main():
    created = []
    skipped = []
    errors = []

    for src, dst in COMPLIANCE_COPIES:
        if not os.path.exists(src):
            errors.append(f"SOURCE MISSING: {src}")
            continue
        if os.path.exists(dst):
            skipped.append(f"ALREADY EXISTS: {dst}")
            continue
        try:
            shutil.copy2(src, dst)
            created.append(f"CREATED: {dst}")
        except Exception as e:
            errors.append(f"ERROR copying {src} -> {dst}: {e}")

    print("\n=== LTG Naming Compliance Copier v002 — Results ===\n")
    for line in created:
        print(f"  [OK]  {line}")
    for line in skipped:
        print(f"  [--]  {line}")
    for line in errors:
        print(f"  [ERR] {line}")

    print(f"\nSummary: {len(created)} created, {len(skipped)} skipped, {len(errors)} errors.")


if __name__ == "__main__":
    main()
