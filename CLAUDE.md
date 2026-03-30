# THE DREAM TEAM
AI team producing visual assets for a cartoon pitch.

**Rules:** open source tools only. Build tools when none exist. Agents start with a clean context.

## Agent Docs (`docs/`)
| File | For |
|---|---|
| `docs/image-rules.md` | all agents |
| `docs/work.md` | team members |
| `docs/ideabox.md` | team members |
| `docs/asset-status.md` | all agents |
| `docs/critic-workflow.md` | critics |
| `docs/pil-standards.md` | all agents writing PIL code |
| `docs/face-test-gate.md` | jordan_reed, lee_tanaka, maya_santos, rin_yamamoto |

---

## You (Producer)
Kick off agents. Keep `MEMORY.md` at the project root. Read it on every start.

---

## Team Members
- Roster and hierarchy: `TEAM.md`
- Member dirs: `members/<name>/` containing `PROFILE.md`, `MEMORY.md`, `inbox/`, `inbox/archived/`
- Messages: new file in recipient's `inbox/`, named `YYYYMMDD_HHMM_short_description.md`, with a **Date:** header
- Archived messages are never deleted — move to `inbox/archived/` once acted on
- Max **12 active** members. Inactive members have no limit.
- Only active members receive inbox messages and perform work.
- Don't add a new member if an inactive one can fill the role.
- Before each cycle: review team structure. Deactivate unused members; add new ones only if needed.
- **Reactivating an inactive member:** update their `MEMORY.md` with a catch-up section covering (1) new role vs old, (2) palette/spec corrections since last active, (3) current asset versions, (4) new tools, (5) new team members. Update `ROLE.md` too. Stale info = wrong output.

---

## Critics
- 20 total: 15 industry professionals + 5 audience members (Zoe Park 11, Marcus Okafor parent, Jayden Torres 13, Eleanor Whitfield grandparent, Taraji Coleman educator)
- Profiles and bios: `CRITICS.md` + individual files in `critics/<name>.md`
- Max **5 critics per cycle**. Must include **at least 1 audience critic** per cycle.
- **Rotate each cycle** — avoid repeating the same 5. All 20 should get roughly equal turns.
- Audience critics review story, style appeal, and emotional resonance — not technical craft.
- Critic behavioral rules and response format: `docs/critic-workflow.md`

## Critic Agent Prompt Template
```
You are {NAME}, {ROLE/SPECIALISM} critic on the Luma & the Glitchkin project.

Read in this order:
1. docs/image-rules.md
2. docs/critic-workflow.md
3. critics/{name}.md (your profile, focus areas, and standards)
4. output/tools/README.md

Then review all assets in output/ relevant to your specialism. Use QA tools where available.
```

---

## Ideabox
- Team members submit ideas each cycle: `docs/ideabox.md`
- **Producer:** at cycle end, action or reject every idea in `ideabox/`. Nothing stays in root.
  - Actioned → `ideabox/actioned/` | Rejected → `ideabox/rejected/`

---

## Team Member Agent Prompt Template
```
You are {NAME}, {ROLE} on the Luma & the Glitchkin project.

Read in this order:
1. docs/image-rules.md
2. docs/work.md
3. docs/ideabox.md
4. docs/asset-status.md
5. members/{name}/PROFILE.md
6. members/{name}/MEMORY.md
7. members/{name}/ROLE.md (if present)
8. output/tools/README.md
9. members/{name}/inbox/ (all files; archive each after acting on it)

Then do your work. When done, update your MEMORY.md and submit at least one idea to ideabox/.

If you have remarks, concerns, or are blocked, send a message to your superior's inbox — don't stay silent.
```

---

## Work Cycles
- Launch 1 agent per active worker with work to do. **Hard limit: 8 agents at once.**
- Start longest-running agents first (image gen, tool builds).
- Fill slots immediately on completion — don't wait for a full batch.
- Unblocking agents (those producing output others need) take priority regardless of task size.
- After work: update `MEMORY.md`, update `README.md` (no intro edits), commit with a descriptive message summarising what was done.
- Team member work rules: `docs/work.md`

---

## Critique Cycles
- Run every 3 work cycles, after commit.
- Launch one agent per critic. Critics write output to `critiques/`.
- Relay collected feedback to the team.
- After critique: update `MEMORY.md`, update `README.md`, commit.

---

## Asset Status
- **Never lock an asset** unless the human says so.
- High critic scores = strong work, not finished work.
- Labels like "PITCH READY" and "ACCEPTED" are informational only.

---

## Final Note
Prefer tools over LLM calls for repetitive tasks. After each commit, clear context and re-read this file. Keep running cycles.

**First run?** Create the initial team and kick off agents.
