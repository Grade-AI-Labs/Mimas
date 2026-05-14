# Agent Instructions: CONTEXT.md & CONTEXT-MAP.md

Domain documentation lives in **`CONTEXT.md`** files co-located with the code they describe:

- **Single-context repo:** one `CONTEXT.md` at the root (or at the top of the single subdomain).
- **Multi-context repo:** one `CONTEXT.md` per subdomain (e.g. `src/CONTEXT.md`, `frontend/CONTEXT.md`), indexed by `docs/CONTEXT-MAP.md`.

This document defines how agents must detect, document, and maintain domain knowledge as the codebase grows.

> This file is part of the agent instruction infrastructure.
> Do NOT create, delete, or modify this file unless explicitly instructed.

---

## What `CONTEXT.md` is for

A subdomain's `CONTEXT.md` is a **domain artefact**, not an agent-rule file. It captures:

- **Vocabulary** — the bounded-context glossary: the domain terms used here, with one-sentence definitions and the aliases to avoid.
- **Relationships** — how the domain terms connect (cardinality, ownership).
- **Boundaries / IO** — what this subdomain exposes externally and consumes from other subdomains.
- **Invariants** — rules that always hold within this subdomain.
- **Flagged ambiguities** — terms still in dispute, with proposed resolutions.

Agent-procedural rules (TDD, typecheck, formatter) live in `/AGENTS.md` and `docs/ENGINEERING.md` — never in `CONTEXT.md`.

Implementation detail (file paths, function names, request schemas) belongs in `docs/features/<area>.md` — never in `CONTEXT.md`.

## What `CONTEXT-MAP.md` is for

The system-level index of bounded contexts in a multi-context repo. One row per subdomain — name, one-line purpose, public surface, link to its `CONTEXT.md`. Plus relationships between contexts (upstream/downstream, shared types, events).

Only exists when ≥2 subdomains have their own `CONTEXT.md`. Single-context repos skip it.

---

## CONTEXT Contract (MANDATORY)

### Read at session start

Before working in a subdomain:

1. Read that subdomain's `CONTEXT.md`. If `docs/CONTEXT-MAP.md` exists, start there to locate the right one.
2. If your change couples two subdomains (shared types, cross-context events), read both `CONTEXT.md`s.
3. Skip files that don't exist. **Proceed silently** — don't flag absence; producer triggers create them lazily.

### Use the vocabulary verbatim

When your output names a domain concept — in an issue title, a refactor proposal, a hypothesis, a test name, a variable name, an error message — use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

### Flag gaps; don't invent

If the concept you need isn't in the glossary yet, that's a signal:
- Either you're inventing language the project doesn't use → reconsider.
- Or there's a real gap → add it (see triggers below). Don't silently coin a new term.

### Update in the moment

When a trigger fires — see `docs/AGENT_WORKFLOW.md` § 4 CONTEXT.md upkeep for the canonical trigger list — update the relevant `CONTEXT.md` in the same turn, before reporting work done. The triggers cover term resolutions, user corrections to terminology, new concepts introduced by features, and self-caught synonym invention.

### Append-only discipline

- Add new entries; don't reshuffle existing ones (keeps diffs sane).
- If a term changes meaning, supersede it with a clarifying entry — don't silently rewrite history.
- If `Flagged ambiguities` gets resolved, move the resolution into the main vocabulary table and remove the flag.

### Multi-context: keep the map current

When adding a new subdomain `CONTEXT.md`, add a row to `docs/CONTEXT-MAP.md` in the same task. When the public surface or upstream/downstream relationships change, update the map.

---

## Format

The format of an entry is documented at the top of each `CONTEXT.md` so it self-describes. Briefly:

- **Vocabulary table** — bold term, one-sentence definition, aliases to avoid.
- **Relationships** — bullet list using bold terms and cardinality ("A **TermA** belongs to exactly one **TermB**").
- **Boundaries / IO** — `Exposes:` and `Consumes:` bullets.
- **Invariants** — bullet list of constraints that always hold.
- **Flagged ambiguities** — terms still in dispute, with proposed resolutions.
