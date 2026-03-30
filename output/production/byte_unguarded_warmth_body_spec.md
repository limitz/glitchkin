<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Byte — UNGUARDED WARMTH Body-Pose Delta Specification
## "Luma & the Glitchkin"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30
**Cycle:** 41
**Flagged by:** Daisuke Tanaka (multiple cycles — UNGUARDED WARMTH differs only in color, no body delta)
**Requested by:** Alex Chen — C41 brief, to be routed to Maya Santos for implementation

---

## 1. Problem Statement

Byte's UNGUARDED WARMTH expression (v005, Maya Santos C33) currently differs from
all other expressions primarily in **color** (gold confetti, SOFT_GOLD star pixel
symbol, UV_PURPLE heart, warm-cream BG) but not in **body language**. Daisuke has
flagged this for multiple cycles: a robot character expressing warmth through color
alone is insufficient.

The RPD silhouette tests confirm this: UNGUARDED WARMTH shares arm/body geometry
with expressions that should feel entirely unlike it.

---

## 2. Design Principle: What "Open" Means for Byte

Byte's default body language is **self-contained and compact**:
- Arms close to body sides or crossing inward (defensive/neutral configs)
- Float height: mid (standard hover)
- Body tilt: neutral (0°) or slight backward lean
- Lower limbs: pointing straight down (stable, controlled)

This compactness is not hostility — it is Byte's default mode. He exists in a world
that has repeatedly asked too much of him. Compact = "I have not agreed to participate yet."

UNGUARDED WARMTH is the one state where Byte is **not managing his presentation**.
He is caught in a genuine feeling. The body language must make this legible WITHOUT
color cues — if you removed the gold confetti and looked at the silhouette alone, it
should still read as emotionally open.

---

## 3. Body-Pose Delta: UNGUARDED WARMTH

### 3.1 Arms

**Current (v005/v006):**
Arms float slightly upward (`arm_l_dy = -5`, `arm_r_dy = -5`) — a small lift, but
within the range of several other expressions.

**Proposed:**
- `arm_l_dy = -14` (left arm floats noticeably high — reaching up, not reaching out)
- `arm_r_dy = -16` (right arm slightly higher — slight asymmetry to avoid "triumphant" read)
- Both arms angled **outward and slightly upward** — at `arm_x_scale ≈ 1.0` (same as NEUTRAL)
  but with the higher `dy`, this creates a floating-open silhouette.
- The tips face upward, not outward — this is a float-drift, not a reach. Byte is not
  asking for something. He is simply not guarded against anything.

**Contrast with other raised-arm states:**
- ALARMED: `arm_x_scale 2.0`, `arm_l/r_dy` at maximum height — rigid, sharp, braced
- TRIUMPHANT (not implemented but comparable): arms raised with body stretch — assertive
- UNGUARDED WARMTH: arms lifted as if carried by buoyancy, not effort. The difference
  is **energy level** — low energy, high arm position. Arms float because Byte is not
  holding them anywhere.

### 3.2 Float Height

**Current (v005/v006):** Standard float height (floating clearance ~0.25 heads)

**Proposed:** Reduce float height by approximately 4px at expression-sheet scale.
**Lower float = more settled, more present, more committed.**

Byte usually maintains distance by floating slightly higher when uncertain or guarded.
Dropping float height toward a surface is a small but legible gesture of presence.
This is the robot equivalent of leaning in.

At 240px panel width (expression sheet scale), a 4px difference is visible if rendered
correctly and will be picked up by the RPD zone separator at the LEGS zone.

### 3.3 Body Tilt

**Current (v005/v006):** `body_tilt = -4` (slight forward lean toward Luma)

**Proposed:** Keep `body_tilt = -4`. The forward lean is correct — do NOT increase it
further. Over-tilt reads as COMMITTED or SEARCHING. UNGUARDED WARMTH is not pursuing.
It is simply open.

The -4° is correct. This is the one pose parameter that should not change.

### 3.4 Lower Limbs

**Current:** Standard downward angle (pointing straight down)

**Proposed:** Toe-in very slightly (each lower limb rotated ~8° inward from vertical).
This creates a soft pigeon-toed silhouette at the base — slightly child-like, slightly
vulnerable. It reads as "not braced." In contrast, ALARMED's wide-braced stance
communicates "ready to react." UNGUARDED WARMTH's toe-in communicates "not ready to
do anything — just here."

At expression-sheet scale this is a 2–3px positional change per lower limb tip. It
is a subtle read but contributes to the overall silhouette.

---

## 4. Silhouette Test Target

The RPD score between UNGUARDED WARMTH and its nearest failing neighbors should
drop below 85% (WARN range) after this fix.

Predicted most similar expression after fix: **RELUCTANT JOY** (also has raised arms,
slight lean). The key differentiator will be:
- RELUCTANT JOY: arms asymmetric (`arm_l_dy = -12`, `arm_r_dy = 18`) — one up, one low
- UNGUARDED WARMTH: arms symmetric and high (`arm_l_dy = -14`, `arm_r_dy = -16`) — bilateral float

The bilateral symmetry of UNGUARDED WARMTH's arm position is intentional — it echoes
the bilateral warmth of the expression itself. Byte is not performing asymmetric
reluctance. He is genuinely, symmetrically, open.

---

## 5. Implementation Brief for Maya Santos

**File:** `output/tools/LTG_TOOL_byte_expression_sheet.py` (v006 → v007)

**Changes to make in the UNGUARDED WARMTH expression config:**

```python
# UNGUARDED WARMTH — body-pose delta (C41, Daisuke flag resolution)
arm_l_dy    = -14      # was -5 — arms float high, buoyant not reaching
arm_r_dy    = -16      # slight asymmetry to avoid triumphant read
arm_x_scale = 1.0      # same as neutral — outward but not spread
float_offset = -4      # drop float height by 4px (settled, present)
body_tilt   = -4       # UNCHANGED — forward lean is correct
# Lower limbs: toe-in ~8° per limb (see below)
lower_l_angle = 8      # degrees inward from vertical (left limb)
lower_r_angle = 8      # degrees inward from vertical (right limb)
```

**Confetti (retain from v005/v006):**
- SOFT_GOLD confetti — ONLY this expression
- Count and spread: retain v005 values

**Color (retain from v005/v006):**
- Star_gold pixel symbol (SOFT_GOLD star, right/organic eye)
- Heart_purple (UV_PURPLE heart, left/cracked eye)
- Warm-cream-leaning-cool background

**After implementing:** Run `LTG_TOOL_expression_silhouette.py` on the updated sheet
with `--mode full` and `--viz-rpd` to verify the RPD score for the UNGUARDED WARMTH
vs RELUCTANT JOY pair drops below the current 90.2%.

---

## 6. Cross-References

- `output/characters/main/byte.md` — Limb config vocabulary (§5, Configuration table)
- `output/tools/LTG_TOOL_byte_motion.py` — UNGUARDED WARMTH motion descriptor: "toward, low, floating high arms, bilateral warm glow" (confirms direction of this spec)
- `output/tools/README.md` — Byte expression sheet current version (v006, C38)
- `output/tools/LTG_TOOL_expression_silhouette.py` — RPD test tool for post-implementation verification
- Daisuke Tanaka critique feedback — multiple cycles flagging color-only distinction

*Cycle 41 — Sam Kowalski, Color & Style Artist*
