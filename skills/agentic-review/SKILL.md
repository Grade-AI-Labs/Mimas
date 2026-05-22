---
name: agentic-review
description: Orchestrate repository-aware code review after `setup-agentic-repository` by deriving module specialists from `AGENTS.md` + `CONTEXT.md`/`CONTEXT-MAP.md`, generating canonical review artifacts, running deterministic policy automation checks, delegating scoped review tasks to subagents, recording specialist attestations, and returning deduplicated severity-ordered findings with fail-closed completion status. Use when the user wants PR review, local-diff review, orchestrated multi-agent review, module-wise code review, policy-aware convention checks, auditability of reviewer coverage, or asks to invoke `agentic-review` with agentic repository setup.
metadata:
  author: Antti Karjalainen
  url: https://github.com/akarjis
---

# agentic-review

Run end-to-end code review using the repository's agentic setup. This skill is the review orchestrator that executes after `setup-agentic-repository`: it discovers module boundaries from `CONTEXT.md` artifacts, applies coding standards from `ENGINEERING.md`, optionally enforces project policy from `<docs-dir>/review/policies/`, runs deterministic policy automation checks (v1 inheritance conventions), builds immutable canonical review artifacts under `<docs-dir>/review/`, routes work to specialists, records specialist attestations, and consolidates findings into one deduplicated severity-ordered report with an explicit completion state.

Read [references/review-contract.md](references/review-contract.md) before dispatching specialists. It defines severity levels, required finding schema, specialist prompt skeleton, attestation schema, policy-compliance reporting, and deduplication/output rules.

---

## Phase 1 — Verify prerequisites and discover `<docs-dir>`

This skill assumes `setup-agentic-repository` has already been run.

1. Read root `AGENTS.md`.
2. Discover `<docs-dir>` from the contract paths listed there (typically `agents-docs/`, but `--docs-dir` may have overridden this).
3. Fallback if needed: find `AGENTS_CONTEXT.md` (`find . -maxdepth 4 -name AGENTS_CONTEXT.md`) and set `<docs-dir>` to its parent directory.
4. Confirm these files exist:
   - `<docs-dir>/AGENTS_CONTEXT.md`
   - `<docs-dir>/AGENT_WORKFLOW.md`
   - `<docs-dir>/ENGINEERING.md`
   - at least one `CONTEXT.md` in the repo

If any are missing, stop and tell the user to run `setup-agentic-repository` first. Do not scaffold missing setup files from this skill.

Policy bootstrap mode:
- Optional policy directory: `<docs-dir>/review/policies/`
- If `POLICY_INDEX.md` is present there, policy enforcement is mandatory for this run.
- If policy files are absent, proceed with baseline review and explicitly recommend running `review-policy-builder` in the final report.

---

## Phase 2 — Resolve review target (PR-first, local fallback)

Default model:
- Prefer PR-style review of branch changes into base branch.
- Fall back to local change review when PR comparison is unavailable or inappropriate.

Resolution order:
1. Parse user overrides from the prompt (explicit base branch or explicit local-only request).
2. If explicit local-only was requested, force `local` mode.
3. Detect current branch (`git rev-parse --abbrev-ref HEAD`).
4. Build ordered base candidates:
   - user-provided base ref (if any)
   - remote default branch (`git symbolic-ref --quiet --short refs/remotes/origin/HEAD`)
   - `origin/main`
   - `origin/master`
   - `main`
   - `master`
5. Select the first existing candidate (`git rev-parse --verify --quiet <ref>`).
6. If current branch is not base and a base ref exists, use PR-style scope:
   - compare `base...HEAD`
7. Otherwise use local scope:
   - unstaged diff (`git diff`)
   - staged diff (`git diff --cached`)
   - untracked files (`git ls-files --others --exclude-standard`)

Capture the resolved scope in the canonical plan before launching specialists:
- review mode (`pr` or `local`)
- base/head refs (or `local`)
- exact changed-file inventory
- any gaps (for example, no remote base available)

---

## Phase 3 — Build module map and specialist roster

Derive module specialists from setup artifacts:

1. If `<docs-dir>/CONTEXT-MAP.md` exists:
   - parse each context row
   - extract context name and `CONTEXT.md` path
   - create one module specialist per context
2. If no context map exists:
   - use the single discovered `CONTEXT.md`
   - create one module specialist for that subtree

Add cross-cut specialists when relevant changes exist:
- `tests-regressions` — test coverage gaps and behavioral regressions
- `migrations-data-safety` — schema/migration/data-risk changes
- `security-authz` — authn/authz/secrets/exposure risk
- `api-contract` — externally visible contract compatibility

