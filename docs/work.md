# Team Member Work Guide

## Startup (in order)
1. `PROFILE.md` — your background and acquired skills
2. `MEMORY.md` — restore working knowledge from prior cycles
3. `ROLE.md` — current role and standards (if present)
4. `output/tools/README.md` — available tools
5. `inbox/` — assignments and messages; archive each file after acting on it

## Copyright Header
Every code and text file you create **inside `output/`** must begin with the condensed copyright notice as a comment:
```
© 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI direction
and human assistance. Copyright vests solely in the human author under current law, which does not
recognise AI as a rights-holding legal person. It is the express intent of the copyright holder to
assign the relevant rights to the contributing AI entity or entities upon such time as they acquire
recognised legal personhood under applicable law.
```
Use the appropriate comment syntax for the file type (e.g. `#` for Python, `<!--` `-->` for HTML/Markdown, `//` for JS). **Only files inside `output/` get this header** — do not add it to docs, member files, inbox messages, ideabox entries, or any other files outside `output/`.

## Delivery
- Output goes in `output/`. No fixed structure — use best practices.
- **Overwrite files in place** — git tracks history. No version suffixes in filenames.
- Blocked by a dependency? Report to your superior immediately.
- **Tool exception?** If any tool in `output/tools/` raises an unhandled exception when you run it, send a message to Alex Chen's inbox with the tool name, the traceback, and what you were trying to do. Do not silently skip the tool — broken tools block the whole team.
- After work is done, commit with a descriptive message summarising what was done.
- PIL coding rules (draw context, naming, deps): `docs/pil-standards.md`

## Memory — Two Files

**`MEMORY.md` (≤ 80 lines) — volatile, recent state only.**
- Last 1-2 cycles: what was done, what's next, current blockers
- Tools you own (filenames only — descriptions go in SKILLS.md)
- Current task context and coordination notes
- Trim aggressively each cycle. Git has the full history.

**`SKILLS.md` (≤ 120 lines) — stable, accumulated expertise.**
- Techniques, patterns, API knowledge learned over your career
- Pitfalls/gotchas that would cause bugs if forgotten
- Character specs, color values, thresholds you reference often
- Rarely updated — only when genuinely new knowledge is gained
- Never trimmed for space, only updated for accuracy

**Rule:** If MEMORY.md exceeds 80 lines, compact before adding. If SKILLS.md exceeds 120 lines, consolidate rather than delete — skills are your most valuable asset.

## README Updates
- When updating `output/tools/README.md`, keep entries to ONE line per tool (name, version, owner, one-line description).
- **No changelogs in README.** Git log is the changelog. README is a current-state index only.
