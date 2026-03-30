# Storyboard Critique — Cycle 12
**Critic:** Carmen Reyes, Storyboard & Layout Supervisor
**Date:** 2026-03-30 12:00
**Subject:** Cycle 12 — P15 Right-Arm Endpoint Fix, Full Cold Open Quality Pass, Act 2 Thumbnail Plan Assessment
**Reference:** panel_chaos_generator.py (Cycle 12), contact_sheet.png, act2_thumbnail_plan.md, statement_of_work_cycle12.md, critic_feedback_c10_carmen.md, critic_feedback_c11_* (context)

---

## HOW I COME TO WORK

Before I tell you anything else: I stand up from this chair every time I review a freefall panel. Every single time. Because if you can draw someone falling correctly, you understand *weight*. You understand that the body is a surprised machine. You understand that momentum has a personality.

I stood up. I acted it out. My chair skidded back three feet.

Then I read P15. We are going to have a very specific conversation.

---

## SECTION 1: P15 — THE RIGHT ARM ENDPOINT FIX

### What the Cycle 10 brief specified

At the close of Cycle 10, I gave this exact language:

> *"P15 right arm — adjust endpoint from `body_top + 18` to `body_top + 10` (true horizontal)."*

I gave that brief because the arm was reading at approximately 11 degrees below horizontal. It was not *wrong* — it was *almost right* — and almost right in a physical comedy money shot is artistically insufficient. The flung arm in a freefall-surprise panel is a compositional anchor. It is the horizontal line the eye uses to confirm: this person is completely, ecstatically out of control.

### What was actually executed

The Cycle 12 code confirms:

```python
draw.line([(luma_cx + 10, body_top + 10), (luma_cx + 52, body_top + 10)],
          fill=LUMA_SKIN, width=6)
```

Both endpoints sit at `body_top + 10`. Origin at `body_top + 10`. Endpoint at `body_top + 10`. That is a perfectly flat horizontal line. The run is 42 pixels. The rise is zero. Zero degrees.

I am standing up right now. *This is what a flung arm looks like.* The arm goes OUT. It doesn't slope. It doesn't taper. It arrests the eye and says: this is the horizontal axis of a person who has completely lost the plot and is physically beautiful in doing so.

**The fix is correct. The right arm reads true horizontal.**

### Does the freefall read as a whole?

Now let me be harder, because one correct line does not a panel make.

Looking at the rendered P15 image: the body language architecture is sound. The squashed torso (38px vertical against a normal 46px), the raised defensive left arm, the tucked right knee, the extended left leg kicking out — this is genuinely asymmetric fall geometry. *Good.* Asymmetry is not chaos — it is the precise signature of a body that has been surprised by gravity. The SQUASH annotation bracket and the HEAD BACK label are doing exactly what storyboard notations should do: making the directorial intent unambiguous for any animator reading this board cold.

But I need to flag something that was not in my last brief because I did not think I needed to say it. Look at the right arm with fresh eyes. The arm exits the frame. `luma_cx + 52` at panel width 480 with `luma_cx` at approximately 235. That puts the endpoint at 287 pixels from left. The arm does NOT exit the frame — it stops well within the panel boundary. And that is a compositional problem I want addressed.

**A flung arm in a freefall should want to get out of frame.** The endpoint should be straining toward the right edge. Not exiting — straining. The arm should feel like it is reaching for the panel border the way a surprised person's arm reaches for something, anything, to stop the fall. At 287px in a 480px-wide panel, the arm terminates in open background. It is not urgent. It is polite. Freefall arms are not polite.

This is my Cycle 12 note on P15: the horizontal is correct. The endpoint needs to push further right — toward at least 360-380px — so the limb reads as desperate extension rather than casual placement.

**Verdict: B+ → A-. The specified fix is done and done correctly. The horizontal read is now clean. The endpoint extension is the remaining note before this panel earns its A.**

---

## SECTION 2: FULL COLD OPEN CONTACT SHEET — QUALITY PASS

