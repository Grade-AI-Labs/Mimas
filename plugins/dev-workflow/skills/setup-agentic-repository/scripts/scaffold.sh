#!/usr/bin/env bash
# Scaffold verbatim files for the agent instruction tree (dev-workflow layout).
#
# Creates directories, copies universal template files, composes
# AGENT_WORKFLOW.md with platform-specific sections, and writes the
# docs/agents/ files the dev-workflow skills read (issue-tracker.md,
# triage-labels.md, domain.md). The LLM only needs to generate
# project-specific files (AGENTS.md, CODING_STANDARDS.md, ENGINEERING.md,
# FEATURES.md, and GLOSSARY.md / GLOSSARY-MAP.md when there are terms to record).
#
# Usage:
#   bash scripts/scaffold.sh --target /path/to/repo --platform github --tracker github
#   bash scripts/scaffold.sh --target . --platform azure-devops --tracker azure-devops
#   bash scripts/scaffold.sh --target /path/to/repo --platform generic --tracker local
#   bash scripts/scaffold.sh --help
#
# Output:
#   JSON object to stdout listing all created files and any warnings.
#   Progress messages go to stderr.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_DIR/templates"

# --- helpers ---

log() { echo "  $1" >&2; }

usage() {
  cat <<'USAGE'
Usage: scaffold.sh --target DIR --platform PLATFORM --tracker TRACKER [OPTIONS]

Options:
  --target DIR        Target repository root directory (required)
  --platform PLATFORM One of: github, azure-devops, gitlab, bitbucket, generic (required)
  --tracker TRACKER   One of: github, gitlab, local, azure-devops, jira, linear, other (required).
                      Copies that tracker's operations to <docs-dir>/issue-tracker.md.
                      "other" copies nothing: write issue-tracker.md from the user's
                      description instead.
  --docs-dir DIR      Relative path inside the repo for the agent docs root.
                      Defaults to "docs/agents", where the dev-workflow skills
                      look for issue-tracker.md, triage-labels.md and domain.md.
  --help              Show this help message

Examples:
  bash scripts/scaffold.sh --target /path/to/repo --platform github --tracker github
  bash scripts/scaffold.sh --target . --platform azure-devops --tracker jira
  bash scripts/scaffold.sh --target . --platform generic --tracker local
USAGE
  exit 0
}

# Copy file if destination doesn't exist, substituting {{DOCS_DIR}} along the way.
# Prints "created" or "skipped".
copy_if_missing() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [[ -f "$dst" ]]; then
    echo "skipped"
  else
    sed "s|{{DOCS_DIR}}|$DOCS_DIR|g" "$src" > "$dst"
    echo "created"
  fi
}

# --- parse args ---

TARGET=""
PLATFORM=""
TRACKER=""
DOCS_DIR="docs/agents"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)   TARGET="$2"; shift 2 ;;
    --platform) PLATFORM="$2"; shift 2 ;;
    --tracker)  TRACKER="$2"; shift 2 ;;
    --docs-dir) DOCS_DIR="$2"; shift 2 ;;
    --help)     usage ;;
    *) echo "Error: Unknown option: $1. Use --help for usage." >&2; exit 1 ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo '{"error": "--target is required. Use --help for usage."}'; exit 1
fi
if [[ -z "$PLATFORM" ]]; then
  echo '{"error": "--platform is required. Use --help for usage."}'; exit 1
fi
if [[ -z "$TRACKER" ]]; then
  echo '{"error": "--tracker is required. Use --help for usage."}'; exit 1
fi
case "$PLATFORM" in
  github|azure-devops|gitlab|bitbucket|generic) ;;
  *) echo "{\"error\": \"--platform must be one of: github, azure-devops, gitlab, bitbucket, generic. Received: $PLATFORM\"}"; exit 1 ;;
esac
case "$TRACKER" in
  github|gitlab|local|azure-devops|jira|linear|other) ;;
  *) echo "{\"error\": \"--tracker must be one of: github, gitlab, local, azure-devops, jira, linear, other. Received: $TRACKER\"}"; exit 1 ;;
esac

# Normalize and validate docs dir: strip leading/trailing slashes, reject absolute paths and parent traversal.
DOCS_DIR="${DOCS_DIR#/}"
DOCS_DIR="${DOCS_DIR%/}"
if [[ -z "$DOCS_DIR" ]]; then
  echo '{"error": "--docs-dir must not be empty."}'; exit 1
fi
if [[ "$DOCS_DIR" == *".."* ]]; then
  echo "{\"error\": \"--docs-dir must be a relative path inside the repo, got: $DOCS_DIR\"}"; exit 1
fi

TARGET="$(cd "$TARGET" && pwd)"
if [[ ! -d "$TARGET" ]]; then
  echo "{\"error\": \"Target directory does not exist: $TARGET\"}"; exit 1
fi

# --- scaffold ---

# Collect JSON report pieces
FILES_JSON=""
WARNINGS=""

