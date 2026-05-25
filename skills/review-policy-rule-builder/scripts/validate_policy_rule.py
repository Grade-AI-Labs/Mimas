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


def validate_block(fields: dict[str, str], idx: int) -> list[str]:
    errs: list[str] = []
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

    return errs


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
    for i, block in enumerate(blocks, start=1):
        fields = parse_top_level_fields(block)
        errors.extend(validate_block(fields, i))

    if errors:
        print("validation: failed")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"validation: ok ({len(blocks)} rule blocks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