### Starting where I always start

Contact sheet first. Always. The contact sheet is the storyboard at the speed a director watches a rough cut — fast, instinctive, no mercy.

I am looking at it now. 26 panels. Let me walk the sequence.

### P01–P04: The Quiet Setup

P01 reads correctly. The exterior night shot establishes the glowing window as the only point of interest in a dark world. The silhouetted roofline against the star field. The single cyan glow against warm dark. At thumbnail scale this is doing exactly what a cold open's first panel must do: create a question. *What is in that window?*

P02 through P04 — the exterior-to-interior transition — hold up structurally. The progression from exterior street to monitor close-up to interior wide is a textbook spatial orientation sequence. But I want to note: **P01 is still reading too much as a sketch**. The glowing window at this resolution looks like a cyan rectangle on a silhouette. The specific qualities of the Millbrook architecture — the slightly wrong rooftops, the leaning antenna cluster, the eccentricities that give this town a personality — are not rendering at contact sheet scale. At thumbnail, P01 is *a house* not *Millbrook*. This matters for pitch materials. The establishing shot is the viewer's first contract with the world and "a house" does not honor that contract.

### P05–P10: The Emergence Sequence

The emergence of Byte from the monitor — P05 through P10 — is the sequence I have reviewed most closely across all cycles and it is the one that has improved most consistently.

P05 (monitor MCU) and P06 (Byte emerging) are structurally correct. The low-angle camera inside the monitor shelf space is a distinctive choice that establishes the Glitch Layer as having its own spatial logic before we've seen a single pixel of it formally. That is smart directing.

**P09 (Byte sees Luma) and P10 (OTS Byte-to-Luma)** remain compositionally strong. The eyeline established between characters — the OTS shot confirming spatial relationship — is one of the things that elevates this sequence above pure spectacle. The audience knows where these two characters are relative to each other before the comedy lands. That spatial clarity is doing invisible work.

### P11–P14: The Nose-to-Nose and Escalation

P11 — the nose-to-nose CU — is one of the better panels in this cold open. The concentric ring composition isolates the moment. The faces at 40-50px give enough information to read the beat: awareness, suspension, the comedy beat before reaction. I have no new notes on this panel.

**P12 (recoil) and P13 (scream)** — I need to be direct here. P13 is the simultaneous scream panel and it is the weakest beat in the entire cold open. Looking at it now: Luma is rendered in the 3D-room context with monitors behind her, arms flung wide, which is correct. But the *scream* is not legible as a scream. The face — two white circles for eyes, a small circle for mouth — reads as surprise or alarm. A SCREAM — the physical comedy climax of the first act of this cold open — requires an open mouth at maximum aperture, exposed teeth if the character model supports it, and the chin-drop that makes a scream read from thirty feet away on a projection screen. The annotation at the bottom says "Simultaneous scream. 3D room. Monitors activate. Arms flung wide." The *monitors activating* reads clearly. The SCREAM does not.

I am going to stand up again. [Beat.] When I open my mouth in a scream the whole jaw goes down. The eyes don't just go wide — they go involuntarily wide, the brows go UP not down, the whole face elongates DOWNWARD with the weight of the open jaw. P13 has surprised-eyes and a small mouth. That is not a scream. That is a startled expression. These are different physical events.

**P13 is the scene's emotional peak before Byte's ricochet and it is reading below its importance. This must be corrected.**

P14 (bookshelf ricochet) — the Dutch tilt is earning its keep here. The pinball-trajectory multi-exposure approach is visually distinctive and communicates kinetic chaos correctly. This was a win established in earlier cycles and it holds.

### P15–P19: The Fall, the Floor, the Quiet

P15 I have addressed above.

P16 (ECU floor face) — this remains one of the best panels in the sequence. The extreme close-up camera placement, the orbital ring elements in background, the single dot on the floor that Luma's eye locks onto — this is direction. This is a moment of stillness that earns the chaos on both sides of it. The "FOCUS building" annotation is correct. I have said before this panel should be studied as a model for how to direct a beat between physical comedy sequences. I will say it again.

