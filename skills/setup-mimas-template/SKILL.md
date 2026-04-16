---
name: setup-mimas-template
description: Scaffold the Mimas agent instruction file tree for any repository — AGENTS.md at root, subdomain AGENTS.md files, the full docs/ hierarchy, and starter skills. Every file is tailored to the repo's actual tech stack, git platform, and conventions. Use this skill whenever someone wants to set up agent instructions, onboard a repo for AI-assisted development, add AGENTS.md files, create engineering docs for agents, or mentions "mimas template". Even if they just say "set up this repo for agents" or "add agent docs", this is the skill to use.
metadata:
  author: Olof Brogeby
---

# setup-mimas-template

You are scaffolding a set of instruction files that AI agents read at the start of every session to understand how to work on a project. The output is a complete, project-specific instruction tree plus a curated set of starter skills — not a generic template dump.

---

## Step 0 — Ask the user: Minimal or Deep-dive?

Before doing anything else, ask:

> **How would you like to set this up?**
>
> 1. **Minimal** — I auto-detect your stack, platform, and conventions, pick smart defaults, and generate everything. Takes about a minute. You can tweak the files afterward.
>
> 2. **Deep-dive** — I auto-detect first, then walk you through the findings and let you confirm, customize, choose which skills to include, and add org-specific guidelines. More tailored, more questions.

Wait for the user's answer before proceeding. If they say something ambiguous, default to **Minimal**.

---

## Phase 1 — Automated Discovery

This phase is the same for both paths. Explore before writing anything. **Launch three subagents in parallel** to maximize speed — each handles an independent research task. Collect their results before proceeding.

### Subagent dispatch

Launch these three subagents simultaneously (one tool call with multiple Agent invocations):

**Subagent A — Tech stack & commands.** Read config files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `tsconfig.json`, `Dockerfile`, `Makefile`, etc.) and report:

- Language(s) and version(s)
- Runtime and framework (Fastify, Express, Next.js, Django, FastAPI, chi, etc.)
- Test framework and how tests are organized
- Database and query layer (if any)
- Authentication mechanism (if any)
- AI/LLM libraries (if any)
- Package manager
- Type checking and linting tools
- Exact, copy-pasteable commands for: setup/install, running tests, type checking, dev server, build, lint (check `package.json` scripts, `Makefile` targets, `pyproject.toml` scripts, `Dockerfile` entrypoints)

**Subagent B — Project structure & conventions.** List top-level directories and report:

- Subdomains identified (top-level dirs that represent distinct parts of the app):
  - Single-package repos: typically `src/`, `app/`, `internal/`, `cmd/`
  - Monorepos: each `packages/<name>/` or `apps/<name>/`
  - Multi-part repos: `backend/`, `frontend/`, `server/`, `client/`, `api/`, `web/`
  - Ignore: `node_modules/`, `dist/`, `build/`, `.git/`, test fixtures, config dirs
- Role of each subdomain (backend API, frontend app, shared library, CLI tool, etc.)
- File naming pattern (kebab-case, camelCase, snake_case)
- Test file placement (colocated? separate `__tests__/` or `tests/` dir?)
- Module organization style (by feature? by layer? by domain?)
- Existing documentation (README.md content, any docs/ folder)

**Subagent C — Git platform, CI/CD & existing files.** Read `.git/config`, check for CI config files, and scan existing docs:

- Git platform from remote URL: `github.com` → GitHub, `dev.azure.com` / `visualstudio.com` → Azure DevOps, `gitlab.com` → GitLab, `bitbucket.org` → Bitbucket
- CI/CD: `.github/workflows/` → GitHub Actions, `azure-pipelines.yml` → Azure Pipelines, `.gitlab-ci.yml` → GitLab CI
- Issue tracker hints from recent commit messages (`#123` → GitHub Issues, `AB#456` → Azure DevOps, `PROJ-789` → Jira/Linear)
- Whether `CLAUDE.md`, `AGENTS.md`, or `README.md` exist and have meaningful content (report a brief summary of what they contain)

### After subagents return

Combine the three reports into a unified picture. If any subagent couldn't determine something (e.g., no database found, no CI detected), that's fine — note it as "not detected" and move on.

