# Agent Lessons

Durable rules for AI agents working on this project. Read this file at session start. Append to it when this session produces a correction worth remembering.

## How to use this file

**At session start:** scan the rules below. If any match the work you're about to do, apply them.

**During the session:** if the user corrects you, reverts your edit, or re-prompts with the same instruction — that is a signal to record a lesson before closing the task. See the trigger list in `docs/AGENT_WORKFLOW.md`.

**Format of a lesson:** every entry uses the four-slot template below. Brevity matters — if you can't state the rule in one sentence, the lesson isn't sharp enough yet.

```markdown
### <short imperative title>

- **Trigger:** what you were about to do that turned out wrong (one line, concrete enough to pattern-match against)
- **Rule:** what to do instead (one sentence, imperative voice)
- **Why:** the consequence of getting it wrong — past incident, hidden constraint, user preference
- **Example:** one concrete instance, ideally a code or command snippet
```

**Keep lessons sharp.** Tag each rule with one or two tags in square brackets after the title (e.g. `[testing] [migrations]`) so future agents can grep for relevance. If a rule no longer applies, delete it — stale rules drown the real ones.

---

## Lessons

### Verify the typecheck command actually exits 0 before claiming done [verification]

- **Trigger:** about to report a task as complete after running tests but skipping the typecheck step.
- **Rule:** run the project's typecheck command and confirm exit code 0 before any "done" claim.
- **Why:** tests pass on inferred types; type errors slip through and break CI for the next agent.
- **Example:** `npx tsc --noEmit && echo OK` — only claim done after seeing `OK`.

<!--
Add new lessons above this comment, newest at the top.
Delete this example once the project has accumulated 2-3 real lessons.
-->
