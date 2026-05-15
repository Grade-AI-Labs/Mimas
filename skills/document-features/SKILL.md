---
name: document-features
description: Populate `<docs-dir>/features/<slug>.md` for one, several, or every undocumented feature area by dispatching up to 10 parallel subagents — one per feature. The agent docs directory is discovered from `AGENTS.md` — typically `agents-docs/` (the `setup-agentic-repository` default) but may be elsewhere if `--docs-dir` was used. Use whenever the user wants to document features, fill out feature docs, write up specific features (e.g. "document auth and billing"), document all undocumented features, or follow up on `find-features` discovery. This is the natural sequel to `find-features`: that skill identifies what is missing, this skill writes the docs in parallel.
metadata:
  author: Olof Brogeby
  url: https://github.com/brogeby
---

# document-features

Write feature documentation for the repository — one populated `<docs-dir>/features/<slug>.md` per requested feature — by dispatching subagents in parallel so an "all" run does not serialize. The agent docs directory (`<docs-dir>`) is discovered in Phase 1; it's typically `agents-docs/` but `setup-agentic-repository` may have written it somewhere else.

This skill is the documentation counterpart to `find-features`. `find-features` discovers what is missing; `document-features` is the focused worker that actually fills the template, in parallel, for the features the user names.

If the user asks "find and document everything", you can start with `find-features` to build the candidate list, then hand that list to this skill. If the user already knows which features they want (e.g. "document auth and billing"), come straight here.

---

## Phase 1 — Verify prerequisites and locate the docs directory

Confirm the repo has been initialized with the Mimas template, and discover where its agent docs actually live. `setup-agentic-repository` writes the agent doc tree to **`agents-docs/`** by default (a sibling of any human-maintained `docs/`), but `--docs-dir <dir>` can override that (e.g. `docs/agents`). Don't assume the path; discover it.

1. Read `AGENTS.md` at the repo root. Every Mimas-generated `AGENTS.md` lists its docs paths in the first block (`<docs-dir>/AGENT_WORKFLOW.md`, `<docs-dir>/AGENTS_FEATURES.md`, etc.) — the directory in those paths is the docs dir for this repo.
2. If `AGENTS.md` doesn't exist or doesn't reference the contract files, fall back to searching for `AGENTS_FEATURES.md` directly (`find . -maxdepth 3 -name AGENTS_FEATURES.md`). The directory containing it is the docs dir.
3. Confirm the files this skill needs are there:
   - `<docs-dir>/AGENTS_FEATURES.md` — feature documentation contract
   - `<docs-dir>/features/feature-template.md` — canonical template
   - `<docs-dir>/FEATURES.md` — feature index

If any are missing, tell the user this skill is designed to run after `setup-agentic-repository` and stop. Do not scaffold them yourself.

For the rest of this skill, treat the discovered directory as `<docs-dir>` and use it wherever paths appear. **Critical:** the subagent prompt in Phase 3 is a template — substitute the actual discovered value into it before dispatching each subagent. The subagents do not run this Phase 1 themselves and will not discover the dir on their own.

Read `<docs-dir>/AGENTS_FEATURES.md` and the root `AGENTS.md` (plus any subdomain `CONTEXT.md` files) so you know the contract — what counts as an area-level doc vs. a per-service doc, and which subdomains exist. These files are authoritative; if anything in this skill drifts from them, the files win.

---

## Phase 2 — Decide what to document

The user's request usually contains the answer. Parse what they said:

- **Named features** ("document auth and billing", "write up the search feature") → take that list of slugs
- **A number** ("document 3 features", "write up the top 5") → take a numeric count of the most significant undocumented features
- **"all" / "every" / "everything"** → every undocumented feature with meaningful implementation
- **Ambiguous or empty** → use `AskUserQuestion` with the same options find-features uses (Top 5 / All / Number / Specific names) plus an "Other" free-text fallback

If the user is continuing from a recent `find-features` session, prefer the candidate list that already exists in the conversation over re-asking.

Then quickly inventory `<docs-dir>/features/`:

- Top-level `.md` files (one per documented area, ignoring `feature-template.md`)
- Subdirectories (areas with per-service docs)
- Entries in `<docs-dir>/FEATURES.md`

Filter the requested list against the inventory:

- Drop slugs that already have `<docs-dir>/features/<slug>.md`. Tell the user which ones you skipped and why
- For named features that you cannot locate in the codebase, surface them and ask whether to skip or scaffold a TODO doc. Do not invent feature areas

If the user asked for a number or "all" and you need to identify candidates yourself, scan the subdomains declared in `AGENTS.md` looking for named concepts with dedicated logic — dedicated service layer, non-trivial handler, dedicated tables/migrations, multiple endpoints, real business rules. A single empty route stub is not enough. Rank by significance and trim to the requested count.

---

## Phase 3 — Dispatch one subagent per feature, in parallel

This is the whole point of the skill. Documentation per feature is independent work — one subagent can read the code for `auth` while another reads the code for `billing`. Serializing them throws away the parallelism the harness gives you.

**Cap concurrency at 10 subagents.** If the final list has more than 10 features, dispatch the first batch of 10 in one message, wait for it to complete, then dispatch the next batch. Do not exceed 10 concurrent agents — it overwhelms tooling and the user's review can't keep up.

