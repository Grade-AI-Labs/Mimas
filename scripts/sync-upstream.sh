#!/usr/bin/env bash
# Vendor Matt Pocock's promoted skills into plugins/dev-workflow/skills/, unchanged.
#
# Usage: scripts/sync-upstream.sh [ref]     (default: main)
#
# Reads the upstream plugin.json `skills` array (exactly the promoted set),
# copies each skill folder flat into the plugin, drops Codex-only files, and
# records the upstream commit in UPSTREAM. Our own skills (listed in OWN_SKILLS)
# are never touched. Review the diff before committing.
set -euo pipefail

REF="${1:-main}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO/plugins/dev-workflow/skills"
OWN_SKILLS=("orchestrate-spec")
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone -q https://github.com/mattpocock/skills.git "$TMP/upstream"
git -C "$TMP/upstream" checkout -q "$REF"
SHA="$(git -C "$TMP/upstream" rev-parse HEAD)"

# Remove previously vendored skills (anything not ours), so upstream deletions propagate.
mkdir -p "$DEST"
for dir in "$DEST"/*/; do
  [ -d "$dir" ] || continue
  name="$(basename "$dir")"
  keep=false
  for own in "${OWN_SKILLS[@]}"; do [ "$name" = "$own" ] && keep=true; done
  $keep || rm -rf "$dir"
done

# Copy the promoted set listed in upstream's plugin.json.
node -e '
  const p = require(process.argv[1]);
  for (const s of p.skills) console.log(s);
' "$TMP/upstream/.claude-plugin/plugin.json" | while read -r rel; do
  name="$(basename "$rel")"
  for own in "${OWN_SKILLS[@]}"; do
    if [ "$name" = "$own" ]; then echo "error: upstream skill '$name' collides with ours" >&2; exit 1; fi
  done
  cp -R "$TMP/upstream/$rel" "$DEST/$name"
  rm -rf "$DEST/$name/agents"   # Codex-only metadata (agents/openai.yaml)
  echo "vendored $name"
done

cp "$TMP/upstream/LICENSE" "$REPO/plugins/dev-workflow/LICENSE-mattpocock-skills"
printf 'repo: https://github.com/mattpocock/skills\ncommit: %s\nsynced: %s\n' \
  "$SHA" "$(date -u +%Y-%m-%d)" > "$REPO/plugins/dev-workflow/UPSTREAM"

echo "done: upstream $SHA"
