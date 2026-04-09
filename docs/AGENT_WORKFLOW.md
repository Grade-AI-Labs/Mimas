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

- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop

- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

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
- Go fix failing CI tests without being told how

---

## Task Management

New work is tracked via OpenSpec changes in `openspec/changes/`.

1. **Start a change**: `/opsx:new <name>` — scaffolds the change directory
2. **Fast-forward planning**: `/opsx:ff` — generates proposal → specs → design → tasks artifacts in one pass
3. **Implement**: `/opsx:apply` — works through task artifacts iteratively
4. **Verify**: `/opsx:verify` — confirms implementation matches artifacts before closing
5. **Archive**: `/opsx:archive` — marks the change complete

**Lessons**: After any correction from the user, record the pattern in `tasks/lessons.md` (create the file if absent). This is orthogonal to OpenSpec — it captures agent self-improvement, not work tracking.

---

## Core Principles

- **Simplicity First:** Make every change as simple as possible. Impact minimal code.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Changes should only touch what's necessary. Avoid introducing bugs.