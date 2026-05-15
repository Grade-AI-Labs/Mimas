---
name: find-features
description: Discover feature areas in the current repository that are not yet documented under the agent docs `features/` tree (scaffolded by `setup-agentic-repository` — `agents-docs/features/` by default, or wherever `--docs-dir` put it), then create populated feature docs from the canonical template. Use whenever the user wants to find undocumented features, fill out `features/`, catch up on missing feature documentation, document feature X/Y/Z, or mentions "find features". This is the natural follow-up to `setup-agentic-repository`, which scaffolds the empty `features/` tree this skill populates.
metadata:
  author: Olof Brogeby
  url: https://github.com/brogeby
---

# find-features

Discover feature areas in this repository that are missing from `<docs-dir>/features/`, then create a populated markdown file for each one — following the contract in `<docs-dir>/AGENTS_FEATURES.md` and the template at `<docs-dir>/features/feature-template.md`. The agent docs directory (`<docs-dir>`) is discovered in Phase 1 — it's typically `agents-docs/` but `setup-agentic-repository` may have written it somewhere else.

The Mimas template (`setup-agentic-repository`) scaffolds an empty `<docs-dir>/features/` tree. This skill is the next step — it fills it in.

---

## Phase 1 — Verify prerequisites and locate the docs directory

Confirm the repo has been initialized with the Mimas template, and discover where its agent docs actually live. `setup-agentic-repository` writes the agent doc tree to **`agents-docs/`** by default (a sibling of any human-maintained `docs/`), but `--docs-dir <dir>` can override that (e.g. `docs/agents`). Don't assume the path; discover it.

1. Read `AGENTS.md` at the repo root. Every Mimas-generated `AGENTS.md` lists its docs paths in the first block (`<docs-dir>/AGENT_WORKFLOW.md`, `<docs-dir>/AGENTS_FEATURES.md`, etc.) — the directory in those paths is the docs dir for this repo.
2. If `AGENTS.md` doesn't exist or doesn't reference the contract files, fall back to searching for `AGENTS_FEATURES.md` directly (`find . -maxdepth 3 -name AGENTS_FEATURES.md`). The directory containing it is the docs dir.
3. Confirm the files this skill needs are there:
   - `<docs-dir>/AGENTS_FEATURES.md` — feature documentation contract
   - `<docs-dir>/features/feature-template.md` — the canonical template
   - `<docs-dir>/FEATURES.md` — the feature index

If any of those are missing, tell the user this skill is designed to run after `setup-agentic-repository` and stop. Don't try to scaffold them yourself — that is the other skill's job.

For the rest of this skill, treat the discovered directory as `<docs-dir>` and use it wherever paths appear. Don't hardcode `docs/` or `agents-docs/` in your reasoning, prompts, or report.

Read `<docs-dir>/AGENTS_FEATURES.md` and the root `AGENTS.md` (plus any subdomain `CONTEXT.md` files) so you know:

- what counts as a feature area — a named concept with dedicated logic in the codebase, identified by naming and behavior, not folder structure alone
- the split between area-level docs (`<docs-dir>/features/<area>.md`) and per-service docs (`<docs-dir>/features/<area>/<service>.md`)
- which subdomains exist and where their code lives

These files define the contract you must satisfy. The whole point of the skill is to produce docs that look like a senior engineer on this project wrote them, following the rules already agreed in `AGENTS_FEATURES.md`.

---

## Phase 2 — Inventory what is already documented

List `<docs-dir>/features/` and capture, before asking the user anything:

- Top-level `.md` files (one per documented area) — ignore `feature-template.md`, it is the template
- Subdirectories under `<docs-dir>/features/` (areas with per-service docs)
- The entries listed in `<docs-dir>/FEATURES.md`

You will use this list to filter out features that already have an area doc. Discrepancies between the filesystem and `<docs-dir>/FEATURES.md` are worth flagging in your final report, but don't block on them.

---

## Phase 3 — Ask the user what to discover

Use `AskUserQuestion` to ask how many features (or which ones) to discover. Phrase the question so it accepts a number, "all", or a free-text list of names. The tool always offers an "Other" free-text fallback, so give a few sensible presets and let the user type a specific answer when none fit.

```
questions:
  - question: "How many features would you like to discover, or which ones specifically?"
    header: "Scope"
    multiSelect: false
    options:
      - label: "Top 5 (Recommended)"
        description: "Discover up to 5 of the most significant undocumented feature areas."
      - label: "All"
        description: "Find every undocumented feature area in the codebase."
      - label: "A specific number (1–10)"
        description: "I'll tell you a number from 1 to 10."
      - label: "Specific names"
        description: "I'll list the feature names I want documented (e.g. 'auth, billing, search')."
```

