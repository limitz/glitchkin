# QA Pipeline Character Relevance Audit — Cycle 50

**Author:** Morgan Walsh (Pipeline Automation Specialist)
**Date:** 2026-03-30
**Purpose:** Identify which QA checks are character-relevant, background-relevant, or both — and document gaps in character quality measurement.

---

## Methodology

Every check in the three QA systems (render_qa, precritique_qa, ci_suite) was tagged as:
- **CHAR** — primarily evaluates character quality
- **BG** — primarily evaluates background/environment quality
- **BOTH** — evaluates aspects that span character and background
- **META** — pipeline/code hygiene, not image quality

---

## 1. render_qa (6 checks)

| # | Check | Tag | What it measures |
|---|-------|-----|-----------------|
| A | Silhouette readability | **CHAR** | Is the character recognizable as a silhouette? |
| B | Value range | **BOTH** | Full-image brightness range (min/max/dynamic range) |
| C | Color fidelity | **BOTH** | Canonical palette adherence (LAB delta-E against master_palette.md) |
| D | Warm/cool separation | **BG** | FG/BG temperature split per Depth Temperature Rule |
| E | Line weight consistency | **BOTH** | Stroke uniformity across entire image |
| F | Value ceiling guard | **BG** | Max brightness loss after thumbnail downscale |

**Character-relevant: 1/6 (17%)**
**Background-relevant: 2/6 (33%)**
**Both: 3/6 (50%)**

---

## 2. precritique_qa (14 sections)

| # | Section | Tag | What it measures |
|---|---------|-----|-----------------|
| 1 | Render QA | **BOTH** | Wraps render_qa (see above — mixed) |
| 2 | Color verify | **BOTH** | Canonical color fidelity on style frames |
| 3 | Proportion verify | **CHAR** | Head/body proportion checks on character sheets |
| 4 | Stub linter | **META** | Broken imports in output/tools/ |
| 5 | Palette warmth lint | **BOTH** | Hoodie/skin warmth compliance |
| 6 | Glitch spec lint | **CHAR** | Glitchkin generator spec validation (colors, patterns) |
| 7 | README sync | **META** | README Script Index completeness |
| 8 | Motion spec lint | **CHAR** | Motion spec sheet structural checks |
| 9 | Delta + Arc-diff | **BOTH** | Version-to-version diff (informational) |
| 10 | Alpha blend lint | **BG** | Fill-light composition defect detection |
| 11 | UV_PURPLE lint | **BG** | Glitch Layer color balance (world-rule, not character) |
| 12 | Depth temperature lint | **BG** | Warm=FG / cool=BG depth grammar |
| 13 | Warm pixel percentage | **BG** | Per-world-type warm/cool pixel classification |
| 14 | Sightline validation | **CHAR** | Gaze angular error (character eye direction) |

**Character-relevant: 4/14 (29%)**
**Background-relevant: 4/14 (29%)**
**Both: 4/14 (29%)**
**Meta: 2/14 (14%)**

---

## 3. ci_suite (10 checks)

| # | Check | Tag | What it measures |
|---|-------|-----|-----------------|
| 1 | stub_linter | **META** | Broken import detection |
| 2 | draw_order_lint | **META** | Draw order violations in generator code |
| 3 | glitch_spec_lint | **CHAR** | Glitchkin spec compliance |
| 4 | spec_sync_ci | **CHAR** | P1 character spec CI gate (5 characters) |
| 5 | char_spec_lint | **CHAR** | Detailed character spec (L/S/M codes) |
| 6 | dual_output_check | **META** | Generator filename conflicts |
| 7 | hardcoded_path_check | **META** | /home/ absolute paths in generators |
| 8 | thumbnail_lint | **META** | Unwhitelisted .thumbnail() calls |
| 9 | motion_sheet_coverage | **CHAR** | Motion sheet exists for each character |
| 10 | doc_staleness | **META** | Documentation freshness |

**Character-relevant: 4/10 (40%)**
**Background-relevant: 0/10 (0%)**
**Meta: 6/10 (60%)**

---

## Aggregate Summary

| Tag | render_qa | precritique_qa | ci_suite | **Total** | **%** |
|-----|-----------|---------------|----------|-----------|-------|
| CHAR | 1 | 4 | 4 | **9** | **30%** |
| BG | 2 | 4 | 0 | **6** | **20%** |
| BOTH | 3 | 4 | 0 | **7** | **23%** |
| META | 0 | 2 | 6 | **8** | **27%** |
| **Total** | 6 | 14 | 10 | **30** | 100% |

### Finding: Character-specific checks are 30% of all checks, not 90%+ background-only.

