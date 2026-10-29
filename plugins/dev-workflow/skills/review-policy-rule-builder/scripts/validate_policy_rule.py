#!/usr/bin/env python3
"""Validate review-policy rule YAML blocks inside a policy markdown file."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "title",
    "scope",
    "severity",
    "intent",
    "check_logic",
    "evidence_expectation",
    "allowed_exceptions",
    "source",
    "status",
}

VALID_SEVERITY = {"critical", "high", "medium", "low"}
VALID_SOURCE = {"derived", "user-specified", "adr"}
VALID_STATUS = {"active", "deprecated", "needs-decision"}
MODULE_FILE_RE = re.compile(r"^module-(?P<slug>[a-z0-9-]+)\.md$")
ID_GLOBAL_RE = re.compile(r"^RP-GLOBAL-[0-9]{3,}$")
ID_GENERIC_RE = re.compile(r"^RP-[A-Z0-9_]+(?:-[A-Z0-9_]+)*-[0-9]{3,}$")
VALID_CHECK_TYPES = {"inheritance_suffix"}
VALID_APPLY_SCOPES = {"changed-files", "all-files"}
VALID_MATCH_STRATEGIES = {"same-stem-suffix", "any-base-with-suffix"}


def parse_yaml_blocks(text: str) -> list[str]:
    pattern = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
    return pattern.findall(text)


def parse_top_level_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def parse_automation(block: str) -> dict[str, str] | None:
    """Flatten the nested `automation:` mapping into dotted keys, e.g. `selector.class_name_suffix`."""
    lines = block.splitlines()
    start = next((i for i, line in enumerate(lines) if re.match(r"^automation:\s*$", line)), None)
    if start is None:
        return None
    flat: dict[str, str] = {}
    stack: list[tuple[int, str]] = []
    for raw_line in lines[start + 1:]:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith((" ", "\t")):
            break
        indent = len(raw_line) - len(raw_line.lstrip())
        content = raw_line.strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        if content.startswith("- "):
            if stack:
                key = ".".join(k for _, k in stack)
                flat[key] = (flat.get(key, "") + "," + content[2:].strip()).lstrip(",")
            continue
        if ":" not in content:
            flat.setdefault("__malformed__", content)
            continue
        key, value = (part.strip() for part in content.split(":", 1))
        path = ".".join([k for _, k in stack] + [key])
        if value:
            flat[path] = value.strip('"').strip("'")
        else:
            stack.append((indent, key))
            flat.setdefault(path, "")
    return flat


def validate_automation(auto: dict[str, str], idx: int) -> list[str]:
    errs: list[str] = []
    if "__malformed__" in auto:
        errs.append(f"rule {idx}: automation: cannot parse line '{auto['__malformed__']}'")
    check_type = auto.get("check_type")
    if not check_type:
        errs.append(f"rule {idx}: automation.check_type is required")
        return errs
    if check_type not in VALID_CHECK_TYPES:
        errs.append(f"rule {idx}: unsupported automation.check_type '{check_type}' (supported: {', '.join(sorted(VALID_CHECK_TYPES))})")
        return errs
    scope = auto.get("apply_scope")
    if scope and scope not in VALID_APPLY_SCOPES:
        errs.append(f"rule {idx}: invalid automation.apply_scope '{scope}'")
    for key in ("selector.class_name_suffix", "expectation.base_class_suffix"):
        if not auto.get(key):
            errs.append(f"rule {idx}: automation.{key} is required for inheritance_suffix")
    strategy = auto.get("expectation.match_strategy")
    if strategy and strategy not in VALID_MATCH_STRATEGIES:
        errs.append(f"rule {idx}: invalid automation.expectation.match_strategy '{strategy}' (one of: {', '.join(sorted(VALID_MATCH_STRATEGIES))})")
    exclude = auto.get("selector.exclude")
    if exclude and exclude.startswith("[") != exclude.endswith("]"):
        errs.append(f"rule {idx}: automation.selector.exclude must be a list")
    return errs


def validate_block(fields: dict[str, str], idx: int) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    missing = sorted(REQUIRED_FIELDS - fields.keys())
    if missing:
        errs.append(f"rule {idx}: missing fields: {', '.join(missing)}")

    sev = fields.get("severity")
    if sev and sev not in VALID_SEVERITY:
        errs.append(f"rule {idx}: invalid severity '{sev}'")

    src = fields.get("source")
    if src and src not in VALID_SOURCE:
        errs.append(f"rule {idx}: invalid source '{src}'")

    status = fields.get("status")
    if status and status not in VALID_STATUS:
        errs.append(f"rule {idx}: invalid status '{status}'")

    scope = fields.get("scope")
    if scope and not (scope == "global" or scope.startswith("module:")):
        errs.append(f"rule {idx}: invalid scope '{scope}'")

    rule_id = fields.get("id")
    if rule_id and not ID_GENERIC_RE.match(rule_id):
        warns.append(f"rule {idx}: non-standard id format '{rule_id}'")

    return errs, warns


def validate_file_context(path: Path, all_fields: list[dict[str, str]]) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []

    name = path.name
    if name == "global-policy.md":
        for idx, fields in enumerate(all_fields, start=1):
            scope = fields.get("scope")
            if scope and scope != "global":
                errs.append(f"rule {idx}: global-policy.md requires scope 'global', got '{scope}'")
            rule_id = fields.get("id")
            if rule_id and not ID_GLOBAL_RE.match(rule_id):
                warns.append(f"rule {idx}: global policy rule id should usually match RP-GLOBAL-###, got '{rule_id}'")
        return errs, warns

    module_match = MODULE_FILE_RE.match(name)
    if module_match:
        slug = module_match.group("slug")
        expected_scope = f"module:{slug}"
        for idx, fields in enumerate(all_fields, start=1):
            scope = fields.get("scope")
            if scope and scope != expected_scope:
                errs.append(f"rule {idx}: {name} requires scope '{expected_scope}', got '{scope}'")
            rule_id = fields.get("id")
            if rule_id and rule_id.startswith("RP-GLOBAL-"):
                warns.append(f"rule {idx}: module policy should usually avoid global id family, got '{rule_id}'")
        return errs, warns

    warns.append("file: filename is not global-policy.md or module-<slug>.md; context checks skipped")
    return errs, warns


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_policy_rule.py <policy-file.md>")
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"error: file not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    blocks = parse_yaml_blocks(text)
    if not blocks:
        print("error: no yaml rule blocks found")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    parsed_fields: list[dict[str, str]] = []
    for i, block in enumerate(blocks, start=1):
        fields = parse_top_level_fields(block)
        parsed_fields.append(fields)
        block_errors, block_warnings = validate_block(fields, i)
        automation = parse_automation(block)
        if automation is not None:
            block_errors.extend(validate_automation(automation, i))
        errors.extend(block_errors)
        warnings.extend(block_warnings)

    context_errors, context_warnings = validate_file_context(path, parsed_fields)
    errors.extend(context_errors)
    warnings.extend(context_warnings)

    if errors:
        print("validation: failed")
        for err in errors:
            print(f"- {err}")
        if warnings:
            print("warnings:")
            for warn in warnings:
                print(f"- {warn}")
        return 1

    if warnings:
        print(f"validation: ok with warnings ({len(blocks)} rule blocks)")
        for warn in warnings:
            print(f"- {warn}")
        return 0

    print(f"validation: ok ({len(blocks)} rule blocks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
