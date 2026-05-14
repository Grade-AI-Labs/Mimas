# File Templates

Templates for the **project-specific** files the LLM generates. Instructions in `[brackets]` tell you what to write — replace them with real content from Phase 1 and the user interview. Merge in relevant sections from `tech-adapters.md` and `platform-adapters.md` where indicated.

Verbatim files (CLAUDE.md, AGENT_WORKFLOW.md, AGENTS_FEATURES.md, feature-template.md) are handled by `scripts/scaffold.py` — they are NOT in this file.

Every generated file should read as if a senior engineer on this project wrote it — specific, accurate, and proportionate.

---

## /AGENTS.md

```markdown
# AGENTS.md

Read these files at the start of every session before doing any work:

1. `{{DOCS_DIR}}/AGENT_WORKFLOW.md` — workflow and operating rules
2. `{{DOCS_DIR}}/LESSONS.md` — durable rules learned from past corrections; apply any that match this session's work
3. `{{DOCS_DIR}}/AGENTS_FEATURES.md` — when and how to update feature docs
4. `{{DOCS_DIR}}/FEATURES.md` — feature index
5. `{{DOCS_DIR}}/ENGINEERING.md` — engineering standards
[If multi-context (≥2 subdomains): "6. `{{DOCS_DIR}}/CONTEXT-MAP.md` — index of bounded contexts in this repo"]

Reference on-demand (when the workflow triggers them — see `{{DOCS_DIR}}/AGENT_WORKFLOW.md` §§ 4–5):

- `{{DOCS_DIR}}/AGENTS_CONTEXT.md` — contract for updating `CONTEXT.md` / `CONTEXT-MAP.md`
- `{{DOCS_DIR}}/AGENTS_ADRS.md` — contract for writing architecture decision records

[If the repo has subdomains, add a line per subdomain. Example:
"When working in the backend source, also read `src/CONTEXT.md`."
"When working on the frontend, also read `frontend/CONTEXT.md`."]

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

After any change that affects API contracts, schemas, invariants, workflows, or major behavior: update the relevant `{{DOCS_DIR}}/features/<slug>.md` as part of the same task — not as a follow-up. New feature area → create `{{DOCS_DIR}}/features/<slug>.md` and add an entry to `{{DOCS_DIR}}/FEATURES.md` (alphabetical).

## Structure of further instructions

- **Agent workflow & operating rules:** `{{DOCS_DIR}}/AGENT_WORKFLOW.md`
- **Agent lessons (durable cross-session rules):** `{{DOCS_DIR}}/LESSONS.md`
- **Engineering standards:** `{{DOCS_DIR}}/ENGINEERING.md`
- **Feature documentation contract:** `{{DOCS_DIR}}/AGENTS_FEATURES.md`
- **CONTEXT documentation contract:** `{{DOCS_DIR}}/AGENTS_CONTEXT.md`
- **ADR contract:** `{{DOCS_DIR}}/AGENTS_ADRS.md`
- **Feature index:** `{{DOCS_DIR}}/FEATURES.md`
- **Feature docs:** `{{DOCS_DIR}}/features/`
- **Architecture decisions:** `{{DOCS_DIR}}/adr/`
[If multi-context (≥2 subdomains): "- **Context map:** `{{DOCS_DIR}}/CONTEXT-MAP.md`"]
[Add one line per subdomain. Example:
"- **Backend source domain:** `src/CONTEXT.md`"
"- **Frontend domain:** `frontend/CONTEXT.md`"]

Keep this file minimal. Do not duplicate detailed rules here.

## Completion checklist

Before marking work complete:

- [ ] Tests written before implementation
- [ ] All tests passing
[If type checking exists: "- [ ] `[typecheck command]` passes"]
[If linter exists: "- [ ] `[lint command]` passes"]
- [ ] Naming conventions followed
- [ ] Errors handled
- [ ] Feature docs updated if contract/schema/invariant changed (see {{DOCS_DIR}}/AGENTS_FEATURES.md)
- [ ] `CONTEXT.md` updated if a domain term was resolved or introduced (see {{DOCS_DIR}}/AGENTS_CONTEXT.md)
- [ ] ADR written if a hard-to-reverse decision was made (see {{DOCS_DIR}}/AGENTS_ADRS.md)
- [ ] Lesson recorded in `{{DOCS_DIR}}/LESSONS.md` if this session produced a correction, revert, or hidden constraint (see triggers in `{{DOCS_DIR}}/AGENT_WORKFLOW.md`)
[If git platform detected: insert completion checklist additions from platform-adapters.md.
Example for GitHub:
"- [ ] PR opened with summary and linked issues"
"- [ ] CI checks passing"
If no platform: omit these items.]
```

---

## {{DOCS_DIR}}/ENGINEERING.md

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

