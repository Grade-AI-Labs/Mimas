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

### 4. CONTEXT.md upkeep

Read `CONTEXT.md` (or `docs/CONTEXT-MAP.md` → per-subdomain `CONTEXT.md`) when working in a subdomain. Use its vocabulary verbatim **where defined** in code, tests, issues, and commits. If a needed term isn't in the glossary, treat it as a trigger (see below) rather than silently inventing a synonym; the full contract lives in `docs/AGENTS_CONTEXT.md`.

**Triggers — capture vocabulary in the moment:**

- A previously-ambiguous domain term gets a clear resolution → add it (one-sentence definition, aliases to avoid).
- User corrects your terminology → record the correct term; mark the wrong one as an alias to avoid.
- A new feature introduces a concept absent from the glossary → add it before claiming the feature done.
- You catch yourself inventing a synonym because the right term isn't there → flag the gap; don't silently coin a new term.

**Write before reporting done.** Update the relevant `CONTEXT.md` in the same turn the trigger fires. Append-only — add new entries, don't reshuffle existing ones. The format is documented at the top of each `CONTEXT.md`. See `docs/AGENTS_CONTEXT.md` for the full contract.

### 5. ADR upkeep

Read `docs/adr/` when about to change anything that crosses an existing decision boundary. If your work would contradict an ADR, surface it explicitly — never silently override.

**Triggers — write an ADR only when all three apply:**

- **Hard to reverse** (schema migration, framework swap, integration redesign).
- **Surprising without context** (future engineers will question the approach).
- **Result of genuine trade-offs** (real alternatives existed and you chose deliberately).

If all three apply: write the ADR in the same turn as the decision. Next number (4-digit zero-padded), kebab-case slug, Nygard short form — see `docs/adr/0001-record-architectural-decisions.md` for the canonical example and `docs/AGENTS_ADRS.md` for the contract. If any of the three is missing: don't write one.

**Supersede, don't delete.** Overturned decisions get a new ADR; the old one stays with a `Superseded by ADR-NNNN` note.

### 6. Verification Before Done

- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 7. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 8. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user

---

{{PLATFORM_SECTION}}

## Core Principles

- **Simplicity First:** Make every change as simple as possible. Impact minimal code.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Changes should only touch what's necessary. Avoid introducing bugs.