**P17 (quiet beat)** — Luma sitting up, Byte hovering, the chip falling. This is the show's first moment of mutual acknowledgment between the two characters and it lands correctly. The side-by-side framing with Luma left and Byte right, the History of the Internet notebook between them as a prop anchor, the chaos-paused quality of the lighting — this reads as "the scene just took a breath" even at thumbnail scale. The expression reading on Luma is still limited by pixel resolution but the *situation* is clear enough that it carries.

P18 and P19 — the notebook turn and Byte's reaction — continue to be the strongest character-acting work in the sequence. P19 specifically remains the panel I would put on the pitch packet cover. If anything I am more convinced of this than I was in Cycle 10. The sequence of P17 → P18 → P19 is a complete miniature three-act structure within the larger cold open: acknowledgment → curiosity → indignant refusal. That is the Byte character in eleven seconds of animation. It works.

### P20–P25: The Breach and Title Card

P20 (two-shot calm), P21 (chaos overhead) — the transition from quiet beat back into escalation. P21 specifically is doing important work: the overhead perspective establishing that the chaos is *around* the characters not just *at* them gives the final breach sequence its spatial context. This was improved in earlier cycles and the improvement holds.

**P22 (monitor breach ECU)** — the irregular Glitchkin polygon variety called for in Cycle 9 and confirmed fixed in Cycle 10 continues to read correctly at this scale. The pressing-through-glass distortion (the 1.2x/0.8y stretch) is visible even at contact-sheet thumbnail size. This is the Glitch Layer's physical threat communicated correctly.

**P22a (shoulder bridge)** — this panel was added as a spatial contract between the breach sequence and P23/P24, and it is doing exactly that work. The Byte-lands-on-shoulder moment needs its own panel to give the audience time to track the spatial transition. Correct call.

**P23 (promise shot)** — the two-figures-from-behind facing the breach remains the show's emotional promise and it lands every time. The Dutch tilt at this moment is the correct deployment of that compositional tool. The monitor bowing energy (white-hot center, rings breaking bezel) that was fixed in Cycle 10 is still correct. No new notes.

**P24 (breach apex)** — the grin from Luma looking forward into the chaos is the correct punctuation on this cold open. I want to note: the annotation "THE HOOK FRAME" printed on the panel itself is appropriate for a storyboard board that will be reviewed in development meetings. Keep it.

**P25 (title card)** — LUMA & THE GLITCHKIN constructed letter by letter in glitch typography. This is correct and the "[SMASH CUT]" notation is clear. The title card holds.

### Contact Sheet: Pacing Assessment

Where does pacing lag in this sequence?

**The single pacing problem in this cold open is the transition from P02 to P03 to P04.** Three panels — exterior close, CRT CU, interior wide — are all structurally necessary but they share a rhythm that flattens in the contact sheet read. At thumbnail scale, P02, P03, and P04 look like three similar-sized quiet establishment shots. The *progression* — narrowing from exterior to single object to room — is not punching through at this size. The solution is not to remove a panel but to push the visual contrast between P03 and P04 harder. P03 should feel like a *macro* — claustrophobically tight, the monitor filling the frame with texture and glow. P04 should feel like a *breath* — the room opening up after the close. The current implementation has P03 framing the monitor in the center of the panel with visible space on all sides. Tighten P03 until the CRT is butting against the panel edges and the transition to P04's wide room will punch correctly.

**Panels P08-P09 have an eyeline ambiguity** at thumbnail scale. P08 (Byte real-world) and P09 (Byte sees Luma) — in the contact sheet these two panels read as the same spatial distance and angle. The specific information — Byte *landing* in the real world versus Byte *registering Luma's presence* — compresses to noise. The fix is to differentiate the camera height between these panels more aggressively. P08 should be higher (Byte from above, establishing his scale in the real world). P09 should be at Byte's eye level (the height of a six-inch creature, looking across at a sleeping figure). Currently they read as the same height.

