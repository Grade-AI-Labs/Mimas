---
name: setup-mimas-template
description: Scaffold the Mimas agent instruction file tree for any repository — AGENTS.md at root, subdomain AGENTS.md files, the full docs/ hierarchy, and starter skills. Every file is tailored to the repo's actual tech stack, git platform, and conventions. Use this skill whenever someone wants to set up agent instructions, onboard a repo for AI-assisted development, add AGENTS.md files, create engineering docs for agents, or mentions "mimas template". Even if they just say "set up this repo for agents" or "add agent docs", this is the skill to use.
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

This phase is the same for both paths. Explore before writing anything. Use subagents for parallel research if available.

### 1. Tech stack

Read config files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `tsconfig.json`, `Dockerfile`, `.github/workflows/`, `Makefile`, etc.) to find:

- Language(s) and version(s)
- Runtime and framework (Fastify, Express, Next.js, Django, FastAPI, chi, etc.)
- Test framework and how tests are organized
- Database and query layer (if any)
- Authentication mechanism (if any)
- AI/LLM libraries (if any)
- Package manager
- Type checking and linting tools

### 2. Project structure

Identify **subdomains** — top-level directories that represent distinct parts of the application:

- Single-package repos: typically `src/`, `app/`, `internal/`, `cmd/`
- Monorepos: each `packages/<name>/` or `apps/<name>/`
- Multi-part repos: `backend/`, `frontend/`, `server/`, `client/`, `api/`, `web/`
- Ignore: `node_modules/`, `dist/`, `build/`, `.git/`, test fixtures, config dirs

For each subdomain, understand its role: backend API, frontend app, shared library, CLI tool, etc.

### 3. Conventions already in use

- File naming pattern (kebab-case, camelCase, snake_case)
- Test file placement (colocated? separate `__tests__/` or `tests/` dir?)
- Existing documentation (README.md content, any docs/ folder, wiki)
- Module organization style (by feature? by layer? by domain?)

### 4. Key commands

Find the exact, copy-pasteable commands for: **setup/install**, running tests, type checking, dev server, build, lint. Check `package.json` scripts, `Makefile` targets, `pyproject.toml` scripts, or `Dockerfile` entrypoints.

Include install/setup commands (e.g., `npm install`, `pip install -e ".[dev]"`, `go mod download`) — agents need to know how to bootstrap the project.

### 5. Git platform & CI/CD (NEW)

Detect from `.git/config` remote URL and config files:

- **Git platform**: `github.com` → GitHub, `dev.azure.com` / `visualstudio.com` → Azure DevOps, `gitlab.com` → GitLab, `bitbucket.org` → Bitbucket
- **CI/CD**: `.github/workflows/` → GitHub Actions, `azure-pipelines.yml` → Azure Pipelines, `.gitlab-ci.yml` → GitLab CI
- **Issue tracker hints**: commit message patterns (`#123` → GitHub Issues, `AB#456` → Azure DevOps, `PROJ-789` → Jira/Linear)

### 6. Incorporating existing files

If the repo already has a `CLAUDE.md`, `AGENTS.md`, or `README.md` with meaningful conventions:

- Pull the project description into the root `AGENTS.md` intro
- Incorporate any documented conventions into `ENGINEERING.md`
- If an existing file is empty or placeholder content, replace it

If there is a populated `CLAUDE.md`, keep it — it serves a different purpose.

---

## Phase 2 — Diverge based on user's choice

### Path A: Minimal

Use smart defaults for everything not auto-detected:

- **Platform/PR workflow**: use what was detected; if nothing detected, omit platform-specific sections
- **Issue tracker**: use what was detected from commit patterns; if nothing detected, default to local task tracking
- **Starter skills**: include ALL universal skills (`grill-me`, `write-a-skill`, `document-feature`, `ubiquitous-language`) plus the `write-a-prd` variant matching the detected platform (GitHub → github variant, Azure DevOps → azure-devops variant, otherwise → generic variant). All skills go into `.claude/skills/`.
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

## Phase 3 — Generate the files

Read the reference files before writing:
- `references/file-templates.md` — base template for every file
- `references/tech-adapters.md` — tech-stack-specific sections to compose into the templates
- `references/platform-adapters.md` — git platform, issue tracker, and CI/CD sections

