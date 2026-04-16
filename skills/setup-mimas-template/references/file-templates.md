# File Templates

Templates for the **project-specific** files the LLM generates. Instructions in `[brackets]` tell you what to write — replace them with real content from Phase 1 and the user interview. Merge in relevant sections from `tech-adapters.md` and `platform-adapters.md` where indicated.

Verbatim files (CLAUDE.md, AGENT_WORKFLOW.md, AGENTS_FEATURES.md, feature-template.md) are handled by `scripts/scaffold.py` — they are NOT in this file.

Every generated file should read as if a senior engineer on this project wrote it — specific, accurate, and proportionate.

---

## /AGENTS.md

```markdown
# AGENTS.md

Read these files at the start of every session before doing any work:

1. `docs/AGENT_WORKFLOW.md` — workflow and operating rules
2. `docs/AGENTS_FEATURES.md` — when and how to update feature docs
3. `docs/FEATURES.md` — feature index
4. `docs/ENGINEERING.md` — engineering standards

[If the repo has subdomains, add a line per subdomain. Example:
"When working in the backend source, also read `src/AGENTS.md`."
"When working on the frontend, also read `frontend/AGENTS.md`."]

---

[Write 2-4 sentences describing what this project is and does.
Use the ACTUAL project name from README, package.json, go.mod, or pyproject.toml — do not invent a name.
Draw from README and config files. Be concrete about the tech stack.
Example: "This is a TypeScript/Node.js backend service — a Fastify API that powers recruitment content generation using LangChain. It uses Kysely for database access and Jest for testing."
If the README already has a good project description, adapt it rather than writing from scratch.]

## CRITICAL — Non-negotiable rules for all agents

### Test-Driven Development (MANDATORY)
**Write tests before implementation code.**

When creating or changing anything:
1. STOP — do not write implementation first
2. Write failing tests (RED)
3. Run tests and confirm failure ([exact test command])
4. Write minimal code to pass tests (GREEN)
5. Refactor while keeping tests green

This applies to all code — routes, services, domain logic, validation, database queries, and any other logic.

[If the project has static type checking, add a second MANDATORY rule.
Use the exact command discovered. Examples:

For TypeScript:
"### TypeScript correctness (MANDATORY)
Before completing any task:
1. Run `npx tsc --noEmit`
2. Fix all TypeScript errors
3. Do not consider work complete until it exits with code 0"

For Python with mypy:
"### Type correctness (MANDATORY)
Before completing any task:
1. Run `mypy .`
2. Fix all type errors
3. Do not consider work complete until it exits with code 0"

For Go:
"### Go vet (MANDATORY)
Before completing any task:
1. Run `go vet ./...`
2. Fix all issues
3. Do not consider work complete until it exits with code 0"

If there is a linter configured (eslint, ruff, golangci-lint, etc.), add it as a third rule with the exact command.

If the project has no type checking or linting, omit these sections entirely.]

## Most important rule

After any change that affects API contracts, schemas, invariants, workflows, or major behavior: update the relevant `docs/features/<slug>.md` as part of the same task — not as a follow-up. New feature area → create `docs/features/<slug>.md` and add an entry to `docs/FEATURES.md` (alphabetical).

## Structure of further instructions

- **Agent workflow & operating rules:** `docs/AGENT_WORKFLOW.md`
- **Engineering standards:** `docs/ENGINEERING.md`
- **Feature documentation contract:** `docs/AGENTS_FEATURES.md`
- **Feature index:** `docs/FEATURES.md`
- **Feature docs:** `docs/features/`
[Add one line per subdomain. Example:
"- **Backend source instructions:** `src/AGENTS.md`"
"- **Frontend instructions:** `frontend/AGENTS.md`"]

Keep this file minimal. Do not duplicate detailed rules here.

## Completion checklist

Before marking work complete:

- [ ] Tests written before implementation
- [ ] All tests passing
[If type checking exists: "- [ ] `[typecheck command]` passes"]
[If linter exists: "- [ ] `[lint command]` passes"]
- [ ] Naming conventions followed
- [ ] Errors handled
- [ ] Feature docs updated if contract/schema/invariant changed (see docs/AGENTS_FEATURES.md)
[If git platform detected: insert completion checklist additions from platform-adapters.md.
Example for GitHub:
"- [ ] PR opened with summary and linked issues"
"- [ ] CI checks passing"
If no platform: omit these items.]
```

---

## docs/ENGINEERING.md

This is the most project-specific file. Build it by combining relevant adapter sections from `tech-adapters.md` with the actual commands and conventions you discovered.

