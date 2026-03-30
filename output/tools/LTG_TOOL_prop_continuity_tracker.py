#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_prop_continuity_tracker.py
Prop Continuity Tracker — Cold Open Pilot Episode
Diego Vargas, Storyboard Artist — Cycle 47

Tracks key props across storyboard panels to prevent continuity errors.
Each prop has a presence map (which panels it appears in, where in the frame,
and what state it should be in).

Usage:
  python LTG_TOOL_prop_continuity_tracker.py                 # print full report
  python LTG_TOOL_prop_continuity_tracker.py --prop notebook  # single prop
  python LTG_TOOL_prop_continuity_tracker.py --panel P18      # single panel
  python LTG_TOOL_prop_continuity_tracker.py --gaps           # show gaps only
  python LTG_TOOL_prop_continuity_tracker.py --save           # save report to output/production/

Output: report to stdout and optionally to output/production/prop_continuity_report.md
"""

import os, sys, json
from datetime import datetime

OUTPUT_DIR = "/home/wipkat/team/output/production"
REPORT_PATH = os.path.join(OUTPUT_DIR, "prop_continuity_report_c47.md")

# ══════════════════════════════════════════════════════════════════════════════
# PROP REGISTRY
# Each prop has:
#   - name: canonical name
#   - first_appearance: panel where it first appears
#   - panels: dict of panel -> {location, state, notes}
#   - continuity_rules: list of rules that must hold across appearances
# ══════════════════════════════════════════════════════════════════════════════

PROP_REGISTRY = {
    "notebook": {
        "name": "Luma's Notebook",
        "description": "Standard composition notebook. Spiral-bound, ruled lines, red margin line.",
        "first_appearance": "P02",
        "panels": {
            "P02": {
                "location": "on couch / near sleeping Luma",
                "state": "closed, visible among snacks",
                "notes": "Establishes notebook location before cold open begins."
            },
            "P18": {
                "location": "fills frame (INSERT shot)",
                "state": "OPEN — page with doodle drawings visible",
                "notes": "Hero prop shot. Processing beat. Spiral binding, ruled lines."
            },
            "P19": {
                "location": "in Luma's lap",
                "state": "OPEN — tiny doodle marks visible as callback to P18",
                "notes": "Prop continuity: she was showing Byte the notebook."
            },
            "P20": {
                "location": "in Luma's lap, pencil in hand",
                "state": "OPEN — tiny marks visible, pencil resting",
                "notes": "Callback to P18. She's still holding it through the naming beat."
            },
        },
        "continuity_rules": [
            "Notebook must be CLOSED before P18 (she hasn't shown it yet).",
            "Notebook must be OPEN in P18, P19, P20 (she opened it to show Byte).",
            "Spiral binding always on LEFT edge of open page.",
            "Red margin line always visible when page is shown.",
            "Pencil present in P18 (on page), P19 (in hand), P20 (in hand).",
        ],
        "missing_panels": [
            "P15-P17: notebook location during ricochet/stillness is implicit (on floor nearby).",
        ],
    },

    "pencil": {
        "name": "Luma's Pencil",
        "description": "Yellow pencil with pink eraser. Her drawing instrument.",
        "first_appearance": "P18",
        "panels": {
            "P18": {
                "location": "resting diagonal on notebook page",
                "state": "yellow body, dark tip, pink eraser end",
                "notes": "On the page — she was just drawing."
            },
            "P19": {
                "location": "in Luma's right hand",
                "state": "held, pointing at notebook",
                "notes": "She picked it up — still engaged with the notebook."
            },
            "P20": {
                "location": "in Luma's right hand",
                "state": "held near notebook",
                "notes": "Continuous hold."
            },
        },
        "continuity_rules": [
            "Yellow body with dark graphite tip — consistent across all appearances.",
            "If notebook is present, pencil should be present (they are a pair).",
        ],
        "missing_panels": [],
    },

    "crt_hero": {
        "name": "Hero CRT Television",
        "description": "Grandma's old CRT TV. The portal. Key story prop.",
        "first_appearance": "P03",
        "panels": {
            "P03": {
                "location": "fills frame (CU shot)",
                "state": "static with single ELEC_CYAN pixel lower-right",
                "notes": "First Glitch Palette moment. One pixel only."
            },
            "P04": {
                "location": "background center",
                "state": "cyan bleeding beyond screen edges",
                "notes": "Contamination begins."
            },
            "P06": {
                "location": "fills frame (CU screen)",
                "state": "Byte's face pressed against glass from inside",
                "notes": "First appearance of Byte."
            },
            "P07": {
                "location": "center frame",
                "state": "bulging, distortion rings, Byte phasing through",
                "notes": "The breach."
            },
            "P09": {
                "location": "BG right, defocused",
                "state": "returning to static (breach was Byte-specific)",
                "notes": "Post-breach. Static normalizing."
            },
            "P12": {
                "location": "camera-right BG",
                "state": "normal static",
                "notes": "Background element."
            },
            "P13": {
                "location": "camera-right BG",
                "state": "normal static, faint glow",
                "notes": "Background element — glow provides directional cyan."
            },
            "P17": {
                "location": "BG behind Byte",
                "state": "gray-green static (normal)",
                "notes": "Room settled. CRT back to normal."
            },
            "P20": {
                "location": "BG right monitors",
                "state": "gray-green static (normal)",
                "notes": "Settled."
            },
            "P21": {
                "location": "part of monitor wall",
                "state": "ALL MONITORS BLAZING — Glitchkin pressing through",
                "notes": "Second crisis. CRT is one of many now."
            },
            "P23": {
                "location": "monitor wall ahead of Luma+Byte",
                "state": "blazing, Glitchkin visible",
                "notes": "Promise shot — both facing the chaos."
            },
            "P24": {
                "location": "part of breached monitor wall",
                "state": "multiple breaches, Glitchkin pouring through",
                "notes": "Chaos apex."
            },
        },
        "continuity_rules": [
            "P01-P03: CRT NOT visible (exterior / establishing only).",
            "P03-P06: CRT shows progressive glitch contamination (pixel → cluster → face).",
            "P07: CRT physically deforms during breach.",
            "P08-P17: CRT returns to NORMAL static (breach was Byte-specific event).",
            "P21+: ALL monitors blaze (not just hero CRT) — escalation from single to swarm.",
        ],
        "missing_panels": [
            "P10-P11: ECU/OTS shots — CRT glow is AMBIENT only (not a visible prop).",
            "P14-P16: Chaos panels — CRT out of frame (action is happening elsewhere).",
        ],
    },

    "pixel_confetti": {
        "name": "Pixel Confetti",
        "description": "ELEC_CYAN irregular polygons (4-7 sides). Residue from breach.",
        "first_appearance": "P07",
        "panels": {
            "P07": {
                "location": "burst from breach point",
                "state": "dense, directional (outward from screen)",
                "notes": "Confetti escapes at hand-press contact points."
            },
            "P08": {
                "location": "drifting around Byte",
                "state": "settling, still directional from breach",
                "notes": "Post-breach scatter."
            },
            "P09": {
                "location": "drifting, sparse",
                "state": "falling DOWN (Byte floats, confetti falls = gravity joke)",
                "notes": "Gravity ghost — confetti obeys physics, Byte doesn't."
            },
            "P14": {
                "location": "scatter from ricochet",
                "state": "28 particles, TENSE density",
                "notes": "Ricochet debris."
            },
            "P15": {
                "location": "drifting down from Byte off-panel right",
                "state": "falling, sparse",
                "notes": "Residual."
            },
            "P17": {
                "location": "single chip falling between Luma and Byte",
                "state": "ONE 6x6px square + descent line",
                "notes": "The chip that breaks the stillness."
            },
            "P20": {
                "location": "3-4 pieces falling",
                "state": "very sparse, last of the breach",
                "notes": "Dying down."
            },
            "P21": {
                "location": "FULL DENSITY RETURN (30+ particles)",
                "state": "dense, multi-color (cyan + magenta)",
                "notes": "Second crisis — confetti erupts again from all monitors."
            },
            "P24": {
                "location": "220 pieces — maximum density",
                "state": "chaos swarm, multi-directional",
                "notes": "Chaos apex."
            },
        },
        "continuity_rules": [
            "Density arc: burst (P07) > settling (P08-P09) > ricochet (P14-P15) > single chip (P17) > dying (P20) > FULL RETURN (P21+).",
            "Always irregular polygons, 4-7 sides. NEVER rectangles (Cycle 11 standard).",
            "Color: ELEC_CYAN dominant. HOT_MAGENTA added only in P21+ escalation.",
            "Gravity: confetti FALLS (obeys physics). Byte floats (doesn't).",
        ],
        "missing_panels": [],
    },

    "hoodie": {
        "name": "Luma's Hoodie",
        "description": "Canonical orange LUMA_HOODIE = (232, 112, 58) = #E8703A.",
        "first_appearance": "P01",
        "panels": {},  # present in every Luma panel — not tracked per-panel
        "continuity_rules": [
            "ALWAYS (232, 112, 58) — CANONICAL ORANGE. Never slate blue, never wrong.",
            "A-line silhouette. Pocket bump on asymmetric hook side.",
            "In P21 flooded room: hoodie is the ONLY warm element. Key visual contrast.",
        ],
        "missing_panels": [],
    },
}


def build_report(prop_filter=None, panel_filter=None, gaps_only=False):
    """Build a text report of prop continuity status."""
    lines = []
    lines.append("# Prop Continuity Report — Cold Open Pilot Episode")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')} (Cycle 47)")
    lines.append("")

    for prop_id, prop in PROP_REGISTRY.items():
        if prop_filter and prop_filter.lower() not in prop_id.lower():
            continue

        lines.append(f"## {prop['name']}")
        lines.append(f"*{prop['description']}*")
        lines.append(f"**First appearance:** {prop['first_appearance']}")
        lines.append("")

        if panel_filter:
            # Show only the specified panel
            pdata = prop["panels"].get(panel_filter.upper())
            if pdata:
                lines.append(f"### {panel_filter.upper()}")
                lines.append(f"- **Location:** {pdata['location']}")
                lines.append(f"- **State:** {pdata['state']}")
                lines.append(f"- **Notes:** {pdata['notes']}")
                lines.append("")
        elif not gaps_only:
            if prop["panels"]:
                lines.append("| Panel | Location | State |")
                lines.append("|-------|----------|-------|")
                for panel, pdata in sorted(prop["panels"].items(),
                                            key=lambda x: int(''.join(filter(str.isdigit, x[0])) or '0')):
                    lines.append(f"| {panel} | {pdata['location']} | {pdata['state']} |")
                lines.append("")

        # Continuity rules
        if not gaps_only:
            lines.append("**Continuity Rules:**")
            for rule in prop["continuity_rules"]:
                lines.append(f"- {rule}")
            lines.append("")

        # Gaps / missing
        if prop["missing_panels"]:
            lines.append("**Known Gaps:**")
            for gap in prop["missing_panels"]:
                lines.append(f"- {gap}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    prop_filter = None
    panel_filter = None
    gaps_only = False
    save = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--prop" and i + 1 < len(args):
            prop_filter = args[i + 1]
            i += 2
        elif args[i] == "--panel" and i + 1 < len(args):
            panel_filter = args[i + 1]
            i += 2
        elif args[i] == "--gaps":
            gaps_only = True
            i += 1
        elif args[i] == "--save":
            save = True
            i += 1
        else:
            i += 1

    report = build_report(prop_filter, panel_filter, gaps_only)
    print(report)

    if save:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(REPORT_PATH, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
