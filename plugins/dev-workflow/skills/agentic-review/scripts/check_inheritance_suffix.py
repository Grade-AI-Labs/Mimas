#!/usr/bin/env python3
"""Deterministic `inheritance_suffix` policy check for agentic-review (Phase 4).

Reads the review policies (`global-policy.md`, `module-<slug>.md`, and the
routing tables in `POLICY_INDEX.md`), selects active rules whose
`automation.check_type` is `inheritance_suffix`, and checks every targeted
class against the rule's base-class expectation.

Usage:
  check_inheritance_suffix.py --policies-dir docs/agents/review/policies \\
      --changed-files changed.txt [--repo .] [--output result.json]

`--changed-files` is a file with one repo-relative path per line (`-` reads
stdin). Output is one JSON object; the exit code is 0 whatever the rules
found, and 2 for a usage error.

Languages: Python (parsed with `ast`); TypeScript/JavaScript, Java and C#
(regex over the source with comments removed). Files in other class-based
languages are reported as unknown targets; other files are not source and
are ignored.

Python standard library only.
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CHECK_TYPE = "inheritance_suffix"
STRATEGIES = {"same-stem-suffix", "any-base-with-suffix"}
SCOPES = {"changed-files", "all-files"}

REGEX_LANGS = {
    ".ts": "ts", ".tsx": "ts", ".mts": "ts", ".cts": "ts",
    ".js": "ts", ".jsx": "ts", ".mjs": "ts", ".cjs": "ts",
    ".java": "java",
    ".cs": "cs",
}
# Class-based languages this checker can't parse: a targeted file in one of
# these makes the rule `unknown` instead of silently passing.
UNSUPPORTED_LANGS = {
    ".kt", ".kts", ".scala", ".rb", ".php", ".swift", ".dart",
    ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".h", ".m", ".mm", ".groovy",
}

CLASS_RE = {
    "ts": re.compile(r"\bclass\s+([A-Za-z_$][\w$]*)\s*(?:<[^{]*?>)?\s*(?:extends\s+([A-Za-z_$][\w$.]*))?"),
    "java": re.compile(r"\bclass\s+([A-Za-z_]\w*)\s*(?:<[^{]*?>)?\s*(?:extends\s+([A-Za-z_][\w.]*))?"),
    "cs": re.compile(r"\bclass\s+([A-Za-z_]\w*)\s*(?:<[^{:]*?>)?\s*(?:\([^)]*\))?\s*(?::\s*([^{\n]+))?"),
}


# --- minimal YAML (the subset policy rule blocks use) ---


class YamlError(ValueError):
    pass


def _scalar(text: str):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [_scalar(part) for part in inner.split(",")] if inner else []
    if text == "{}":
        return {}
    return text


def parse_yaml(text: str):
    """Parse nested maps, block lists, inline lists and block scalars."""
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise YamlError("tab indentation")
        lines.append((len(raw) - len(raw.lstrip(" ")), raw.strip()))
    if not lines:
        return {}
    value, end = _parse_node(lines, 0, lines[0][0])
    if end != len(lines):
        raise YamlError(f"unexpected indentation at: {lines[end][1]}")
    return value


def _parse_node(lines, i, indent):
    if lines[i][1].startswith("- ") or lines[i][1] == "-":
        return _parse_list(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_list(lines, i, indent):
    items = []
    while i < len(lines) and lines[i][0] == indent and (lines[i][1].startswith("- ") or lines[i][1] == "-"):
        items.append(_scalar(lines[i][1][1:]))
        i += 1
    return items, i


def _parse_map(lines, i, indent):
    out: dict = {}
    while i < len(lines):
        ind, content = lines[i]
        if ind < indent:
            break
        if ind > indent:
            raise YamlError(f"unexpected indentation at: {content}")
        if content.startswith("- "):
            break
        key, sep, rest = content.partition(":")
        if not sep or not key.strip():
            raise YamlError(f"expected 'key: value', got: {content}")
        key, rest = key.strip(), rest.strip()
        i += 1
        if rest in {"|", ">", "|-", ">-", "|+", ">+"}:
            parts = []
            while i < len(lines) and lines[i][0] > ind:
                parts.append(lines[i][1])
                i += 1
            out[key] = ("\n" if rest.startswith("|") else " ").join(parts)
        elif rest:
            out[key] = _scalar(rest)
        elif i < len(lines) and (lines[i][0] > ind or (lines[i][0] == ind and lines[i][1].startswith("- "))):
            out[key], i = _parse_node(lines, i, lines[i][0])
        else:
            out[key] = None
    return out, i


# --- policies ---


YAML_BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
ID_LINE_RE = re.compile(r"^id:\s*['\"]?([^'\"\s]+)", re.MULTILINE)


def load_rules(policies_dir: Path) -> list[dict]:
    files = []
    if (policies_dir / "global-policy.md").is_file():
        files.append(policies_dir / "global-policy.md")
    files.extend(sorted(policies_dir.glob("module-*.md")))
    rules = []
    for path in files:
        for block in YAML_BLOCK_RE.findall(path.read_text(encoding="utf-8")):
            id_match = ID_LINE_RE.search(block)
            if not id_match:
                continue
            try:
                data = parse_yaml(block)
                error = None if isinstance(data, dict) else "rule block is not a mapping"
            except YamlError as exc:
                data, error = {}, f"malformed rule YAML: {exc}"
            rules.append({"file": path.name, "id": id_match.group(1), "data": data if isinstance(data, dict) else {},
                          "error": error, "has_automation": re.search(r"^automation:", block, re.MULTILINE) is not None})
    return rules


ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
MODULE_FILE_RE = re.compile(r"module-[a-z0-9-]+\.md")


def load_routes(policies_dir: Path) -> dict[str, list[str]]:
    """Map `module-<slug>.md` to the subtree patterns POLICY_INDEX.md routes to it."""
    index = policies_dir / "POLICY_INDEX.md"
    routes: dict[str, list[str]] = {}
    if not index.is_file():
        return routes
    for line in index.read_text(encoding="utf-8").splitlines():
        row = ROW_RE.match(line)
        if not row:
            continue
        cells = [c.strip() for c in row.group(1).split("|")]
        module_files = [m for c in cells for m in MODULE_FILE_RE.findall(c)]
        if len(set(module_files)) != 1:
            continue
        for cell in cells:
            if MODULE_FILE_RE.search(cell):
                continue
            for pattern in re.findall(r"`([^`]+)`", cell):
                if "/" in pattern or "*" in pattern:
                    routes.setdefault(module_files[0], []).append(pattern.strip())
    return routes


def in_subtree(path: str, pattern: str) -> bool:
    pattern = pattern.removeprefix("./")
    if any(ch in pattern for ch in "*?["):
        return fnmatch.fnmatchcase(path, pattern)
    prefix = pattern.rstrip("/") + "/"
    return path.startswith(prefix) or path == pattern.rstrip("/")


# --- source parsing ---


def _blank_comments(source: str) -> str:
    def keep_newlines(match: re.Match) -> str:
        return re.sub(r"[^\n]", " ", match.group(0))

    source = re.sub(r"/\*.*?\*/", keep_newlines, source, flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", source)


def _base_name(base: str) -> str:
    base = re.sub(r"<.*", "", base.strip())  # drop generic arguments
    base = re.sub(r"\(.*", "", base)
    return base.split(".")[-1].strip()


def _py_base(node: ast.expr) -> str | None:
    if isinstance(node, ast.Subscript):
        node = node.value
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def find_classes(path: Path, rel: str) -> tuple[list[tuple[str, int, list[str]]] | None, str | None]:
    """Return ([(class, line, [base names])], None) or (None, reason) when the file can't be analysed."""
    ext = path.suffix.lower()
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return None, f"unreadable: {exc}"
    if ext == ".py":
        try:
            tree = ast.parse(source, filename=rel)
        except SyntaxError as exc:
            return None, f"python syntax error at line {exc.lineno}"
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = [b for b in (_py_base(n) for n in node.bases) if b]
                classes.append((node.name, node.lineno, bases))
        return sorted(classes, key=lambda c: c[1]), None
    lang = REGEX_LANGS.get(ext)
    if lang:
        text = _blank_comments(source)
        classes = []
        for match in CLASS_RE[lang].finditer(text):
            name, raw_bases = match.group(1), match.group(2) or ""
            if lang == "cs":
                raw_bases = re.split(r"\bwhere\b", raw_bases)[0]
                parts = [p for p in re.split(r",(?![^<]*>)", raw_bases) if p.strip()]
            else:
                parts = [raw_bases] if raw_bases else []
            line = text.count("\n", 0, match.start()) + 1
            classes.append((name, line, [_base_name(p) for p in parts]))
        return classes, None
    if ext in UNSUPPORTED_LANGS:
        return None, f"language not supported ({ext})"
    return [], None  # not source code: nothing to check


