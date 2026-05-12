# Agent Workflow & Operating Instructions

These rules apply to **all AI agents** working on this project, regardless of platform or model.

Read this file at the start of every session.

---

## Workflow Orchestration

### 1. Plan Mode Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy

- Use subagents liberally to keep the main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop

The goal is a small, sharp file of project-specific rules in `docs/LESSONS.md` that future sessions read and apply. The format of a lesson is defined at the top of `docs/LESSONS.md` — read it before writing one.

**Read at session start.** Open `docs/LESSONS.md` and apply any rules that match the work you're about to do. This is non-optional; the file exists so the same mistake isn't made twice.

**Triggers — record a lesson when any of these happen.** Don't wait for a formal request; these are the signals:

- User says "no", "actually", "don't", "stop", "that's wrong", or "instead do X"
- User reverts, rewrites, or asks you to redo your edit
- User re-prompts you with the same or similar instruction (signal that the first attempt missed something)
- User points out a hidden constraint, past incident, or convention you didn't know
- Code review (human or `/review`) surfaces an issue caused by your approach
- You catch yourself about to do the same thing the project has been corrected on before

If unsure whether it's worth recording: write it. Sharper is better than missing, and grooming the file is cheap.

**Write before reporting done.** A session that produced a correction must produce a lesson — record it in the same turn the work is completed, not "later". The `AGENTS.md` completion checklist has a line for this; don't tick the box without it.

**Groom periodically.** When `docs/LESSONS.md` passes ~20 entries, propose consolidations to the user — merge duplicates, delete rules that no longer apply, shorten anything vague.

### 4. Verification Before Done

- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user

---

{{PLATFORM_SECTION}}

## Core Principles

- **Simplicity First:** Make every change as simple as possible. Impact minimal code.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Changes should only touch what's necessary. Avoid introducing bugs.
