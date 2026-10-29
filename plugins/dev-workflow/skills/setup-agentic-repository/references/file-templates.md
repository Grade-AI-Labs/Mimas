# File Templates

Templates for the **project-specific** files the LLM generates. Instructions in `[brackets]` tell you what to write — replace them with real content from Phase 1 and the user interview. Merge in relevant sections from `tech-adapters.md` and `platform-adapters.md` where indicated.

Verbatim files (under `{{DOCS_DIR}}/`: `AGENT_WORKFLOW.md`, `AGENTS_FEATURES.md`, `features/feature-template.md`, `LESSONS.md`, `domain.md`, `triage-labels.md`, `issue-tracker.md`) are handled by `scripts/scaffold.sh` — they are NOT in this file.

Every generated file should read as if a senior engineer on this project wrote it — specific, accurate, and proportionate. When you leave out an optional section, drop the `---` separator that went with it.

---

## /AGENTS.md

```markdown
# AGENTS.md

Read these files at the start of every session before doing any work:

1. `{{DOCS_DIR}}/AGENT_WORKFLOW.md` — workflow and operating rules
2. `{{DOCS_DIR}}/LESSONS.md` — durable rules learned from past corrections; apply any that match this session's work
3. `{{DOCS_DIR}}/AGENTS_FEATURES.md` — when and how to update feature docs
4. `{{DOCS_DIR}}/FEATURES.md` — feature index
5. `{{DOCS_DIR}}/ENGINEERING.md` — commands, setup, CI and conventions
[If a glossary was written: "6. `GLOSSARY.md` — the domain language; use its terms verbatim" (or "`GLOSSARY-MAP.md` — index of the per-context glossaries" when multi-context)]

`CODING_STANDARDS.md` holds the coding standards. It is read during review, by `/code-review` and `/agentic-review`.

## Agent skills

### Issue tracker

[One-line summary of where issues are tracked, e.g. "Issues live in GitHub Issues for this repo, via the `gh` CLI."]. See `{{DOCS_DIR}}/issue-tracker.md`.

### Triage labels

[One-line summary of the label vocabulary, e.g. "Default label strings for the five triage roles."]. See `{{DOCS_DIR}}/triage-labels.md`.

### Domain docs

[One line: "Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root." or "Multi-context: `GLOSSARY-MAP.md` at the repo root points to one `GLOSSARY.md` per context."]. See `{{DOCS_DIR}}/domain.md`.

## Modules

[One line per subdomain detected in Phase 1, as "`<path>/` — <one-line role>". Review skills route changed files to one reviewer per module from this list, so cover every top-level directory that holds product code. Example:
"- `src/api/` — Fastify HTTP API: routes, validation, auth"
"- `src/worker/` — background jobs consuming the queue"
"- `web/` — Next.js frontend"
Single-package repos with no meaningful split get one line for the source root.]

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

This applies to all code — routes, services, domain logic, validation, database queries, and any other logic. The `/tdd` skill drives this loop.

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

If there is a linter configured (eslint, ruff, golangci-lint, etc.), add it as another MANDATORY rule with the exact command.

If the project has no type checking or linting, omit these sections entirely.]

[If an existing CLAUDE.md was merged in Phase 2, add its project rules here as "### Project rules", one bullet each (e.g. "Money is always integer cents").]

## Most important rule

After any change that affects API contracts, schemas, invariants, workflows, or major behavior: update the relevant `{{DOCS_DIR}}/features/<slug>.md` as part of the same task — not as a follow-up. New feature area → create `{{DOCS_DIR}}/features/<slug>.md` and add an entry to `{{DOCS_DIR}}/FEATURES.md` (alphabetical).

## Structure of further instructions

- **Agent workflow & operating rules:** `{{DOCS_DIR}}/AGENT_WORKFLOW.md`
- **Agent lessons (durable cross-session rules):** `{{DOCS_DIR}}/LESSONS.md`
- **Commands, setup, CI and conventions:** `{{DOCS_DIR}}/ENGINEERING.md`
- **Coding standards (read during review):** `CODING_STANDARDS.md`
- **Feature documentation contract:** `{{DOCS_DIR}}/AGENTS_FEATURES.md`
- **Feature index:** `{{DOCS_DIR}}/FEATURES.md`
- **Feature docs:** `{{DOCS_DIR}}/features/`
- **Domain language:** `GLOSSARY.md` (or `GLOSSARY-MAP.md`), created lazily — see `{{DOCS_DIR}}/domain.md`
- **Architecture decisions:** `docs/adr/`, created lazily
[If review policies exist: "- **Review policies:** `{{DOCS_DIR}}/review/policies/`"]

Keep this file minimal. Do not duplicate detailed rules here.

## Completion checklist

Before marking work complete:

- [ ] Tests written before implementation
- [ ] All tests passing
[If type checking exists: "- [ ] `[typecheck command]` passes"]
[If linter exists: "- [ ] `[lint command]` passes"]
- [ ] Naming conventions followed
- [ ] Errors handled
- [ ] Security considered
- [ ] Feature docs updated if contract/schema/invariant changed (see {{DOCS_DIR}}/AGENTS_FEATURES.md)
- [ ] `GLOSSARY.md` updated if a domain term was resolved or introduced (see {{DOCS_DIR}}/AGENT_WORKFLOW.md § Glossary upkeep)
- [ ] ADR written in `docs/adr/` if a hard-to-reverse decision was made (see {{DOCS_DIR}}/AGENT_WORKFLOW.md § ADR upkeep)
- [ ] Lesson recorded in `{{DOCS_DIR}}/LESSONS.md` if this session produced a correction, revert, or hidden constraint (see triggers in `{{DOCS_DIR}}/AGENT_WORKFLOW.md`)
[If git platform detected: insert completion checklist additions from platform-adapters.md.
Example for GitHub:
"- [ ] PR opened with summary and linked issues"
"- [ ] CI checks passing"
If no platform: omit these items.]
```