For each feature in the current batch, spawn one `Agent` call in the **same message** (this is what makes them run in parallel). Use the `general-purpose` subagent unless something more specific fits.

Each subagent gets a self-contained prompt — it has not seen this conversation, so include everything it needs. **Before dispatching, substitute `<docs-dir>` with the value you discovered in Phase 1** (typically `agents-docs`). The subagents do not discover the dir on their own.

```
You are documenting a single feature area for this repository. The output is one populated markdown file at `<docs-dir>/features/<slug>.md` that follows the project's feature documentation contract.

Feature slug: <slug>
One-line concept (from discovery, may be rough): <concept>

Authoritative reading order (read these first, in order):
1. `<docs-dir>/AGENTS_FEATURES.md` — the contract that governs how feature docs are written
2. `<docs-dir>/features/feature-template.md` — the canonical template. Mirror its section order and headings; do not invent your own structure
3. `AGENTS.md` and any subdomain `CONTEXT.md` files — for vocabulary and where the code lives

Your task:
- Locate this feature in the codebase. Confirm it has meaningful implementation (service layer, handler, endpoints, tables, real business rules). If it is only a stub, stop and report that back — do not write a doc for a stub
- Create `<docs-dir>/features/<slug>.md` from the template
- Fill in what you can verify from the code: overview, responsibilities, key concepts, endpoint(s), service/handler/repository paths, key types, tests location, related features
- Set `Area:` to the slug, `Status:` to `Active` for production code or `In Progress` for half-built features, and `Last updated:` to today's date in `YYYY-MM-DD`
- For sections you cannot confidently fill (performance, security review, undocumented edge cases), keep the template's prompt and add a clear `TODO:` marker. Honest gaps beat invented content
- If the feature has multiple distinct services or endpoints worth separating, also create `<docs-dir>/features/<slug>/<service>.md` files from the same template and link them from the area doc — but only when complexity actually warrants it. Do not duplicate large sections between area and per-service docs
- Do not edit `<docs-dir>/FEATURES.md` — the dispatcher will update the index once all features are written, to avoid concurrent edits to the same file
- Do not commit anything

Report back when done with:
- Path(s) of the file(s) you created
- One-line description of the feature (this will be used for the FEATURES.md entry)
- Which template sections you left as TODO
- Anything you noticed that needs human judgment
```

Substitute `<slug>`, `<concept>`, and `<docs-dir>` per feature. Keep the rest verbatim — the subagent depends on having the contract in its own context.

If features turn out to be unrelated to one another (different subdomains, different layers), there's no need to coordinate beyond avoiding the shared `<docs-dir>/FEATURES.md` file. The dispatcher updates the index after the batch returns.

---

## Phase 4 — Update the index and report back

Once a batch completes, collect each subagent's reported one-liner and add entries to `<docs-dir>/FEATURES.md` in alphabetical order, in the form:

```
- [<slug>](./features/<slug>.md) — one-line description
```

If `<docs-dir>/FEATURES.md` still contains the placeholder `_No feature areas documented yet. Add entries as you build out the system._`, remove that line as you add the first real entry.

Then, if more features remain (because the original list was >10), dispatch the next batch of up to 10 and repeat.

When everything is written, tell the user:

- Which feature docs were created (full paths), grouped by batch if there were multiple
- Which requested features were skipped, and why ("already documented at `<docs-dir>/features/<slug>.md`", "could not locate in codebase", "implementation too thin to earn an entry yet")
- Which sections in the new docs are TODOs that still need human judgment
- That `<docs-dir>/FEATURES.md` was updated and how many entries were added
- Any discrepancies you noticed between `<docs-dir>/FEATURES.md` and the filesystem

Do not commit the changes. The user reviews before committing.

---

## Why this is structured around subagents

Documenting one feature is read-heavy and largely independent of documenting another — different files, different services, different endpoints. The slow part is the reading, and parallelizing the reading is the entire reason this skill exists separately from `find-features`. Spawning ten subagents in one message and letting them work concurrently turns a 10-minute sequential run into something closer to a 1–2 minute parallel one, with each subagent producing a focused, faithful doc because its whole context is one feature.

The 10-agent cap is pragmatic, not theoretical: more than that and you risk rate limits, output you can't usefully review at once, and the dispatcher running out of room to track which agent owns which slug. Two batches of ten is fine; ten batches of one is the failure mode this skill is designed to avoid.

---

## What makes a good output

**Faithful to the code.** Endpoint paths, file locations, method names, table names must match what is actually in the repo. If a subagent can't find something, the right move is a `TODO:` marker, not a guess.

**Concept-first for area docs.** The area-level doc explains what the feature is *for* — responsibilities, boundaries, vocabulary. Deep implementation detail belongs in per-service docs once they exist.

**Honest about gaps.** A clear `TODO: describe rate limiting` is more useful than a fabricated rate limit policy. Future sessions can fill these in from real information.

**Proportionate.** A small CRUD endpoint with one handler does not need every section of the template. Trim or skip sections that genuinely do not apply. The template is a checklist of what *might* be relevant, not a contract that every section must be populated.

**Honors the contract.** The structure, headings, and rules in `<docs-dir>/AGENTS_FEATURES.md` and `<docs-dir>/features/feature-template.md` win every time. If this skill's instructions ever drift from those files, the files are authoritative — they live with the project and are what other agents read.
