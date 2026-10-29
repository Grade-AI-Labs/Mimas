---
name: agentic-review
description: Orchestrate repository-aware code review after `setup-agentic-repository` by deriving module specialists from `GLOSSARY-MAP.md` contexts or the `## Modules` list in `AGENTS.md`, applying `CODING_STANDARDS.md`, generating canonical review artifacts, running deterministic policy automation checks, delegating scoped review tasks to subagents, recording specialist attestations, and returning deduplicated severity-ordered findings with fail-closed completion status. Use when the user wants PR review, local-diff review, orchestrated multi-agent review, module-wise code review, policy-aware convention checks, auditability of reviewer coverage, or asks to invoke `agentic-review` after `/setup-agentic-repository`.
metadata:
  author: Antti Karjalainen
  url: https://github.com/akarjis
---

# agentic-review

Run end-to-end code review using the repository's agentic setup. This skill is the review orchestrator that executes after `/setup-agentic-repository`: it discovers module boundaries from `GLOSSARY-MAP.md` or the `## Modules` list in `AGENTS.md`, applies coding standards from `CODING_STANDARDS.md`, optionally enforces project policy from `<docs-dir>/review/policies/`, runs deterministic policy automation checks (v1 inheritance conventions), builds immutable canonical review artifacts under `<review-dir>` (default `<docs-dir>/review/`), routes work to specialists, records specialist attestations, and consolidates findings into one deduplicated severity-ordered report with an explicit completion state.

Read [references/review-contract.md](references/review-contract.md) before dispatching specialists. It defines severity levels, required finding schema, specialist prompt skeleton, attestation schema, policy-compliance reporting, and deduplication/output rules. [references/agentic-review-flow.md](references/agentic-review-flow.md) shows the phases below as one diagram.

`<skill-dir>` below is this skill's base directory, as Claude Code printed it when it loaded the skill.

---

## Phase 1 — Verify prerequisites and discover `<docs-dir>`

This skill assumes `/dev-workflow:setup-agentic-repository` has already been run.

1. Read root `AGENTS.md`.
2. Discover `<docs-dir>` from the docs paths listed there (typically `docs/agents/`, but `--docs-dir` may have overridden this).
3. Fallback if needed: find `AGENT_WORKFLOW.md` (`find . -maxdepth 4 -name AGENT_WORKFLOW.md`) and set `<docs-dir>` to its parent directory.
4. Confirm these files exist:
   - `AGENTS.md`
   - `<docs-dir>/AGENT_WORKFLOW.md`

If either is missing, stop and tell the user to run `/dev-workflow:setup-agentic-repository` first. Do not scaffold missing setup files from this skill.

Also look for `CODING_STANDARDS.md` at the repo root and `<docs-dir>/ENGINEERING.md`. Proceed without them, but record each missing one in `Testing gaps / unverified areas` and in the standards-compliance section of the report. `GLOSSARY.md`/`GLOSSARY-MAP.md` and ADRs (`docs/adr/`, plus `<context-path>/docs/adr/` in multi-context repos) are created lazily; never require them.

Policy bootstrap mode:
- Optional policy directory: `<docs-dir>/review/policies/`
- If `POLICY_INDEX.md` is present there, policy enforcement is mandatory for this run.
- If policy files are absent, proceed with baseline review and explicitly recommend running `review-policy-builder` in the final report.

Artifact directory (`<review-dir>`):
- Default: `<docs-dir>/review/`, so review history is kept with the repo.
- If the caller names an output directory (for example `/orchestrate-spec`, which reviews an integration branch that must not pick up review files), write every artifact there instead and leave `<docs-dir>/review/` untouched apart from reading policies.

---

## Phase 2 — Resolve review target (PR-first, local fallback)

Stamp the run first: `<run-id>` is `<YYYYMMDD>-<HHMMSS>` in UTC (`date -u +%Y%m%d-%H%M%S`), taken once now and reused for every artifact and temporary path of this run. All other timestamps (`signed_at`, the run timestamp) are UTC ISO-8601.

Default model:
- Prefer PR-style review of branch changes into base branch.
- Fall back to local change review when PR comparison is unavailable or inappropriate.

Resolution order:
1. Parse user overrides from the prompt: an explicit base branch, an explicit head ref (for example the integration branch `/orchestrate-spec` passes), or an explicit local-only request.
2. If explicit local-only was requested, force `local` mode.
3. Resolve the head: the explicit head ref if one was given, otherwise the current branch (`git rev-parse --abbrev-ref HEAD`). Don't check out a different branch in the user's checkout.
4. Build ordered base candidates:
   - user-provided base ref (if any)
   - remote default branch (`git symbolic-ref --quiet --short refs/remotes/origin/HEAD`)
   - `origin/main`
   - `origin/master`
   - `main`
   - `master`
5. Select the first existing candidate (`git rev-parse --verify --quiet <ref>`).
6. If the head is not the base and a base ref exists, use PR-style scope:
   - compare `<base>...<head>` everywhere (`git diff <base>...<head>`, `git diff --name-only <base>...<head>`)
   - when the head is not what's checked out, add a detached worktree of it outside the repo (`git worktree add --detach "$TMPDIR/agentic-review-<run-id>" <head>`) and use it as `<head-checkout>` for reading files and running checks; remove it at the end of Phase 7. Otherwise `<head-checkout>` is the repo root
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

