# Maya Santos — Memory

## Cycle 61 — Human feedback head/body polish — COMPLETE

### 6 fixes from inbox (all archived):

**Fix 1 — Shoulders too broad**
- Reduced sh_w in ALL views: front 0.95→0.75, 3q 0.70→0.58, side/side_l 0.50→0.40, back 0.90→0.75
- w_bot front 0.62→0.50
- Affects arm attachment (arms still hang from shoulder edge — checked visually)

**Fix 2 — Hair sharp edges at ear area**
- Side/side_l: replaced (-0.85,0.02,0.30,0.32) and (-0.60,0.08,0.35,0.30) blobs with
  smaller progressively-tapering blobs near ear zone (0.22→0.16→0.12 radii)
- Gradual taper prevents hard cut at face-skin edge

**Fix 3 — Neck-face transition too abrupt**
- Extended face skin overdraw ry in all views:
  - side/side_l: ry 0.80→0.88, cy 0.08→0.10
  - front: ry 0.70→0.85 (with cy=0.10)
  - 3/4: ry 0.70→0.85 (with cy=0.10)
- Bottom of face skin now reaches neck_top_y at +0.95*head_r, covering the seam

**Fix 4 — Forehead/face shape wrong in 3/4 and side**
- Side-R head loop: added brow ridge protrusion `cos(angle - (-pi/6))^12 * 0.06 * head_r`
- Side-L head loop: added brow ridge protrusion `cos(angle - (pi+pi/6))^12 * 0.06 * head_r`
- 3/4 head loop: added far-side brow bump `cos(angle - (-pi/5))^10 * 0.04 * head_r`
- Gives heads proper forward-leaning forehead silhouette in profile/3q views

**Fix 5 — Nose looks stuck on**
- Side-R/side-L: changed from fill_preserve+stroke_full_path to:
  1. fill() the full closed nose shape (skin color, no seam)
  2. new_path stroke ONLY the outer free arc (start/end shifted inward from face edge)
- This removes the outline where nose meets face, making it read as growing from face

**Fix 6 — Eyebrows hidden in hair**
- Draw order was already correct (hair → face skin → eyes → brows)
- Extended face skin ry (fix 3) ensures brow positions at ~-0.32*head_r are well within face skin
- Brow y positions unchanged — they are on the face skin area

**Test:** char_module_test PASS (7/7 Luma). Turnaround regenerated.
**Version:** LTG_TOOL_char_luma.py v1.4.0

**Deliverables:**
- `LTG_TOOL_char_luma.py` v1.4.0 (in-place)
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` (1280x560) — regenerated
- `output/tools/LTG_TOOL_luma_canonical_test.py` v1.0.0 — NEW: 7-expr front-view test sheet
- `output/characters/main/LTG_CHAR_luma_canonical_test.png` (1160x888) — regenerated

## Cycle 60 — Arm draw order + pants/torso join — COMPLETE
- Arm draw order fixed (far arm first) in all 3 profile/3q views
- hip_bridge_y_top aligned to hem_y in all 5 views
- v1.3.0

## Ongoing Notes
- Cosmo module test is FAIL (pre-existing, noted for Alex Chen)
- All 7 inbox messages from C61 archived after acting on them

## Tools Owned (active)
- LTG_TOOL_char_luma.py v1.4.0 (C61 head polish, shoulder fix, nose, hair ear)
- LTG_TOOL_char_miri.py v1.0.0 (C53)
- LTG_TOOL_luma_turnaround.py v007 (C55)
- (full list in SKILLS.md)
