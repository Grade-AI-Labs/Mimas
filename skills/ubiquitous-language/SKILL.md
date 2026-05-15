---
name: ubiquitous-language
description: Interview the user about the project's domain vocabulary one term at a time, resolving ambiguities and picking canonical terms, then append the resulting glossary into the appropriate `CONTEXT.md` (the bounded-context vocabulary file scaffolded by `setup-agentic-repository`). Use whenever the user wants to define domain terms, harden vocabulary, build a glossary, capture a ubiquitous language, fill in `CONTEXT.md`, or mentions "domain model", "DDD", "bounded context", or "vocabulary".
metadata:
  author: Olof Brogeby
  url: https://github.com/brogeby
---

# ubiquitous-language

Drive a focused interview with the user about the domain vocabulary they use, then write the result into the bounded-context `CONTEXT.md` that `setup-agentic-repository` scaffolded for that subdomain. The output is **not** a standalone `UBIQUITOUS_LANGUAGE.md` — it is appended into the right `CONTEXT.md` so other agent sessions automatically pick it up via the contract in `<docs-dir>/AGENTS_CONTEXT.md` (the docs dir is discovered in Phase 1; typically `agents-docs/` but `--docs-dir` may have put it elsewhere).

The previous version of this skill wrote a sidecar file. That file is invisible to the Mimas instruction tree, so terms captured there never reach the agents reading `CONTEXT.md` at session start. This rewrite fixes that: the glossary lives where the contract says glossaries live.

---

## Phase 1 — Verify prerequisites and locate the docs directory

Confirm the repo has been initialized with the Mimas template, and discover where its agent docs actually live. `setup-agentic-repository` writes the agent doc tree to **`agents-docs/`** by default — kept as a sibling of any human-maintained `docs/` so the two don't collide — but the user can pass `--docs-dir <dir>` (e.g. `docs/agents`) to put it somewhere else. Don't assume the path; discover it.

1. Read `AGENTS.md` at the repo root. Every Mimas-generated `AGENTS.md` lists its docs paths in the very first block (`<docs-dir>/AGENT_WORKFLOW.md`, `<docs-dir>/AGENTS_CONTEXT.md`, etc.). The directory in those paths is the docs dir for this repo.
2. If `AGENTS.md` doesn't exist or doesn't reference the contract files, fall back to searching for `AGENTS_CONTEXT.md` directly (`find . -maxdepth 3 -name AGENTS_CONTEXT.md`). The directory containing it is the docs dir.
3. Confirm the file you actually need is there: `<docs-dir>/AGENTS_CONTEXT.md` — the CONTEXT.md / CONTEXT-MAP.md contract.
4. Confirm at least one `CONTEXT.md` exists somewhere in the tree (root, a subdomain, or both). The CONTEXT.md files live with the code they describe, **not** under the docs dir.

If `AGENTS_CONTEXT.md` cannot be found at all, tell the user this skill is designed to run after `setup-agentic-repository` (which scaffolds both the contract and the `CONTEXT.md` skeletons) and stop. Don't try to create them yourself — that is the other skill's job.

For the rest of this skill, treat the discovered directory as `<docs-dir>` and use it wherever paths appear. Don't hardcode `docs/` or `agents-docs/` in your reasoning, prompts, or report — use the discovered value.

Read `<docs-dir>/AGENTS_CONTEXT.md` end-to-end so the rules in scope here are loaded:

- What `CONTEXT.md` is for (vocabulary, relationships, boundaries/IO, invariants, flagged ambiguities) and what it is **not** for (procedural agent rules, implementation detail)
- Multi-context vs. single-context: single repo = one `CONTEXT.md`; multi-context = one per subdomain, indexed by `<docs-dir>/CONTEXT-MAP.md`
- The append-only discipline: add new entries, don't reshuffle existing ones; supersede rather than rewrite

That contract is authoritative. If anything in this skill ever drifts from it, the contract wins.

---

## Phase 2 — Locate the target CONTEXT.md