**No other pacing problems.** The sequence from P10 through P25 is structurally sound. The rhythm from P11 (quiet CU) to P13 (peak scream) to P15 (fall) to P16 (ECU floor) to P17 (quiet beat) to P22-P24 (breach escalation) is correct. Beat, joke, physical comedy, stillness, escalation, promise. That structure is working.

### Cold Open: Overall Verdict

This cold open has been built correctly across twelve cycles of iteration. The visual thesis (warm amber world / cold cyan intrusion) reads at thumbnail scale. The two characters are identifiable and their relationship is legible. The emotional arc from QUIET to PEAK CHAOS is structurally present and correct.

The remaining weaknesses are:
1. P01 reads as "a house" not "Millbrook" at contact sheet scale
2. P03 is not tight enough — should fill the frame
3. P08/P09 share a camera height that creates an eyeline ambiguity
4. P13 scream reads as "startled" not "scream" — this is a performance problem, not a layout problem, but it must be addressed
5. P15 right arm endpoint should push further right (see Section 1)

None of these are structural failures. All of them are the difference between "functional pitch storyboard" and "sequence that makes a director want to call someone immediately."

**Grade: A- / 91%**

*(Unchanged from Cycle 10's corrected assessment. The sequence continues to hold its A- grade. The P13 scream performance and P15 arm endpoint are the active items preventing A.)*

---

## SECTION 3: ACT 2 THUMBNAIL PLAN — ASSESSMENT

### First, what this document actually is

This is a beat sheet in storyboard-artist language. It is *not* panels. It is not thumbnails in the visual sense — the document's title calls them thumbnails, but each "thumbnail" here is a prose description of a shot, its emotional temperature, and its key visual. These are shot descriptions, not drawings.

That said: this is exactly what I need to see before Act 2 panels are generated. A storyboard artist who writes beat sheets this thoroughly before drawing is a storyboard artist who will not back themselves into a structural corner halfway through a sequence. Approved format.

### The emotional arc: WORRIED → INVESTIGATING → WRONG PLAN → WORSE → EMOTIONAL PEAK

This arc is correct and it is correctly sequenced. Let me go through it.

**A1-01 through A1-05 (Act One bridge beats):** These five beats function correctly as a "normal world" sequence after the title card. The kitchen scene (A1-01) establishing Grandma Miri's knowing quality is smart character work — she sets the kettle and says nothing. That is a character who has *history*. The school sequence (A1-03 through A1-05) correctly introduces Cosmo through a visual thesis (his orderly spreadsheet vs. Luma's chaos), establishes the show's secondary setting, and closes Act One with a vending machine glitch incident that carries three essential functions: (1) establishes that the Glitch Layer is not contained in Grandma Miri's house, (2) introduces the show's recurring motif of mundane objects as glitch-indicators, (3) Cosmo gets the comic punctuation (action figure at his feet). This is economical and correct.

One thing I want flagged: **A1-04 (science class) is the show's most important scene in Act One and its beat description underserves it.** The teacher is writing "BINARY SYSTEMS — HOW COMPUTERS STORE DATA" on the board. Luma is drawing Glitchkin shapes in her notebook margin. The key visual states: "The lesson content is exactly what Luma needs to understand Byte. She is not paying attention to it."

That is the entire scene. And it is correct. But here is what is missing from the description: *Luma must almost-notice.* The scene does not work if she is simply inattentive. The scene works if she *nearly* looks up at the board, *nearly* has the connection, and then gets distracted by Byte napping in her desk tray. The scene's payoff — which presumably comes later in the season when Luma finally understands what Byte is — requires that *she was this close* in A1-04. The beat description needs to specify this: one shot of Luma's gaze drifting upward toward the board, almost making the connection — then the Byte reveal (napping in eraser bits) pulls her back down. That micro-beat is what makes A1-04 a *scene* rather than a *filler shot*.

