# Pre-Critique Audit — Cycle 37
**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-30
**Purpose:** Identify the top concern areas heading into Critique Cycle 15. This document gives the critique panel a focused starting point and helps the team anticipate where the work is weakest.

---

## How to Read This Document

Each concern area is listed with: what is at risk, what evidence supports the concern, and what a critic should specifically look for. Priority is descending — P1 is the most urgent.

---

## P1 — THE NOTICING: Still Not Fully Landing (Character/Expression)

**What is at risk:** The emotional core of the pitch. "THE NOTICING" is the moment Luma first understands that the Glitchkin are real — the freeze-between-worlds beat that has been called out in MEMORY.md as unresolved since C33. Maya Santos has been directed on it across multiple cycles. Luma expression sheet v009 is the current pitch-primary version.

**Evidence:** MEMORY.md C36 open items include "THE NOTICING still not fully landing: Maya (P2 ongoing)." The critique panel has not formally evaluated v009's execution of this specific beat.

**What critics should look for:**
- Does the "THE NOTICING" expression panel communicate frozen wonder vs. any other wide-eyed reaction? (It must not read as SURPRISED or SCARED.)
- Is the expression distinct at thumbnail scale — does it survive the squint test independently of the label?
- If it does not survive thumbnail as a distinct emotional register, this is a pitch-blocking issue.

---

## P2 — Cosmo v005 Glasses Tilt Violation (Character Spec Compliance)

**What is at risk:** Cosmo expression sheet v005 (current pitch-primary). The C36 spec_sync_ci_v001 tool (Kai Nakamura) found that `glasses_tilt = 10°` in the v005 generator violates S003 (canonical neutral = 7°). This was flagged as P1 in MEMORY.md and Maya was directed to produce a v006 correction.

**Evidence:** MEMORY.md C36 open items: "Cosmo v006 P1: glasses_tilt 10° → 7° (S003 violation found by Kai spec_sync_ci). Maya directed. (P1)"

**What critics should look for:**
- If v006 is delivered before critique: verify glasses tilt reads as 7° neutral, not tilted further by emotional states unless intended.
- If v006 is NOT delivered and v005 remains pitch-primary: flag the tilt as a spec violation. The Cosmo design spec has always treated the 7° neutral tilt as a character fingerprint — a character who deviates from their own spec is no longer fully themselves.
- Also: Cosmo has a history of thumbnail-readability issues (SKEPTICAL expression fails squint test at Dmitri C8/C15). Check whether silhouette differentiation improvements from C35/C36 work have resolved these.

---

## P3 — RPD Baseline Not Yet Run (QA Infrastructure Gap)

**What is at risk:** All silhouette QA scores for the current pitch-primary expression sheets are based on the old IoM metric (v002 tool), which is now known to be biased toward shared trunk geometry. The v003 silhouette tool uses the RPD (Regional Pose Delta) metric — HEAD 35%, ARMS 45%, LEGS 20%. Old scores are not comparable to new scores. Until the RPD baseline is run against all five current sheets (Luma v009, Cosmo v005, Miri v004, Byte v005, Glitch v003), the production cannot objectively claim any expression sheet passes the silhouette differentiation standard.

**Evidence:** MEMORY.md C36: "RPD baseline run NEEDED: Run silhouette_v003.py against all current sheets… Old IoM scores not comparable to RPD. (P2)"

**What critics should look for:**
- Are there expression pairs that feel visually similar? (Byte: RESIGNED vs POWERED DOWN has been a recurring concern since C15.)
- Do character silhouettes differentiate at 10% thumbnail across all five characters?
- Note: the QA gap means critics cannot lean on the tool output for this — they must apply their own eyes to the squint test.

---

## P4 — Storyboard/Story Integration (New This Cycle)

**What is at risk:** Two brand-new team members (Diego Vargas, Storyboard; Priya Shah, Story & Script) have delivered their first work this cycle. This is the first time the pitch will have a formal story bible and a purpose-built cold open storyboard sequence. These assets are untested against the established visual language.

**Specific concerns entering critique:**

1. **Cold open board alignment**: Does Diego's board staging match the world and character language established by 36 cycles of visual development? The warm/Glitch color language, the depth layers, and Luma's body language vocabulary all need to read consistently in board form. If the boards use neutral/default staging, the pitch will feel schizophrenic between the polished style frames and the boards.

2. **Story bible consistency**: Does Priya's story bible v001 reflect the show that 36 cycles of visual development has been building, or does it describe a different show? The visual development has strongly implied: comedy-first, emotional warmth vs. digital cool as the central tension, Byte as a character with an interior life expressed through color asymmetry. If the bible describes anything materially different, critics will feel the disconnect.

3. **"THE NOTICING" as narrative payload**: The story bible must treat the pilot cold open beat — the moment at the CRT screen — as the earned climax it is visually. If the bible describes it as a generic discovery moment, the visual team's years of specificity on this beat become orphaned.

**What critics should look for:**
- Read boards against the character spec sheets. Does Luma read as Luma in board form?
- Read the story bible against the style frames. Does the world the bible describes match the world the frames show?

---

## P5 — Warm/Cool QA False Positive Saturation (Pipeline Noise)

**What is at risk:** Operational clarity during critique prep. The C36 QA run returned WARN on all four style frames (SF01–SF04) for warm/cool separation — all confirmed false positives. The known issue is that render_qa_v001.py does not use world-type-aware thresholds. Sam Kowalski built `ltg_warmth_guarantees.json` and the `--world-type` / `--world-threshold-only` flags in C36, but Kai has not yet integrated these into render_qa. Until the integration is done, the QA report will continue to show 4 WARNs that are known-false, which degrades the signal value of the report.

**Evidence:** Sam C36 completion report; MEMORY.md C36 carry-forward: "Warm/cool QA `expected_temp` param: Kai (P2 — Sam directed)."

**What critics should look for:** This concern is primarily operational (not visual). However, if critics use the QA report as part of their assessment, they should weight color-quality warnings carefully for the Glitch World and Other Side frames, which are intentionally cold and will always fail a global warm/cool threshold.

---

## Summary Table

| Priority | Area | Asset(s) Affected | Status |
|---|---|---|---|
| P1 | THE NOTICING expression | Luma expr v009 | P2 open — unresolved 3+ cycles |
| P2 | Cosmo glasses tilt S003 violation | Cosmo expr v005/v006 | Maya directed C36 — v006 TBD |
| P3 | RPD baseline scores missing | All 5 expr sheets | Run silhouette_v003.py first |
| P4 | Story/board integration (new) | story_bible_v001, SB cold open | First delivery — untested |
| P5 | Warm/cool QA false positives | SF01–SF04 QA output | Infrastructure gap, not visual |

---

## What This Cycle Added (C37 New Assets for Critique)

- Story Bible v001 (Priya Shah) — first narrative anchor document
- Cold Open Storyboard (Diego Vargas) — first purpose-built pitch boards
- Hana Okonkwo environment delivery (awaited)
- Ryo Hasegawa motion spec delivery (awaited)
- SF02 v008 (Rin Yamamoto) — fill-light direction fix (P1 resolved)

---

*Alex Chen, Art Director*
*"The work tells you what it needs. Listen to the gaps."*
