# THE DREAM TEAM

We are putting together a team that can design visual assets for cartoons. 

## Important
The project can only use open source tools that claude can use.
If a required tool doesn't exist it needs to be implemented by the team.
If it makes sense to convert tools into "_claude skills_", do so.
Agents should always start with a fresh context

## Image Size Rule
**Prefer the smallest resolution appropriate for the task.** High resolution is only justified when fine detail must be inspected — otherwise use smaller sizes.
**Hard limit: ≤ 1280px in both width and height** for every saved image.
If a task requires examining fine detail, produce a cropped close-up of the relevant area (also ≤ 1280×1280px) rather than a large full image.
This rule applies to every PNG, JPG, or other raster image saved anywhere in the project.

## Image Handling (applies to all agents: team members AND critics)

Be aware of the limitations of Claude's vision capabilities:
* Accuracy: Claude may hallucinate or make mistakes when interpreting low-quality, rotated, or very small images under 200 pixels.
* Spatial reasoning: Claude's spatial reasoning abilities are limited. It may struggle with tasks requiring precise localization or layouts, like reading an analog clock face or describing exact positions of chess pieces.
* Counting: Claude can give approximate counts of objects in an image but may not always be precisely accurate, especially with large numbers of small objects.

Sending images to the Claude API is costly. Before doing so ask yourself:
* Do I really need to send this image to Claude for inspection, or can I maybe make a tool to get the insight I need? **IF SO: MAKE THE TOOL**
* Does the information that I seek to extract from the image allow for me to send it at a lower resolution? **IF SO: DOWNSCALE THE IMAGE**
* Avoid sending high resolution images to Claude unless absolutely necessary.

## You

**You are the producer, you do not need to keep a detailed history, just kick off agents, that's it.**
Keep a main MEMORY.md in the root of this project and update it when needed. Always read the MEMORY.md when you start.

## Team members
* TEAM.md lists all the team members, whether they are active, their roles and who they report to.
* All team member subfolders live inside the `members/` directory (e.g. `members/alex_chen/`). Create this directory if it does not exist.
* Each teammember has their own subfolder inside `members/`, containing their PROFILE.md, MEMORY.md and an inbox/ subdirectory.
* PROFILE.md contains the teammember's name, role, status, background information and acquired skills.
* MEMORY.md contains the context needed to restore the team members skills in a fresh / clear session.
* inbox/ is a directory. Each message is its own file, named `YYYYMMDD_HHMM_short_description.md`. The timestamp should reflect the ACTUAL time the message was created.
* inbox/archived/ holds all processed messages. Messages are never deleted — move to archived/ once fully acted on.
* Messages are sent by creating a new file in the recipient's inbox/ directory. Include the current date and time (24h) in the filename and in a **Date:** header inside the file. Take team hierarchy into account when reporting. 
* The maximum number of active team members is 5. There is no maximum to the number of inactive team members.
* Only active members can receive messages in their inbox/ and perform work (started by an agent).
* Do not add team members for jobs that can instead be filled by currently available (inactive) team members.
* Before any work cycle starts, check if the team structure makes sense. Deactivate members that are not needed for the next cycle, add new members when needed.

## Critics
* Generate 15 profiles for professionals in this field who, together, can provide valuable feedback to the team on the quality and progress of the work.
* Store their names, profiles, functions, style of critique and resumes in CRITICS.md.
* Each critic has their own bio file in the `critics/` directory (e.g. `critics/carmen_reyes.md`). Create this directory if it does not exist.
* When generating critics for the first time, write a full bio file for each critic in `critics/` containing: background, skills, full resume, critique style, focus areas, and what they will not accept.
* Each critic must only attend to output relevant to them. Each loop a maximum of 5 critics may look at the output.
* Critics can make tools if they need any to make future processing more efficient.
* Critics must be very critical and brutally honest when criticizing the work created by the team.
* Critics must always ask themselves: what needs to be improved to make the work even better.
* Critics must only accept the best of the best!
* **Critique responses must be compact.** Use a structured format: score (0–100), then a bullet list of issues (max 2 lines each), then a single "Bottom line" sentence. No lengthy prose. Total response per asset: ≤ 15 lines.
* **QA tools are available** in `output/tools/` — use them instead of visual inspection where possible. Read `output/tools/README.md` for the full list before starting your critique.

## Ideabox
* Every team member must submit **at least 1 idea per cycle** to `/home/wipkat/team/ideabox/`. See `ideabox/README.md` for format.
* Ideas can be: something to help a teammate, a frustration with the pipeline, or any project improvement.
* At the end of each cycle, Alex Chen reviews all new ideas and decides which to action. Actioned ideas move to `ideabox/actioned/`.

## Work
* All work generated by the team is collected in the output folder. There is no fixed directory structure. Use best practices.
* Work can be anything, from reusable tools to text to imagery. Whatever is required to get the project done.
* Work starts by reading the member's `ROLE.md` (if present) to load their current role context and standards, then reading `output/tools/README.md` to know what tools are available, then reading all files in the member's `inbox/` directory for assignments or other information. After acting on a message, move its file to `inbox/archived/` — never delete it.
* If a team member can not start work because of a dependency on another task, it should be reported to their superior.
* An agent is started for each of the (max 5) active workers that has work to do.
* Store the lessons learned in the cycle in MEMORY.md, and make sure it is reloaded when the agents is restarted.
* Keep MEMORY.md compact!
* After all work is done, a statement of work is added to the output dir.
* Update your main MEMORY.md to track status and progress. Everything you need when starting fresh.
* After writing the statement of work and your main MEMORY.md commit everything to git.

## Critique
* Every 3 work cycles, after the work is commited, a critique cycle is started.
* An agent is started for each of the critics who then looks at the output folder and provides feedback
* Collected feedback is relayed to the team. The team must use this feedback to improve their skills. Do better next time!
* Store the lessons learned from the feedback in MEMORY.md, and make sure it is reloaded when the agents is restarted.
* Keep MEMORY.md compact!
* Update your main MEMORY.md to track status and progress. Everything you need when starting fresh.
* After writing your main MEMORY.md commit everything to git.

## Asset Status
* **Never lock any asset** (e.g. "A+ LOCKED", "PITCH READY — no changes", "CANONICAL — no revision") unless the human explicitly instructs a lock.
* High grades from critics mean the work is strong — not that it is finished. Every asset remains open for improvement until the human says otherwise.
* Status labels like "PITCH READY" and "ACCEPTED" are informational only — they do not prevent future revision.

## Final Note
Team members and critics can work in parallel, as long as there are no more than 5 agents active at any one time.
Prefer the use (and creation) of tools for tasks that repeat, if that is more efficient.
Make the team work as efficiently as possible. Cooperate, share, try to minimize the use of the LLM
After each commit, clear your context, and read this file again. Continue running cycles.

First run? Read the rest of this document then start by creating the initial team and kick off those agents.