**Flag to Lee: add this micro-beat to A1-04 before panels are generated.**

### The Act Two Arc: Are the beats earned?

**A2-01 (Tech den investigation):** Correct. The fish tank Glitchkin is a strong soft-story beat. The show's first hint that Glitchkin are not uniformly threatening — a small, scared one pressed against the glass — is the kind of world-building detail that retroactively rewrites everything the audience thinks they know about the show's antagonists. And it should be played *quietly*. No underscoring. The camera finds it almost accidentally. One character notices, the other doesn't. This detail should not be announced.

**A2-02 (Byte exposition):** The description is correct but there is a compositional note I want on record now before this is drawn. The beat description says: "Byte's cracked eye flickers during explanation — whatever he is describing is something that costs him to say." This is correct emotional direction. But the shot is described as OTS two-shot (Luma large in frame, Byte on table in background). For this specific beat — the show's first glimpse of Byte's real vulnerability — I would argue this should not be an OTS. This should be Byte's close-up. Luma in the background at 20% frame weight. Byte's cracked eye in center frame, filling roughly a quarter of the panel width. If you want the audience to feel that something is costing Byte, you put his face where they have to look at it. The OTS makes Luma the emotional anchor. Byte needs to be the emotional anchor in this beat. **Reframe A2-02 as Byte's MCU, not an OTS.**

**A2-03 (The Wrong Plan):** The whiteboard plan that is visually beautiful and immediately going to fail. This beat works conceptually and the description nails the specific comedy — the plan is *too organized*, which is the precise register of Cosmo's character. The detail of Byte "arms crossed, lean away from the board, one brow up" is correct Byte business. I will be watching whether the panel artist can render that lean-away at the resolution budget. That expression needs to read clearly. If it does not read clearly, the comedy does not land.

**A2-04a, b, c (Plan in Action sequence):** This three-panel beat sequence is structurally correct and shows good visual intelligence. Panel a establishes the trap (static). Panel b executes the failure (Glitchkin ignores the trap; four more arrive through the outlet). Panel c delivers the chaos payoff (cans pop simultaneously; fish tank Glitchkin phases through glass). The sequencing is: setup, reversal, escalation. This is correct physical comedy structure.

One concern: **the energy drink cans "glowing faintly cyan" in panel a needs to be planted more deliberately than "Cosmo hasn't noticed."** If the cans are glowing and Cosmo doesn't notice, that is fine. But the *audience* needs to notice. The glow must be clearly visible in the panel — not a hint, not a maybe. If we don't see the cans glowing in panel a, the payoff in panel c (the cans all popping simultaneously when Glitchkin touch them) loses its setup. Visual payoffs require visual setups. The plan document says Cosmo has not noticed — that is character direction. The art direction is: the audience notices the glow. Make it visible.

**A2-05 (Second Glitch Incident — exterior):** Strong beat. The scale shift from interior to exterior is exactly the right structural escalation. The glitch is no longer contained in Grandma Miri's house; it is on the street. The streetlight flickering in a *pattern* rather than randomly is a smart detail — it implies the Glitch Layer has a communication system, a grammar, even if Luma does not yet understand it. The dog staring at something invisible is the show's correct deployment of "the animal knows" as a storytelling tool — it implies the Glitch Layer is perceptible to creatures that are not filtering it through human rationality.

