<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Color Readiness Statement — Critique 13
**Prepared by:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29 (C31)
**Scope:** All pitch-primary assets — 4 style frames + 8 character sheets/models

---

## 1. Palette Integrity

All registered palette entries verified. Master palette (master_palette.md) is current through C31:
- **GL-01 through GL-08a** complete — no gaps, all shadow companions documented.
- **CHAR-L-01 through CHAR-L-11** complete — CHAR-L-11 (#E8C95A Soft Gold hoodie pixel) registered C14, hex error corrected C30 (GL-01 cold scene, not GL-01b).
- **Section 8 (Act 2)** complete — CHAR-M, TD-01–13, SH-01–12 all present.
- **GL-06c** (#0A4F8C Storm Confetti Blue) registered C28.
- **DRW-16** (Luma shoulder under Data Stream Blue) and **DRW-18** (Luma Hair Glitch Layer) documented.

---

## 2. Style Frame Color Continuity

### SF01 v004 — Discovery (PITCH PRIMARY)
- Warm/cool arc: lamp-warm dominant, CRT cyan rim. PASS on all checks except warm_cool tool WARN (see §4).
- GL-07 CORRUPT_AMBER: Δ0.0° — exact. BYTE_TEAL: Δ2.1° — within tolerance.
- Cold overlay: cold_alpha_max=60, ~11.8% at boundary. Correctly reads as split-light, not Glitch Layer immersion.

### SF02 v005 — Glitch Storm (PITCH PRIMARY)
- All GL colors confirmed: GL-07 #FF8C00 (Δ1.4°), GL-01b Δ1.6°, HOT_MAGENTA Δ1.6°, ELECTRIC_CYAN Δ0.3°, SUNLIT_AMBER Δ0.4°.
- CORRUPT_AMBER corrected to canonical GL-07 in C22. Window pane alpha 115/110.
- ENV-06 terracotta-cyan-lit (150,172,162) confirmed correct.
- Warm/cool tool WARN: false positive (see §4).

### SF03 v005 — Other Side (PITCH PRIMARY)
- UV_PURPLE_DARK corrected to GL-04a (58,16,96) in C28 — deep void reads as digital void.
- Confetti constrained to 150px of anchors (C27).
- Color fidelity WARN (UV_PURPLE Δ9.2°, SUNLIT_AMBER Δ9.3°): both are documented false positives (see §4).
- Zero warm light sources confirmed in generator.

### SF04 v003 — Luma & Byte (CARRY-FORWARD ISSUES)
- **Silhouette: ambiguous** — SF04 reads soft; may be intentional warm diffuse lighting or generator issue.
- **No bright highlights** (max=198 vs threshold 225) — soft-key lighting or highlight gap.
- **Byte teal below canonical** — luminance ~60-70% of (0,212,232); pending Alex Chen decision (carry-forward since C26).
- **Generator source missing** — LTG_TOOL_styleframe_luma_byte_v*.py are forwarding stubs. Kai must resolve before SF04 can be regenerated. **HIGH RISK item.**
- SUNLIT_AMBER false positive (see §4).
- These issues are pre-existing carry-forwards, not C31 regressions.

---

## 3. GL Color Containment

The warm/cool light-source containment rule (Glitch colors may not appear as warm light sources) is enforced in all three primary style frames:
- **SF01**: No Glitch palette colors in warm lamp zone. Cyan emission from monitor only.
- **SF02**: CORRUPT_AMBER is crack-line stroke + outline only. No amber area fill.
- **SF03**: Zero warm light sources in generator code. All amber values are material pigment / crack-line strokes.

---

## 4. Known False-Positive Exceptions (QA Tool)

The following WARN flags are documented false positives and do NOT represent production color errors:

| Asset | Flag | Root Cause | Status |
|---|---|---|---|
| All Luma sheets, lineup | SUNLIT_AMBER FAIL (Δ9-16°) | Skin tones hue ~18-25° sampled within radius=40 of SUNLIT_AMBER target hue 34.3° | Documented C26 — false positive |
| Miri expression sheet | SUNLIT_AMBER FAIL (Δ16.2°) | Same: warm skin tones | False positive |
| SF03 v005 | UV_PURPLE FAIL (Δ9.2°) | Gradient/AA edge pixels pull median off canonical GL-04 | Documented C30 — false positive |
| SF03 v005 | SUNLIT_AMBER FAIL (Δ9.3°) | GL-07/amber crack-line hue sampled as SUNLIT_AMBER at radius=40 | Documented C30 — false positive |
| SF04 v003 | SUNLIT_AMBER FAIL (Δ12.4°) | Soft Gold swatch at hue ~46° falls in SUNLIT_AMBER sampling radius | Documented C30 — false positive |
| All style frames | Warm/cool WARN | Tool compares top-half vs. bottom-half median hue — valid for mixed-temperature scenes, unreliable for single-dominant-key or uniformly-cool frames | Tool limitation, not production error |

---

## 5. Open Issues

- **SF04 generator source missing** — HIGH. Kai Nakamura must restore or rebuild. SF04 PNG exists but is non-reproducible. Blocking for any SF04 revision.
- **SF04 Byte teal luminance** — PENDING Alex Chen decision. If intentional scene lighting, document in SF04 spec; if error, requires generator access (above).
- **SF04 ambiguous silhouette / no bright highlights** — Likely a soft-key lighting artifact. Needs director review once generator is restored.

---

## Bottom Line

**3 PASS / 9 WARN / 0 FAIL** out of 12 pitch-primary assets. All WARNs on the three primary style frames (SF01, SF02, SF03) are documented false positives from known QA tool limitations. SF04 carries three unresolved issues (generator missing, Byte teal, silhouette) that are pre-existing and require Kai/Alex action — they are not C31 regressions. The primary pitch color arc (warm → contested → cold/alien) is intact and correctly rendered across SF01–SF03.
