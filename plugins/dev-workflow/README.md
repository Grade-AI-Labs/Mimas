# dev-workflow

[Matt Pocock's skills](https://github.com/mattpocock/skills) for real engineering, plus the one thing they leave open: **which model does the work**. This plugin adds tiered worker agents and an orchestrator, `/orchestrate-spec`, in the style of [savvy-flow](https://github.com/JohnnyVizz/claude-kit/tree/main/plugins/savvy-flow).

Unofficial. Not affiliated with or endorsed by Matt Pocock. His skills are MIT-licensed and forked here (see `UPSTREAM` for the commit and `LICENSE-mattpocock-skills`). They keep his repo layout; the only change is that Mimas's setup and review skills take the place of his `/setup-matt-pocock-skills`.

## Install

```
/plugin marketplace add Grade-AI-Labs/Mimas
/plugin install dev-workflow@mimas
```

Or in one step:

```
/plugin install dev-workflow --marketplace Grade-AI-Labs/Mimas
```

To offer it to everyone working in a repo, see the project-scope snippet in the [Mimas README](../../README.md#plugin-marketplace).

## What ships

- **Matt's promoted skills**, forked: `/grill-with-docs`, `/to-spec`, `/to-tickets`, `/implement`, `/implement-spec`, `/tdd`, `/code-review`, `/pr`, `/retro`, `/ask-matt` and the rest. His `/setup-matt-pocock-skills` is replaced by `/setup-agentic-repository`; see [Setup](#setup).
- **Mimas setup and review**: `/setup-agentic-repository`, `/review-policy-builder`, `/review-policy-rule-builder` and `/agentic-review`, adapted from the copies in [`skills/`](../../skills) to Matt's layout.
- **`/orchestrate-spec <spec>`**: Matt's `/implement-spec` flow (task graph, ready frontier, worktree per ticket, one integration branch, final two-axis review) with two additions:
  1. each ticket gets a **tier**, the cheapest model and effort that gets it right first time;
  2. the orchestrator **reviews every worker's diff** against the ticket before a merger lands it, and returns defects instead of merging them.
- **Agents**:

  | Agent | Model / effort | Role |
  | --- | --- | --- |
  | `explorer` | Sonnet / medium | Reads code and docs, writes notes outside the repo |
  | `tier-fable` | Fable / high | Reserve tier: hardest logic, bugs that survived Heavy |
  | `tier-heavy` | Opus / xhigh | Unfamiliar code, unclear cause |
  | `tier-careful` | Opus / high | Delicate but clear: wide refactors, invariants |
  | `tier-medium` | Opus / medium | Standard tracer-bullet ticket (default) |
  | `tier-light` | Opus / low | Mechanical: expand/contract steps, config |
  | `merger` | Opus / medium | Merges an accepted branch, aborts on judgement conflicts |
  | `reviewer` | Opus / high, read-only | One axis of `code-review` (Standards or Spec) |

  Without Fable access, change `model:` in `agents/tier-fable.md` (to `opus`, say).

## Setup

Run `/setup-agentic-repository` once per repo. It writes everything Matt's setup writes, in the same places, so his skills run unchanged, and adds the Mimas instruction tree on top:

| Path | What it is |
| --- | --- |
| `docs/agents/issue-tracker.md` | Tracker operations. Matt's GitHub, GitLab and local templates, plus Azure DevOps, Jira and Linear |
| `docs/agents/triage-labels.md`, `docs/agents/domain.md` | Matt's label table and domain-doc rules |
| `AGENTS.md` | Matt's `## Agent skills` block, a `## Modules` list, pointers and critical rules. No `CLAUDE.md`: Claude Code (v2.1.277+) reads `AGENTS.md` natively, but only while no `CLAUDE.md` exists, so setup offers to merge an existing one into `AGENTS.md` |
| `CODING_STANDARDS.md` | Coding standards: read by `/code-review` and `/agentic-review`, grown by `/retro` |
| `docs/agents/AGENT_WORKFLOW.md`, `ENGINEERING.md`, `LESSONS.md`, `FEATURES.md`, `AGENTS_FEATURES.md`, `features/` | Mimas workflow, commands, lessons and feature docs |
| `GLOSSARY.md` / `GLOSSARY-MAP.md`, `docs/adr/` | Matt's domain docs, created lazily by `/domain-modeling` |

It also offers to migrate a repo that has Mimas's older `agents-docs/` + `CONTEXT.md` layout, or Matt's pre-1.3 `CONTEXT.md` names.

## Review

`/code-review` (Matt's two axes, Standards and Spec) runs everywhere it did before: `/implement`, `/implement-spec`, `/orchestrate-spec`. It checks against `CODING_STANDARDS.md` and, once they exist, the review policies.

For stricter, module-aware review:

1. `/review-policy-builder` writes `docs/agents/review/policies/`: module-scoped and machine-checkable rules, one file per module in `AGENTS.md`'s `## Modules` (or per `GLOSSARY-MAP.md` context). `/review-policy-rule-builder` edits single rules later.
2. `/agentic-review` reviews a branch with one specialist per module against those policies and fails closed when a specialist doesn't report. When policies exist, `/orchestrate-spec` uses it for the final Standards axis.

`/retro` sends module-scoped or machine-checkable rules to `/review-policy-rule-builder`, and judgement calls to `CODING_STANDARDS.md`.

## The flow

```
/setup-agentic-repository                          (once per repo)
/grill-with-docs → /to-spec → /to-tickets          (Matt's front half)
/orchestrate-spec <spec>                           (instead of /implement-spec)
  orchestrator: read spec + tickets → tier each → delegate frontier (background, worktrees)
  per result:   review diff → accept → merger   |   return with defects (max 2 rounds)
  at the end:   code-review (2 × reviewer; agentic-review for Standards when policies exist) → one fixer → PR or branch
/retro                                             (Matt's)
```

Run the orchestrator session on your strongest model at high effort: the judgement lives there.

## With dev-progress

If the [dev-progress](../dev-progress) mod is installed, the orchestrator drives its progress bar and workers report steps to its agents panel. Without it those calls are skipped.

## Don't install twice

If you also have `mattpocock-skills` installed, every Matt skill appears twice and model-invoked ones (`tdd`, `code-review`, `grilling`...) can trigger from either. Uninstall one.
