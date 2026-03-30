# Critique C17 — Priya Nair (Color Theory & Emotional Palette)
**Cycle 40 — 2026-03-30**
**Assets reviewed:** SF01 v005 (C38), SF02 v008 (C34 lighting pass), SF03 v005, SF04 v004 (C32 rebuild), Luma/Byte/Cosmo/Miri/Glitch color models
**Tools used:** LTG_TOOL_render_qa.py (v1.3.0), LTG_TOOL_color_verify.py (v002), LTG_TOOL_precritique_qa.py (v2.4.0 C39 baseline)

---

## SF01 — LTG_COLOR_styleframe_discovery.png
**Score: 74/100**

- **Warm/cool separation 17.4 — now passing threshold 12.0.** This is a genuine improvement. The C29/C32 rim-light fixes and C38 threshold correction have together brought SF01 into compliance. The lamp-left / CRT-right split is working numerically.
- **BYTE_TEAL median still at 183.5° (Δ1.6° from canonical 185.2°).** The 183.5° bucket dominates: 56,853 of the 60,943 sampled ELECTRIC_CYAN-range pixels land there. The CRT teal is reading as generic ELEC_CYAN, not BYTE_TEAL specifically. Byte's identity is not encoded in SF01's screen color — this matters because SF01 is the frame that introduces the audience to the idea that something specific (Byte, not just "digital") is present in the monitor.
- **Color fidelity overall_pass=True** on hue-delta check; the LAB ΔE version from C39 QA showed BYTE_TEAL at ΔE=22.83 — a substantial perceptual distance. Hue pass does not mean perceptual match. The two metrics are in conflict and the LAB reading is more relevant to viewer perception.
- **Bottom line:** SF01 has crossed the warm/cool threshold and its warm-room logic holds, but the CRT screen still reads as generic digital emission rather than specifically Byte — the frame's central promise is color-ambiguous at the pixel level.

---

## SF02 — LTG_COLOR_styleframe_glitch_storm.png
**Score: 52/100**

- **Warm/cool separation 8.5, now passing the storm threshold.** The C34 HOT_MAGENTA fill-light pass raised separation from 6.5 to 8.5. Marginal but real. However: at 8.5 units, the frame is threading the minimum rather than building temperature contrast. The storm is a contested-world scene — the warm/cool tension should be dramatically evident, not just technically present.
- **Color fidelity: CORRUPT_AMBER (32.9°, Δ0.2°), ELECTRIC_CYAN (183.5°, Δ1.9°), HOT_MAGENTA (342.3°, Δ1.6°), BYTE_TEAL (185.2°, Δ1.6°) — all PASS.** The GL-07 canonical value is confirmed intact. This is the one area of consistent progress.
- **SUNLIT_AMBER registered at 34.3°, Δ0.4°, n=206.** Warm window spill is present and correctly registered. However 206 pixels in a 1280×720 frame is 0.02% coverage — this is not the "warm street life holds the ground" narrative the color story document promises. The warm window glow is technically verifiable but visually imperceptible. SUNLIT_AMBER needs 10× more pixels to read as a compositional element.
- **G007 persistent: VOID_BLACK outline on Glitch body polygon undetected across all SF02 generators (v001–v008).** Eight versions. The Glitch spec linter has flagged this continuously since C9. This is not a tool false positive — it is a structural spec violation that means Glitch reads as a flat amber shape without boundary definition against the storm.
- **Bottom line:** The storm palette is technically compliant but narratively mute — the warm/cool battle the color story document promises is present at sub-perceptual scale, and the Glitch G007 violation has now persisted through eight generator versions without resolution.

---

## SF03 — LTG_COLOR_styleframe_otherside.png
**Score: 57/100**

- **UV_PURPLE hue drift Δ9.2° — flagged FAIL, documented as false positive since C30.** The 447 sampled pixels span 250–275° (sky gradient transition zone); exact canonical pixels are present at 271.9°. This is confirmed FP. But the false positive has been documented and un-fixed for 10 cycles. A false positive registry that has existed as an open action item since C25 without implementation is a pipeline quality debt, not a theoretical concern.
- **Warm/cool separation 3.6, threshold 0.0 (OTHER_SIDE world type) — PASS.** The near-zero separation is by design — this is the cold alien world. However: the color story document states that "Luma's warm pigments (hoodie orange DRW-14 and skin DRW-11) are the only warmth in the frame." If they are the only warmth, the warm/cool ratio should show a small but clear signal from those two characters. A 3.6-unit reading suggests those warm pigments are not registering distinctly against the void — they are being absorbed, not contrasting.
- **CORRUPT_AMBER registered at 32.9°, Δ3.6° — the amber crack fragments in the void are present but shifted toward more orange range.** 263 samples; acceptable at this density.
- **G007 persistent across all SF03 generators (v001–v005), five versions.** The Glitch character outline required by spec has never appeared in this frame. Against the void-dark background, an unoutlined Glitch body dissolves — the most narratively critical character (Glitch, native to this world) is visually absent from the environment they supposedly inhabit.
- **Bottom line:** SF03's palette compliance is strong but the frame cannot deliver its narrative — Luma's warm pigments don't read as contrast against the void, and Glitch has no visual boundary in the environment that is supposed to be their home.

