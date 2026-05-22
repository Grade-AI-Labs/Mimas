# Review Policy Contract (`review-policy-builder`)

This contract defines the policy artifacts consumed by `agentic-review`.

Policy directory:
- `<docs-dir>/review/policies/`

Required files:
- `POLICY_INDEX.md`
- `global-policy.md`
- `module-<slug>.md` (one or more)

Audit-governance requirement:
- `POLICY_INDEX.md` must include a `Review Audit Contract` section consumed by `agentic-review`.

## Rule Schema (Required)

Each policy rule must follow this metadata schema:

```yaml
id: RP-GLOBAL-001
title: No inward dependency violations
scope: global | module:<slug>
severity: critical | high | medium | low
intent: Why this rule exists in domain/runtime terms
check_logic: How reviewer determines pass/fail/unknown
evidence_expectation: Required evidence in findings (file/line/tests/trace)
allowed_exceptions: Explicitly allowed exception cases or "none"
source: derived | user-specified | adr
related_adr: ADR-0042 (optional)
status: active | deprecated | needs-decision
```

Rules without these fields are invalid.

Optional automation metadata (for deterministic checks by `agentic-review`):

```yaml
automation:
  check_type: inheritance_suffix
  apply_scope: changed-files | all-files
  selector:
    class_name_suffix: Controller
  expectation:
    base_class_suffix: MainController
    match_strategy: same-stem-suffix
```

Automation notes:
- `check_type: inheritance_suffix` is the v1 machine-check type.
- `apply_scope` defaults to `changed-files` when omitted.
- `selector.class_name_suffix` targets classes to validate (for example `Controller`).
- `expectation.base_class_suffix` defines the required base pattern.
- `expectation.match_strategy: same-stem-suffix` means `<Stem><selector suffix>` must extend `<Stem><base suffix>`.

## Artifact Templates

## `global-policy.md`

Use:
- cross-project architecture constraints
- global security/data/API rules
- org-level invariants

Template:

````markdown
# Global Review Policy

## Metadata
- Updated: YYYY-MM-DD
- Source inputs: AGENTS.md, ENGINEERING.md, ADRs

## Rules
### RP-GLOBAL-001
```yaml
id: RP-GLOBAL-001
title: ...
scope: global
severity: high
intent: ...
check_logic: ...
evidence_expectation: ...
allowed_exceptions: none
source: derived
related_adr: ADR-0007
status: active
```
````

## `module-<slug>.md`

Use:
- module-specific architecture/call-flow/dependency rules
- module-specific risk hotspots and exception corridors

Template:

````markdown
# Module Review Policy: <slug>

## Metadata
- Context: <context name/path>
- Updated: YYYY-MM-DD
- Owning subtree(s): ...

## Rules
### RP-<SLUG>-001
```yaml
id: RP-<SLUG>-001
title: ...
scope: module:<slug>
severity: critical
intent: ...
check_logic: ...
evidence_expectation: ...
allowed_exceptions: "Only for <adapter-type> behind <interface>"
source: user-specified
related_adr: ADR-0013
status: active
automation:
  check_type: inheritance_suffix
  apply_scope: changed-files
  selector:
    class_name_suffix: Controller
  expectation:
    base_class_suffix: MainController
    match_strategy: same-stem-suffix
```
````

## `POLICY_INDEX.md`

Must include:
- policy coverage map by module
- mapping from context/subtree to module policy file
- unresolved conflicts (`needs-decision`)
- last updated stamp
- review audit contract metadata for specialist attestations/completion mode

Template:

```markdown
# Review Policy Index

## Metadata
- Updated: YYYY-MM-DD
- Policy schema version: 1

## Module Coverage
| Module | Context path | Policy file | Coverage status |
| --- | --- | --- | --- |
| billing | `backend/billing` | `module-billing.md` | complete |

## Routing Map
| File subtree | Module policy |
| --- | --- |
| `backend/billing/**` | `module-billing.md` |

## Global Policy
- `global-policy.md`

## Review Audit Contract
```yaml
audit_contract_version: 1
completion_mode: fail-closed
required_attestation_fields:
  - specialist_slug
  - specialist_type
  - assigned_scope
  - status
  - signed_at
  - attestation_text
  - output_artifact_path
required_specialist_categories:
  module: always
  cross_cut: when-routed-by-file-semantics
transparency_mode: summary + artifact links
```

## Needs Decision
- [ ] RP-BILLING-004 contradicts ADR-0012 (explain conflict)

## Automated Checks
| Rule ID | Check type | Scope | Policy file |
| --- | --- | --- | --- |
| RP-BILLING-006 | inheritance_suffix | changed-files | module-billing.md |
```

## Onion / Clean Architecture Templates

Use these templates when architecture requires layered constraints.

### 1. Dependency Direction Matrix

Define allowed dependencies:

| From \ To | presentation | application | domain | infrastructure |
| --- | --- | --- | --- | --- |
| presentation | allow | allow | deny | deny |
| application | deny | allow | allow | allow (via port) |
| domain | deny | deny | allow | deny |
| infrastructure | deny | allow | allow | allow |

Convert each denied edge into explicit policy rules.

### 2. Call-Flow Integrity Rule

Template:

```yaml
id: RP-ARCH-ONION-001
title: Controller call flow respects onion boundaries
scope: module:<slug>
severity: critical
intent: Prevent business logic leakage and boundary inversion
check_logic: "Handlers/controllers call application services only; domain logic is not orchestrated in transport layer; infrastructure adapters are invoked via ports/interfaces."
evidence_expectation: "File+line references showing call chain or forbidden direct call."
allowed_exceptions: "none"
source: user-specified
related_adr: ADR-00XX
status: active
```

### 3. Anti-Corruption Boundary Rule

Template:

```yaml
id: RP-ARCH-ONION-002
title: External models must pass through anti-corruption mapping
scope: module:<slug>
severity: high
intent: Shield domain model from external schema drift
check_logic: "No direct external DTO/entity usage in domain/application core; mapping occurs at boundary adapters."
evidence_expectation: "Evidence of direct external type crossing boundary or proof of mapper usage."
allowed_exceptions: "none"
source: derived
status: active
```

## Merge and Lifecycle Rules

- Preserve stable `id` values for unchanged policy intent.
- If intent changes materially, create a new rule id and deprecate the old one.
- Never delete rules silently; mark `status: deprecated` and include rationale.
- Contradictions with ADRs or unresolved stakeholder disagreements must be marked `status: needs-decision`.
- Keep `Review Audit Contract` synchronized with current attestation/completion requirements; when changed, update `audit_contract_version` and document rationale.