add_file_entry() {
  local path="$1" status="$2" extra="${3:-}"
  local entry="{\"path\": \"$path\", \"status\": \"$status\"$extra}"
  if [[ -n "$FILES_JSON" ]]; then FILES_JSON="$FILES_JSON, $entry"; else FILES_JSON="$entry"; fi
}

# 1. Create directory structure
mkdir -p "$TARGET/$DOCS_DIR/features"
log "dir: $DOCS_DIR/"
log "dir: $DOCS_DIR/features/"

# 2. CLAUDE.md — not created: Claude Code reads AGENTS.md natively, but only while no CLAUDE.md exists
if [[ -f "$TARGET/CLAUDE.md" || -f "$TARGET/CLAUDE.local.md" ]]; then
  WARNINGS="\"CLAUDE.md or CLAUDE.local.md exists: Claude Code ignores AGENTS.md while it does. Merge it into AGENTS.md and remove it, or add @AGENTS.md to it.\""
  log "warning: CLAUDE.md exists — AGENTS.md will not load until it is merged and removed"
fi

# 3. Verbatim docs (with DOCS_DIR substitution)
for pair in \
  "AGENTS_FEATURES.md:AGENTS_FEATURES.md" \
  "feature-template.md:features/feature-template.md" \
  "LESSONS.md:LESSONS.md" \
  "domain.md:domain.md" \
  "triage-labels.md:triage-labels.md"; do
  src="${pair%%:*}"; dst="${pair#*:}"
  STATUS=$(copy_if_missing "$TEMPLATES_DIR/$src" "$TARGET/$DOCS_DIR/$dst")
  add_file_entry "$DOCS_DIR/$dst" "$STATUS"
  log "$STATUS: $DOCS_DIR/$dst"
done

# 4. $DOCS_DIR/issue-tracker.md — the chosen tracker's operations ("other" is written by the LLM)
if [[ "$TRACKER" == "other" ]]; then
  log "pending: $DOCS_DIR/issue-tracker.md (tracker: other — write it from the user's description)"
else
  STATUS=$(copy_if_missing "$TEMPLATES_DIR/issue-trackers/$TRACKER.md" "$TARGET/$DOCS_DIR/issue-tracker.md")
  add_file_entry "$DOCS_DIR/issue-tracker.md" "$STATUS" ", \"tracker\": \"$TRACKER\""
  log "$STATUS: $DOCS_DIR/issue-tracker.md (tracker: $TRACKER)"
fi

# 5. $DOCS_DIR/AGENT_WORKFLOW.md — composed from base + platform section, then DOCS_DIR substituted
if [[ -f "$TARGET/$DOCS_DIR/AGENT_WORKFLOW.md" ]]; then
  add_file_entry "$DOCS_DIR/AGENT_WORKFLOW.md" "skipped"
  log "skipped: $DOCS_DIR/AGENT_WORKFLOW.md (already exists)"
else
  PLATFORM_SECTION=""
  SECTION_FILE="$TEMPLATES_DIR/workflow-sections/$PLATFORM.md"
  if [[ "$PLATFORM" != "generic" && -f "$SECTION_FILE" ]]; then
    PLATFORM_SECTION="$(cat "$SECTION_FILE")"
  fi

  # Replace placeholder with platform section (or remove it)
  BASE="$(cat "$TEMPLATES_DIR/AGENT_WORKFLOW.base.md")"
  if [[ -n "$PLATFORM_SECTION" ]]; then
    COMPOSED="${BASE/\{\{PLATFORM_SECTION\}\}/$PLATFORM_SECTION}"
  else
    COMPOSED="${BASE/\{\{PLATFORM_SECTION\}\}
/}"
  fi

  # Substitute {{DOCS_DIR}} placeholder after composition
  printf '%s\n' "$COMPOSED" | sed "s|{{DOCS_DIR}}|$DOCS_DIR|g" > "$TARGET/$DOCS_DIR/AGENT_WORKFLOW.md"
  add_file_entry "$DOCS_DIR/AGENT_WORKFLOW.md" "created" ", \"platform\": \"$PLATFORM\""
  log "created: $DOCS_DIR/AGENT_WORKFLOW.md (platform: $PLATFORM)"
fi

CREATED_FILES=$(echo "[$FILES_JSON]" | { grep -o '"created"' || true; } | wc -l | tr -d ' ')

# Summary
log ""
log "Scaffolded $CREATED_FILES files in $DOCS_DIR/."
log "LLM still needs to generate: AGENTS.md, CODING_STANDARDS.md, $DOCS_DIR/ENGINEERING.md, $DOCS_DIR/FEATURES.md, GLOSSARY.md or GLOSSARY-MAP.md if there are terms to record$([[ "$TRACKER" == "other" ]] && echo ", $DOCS_DIR/issue-tracker.md")."

# JSON report to stdout
cat <<REPORT
{
  "docs_dir": "$DOCS_DIR",
  "files": [$FILES_JSON],
  "warnings": [$WARNINGS]
}
REPORT
