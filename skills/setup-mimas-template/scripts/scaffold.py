#!/usr/bin/env python3
"""Scaffold verbatim files for the Mimas agent instruction tree.

Creates directories, copies universal template files, composes
AGENT_WORKFLOW.md with platform-specific sections, and scaffolds
starter skills. The LLM only needs to generate project-specific
files (AGENTS.md, ENGINEERING.md, FEATURES.md, subdomain AGENTS.md).

Usage:
    python3 scripts/scaffold.py --target /path/to/repo --platform github
    python3 scripts/scaffold.py --target . --platform azure-devops --skills grill-me,write-a-prd
    python3 scripts/scaffold.py --target /path/to/repo --platform generic --no-skills
    python3 scripts/scaffold.py --help

Output:
    JSON object to stdout listing all created files and any warnings.
    Progress messages go to stderr.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
STARTER_SKILLS_DIR = SKILL_DIR / "starter-skills"

ALL_UNIVERSAL_SKILLS = ["grill-me", "write-a-skill", "document-feature", "ubiquitous-language"]
VALID_PLATFORMS = ["github", "azure-devops", "gitlab", "bitbucket", "generic"]


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def copy_file(src: Path, dst: Path) -> bool:
    """Copy a file, creating parent dirs. Returns True if created, False if skipped."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return False
    shutil.copy2(src, dst)
    return True


def write_file(dst: Path, content: str, append: bool = False) -> str:
    """Write content to a file. Returns 'created', 'appended', or 'skipped'."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if append and dst.exists():
        existing = dst.read_text()
        if content.strip() in existing:
            return "skipped"
        with open(dst, "a") as f:
            f.write("\n" + content)
        return "appended"
    if dst.exists():
        return "skipped"
    dst.write_text(content)
    return "created"


def compose_agent_workflow(platform: str) -> str:
    """Compose AGENT_WORKFLOW.md from base template + platform section."""
    base = (TEMPLATES_DIR / "AGENT_WORKFLOW.base.md").read_text()

    platform_section = ""
    if platform != "generic":
        section_file = TEMPLATES_DIR / "workflow-sections" / f"{platform}.md"
        if section_file.exists():
            platform_section = section_file.read_text()

    return base.replace("{{PLATFORM_SECTION}}\n", platform_section)


def scaffold_skills(target: Path, platform: str, skills: list[str]) -> list[dict]:
    """Copy selected starter skills to .claude/skills/. Returns list of results."""
    results = []
    skills_dir = target / ".claude" / "skills"

    for skill_name in skills:
        if skill_name == "write-a-prd":
            # Platform-variant skill
            variant = platform if platform in ("github", "azure-devops") else "generic"
            src = STARTER_SKILLS_DIR / "platform-variants" / "write-a-prd" / variant
            dst = skills_dir / "write-a-prd"
        elif skill_name in ALL_UNIVERSAL_SKILLS:
            src = STARTER_SKILLS_DIR / "universal" / skill_name
            dst = skills_dir / skill_name
        else:
            results.append({"skill": skill_name, "status": "unknown_skill"})
            continue

        if not src.exists():
            results.append({"skill": skill_name, "status": "source_missing"})
            continue

        if dst.exists():
            results.append({"skill": skill_name, "status": "skipped", "path": str(dst.relative_to(target))})
            continue

        shutil.copytree(src, dst)
        results.append({"skill": skill_name, "status": "created", "path": str(dst.relative_to(target))})

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold verbatim files for the Mimas agent instruction tree.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/scaffold.py --target /path/to/repo --platform github
  python3 scripts/scaffold.py --target . --platform azure-devops --skills grill-me,write-a-prd
  python3 scripts/scaffold.py --target . --platform generic --no-skills
        """,
    )
    parser.add_argument(
        "--target", required=True,
        help="Target repository root directory",
    )
    parser.add_argument(
        "--platform", required=True, choices=VALID_PLATFORMS,
        help="Git platform for PR workflow and skill variants",
    )
    parser.add_argument(
        "--skills", default=",".join(ALL_UNIVERSAL_SKILLS + ["write-a-prd"]),
        help="Comma-separated list of starter skills to scaffold (default: all)",
    )
    parser.add_argument(
        "--no-skills", action="store_true",
        help="Skip starter skill scaffolding entirely",
    )

    args = parser.parse_args()
    target = Path(args.target).resolve()

    if not target.is_dir():
        print(json.dumps({"error": f"Target directory does not exist: {target}"}))
        sys.exit(1)

    report = {"files": [], "skills": [], "warnings": []}

    # 1. Create directory structure
    dirs = ["docs", "docs/features"]
    if not args.no_skills:
        dirs.append(".claude/skills")
    for d in dirs:
        p = target / d
        p.mkdir(parents=True, exist_ok=True)
        log(f"  dir: {d}/")

    # 2. CLAUDE.md — append if exists, create if not
    claude_md_content = (TEMPLATES_DIR / "CLAUDE.md").read_text()
    status = write_file(target / "CLAUDE.md", claude_md_content, append=True)
    report["files"].append({"path": "CLAUDE.md", "status": status})
    log(f"  {status}: CLAUDE.md")

    # 3. docs/AGENTS_FEATURES.md — universal, verbatim
    src = TEMPLATES_DIR / "AGENTS_FEATURES.md"
    dst = target / "docs" / "AGENTS_FEATURES.md"
    created = copy_file(src, dst)
    status = "created" if created else "skipped"
    report["files"].append({"path": "docs/AGENTS_FEATURES.md", "status": status})
    log(f"  {status}: docs/AGENTS_FEATURES.md")

    # 4. docs/features/feature-template.md — verbatim
    src = TEMPLATES_DIR / "feature-template.md"
    dst = target / "docs" / "features" / "feature-template.md"
    created = copy_file(src, dst)
    status = "created" if created else "skipped"
    report["files"].append({"path": "docs/features/feature-template.md", "status": status})
    log(f"  {status}: docs/features/feature-template.md")

    # 5. docs/AGENT_WORKFLOW.md — composed from base + platform section
    dst = target / "docs" / "AGENT_WORKFLOW.md"
    if dst.exists():
        report["files"].append({"path": "docs/AGENT_WORKFLOW.md", "status": "skipped"})
        log("  skipped: docs/AGENT_WORKFLOW.md (already exists)")
    else:
        content = compose_agent_workflow(args.platform)
        dst.write_text(content)
        report["files"].append({"path": "docs/AGENT_WORKFLOW.md", "status": "created", "platform": args.platform})
        log(f"  created: docs/AGENT_WORKFLOW.md (platform: {args.platform})")

    # 6. Scaffold starter skills
    if not args.no_skills:
        skills_list = [s.strip() for s in args.skills.split(",") if s.strip()]
        report["skills"] = scaffold_skills(target, args.platform, skills_list)
        for s in report["skills"]:
            log(f"  {s['status']}: .claude/skills/{s['skill']}/")

    # Summary
    created_count = sum(1 for f in report["files"] if f["status"] == "created")
    skills_count = sum(1 for s in report["skills"] if s["status"] == "created")
    log(f"\nScaffolded {created_count} files and {skills_count} skills.")
    log("LLM still needs to generate: AGENTS.md, ENGINEERING.md, FEATURES.md, subdomain AGENTS.md files.")

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
