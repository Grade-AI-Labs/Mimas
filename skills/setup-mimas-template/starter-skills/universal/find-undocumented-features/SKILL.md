---
name: find-undocumented-features
description: Audit the repository for feature areas that lack documentation under docs/features/, present the findings, and hand the chosen ones off to /document-feature. Use whenever the user wants to find undocumented features, audit documentation coverage, check what's missing from docs/features/, or says "find undocumented features", "audit feature docs", or anything that implies surveying doc coverage — even if they don't explicitly name this skill.
metadata:
  author: Olof Brogeby
---

# Find Undocumented Features

Find feature areas in the codebase that do not yet have a `docs/features/<slug>.md` file, then hand the chosen candidates off to `/document-feature` for the actual writing.

This skill does **not** produce documentation itself. It surfaces candidates, lets the user choose which to document, and delegates. Keep this separation — `/document-feature` is where the domain knowledge about templates and section structure lives, and we don't want two skills drifting apart.

## Process

### 1. Ask how many candidates to surface

Use `AskUserQuestion` with the question "How many undocumented features should I surface?" and these options: `1`, `5`, `10`, `All`. The user can also type a custom number via the "Other" field.

Interpret the answer:
- a number N → surface at most N candidates, ranked by how clearly they look like a feature area
- `All` → surface every candidate you find

Do the exploration even if the user picks a small N. It's cheap, and you need the full picture to pick the top N.

### 2. Explore the repo

Read `docs/FEATURES.md` and list `docs/features/` so you know what's already documented. Treat any slug with an existing `docs/features/<slug>.md` as covered.

Then explore broadly for plausible feature areas that aren't covered. Good signals:

- route handlers or controllers that aren't referenced from any existing feature doc
- service modules or domain folders under `src/` without a matching `docs/features/<slug>.md`
- cron jobs, workers, or background tasks
- integrations with external services (APIs, message buses, SDKs)
- CLI entry points or scheduled commands

Compare what you find against `docs/FEATURES.md`. Anything in the code that isn't in the index and lacks a per-area doc is a candidate.

Prefer substantive capabilities. A one-file utility or internal helper is not a feature; a coherent capability exposed to users, other services, or operators is.

### 3. Present the candidates

Build a short list. For each candidate, note:

- **slug** — kebab-case, matching existing `docs/features/` naming conventions
- **one-sentence description** of what the feature does
- **primary file paths** that led you to list it (so `/document-feature` doesn't have to rediscover them)

Show the list to the user as plain text so they can see all candidates at once, then use `AskUserQuestion` to ask "Which of these should I queue up for `/document-feature`?" with three options:

- `Document all` — proceed with every candidate
- `Let me pick` — follow up with a multi-select `AskUserQuestion` listing each candidate; the user checks the ones they want
- `Skip` — end the skill without documenting anything

### 4. Hand off to /document-feature

Act on the user's choice:

- **Skip** — tell the user they can run `/document-feature <slug>` later for any item on the list, and stop. Don't write the candidate list to disk; this is a session artifact.
- **One feature chosen** — invoke `/document-feature` yourself for that feature, passing the slug, description, and file paths as context so it can skip its own discovery step.
- **Multiple features chosen** — spawn one subagent per feature, in parallel, in a single tool-call block. Each subagent should use `/document-feature` for its assigned feature and write the result to `docs/features/<slug>.md`. Brief each subagent with:
  - the slug
  - the one-sentence description
  - the primary file paths
  - the path to `docs/features/feature-template.md`
  - the instruction to update `docs/FEATURES.md` with the new entry when done

Parallel subagents speed this up considerably for larger batches, which is why we prefer them over a sequential loop. The tradeoff is that the user can't review each draft before the next starts — that's acceptable here because `/document-feature` itself includes a review step, and the user can always edit the resulting files afterward.

## Rules

- The candidate list lives only in the conversation. Do not write it to any file.
- Never document a feature yourself inside this skill — always defer to `/document-feature`. If `/document-feature` isn't available in the user's environment, say so and stop rather than improvising.
- If `docs/FEATURES.md` doesn't exist, proceed anyway: the presence of `docs/features/<slug>.md` files is the authoritative signal for what's covered.
- If you find no undocumented feature areas, say so plainly and stop. Don't manufacture candidates to pad the list.
- When ranking candidates for a bounded N, prefer features with higher user-facing impact (exposed routes, external integrations) over internal plumbing.