---

## SF04 — LTG_COLOR_styleframe_luma_byte.png
**Score: 50/100**

- **Warm/cool separation 1.1 — FAIL against threshold 12.0 (world=None, falls back to REAL default).** No movement from C14 critique (1.1 units). This is not a soft failure — 1.1 means the frame has effectively no color temperature information. A scene explicitly about the tension between Luma's warm world and Byte's digital nature should be delivering maximum warm/cool contrast. The scene's entire emotional argument is encoded in color temperature. It is not encoded here.
- **SUNLIT_AMBER FAIL at Δ15.7° — documented FP.** The 6,752 sampled pixels are at hue 15–30° (Luma skin and hoodie family), not SUNLIT_AMBER. But this false positive surfaces a real design question: if the face lamp lighting (at ~18° hue) is being sampled where SUNLIT_AMBER (34.3°) should be, the warm face light is in the raw-orange/skin family, not the Soft Gold/Sunlit Amber lighting family specified in Color Key 01. The lamp color may be too close to Luma's costume hue to read as a distinct light source.
- **BYTE_TEAL PASS (Δ0.0°), HOT_MAGENTA PASS (Δ0.0°).** The C32 rebuild correctly stabilized Byte's canonical colors. These remain the only solid color achievements in this frame.
- **SF04 generator source files still missing.** Documented in C30 carry-forward as HIGH priority. The current PNG cannot be regenerated — any fix requires a ground-up rebuild. This is a production risk that has been open for 10 cycles.
- **Bottom line:** SF04 is technically precise in Byte's colors and structurally broken in the only metric that matters for its narrative purpose — warm/cool separation — and the missing source files mean fixing it requires a full rebuild that has not happened.

---

## LTG_COLOR_glitch_color_model.png
**Score: 63/100**

- **CORRUPT_AMBER exact canonical (32.9°, Δ0.0°, n=9,247) — confirmed.** The primary body fill is correct.
- **CORRUPT_AMBER_HIGHLIGHT drift: 951 pixels at hue 40–45° (found=40.0°, Δ5.7° from SUNLIT_AMBER canonical).** This is not a SUNLIT_AMBER false positive — it is the highlight facet (#FFB950, RGB 255,185,80) landing in yellow-gold territory. The issue is categorical: CORRUPT_AMBER_HIGHLIGHT at 40–45° hue reads as Real World gold (Soft Gold RW-02 is at ~46°). The spec requires that CORRUPT_AMBER reads as "corrupted" — distinct from Real World warmth. A highlight facet that bleeds into the Soft Gold family undermines the categorical separation. The corrupted amber should stay on the orange side of the warm family (below 38°), not drift into gold.
- **UV_PURPLE (271.9°, Δ0.0°) and HOT_MAGENTA (342.3°, Δ0.0°) exact.** Shadow and crack colors are correct.
- **Bottom line:** Glitch's primary body color is confirmed but the highlight facet is drifting into Real World gold territory — a categorical color leak that blurs the boundary between corrupted-digital and warm-organic.

---

## Cross-Pitch Color Story Assessment
**Score: 45/100 (coherence)**

- **Measured warm/cool progression across the pitch: SF01=17.4, SF02=8.5, SF03=3.6, SF04=1.1 PIL units.** This reads as a monotonic decline but not an intentional arc — SF04 (the intimate character interaction) should not have lower warm/cool contrast than SF03 (the cold alien void). SF04's 1.1 is architecturally wrong for its scene type. The progression says: warm home → contested storm → alien cold → even colder character interaction. That is not the story.
- **SF02's warm/cool improvement from 6.5 (C38) to 8.5 (C40) is real but insufficient.** The storm scene should be the warmth-under-siege high point of visible tension — 8.5 units against a threshold of ~8 means the frame passes the minimum. Passing the minimum is not encoding the story.
- **The C39 QA report showed SF01 warm/cool dropping to 7.4 (FAIL) before recovering to 17.4 in the current file.** This suggests the SF01 PNG was regenerated between C39 and C40 — but no documentation of this regeneration appears in the C40 README or QA baseline. Unexplained version changes to pitch-primary PNGs are a color management problem.
- **G007 (VOID_BLACK outline on Glitch body) persists across 14 generator versions across SF02 and SF03.** This is the longest-running unfixed spec violation in the production. It is not a style choice — the Glitch spec requires it, the linter has flagged it every cycle, and it has never been implemented. Glitch as a character currently has no structural boundary in two of the four pitch frames.
- **Bottom line:** The pitch's color temperature narrative is partially functional for SF01, technically marginal for SF02, correctly cold for SF03, and architecturally wrong for SF04 — the four frames do not describe a coherent color arc, and the 14-cycle G007 omission means the show's most visually distinctive character lacks a defining structural color element.

---

*Priya Nair — Color Theory & Emotional Palette Specialist*
*"A palette that passes the threshold is not the same as a palette that lands."*