---

## CODING_STANDARDS.md

The repo-root file the review skills check code against (`/code-review`'s Standards axis, `/agentic-review`'s specialists). `/retro` adds judgement-call rules to it over time; mechanical rules belong in a linter or CI check instead. Build it by combining the matching adapter sections from `tech-adapters.md` with the conventions you actually observed. Implementation commands do **not** go here — they live in `{{DOCS_DIR}}/ENGINEERING.md`.

```markdown
# Coding Standards

The standards [project name] code is reviewed against. Rules that a linter, typechecker or CI job already enforces don't belong here.

---

## Testing standards

[Insert the testing adapter section from tech-adapters.md that matches this project's test framework.
Fill in the actual test file pattern and location you discovered.
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

[Insert the framework "focus areas" from tech-adapters.md for each framework in use, as review checks.]

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

[If the user supplied org coding guidelines in Phase 2b, weave them into the sections above.]
```

---

## {{DOCS_DIR}}/ENGINEERING.md

How to work in this repo: commands, setup, CI and conventions. Build it from the commands and conventions you discovered. Coding standards go in `CODING_STANDARDS.md`, not here.

```markdown
# Engineering Workflows

How to build, test and ship [project name]. Coding standards live in `CODING_STANDARDS.md`.

---

## Root README.md policy

README.md exists to answer:
- what this repo is
- how to run it locally
- where to find canonical documentation

Agents should update README.md when dev commands change, ports or startup steps change, or links to docs move.

Agents should not describe feature behavior, list API endpoints, or include request/response schemas. Canonical documentation lives under `{{DOCS_DIR}}/`.

---

[If pre-commit hooks were found: a "## Setup" section with the install step and what each hook runs.]

---

[If a git platform and/or CI system was detected, insert the CI/CD section
from platform-adapters.md here. If no CI detected: omit.]

---

[Insert the issue/work-item linking section from platform-adapters.md for the confirmed tracker.]

---

[If a clear commit-message convention was detected: a "## Commit messages" section with one example in the repo's actual style. Otherwise omit.]

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
[format command]                  # format (if applicable)
[lint command]                    # lint (if applicable)
[migration command]               # run database migrations (if applicable)
```

---

## Completion checklist

The completion checklist lives in `AGENTS.md`, so there is exactly one.
```

---

## {{DOCS_DIR}}/FEATURES.md

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

When listing (no link until the feature doc exists):
"- area-name — one-line description (_not documented yet_)"

If the project is new or feature boundaries are unclear:]

_No feature areas documented yet. Add entries as you build out the system._

---

## Rules for agents

- Introducing a new feature area requires:
  - creating `{{DOCS_DIR}}/features/<feature>.md`
  - adding it to this list (alphabetical), linked to that file
- An entry marked _not documented yet_ has no file yet: write it (or run the Mimas `document-features` skill, installed separately) and turn the entry into a link
- Per-service docs live under `{{DOCS_DIR}}/features/<area>/` and are linked from the area doc
- Renaming or merging features requires updating links and notes
- This file should remain concise and navigable
```

---

## GLOSSARY.md

The domain language, in the format the `/domain-modeling` skill defines (`GLOSSARY-FORMAT.md` in that skill). Glossaries are created lazily: write one now **only** if Phase 1 surfaced clear, project-specific domain terms (distinctive type, table or route names that mean something to the business). Otherwise skip it — `/domain-modeling`, `/grill-with-docs` and the triggers in `{{DOCS_DIR}}/AGENT_WORKFLOW.md` create it when the first term is resolved.

Single-context repos (almost all) get one `GLOSSARY.md` at the repo root. Never put implementation detail or agent rules in it.

```markdown
# [Context Name]

[One or two sentences on what this context is and why it exists, in domain terms.]

## Language

**[Term]**:
[One or two sentences defining what it IS, not what it does.]
_Avoid_: [Synonym1, Synonym2]
```

---

## GLOSSARY-MAP.md

Only when the user confirmed a **multi-context** layout in Phase 2 (monorepo signals). It sits at the repo root and points to one `GLOSSARY.md` per context, each created lazily like the single-context one.

```markdown
# Glossary Map

## Contexts

- [[Context]](./[path]/GLOSSARY.md): [one-line purpose]

## Relationships

- **[Context A] → [Context B]**: [how they couple — events, shared types]
```
