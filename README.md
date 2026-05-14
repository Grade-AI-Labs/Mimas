# Mimas

A collection of agent skills for bootstrapping repositories with agent
instructions and day-to-day engineering workflows. Works with any coding
agent supported by [`vercel-labs/skills`](https://github.com/vercel-labs/skills)
— Claude Code, Cursor, Codex, OpenCode, GitHub Copilot, and 50+ others.

## Quick start

Install the `setup-agentic-repository` skill. The CLI auto-detects which agents
you have installed and asks where to put the skill:

```sh
npx skills@latest add Grade-AI-Labs/Mimas@setup-agentic-repository
```

Then, from inside the repository you want to onboard, launch your agent and
invoke the skill (`/setup-agentic-repository` in Claude Code; check your agent's
docs for its skill-invocation syntax).

## Install for a specific agent

Pass `-a <agent>` to target a single agent and skip the prompt. Add `-g` to
install globally (available across all projects) instead of into the current
project. Examples for the most common agents:

```sh
# Claude Code              — installs to .claude/skills/ (or ~/.claude/skills/ with -g)
npx skills@latest add Grade-AI-Labs/Mimas@setup-agentic-repository -a claude-code

# Cursor                   — installs to .agents/skills/ (or ~/.cursor/skills/ with -g)
npx skills@latest add Grade-AI-Labs/Mimas@setup-agentic-repository -a cursor

# Codex                    — installs to .agents/skills/ (or ~/.codex/skills/ with -g)
npx skills@latest add Grade-AI-Labs/Mimas@setup-agentic-repository -a codex

# OpenCode                 — installs to .agents/skills/ (or ~/.config/opencode/skills/ with -g)
npx skills@latest add Grade-AI-Labs/Mimas@setup-agentic-repository -a opencode

# GitHub Copilot           — installs to .agents/skills/ (or ~/.copilot/skills/ with -g)
npx skills@latest add Grade-AI-Labs/Mimas@setup-agentic-repository -a github-copilot
```

You can target multiple agents in one call with repeated `-a` flags
(`-a claude-code -a cursor`). For the full list of supported agents, install
scopes, and CLI flags, see the
[vercel-labs/skills documentation](https://github.com/vercel-labs/skills#supported-agents).

## What `/setup-agentic-repository` does

The skill scaffolds a complete, project-specific agent instruction tree — not
a generic template dump. Every file is tailored to the repo's actual tech
stack, git platform, and conventions.

When you run it, the agent will:

1. **Inspect the repository in parallel** — languages, frameworks, build
   tooling, test runners, formatter/linter, pre-commit hooks, commit-message
   conventions, git remote (GitHub / GitLab / Azure DevOps / Bitbucket), and
   existing documentation.
2. **Show you what it found** and ask you to confirm or correct the stack,
   platform, and subdomain detection before any files are written.
3. **Offer to weave in org-specific guidelines** (coding standards, naming
   conventions, etc.) if you have them.
4. **Generate an `AGENTS.md` at the repo root**, plus subdomain `CONTEXT.md`
   files for each meaningful module.
5. **Create a `docs/` hierarchy** with engineering standards, the agent
   workflow, a feature-doc contract, and a seeded `LESSONS.md` for durable
   cross-session rules.
6. **Add a `CLAUDE.md` bridge file** at the repo root pointing Claude at
   `AGENTS.md`. If a `CLAUDE.md` already exists, the pointer is appended
   rather than overwriting your content.
7. **Point you at follow-up skills** (`find-features`, `document-feature`)
   for populating `docs/features/`.

The output is a set of instruction files that future agent sessions read
automatically, so any agent working on the repo picks up the project's
conventions without being briefed each time.

## Adding the other skills

Every skill in this repository can be installed the same way — just swap the
skill name at the end of the `npx` command (and add `-a <agent>` / `-g` as
needed):

```sh
npx skills@latest add Grade-AI-Labs/Mimas@find-features
npx skills@latest add Grade-AI-Labs/Mimas@grill-me
npx skills@latest add Grade-AI-Labs/Mimas@ubiquitous-language
npx skills@latest add Grade-AI-Labs/Mimas@write-a-skill
```

After installing, invoke each one from your agent (e.g. `/grill-me` in
Claude Code). Other agents expose skills differently — check their docs.

## Manual install (no `npx`)

`npx skills@latest add` is just a convenience wrapper — skills are plain
folders with a `SKILL.md`, so you can install them any way you can get files
onto disk. The destination depends on your agent (see the
[full path table](https://github.com/vercel-labs/skills#supported-agents)):

- **Claude Code:** `~/.claude/skills/<name>/` (global) or
  `./.claude/skills/<name>/` (project)
- **Cursor / Codex / OpenCode / GitHub Copilot** (and most other agents):
  `./.agents/skills/<name>/` (project) — the global path varies per agent

The examples below use Claude Code's path (`~/.claude/skills/`); substitute
your agent's path from the table above.

### Option 1 — clone and copy

```sh
git clone --depth=1 https://github.com/Grade-AI-Labs/Mimas.git /tmp/mimas
cp -r /tmp/mimas/skills/setup-agentic-repository ~/.claude/skills/
```

### Option 2 — sparse checkout (grab one skill)

```sh
git clone --depth=1 --filter=blob:none --sparse \
  https://github.com/Grade-AI-Labs/Mimas.git
cd Mimas
git sparse-checkout set skills/setup-agentic-repository
cp -r skills/setup-agentic-repository ~/.claude/skills/
```

### Option 3 — git submodule (track upstream updates)

```sh
git submodule add https://github.com/Grade-AI-Labs/Mimas.git vendor/mimas
ln -s ../../vendor/mimas/skills/setup-agentic-repository \
  ./.claude/skills/setup-agentic-repository
```

Swap `setup-agentic-repository` for any other skill name to install a different
one.

> **Note:** Adding a skill to an existing skills directory is picked up
> mid-session. Creating the directory for the first time usually needs an
> agent restart.

### Available skills

| Skill | What it does |
| --- | --- |
| `setup-agentic-repository` | Scaffolds the Mimas agent instruction tree (`AGENTS.md`, `docs/`) tailored to the current repo. |
| `find-features` | Discovers feature areas missing from `docs/features/` and creates populated feature docs from the template. Natural follow-up to `setup-agentic-repository`. |
| `grill-me` | Interviews you relentlessly about a plan or design until every branch of the decision tree is resolved. |
| `ubiquitous-language` | Extracts a DDD-style glossary from the current conversation and writes it to `UBIQUITOUS_LANGUAGE.md`. |
| `write-a-skill` | Guides you through authoring a new agent skill with proper structure and progressive disclosure. |

## Requirements

- A coding agent that supports the open skills format — Claude Code, Cursor,
  Codex, OpenCode, GitHub Copilot, or any of the
  [50+ others](https://github.com/vercel-labs/skills#supported-agents)
  supported by `vercel-labs/skills`.
- `npx` (ships with Node.js) — only needed for the quick-start install; the
  manual install options above require only `git`.
