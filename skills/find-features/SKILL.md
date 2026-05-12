---
name: find-features
description: Discover feature areas in the current repository that are not yet documented under `docs/features/`, then create populated feature docs from the canonical template. Use whenever the user wants to find undocumented features, fill out `docs/features/`, catch up on missing feature documentation, document feature X/Y/Z, or mentions "find features". This is the natural follow-up to `setup-mimas-template`, which scaffolds the empty `docs/features/` tree this skill populates.
metadata:
  author: Olof Brogeby
  url: https://github.com/brogeby
---

# find-features

Discover feature areas in this repository that are missing from `docs/features/`, then create a populated markdown file for each one — following the contract in `docs/AGENTS_FEATURES.md` and the template at `docs/features/feature-template.md`.

The Mimas template (`setup-mimas-template`) scaffolds an empty `docs/features/` tree. This skill is the next step — it fills it in.

---

## Phase 1 — Verify prerequisites

Confirm the repo has been initialized with the Mimas template. Check for:

- `docs/AGENTS_FEATURES.md` — feature documentation contract
- `docs/features/feature-template.md` — the canonical template
- `docs/FEATURES.md` — the feature index

If any of those are missing, tell the user this skill is designed to run after `setup-mimas-template` and stop. Don't try to scaffold them yourself — that is the other skill's job.

Read `docs/AGENTS_FEATURES.md` and the root `AGENTS.md` (plus any subdomain `AGENTS.md` files) so you know:

- what counts as a feature area — a named concept with dedicated logic in the codebase, identified by naming and behavior, not folder structure alone
- the split between area-level docs (`docs/features/<area>.md`) and per-service docs (`docs/features/<area>/<service>.md`)
- which subdomains exist and where their code lives

These files define the contract you must satisfy. The whole point of the skill is to produce docs that look like a senior engineer on this project wrote them, following the rules already agreed in `AGENTS_FEATURES.md`.

---

## Phase 2 — Inventory what is already documented

List `docs/features/` and capture, before asking the user anything:

- Top-level `.md` files (one per documented area) — ignore `feature-template.md`, it is the template
- Subdirectories under `docs/features/` (areas with per-service docs)
- The entries listed in `docs/FEATURES.md`

You will use this list to filter out features that already have an area doc. Discrepancies between the filesystem and `docs/FEATURES.md` are worth flagging in your final report, but don't block on them.

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

Scan the codebase for feature areas using the definition from `docs/AGENTS_FEATURES.md`. Start from the subdomains declared in the root `AGENTS.md` — if there are several large subdomains, **launch one subagent per subdomain in parallel** so discovery doesn't serialize.

For each candidate feature, capture:

- **Slug** — kebab-case, ideally matching how the area is referenced in code or routes (e.g. `auth`, `billing`, `recruitment-content`)
- **One-sentence concept** — what the feature does, in user-facing terms
- **Where the code lives** — routes, services, handlers, components, modules
- **Significance signal** — at least one of: dedicated service layer, non-trivial handler, dedicated DB tables/migrations, multiple endpoints, real business rules. A single empty route stub is not enough
- **Whether it is already documented** — does `docs/features/<slug>.md` exist already?

Then filter:

- Drop anything that already has an area-level doc
- Drop stubs and scaffolding — `docs/AGENTS_FEATURES.md` says an entry must have meaningful implementation. Err on the side of leaving thin features out and noting them as "not yet earning an entry"

Rank what is left by significance (surface area, number of endpoints, depth of business logic), then trim to what the user asked for:

- **Number** → take the top N from the ranked list
- **"all"** → take everything that survived the filter
- **Named features** → take only those, matched by slug or close fuzzy match, warning about any that didn't match

---

## Phase 5 — Create the feature docs

For each chosen feature:

1. Read `docs/features/feature-template.md` once and use it as the structural template — section order, headings, prompts. Do not invent your own structure.
2. Create `docs/features/<slug>.md` populated from the template:
   - Fill in what you can verify from the code: overview, responsibilities, key concepts, API endpoint(s), service/handler/repository paths, key types, tests location, related features
   - Set **`Area:`** to the slug, **`Status:`** to `Active` for production code or `In Progress` for half-built features, and **`Last updated:`** to today's date in `YYYY-MM-DD`
   - For sections you cannot confidently fill (performance characteristics, security review, edge cases nobody has documented), keep the template's prompt and add a clear TODO marker. Leaving an honest gap is better than inventing content
3. If the feature has multiple distinct services or endpoints worth separating, also create `docs/features/<slug>/` and seed per-service docs (`docs/features/<slug>/<service>.md`) from the same template, then link them from the area doc. Only do this when complexity actually warrants it — the contract says don't duplicate large sections between area and per-service docs

After writing each file, add an entry to `docs/FEATURES.md` in alphabetical order, in the form:

```
- [<slug>](./features/<slug>.md) — one-line description
```

If `docs/FEATURES.md` still contains the placeholder `_No feature areas documented yet. Add entries as you build out the system._`, remove that line as you add the first real entry.

---

## Phase 6 — Report back

Tell the user:

- Which feature docs were created (full paths)
- Which candidates were considered but rejected, and why ("too thin to earn an entry yet", "matches existing doc <name>", etc.)
- Which sections in the new docs are TODOs that still need human judgment (performance, security, business rules, error scenarios)
- Whether `docs/FEATURES.md` was updated, and any discrepancies you noticed between it and the filesystem

Do not commit the changes. The user reviews before committing.

---

## What makes a good output

**Faithful to the code.** Endpoint paths, file locations, method names, table names must match what is actually in the repo. If you cannot find something, leave the template prompt in place with a TODO — do not guess.

**Concept-first for area docs.** The area-level doc explains what the feature is *for* — responsibilities, boundaries, vocabulary. Implementation detail belongs in per-service docs once they exist.

**Honest about gaps.** A clear `TODO: describe rate limiting` is more useful than a fabricated rate limit policy. Future sessions can fill these in from real information.

**Proportionate.** A small CRUD endpoint with one handler does not need every section of the template. Trim or skip sections that genuinely do not apply (no auth, no caching, no migrations, no feature flags). The template is a checklist of what *might* be relevant, not a contract that every section must be populated.

**Honors the contract.** The structure, headings, and rules in `docs/AGENTS_FEATURES.md` and `docs/features/feature-template.md` win every time. If this skill's instructions ever drift from those files, the files are authoritative — they live with the project and are what other agents read.
