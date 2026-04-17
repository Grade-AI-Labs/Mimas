# Mimas

A collection of Claude Code agent skills for bootstrapping repositories with
agent instructions and day-to-day engineering workflows.

## Quick start

Install the `setup-mimas-template` skill into your Claude Code environment:

```sh
npx skills@latest add Grade-AI-Labs/Mimas/setup-mimas-template
```

Then, from inside the repository you want to onboard, launch Claude Code and
run:

```
/setup-mimas-template
```

## What `/setup-mimas-template` does

The skill scaffolds a complete, project-specific agent instruction tree — not
a generic template dump. Every file is tailored to the repo's actual tech
stack, git platform, and conventions.

When you run it, Claude will:

1. **Ask you whether to run a Minimal or Deep-dive setup.** Minimal gets you
   a working instruction tree fast; Deep-dive interviews you about the
   project so the generated files capture real context.
2. **Inspect the repository** — languages, frameworks, build tooling, test
   runners, git remote (GitHub / GitLab / Azure DevOps), and existing
   conventions.
3. **Generate an `AGENTS.md` at the repo root**, plus subdomain `AGENTS.md`
   files for each meaningful module it finds.
4. **Create a `docs/` hierarchy** with engineering standards, architecture
   notes, and onboarding material agents can read at the start of every
   session.
5. **Add a `CLAUDE.md` bridge file** at the repo root pointing Claude at
   `AGENTS.md`. If a `CLAUDE.md` already exists, the pointer is appended
   rather than overwriting your content.
6. **Install a curated set of starter skills** into `.claude/skills/` so the
   project is immediately productive with Claude Code.

The output is a set of instruction files that future agent sessions read
automatically, so any agent working on the repo picks up the project's
conventions without being briefed each time.

## Adding the other skills

Every skill in this repository can be installed the same way — just swap the
skill name at the end of the `npx` command:

```sh
npx skills@latest add Grade-AI-Labs/Mimas/grill-me
npx skills@latest add Grade-AI-Labs/Mimas/ubiquitous-language
npx skills@latest add Grade-AI-Labs/Mimas/write-a-prd-irecommend
npx skills@latest add Grade-AI-Labs/Mimas/write-a-skill
```

After installing, invoke each one from Claude Code with its slash command
(e.g. `/grill-me`, `/write-a-skill`).

## Manual install (no `npx`)

`npx skills@latest add` is just a convenience wrapper — skills are plain
folders with a `SKILL.md`, so you can install them any way you can get files
onto disk. Pick the scope you want:

- `~/.claude/skills/<name>/` — global, available in every project
- `./.claude/skills/<name>/` — project-local, only this repo

### Option 1 — clone and copy

```sh
git clone --depth=1 https://github.com/Grade-AI-Labs/Mimas.git /tmp/mimas
cp -r /tmp/mimas/skills/setup-mimas-template ~/.claude/skills/
```

### Option 2 — sparse checkout (grab one skill)

```sh
git clone --depth=1 --filter=blob:none --sparse \
  https://github.com/Grade-AI-Labs/Mimas.git
cd Mimas
git sparse-checkout set skills/setup-mimas-template
cp -r skills/setup-mimas-template ~/.claude/skills/
```

### Option 3 — git submodule (track upstream updates)

```sh
git submodule add https://github.com/Grade-AI-Labs/Mimas.git vendor/mimas
ln -s ../../vendor/mimas/skills/setup-mimas-template \
  ./.claude/skills/setup-mimas-template
```

Swap `setup-mimas-template` for any other skill name to install a different
one.

> **Note:** Adding a skill to an existing `.claude/skills/` directory is
> picked up mid-session. Creating the `.claude/skills/` directory for the
> first time usually needs a Claude Code restart.

### Available skills

| Skill | What it does |
| --- | --- |
| `setup-mimas-template` | Scaffolds the Mimas agent instruction tree (`AGENTS.md`, `docs/`, starter skills) tailored to the current repo. |
| `grill-me` | Interviews you relentlessly about a plan or design until every branch of the decision tree is resolved. |
| `ubiquitous-language` | Extracts a DDD-style glossary from the current conversation and writes it to `UBIQUITOUS_LANGUAGE.md`. |
| `write-a-prd-irecommend` | Builds a PRD through interview + codebase exploration and submits it as an Azure DevOps User Story. |
| `write-a-skill` | Guides you through authoring a new Claude Code skill with proper structure and progressive disclosure. |

## Requirements

- [Claude Code](https://claude.com/claude-code)
- `npx` (ships with Node.js) — only needed for the quick-start install; the
  manual install options above require only `git`.