Agents should not describe feature behavior, list API endpoints, or include request/response schemas. Canonical documentation lives under `{{DOCS_DIR}}/`.

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
* [ ] Feature docs updated if contract/schema/invariant changed (see {{DOCS_DIR}}/AGENTS_FEATURES.md)
* [ ] `CONTEXT.md` updated if a domain term was resolved or introduced (see {{DOCS_DIR}}/AGENTS_CONTEXT.md)
* [ ] ADR written if a hard-to-reverse decision was made (see {{DOCS_DIR}}/AGENTS_ADRS.md)
* [ ] Lesson recorded in `{{DOCS_DIR}}/LESSONS.md` if this session produced a correction, revert, or hidden constraint (see triggers in `{{DOCS_DIR}}/AGENT_WORKFLOW.md`)
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

When listing:
"- [area-name](./features/area-name.md) — one-line description"

If the project is new or feature boundaries are unclear:]

_No feature areas documented yet. Add entries as you build out the system._

---

## Rules for agents

- Introducing a new feature area requires:
  - creating `{{DOCS_DIR}}/features/<feature>.md`
  - adding it to this list (alphabetical)
- Per-service docs live under `{{DOCS_DIR}}/features/<area>/` and are linked from the area doc
- Renaming or merging features requires updating links and notes
- This file should remain concise and navigable
```

---

## `<subdomain>/CONTEXT.md`

Create one per discovered subdomain. **Domain-bearing, not procedural** — captures the bounded-context vocabulary, relationships, IO, and invariants. Agent rules (TDD, typecheck, etc.) live in `/AGENTS.md`, not here. Implementation detail (file paths, request schemas) lives in `{{DOCS_DIR}}/features/`, not here.

Scaffold the skeleton eagerly so agents know where to write. Leave Vocabulary / Invariants empty until real content arrives — they get filled in lazily via the triggers in `{{DOCS_DIR}}/AGENT_WORKFLOW.md`.

```markdown
# [Subdomain Name]

[One or two sentences describing what this subdomain owns, in domain terms — not "this is the React frontend code". Example: "Owns recruitment-content generation: turning a recruiter brief into structured job posts, screening questions, and interview prompts."]

> **Format reference:**
> - **Vocabulary** — bold term, one-sentence definition, aliases to avoid.
> - **Relationships** — bullets with bold terms and cardinality.
> - **Boundaries / IO** — what this subdomain exposes and consumes.
> - **Invariants** — rules that always hold.
> - **Flagged ambiguities** — terms in dispute with proposed resolutions.
>
> See `{{DOCS_DIR}}/AGENTS_CONTEXT.md` for the contract. Update in the same turn a trigger fires (see `{{DOCS_DIR}}/AGENT_WORKFLOW.md` § CONTEXT.md upkeep).

## Vocabulary

| Term | Definition | Aliases to avoid |
|------|------------|------------------|
| **[Term]** | [One-sentence definition.] | [Synonym1, Synonym2] |

## Relationships

- [Example: "A **Candidate** has zero or more **Applications**."]
- [Example: "An **Application** belongs to exactly one **Role**."]

## Boundaries / IO

- **Exposes:** [public surface — REST endpoints, events emitted, shared types other subdomains consume]
- **Consumes:** [what this subdomain reads from other subdomains — events subscribed, shared services, cross-context types]

## Invariants

- [Example: "An **Application** cannot exist without a **Candidate**."]

## Flagged ambiguities

- [Terms still in dispute. Resolve via the triggers in `{{DOCS_DIR}}/AGENT_WORKFLOW.md` and move resolutions into the Vocabulary table above.]

---

*Agent-procedural rules (TDD, typecheck, etc.) live in `/AGENTS.md`. Implementation detail belongs in `{{DOCS_DIR}}/features/`. This file is the bounded-context domain artefact.*
```

---

## {{DOCS_DIR}}/CONTEXT-MAP.md

Only generated when **≥2 subdomains** are detected. Single-context repos skip this file — the single `CONTEXT.md` is enough.

```markdown
# Context Map

Bounded contexts in this system. Before working in a subdomain, read its `CONTEXT.md`. See `{{DOCS_DIR}}/AGENTS_CONTEXT.md` for the contract.

## Contexts

| Context | Purpose | Public surface | CONTEXT.md |
|---------|---------|----------------|------------|
| **[name]** | [one-line purpose] | [one-line: endpoints / events emitted / shared types] | `[path]/CONTEXT.md` |

## Relationships

[Document cross-context coupling — upstream/downstream, shared types, events. Examples:
- "**Recruitment** is upstream of **Assessment** via the `candidate-created` event."
- "**Offer** depends on **Recruitment** for the shared `Candidate` type."
- "**Sourcing** and **Recruitment** are partners — they share the `Application` lifecycle bidirectionally."]

## Rules for agents

- Add a row when a new subdomain gains its own `CONTEXT.md`.
- Update the public surface or relationships when they change.
- Keep this file scannable — one row per context, terse purpose strings.
```
