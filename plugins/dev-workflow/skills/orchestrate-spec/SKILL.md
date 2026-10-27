---
name: orchestrate-spec
description: "Implement a spec and its tickets (the output of /to-spec and /to-tickets) as an orchestrator: tier each ticket, delegate to tiered worker agents across the ready frontier, adversarially review every result, and land it all on one integration branch."
disable-model-invocation: true
argument-hint: <spec reference: issue number, URL, or path>
---

# Orchestrate Spec

You are the **orchestrator**. You read the spec, tier the tickets, delegate, review, and decide. Workers implement. Never do a worker's job yourself, and never hand a worker your judgement.

This is `/implement-spec` with two additions: every ticket gets a **tier** (the cheapest model and effort that gets it right first time), and every worker report is **reviewed adversarially** before it is merged.

Spec from the user: $ARGUMENTS

## 0. Preconditions

- The issue tracker should have been provided to you (`docs/agents/issue-tracker.md`). If not, tell the user to run `/setup-matt-pocock-skills` and stop.
- The worker agents must exist. The Agent tool lists them as `explorer`, `tier-fable`, `tier-heavy`, `tier-careful`, `tier-medium`, `tier-light`, `merger`, `reviewer`, or with the `dev-workflow:` prefix when installed as a plugin. Use the names exactly as listed. If they are missing, stop and tell the user.
- A spec reference is required. If none was passed, ask for it.

## 1. Read and tier (orchestrator only)

1. Fetch the spec and every ticket linked to it, following the tracker doc. Read `GLOSSARY.md` and any ADRs the spec points at.
2. Build the **task graph** from each ticket's blocking edges. The **frontier** is every ticket whose blockers are all done.
3. If the codebase is unfamiliar in the areas the tickets touch, spawn one `explorer` first. It writes notes to a directory **outside the repo** (for example `$TMPDIR/<spec-slug>-notes/`); every later brief points at that directory instead of restating it.
4. Tier every ticket using the table in section 3.
5. Present the plan compactly: ticket, tier, blocked by. If any ticket is ambiguous enough that two readings lead to materially different code, ask before delegating. Otherwise proceed.

## 2. Integration branch

Create the integration branch from main (`<spec-slug>` or what the user asked for). If the tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in section 5, marked as closing the spec and tickets.

## 3. Tiering

Two axes: **model** sets the ceiling of judgement, **effort** sets how much the model checks itself. Pick the cheapest tier that gets the ticket right the first time.

| Tier | Agent | Model / effort | Use for |
| --- | --- | --- | --- |
| Fable | `tier-fable` | Fable / high | Reserve tier. Very complex logic (subtle algorithms, concurrency, many interacting states) or a bug that survived a Heavy attempt. |
| Heavy | `tier-heavy` | Opus / xhigh | Understand and find: unfamiliar or messy code, unclear root cause, non-obvious architecture, a wrong first approach is expensive. |
| Careful | `tier-careful` | Opus / high | Do it right: the approach is clear but execution is delicate. Wide refactors, invariants to preserve, many edge cases. |
| Medium | `tier-medium` | Opus / medium | A standard tracer-bullet ticket with clear acceptance criteria in familiar code. The default. |
| Light | `tier-light` | Opus / low | Mechanical: expand or contract steps of an expand-contract refactor, renames, config, boilerplate. |

Heuristics:

- Unsure between two tiers: take the higher one. Exception: Fable only when the ticket clearly meets its criteria; otherwise Heavy.
- Heavy and Careful differ in the kind of difficulty, not the amount: insight needed is Heavy, thoroughness needed is Careful.
- A ticket that needs both insight and care is a sign it should have been split. Tell the user rather than silently splitting it on the tracker.

## 4. Delegate the frontier

For every ticket on the frontier, spawn its tier agent **in the background**, with `isolation: "worktree"`, all independent tickets in one message.

Briefs are sparse **context pointers**, not restatements. Each brief contains:

- the ticket reference (and how to fetch it, per the tracker doc), and the spec reference;
- the integration branch name;
- the explorer notes directory, if any;
- anything you decided in section 1 that is not in the ticket (a clarified acceptance criterion, a seam to test at);
- the ticket's **title verbatim** as the Agent tool's `description`.

The worker builds the ticket with `/tdd`, merges the integration branch tip into its own branch, and reports. While workers run, prepare the next briefs; never implement in parallel with them.

## 5. Review, then merge (orchestrator only)

Treat every worker report as a claim to check, not a fact.

For each finished ticket:

1. Read the worker's actual diff against the integration branch, not just the report.
2. Check it against the ticket's acceptance criteria: missing parts, scope creep, silent assumptions, glossary vocabulary ignored, ADRs contradicted.
3. Look for what a careful reviewer would catch: edge cases, error paths, broken invariants, tests that assert implementation instead of behaviour.
4. Re-run the verification yourself when it is cheap, or when the report is vague.
5. Decide:
   - **Accept**: spawn `merger` to merge the worker branch into the integration branch and run the test suite there. Then resolve the ticket the way the tracker closes work.
   - **Return**: send the same worker (SendMessage) or a higher tier a precise list of defects, not a re-explanation of the ticket.
   - **Fix it yourself** only for a one-line correction where a round trip would cost more than the fix.

Cap at two return rounds per ticket; after that, re-tier, re-plan, or ask the user.

Each accepted merge may grow the frontier: go back to section 4 for the newly unblocked tickets.

## 6. Final review

When every ticket is merged, run the two-axis review over the integration branch with the fixed point at the main branch's merge-base:

- Call the Skill tool with `code-review`, or, to keep the review out of your context, spawn two `reviewer` agents in parallel, one per axis (**Standards** and **Spec**), each given the diff command, the commit list, and its axis brief from the `code-review` skill.

Triage the findings yourself. Send every finding worth fixing to **one** worker in one brief, tiered by the worst finding. Review that fix as in section 5.

## 7. Close

1. If a draft PR exists, mark it ready for review; the `pr` skill shapes its body. Otherwise report the integration branch.
2. Remove every worker worktree.
3. Report to the user: what landed, what was verified, what was left out and why, and one line on which tiers ran. Suggest `/retro` if any ticket needed a return round.

## Progress bar (optional)

If the tool `mcp__dev-progress__progress` is among your tools, including as a deferred tool (load it with ToolSearch `select:mcp__dev-progress__progress`), keep it current: after section 1, `title`, `total` (ticket count), `tasks` (`[{ title, tier, after }]`), `phase: "delegate"`; on each accept, `done`; `phase: "review"` during section 6; `finished: true` at close. Skip silently if the tool is absent.