Routing rules:
- Route files to module specialists by subtree ownership from `CONTEXT.md` paths.
- Route files to cross-cut specialists by pattern and semantics (migrations, auth, API surface, testing changes/gaps).
- Every changed file must be assigned to at least one specialist.
- Multi-match files must be assigned to all matching specialists (broader coverage is preferred to under-routing).

Policy routing additions (when policy exists):
- Read `<docs-dir>/review/policies/POLICY_INDEX.md` to map module/context/subtree -> policy files.
- Load global policy (`global-policy.md`) for all specialists.
- Load module policy (`module-<slug>.md`) for specialists owning that module/subtree.
- If a changed file maps to multiple module policies, attach all relevant policies.
- Build an automated-rule roster from policy rules that include machine metadata (for example `automation.check_type`).
- If `POLICY_INDEX.md` includes a `Review Audit Contract` section, load it and apply its audit-governance fields.
- If no audit contract is present, apply built-in defaults:
  - `audit_contract_version: 1`
  - `completion_mode: fail-closed`
  - required attestation fields from this skill contract
  - required specialist categories: module specialists always, cross-cut specialists when routed by file semantics
  - transparency mode: `summary + artifact links`
- Record whether policy-driven audit governance or fallback defaults were used in the plan and final result.

---

## Phase 4 — Create canonical review artifacts and run automated policy checks

Create artifacts under `<docs-dir>/review/`:

- Plan file (execution input source of truth):
  - `review-plan-<YYYYMMDD>-<branch-or-local>.md`
- Diff directory (execution input):
  - `review-plan-<YYYYMMDD>-<branch-or-local>.diffs/`
  - one `.diff` file per specialist/module assignment
- Specialist raw-output directory:
  - `review-result-<YYYYMMDD>-<HHMMSS>-<scope>.specialists/`
  - one artifact per specialist slug (for example `backend-api.md`, `security-authz.md`)
- Human-readable result file:
  - `review-result-<YYYYMMDD>-<HHMMSS>-<scope>.md`
- Machine-readable manifest file:
  - `review-manifest-<YYYYMMDD>-<HHMMSS>-<scope>.json`

Retention rule:
- Artifacts are immutable history. Never overwrite prior `review-result-*` or `review-manifest-*` files.

The plan file is the canonical execution source of truth and must contain:
- target summary (mode, base/head refs, branch)
- changed file inventory
- specialist roster
- routing table (file -> specialist(s))
- policy routing table (specialist -> policy files)
- audit-governance mode (`policy-contract` or `fallback-defaults`) and active settings
- automated policy-check roster (rule id, scope, check type, severity, apply scope)
- automated policy-check results (`pass|fail|unknown`) with evidence paths
- artifact paths
- coverage checklist (all files assigned, all specialists dispatched)

The result file is the canonical human audit output and must contain:
- run metadata (mode, refs, branch, timestamp, run id)
- changed file inventory
- specialist routing matrix (module/diff/file ownership -> specialist)
- specialist attestation ledger (one row per specialist)
- `Findings` (deduplicated, severity ordered)
- `Standards compliance (ENGINEERING.md)`
- `Project policy compliance`
- `Testing gaps / unverified areas`
- `Coverage + completion status`
- `Artifacts` (plan, diffs, specialist raw outputs, manifest)

The manifest file is the machine-audit output and must include top-level fields:
- `run_id`
- `target` metadata (mode, base/head refs, branch, timestamp)
- `changed_files`
- `specialist_roster`
- `routing_map`
- `attestations`
- `compliance_results` (standards + policy + deterministic checks)
- `completion_state`
- `completion_blockers`

Diff artifact rules:
- Keep full diffs in the `.diffs/` directory, not in the summary.
- Name files clearly by specialist slug (for example `backend-api.diff`, `security-authz.diff`).
- Ensure each specialist receives only relevant diff slices plus shared global context as needed.

Automated policy checks (pre-specialist, deterministic):
1. Parse active policy rules from global/module files.
2. Select rules with `automation.check_type` metadata. V1 required support:
   - `inheritance_suffix`
3. Validate automation metadata before evaluation:
   - parser must handle nested/indented keys in YAML blocks (for example, if using regex extraction, support leading whitespace)
   - required fields for `inheritance_suffix`:
     - `automation.selector.class_name_suffix`
     - `automation.expectation.base_class_suffix`
   - if required metadata is missing or malformed, do not fail the run:
     - mark the rule `unknown`
     - include reason/evidence (`malformed automation metadata`)
     - continue processing remaining rules
4. Build target file set:
   - default from `automation.apply_scope = changed-files`
   - module scoping based on policy routing ownership
