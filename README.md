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
- `npx` (ships with Node.js)
