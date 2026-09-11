# CONTEXT.md Format

> **This file is the fallback.** If the repo has an `agents-docs/` tree, `agents-docs/AGENTS_CONTEXT.md` is authoritative — read it and follow it over this file. What's below mirrors that contract so an un-scaffolded repo ends up with the same shape.

## What it is

A `CONTEXT.md` is a **bounded-context domain artefact**: the vocabulary of one subdomain, how those terms relate, what the subdomain exposes and consumes, and the rules that always hold.

It is not a spec and not a scratch pad. Two things never belong in it:

- **Implementation detail** — file paths, function names, request schemas. Those go in `agents-docs/features/<area>.md`.
- **Agent-procedural rules** — TDD, typecheck, formatter. Those go in `AGENTS.md` and `agents-docs/ENGINEERING.md`.

## Where it lives

One `CONTEXT.md` at the **top level of each subdomain** — `src/CONTEXT.md`, `frontend/CONTEXT.md`, `packages/auth/CONTEXT.md` — never deeper, and never for utility, config, or generated directories.

## Structure

```md
# {Subdomain Name}

{One or two sentences on what this subdomain owns, in domain terms.}

## Vocabulary

| Term | Definition | Aliases to avoid |
|------|------------|------------------|
| **Order** | A customer's request to purchase goods, priced and confirmed. | Purchase, transaction |
| **Invoice** | A request for payment sent to a customer after delivery. | Bill, payment request |

## Relationships

- A **Customer** places zero or more **Orders**.
- An **Invoice** belongs to exactly one **Order**.

## Boundaries / IO

- **Exposes:** `POST /orders`, the `OrderPlaced` event, the shared `OrderId` type
- **Consumes:** the `ShipmentDispatched` event from Fulfillment

## Invariants

- An **Invoice** cannot exist without a delivered **Order**.

## Flagged ambiguities

- **Cancellation** — partial vs. whole-order is unresolved. Proposed: whole-order only.
```

## Rules

- **Be opinionated.** When several words exist for one concept, pick the best and list the rest under *Aliases to avoid*.
- **Keep definitions tight.** One sentence. Define what it IS, not what it does.
- **Only project-specific terms.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project leans on them heavily. Before adding a term, ask: is this unique to this context, or generic? Only the former belongs.
- **Append-only.** Add entries; don't reshuffle existing ones — it keeps diffs reviewable. If a term changes meaning, supersede it with a clarifying entry rather than rewriting history.
- **Resolve flags upward.** When a flagged ambiguity is settled, move it into the Vocabulary table and delete the flag.
- **Populate lazily.** Leave *Vocabulary* and *Invariants* thin until real content arrives; they fill in as triggers fire, not up front.

## Single vs multi-context repos

**Single context (most repos):** one `CONTEXT.md` at the top of the single subdomain. No map.

**Two or more contexts:** each subdomain gets its own `CONTEXT.md`, indexed by **`agents-docs/CONTEXT-MAP.md`** — under the agent docs root, *not* at the repo root:

```md
# Context Map

Bounded contexts in this system. Before working in a subdomain, read its `CONTEXT.md`.

## Contexts

| Context | Purpose | Public surface | CONTEXT.md |
|---------|---------|----------------|------------|
| **Ordering** | Receives and tracks customer orders | `POST /orders`, `OrderPlaced` | `src/ordering/CONTEXT.md` |
| **Billing** | Generates invoices and processes payments | `InvoiceIssued` | `src/billing/CONTEXT.md` |

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced`; Fulfillment consumes it to start picking.
- **Ordering ↔ Billing**: shared `CustomerId` and `Money` types.
```

Infer which structure applies:

- If `agents-docs/CONTEXT-MAP.md` exists, read it to find the contexts.
- If only one `CONTEXT.md` exists, single context.
- If neither exists, create a `CONTEXT.md` lazily at the top of the relevant subdomain when the first term is resolved.

When several contexts exist, infer which one the current topic belongs to. If unclear, ask. Adding a new subdomain `CONTEXT.md` means adding its row to the map in the same turn.
