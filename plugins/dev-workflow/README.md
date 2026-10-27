# dev-workflow

[Matt Pocock's skills](https://github.com/mattpocock/skills) for real engineering, plus the one thing they leave open: **which model does the work**. This plugin adds tiered worker agents and an orchestrator, `/orchestrate-spec`, in the style of [savvy-flow](https://github.com/JohnnyVizz/claude-kit/tree/main/plugins/savvy-flow).

Unofficial. Not affiliated with or endorsed by Matt Pocock. His skills are MIT-licensed and vendored here unchanged (see `UPSTREAM` for the commit and `LICENSE-mattpocock-skills`).

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

- **Matt's 27 promoted skills**, unchanged: `/grill-with-docs`, `/to-spec`, `/to-tickets`, `/implement`, `/implement-spec`, `/tdd`, `/code-review`, `/pr`, `/retro`, `/ask-matt` and the rest. Run `/setup-matt-pocock-skills` once per repo first.
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

## The flow

```
/grill-with-docs → /to-spec → /to-tickets          (Matt's front half, unchanged)
/orchestrate-spec <spec>                           (instead of /implement-spec)
  orchestrator: read spec + tickets → tier each → delegate frontier (background, worktrees)
  per result:   review diff → accept → merger   |   return with defects (max 2 rounds)
  at the end:   code-review (2 × reviewer) → one fixer → PR (pr skill) or branch
/retro                                             (Matt's, unchanged)
```

Run the orchestrator session on your strongest model at high effort: the judgement lives there.

## With savvy-progress

If the [savvy-progress](https://github.com/JohnnyVizz/claude-kit/tree/main/plugins/savvy-progress) mod is installed, the orchestrator drives its progress bar and workers report steps to its agents panel. Without it those calls are skipped.

## Don't install twice

If you also have `mattpocock-skills` installed, every Matt skill appears twice and model-invoked ones (`tdd`, `code-review`, `grilling`...) can trigger from either. Uninstall one.