However, the **effective character coverage** is worse than 30% suggests:
- CHAR checks are shallow: proportion ratios, spec code linting, motion sheet existence, sightline on 1 registered asset.
- No check evaluates: **face quality**, **expression readability at scale**, **character appeal**, **pose believability**, **shoulder mechanics** (codified C47), or **before/after improvement tracking**.
- The "BOTH" checks (color fidelity, value range, line weight) are dominated by background pixels — characters are typically <20% of canvas area, so these metrics are BG-weighted in practice.
- The BG checks (depth temp, warm pixel, UV_PURPLE, alpha blend) were all added C44-C49 — the last 6 cycles have been background quality focused.

**Effective character quality measurement: ~15% of pipeline capacity.**

---

## 4. Character Quality Gaps

### Critical gaps (no tool exists)

| Gap | Impact | Recommendation |
|-----|--------|---------------|
| **Face quality at render scale** | Faces are the #1 thing viewers look at. No automated check. | Integrate face_test results into precritique_qa as Section 15 |
| **Expression readability at thumbnail** | Pitch decks show characters at ~64px. No scale test. | New tool built this cycle: `LTG_TOOL_thumbnail_readability.py` |
| **Before/after comparison** | No way to quantify improvement when iterating. | New tool built this cycle: `LTG_TOOL_char_compare.py` |
| **Shoulder mechanics (C47 rule)** | Codified in image-rules.md but not checked by any tool. | Build shoulder angle detector or integrate into char_spec_lint |
| **Character appeal metrics** | Silhouette distinctiveness is new (Kai C50) but not in QA pipeline. | Integrate `LTG_TOOL_silhouette_distinctiveness.py` into precritique_qa |
| **Pose believability** | No check for anatomical plausibility of poses. | Lower priority — hard to automate without neural models |

### Existing tools NOT integrated into QA pipeline

| Tool | What it does | Should be in pipeline? |
|------|-------------|----------------------|
| `LTG_TOOL_character_face_test.py` | Face legibility at sprint scale | YES — Section 15 |
| `LTG_TOOL_char_diff.py` | Proportion diff between reference/candidate | YES — Section 16 (regression gate) |
| `LTG_TOOL_silhouette_distinctiveness.py` | Pairwise silhouette distinction (Kai C50) | YES — Section 17 |
| `LTG_TOOL_face_landmark_detector.py` | Face landmark detection | YES — feed into face quality metric |
| `LTG_TOOL_face_curve_validator.py` | Face curve validation | YES — Section 18 |
| `LTG_TOOL_multi_char_face_gate.py` | Multi-character face gate | YES — Section 19 |
| `LTG_TOOL_thumbnail_readability.py` | Multi-scale readability (NEW C50) | YES — Section 20 |
| `LTG_TOOL_char_compare.py` | Before/after comparison (NEW C50) | Standalone — on-demand |

---

## 5. Recommendations

### Deprecate or demote
- **None.** All existing checks serve valid purposes. The issue is not bad checks — it is missing character checks.

### Modify
1. **render_qa silhouette check (A):** Currently scores "distinct/ambiguous/blob" — too coarse. Should output numeric distinctiveness score per the silhouette_distinctiveness tool API.
2. **precritique_qa proportion verify (3):** Only runs on character sheets. Should also validate proportions in style frames where characters appear (extract character from scene).
3. **render_qa color fidelity (C):** Weight foreground pixels 2x when calculating delta-E for character assets. Currently background dominates.

### Add (priority order)
1. **precritique_qa Section 15: Face Quality Gate** — integrate character_face_test + face_landmark_detector. PASS/WARN/FAIL based on feature count and spacing at render scale.
2. **precritique_qa Section 16: Silhouette Distinctiveness** — integrate Kai's new tool. FAIL if any character pair DS < 0.15.
3. **precritique_qa Section 17: Thumbnail Readability** — integrate new LTG_TOOL_thumbnail_readability. Test all character assets at 128/64/32px.
4. **precritique_qa Section 18: Face Curve Validation** — integrate face_curve_validator for all human characters.
5. **ci_suite Check 11: Shoulder Mechanics Lint** — static analysis of character generators for shoulder-arm coupling code (C47 rule compliance).

### Pipeline priority shift
The last 6 cycles (C44-C49) added 4 background checks and 1 character check (sightline). This cycle should add 3-5 character checks to rebalance the pipeline toward 50/50 character/background coverage.

---

## 6. New Tools Delivered This Cycle

### LTG_TOOL_char_compare.py v1.0.0
- Before/after comparison: side-by-side PNG + diff heatmap + quantitative metrics
- Metrics: SSIM, pixel delta %, silhouette IoU, FG-only delta, hue shift, value shift
- CLI and programmatic API (`compare_characters()`)
- Grades: SIMILAR / MODIFIED / MAJOR_CHANGE

### LTG_TOOL_thumbnail_readability.py v1.0.0
- Multi-scale character evaluation at 128/64/32px heights
- Metrics: silhouette preservation (IoU), edge retention, hue stability, expression density
- Per-scale PASS/WARN/FAIL with calibrated thresholds
- Contact sheet generation + batch mode for directories
- CLI and programmatic API (`test_readability()`, `batch_test()`)