# --- evaluation ---


def _get(data: dict, *keys):
    for key in keys:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def automation_problems(auto: dict) -> list[str]:
    problems = []
    suffix = _get(auto, "selector", "class_name_suffix")
    base = _get(auto, "expectation", "base_class_suffix")
    if not isinstance(suffix, str) or not suffix:
        problems.append("missing automation.selector.class_name_suffix")
    if not isinstance(base, str) or not base:
        problems.append("missing automation.expectation.base_class_suffix")
    exclude = _get(auto, "selector", "exclude")
    if exclude is not None and not (isinstance(exclude, list) and all(isinstance(x, str) for x in exclude)):
        problems.append("automation.selector.exclude must be a list of class names")
    scope = auto.get("apply_scope", "changed-files")
    if scope not in SCOPES:
        problems.append(f"unknown apply_scope '{scope}'")
    return problems


def evaluate_rule(rule: dict, targets: list[str], repo: Path) -> dict:
    data, auto = rule["data"], rule["data"].get("automation") or {}
    strategy = _get(auto, "expectation", "match_strategy") or "same-stem-suffix"
    result = {
        "rule_id": rule["id"],
        "policy_file": rule["file"],
        "scope": data.get("scope"),
        "severity": data.get("severity"),
        "check_type": CHECK_TYPE,
        "apply_scope": auto.get("apply_scope", "changed-files") if isinstance(auto, dict) else None,
        "match_strategy": strategy,
        "status": "pass",
        "reason": "",
        "targets": targets,
        "violations": [],
        "evaluated": [],
        "skipped_excluded": [],
        "unknown_targets": [],
    }
    problems = automation_problems(auto)
    if strategy not in STRATEGIES:
        problems.append(f"unknown match_strategy '{strategy}'")
    if problems:
        result.update(status="unknown", reason="malformed automation metadata: " + "; ".join(problems))
        return result

    suffix = auto["selector"]["class_name_suffix"]
    base_suffix = auto["expectation"]["base_class_suffix"]
    exclude = set(_get(auto, "selector", "exclude") or [])
    for rel in targets:
        classes, problem = find_classes(repo / rel, rel)
        if classes is None:
            result["unknown_targets"].append({"file": rel, "reason": problem})
            continue
        for name, line, bases in classes:
            if not name.endswith(suffix):
                continue
            label = f"{rel}:{line} {name}({', '.join(bases)})"
            if name in exclude:
                result["skipped_excluded"].append(label)
                continue
            result["evaluated"].append(label)
            if strategy == "same-stem-suffix":
                expected = name[: -len(suffix)] + base_suffix
                ok = expected in bases
            else:
                expected = f"any base ending in {base_suffix}"
                ok = any(b.endswith(base_suffix) for b in bases)
            if not ok:
                result["violations"].append({"file": rel, "line": line, "class": name, "bases": bases, "expected": expected})

    if result["violations"]:
        result["status"] = "fail"
        result["reason"] = f"{len(result['violations'])} class(es) violate the expectation"
    elif result["unknown_targets"]:
        result["status"] = "unknown"
        result["reason"] = "some targeted files could not be analysed"
    else:
        result["reason"] = "no violations in targeted files" if result["evaluated"] else "no matching classes in targeted files"
    return result


