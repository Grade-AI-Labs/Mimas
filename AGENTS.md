# AGENTS.md

Read these files at the start of every session before doing any work:

1. `docs/AGENT_WORKFLOW.md` — workflow and operating rules
2. `docs/AGENTS_FEATURES.md` — when and how to update feature docs
3. `docs/FEATURES.md` — feature index
4. `docs/ENGINEERING.md` — engineering standards

When touching the backend source, also read `src/AGENTS.md`.

---

This is a single-package Node.js/TypeScript project — a Fastify backend (`src/`) with:
- Domain-based service architecture under `src/domains/`
- Kysely for database access
- LangChain + Langfuse for generative AI features
- Jest for testing

## CRITICAL — Non-negotiable rules for all agents

### Test-Driven Development (MANDATORY)
**You MUST ALWAYS write tests before implementation code.**

When creating or changing anything:
1. STOP — do not write implementation first
2. Write failing tests (RED)
3. Run tests and confirm failure (`npm test -- --testPathPattern=<your-test>`)
4. Write minimal code to pass tests (GREEN)
5. Refactor while keeping tests green

This applies to **all code**:
- API routes & controllers
- Domain services & repositories
- Schemas & validation
- Database logic & migrations
- Generative AI services & prompts

**NO EXCEPTIONS.**

### TypeScript correctness (MANDATORY)
Before completing any task:
1. Run `npx tsc --noEmit` from the repo root
2. Fix all TypeScript errors
3. Do not consider work complete until it exits with code 0

## Most important rule

After any change that affects API contracts, schemas, invariants, workflows, or major behavior: update the relevant `docs/features/<slug>.md` as part of the same task — not as a follow-up. New feature area → create `docs/features/<slug>.md` and add an entry to `docs/FEATURES.md` (alphabetical).

## Structure of further instructions

- **Agent workflow & operating rules:** `docs/AGENT_WORKFLOW.md`
- **Engineering standards:** `docs/ENGINEERING.md`
- **Feature documentation contract:** `docs/AGENTS_FEATURES.md`
- **Feature index:** `docs/FEATURES.md`
- **Project context & tech stack:** `openspec/project.md`
- **Application architecture:** `openspec/specs/application.md`
- **Feature specs (deep):** `openspec/specs/features/`
- **Feature docs (behavioral):** `docs/features/`
- **Source-level instructions:** `src/AGENTS.md`

Keep this file minimal. Do not duplicate detailed rules here.

## Completion checklist

Before marking work complete:

- [ ] Tests written before implementation
- [ ] All tests passing
- [ ] `npx tsc --noEmit` passes
- [ ] Naming conventions followed
- [ ] Errors handled
- [ ] Feature docs updated if contract/schema/invariant changed (see docs/AGENTS_FEATURES.md)

## README maintenance

The root README.md is an entry point for developers.

Agents MAY update README.md to:
- keep setup steps, commands, and ports accurate
- update links to canonical documentation
- reflect changes to project structure or dev workflows

Agents MUST NOT:
- add feature-level documentation
- document API endpoints or payloads
- duplicate content from `openspec/specs/features/`

Feature behavior belongs in feature docs, not README.md.
