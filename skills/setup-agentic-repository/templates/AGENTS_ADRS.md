# Agent Instructions: Architecture Decision Records (ADRs)

Architectural decisions live in **`{{DOCS_DIR}}/adr/`** as numbered Markdown files (`NNNN-slug.md`).

This document defines how agents must detect, document, and maintain architectural decisions as the codebase grows.

> This file is part of the agent instruction infrastructure.
> Do NOT create, delete, or modify this file unless explicitly instructed.

---

## What an ADR is

A short record of an architectural decision that future engineers (and agents) will need context for. The format is Nygard short form:

- Title and number (`ADR-NNNN: <slug>`).
- Required: 1–3 sentences each covering **Context** (why this came up), **Decision** (what was chosen), and **Rationale** (why this option over alternatives).
- Conventional: `Status` (usually `Accepted` for new ADRs; `Superseded by ADR-MMMM` once overturned).
- Optional: `Considered Options`, `Consequences` — add only when they genuinely help. Most ADRs won't need them.

See `{{DOCS_DIR}}/adr/0001-record-architectural-decisions.md` for the canonical example — a minimal four-section ADR that matches the typical shape.

The value is in recording **that a decision was made** and **why** — not in completing formal sections.

---

## ADR Contract (MANDATORY)

### When to write an ADR

The canonical criteria — the 3-criteria gate — live in `{{DOCS_DIR}}/AGENT_WORKFLOW.md` § 5 ADR upkeep. Read those before writing. In short: write an ADR only when the decision is **hard to reverse**, **surprising without context**, and the **result of genuine trade-offs**. If any of the three is missing, don't.

Suitable topics: architectural patterns, integration approaches, significant technology selections, scope boundaries, intentional deviations from standard practices, non-obvious rejections of alternatives.

### Read before crossing decision boundaries

Before non-trivial changes in an area, scan `{{DOCS_DIR}}/adr/` for decisions that touch it. If your work would contradict an existing ADR:

- **Surface it explicitly**, don't silently override. Phrase it as: "_Contradicts ADR-NNNN (slug) — but worth reopening because…_"
- If the contradiction is intentional, write a new ADR that supersedes the old one (see below).

### Write the ADR in the same turn as the decision

When the 3-criteria gate is met, write the ADR before reporting the task done. The `AGENTS.md` completion checklist has a line for this; don't tick the box without it.

### Numbering

Scan `{{DOCS_DIR}}/adr/` for the highest existing number; the new ADR is `NNNN+1`. Use 4-digit zero-padded numbers (`0001`, `0002`, …).

Slugs are kebab-case and describe the decision concisely: `0042-postgres-for-write-model.md`, `0043-event-sourced-orders.md`.

### Supersede, don't delete

ADRs are append-only:

- When a decision is overturned, write a new ADR. The old one stays.
- Add `Superseded by ADR-NNNN` near the top of the old ADR.
- Add `Supersedes ADR-MMMM` near the top of the new one.
- Never delete or rewrite history.

---

## Format

```markdown
# ADR-NNNN: <Slug Title>

## Status
<Proposed | Accepted | Superseded by ADR-MMMM>

## Context
<1–3 sentences: what prompted this decision, what constraint or fork was hit.>

## Decision
<1–3 sentences: what was chosen, plainly stated.>

## Rationale
<1–3 sentences: why this option over the alternatives.>

<!-- Optional sections, only when they help: -->

## Considered Options
<bullet list of alternatives evaluated and rejected>

## Consequences
<bullet list of follow-on effects, especially constraints this locks in>
```

Keep ADRs short. Three sentences per section beats three paragraphs.