For existing files:
- Pull project description from README into root `AGENTS.md` intro
- Incorporate documented conventions into `ENGINEERING.md`
- If an existing `AGENTS.md` or `CLAUDE.md` is empty or placeholder, replace it
- If there is a populated `CLAUDE.md`, keep it — it serves a different purpose

---

## Phase 2 — Diverge based on user's choice

### Path A: Minimal

Use smart defaults for everything not auto-detected:

- **Platform/PR workflow**: use what was detected; if nothing detected, omit platform-specific sections
- **Issue tracker**: use what was detected from commit patterns; if nothing detected, default to local task tracking
- **Starter skills**: include ALL universal skills (`tdd`, `grill-me`, `write-a-skill`, `document-feature`, `ubiquitous-language`) plus the `write-a-prd` variant matching the detected platform (GitHub → github variant, Azure DevOps → azure-devops variant, otherwise → generic variant). All skills go into `.claude/skills/`.
- **Org guidelines**: skip (none included)

Proceed directly to Phase 3.

### Path B: Deep-dive

Present your findings and walk through each decision.

#### 2a. Present findings

Show the user what you discovered:

```
Here's what I found:

  Stack:        [language] / [framework] / [db] / [test framework]
  Platform:     [GitHub | Azure DevOps | GitLab | Bitbucket | unknown]
  CI:           [GitHub Actions | Azure Pipelines | GitLab CI | none detected]
  Tracker:      [GitHub Issues | Azure DevOps | Jira | Linear | none detected]
  Subdomains:   [list of discovered subdomains]

Anything I got wrong?
```

Wait for corrections before continuing.

#### 2b. Work tracking

If not confidently detected, ask:

> **Where do you track issues / work items?**
> 1. GitHub Issues
> 2. Azure DevOps Work Items
> 3. Jira
> 4. Linear
> 5. Other / None

#### 2c. Starter skills

Present the available skills and let the user choose:

> **Which starter skills should I scaffold into `.claude/skills/`?**
>
> Universal (work with any project):
> - [x] `tdd` — test-driven development with red-green-refactor loop and deep module design
> - [x] `grill-me` — stress-test plans and designs through relentless questioning
> - [x] `write-a-skill` — create new agent skills with proper structure
> - [x] `document-feature` — guided walkthrough to populate feature docs
> - [x] `ubiquitous-language` — extract DDD-style glossary from conversations
>
> Platform-specific:
> - [x] `write-a-prd` — write PRDs via interview, submit to [detected platform]
>
> All are pre-selected. Deselect any you don't want, or just confirm.

#### 2d. Org guidelines (optional)

> **Do you have coding guidelines or standards to include?**
> Paste a file path, a URL, or the content directly. These will be woven into `ENGINEERING.md`.
> Press enter to skip.

If the user provides content, incorporate it into the relevant sections of `ENGINEERING.md` (coding standards, naming conventions, review practices, etc.). Don't dump it verbatim — integrate it naturally alongside the tech-stack-specific standards.

---

## Phase 3 — Scaffold verbatim files (script)

Run the scaffolding script to create all deterministic files — directories, universal templates, composed AGENT_WORKFLOW.md, CLAUDE.md bridge file, and starter skills. This saves tokens by avoiding LLM generation of verbatim content.

```bash
bash scripts/scaffold.sh --target <repo-root> --platform <platform> [--skills <comma-separated>] [--no-skills]
```

The `--platform` flag determines:
- Which PR/MR workflow section is injected into `docs/AGENT_WORKFLOW.md`
- Which `write-a-prd` variant is copied (github, azure-devops, or generic)

If the user chose deep-dive and deselected some skills, pass only the selected ones via `--skills`.

The script creates:

| File | How |
|---|---|
| `CLAUDE.md` | Created (or appended if exists) — points Claude to AGENTS.md |
| `docs/AGENT_WORKFLOW.md` | Composed from base template + platform PR/MR section |
| `docs/AGENTS_FEATURES.md` | Copied verbatim — universal feature doc contract |
| `docs/features/feature-template.md` | Copied verbatim — template for future feature docs |
| `.claude/skills/*/SKILL.md` | Copied from starter-skills (universal + platform variant) |