The templates are starting points. Replace every `{{placeholder}}` and generic section with what you actually discovered. Every generated file should read as if a senior engineer on this project wrote it.

### Files to generate

| File | Purpose |
|---|---|
| `CLAUDE.md` | Points Claude Code to read AGENTS.md — bridge file (see below) |
| `/AGENTS.md` | Entry point — links to docs, critical rules, completion checklist |
| `docs/AGENT_WORKFLOW.md` | How agents plan, verify, self-improve, and handle PRs |
| `docs/ENGINEERING.md` | Engineering standards — testing, language, naming, DB, auth, CI/CD, commands |
| `docs/AGENTS_FEATURES.md` | Contract for when/how to create and update feature docs |
| `docs/FEATURES.md` | Feature area index (start minimal or empty) |
| `docs/features/feature-template.md` | Template for per-service feature docs (copy verbatim from template) |
| `<subdomain>/AGENTS.md` | One per discovered subdomain — scope and focus for that area |

### CLAUDE.md bridge file

Claude Code does not natively look for `AGENTS.md`. Create a `CLAUDE.md` at the repo root that points to it. If a `CLAUDE.md` already exists, **append** the instruction — don't overwrite existing content.

Content to write (or append):

```markdown
Read AGENTS.md at the root of this repository at the start of every session before doing any work. It links to all other agent instruction files.
```

This keeps `CLAUDE.md` minimal — it's a pointer, not a duplicate. All actual instructions live in the AGENTS.md tree.

### Subdomain AGENTS.md rules

Create one `AGENTS.md` at the **top level** of each subdomain — not deeper:

- `src/` → `src/AGENTS.md` (not `src/routes/AGENTS.md`)
- `internal/` → `internal/AGENTS.md` (not `internal/handlers/AGENTS.md`)
- `packages/auth/` → `packages/auth/AGENTS.md`
- `frontend/` → `frontend/AGENTS.md`

Each subdomain AGENTS.md covers everything within its subtree. Don't create them for utility folders, config dirs, or generated output.

### Feature index

`docs/FEATURES.md` should start minimal. Only add entries if you found feature domains with **meaningful implementation** — not just a route stub or empty handler. Even when you add entries, only add index entries — do not create the `docs/features/<area>.md` files themselves.

Always create `docs/features/feature-template.md` — it is a template for future use, not a feature doc itself.

### Platform-specific content

Weave platform content from `references/platform-adapters.md` into the generated files:

- **`AGENTS.md` completion checklist**: add platform-specific items (PR opened, CI passing, issues linked)
- **`docs/AGENT_WORKFLOW.md`**: add a "Pull Requests" or "Merge Requests" section with the platform's conventions
- **`docs/ENGINEERING.md`**: add CI/CD section and issue linking conventions

If no platform was detected and the user didn't specify one, omit platform-specific sections entirely — don't guess.

---

## Phase 4 — Scaffold starter skills

Copy the selected starter skills into the target repo's `.claude/skills/` directory.

### Universal skills

Located in `starter-skills/universal/`. Copy each selected skill's directory as-is:

| Skill | What it does |
|---|---|
| `grill-me` | Interviews the user relentlessly about a plan or design until reaching shared understanding |
| `write-a-skill` | Guides creation of new agent skills with proper structure and progressive disclosure |
| `document-feature` | Walks through populating a `docs/features/<slug>.md` from the feature template |
| `ubiquitous-language` | Extracts DDD-style ubiquitous language glossary from conversations |

### Platform-variant skills

Located in `starter-skills/platform-variants/`. Pick the variant matching the confirmed platform:

| Skill | Variants | Selection logic |
|---|---|---|
| `write-a-prd` | `github/`, `azure-devops/`, `generic/` | GitHub → github, Azure DevOps → azure-devops, anything else → generic |

Copy the selected variant's directory into `.claude/skills/write-a-prd/` in the target repo (not the variant subdirectory — flatten it).

### Skills directory structure in target repo

After scaffolding, the target repo should have:

```
.claude/skills/
├── grill-me/SKILL.md
├── write-a-skill/SKILL.md
├── document-feature/SKILL.md
├── ubiquitous-language/SKILL.md
└── write-a-prd/SKILL.md
```

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