```markdown
# Engineering Standards & Workflows

This document defines shared engineering practices for [project name].

---

## Root README.md policy

README.md exists to answer:
- what this repo is
- how to run it locally
- where to find canonical documentation

Agents should update README.md when dev commands change, ports or startup steps change, or links to docs move.

Agents should not describe feature behavior, list API endpoints, or include request/response schemas. Canonical documentation lives under `docs/`.

---

## Testing standards

[Insert the testing adapter section from tech-adapters.md that matches this project's test framework.
Fill in the actual test file pattern and location you discovered.
Include the exact command to run a single file/test.
Include integration test approach if applicable (Testcontainers, docker-compose, etc.).]

---

[Insert the language standards section from tech-adapters.md — TypeScript, Python, Go, etc.
Only include if applicable.]

---

## Naming conventions

[Insert naming conventions from tech-adapters.md for this language.
If the project already uses a different convention, use that instead.]

---

## Error handling

- Use typed/structured errors
- Never swallow errors silently
- Log errors intentionally
- Centralize error handling where applicable

---

[If the project uses a database: insert the relevant database adapter from tech-adapters.md.
Fill in the actual migration directory and query layer.
If no database: omit this section entirely.]

---

[If the project has authentication: insert the relevant auth adapter from tech-adapters.md.
Fill in the actual module path where auth logic lives.
If no auth: omit this section.]

---

[If the project uses AI/LLM libraries: add a section describing where AI code lives and
what counts as a behavioral change requiring doc updates.
See AI adapters in tech-adapters.md.
If no AI: omit this section.]

---

[If a git platform and/or CI system was detected, insert the CI/CD section
from platform-adapters.md here. If no CI detected: omit.]

---

[If an issue tracker was detected or confirmed, insert the issue/work-item linking
section from platform-adapters.md here. If no tracker: omit.]

---

## Commands reference

[List the exact commands for this project. Only include commands that actually exist.
Start with setup, then the most frequently used commands.]

```bash
[install command]                 # install dependencies / setup
[test command]                    # run all tests
[single test command]             # run a single test file
[typecheck command]               # type check (if applicable)
[dev command]                     # start dev server
[build command]                   # build for production
[lint command]                    # lint (if applicable)
[migration command]               # run database migrations (if applicable)
```

---

## Completion checklist

Before marking work complete:

* [ ] Tests written before implementation
* [ ] All tests passing
[If type checking: "* [ ] `[typecheck command]` passes"]
[If linting: "* [ ] `[lint command]` passes"]
* [ ] Naming conventions followed
* [ ] Errors handled
* [ ] Security considered
* [ ] Feature docs updated if contract/schema/invariant changed (see docs/AGENTS_FEATURES.md)
```

---

## docs/FEATURES.md

Start minimal. Only add entries if you clearly identified feature domains from the codebase.

```markdown
# Feature Areas

This index represents the known feature areas in the system.

It must stay accurate as new features are introduced, renamed, merged, or removed.

---

## Feature list (alphabetical)

[Only list feature areas that have MEANINGFUL implementation — not just a route stub,
empty handler, or scaffolded directory. A feature area should have at least some
business logic, a service layer, or a non-trivial handler to earn an entry here.
If the codebase is mostly scaffolding or stubs, leave the list empty.

When listing:
"- [area-name](./features/area-name.md) — one-line description"

If the project is new or feature boundaries are unclear:]

_No feature areas documented yet. Add entries as you build out the system._

---

## Rules for agents

- Introducing a new feature area requires:
  - creating `docs/features/<feature>.md`
  - adding it to this list (alphabetical)
- Per-service docs live under `docs/features/<area>/` and are linked from the area doc
- Renaming or merging features requires updating links and notes
- This file should remain concise and navigable
```

---

## `<subdomain>/AGENTS.md`

Create one per discovered subdomain. The purpose is to tell an agent entering this directory what it owns and what rules apply here.

```markdown
# [Subdomain Name] Instructions

This directory contains the [describe what this subdomain is — e.g. "Fastify REST API",
"React frontend application", "shared Go packages", "Python data pipeline"].

You MUST follow:
- Root TDD [and type checking if applicable] rules (see `/AGENTS.md`)
- `docs/ENGINEERING.md` standards

Focus here on:
[List 4-6 things an agent working in this subdomain should pay attention to.
Be specific to what you actually found in this directory. Examples:
- "API route definitions and request validation"
- "Database query correctness and migration safety"
- "React component contracts and prop types"
- "Authentication middleware and token handling"
- "AI prompt management and chain configuration"
- "CLI argument parsing and error reporting"]

If a change introduces or modifies a feature area, follow `docs/AGENTS_FEATURES.md`.
```
