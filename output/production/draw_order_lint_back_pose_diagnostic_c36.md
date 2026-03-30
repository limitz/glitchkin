<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Draw Order Lint — Back Pose Investigation
## "Luma & the Glitchkin" — Diagnostic Note

**Author:** Alex Chen, Art Director
**Date:** 2026-03-30
**Cycle:** 36
**Subject:** Does `LTG_TOOL_draw_order_lint.py` incorrectly flag back-pose draw order in turnaround generators?

---

## Summary

**Verdict: No current false positive.** The draw_order linter does NOT incorrectly flag back-pose draw order in any existing turnaround generator. However, a latent risk exists for future generators that name depth-layering elements using "shadow" or "body" keywords in a back-pose context. This note documents the finding and the recommended linter update.

---

## Investigation

### What Was Checked

All 5 turnaround generators were linted with both v001 and v002:

- `LTG_TOOL_luma_turnaround.py` — PASS (v001 and v002)
- `LTG_TOOL_cosmo_turnaround.py` — PASS (v002)
- `LTG_TOOL_miri_turnaround.py` — PASS (v002)
- `LTG_TOOL_glitch_turnaround.py` — PASS (v002)
- `LTG_TOOL_luma_turnaround.py` — PASS (v002)

No warnings in any file. The Producer's concern is valid in principle — but the current generators are not triggering it.

### Back Pose Draw Order: What Correct Looks Like

In a back pose (viewing a character from behind), the correct painter's-algorithm order is:

1. Ground shadow
2. Feet / slippers (back elements, partially hidden)
3. Back leg (recedes behind body — drawn BEFORE body to be covered by it)
4. Body / torso (covers leg tops)
5. Arms (on top of body)
6. Head / hair (on top of body)
7. Front elements (front leg, if split-leg pose)

Miri's side-view function (`draw_miri_side`) follows this correctly: at line 784, the comment reads `# Back leg (slightly offset, partially hidden)` and the back leg is drawn before the cardigan body at line 788. This is correct draw order — the body covers the top of the back leg — and the linter does NOT flag it.

### Why the Linter Does Not Flag This (Correctly)

The linter's four checks are:

- **W001** — HEAD draw call before BODY draw call. Keywords tracked: `body|torso|trunk|chest|abdomen|belly|hull|shell|carapace` (body) and `head|face|skull|cranium|muzzle|snout` (head). "Leg", "pants", "shoe", "arm" are NOT in either keyword list. A back leg drawn before the body triggers no W001.

- **W002** — OUTLINE before FILL. Scans the same keyword lists. Back legs are never tagged as body/head, so no W002.

- **W003** — SHADOW after ELEMENT. Keywords: `shadow|drop_shadow|dropshadow|shade|cast`. If a back-leg draw call line contains one of these words (e.g., a comment `# back leg shadow for depth`) AND the function has already drawn a body/head element, W003 fires. In current generators, back legs use `PANTS_SH` as the fill color constant name — not the string "shadow" in a comment or variable name — so W003 does not fire. The risk is latent: if a future generator writes `# depth shadow — back leg` in a comment on the same line as a leg draw call after the body has been drawn, W003 would fire as a false positive.

- **W004** — Missing `draw = ImageDraw.Draw(img)` refresh after paste/composite. Not related to back pose order.

### Latent Risk: W003 False Positives in Future Back-Pose Generators

A developer writing a back-pose section might write:

```python
# --- TORSO (back)
draw.polygon(torso_pts, fill=HOODIE)

# --- BACK LEG shadow (depth indicator — this leg is behind body)
draw.rectangle([...], fill=PANTS_SH)   # W003 fires here if "shadow" is in the comment
```

W003 checks the TEXT OF THE LINE (including inline comments) for the `shadow` keyword. The body/torso draw appears earlier → the shadow-keyword leg line would trigger W003 as a false positive.

### Current Generators: Safe

All current turnaround generators avoid this by:
1. Drawing legs BEFORE the body (correct order: back leg first), or
2. Drawing legs AFTER the body but using neutral variable names (`PANTS_SH`, not `shadow`) and no shadow comments.

No generator violates correct back-to-front order for back poses.

---

## Recommendation

### Short Term (No Change Required)

No linter change is strictly necessary for current generators. All pass cleanly.

### Medium Term (Linter Enhancement for Future-Proofing)

Recommend Kai Nakamura add a **pose-context flag** to the draw_order linter:

```python
# In generator files, add a comment to scope the pose section:
# LINT: back_pose_begin
# ... back leg, back arm draws (drawn before body — correct for back view) ...
# LINT: back_pose_end
```

When the linter encounters `# LINT: back_pose_begin`, it inverts the expected draw order logic within that block: elements drawn before the body are expected and correct (back-to-front perspective). This eliminates any risk of W003 false positives for back-pose shadow/depth elements.

**Alternative simpler approach:** Add `back_pose` to a suppression list analogous to how docstrings are skipped for W004. Any draw call line where the comment contains "back_leg" or "back_arm" is excluded from W003 checking.

**Recommendation:** Route to Kai Nakamura as a P3 (non-blocking) enhancement for the linter. File in ideabox.

---

## Action Items

| Item | Owner | Priority |
|---|---|---|
| No immediate linter change needed | — | — |
| Kai: add back-pose suppression to W003 (or pose-context flag system) | Kai Nakamura | P3 |
| Team: when writing back-pose sections, draw back elements BEFORE body and use variable names (not inline comments) for depth/shade fills | All | Style guidance |

---

*Alex Chen, Art Director — Cycle 36 — 2026-03-30*
