# File Templates

Base templates for every file the skill generates. Instructions in `[brackets]` tell you what to write — replace them with real content from Phase 1 and the user interview. Merge in relevant sections from `tech-adapters.md` and `platform-adapters.md` where indicated.

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

## docs/AGENT_WORKFLOW.md

This file is largely universal — it describes how agents should approach work on any project. Customize the "Task Management" section if the repo has an existing task tracking setup, and add the platform-specific "Pull Requests" (or "Merge Requests") section from `platform-adapters.md`.

```markdown
# Agent Workflow & Operating Instructions

These rules apply to **all AI agents** working on this project, regardless of platform or model.

Read this file at the start of every session.

---

## Workflow Orchestration

### 1. Plan Mode Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy

- Use subagents liberally to keep the main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop

- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant context

### 4. Verification Before Done

- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user

---

[If a git platform was detected or confirmed by the user, insert the Pull Requests
(or Merge Requests for GitLab) section from platform-adapters.md here.
If no platform: omit this section entirely.]

---

## Task Management

Track ongoing work in `tasks/`. After any correction from the user, record the lesson in `tasks/lessons.md` (create the file if absent). This captures agent self-improvement separate from feature work.

---

## Core Principles

- **Simplicity First:** Make every change as simple as possible. Impact minimal code.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Changes should only touch what's necessary. Avoid introducing bugs.
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

## docs/AGENTS_FEATURES.md

This file is universal. Copy it as-is — the structure and rules don't change between projects.

```markdown
# Agent Instructions: Feature Areas & Documentation

All feature documentation lives under **`docs/features/`**:

- **Area-level docs** (`docs/features/<area>.md`): concept-first overview of a feature area — responsibilities, boundaries, key concepts.
- **Per-service docs** (`docs/features/<area>/<service>.md`): API contracts, request/response schemas, implementation details, changelogs.

This document defines how agents must detect, document, and maintain feature knowledge as the codebase grows.

> This file is part of the agent instruction infrastructure.
> Do NOT create, delete, or modify this file unless explicitly instructed.

---

## What is a feature area?

A feature area is a named concept that:
- appears in API routes, domain services, or handlers
- has dedicated logic in the codebase
- represents a coherent responsibility or capability

Feature areas are identified **by naming and behavior**, not by folder structure alone.

---

## Feature Documentation Contract (MANDATORY)

### When to create or update area-level docs (`docs/features/<slug>.md`)

- New feature area introduced → create `docs/features/<slug>.md` and add to `docs/FEATURES.md` (alphabetical).
- Changes to **responsibilities, boundaries, workflows, or high-level behavior** → update the relevant area doc in the same task.

### When to create or update per-service docs (`docs/features/<area>/<service>.md`)

- **API contracts change** (endpoints, request/response schemas, versioning) → update the corresponding doc.
- **New API or capability** → create a per-service doc and link it from the area doc.
- **Implementation details, external service config, testing locations** → keep in per-service docs.

### When an existing feature area changes

If a change affects any of the following, update the **appropriate** doc in the same task — not as a follow-up:

- public API behavior or contracts → per-service doc
- schemas or shared types → per-service doc
- invariants or business rules → area-level doc

### When a feature is renamed, merged, or split

You MUST:
- Create or update the new feature doc(s)
- Add a short note near the top (e.g. "Renamed from …" or "Merged from …")
- Update `docs/FEATURES.md` as needed

---

## How to write feature docs

**Area-level docs (`docs/features/<area>.md`):**
- concept-first, not file-path-first
- responsibilities and boundaries
- key concepts and vocabulary
- links to per-service docs for API and implementation detail

**Per-service docs (`docs/features/<area>/<service>.md`):**
- API endpoint, request/response, business logic, technical implementation, testing, changelog
- Use [`docs/features/feature-template.md`](./features/feature-template.md) as the canonical template

### Avoid:
- Duplicating process rules (TDD, typecheck, etc.) in feature docs
- Listing volatile file paths unless they are stable

### Progressive disclosure

If a feature grows complex:
- Split deep detail into focused per-service docs under `docs/features/<area>/`
- Link to them from the area-level doc
- Do NOT duplicate large sections of content between area and per-service docs
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

## docs/features/feature-template.md

Copy this verbatim. It is a template for future feature docs — not a doc itself. Agents will use this as a starting point when creating new per-service feature documentation.

The template is deliberately comprehensive. When agents create a real feature doc from this template, they should **delete sections that don't apply** rather than leaving them empty. A frontend feature won't need "Rate Limiting"; a utility library won't need "API Endpoint". The template covers the superset.

```markdown
# [Feature Name]

> **Area:** [area-name]
> **Status:** Active | In Progress | Deprecated
> **Last updated:** YYYY-MM-DD

## Overview

One paragraph describing what this feature does and why it exists.

## Responsibilities

- What this feature is responsible for
- Its boundaries — what it does NOT own

## Key concepts

- **ConceptA**: short definition
- **ConceptB**: short definition

---

## API Endpoint

### Endpoint Details
- **Method**: [GET | POST | PUT | PATCH | DELETE]
- **Path**: `/api/v1/[feature-path]`
- **Authentication**: [Required | Optional | None]
- **Rate Limiting**: [Yes — describe | No]

### Request Schema

```json
{
  "field": "type — description"
}
```

**Required fields:**
- `field` (type, constraints): description

**Optional fields:**
- `field` (type): description. Defaults to "X" if not provided.

### Response Schema

```json
{
  "field": "type — description"
}
```

### Error Responses

- **400 Bad Request**: [specific causes]
- **401 Unauthorized**: missing or invalid authentication
- **404 Not Found**: [when this applies]
- **500 Internal Server Error**: [specific causes]

---

## Business Logic

### Core Functionality

1. **Step 1**: description
2. **Step 2**: description
3. **Step 3**: description

### Business Rules

- Rule 1
- Rule 2

### Data Flow

```
Input → Validation → [Processing Steps] → Response
```

### Dependencies

- **Service/Library**: what it's used for
- **External API**: what it's used for
- **Database**: what tables/collections are involved

---

## Technical Implementation

### Service Layer

- **Location**: `path/to/service`
- **Key methods**: `methodName()` — description

### Controller / Handler

- **Location**: `path/to/handler`
- **Responsibilities**: request validation, service invocation, response formatting

### Repository / Data Access

- **Location**: `path/to/repository`
- **Tables/Collections**: list the relevant database objects
- **Migrations**: reference the migration that created/modified the schema

### Key Types

- `TypeName`: description of what it represents

---

## Configuration

### Environment Variables

- `VAR_NAME`: description (required | optional, default: X)

### Feature Flags

- [List any feature flags, or "None"]

---

## Testing

### Unit Tests

- **Location**: `path/to/tests`
- **Key scenarios**: list the most important test cases

### Integration Tests

- **Location**: `path/to/integration/tests`
- **Setup**: describe any required infrastructure (database, external services, etc.)
- **Mocking**: what external services are mocked and how

---

## Error Handling & Edge Cases

### Common Errors

- **Error scenario**: how it's handled

### Edge Cases

- **Edge case**: expected behavior

---

## Security Considerations

- Authentication requirements
- Authorization / access control
- Input validation and sanitization
- Data privacy considerations

---

## Performance Considerations

- Expected response times
- Known bottlenecks
- Caching strategy (if any)

---

## Known Issues and Limitations

1. **Limitation**: description

---

## Related Features

- **[Related Feature]**: brief description of relationship

## Changelog

| Date | Change |
|------|--------|
| YYYY-MM-DD | Initial documentation |
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
