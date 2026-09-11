# ADR Format

> **This file is the fallback.** If the repo has an `agents-docs/` tree, `agents-docs/AGENTS_ADRS.md` is authoritative — read it and follow it over this file. What's below mirrors that contract so an un-scaffolded repo ends up with the same shape.

## Where ADRs live

All ADRs go in the single **`agents-docs/adr/`** directory, as `NNNN-slug.md`. One central tree — don't scatter per-subdomain `adr/` folders; a context-specific decision still lands here.

Create the directory lazily: only when the first ADR is needed.

## Numbering

Scan `agents-docs/adr/` for the highest existing number and increment by one. Four digits, zero-padded, kebab-case slug describing the decision: `0042-postgres-for-write-model.md`, `0043-event-sourced-orders.md`.

## Template

Nygard short form. **Context**, **Decision** and **Rationale** are required, 1–3 sentences each; `Status` is conventional.

```md
# ADR-NNNN: {Short title of the decision}

## Status
{Proposed | Accepted | Superseded by ADR-MMMM}

## Context
{1–3 sentences: what prompted this, what constraint or fork was hit.}

## Decision
{1–3 sentences: what was chosen, plainly stated.}

## Rationale
{1–3 sentences: why this option over the alternatives.}
```

Keep them short — three sentences per section beats three paragraphs. The value is in recording *that* a decision was made and *why*, not in filling out sections.

## Optional sections

Add only when they earn their place. Most ADRs need neither.

- **Considered Options** — when the rejected alternatives are worth remembering
- **Consequences** — when non-obvious downstream effects, especially constraints this locks in, need calling out

## Supersede, don't delete

ADRs are append-only. When a decision is overturned, write a new one; the old file stays. Add `Superseded by ADR-NNNN` near the top of the old ADR and `Supersedes ADR-MMMM` near the top of the new one. Never delete or rewrite history.

Before a non-trivial change, scan `agents-docs/adr/` for decisions touching the area. If your work would contradict one, surface it explicitly — "_Contradicts ADR-NNNN (slug) — but worth reopening because…_" — rather than silently overriding it.

## When to offer an ADR

All three must be true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it: you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library: just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it; otherwise someone will suggest GraphQL again in six months.
