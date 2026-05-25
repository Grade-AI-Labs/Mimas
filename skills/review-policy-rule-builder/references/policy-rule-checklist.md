# Policy Rule Checklist

Use this checklist before saving module policy edits.

## Required rule schema

Every rule YAML block must include:

- `id`
- `title`
- `scope` (`module:<slug>` for module files)
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

- File path is `<docs-dir>/review/policies/module-<slug>.md`.
- Header format stays `# Module Review Policy: <slug>`.
- Metadata `Updated` date is refreshed.
- Rule added under `## Rules` with `### RP-...` heading and fenced YAML.
