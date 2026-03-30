<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Design-to-Bible Sync Checklist
## "Luma & the Glitchkin" — Preventing Production Bible Staleness

**Author:** Priya Shah, Story & Script Developer
**Created:** Cycle 49 (2026-03-30)
**Primary readers:** Alex Chen, Maya Santos, Priya Shah, all character/design artists
**Trigger:** C48 ideabox submission — production bible went 47 cycles stale; this checklist prevents recurrence.

---

## Purpose

When a design decision changes a character's appearance, shape language, color spec, or visual hook, the production bible and story bible must be updated in the same cycle or flagged for immediate update. This checklist maps each category of design change to the specific bible sections that must be checked.

This is a manual checklist, not an automated tool. The owner of each category is responsible for either (a) making the bible update themselves, or (b) sending a message to Priya Shah's inbox with the change details so she can update the story bible and flag the production bible.

---

## When to Use This Checklist

Use this checklist whenever ANY of the following occur:
1. A character design document is updated (new version of luma.md, byte.md, cosmo.md, glitch.md, grandma_miri.md)
2. A new expression sheet or turnaround version is generated
3. A critic flags a design change that is then implemented
4. A production rule is added to `docs/image-rules.md`
5. A new character is canonized or a supporting character receives a design spec
6. A naming/accessory/color decision is made by Alex Chen

---

## Checklist by Change Category

### A. Character Shape/Proportion Change
(e.g., head ratio, body height, shape language shift)

- [ ] Update `production_bible.md` Section 5 (character entry) — shape language line
- [ ] Update `production_bible.md` Section 8 — shape language summary
- [ ] Update `story_bible` character section (Section 5) — Appearance paragraph
- [ ] Verify character design doc (e.g., `cosmo.md`) matches bible description
- [ ] Notify: Priya Shah (story bible), Alex Chen (production bible sign-off)

### B. Visual Hook Change
(e.g., Cosmo bridge tape, Luma hoodie pattern, Byte scar)

- [ ] Update `production_bible.md` Section 5 — Visual hook line for affected character
- [ ] Update `production_bible.md` Section 8 — shape language summary if relevant
- [ ] Update `story_bible` character section — Appearance paragraph
- [ ] Check `pitch_delivery_manifest.md` — does the character description match?
- [ ] Check `pitch_package_index.md` — does the asset description match?
- [ ] Notify: Priya Shah

### C. Color Spec Change
(e.g., body fill, palette swap, new color token)

- [ ] Update `production_bible.md` Section 5 — Canonical body fill/color notes
- [ ] Update `style_guide.md` if global palette change
- [ ] Check all tool generators that render the affected character
- [ ] Notify: Sam Kowalski (color QA), Priya Shah

### D. Accessory/Costume Change
(e.g., Miri hairpin fix, Cosmo notebook, Luma hoodie)

- [ ] Update `production_bible.md` Section 5 and/or Section 7 — visual description
- [ ] Update `story_bible` character section — Appearance and Design note
- [ ] Update character design doc — accessory spec section
- [ ] Check `grandma_miri.md` or relevant character doc for canonical spec
- [ ] Verify all active tool generators have been updated (coordinate with Maya Santos)
- [ ] Notify: Priya Shah, Alex Chen

### E. New Character Canonized
(e.g., Glitch C39, supporting cast additions)

- [ ] Add entry to `production_bible.md` Section 5
- [ ] Add entry to `story_bible` Section 5
- [ ] Update `production_bible.md` Section 8 — shape language summary
- [ ] Update `pitch_delivery_manifest.md` — character count
- [ ] Update `pitch_package_index.md` — character assets
- [ ] If antagonist: create staging guide and voice direction (Priya Shah)
- [ ] Notify: Priya Shah, Diego Vargas (storyboards), Lee Tanaka (staging)

### F. Production Rule Added
(e.g., shoulder involvement C47, depth temperature C45, face test gate)

- [ ] Verify rule is in `docs/image-rules.md` (or appropriate docs/ file)
- [ ] Add reference line to `production_bible.md` Section 8 — production rules
- [ ] Check if rule affects `character_sheet_standards.md`
- [ ] No story bible update needed (production rules live in image-rules.md, not the bible)
- [ ] Notify: all affected character artists

### G. World/Location Change
(e.g., Millbrook specificity C43, school name, CRT location)

- [ ] Update `production_bible.md` Section 6 — affected location entry
- [ ] Update `story_bible` Section 3 — World Rules
- [ ] Check environment generators/paintings for consistency
- [ ] Notify: Hana Okonkwo (environments), Diego Vargas (storyboards), Priya Shah

---

## Responsibility Matrix

| Change Category | Primary Owner | Bible Updater | Sign-off |
|----------------|---------------|---------------|----------|
| Shape/Proportion | Maya Santos | Priya Shah (story) + Alex Chen (production) | Alex Chen |
| Visual Hook | Maya Santos | Priya Shah (story) + Alex Chen (production) | Alex Chen |
| Color Spec | Sam Kowalski / Maya Santos | Priya Shah flags, Alex updates production | Alex Chen |
| Accessory/Costume | Maya Santos | Priya Shah (story) + Maya (design doc) | Alex Chen |
| New Character | Alex Chen (decision) | Priya Shah (both bibles) | Alex Chen |
| Production Rule | Alex Chen / Lee Tanaka | Alex Chen (production bible) | Alex Chen |
| World/Location | Priya Shah (story decision) | Priya Shah (both bibles) | Alex Chen |

---

## Integration with Doc Governance Tracker

This checklist feeds into `output/production/doc_governance_tracker.md`. When a checklist item is completed, the governance tracker's "Last Updated" column for the affected document should be updated to the current cycle. When a checklist item is NOT completed in the same cycle as the change, the governance tracker should flag the document as AT RISK.

---

*Priya Shah — Story & Script Developer*
*Document: `output/production/design_to_bible_sync_checklist.md`*
*Created C49.*