Parse whatever they answer with — accept a bare number, the word "all" (any case), or a comma- or space-separated list. Phrases like "find feature x, y, z" or "auth and billing" should yield `["x", "y", "z"]` and `["auth", "billing"]` respectively. Don't be strict about format; pull out the names.

If the user names features you can't locate in the codebase, surface that and ask whether to skip them or create scaffolded TODO docs for them. Do not silently invent them.

---

## Phase 4 — Discover undocumented feature areas

Scan the codebase for feature areas using the definition from `<docs-dir>/AGENTS_FEATURES.md`. Start from the subdomains declared in the root `AGENTS.md` — if there are several large subdomains, **launch one subagent per subdomain in parallel** so discovery doesn't serialize.

For each candidate feature, capture:

- **Slug** — kebab-case, ideally matching how the area is referenced in code or routes (e.g. `auth`, `billing`, `recruitment-content`)
- **One-sentence concept** — what the feature does, in user-facing terms
- **Where the code lives** — routes, services, handlers, components, modules
- **Significance signal** — at least one of: dedicated service layer, non-trivial handler, dedicated DB tables/migrations, multiple endpoints, real business rules. A single empty route stub is not enough
- **Whether it is already documented** — does `<docs-dir>/features/<slug>.md` exist already?

Then filter:

- Drop anything that already has an area-level doc
- Drop stubs and scaffolding — `<docs-dir>/AGENTS_FEATURES.md` says an entry must have meaningful implementation. Err on the side of leaving thin features out and noting them as "not yet earning an entry"

Rank what is left by significance (surface area, number of endpoints, depth of business logic), then trim to what the user asked for:

- **Number** → take the top N from the ranked list
- **"all"** → take everything that survived the filter
- **Named features** → take only those, matched by slug or close fuzzy match, warning about any that didn't match

---

## Phase 5 — Create the feature docs

For each chosen feature:

1. Read `<docs-dir>/features/feature-template.md` once and use it as the structural template — section order, headings, prompts. Do not invent your own structure.
2. Create `<docs-dir>/features/<slug>.md` populated from the template:
   - Fill in what you can verify from the code: overview, responsibilities, key concepts, API endpoint(s), service/handler/repository paths, key types, tests location, related features
   - Set **`Area:`** to the slug, **`Status:`** to `Active` for production code or `In Progress` for half-built features, and **`Last updated:`** to today's date in `YYYY-MM-DD`
   - For sections you cannot confidently fill (performance characteristics, security review, edge cases nobody has documented), keep the template's prompt and add a clear TODO marker. Leaving an honest gap is better than inventing content
3. If the feature has multiple distinct services or endpoints worth separating, also create `<docs-dir>/features/<slug>/` and seed per-service docs (`<docs-dir>/features/<slug>/<service>.md`) from the same template, then link them from the area doc. Only do this when complexity actually warrants it — the contract says don't duplicate large sections between area and per-service docs

After writing each file, add an entry to `<docs-dir>/FEATURES.md` in alphabetical order, in the form:

```
- [<slug>](./features/<slug>.md) — one-line description
```

If `<docs-dir>/FEATURES.md` still contains the placeholder `_No feature areas documented yet. Add entries as you build out the system._`, remove that line as you add the first real entry.

---

## Phase 6 — Report back

Tell the user:

- Which feature docs were created (full paths)
- Which candidates were considered but rejected, and why ("too thin to earn an entry yet", "matches existing doc <name>", etc.)
- Which sections in the new docs are TODOs that still need human judgment (performance, security, business rules, error scenarios)
- Whether `<docs-dir>/FEATURES.md` was updated, and any discrepancies you noticed between it and the filesystem

Do not commit the changes. The user reviews before committing.

---

## What makes a good output

**Faithful to the code.** Endpoint paths, file locations, method names, table names must match what is actually in the repo. If you cannot find something, leave the template prompt in place with a TODO — do not guess.

**Concept-first for area docs.** The area-level doc explains what the feature is *for* — responsibilities, boundaries, vocabulary. Implementation detail belongs in per-service docs once they exist.

**Honest about gaps.** A clear `TODO: describe rate limiting` is more useful than a fabricated rate limit policy. Future sessions can fill these in from real information.

**Proportionate.** A small CRUD endpoint with one handler does not need every section of the template. Trim or skip sections that genuinely do not apply (no auth, no caching, no migrations, no feature flags). The template is a checklist of what *might* be relevant, not a contract that every section must be populated.

**Honors the contract.** The structure, headings, and rules in `<docs-dir>/AGENTS_FEATURES.md` and `<docs-dir>/features/feature-template.md` win every time. If this skill's instructions ever drift from those files, the files are authoritative — they live with the project and are what other agents read.
