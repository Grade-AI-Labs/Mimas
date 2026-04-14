---
name: setup-mimas-template
description: Scaffold the Mimas agent instruction file tree for any repository — AGENTS.md at root, subdomain AGENTS.md files, and the full docs/ hierarchy (AGENT_WORKFLOW.md, ENGINEERING.md, AGENTS_FEATURES.md, FEATURES.md, features/feature-template.md). Every file is tailored to the repo's actual tech stack, project structure, and conventions. Use this skill whenever someone wants to set up agent instructions, onboard a repo for AI-assisted development, add AGENTS.md files, create engineering docs for agents, or mentions "mimas template". Even if they just say "set up this repo for agents" or "add agent docs", this is the skill to use.
---

# setup-mimas-template

You are scaffolding a set of instruction files that AI agents read at the start of every session to understand how to work on a project. The output is a complete, project-specific instruction tree — not a generic template dump.

The process: **research** the repository thoroughly, then **generate** tailored files.

---

## Phase 1 — Research the repository

Explore before writing anything. Use subagents for parallel research if available. You need to understand four things:

### 1. Tech stack

Find the answers to these questions by reading config files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `tsconfig.json`, `Dockerfile`, `.github/workflows/`, `Makefile`, etc.):

- Language(s) and version(s)
- Runtime and framework (Fastify, Express, Next.js, Django, FastAPI, chi, etc.)
- Test framework and how tests are organized
- Database and query layer (if any)
- Authentication mechanism (if any)
- AI/LLM libraries (if any)
- Package manager
- Type checking and linting tools
- CI/CD setup

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

Find the exact, copy-pasteable commands for: **setup/install**, running tests, type checking, dev server, build, lint. Check `package.json` scripts, `Makefile` targets, `pyproject.toml` scripts, or `Dockerfile` entrypoints. These go into `ENGINEERING.md` and the completion checklist.

Include install/setup commands (e.g., `npm install`, `pip install -e ".[dev]"`, `go mod download`) — agents need to know how to bootstrap the project.

### Incorporating existing files

If the repo already has a `CLAUDE.md`, `AGENTS.md`, or `README.md` with meaningful conventions or project description:

- Pull the project description into the root `AGENTS.md` intro
- Incorporate any documented conventions into `ENGINEERING.md`
- If an existing file is empty or placeholder content, replace it

If there is a populated `CLAUDE.md`, keep it — it serves a different purpose (Claude Code-specific config). The AGENTS.md tree you create is for all AI agents regardless of platform.

---

## Phase 2 — Generate the files

Read the reference files before writing:
- `references/file-templates.md` — base template for every file
- `references/tech-adapters.md` — tech-stack-specific sections to compose into the templates

The templates are starting points. Replace every `{{placeholder}}` and generic section with what you actually discovered. Every generated file should read as if a senior engineer on this project wrote it.

### Files to generate

| File | Purpose |
|---|---|
| `/AGENTS.md` | Entry point — links to docs, critical rules, completion checklist |
| `docs/AGENT_WORKFLOW.md` | How agents plan, verify, self-improve |
| `docs/ENGINEERING.md` | Engineering standards — testing, language, naming, DB, auth, commands |
| `docs/AGENTS_FEATURES.md` | Contract for when/how to create and update feature docs |
| `docs/FEATURES.md` | Feature area index (start minimal or empty) |
| `docs/features/feature-template.md` | Template for per-service feature docs (copy verbatim) |
| `<subdomain>/AGENTS.md` | One per discovered subdomain — scope and focus for that area |

### Subdomain AGENTS.md rules

Create one `AGENTS.md` at the **top level** of each subdomain — not deeper:

- `src/` → `src/AGENTS.md` (not `src/routes/AGENTS.md`)
- `internal/` → `internal/AGENTS.md` (not `internal/handlers/AGENTS.md`)
- `packages/auth/` → `packages/auth/AGENTS.md`
- `frontend/` → `frontend/AGENTS.md`

Each subdomain AGENTS.md covers everything within its subtree. Don't create them for utility folders, config dirs, or generated output.

### Feature index

`docs/FEATURES.md` should start minimal. Only add entries if you found feature domains with **meaningful implementation** — not just a route stub or empty handler. A feature area should have at least some business logic, a service layer, or a non-trivial handler before it earns an index entry. If the codebase is mostly scaffolding, leave the feature list empty with the placeholder message.

Even when you do add entries, only add index entries — do not create the `docs/features/<area>.md` files themselves.

Always create `docs/features/feature-template.md` — it is a template for future use, not a feature doc itself.

---

## What makes a good output

**Specific, not generic.** If the repo uses Vitest, write "Vitest" — not "your test framework". If type checking is `npx tsc --noEmit`, write exactly that.

**Use the actual project name.** Refer to the project by the name you found in README, package.json, or go.mod — not a name you inferred or invented. If the README says "Applicant Service", use "Applicant Service", not "Inventory API" or "Go Backend".

**Accurate commands.** Test, typecheck, dev server, build, and setup commands must be correct and copy-pasteable for this specific repo. Verify them against the actual config files.

**Proportionate.** Don't add a "Database guidelines" section to a frontend-only repo. Don't add "TypeScript standards" to a Python project. Only include what applies.

**Opinionated where it matters.** These rules are always included regardless of stack because they make agents better at any engineering work:
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
3. Any tech stack details you were uncertain about — be honest about gaps
4. What they should review and customize before committing