1. If `GLOSSARY-MAP.md` exists at the repo root:
   - parse each entry under `## Contexts`
   - extract the context name and the directory holding its `GLOSSARY.md`
   - create one module specialist per context, owning that directory's subtree
2. Else, if `AGENTS.md` has a `## Modules` section:
   - parse each "`<path>/` — <role>" line
   - create one module specialist per module, owning `<path>/`
3. Else:
   - create one repo-wide module specialist owning the whole tree

Add cross-cut specialists when relevant changes exist:
- `tests-regressions` — test coverage gaps and behavioral regressions
- `migrations-data-safety` — schema/migration/data-risk changes
- `security-authz` — authn/authz/secrets/exposure risk
- `api-contract` — externally visible contract compatibility

Routing rules:
- Route files to module specialists by subtree ownership from the module paths above.
- Route files to cross-cut specialists by pattern and semantics (migrations, auth, API surface, testing changes/gaps).
- Every changed file must be assigned to at least one specialist. Docs-only files that no module owns (`GLOSSARY.md`, `docs/`, `.scratch/`) go to the module specialist whose feature they describe; if none fits, list them in the routing table as `docs-only` — that counts as routed.
- Test files outside every module subtree (a top-level `tests/`, say) go to the module whose code they exercise (by import or name) and to `tests-regressions`.
- Name module specialists `module-<slug>`, where `<slug>` is the module's policy slug (`module-<slug>.md`) or, without policies, the last segment of its path. Cross-cut specialists keep the names above. Use the same slugs for diff files, raw outputs and attestations.
- Multi-match files must be assigned to all matching specialists (broader coverage is preferred to under-routing).

Policy routing additions (when policy exists):
- Read `<docs-dir>/review/policies/POLICY_INDEX.md` to map module/context/subtree -> policy files.
- Load global policy (`global-policy.md`) for all specialists.
- Load module policy (`module-<slug>.md`) for specialists owning that module/subtree.
- If a changed file maps to multiple module policies, attach all relevant policies.
- Build an automated-rule roster from policy rules that include machine metadata (for example `automation.check_type`).
- If `POLICY_INDEX.md` includes a `Review Audit Contract` section, load it and apply its audit-governance fields.
  `required_specialist_categories.module: always` means every module **with changed files** always gets a required specialist; modules the diff doesn't touch get none.
- If no audit contract is present, apply built-in defaults:
  - `audit_contract_version: 1`
  - `completion_mode: fail-closed`
  - required attestation fields from this skill contract
  - required specialist categories: a module specialist for every module with changed files (modules with none get no specialist), cross-cut specialists when routed by file semantics
  - transparency mode: `summary + artifact links`
- Record whether policy-driven audit governance or fallback defaults were used in the plan and final result.

---

## Phase 4 — Create canonical review artifacts and run automated policy checks

Every artifact of the run carries the `<run-id>` stamped in Phase 2 and a `<scope>`: the head branch name (slashes as `-`) or `local`.

Create artifacts under `<review-dir>/`:

- Plan file (execution input source of truth):
  - `review-plan-<run-id>-<scope>.md`
- Diff directory (execution input):
  - `review-plan-<run-id>-<scope>.diffs/`
  - one `.diff` file per specialist/module assignment, plus `changed-files.txt` (one path per line)
- Deterministic policy-check output:
  - `review-plan-<run-id>-<scope>.policy-checks.json`
- Specialist raw-output directory:
  - `review-result-<run-id>-<scope>.specialists/`
  - one artifact per specialist slug (for example `module-orders.md`, `security-authz.md`)
- Human-readable result file:
  - `review-result-<run-id>-<scope>.md`
- Machine-readable manifest file:
  - `review-manifest-<run-id>-<scope>.json`

Retention rule:
- Artifacts are immutable history. Never overwrite any prior review artifact: a second review of the same branch on the same day gets a new `<run-id>`. If a name already exists, take a fresh timestamp.

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
- coverage checklist (all files assigned, all specialists dispatched). Write the plan before dispatch, with every item above but the dispatch box; tick that box when you update the plan after Phase 5

The result file is the canonical human audit output and must contain:
- run metadata (mode, refs, branch, timestamp, run id)
- changed file inventory
- specialist routing matrix (module/diff/file ownership -> specialist)
- specialist attestation ledger (one row per specialist)
- `Findings` (deduplicated, severity ordered)
- `Standards compliance (CODING_STANDARDS.md)`
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
- Name files clearly by specialist slug (for example `module-orders.diff`, `security-authz.diff`).
- Ensure each specialist receives only relevant diff slices plus shared global context as needed.

Automated policy checks (pre-specialist, deterministic): run the checker this skill ships. Never write your own, so two runs over the same diff always agree.