5. Evaluate each targeted file for each applicable rule:
   - find classes matching `automation.selector.class_name_suffix`
   - verify base class pattern against `automation.expectation` (for v1, `same-stem-suffix`)
6. Record compliance status per rule:
   - `pass`: no violations found in targeted files
   - `fail`: at least one violation with concrete file+line evidence
   - `unknown`: parse/analysis could not determine compliance for one or more targets
7. Convert `fail` results into standard findings with policy rule reference.
8. Send `unknown` results to `Testing gaps / unverified areas` with concrete validation steps.

Backward compatibility:
- If no rules include automation metadata, skip deterministic checks and proceed with baseline specialist review.

---

## Phase 5 — Dispatch specialists in parallel

Dispatch specialists in parallel batches of up to 5.

For each specialist, provide:
- its scoped diff artifact
- relevant `CONTEXT.md`
- shared `AGENTS.md` and `<docs-dir>/ENGINEERING.md` (always)
- policy files (global + module-specific) when present
- automated policy-check summaries for overlapping files/rules when available
- review contract from `references/review-contract.md`
- output path for raw specialist result artifact under `review-result-*.specialists/`

Specialist requirements (strict):
- Return actionable findings only (exclude style-only commentary unless user requested style review).
- Use required schema for every finding:
  - `severity`
  - `title`
  - `evidence` (file + line)
  - `impact`
  - `recommended_fix`
  - `confidence`
- When a finding is a standards/policy violation, cite the violated rule id/section from `ENGINEERING.md` or policy file.
- Call out verification gaps explicitly when confidence depends on missing tests or runtime validation.

If a specialist finds no actionable issues, it should explicitly return "no actionable findings" plus any testing/verification gaps.

Specialist attestation requirements (strict):
- For every dispatched specialist, the orchestrator must record an attestation object with:
  - `specialist_slug`
  - `specialist_type` (`module` or `cross-cut`)
  - `assigned_scope` (owned module/subtree and reviewed file count)
  - `status` (`findings-submitted` | `no-actionable-findings` | `failed` | `skipped` | `missing`)
  - `signed_at`
  - `attestation_text`
  - `output_artifact_path`
- `attestation_text` fixed statement:
  - `"I reviewed the assigned scope and reported all actionable findings I could verify from the provided artifacts."`
- For missing specialist output, still emit an attestation row with status `missing` and an explicit reason.

---

## Phase 6 — Consolidate, deduplicate, and finalize completion state

Merge specialist outputs plus deterministic policy-check findings into one consolidated result:

1. Group duplicate findings by root cause.
2. Preserve the strongest instance:
   - highest severity
   - clearest evidence
   - most actionable fix
3. Keep cross-specialist corroboration notes when useful, but do not duplicate findings.
4. Sort final findings by severity, then impact.

Fail-closed completion rules:
- Compute `completion_state` from required specialist attestations:
  - `complete`: every required specialist has status `findings-submitted` or `no-actionable-findings`
  - `incomplete`: any required specialist has status `failed`, `skipped`, or `missing`
- `completion_mode` is always fail-closed.
- Generate explicit `completion_blockers` for all non-success required attestations.

Result/report sections (required):
- `Run metadata`
- `Changed file inventory`
- `Specialist routing matrix`
- `Specialist attestation ledger`
- `Findings` (deduplicated, severity ordered)
- `Standards compliance (ENGINEERING.md)`
- `Project policy compliance`:
  - when policy files exist: include each evaluated rule id with `pass|fail|unknown`, supporting evidence, and exception usage
  - when policy files are absent: include bootstrap recommendation
  - always include whether audit governance came from policy contract or fallback defaults
- `Testing gaps / unverified areas`
- `Coverage + completion status`:
  - route completeness
  - attestation completeness
  - `completion_state`
  - `completion_blockers` when incomplete
- `Artifacts`:
  - plan path
  - diff directory path
  - specialist raw output directory path
  - manifest path

If no actionable findings exist, say so explicitly and still provide attestation coverage, completion status, and verification gaps.

---

## Phase 7 — Output quality checks

Before completing:
- Confirm every changed file appears in the routing table.
- Confirm every specialist output was collected or explicitly marked failed/skipped.
- Confirm every required specialist has an attestation row.
- Confirm policy files were loaded when `POLICY_INDEX.md` is present.
- Confirm automatable policy rules were executed or explicitly marked `unknown` with reason.
- Confirm malformed automation metadata is handled as `unknown` (not a run-stopping parser error).
- Confirm artifact paths in result and manifest are real and consistent with the plan.
- Confirm severity vocabulary is only: `critical`, `high`, `medium`, `low`.
- Confirm `completion_state` is set and fail-closed rules were applied correctly.

Do not commit changes. The user reviews artifacts and findings before any commit.