The script is idempotent — re-running skips existing files.

### Available scripts

- **`scripts/scaffold.sh`** — Scaffolds verbatim files, composes AGENT_WORKFLOW.md, copies starter skills

---

## Phase 4 — Generate project-specific files (LLM)

These files require LLM reasoning and cannot be scripted. Read the reference files before writing:
- `references/file-templates.md` — base template for each file
- `references/tech-adapters.md` — tech-stack-specific sections
- `references/platform-adapters.md` — CI/CD and issue linking sections for ENGINEERING.md

Replace every `{{placeholder}}` with what you actually discovered. Every generated file should read as if a senior engineer on this project wrote it.

### Files to generate

| File | Purpose |
|---|---|
| `/AGENTS.md` | Entry point — links to docs, critical rules, completion checklist |
| `docs/ENGINEERING.md` | Engineering standards — testing, language, naming, DB, auth, CI/CD, commands |
| `docs/FEATURES.md` | Feature area index (start minimal or empty) |
| `<subdomain>/AGENTS.md` | One per discovered subdomain — scope and focus for that area |

### Subdomain AGENTS.md rules

Create one `AGENTS.md` at the **top level** of each subdomain — not deeper:

- `src/` → `src/AGENTS.md` (not `src/routes/AGENTS.md`)
- `internal/` → `internal/AGENTS.md` (not `internal/handlers/AGENTS.md`)
- `packages/auth/` → `packages/auth/AGENTS.md`
- `frontend/` → `frontend/AGENTS.md`

Each subdomain AGENTS.md covers everything within its subtree. Don't create them for utility folders, config dirs, or generated output.

### Feature index

`docs/FEATURES.md` should start minimal. Only add entries if you found feature domains with **meaningful implementation** — not just a route stub or empty handler. Even when you add entries, only add index entries — do not create the `docs/features/<area>.md` files themselves.

### Platform-specific content in AGENTS.md and ENGINEERING.md

Weave platform content from `references/platform-adapters.md` into the files you generate:

- **`AGENTS.md` completion checklist**: add platform-specific items (PR opened, CI passing, issues linked)
- **`docs/ENGINEERING.md`**: add CI/CD section and issue linking conventions

If no platform was detected and the user didn't specify one, omit platform-specific sections entirely — don't guess.

Note: `docs/AGENT_WORKFLOW.md` is already handled by the script with the correct platform section.

---

## What makes a good output

**Specific, not generic.** If the repo uses Vitest, write "Vitest" — not "your test framework". If type checking is `npx tsc --noEmit`, write exactly that.

**Use the actual project name.** Refer to the project by the name you found in README, package.json, or go.mod — not a name you inferred or invented.

**Accurate commands.** Test, typecheck, dev server, build, and setup commands must be correct and copy-pasteable.

**Proportionate.** Don't add a "Database guidelines" section to a frontend-only repo. Don't add "TypeScript standards" to a Python project. Only include what applies.

**Opinionated where it matters.** These rules are always included regardless of stack:
- TDD (red-green-refactor) is mandatory
- Plan mode for non-trivial tasks
- Verification before marking work done
- Self-improvement loop (lessons learned)
- Feature documentation contract

**Keep root AGENTS.md lean.** It is an index plus the most critical non-negotiable rules. Detail lives in the docs it points to.

---

## After generating

Tell the user:
1. Which files were created (full list with paths)
2. Which subdomains were detected and got their own AGENTS.md
3. Which starter skills were scaffolded
4. Which platform/tracker was used for platform-specific content
5. Any tech stack details you were uncertain about — be honest about gaps
6. What they should review and customize before committing

Then suggest next steps:

> **Recommended next steps** (each in a fresh session to keep context clean):
>
> 1. **Define your domain language** — run `/ubiquitous-language` to extract a glossary of canonical terms from your codebase and team conversations. This gives agents a shared vocabulary.
>
> 2. **Document your key features** — run `/document-feature` for each major feature area. This populates `docs/features/` so agents understand your system's contracts and behavior.
>
> 3. **Review and commit** — look through the generated files, tweak anything that doesn't feel right, then commit.