def unknown_result(rule: dict, check_type: str | None, reason: str) -> dict:
    return {"rule_id": rule["id"], "policy_file": rule["file"], "check_type": check_type or CHECK_TYPE,
            "status": "unknown", "reason": reason, "targets": [], "violations": [], "evaluated": [],
            "skipped_excluded": [], "unknown_targets": []}


def all_files(repo: Path) -> list[str]:
    try:
        out = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True).stdout
        return [line for line in out.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for root, dirs, names in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules"}]
            files.extend(str(Path(root, n).relative_to(repo)) for n in names)
        return sorted(files)


def run(policies_dir: Path, repo: Path, changed: list[str]) -> dict:
    routes = load_routes(policies_dir)
    results, skipped = [], []
    repo_files: list[str] | None = None
    for rule in load_rules(policies_dir):
        data = rule["data"]
        auto = data.get("automation")
        if rule["error"]:
            if rule["has_automation"]:
                results.append(unknown_result(rule, None, rule["error"]))
            continue
        if not auto:
            continue
        if data.get("status", "active") != "active":
            skipped.append({"rule_id": rule["id"], "reason": f"status {data.get('status')}"})
            continue
        check_type = auto.get("check_type") if isinstance(auto, dict) else None
        if check_type != CHECK_TYPE:
            results.append(unknown_result(rule, check_type, f"unsupported check_type '{check_type}'"))
            continue

        scope = auto.get("apply_scope", "changed-files")
        if scope == "all-files":
            repo_files = all_files(repo) if repo_files is None else repo_files
            candidates = repo_files
        else:
            candidates = changed
        candidates = [f for f in candidates if (repo / f).is_file()]

        if rule["file"].startswith("module-"):
            patterns = routes.get(rule["file"])
            if not patterns:
                result = evaluate_rule(rule, [], repo)
                if result["status"] != "unknown":
                    result.update(status="unknown", reason=f"POLICY_INDEX.md routes no subtree to {rule['file']}")
                results.append(result)
                continue
            candidates = [f for f in candidates if any(in_subtree(f, p) for p in patterns)]
        results.append(evaluate_rule(rule, candidates, repo))

    summary = {s: sum(1 for r in results if r["status"] == s) for s in ("pass", "fail", "unknown")}
    return {
        "checker": "check_inheritance_suffix",
        "version": 1,
        "policies_dir": str(policies_dir),
        "changed_files": changed,
        "summary": summary,
        "rules": results,
        "skipped_rules": skipped,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--policies-dir", required=True, help="the review policies directory")
    parser.add_argument("--changed-files", required=True, help="file listing changed paths, one per line ('-' for stdin)")
    parser.add_argument("--repo", default=".", help="repository root the paths are relative to (default: .)")
    parser.add_argument("--output", help="write the JSON here instead of stdout")
    args = parser.parse_args(argv)

    policies_dir, repo = Path(args.policies_dir), Path(args.repo)
    if not policies_dir.is_dir():
        print(f"error: policies directory not found: {policies_dir}", file=sys.stderr)
        return 2
    if args.changed_files == "-":
        listing = sys.stdin.read()
    else:
        try:
            listing = Path(args.changed_files).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read --changed-files: {exc}", file=sys.stderr)
            return 2
    changed = [line.strip().removeprefix("./") for line in listing.splitlines() if line.strip()]

    report = json.dumps(run(policies_dir, repo, changed), indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(report + "\n", encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
