---
name: review-policy-builder
description: Build and maintain project-specific review policy for `agentic-review` by combining repository docs (`AGENTS.md`, `ENGINEERING.md`, `CONTEXT.md`/`CONTEXT-MAP.md`, ADRs), repository-mined conventions, and structured user input, then writing machine-usable policy files under `<docs-dir>/review/policies/`, including audit-governance metadata consumed by `agentic-review`. Use when the user wants architecture integrity checks (onion/clean/hexagonal), module-specific review rules, dependency-direction policy, naming/inheritance convention enforcement, stricter project/domain review standards, or explicit auditability requirements for specialist review coverage.
metadata:
  author: Antti Karjalainen
  url: https://github.com/akarjis
---

# review-policy-builder

Create and maintain the project-specific review policy consumed by `agentic-review`.

This skill is interview-first and evidence-grounded:
- derive what is already true from repo docs and ADRs
- mine high-confidence implementation conventions from the repository
- capture missing project/domain constraints from the user
- write structured policy artifacts in `<docs-dir>/review/policies/`
- define review audit governance in `POLICY_INDEX.md` for specialist attestation and completion rules

Read [references/policy-contract.md](references/policy-contract.md) before writing policy files. It is the canonical schema and includes onion/clean-architecture templates.

---

## Phase 1 — Verify prerequisites and locate `<docs-dir>`

This skill runs after `setup-agentic-repository`.

1. Read root `AGENTS.md`.
2. Discover `<docs-dir>` from `AGENTS.md` contract paths.
3. Fallback: find `AGENTS_CONTEXT.md` and use its parent directory as `<docs-dir>`.
4. Confirm required files:
   - `AGENTS.md`
   - `<docs-dir>/ENGINEERING.md`
   - `<docs-dir>/AGENTS_CONTEXT.md`
   - at least one `CONTEXT.md`
5. Optional but strongly preferred:
   - `<docs-dir>/CONTEXT-MAP.md`
   - `<docs-dir>/adr/*.md`

If required files are missing, fail fast with actionable remediation: run/fix `setup-agentic-repository` first.

---

## Phase 2 — Load baseline truth before asking questions

Read these sources first, then summarize extracted constraints:

1. `AGENTS.md` for global workflow and non-negotiables
2. `<docs-dir>/ENGINEERING.md` for coding/testing/quality standards
3. `<docs-dir>/CONTEXT-MAP.md` (if present) and relevant `CONTEXT.md` files for module boundaries, public surfaces, invariants, and dependency direction hints
4. `<docs-dir>/adr/*.md` for architecture decisions and constraints

Extract candidate rules from those files into a working list tagged `source: derived` or `source: adr`.

Do not ask the user to restate anything already explicit in these files.

---

## Phase 3 — Mine repository convention candidates (inheritance v1)

Before interviewing, mine code-level conventions that can become automatable review checks.

Scope (v1):
- inheritance conventions only (`check_type: inheritance_suffix`)

Mining workflow:
1. Scan repository code (prioritize module-owned subtrees from `CONTEXT-MAP.md`/`CONTEXT.md`) for class declarations and inheritance/base-type relationships.
2. Detect suffix-based inheritance candidates (for example `*Controller` extending `*MainController`, `*Service` extending `*MainService`).
3. Build candidate evidence:
   - class suffix
   - expected base suffix
   - sample count
   - adoption ratio (`matching_samples / total_samples`)
   - representative file+line evidence for matching and violating samples
4. Candidate promotion defaults:
   - `min_samples = 4`
   - `min_adoption_ratio = 0.85`
5. Classify candidates:
   - `promoted-candidate`: meets both thresholds
   - `exploratory-candidate`: below threshold (show to user only when useful)

Scoping defaults:
- module-first by subtree ownership
- if the same candidate is confirmed across multiple modules, promote to a global rule

Never persist mined conventions automatically. They must be explicitly confirmed in the interview.

---

## Phase 4 — Structured interview for missing policy

Run a focused interview to capture project-specific review checks not present in baseline docs. Use `AskUserQuestion` and resolve one decision at a time.

Target gaps:
- architecture integrity rules (onion/clean/hexagonal)
- allowed dependency direction and forbidden layer crossings
- call-flow restrictions (for example controller -> application -> domain -> infrastructure)
- inherited code conventions discovered in Phase 3 (candidate confirmation, severity, exceptions)
- module exceptions (allowed boundary breaks and justification)
- transaction/data integrity rules
- security/business-risk hotspots that deserve stricter scrutiny

Rules for the interview:
- propose concrete options with recommended defaults
- for each promoted convention candidate, request explicit confirm/reject
- when confirmed, capture severity and explicit allowed exceptions
- capture explicit exceptions and evidence requirements
- resolve ambiguities immediately; do not leave vague prose
- when user input conflicts with ADRs, mark conflict as `needs decision` in output artifacts

---

## Phase 5 — Write policy artifacts under `<docs-dir>/review/policies/`

Produce this contract:

1. `global-policy.md` — cross-project rules and global constraints
2. `module-<slug>.md` — one per module/context
   - multi-context: derive `<slug>` from context rows in `CONTEXT-MAP.md`
   - single-context: write one module file for the single context
