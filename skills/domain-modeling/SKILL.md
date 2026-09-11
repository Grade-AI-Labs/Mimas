---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR.
metadata:
  author: Olof Brogeby & Matt Pocock
  url: https://github.com/brogeby, https://github.com/mattpocock
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## The contracts come first

If this repo was scaffolded by `setup-agentic-repository`, it already carries the authoritative contracts for both artefacts this skill writes:

- **`agents-docs/AGENTS_CONTEXT.md`** — the `CONTEXT.md` / `CONTEXT-MAP.md` contract.
- **`agents-docs/AGENTS_ADRS.md`** — the ADR contract.
- **`agents-docs/AGENT_WORKFLOW.md`** §§ 4–5 — the canonical upkeep triggers.

**Read those before writing anything, and follow them over this file where they differ.** They are the project's source of truth; this skill only tells you how to *drive the conversation* that fills them in. Never edit those contract files themselves — they're agent instruction infrastructure.

**Discover the docs dir; don't hardcode it.** It defaults to `agents-docs/`, but `setup-agentic-repository` accepts a `--docs-dir` override:

1. Read `AGENTS.md` at the repo root — every Mimas-generated one lists its docs paths in the first block. The directory in those paths is the docs dir.
2. If that fails, search for the contract directly: `find . -maxdepth 3 -name AGENTS_CONTEXT.md`. The directory containing it is the docs dir.

Treat the discovered directory as `<docs-dir>` and use it wherever a path appears below — the `agents-docs/` in the examples is only the default.

If the repo has **no** such tree, fall back to the bundled formats: [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) and [ADR-FORMAT.md](./ADR-FORMAT.md). They match the scaffolded contracts, so the model you build transfers cleanly if the repo is scaffolded later.

## File structure

A scaffolded single-context repo:

```
/
├── AGENTS.md
├── agents-docs/
│   ├── AGENTS_CONTEXT.md
│   ├── AGENTS_ADRS.md
│   └── adr/
│       ├── 0001-record-architectural-decisions.md
│       └── 0002-postgres-for-write-model.md
└── src/
    └── CONTEXT.md          ← one per subdomain, at its top level
```

With two or more subdomains, `agents-docs/CONTEXT-MAP.md` indexes them:

```
/
├── agents-docs/
│   ├── CONTEXT-MAP.md      ← index of bounded contexts
│   └── adr/                ← all ADRs, system-wide and context-specific
├── src/
│   ├── ordering/CONTEXT.md
│   └── billing/CONTEXT.md
```

Three things to get right:

- **`CONTEXT.md` sits at the top level of a subdomain**, never deeper. `src/CONTEXT.md`, not `src/routes/CONTEXT.md`.
- **ADRs are centralised** in the one `agents-docs/adr/` directory. Don't scatter per-subdomain `adr/` folders; a context-specific decision still lands in the central tree.
- **`CONTEXT-MAP.md` lives under `agents-docs/`**, not at the repo root, and only exists when ≥2 subdomains have their own `CONTEXT.md`.

Create files lazily: only when you have something to write. If the relevant `CONTEXT.md` doesn't exist, create it when the first term is resolved. When you add a new subdomain `CONTEXT.md` to a multi-context repo, add its row to `CONTEXT-MAP.md` in the same turn.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update CONTEXT.md inline

When a term is resolved, update the relevant `CONTEXT.md` right there. Don't batch these up: capture them as they happen, before reporting any work done.

A `CONTEXT.md` is a **domain artefact**, holding vocabulary, the relationships between those terms, the subdomain's boundaries and IO, its invariants, and any flagged ambiguities. It is not a spec, a scratch pad, or a home for implementation decisions — no file paths, function names, or request schemas (those belong in `agents-docs/features/<area>.md`), and no agent-procedural rules like TDD or typecheck (those belong in `AGENTS.md` and `agents-docs/ENGINEERING.md`).

**Append-only.** Add new entries; don't reshuffle existing ones — it keeps diffs reviewable. If a term changes meaning, supersede it with a clarifying entry rather than rewriting history. When a flagged ambiguity is resolved, move it into the vocabulary table and drop the flag.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR.

When all three hold, write it in the same turn as the decision. Scan `agents-docs/adr/` for the highest existing number and increment it, zero-padded to four digits, with a kebab-case slug: `0042-postgres-for-write-model.md`.

**Supersede, don't delete.** If a decision is overturned, write a new ADR; the old one stays, annotated `Superseded by ADR-NNNN`, and the new one notes `Supersedes ADR-MMMM`. Before making a non-trivial change, scan `agents-docs/adr/` for decisions that touch the area — if your work contradicts one, surface it explicitly rather than silently overriding it.
