---
name: review-policy-rule-builder
description: Creates or updates single `agentic-review` policy rules in `<docs-dir>/review/policies/module-<slug>.md` using a structured interview and contract-safe merge behavior. Use when the user asks to add, modify, refine, deprecate, or clarify a review policy rule, or mentions rule severity, intent, evidence, automation metadata, or policy IDs like `RP-<MODULE>-NNN`.
---

# Review Policy Rule Builder

Adds a new rule or updates an existing rule in module policy files under `<docs-dir>/review/policies/`.

Read [references/policy-rule-checklist.md](references/policy-rule-checklist.md) before editing any policy file.

## Quick start

Example user prompts:
- "Add a new high-severity rule for `<module-slug>` to enforce `<constraint>`."
- "Update rule `RP-<MODULE>-NNN` in `<module-slug>` to refine check logic and exceptions."

1. Locate `<docs-dir>/review/policies/module-<slug>.md`.
2. Ask for missing fields: domain/module, intent, severity, check logic, evidence expectation, exceptions, optional automation.
3. Create a new rule ID (`RP-<MODULE>-NNN`) for add mode, or keep the existing ID for modify mode.
4. Write or merge rule YAML under `## Rules` and update `- Updated: YYYY-MM-DD`.
5. Validate required schema fields and report result.

## Workflow

1. **Locate target policy file**
   - Resolve `<docs-dir>` from repository contract docs.
   - Route to `module-<slug>.md` from user domain/module input.
   - If file missing, create it using module template.

2. **Run AskTheUser interview**
   - Collect:
     - policy domain/module
     - policy description (title + intent)
     - code sample(s) from repo or user snippet
     - additional metadata (severity, evidence expectation, exceptions, source, ADR, status)
   - Offer defaults when user is unsure:
     - `severity: high`
     - `source: user-specified`
     - `status: active`
     - `allowed_exceptions: none`

3. **Decide operation mode**
   - **Add**: no matching rule ID/intent found.
   - **Modify**: user names rule ID, or intent clearly maps to an existing rule.
   - Preserve stable IDs when intent is unchanged.
   - If intent changes materially, add a new ID and deprecate old rule with rationale.

4. **Write contract-compliant rule**
   - Required fields:
     - `id`, `title`, `scope`, `severity`, `intent`, `check_logic`, `evidence_expectation`, `allowed_exceptions`, `source`, `status`
   - Optional fields:
     - `related_adr`
     - `automation` metadata
   - Keep scope as `module:<slug>` for module files.

5. **Validate and report**
   - Validate against checklist in `references/policy-rule-checklist.md`.
   - If available, run `python skills/review-policy-rule-builder/scripts/validate_policy_rule.py <policy-file>`.
   - Report created/updated rule IDs, file path, and any unresolved ambiguity.

## Guardrails

- Never silently delete existing rules.
- If replacing policy intent, mark prior rule `status: deprecated`.
- Keep edits minimal and localized to target module policy.
- Keep policy language testable and evidence-oriented.
- If user input conflicts with ADR constraints, mark `status: needs-decision` and note conflict.
