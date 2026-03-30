<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Dual-Miri Visual Plant — Proposal
## Jordan Reed | C38 | 2026-03-29

**Status:** PROPOSAL — awaiting Alex Chen brief before execution

---

## Background

The story bible (Priya Shah, C37) explicitly names the Grandma Miri / Glitch Layer Miri
name connection as the season 1 finale seed, and states: "The show plants this connection
early and pays it off in the season 1 finale."

Ingrid Solberg (Critique 15, score 78) is categorical: "The Miri/Miri connection, the
show's most resonant long-form storytelling device, has no visual seed anywhere in the
pitch package." She flagged it as a story promise the visuals cannot yet cash.

Zoe Park (age 11) and Ingrid both independently flagged the connection as compelling
but invisible. This is a P2 task dependent on Alex Chen's cold open canon decision.

---

## Constraint

The plant must be:
- **Subtle** — invisible to a first-time viewer, rereadable in hindsight only
- **Specific** — a concrete visual detail, not a vague color association
- **Achievable in one existing image** — we are modifying an existing asset, not creating new
- **Real World only** — the Glitch Layer palette must not appear in Miri's kitchen or den
- **Palette-safe** — no GL hue drift in Miri's scene (per CHAR-M production note, master_palette.md)

---

## Asset Candidates

### Candidate A — Grandma Kitchen (RECOMMENDED)
**Asset:** `LTG_ENV_grandma_kitchen.png`
**Generator:** `LTG_TOOL_bg_grandma_kitchen.py`

The Grandma Miri kitchen is the strongest candidate because:
1. It is the scene where "everything begins" — the CRT doorway is already present
2. The kitchen is established as Miri's most personal space (crossword, rose mug, travel
   magnets, medicine bottles, knitting bag — all individuated character details)
3. A viewer will spend time in this image — the warmth invites lingering

**Proposed plant:** A HANDWRITTEN NAME on a small object in the kitchen — specifically,
a piece of mail or a sticky note on the fridge, visible near the fridge magnets, that reads
"MIRI" in handwriting. This is Grandma Miri's name displayed naturally in her own space.
The connection to the Glitch Layer elder named "Miri" is only meaningful in hindsight.

The word "MIRI" drawn at 15–18px uppercase, in DEEP_COCOA at 70% opacity, on a
small paper rectangle attached to the fridge alongside the travel magnets. The handwriting
style: slightly uneven lowercase-ish uppercase (she writes quickly, comfortably, at home).
It should read as a grocery list or medication reminder — mundane — not a signature.

**Why this works:** The fridge is the domestic object most associated with family accumulation.
A name on a fridge reads as a household label. Nobody will notice on first viewing. On
rewatch, after the finale reveal, the image of "MIRI" in a warm, domestic, human context
will be precisely the anchor the emotional payoff needs.

---

### Candidate B — Grandma Living Room
**Asset:** `LTG_ENV_grandma_living_room.png`
**Generator:** `LTG_TOOL_env_grandma_living_room.py`

The living room has less narrative weight in the pitch package — it is not the scene where
discovery happens. A plant here would be less meaningful in hindsight.

**Proposed plant (backup):** A handwritten label on a shelf or a book spine reading "MIRI"
in the same approach as Candidate A.

---

### Candidate C — SF01 Discovery (v005)
**Asset:** `LTG_COLOR_styleframe_discovery.png`
**Generator:** `LTG_TOOL_styleframe_discovery.py`

SF01 is the strongest NARRATIVE candidate because it is already being revised for C38
(Ingrid's sight-line fix — Lee Tanaka Brief 3 to Rin Yamamoto). If we are rebuilding
the pose, we could integrate the plant into the same pass.

However: SF01 is already tasked to Rin Yamamoto for the sight-line fix. Dual modification
risk is high. I would need to coordinate with Rin before adding anything here.

**Proposed plant (if coordinating with Rin):** A sticky note on the side of the CRT monitor
(in the background, lower-right of screen body) that reads "MIRI" in Grandma Miri's
handwriting. The CRT is Miri's. She named it, or labelled it. This becomes deeply resonant
in hindsight when the CRT is revealed to be a portal between the two Miris.

This is the most emotionally potent location but requires coordination and has higher risk
of disrupting Rin's current generator work.

---

## Recommendation

**Execute in Grandma Kitchen v004 → v005.**

Rationale:
- Lowest disruption risk (no other C38 work active on this asset)
- Highest narrative clarity — the kitchen is Miri's most personal, viewer-lingered space
- Achievable in a single targeted modification to the existing generator
- The fridge-label placement reads as domestic mundanity, not as a planted clue

The plant is: A small piece of paper on the fridge (near the travel magnets, right-center
of fridge body) reading "MIRI" in simple handwriting. Real World palette only. No GL colors.

---

## Awaiting

- Alex Chen's cold open canon decision (P1 blocker resolved by Alex in C38)
- Alex's brief on specific plant requirements (Dual-Miri visual plant, P2 in Alex's C38 directives)
- If coordinating on SF01: Lee Tanaka's Brief 3 delivery to Rin Yamamoto (and copy to Jordan)

Once Alex's brief arrives, execution is a single generator modification: add one small paper
rectangle + handwritten "MIRI" text to the fridge section of the kitchen generator.
Estimated complexity: LOW. No QA concerns expected (single Real World text element).

---

*Jordan Reed — Style Frame Art Specialist*
*Cycle 38 — "Luma & the Glitchkin"*
