# dev-progress

A Claude Code mod: a progress bar above the prompt and a live panel of subagents, made for [`dev-workflow`](../dev-workflow)'s `/orchestrate-spec` and useful with any subagents.

Forked from [savvy-progress](https://github.com/JohnnyVizz/claude-kit/tree/main/plugins/savvy-progress) by johnnyvizz (MIT, see `LICENSE-claude-kit`). The drawing, cost estimate and step reporting are unchanged; what changed is which agents it recognises and the names of its tools.

## Install

```
/plugin marketplace add Grade-AI-Labs/Mimas
/plugin install dev-progress@mimas
```

Or in one step: `/plugin install dev-progress --marketplace Grade-AI-Labs/Mimas`. Restart the session afterwards.

Mods are built on function hooks (`hooks/register.tsx`), an early-access Claude Code API that may change between releases. If the mod does not show up after installing, load it by hand for one session with `claude --plugin-dir <clone>/plugins/dev-progress`, or for every session through `env` in `~/.claude/settings.json`:

```json
{ "env": { "CLAUDE_CODE_PLUGIN_DIRS": "<clone>/plugins/dev-progress" } }
```

## What it shows

- **Progress bar**: the flow's title, phase, accepted tickets out of planned, and a button with the crew size that opens the panel. It appears once `/orchestrate-spec` reports a plan or a `dev-workflow` agent starts.
- **Agents panel** (`/agents-info` toggles it; `/agents-info open` opens it without toggling): running, finished and planned subagents with model, effort, step progress, context, estimated cost and time. Each tier has its own crab costume; `explorer` is the pirate.

It recognises these agents, with or without the `dev-workflow:` prefix:

| Agent | Shown as |
| --- | --- |
| `tier-light`, `tier-medium`, `tier-careful`, `tier-heavy`, `tier-fable` | their tier, in the tier's colour |
| `explorer`, `merger`, `reviewer` | their role |
| anything else | its agent type; listed, but not briefed and does not open the panel |

## Tools it adds

- `mcp__dev-progress__progress`: the orchestrator reports the plan, phase and accepted tickets. Only the main session can; a call from a subagent is ignored.
- `mcp__dev-progress__step`: an agent reports its own steps (`done`, `total`, `note`). It is listed up front, and each `dev-workflow` agent gets one line at the end of its brief asking for these reports. An agent that does not report shows its context fill in grey instead.

Cost is a rough estimate from token counts and a built-in price table (`PRICES` in `hooks/register.tsx`), not a bill.

## Settings

`language`: `auto` (default), `en`, `ru` or `he`. `autoOpen`: `workflow` (default) opens the panel when a `dev-workflow` agent starts or a plan is reported; `any` also opens it, once per session, for any other subagent. Set them in `/config`, or for a mod loaded by hand:

```json
{ "pluginConfigs": { "dev-progress": { "options": { "autoOpen": "any" } } } }
```

## Overlap with other mods

If you run `subagent-tree` or another subagent panel, both will list the same agents. `context-bar` shows the main session's context; this mod shows each subagent's.

## Tests

```bash
claude plugin test plugins/dev-progress
```
