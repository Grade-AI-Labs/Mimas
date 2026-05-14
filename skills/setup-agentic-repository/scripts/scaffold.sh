#!/usr/bin/env bash
# Scaffold verbatim files for the Mimas agent instruction tree.
#
# Creates directories, copies universal template files, and composes
# AGENT_WORKFLOW.md with platform-specific sections. The LLM only needs
# to generate project-specific files (AGENTS.md, ENGINEERING.md,
# FEATURES.md, subdomain CONTEXT.md).
#
# Usage:
#   bash scripts/scaffold.sh --target /path/to/repo --platform github
#   bash scripts/scaffold.sh --target . --platform azure-devops --docs-dir docs/agents
#   bash scripts/scaffold.sh --target /path/to/repo --platform generic
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
Usage: scaffold.sh --target DIR --platform PLATFORM [OPTIONS]

Options:
  --target DIR        Target repository root directory (required)
  --platform PLATFORM One of: github, azure-devops, gitlab, bitbucket, generic (required)
  --docs-dir DIR      Relative path inside the repo for the agent docs root.
                      Defaults to "agents-docs" — a sibling of any existing
                      "docs/" so the agent-instruction tree stays out of the
                      way of human-maintained project docs. Override with e.g.
                      "docs" or "docs/agents" if you want them under one roof.
  --help              Show this help message

Examples:
  bash scripts/scaffold.sh --target /path/to/repo --platform github
  bash scripts/scaffold.sh --target . --platform azure-devops --docs-dir docs/agents
  bash scripts/scaffold.sh --target . --platform generic --docs-dir docs
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
DOCS_DIR="agents-docs"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)   TARGET="$2"; shift 2 ;;
    --platform) PLATFORM="$2"; shift 2 ;;
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
case "$PLATFORM" in
  github|azure-devops|gitlab|bitbucket|generic) ;;
  *) echo "{\"error\": \"--platform must be one of: github, azure-devops, gitlab, bitbucket, generic. Received: $PLATFORM\"}"; exit 1 ;;
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

add_file_entry() {
  local path="$1" status="$2" extra="${3:-}"
  local entry="{\"path\": \"$path\", \"status\": \"$status\"$extra}"
  if [[ -n "$FILES_JSON" ]]; then FILES_JSON="$FILES_JSON, $entry"; else FILES_JSON="$entry"; fi
}

# 1. Create directory structure
mkdir -p "$TARGET/$DOCS_DIR/features"
log "dir: $DOCS_DIR/"
log "dir: $DOCS_DIR/features/"

# 2. CLAUDE.md — append if exists, create if not (no DOCS_DIR substitution needed)
CLAUDE_CONTENT="$(cat "$TEMPLATES_DIR/CLAUDE.md")"
if [[ -f "$TARGET/CLAUDE.md" ]]; then
  if grep -qF "$CLAUDE_CONTENT" "$TARGET/CLAUDE.md" 2>/dev/null; then
    add_file_entry "CLAUDE.md" "skipped"
    log "skipped: CLAUDE.md"
  else
    printf '\n%s' "$CLAUDE_CONTENT" >> "$TARGET/CLAUDE.md"
    add_file_entry "CLAUDE.md" "appended"
    log "appended: CLAUDE.md"
  fi
else
  printf '%s' "$CLAUDE_CONTENT" > "$TARGET/CLAUDE.md"
  add_file_entry "CLAUDE.md" "created"
  log "created: CLAUDE.md"
fi

# 3. $DOCS_DIR/AGENTS_FEATURES.md — universal, verbatim (with DOCS_DIR substitution)
STATUS=$(copy_if_missing "$TEMPLATES_DIR/AGENTS_FEATURES.md" "$TARGET/$DOCS_DIR/AGENTS_FEATURES.md")
add_file_entry "$DOCS_DIR/AGENTS_FEATURES.md" "$STATUS"
log "$STATUS: $DOCS_DIR/AGENTS_FEATURES.md"

# 4. $DOCS_DIR/features/feature-template.md — verbatim
STATUS=$(copy_if_missing "$TEMPLATES_DIR/feature-template.md" "$TARGET/$DOCS_DIR/features/feature-template.md")
add_file_entry "$DOCS_DIR/features/feature-template.md" "$STATUS"
log "$STATUS: $DOCS_DIR/features/feature-template.md"

# 4b. $DOCS_DIR/LESSONS.md — scaffolded with format and one seeded example
STATUS=$(copy_if_missing "$TEMPLATES_DIR/LESSONS.md" "$TARGET/$DOCS_DIR/LESSONS.md")
add_file_entry "$DOCS_DIR/LESSONS.md" "$STATUS"
log "$STATUS: $DOCS_DIR/LESSONS.md"

# 4c. $DOCS_DIR/AGENTS_CONTEXT.md — universal, verbatim — CONTEXT.md consumer/producer contract
STATUS=$(copy_if_missing "$TEMPLATES_DIR/AGENTS_CONTEXT.md" "$TARGET/$DOCS_DIR/AGENTS_CONTEXT.md")
add_file_entry "$DOCS_DIR/AGENTS_CONTEXT.md" "$STATUS"
log "$STATUS: $DOCS_DIR/AGENTS_CONTEXT.md"

# 4d. $DOCS_DIR/AGENTS_ADRS.md — universal, verbatim — ADR consumer/producer contract
STATUS=$(copy_if_missing "$TEMPLATES_DIR/AGENTS_ADRS.md" "$TARGET/$DOCS_DIR/AGENTS_ADRS.md")
add_file_entry "$DOCS_DIR/AGENTS_ADRS.md" "$STATUS"
log "$STATUS: $DOCS_DIR/AGENTS_ADRS.md"

# 4e. $DOCS_DIR/adr/0001-record-architectural-decisions.md — seeded meta-ADR
mkdir -p "$TARGET/$DOCS_DIR/adr"
log "dir: $DOCS_DIR/adr/"
STATUS=$(copy_if_missing "$TEMPLATES_DIR/ADR_0001.md" "$TARGET/$DOCS_DIR/adr/0001-record-architectural-decisions.md")
add_file_entry "$DOCS_DIR/adr/0001-record-architectural-decisions.md" "$STATUS"
log "$STATUS: $DOCS_DIR/adr/0001-record-architectural-decisions.md"

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

CREATED_FILES=$(echo "[$FILES_JSON]" | grep -o '"created"' | wc -l)

# Summary
log ""
log "Scaffolded $CREATED_FILES files in $DOCS_DIR/."
log "LLM still needs to generate: AGENTS.md, ENGINEERING.md, FEATURES.md, subdomain CONTEXT.md files (and $DOCS_DIR/CONTEXT-MAP.md if multi-context)."

# JSON report to stdout
cat <<REPORT
{
  "docs_dir": "$DOCS_DIR",
  "files": [$FILES_JSON],
  "warnings": []
}
REPORT