You need to know which `CONTEXT.md` to write into before you start interviewing — otherwise the conversation will collect terms that span multiple bounded contexts and you'll have to re-sort them at the end.

1. If `<docs-dir>/CONTEXT-MAP.md` exists, read it. It lists every subdomain that has its own `CONTEXT.md`, with a one-line purpose for each.
2. Otherwise, find the single `CONTEXT.md` (root or top of the single subdomain).

Then decide the target:

- **Conversation already implies a subdomain** (you've been working in `frontend/` for the whole session, or the user is asking about a feature that lives in one subdomain) → propose that one and confirm with the user in the first interview question.
- **Multi-context repo with no obvious subdomain** → use `AskUserQuestion` to let the user pick which `CONTEXT.md` to extend. List each subdomain from `CONTEXT-MAP.md` as an option with its one-line purpose; an "Other" free-text option is always available.
- **Single-context repo** → that one `CONTEXT.md` is the target; mention it to the user but don't ask.

If the user names terms during the interview that clearly belong to a different bounded context, surface that ("**Invoice** sounds like it belongs in the `billing/` context, not `recruitment/`") and ask whether to switch target or capture both. Don't quietly mix contexts in one file — that defeats the point of bounded contexts.

---

## Phase 3 — Read what's already there

Read the target `CONTEXT.md` in full before asking the user anything:

- The existing **Vocabulary** table — every term already defined, with its aliases-to-avoid column
- **Relationships**, **Boundaries / IO**, **Invariants**, **Flagged ambiguities**

You will use this to:

- Skip terms that are already canonical
- Recognize aliases the project has already decided against (don't propose them back as canonical)
- Pick up unresolved entries in **Flagged ambiguities** as the first thing to grill the user about — resolving an existing flag is more valuable than adding a new term

Also do a light pass over the current conversation: any domain nouns/verbs the user has used repeatedly, especially ones with conflicting phrasing, are good seed candidates for the interview.

---

## Phase 4 — Interview the user

The point of the interview is to leave with a small set of **canonical terms with one-sentence definitions and explicit aliases-to-avoid**, plus any relationships, invariants, and unresolved ambiguities the user is willing to commit to. Quality over quantity: five well-defined terms beat fifteen vague ones.

Use `AskUserQuestion` to drive the interview. Ask **one question at a time**, focused on one term or one ambiguity. Each option in the question should be a concrete proposal — never a vague "what do you think" prompt. Always include an "Other" free-text fallback (the tool gives that automatically).

A good question pattern:

```
question: "You've used 'Candidate' and 'Applicant' interchangeably. Which is canonical?"
header: "Term choice"
options:
  - label: "Candidate (Recommended)"
    description: "A person being considered for one or more Roles. 'Applicant' becomes an alias to avoid."
  - label: "Applicant"
    description: "A person who has applied to a Role. 'Candidate' becomes an alias to avoid."
  - label: "They mean different things"
    description: "I'll define each one separately — they aren't synonyms."
```

Order the interview from most to least useful:

1. **Resolve existing flagged ambiguities** in the target `CONTEXT.md`, one at a time. Each resolution moves the term into the Vocabulary table.
2. **Resolve synonyms you observed in the conversation** — same concept, different words. Propose a canonical, with the others as aliases to avoid.
3. **Pin down overloaded terms** — same word, different concepts (e.g. "account" meaning both a customer and a login). Propose two distinct terms.
4. **Capture genuinely new concepts** the user keeps using that aren't in `CONTEXT.md` yet — start with the ones with clearest meaning, leave the hazy ones for last.
5. **Check obvious relationships** the user has implied ("an Order produces one or more Invoices"). One question per relationship is fine; offer a few cardinality choices.
6. **Stop when the user is done.** After 5–8 productive questions, ask if they want to keep going or wrap up. Don't drag the interview past the point where the user is still finding the questions sharp.

Throughout the interview:

- **Be opinionated.** Lead with a "(Recommended)" choice you'd actually defend. Hedging produces a glossary nobody trusts.
- **Define what the term *is*, not what it does.** "A Candidate is a person being considered for one or more Roles" beats "Candidate represents the candidate flow".
- **Surface the consequence of the choice** when it's not obvious. ("If we pick Candidate as canonical, the existing `applicantId` column in the codebase is now an alias-to-avoid — future renames should drop the old name.")
- **Don't invent.** If the user can't articulate what a term means, that goes into **Flagged ambiguities** with the proposed resolution, not into the Vocabulary table.
- **Stay inside the bounded context.** When a term feels like it belongs in another subdomain, route it there rather than appending it to the wrong file.

---

## Phase 5 — Append to CONTEXT.md

Apply the resolutions from the interview to the target `CONTEXT.md`. Respect the append-only discipline from `<docs-dir>/AGENTS_CONTEXT.md`:

- **Vocabulary table:** add rows for each newly canonicalized term. Don't reshuffle existing rows. If a term changes meaning, add a superseding row that explicitly references the old one (e.g. `"replaces earlier definition: ..."`) rather than rewriting history.
- **Relationships:** append new bullets using bold term names and explicit cardinality ("An **Order** produces one or more **Invoices**.")
- **Boundaries / IO:** only update if the interview surfaced something the user is committing to about what this subdomain exposes or consumes. Don't touch this section just because a term was added.
- **Invariants:** append rules the user explicitly committed to ("A **Candidate** cannot exist without at least one **Application**.") — never invent invariants from a definition alone.
- **Flagged ambiguities:** add the things the user couldn't resolve, with a proposed resolution and a clear note about what's blocking the decision. When you resolve an existing flag, **move it** from this section into the Vocabulary table — don't leave a duplicate.

If the target `CONTEXT.md` still contains the original `> **Format reference:**` scaffold and empty placeholder rows (e.g. `| **[Term]** | [One-sentence definition.] | ...`), remove the placeholders as you add the first real entries. Keep the format-reference block — it's documentation for the next agent.

If the interview touched a second bounded context (because the user inevitably named cross-context concepts), apply the same append rules to that context's `CONTEXT.md` too. Note any cross-context relationship in `<docs-dir>/CONTEXT-MAP.md`'s Relationships section if it isn't already captured there.

Do not commit the changes. The user reviews before committing.

---

## Phase 6 — Report back

Tell the user:

- Which `CONTEXT.md` files were modified (full paths)
- For each: the canonical terms added, ambiguities resolved, relationships and invariants captured, and ambiguities left flagged with the proposed resolution
- Any term the user named that belonged in a different bounded context, and where you routed it (or left it for a future session)
- Anything that came up in the interview that doesn't fit in `CONTEXT.md` (e.g. process rules, implementation detail) and where it actually belongs — `/AGENTS.md`, `<docs-dir>/ENGINEERING.md`, or `<docs-dir>/features/`

---

## Re-running in the same conversation

When invoked again later in the same conversation:

1. Re-read the target `CONTEXT.md` — your earlier edits are now part of the canonical state
2. Pick up any flagged ambiguities you couldn't close last time, and any new terms the user has started using since
3. Resume the interview from where it stalled — don't re-ask questions you've already resolved

The append-only discipline means re-running is safe: nothing you wrote earlier gets stomped, and new entries layer on top.

---

## What makes a good output

**The right file.** The vocabulary lives in the `CONTEXT.md` for the bounded context it belongs to. No sidecar files. No mixing contexts in one file.

**Opinionated.** Every term picked as canonical has a clear winner among synonyms. Aliases-to-avoid is populated, not blank.

**Honest about gaps.** Terms the user couldn't define cleanly are in **Flagged ambiguities** with a proposed resolution, not invented into the Vocabulary table.

**Append-only.** Existing rows are not reshuffled. Supersessions are explicit. The diff is readable.

**Honors the contract.** `<docs-dir>/AGENTS_CONTEXT.md` is authoritative on what `CONTEXT.md` is for and how to maintain it. If this skill drifts from that file, the file wins — it's what every other agent reads.
