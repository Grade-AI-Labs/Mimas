# Policy Rule Checklist

Use this checklist before saving global or module policy edits.

## Required rule schema

Every rule YAML block must include:

- `id`
- `title`
- `scope` (`global` for global file, `module:<slug>` for module files)
- `severity` (`critical|high|medium|low`)
- `intent`
- `check_logic`
- `evidence_expectation`
- `allowed_exceptions`
- `source` (`derived|user-specified|adr`)
- `status` (`active|deprecated|needs-decision`)

Optional fields:

- `related_adr`
- `automation`

## Merge rules

- Keep ID stable when rule intent is unchanged.
- If intent changes materially, add a new ID and deprecate the old rule.
- Never remove historical rules silently.

## Interview minimums

Confirm these inputs via AskTheUser:

- target domain/module
- plain-language rule description
- code example(s) or snippet context
- severity and intent
- explicit exceptions

## Suggested defaults

- `severity: high`
- `source: user-specified`
- `status: active`
- `allowed_exceptions: none`

## File integrity

- Target file is one of:
  - `<docs-dir>/review/policies/global-policy.md`
  - `<docs-dir>/review/policies/module-<slug>.md`
- Header format stays:
  - `# Global Review Policy` for global file
  - `# Module Review Policy: <slug>` for module file
- Metadata `Updated` date is refreshed.
- Rule added under `## Rules` with `### RP-...` heading and fenced YAML.

## Scope and ID alignment

- In `global-policy.md`, every rule uses `scope: global`.
- In `module-<slug>.md`, every rule uses `scope: module:<slug>`.
- Prefer ID family by file:
  - global file: `RP-GLOBAL-...`
  - module file: `RP-<MODULE>-...`

## POLICY_INDEX updates

When `<docs-dir>/review/policies/POLICY_INDEX.md` exists and the rule change is relevant:

- Refresh `- Updated: YYYY-MM-DD`.
- Update `## Needs Decision` for new/changed `status: needs-decision` rules.

### Purpose of `Automated Checks`

- `Automated Checks` lists machine-checkable policy rules so reviewers can see deterministic enforcement coverage.
- Include a rule when it has actionable `automation` metadata that should be tracked for auditability.
- Exclude only when the user explicitly defers index tracking.

### `Automated Checks` decision rule

- If automation is added, changed, or removed, ask the user whether to update `Automated Checks`.
- Recommended default is `Yes` for all automation changes.
- If user answers `Yes`, upsert or remove row keyed by Rule ID.
- If user answers `No`, leave section unchanged and report override.