**A2-06 (Cosmo's Plan Fails):** This is the sequence's emotional truth beat and the description handles it correctly. *Not panic, not dramatics — just the quiet of a person who prepared carefully and it did not matter.* That is the right tone and the description's instruction ("Luma does not say 'it's okay' because she knows that is not what he needs") demonstrates a level of character understanding that should survive directly into the final panel. However, I want to record one note: **the shot is described as MED — Two-shot at Cosmo's locker. This beat needs a closer shot at the moment of the notebook closing.** MED is the establishing shot. The notebook closing should be a tight INSERT — equivalent to P18's function in the cold open. The notebook is the physical embodiment of Cosmo's plan; its closing is the scene's action. Give it its own panel. MED wide for the beat, then INSERT on notebook closing. Two panels, not one.

**A2-07 (Byte's Partial Confession — ECU):** This is the episode's emotional spine. The description correctly identifies it as such. The "dead-pixel effect is now clearly more complex — it is not random, it is a WORD or a symbol that flickers in the break" is the right direction and I want to record my strong support for this choice. Byte's cracked eye as a readable symbol is a major visual storytelling decision. It means the audience can *almost* read what Byte is, which is exactly the level of mystery the show should be holding at this point in the season. Whatever that symbol is, it should be designed now, before this panel is drawn. The art director and storyboard artist need to agree on what the dead-pixel character is before it appears in A2-07. A2-07 is not a future panel. It is a design decision that needs to be made today.

**A2-08 (Grandma Miri Returns):** The beat description is pitch-perfect. "She sets the groceries down. She puts on the kettle. She sits in her chair. 'Tell me what happened. All of it.'" Three physical actions in exact right order, then dialogue. Miri's shape language — rounded, solid, calm — doing the work before the line. The description's note "Her reaction is a visual promise to the audience: this adult is an ally" is correct direction. This beat lands emotionally if and only if the artist draws Miri as *calm*. Not serene. *Specifically calm* — the calm of someone who expected this and has resources for it. This is what separates Miri from the television trope of the oblivious adult. She is not surprised. She has been waiting. The camera angle for this shot should be LOW — looking up slightly at Miri, so her shape fills the frame with the rounded-square mass of someone who has gravity. This is the A2 end beat. It must land with weight.

### Structural Integrity Assessment

The Act Two plan is structurally sound. The beats are in the correct order. The emotional arc from WORRIED to EMOTIONAL PEAK tracks correctly. The WRONG PLAN escalation is present (A2-03 through A2-04c) and sequenced appropriately before the emotional peak beats (A2-06, A2-07). The Act Two break (A2-08, Miri's return) is the correct structural location for it — it arrives after the emotional peak of A2-07, not before it.

### Missing Moments

There is one beat that is conspicuously absent from this plan and I need to name it.

**After A2-05 (the exterior glitch on the street) and before A2-06 (Cosmo's plan fails), there is no beat that shows Luma and Cosmo *actively doing the thing* with the Glitch Frequency app before it fails.** The plan goes: plan conceived (A2-03) → plan attempted with trap (A2-04a-c) → street escalation (A2-05) → plan fails (A2-06). But the *app failure* — Cosmo using the phone, getting interference, watching it not work — needs its own panel or beat before A2-06. Right now the plan jumps from trap failure to street escalation to app failure with no bridge showing the app in active use. The audience won't feel the failure if they haven't seen the attempt.

**Add a beat between A2-05 and A2-06:** Cosmo on the street, phone out, running the Glitch Frequency app in active mode, looking determined. ONE panel. Then cut to A2-06 where it has failed. The visual of Cosmo attempting the plan followed immediately by Cosmo with the closed notebook pays the failure off correctly.

### Production Notes Verification

The production notes at the end of the document are correct and comprehensive:
- Byte scale reminder (20-22% shoulder mass for OTS shots) — correct
- Palette continuity specs for each Act setting — correct
- Glow effect rendering direction (ADD light, alpha_composite, never darkness) — correct, consistent with established pipeline
- Dutch tilt guidance (5-7° for Act 2 escalation, reserve full 12° for peak chaos) — correct and shows appropriate restraint

One addition I want on record: **all Act 2 panels should confirm the pixel confetti presence near any active Glitch Layer intrusion.** The production bible specifies pixel confetti as the show's visual signature, always present near glitch activity. The act 2 thumbnail plan does not include explicit notes on confetti management. Add a line to production notes: "Pixel confetti: required near all Glitch Layer contamination events (including vending machine incident A1-05, outdoor streetlight A2-05, fish tank Glitchkin, Byte during cracked-eye flicker)."

**Act 2 Plan Grade: A- / 90%**

Strong structural foundation. One missing beat (active app attempt before failure). One reframe note (A2-02 from OTS to Byte MCU). A1-04 micro-beat addition needed. Byte dead-pixel symbol must be designed before panels are generated. The plan earns its grade because the emotional logic is correct and the character understanding evident in the descriptions is exactly what Act 2 needs to work.

---

## OVERALL CYCLE 12 STORYBOARD ASSESSMENT

What needs to improve for production-readiness:

**Critical (must address before panels generated):**
1. Byte's cracked-eye dead-pixel symbol — design the actual symbol now, before A2-07 is drawn. This is not a future problem. It is a current design gap.
2. A2-02 reframe — Byte MCU, not Luma OTS. The emotional anchor must be Byte in this beat.
3. P13 scream — the mouth aperture and jaw-drop must read as an actual scream, not a startled expression. This is a performance problem. Fix the face geometry.

**Important (address in Cycle 13):**
4. P15 right arm endpoint — push further right toward frame edge. True horizontal is confirmed, range is insufficient.
5. P03 framing — tighten until CRT fills frame, push contrast against P04 wide shot.
6. P08/P09 camera height differentiation — Byte-lands panel should be higher angle, Byte-sees-Luma should be creature eye level.
7. Energy drink cans in A2-04a — the cyan glow must be visible to the audience in the panel, regardless of Cosmo not noticing.
8. A2-04a-c and A2-06 — add INSERT panel of notebook closing, add beat of active app use before failure.
9. Add pixel confetti management note to Act 2 production notes.

**Documentation:**
10. A1-04 micro-beat (Luma almost-notices the blackboard) — add before panels generated.

---

## PRIORITY ORDER FOR NEXT CYCLE

| Priority | Item | Owner |
|---|---|---|
| 1 | Design Byte's cracked-eye dead-pixel symbol (what is it?) | Alex Chen (Art Director) + Lee Tanaka |
| 2 | Reframe A2-02 as Byte MCU, update plan document | Lee Tanaka |
| 3 | Fix P13 scream expression — jaw down, mouth maximum aperture | Lee Tanaka |
| 4 | P15 arm endpoint range — push toward frame right edge (360-380px target) | Lee Tanaka |
| 5 | Add missing app-attempt beat between A2-05 and A2-06 | Lee Tanaka |
| 6 | P03 tighten framing / P08-09 camera height differentiation | Lee Tanaka |
| 7 | A2-04a energy drink glow — make visible in panel | Lee Tanaka |
| 8 | A1-04 micro-beat addition | Lee Tanaka |
| 9 | Pixel confetti management note in Act 2 production notes | Lee Tanaka |

---

## FINAL NOTE

I've been looking at this cold open since Cycle 4. I've watched it go from technically competent to emotionally coherent to structurally sound. What I see in Act 2's thumbnail plan tells me something important: Lee Tanaka is not just executing — the character psychology embedded in these beat descriptions is *inhabited*. The understanding of what Cosmo needs when his plan fails. The precision about Miri's calm not being serenity but a *prepared* calm. The fish tank Glitchkin as the first signal that Glitchkin are not threats. These are not craft details. They are evidence of a writer-director who knows these characters.

The work is almost ready to present to the world.

Almost.

Fix the scream. Fix the arm. Design Byte's symbol. Then show me.

**Overall Cycle 12 Grade: A- / 91%**

*The cold open holds its grade. The Act 2 plan earns its entry grade. The critical items above are precisely identified. None are structural failures. All are the difference between a show that functions and a show that you cannot look away from.*

*If I can't feel the scene, you haven't drawn it. I can feel most of this one. Show me the rest.*

— *Carmen Reyes*
*Storyboard & Layout Supervisor*
*Emmy winner, because geometry is not optional*