3. `POLICY_INDEX.md` — index and routing map:
   - module/context -> policy file
   - primary subtree ownership
   - policy version/updated metadata
   - review audit contract for `agentic-review`

Use the schema from `references/policy-contract.md`. Each rule must include required metadata fields:
- `id`
- `title`
- `scope` (`global` or `module:<slug>`)
- `severity` (`critical|high|medium|low`)
- `intent`
- `check_logic`
- `evidence_expectation`
- `allowed_exceptions`
- `source` (`derived|user-specified|adr`)
- `related_adr` (optional)

Automation metadata (optional, recommended for deterministic checks):
- Add machine-usable `automation` metadata for confirmed inheritance conventions.
- For inheritance checks, set:
  - `check_type: inheritance_suffix`
  - `apply_scope: changed-files` (default)
  - selector and expectation fields defined by the policy contract

Convention rule scoping:
- default to module policy files (`module-<slug>.md`)
- promote to `global-policy.md` only when the same convention is confirmed across modules
- keep module-specific exceptions local unless explicitly approved as global

`POLICY_INDEX.md` must include `Review Audit Contract` with:
- `audit_contract_version`
- `completion_mode: fail-closed`
- required attestation fields:
  - `specialist_slug`
  - `specialist_type`
  - `assigned_scope`
  - `status`
  - `signed_at`
  - `attestation_text`
  - `output_artifact_path`
- required specialist categories:
  - module specialists always required
  - cross-cut specialists required when routed by file semantics
- transparency mode:
  - `summary + artifact links`

---

## Phase 6 — Update/merge behavior on reruns

If policy files already exist:
- merge/update in place; do not overwrite blindly
- preserve stable `id` values for unchanged rules
- update metadata and content for modified rules
- mark obsolete rules as deprecated; do not silently delete history
- keep `POLICY_INDEX.md` synchronized with current module list

Conflict handling:
- if a new/updated rule contradicts ADR constraints, mark it as `needs decision` and document the conflict in both impacted policy file and `POLICY_INDEX.md`

---

## Phase 7 — Integration contract for `agentic-review`

This skill must produce artifacts that `agentic-review` can consume deterministically:

- policy location: `<docs-dir>/review/policies/`
- expected files:
  - `POLICY_INDEX.md`
  - `global-policy.md`
  - `module-<slug>.md`
- each rule has machine-usable metadata fields (no prose-only rules)
- inheritance convention rules that should run automatically include `automation.check_type: inheritance_suffix`
- `POLICY_INDEX.md` includes a machine-readable `Review Audit Contract` section

Document in `POLICY_INDEX.md`:
- which modules have policy coverage
- which rules are global vs module-scoped
- which rules are automatable (`check_type`, scope, and owning policy file)
- review audit contract values (`audit_contract_version`, `completion_mode`, required attestation fields, required specialist categories, transparency mode)
- any `needs decision` conflicts unresolved at authoring time

---

## Phase 8 — Report back

Tell the user:
- which files were created/updated
- which rules were derived vs user-specified
- which mined convention candidates were confirmed, rejected, or deferred
- which review audit contract values were set in `POLICY_INDEX.md`
- unresolved `needs decision` conflicts
- which modules still need policy refinement
- artifact hygiene outcome (what `.gitignore` entries were added, or that no changes were applied)

At the end of **every run**, add an artifact-hygiene decision step before finishing:

1. Explain that `agentic-review` produces multiple generated artifacts under `<docs-dir>/review/`:
   - `review-plan-*.md` (plan)
   - `review-plan-*.diffs/` (full scoped diffs)
   - `review-result-*.specialists/` (raw specialist outputs)
   - `review-result-*.md` (human-readable summary)
   - `review-manifest-*.json` (machine-readable manifest)
2. Explain the tradeoff explicitly:
   - keeping these files tracked preserves review/audit history
   - ignoring some or all reduces repository noise
3. Ask the user to choose one ignore strategy with `AskUserQuestion`:

```yaml
questions:
  - question: "Would you like me to update `.gitignore` for generated `agentic-review` artifacts?"
    header: "Review Artifacts"
    multiSelect: false
    options:
      - label: "Ignore all review artifacts (Recommended)"
        description: "Add ignore patterns for plans, diff directories, specialist outputs, result summaries, and manifests."
      - label: "Ignore diff files only"
        description: "Ignore only `review-plan-*.diffs/` directories and keep other review artifacts tracked."
      - label: "Keep review artifacts tracked"
        description: "Do not modify `.gitignore`."
```

Apply deterministic mapping to root `.gitignore`:
- `Ignore all review artifacts (Recommended)`:
  - `<docs-dir>/review/review-plan-*.md`
  - `<docs-dir>/review/review-plan-*.diffs/`
  - `<docs-dir>/review/review-result-*.specialists/`
  - `<docs-dir>/review/review-result-*.md`
  - `<docs-dir>/review/review-manifest-*.json`
- `Ignore diff files only`:
  - `<docs-dir>/review/review-plan-*.diffs/`
- `Keep review artifacts tracked`:
  - no `.gitignore` changes

Idempotency requirements:
- never add duplicate `.gitignore` lines
- preserve existing `.gitignore` content order except for appended new lines when needed
- if all required lines already exist for the chosen option, report `no-op` instead of rewriting

Do not commit changes. The user reviews policy artifacts first.