```bash
python3 <skill-dir>/scripts/check_inheritance_suffix.py \
  --policies-dir <docs-dir>/review/policies \
  --repo <head-checkout> \
  --changed-files <review-dir>/review-plan-<run-id>-<scope>.diffs/changed-files.txt \
  --output <review-dir>/review-plan-<run-id>-<scope>.policy-checks.json
```

What it does, so you can read its output:
1. Parses the active rules in `global-policy.md` and `module-*.md`, including nested `automation` metadata, and selects those with `automation.check_type`. V1 supports `inheritance_suffix`; any other check type comes back `unknown`.
2. Validates the metadata: `automation.selector.class_name_suffix` and `automation.expectation.base_class_suffix` are required, and `match_strategy` must be `same-stem-suffix` (default) or `any-base-with-suffix`. Missing or malformed metadata makes the rule `unknown` with the reason; the other rules still run.
3. Builds each rule's target files from `automation.apply_scope` (default `changed-files`; `all-files` is every tracked file), limited for module rules to the subtrees `POLICY_INDEX.md` routes to that module file.
4. Finds classes ending in the selector suffix (Python via `ast`; TypeScript/JavaScript, Java and C# via regex), skips `selector.exclude`, and checks the direct bases: `same-stem-suffix` needs `<Stem><base suffix>` for `<Stem><selector suffix>`; `any-base-with-suffix` needs any base ending in `<base suffix>`.
5. Reports per rule `pass` (no violations), `fail` (each violation with file, line, class, bases and expectation) or `unknown` (malformed metadata, no route for a module rule, or a target it couldn't parse, such as a syntax error or a Kotlin file), with `evaluated`, `skipped_excluded` and `unknown_targets` lists.

Then:
- Record each rule's status in the plan, with the JSON file as its evidence path.
- Convert each `fail` violation into a standard finding that cites the rule id.
- Send each `unknown` to `Testing gaps / unverified areas` with its reason and how to verify it by hand.
- If `python3` is unavailable or the script exits non-zero, mark every automated rule `unknown` with the error as the reason, and say so in the report.

Backward compatibility:
- If no rules include automation metadata, skip deterministic checks and proceed with baseline specialist review.

---

## Phase 5 — Dispatch specialists in parallel

Dispatch specialists in parallel batches of up to 5, each as a `reviewer` agent (`dev-workflow:reviewer` when installed as a plugin): its definition covers specialist work, with this skill's contract taking precedence over its axis rules. If the agent isn't listed, use a general-purpose subagent with the same brief.

For each specialist, provide:
- its scoped diff artifact
- the module's `GLOSSARY.md` (or the root `GLOSSARY.md`) and ADRs touching its subtree, when they exist
- shared `AGENTS.md` and `CODING_STANDARDS.md` (always, when present), plus `<docs-dir>/ENGINEERING.md` as supporting context
- policy files (global + module-specific) when present
- automated policy-check summaries for overlapping files/rules when available
- review contract from `references/review-contract.md`
- output path for raw specialist result artifact under `review-result-*.specialists/`. Specialists may be read-only (the plugin's `reviewer` agent is): they return their output in the reply, and you write it to that path

Specialist requirements (strict):
- Return actionable findings only (exclude style-only commentary unless user requested style review).
- Use required schema for every finding:
  - `severity`
  - `title`
  - `evidence` (file + line)
  - `impact`
  - `recommended_fix`
  - `confidence`
- When a finding is a standards/policy violation, cite the violated rule id/section from `CODING_STANDARDS.md` or policy file.
- Call out verification gaps explicitly when confidence depends on missing tests or runtime validation.

If a specialist finds no actionable issues, it should explicitly return "no actionable findings" plus any testing/verification gaps.

Specialist attestation requirements (strict):
- For every required specialist, dispatched or not, the orchestrator must record an attestation object with the fields below. The specialist supplies only `status` and `attestation_text`; you fill in the rest:
  - `specialist_slug`
  - `specialist_type` (`module` or `cross-cut`)
  - `assigned_scope` (owned module/subtree and reviewed file count)
  - `status` (`findings-submitted` | `no-actionable-findings` | `failed` | `skipped` | `missing`)
  - `signed_at`
  - `attestation_text`
  - `output_artifact_path`
- `attestation_text` fixed statement:
  - `"I reviewed the assigned scope and reported all actionable findings I could verify from the provided artifacts."`
- For missing specialist output, or a required specialist that was never dispatched, still emit an attestation row with status `missing` and an explicit reason.

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
- `Standards compliance (CODING_STANDARDS.md)`
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
- Confirm every specialist output was collected or explicitly marked `failed`, `skipped` or `missing`.
- Confirm every required specialist has an attestation row.
- Confirm policy files were loaded when `POLICY_INDEX.md` is present.
- Confirm automatable policy rules were executed or explicitly marked `unknown` with reason.
- Confirm malformed automation metadata is handled as `unknown` (not a run-stopping parser error).
- Confirm artifact paths in result and manifest are real and consistent with the plan.
- Confirm severity vocabulary is only: `critical`, `high`, `medium`, `low`.
- Confirm `completion_state` is set and fail-closed rules were applied correctly.

Remove the head worktree from Phase 2 if you added one. Do not commit changes. The user reviews artifacts and findings before any commit.
