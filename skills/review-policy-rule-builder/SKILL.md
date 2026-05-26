---
name: review-policy-rule-builder
description: Creates or updates `agentic-review` policy rules in `<docs-dir>/review/policies/global-policy.md` and `module-<slug>.md` using a structured interview and contract-safe merge behavior. Use when the user asks to add, modify, refine, deprecate, or clarify global or module review policy rules, or mentions rule severity, intent, evidence, automation metadata, or policy IDs like `RP-GLOBAL-###` and `RP-<MODULE>-###`.
---

# Review Policy Rule Builder

Adds a new rule or updates an existing rule in global or module policy files under `<docs-dir>/review/policies/`.

Read [references/policy-rule-checklist.md](references/policy-rule-checklist.md) before editing any policy file.

## Quick start

Example user prompts:
- "Add a new high-severity rule for `<module-slug>` to enforce `<constraint>`."
- "Update rule `RP-<MODULE>-NNN` in `<module-slug>` to refine check logic and exceptions."
- "Add a global policy rule to enforce `<cross-project-constraint>`."
- "Update global rule `RP-GLOBAL-NNN` to tighten evidence expectation."

1. Locate `<docs-dir>/review/policies/global-policy.md` or `module-<slug>.md`.
2. Ask for missing fields: scope, domain/module, intent, severity, check logic, evidence expectation, exceptions, optional automation.
3. Create a new rule ID (`RP-GLOBAL-NNN` or `RP-<MODULE>-NNN`) for add mode, or keep the existing ID for modify mode.
4. Write or merge rule YAML under `## Rules` and update `- Updated: YYYY-MM-DD`.
5. When applicable, update `POLICY_INDEX.md` metadata tables.
6. Validate required schema fields and report result.

## Workflow

1. **Locate target policy file**
   - Resolve `<docs-dir>` from repository contract docs.
   - Ask whether the target is `global` or `module` if not explicit.
   - Route to `global-policy.md` for global scope and `module-<slug>.md` for module scope.
   - If file missing, create it using the appropriate template.

2. **Run AskTheUser interview**
   - Collect:
     - rule scope (`global` or `module`)
     - policy domain/module
     - policy description (title + intent)
     - code sample(s) from repo or user snippet
     - additional metadata (severity, evidence expectation, exceptions, source, ADR, status)
     - for global scope: cross-project impact and why module-local scope is insufficient
    - Offer defaults when user is unsure:
      - `severity: high`
      - `source: user-specified`
      - `status: active`
      - `allowed_exceptions: none`
   - If `automation` is added/changed/removed, ask:
     - "Should I update `POLICY_INDEX.md` -> `Automated Checks` for this rule?"
     - Recommend `Yes` when automation exists or changed.
     - Recommend `Yes` when automation was removed (to remove stale row).
     - Recommend `No` only when user explicitly wants to defer index updates.
   - Explain purpose before asking: `Automated Checks` is the governance index of machine-checkable rules used for review traceability and deterministic enforcement visibility.

3. **Decide operation mode**
    - **Add**: no matching rule ID/intent found.
    - **Modify**: user names rule ID, or intent clearly maps to an existing rule.
    - Preserve stable IDs when intent is unchanged.
    - If intent changes materially, add a new ID and deprecate old rule with rationale.
   - ID family:
     - global: `RP-GLOBAL-NNN`
     - module: `RP-<MODULE>-NNN`

4. **Write contract-compliant rule**
   - Required fields:
     - `id`, `title`, `scope`, `severity`, `intent`, `check_logic`, `evidence_expectation`, `allowed_exceptions`, `source`, `status`
   - Optional fields:
     - `related_adr`
     - `automation` metadata
   - Scope rules:
     - `global-policy.md` must use `scope: global`
     - `module-<slug>.md` must use `scope: module:<slug>`

5. **Update `POLICY_INDEX.md` when applicable**
   - Update only if `<docs-dir>/review/policies/POLICY_INDEX.md` exists.
   - If missing, do not create it in this skill; report warning and remediation.
    - Always update after policy file edits:
      - `- Updated: YYYY-MM-DD`
   - Update `## Needs Decision` when rule status is `needs-decision`.
    - Update `## Automated Checks` only when automation changed and based on AskTheUser decision:
      - `Yes`: upsert/remove row keyed by rule ID.
      - `No`: leave unchanged and report explicit user override.
   - If a global rule is added/deprecated/needs-decision, ensure index reflects it in relevant sections.

6. **Validate and report**
   - Validate against checklist in `references/policy-rule-checklist.md`.
   - If available, run `python skills/review-policy-rule-builder/scripts/validate_policy_rule.py <policy-file>`.
   - Report created/updated rule IDs, file path, and any unresolved ambiguity.

## Guardrails

- Never silently delete existing rules.
- If replacing policy intent, mark prior rule `status: deprecated`.
- Keep edits minimal and localized to target policy file plus `POLICY_INDEX.md` when applicable.
- Keep policy language testable and evidence-oriented.
- If user input conflicts with ADR constraints, mark `status: needs-decision` and note conflict.

## AskTheUser prompt snippet

Use this prompt when `automation` metadata was added, changed, or removed:

"This rule has automation metadata changes. Should I update `POLICY_INDEX.md` -> `Automated Checks` for traceability of machine-enforced rules?"

Options:
- `Yes (Recommended)` - keep index aligned with deterministic checks.
- `No` - keep policy rule change only and defer index update.

Decision handling:
- If `Yes`, upsert or remove `Automated Checks` row by Rule ID.
- If `No`, leave `Automated Checks` unchanged and report user override.
- If `POLICY_INDEX.md` is missing, report warning and skip index update.
