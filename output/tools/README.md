# Tools Index — "Luma & the Glitchkin"

**Maintained by:** Alex Chen, Art Director
**Last updated:** 2026-03-29

---

## Open Source Tools Policy

This production uses **open source tools exclusively**. No proprietary software is permitted at any stage of the pipeline. The approved open source stack is:

| Tool | Role | Notes |
|---|---|---|
| **OpenToonz** | 2D animation | Primary animation tool. Used by Studio Ghibli. |
| **Krita** | Digital painting | Backgrounds, character sheets, color keys, style frames |
| **Inkscape** | Vector graphics | Model sheets, style guides, title cards, SVG assets |
| **Natron** | Compositing | Final composite, color grade, FX assembly |
| **Python + Pillow/PIL** | Image scripting | Batch processing, image generation, pipeline automation |
| **Python + pycairo / svgwrite** | Vector scripting | SVG and vector asset generation |
| **ImageMagick** | CLI image processing | Format conversion, batch resizing, asset pipeline |
| **Git + Git LFS** | Version control | Documents via standard Git; binaries via Git LFS |

**If a required tool does not exist in the open source ecosystem, the team must implement it in Python** and register it in the table below.

---

## Script Index

| Script Name | Created By | Purpose | Dependencies |
|---|---|---|---|
| `color_swatch_generator.py` | Maya Santos / Production | Generates labeled PNG color swatch sheets from hex/name pairs. Reusable CLI + module. | Pillow |
| `proportion_diagram.py` | Maya Santos / Production | Generates character proportion diagrams side-by-side in head-unit scale. | Pillow |
| `silhouette_generator.py` | Maya Santos / Production | Generates solid-black character silhouette sheets for squint-test validation. | Pillow |
| `bg_layout_generator.py` | Jordan Reed / Production | Generates 1920×1080 color-block background layout compositions from zone definitions. Includes Luma's House, Glitch Layer, Millbrook Street scene generators. | Pillow |
| `storyboard_panel_generator.py` | Lee Tanaka / Production | Generates 480×270px storyboard panels with caption bars, shot labels, and drawn scene content. Cycle 5: 7 panels (P01, P03, P07-bridge, P11, P12-bridge, P13, P25) + 2-row contact sheet. P03 fixed: pulse visible. P13 redrawn: 3D spatial staging. | Pillow |
| `luma_face_generator.py` | Maya Santos / Production | Draws Luma's face at 600×600px with asymmetric hair cloud, wide reckless eyes, arched brows, reckless grin, blush, and pixel-pattern hoodie collar. | Pillow |
| `byte_expressions_generator.py` | Alex Chen / Production | Generates 6-expression sheet for Byte using 5×5 pixel grid eye system. Expressions: GRUMPY, SEARCHING, ALARMED, RELUCTANT JOY, CONFUSED, POWERED DOWN. Body color #00D4E8. | Pillow |

---

## Registration Instructions

When a new script is created, add a row to the Script Index above with:
- **Script Name:** filename including extension (e.g. `LTG_TOOL_confetti_emitter_v001.py`)
- **Created By:** team member name
- **Purpose:** one-sentence description of what the script does
- **Dependencies:** Python packages or external tools required (e.g. `Pillow`, `ImageMagick`, `svgwrite`)

Scripts must follow the standard naming convention: `LTG_TOOL_[descriptor]_v[###].[ext]`

All scripts are stored in this directory (`/home/wipkat/team/output/tools/`) and version-controlled via standard Git.
