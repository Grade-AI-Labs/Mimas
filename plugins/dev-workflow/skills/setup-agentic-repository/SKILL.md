---
name: setup-agentic-repository
description: "Configure this repo for the dev-workflow skills and scaffold its agent instructions: issue tracker, triage labels and domain doc layout (docs/agents/, GLOSSARY.md, docs/adr/), plus AGENTS.md, CODING_STANDARDS.md and the agent docs, all tailored to the repo's stack, git platform and conventions. Run once before first use of the other engineering skills."
disable-model-invocation: true
metadata:
  author: Olof Brogeby
  url: https://github.com/brogeby
---

# setup-agentic-repository

You are configuring a repository for the dev-workflow skills and scaffolding the instruction files agents read at the start of every session. This replaces Matt Pocock's `setup-matt-pocock-skills`: it writes everything that skill writes, in the same places, so every other skill in this plugin works unchanged — plus the Mimas instruction tree on top.

What the repo ends up with:

| Path | Read by |
|---|---|
| `AGENTS.md` (with the `## Agent skills` block and `## Modules`) | every session — Claude Code (v2.1.277+), Codex and other agents load it natively |
| `docs/agents/issue-tracker.md`, `triage-labels.md`, `domain.md` | `to-spec`, `to-tickets`, `triage`, `wayfinder`, `code-review`, `implement-spec`, `orchestrate-spec`, … |
| `GLOSSARY.md` / `GLOSSARY-MAP.md`, `docs/adr/` (both lazy) | `domain-modeling`, `grill-with-docs`, `tdd`, `pr`, … |
| `CODING_STANDARDS.md` | `code-review`, `agentic-review`, `retro` |
| `docs/agents/AGENT_WORKFLOW.md`, `ENGINEERING.md`, `LESSONS.md`, `FEATURES.md`, `AGENTS_FEATURES.md`, `features/` | every session, via `AGENTS.md` |

`docs/agents/` is the docs dir (`{{DOCS_DIR}}` in the references). Don't move it: the other skills look for their files there.

---

## Phase 1 — Automated Discovery

Explore before writing anything. **Launch three subagents in parallel** to maximize speed — each handles an independent research task. Collect their results before proceeding. In a small repo (roughly 50 source files or fewer), do the three tasks yourself instead: the subagents would cost more than they save.

### Subagent dispatch

Launch these three subagents simultaneously (one tool call with multiple Agent invocations):

**Subagent A — Tech stack & commands.** Read config files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `tsconfig.json`, `Dockerfile`, `Makefile`, `.prettierrc*`, `.eslintrc*`, `ruff.toml`, `.golangci.yml`, etc.) and report:

- Language(s) and version(s)
- Runtime and framework (Fastify, Express, Next.js, Django, FastAPI, chi, etc.)
- Test framework and how tests are organized
- Database and query layer (if any)
- Authentication mechanism (if any)
- AI/LLM libraries (if any)
- Package manager
- Type checking tool (e.g., tsc, mypy, pyright)
- **Formatter** (e.g., Prettier, Black, Ruff format, gofmt, rustfmt) — note this separately from the linter, since many stacks run them as distinct commands
- **Linter** (e.g., ESLint, Ruff, golangci-lint, Clippy)
- Exact, copy-pasteable commands for: setup/install, running tests, type checking, dev server, build, **format**, **lint** (check `package.json` scripts, `Makefile` targets, `pyproject.toml` scripts, `Dockerfile` entrypoints). If format and lint share a script, say so; if they're distinct, capture both.

**Subagent B — Project structure & conventions.** List top-level directories and report:

- Subdomains identified (top-level dirs that represent distinct parts of the app):
  - Single-package repos: typically `src/`, `app/`, `internal/`, `cmd/`
  - Monorepos: each `packages/<name>/` or `apps/<name>/`
  - Multi-part repos: `backend/`, `frontend/`, `server/`, `client/`, `api/`, `web/`
  - Ignore: `node_modules/`, `dist/`, `build/`, `.git/`, test fixtures, config dirs
- Role of each subdomain (backend API, frontend app, shared library, CLI tool, etc.)
- File naming pattern (kebab-case, camelCase, snake_case)
- Test file placement (colocated? separate `__tests__/` or `tests/` dir?)
- Module organization style (by feature? by layer? by domain?)
- Existing documentation (README.md content, any docs/ folder)
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Their absence means single-context, which is almost every repo.

**Subagent C — Git platform, CI/CD, hooks & existing files.** Read `.git/config`, check for CI and hook config files, sample recent commits, and scan existing docs:

- Git platform from remote URL: `github.com` → GitHub, `dev.azure.com` / `visualstudio.com` → Azure DevOps, `gitlab.com` → GitLab, `bitbucket.org` → Bitbucket
- CI/CD: `.github/workflows/` → GitHub Actions, `azure-pipelines.yml` → Azure Pipelines, `.gitlab-ci.yml` → GitLab CI
- **Pre-commit hooks**: check for `.husky/`, `.pre-commit-config.yaml`, `lefthook.yml`/`lefthook.yaml`, `.git/hooks/` with non-sample files. If found, report which framework is in use and what each hook runs (open the config and summarize) — agents need to know these will block their commits, and the setup section must include the install step (`pnpm install` runs Husky's prepare script, `pre-commit install`, `lefthook install`, etc.).
- **Commit message conventions**: run `git log -n 100 --pretty=%s` and report patterns you observe:
  - Conventional Commits prefixes (`feat:`, `fix:`, `chore:`, scopes like `feat(api):`)
  - Ticket-key prefixes/suffixes (`AB#123`, `PROJ-456`, `#789`) — this confirms or overrides the platform-based tracker guess
  - Imperative vs. past tense, line-length norms, anything else consistent across 10+ commits
  - If commits are inconsistent, say so — don't invent a convention. If every commit follows one pattern but there are fewer than ~10, document it and note the small sample
- Issue tracker hints from those same commit messages (`#123` → GitHub Issues, `AB#456` → Azure DevOps, `PROJ-789` → Jira/Linear)
- Whether `CLAUDE.md`, `AGENTS.md`, or `README.md` exist and have meaningful content (report a brief summary of what they contain), and whether either already has an `## Agent skills` block
- Prior setup output: `docs/agents/` (from this skill or `setup-matt-pocock-skills`), `GLOSSARY.md` / `GLOSSARY-MAP.md`, `docs/adr/` and any `*/docs/adr/`, `.scratch/` (a local-markdown tracker in use), `.out-of-scope/`
- Legacy domain docs: `CONTEXT.md` / `CONTEXT-MAP.md` anywhere (Matt's pre-1.3 name, or a Mimas `agents-docs/` scaffold), and an `agents-docs/` tree
- Duplicate skills: standalone copies of skills this plugin ships, which would trigger alongside the plugin's versions and expect the old layout. Look in `.claude/skills/`, `.agents/skills/` and `~/.claude/skills/` for folders named like any skill this plugin ships (the folder names in this plugin's `skills/` directory, next to this skill's own folder), plus `setup-matt-pocock-skills`. These are standalone copies, never the plugin's own. Also check whether the `mattpocock-skills` plugin is enabled (`enabledPlugins` in `.claude/settings.json` and `~/.claude/settings.json`).

### After subagents return

Combine the three reports into a unified picture. If any subagent couldn't determine something (e.g., no database found, no CI detected), that's fine — note it as "not detected" and move on.

For existing files:
- Pull project description from README into root `AGENTS.md` intro
- Incorporate documented conventions into `ENGINEERING.md` / `CODING_STANDARDS.md`
- If an existing `AGENTS.md` is empty or placeholder, replace it
- An existing `CLAUDE.md` (or `CLAUDE.local.md`) needs a decision in Phase 2: while one exists, Claude Code ignores `AGENTS.md`
- If an `## Agent skills` block exists, update it in place rather than adding a second one
- Existing `docs/agents/*.md` files are kept; the scaffold skips them

---

## Phase 2 — Confirm findings and gather guidelines

Present your findings and walk through each decision.

### 2a. Present findings

Show the user what you discovered as a formatted summary:

```
Here's what I found:

  Stack:        [language] / [framework] / [db] / [test framework]
  Format/Lint:  [formatter] / [linter]  (or "shared: <tool>" if same)
  Platform:     [GitHub | Azure DevOps | GitLab | Bitbucket | unknown]
  CI:           [GitHub Actions | Azure Pipelines | GitLab CI | none detected]
  Tracker:      [GitHub Issues | GitLab Issues | Azure DevOps | Jira | Linear | local markdown | none detected]
  Domain docs:  [single-context | multi-context (monorepo signals: …)]
  Legacy:       [CONTEXT.md files / agents-docs/ found at … | none]
  Duplicates:   [standalone skill folders / mattpocock-skills plugin found at … | none]
  CLAUDE.md:    [none | pointer to AGENTS.md only | has content (hides AGENTS.md)]
  Commits:      [Conventional Commits | ticket-prefixed | freeform | none detected]
  Hooks:        [Husky | pre-commit | lefthook | none detected]
  Subdomains:   [list of discovered subdomains]
```

Then use `AskUserQuestion` to confirm findings, the tracker and the triage labels in a single call. Lead each with the recommended answer. If the tracker was confidently detected, skip the tracker question; the plugin's skills were designed for GitHub, so propose it whenever the remote is GitHub (GitLab likewise).

```
questions:
  - question: "Does this look right, or should I correct anything?"
    header: "Findings"
    multiSelect: false
    options:
      - label: "Looks good (Recommended)"
        description: "Proceed with the detected stack, platform, and subdomains as shown above."
      - label: "Needs corrections"
        description: "I'll tell you what to fix before we continue."
  - question: "Where do you track issues / work items?"
    header: "Tracker"
    multiSelect: false
    options:
      - label: "GitHub Issues"
        description: "Issues tracked in GitHub, linked with #123 in commits and PRs."
      - label: "Azure DevOps"
        description: "Work items tracked in Azure Boards, linked with #123 in commits and attached to PRs (AB#123 from GitHub)."
      - label: "Jira"
        description: "Issues tracked in Jira, linked with PROJECT-123."
      - label: "Local markdown"
        description: "Specs and tickets as files under .scratch/<feature>/ in this repo. For repos without a tracker or remote."
  - question: "Keep the default triage labels (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix)?"
    header: "Labels"
    multiSelect: false
    options:
      - label: "Keep defaults (Recommended)"
        description: "/triage, /to-spec and /to-tickets apply these five strings."
      - label: "Use our own names"
        description: "I'll tell you which of our existing labels plays each role."
```

Adjust the four options to the likeliest trackers for this repo (with no git remote, lead with local markdown, and `--platform` is `generic`); GitLab, Linear and any other tracker are reachable through "Other". For a tracker with no template, ask the user to describe the workflow in one paragraph; you'll write `docs/agents/issue-tracker.md` from it.

If the user picks "Needs corrections" or "Use our own names", wait for their answer before continuing.

**GitHub or GitLab need a reachable repo.** When the user picks one and no `git remote` points at that host, get the repo URL from them and wire it up (`git init` if needed, `git remote add origin <url>`). Done when `gh repo view` / `glab repo view` prints the project from inside this directory; if it can't, stop and tell the user what's missing.

**Domain layout.** Default to single-context (one `GLOSSARY.md` + `docs/adr/` at the root) without asking. Only when Subagent B found monorepo signals, ask whether they want multi-context (a root `GLOSSARY-MAP.md` pointing at one `GLOSSARY.md` per context).

**Existing `CLAUDE.md`.** Settle this before Phase 3, so the scaffold no longer warns about it. No `CLAUDE.md` is created: Claude Code reads `AGENTS.md` natively, but only when no `CLAUDE.md` or `CLAUDE.local.md` exists. If one does:
- If it holds only a pointer to `AGENTS.md` (Mimas's old bridge line, or `@AGENTS.md`), remove it with `git rm` and say so.
- Otherwise offer to merge it into `AGENTS.md` and remove it (recommended): move an existing `## Agent skills` block (written by `setup-matt-pocock-skills`) into `AGENTS.md` as the single block, and move the rest under the matching `AGENTS.md` sections or into the doc it belongs in. If the user wants to keep `CLAUDE.md`, add an `@AGENTS.md` line to it instead and leave no `## Agent skills` block in it, so there is exactly one.
- `CLAUDE.local.md` is personal and usually gitignored: don't touch it, but tell the user it hides `AGENTS.md` unless it contains `@AGENTS.md`.

**Duplicate skills.** If Subagent C found any, list each path. Offer to remove the ones inside this repo with `git rm -r` (one yes for the lot). Never change anything outside the repo yourself: for folders under `~/.claude/skills/` and a `mattpocock-skills` plugin enabled in `~/.claude/settings.json`, give the user the exact command or setting to change, since they affect every project on the machine. Whatever stays, warn that it may trigger instead of the plugin's version.

**Legacy domain docs.** If `CONTEXT.md` / `CONTEXT-MAP.md` files or an `agents-docs/` tree exist, offer to migrate them, and do it only on a yes:
- `git mv` each `CONTEXT.md` to `GLOSSARY.md` and `CONTEXT-MAP.md` to a root `GLOSSARY-MAP.md`, then rewrite each into the `/domain-modeling` glossary format: the vocabulary becomes `## Language` entries (`**Term**:` definition, `_Avoid_:` aliases); cross-context relationships move to the map's `## Relationships`. Boundaries/IO and invariants are not glossary content: move them to the matching `docs/agents/features/<area>.md`, or show them to the user if no feature doc fits.
- `git mv` `agents-docs/adr/` to `docs/adr/`, and the other `agents-docs/` files to their `docs/agents/` counterparts, splitting `ENGINEERING.md`'s coding standards out into `CODING_STANDARDS.md`. Drop `AGENTS_CONTEXT.md` and `AGENTS_ADRS.md`: `docs/agents/domain.md` and `/domain-modeling` replace them.

### 2b. Org guidelines (optional)

Use `AskUserQuestion` to ask about org guidelines:

```
questions:
  - question: "Do you have coding guidelines or standards to include?"
    header: "Guidelines"
    multiSelect: false
    options:
      - label: "Skip"
        description: "No org-specific guidelines — use only the auto-detected conventions."
      - label: "Yes, I'll provide them"
        description: "I'll paste a file path, URL, or content to weave into CODING_STANDARDS.md and ENGINEERING.md."
```

If the user chooses to provide guidelines, wait for their input. Incorporate coding rules into `CODING_STANDARDS.md` and workflow rules (branching, commits, CI) into `ENGINEERING.md`. Don't dump it verbatim — integrate it naturally alongside the tech-stack-specific standards.

---

## Phase 3 — Scaffold verbatim files (script)

First finish the file changes agreed in Phase 2 — `CLAUDE.md`, duplicate skills, legacy migration — so the script sees the repo as it will be. Then run the scaffolding script to create all deterministic files. This saves tokens by avoiding LLM generation of verbatim content.

```bash
bash scripts/scaffold.sh --target <repo-root> --platform <platform> --tracker <tracker>
```

- `--platform` (`github`, `azure-devops`, `gitlab`, `bitbucket`, `generic`) picks the PR/MR section injected into `docs/agents/AGENT_WORKFLOW.md`.
- `--tracker` (`github`, `gitlab`, `local`, `azure-devops`, `jira`, `linear`, `other`) picks the template copied to `docs/agents/issue-tracker.md`. `other` copies nothing; you write the file in Phase 4.

The script creates:

| File | How |
|---|---|
| `docs/agents/issue-tracker.md` | Copied from `templates/issue-trackers/<tracker>.md` |
| `docs/agents/triage-labels.md` | Copied verbatim — triage role → label string table |
| `docs/agents/domain.md` | Copied verbatim — how skills read `GLOSSARY.md` and ADRs |
| `docs/agents/AGENT_WORKFLOW.md` | Composed from base template + platform PR/MR section |
| `docs/agents/AGENTS_FEATURES.md` | Copied verbatim — universal feature doc contract |
| `docs/agents/features/feature-template.md` | Copied verbatim — template for future feature docs |
| `docs/agents/LESSONS.md` | Copied verbatim — lessons-file format and one seeded example |

The script is idempotent — re-running skips existing files.

---

## Phase 4 — Generate project-specific files (LLM)

These files require LLM reasoning and cannot be scripted. Read the reference files before writing:
- `references/file-templates.md` — base template for each file
- `references/tech-adapters.md` — tech-stack-specific sections
- `references/platform-adapters.md` — CI/CD and issue linking sections for ENGINEERING.md

Replace every `{{placeholder}}` with what you actually discovered. The references use `{{DOCS_DIR}}` wherever the agent docs root path appears — substitute `docs/agents` for every occurrence as you write each file (or whatever value was passed to `--docs-dir` if it was overridden). Don't leave the placeholder in final output. Every generated file should read as if a senior engineer on this project wrote it.

### Files to generate

| File | Purpose |
|---|---|
| `/AGENTS.md` | Entry point — `## Agent skills` block, `## Modules`, links to docs, critical rules, completion checklist |
| `/CODING_STANDARDS.md` | Coding standards the review skills check against — testing, language, naming, errors, framework focus areas, DB, auth, AI |
| `docs/agents/ENGINEERING.md` | How to work here — setup, hooks, commands, CI/CD, issue linking, commit conventions |
| `docs/agents/FEATURES.md` | Feature area index (start minimal or empty) |
| `/GLOSSARY.md` | **Only if Phase 1 found clear domain terms** — otherwise created lazily later |
| `/GLOSSARY-MAP.md` | **Only if the user chose multi-context** — points to one lazily created `GLOSSARY.md` per context |
| `docs/agents/issue-tracker.md` | **Only for `--tracker other`** — written from the user's description, with the same sections as the templates: Conventions (including Blocking), "publish to the issue tracker", "fetch the relevant ticket", Wayfinding operations |

### Modules

Every subdomain Subagent B found gets one line in `AGENTS.md`'s `## Modules` section: its path and a one-line role. When the source root only groups packages (`src/` holding `orders/`, `billing/`), list each package (`src/orders/`), not the root. `agentic-review` and `review-policy-builder` derive one reviewer and one policy file per module from this list (or from `GLOSSARY-MAP.md` contexts when the repo is multi-context), so cover every top-level directory that holds product code, and don't go deeper than the top level of each subdomain.

### Glossary

Domain language lives in `GLOSSARY.md`, in the format the `/domain-modeling` skill defines (see `references/file-templates.md`). It is created lazily: write one now only if Phase 1 surfaced clear, project-specific domain terms, and only those terms. Don't invent entries and don't add general programming concepts. Never put agent rules (TDD, typecheck) or implementation detail (file paths, request schemas) in it; those belong in `AGENTS.md`, `CODING_STANDARDS.md` and `docs/agents/features/`. ADRs are not scaffolded at all: `docs/adr/` appears when the first decision is recorded.

### Feature index

`docs/agents/FEATURES.md` should start minimal. Only add entries if you found feature domains with **meaningful implementation** — not just a route stub or empty handler. Even when you add entries, only add index entries — do not create the `docs/agents/features/<area>.md` files themselves, and don't link to them yet: write each entry as `- <area> — <one-line description> (_not documented yet_)`. `find-features` / `document-features` turn them into links when they write the files.

### Platform-specific content in AGENTS.md and ENGINEERING.md

Weave platform content from `references/platform-adapters.md` into the files you generate:

- **`AGENTS.md` completion checklist**: add platform-specific items (PR opened, CI passing, issues linked)
- **`docs/agents/ENGINEERING.md`**: add CI/CD section and issue linking conventions

If no platform was detected and the user didn't specify one, omit platform-specific sections entirely — don't guess.

Note: `docs/agents/AGENT_WORKFLOW.md` is already handled by the script with the correct platform section.

### Where Phase-1 signals land

The discovery phase captures a few signals beyond stack and platform — make sure each one shows up in the right file:

- **Formatter and linter** (Subagent A): list both as distinct commands in the `docs/agents/ENGINEERING.md` commands section. If the project runs them as one script, say so; otherwise document each. Mention the formatter in the completion checklist alongside typecheck/tests.
- **Pre-commit hooks** (Subagent C): if hooks were found, document the framework and install step (`pre-commit install`, `lefthook install`, or "Husky installs automatically on `pnpm install`") in `docs/agents/ENGINEERING.md` under setup, and add a short note in `AGENTS.md` so agents know commits will be gated. Name what each hook runs so agents understand why a commit was rejected.
- **Commit conventions** (Subagent C): if a clear pattern was detected, document it in `docs/agents/ENGINEERING.md` (commit-message section) with one example matching the repo's actual style. If commits are inconsistent, omit this section rather than imposing Conventional Commits by default. A consistent pattern from fewer than ~10 commits is documented, with a note on the small sample.
- **Subdomains** (Subagent B): each detected subdomain gets a line in `AGENTS.md`'s `## Modules` section. Distinctive domain terms seen along the way are glossary candidates (see *Glossary* above).
- **Framework focus areas** (Subagent A): the matching "Focus areas" from `tech-adapters.md` go into `CODING_STANDARDS.md` as review checks.

### Tailor `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`

The other skills follow these two files literally, so they must be runnable as written:

- **Project settings**: the Azure DevOps, Jira and Linear templates open with a *Project settings* section of `[bracketed]` defaults. Replace each with the real value — organization and project from the remote URL, the work item type and done state of the process (Azure DevOps); the site and project key from commit messages (Jira); the team key (Linear). Ask the user for any you can't discover. GitHub, GitLab and local need no edits.
- **Check the tracker is reachable**: for Azure DevOps, run `az boards work-item show --id <any known id>` (it needs the `azure-devops` CLI extension and `az login`); for Jira or Linear, confirm their MCP tools are among your tools and fetch one known issue. If it fails, tell the user exactly what to install or connect: the other skills will hit the same wall.
- **Local markdown**: `.scratch/` is the tracker, so it is committed like any other doc. Don't gitignore it.
- **Triage labels**: if the user named their own labels, edit the "Label in our tracker" column to match.
- **Create missing labels**: on GitHub or GitLab, create each configured label the tracker lacks (`gh label create` / `glab label create`).

### Ignore worker worktrees

Add `.claude/worktrees/` to `.gitignore` (create the file if needed). `/orchestrate-spec` runs each worker in a worktree there, and they must not show up as untracked files.

### Write the `## Agent skills` block

The block in `AGENTS.md` (see `references/file-templates.md`) is how the other skills find the tracker, the labels and the domain docs — they expect it in context, not at a fixed path. Fill each one-line summary from what was confirmed in Phase 2. Claude Code, Codex and other agents load `AGENTS.md` at session start (Claude Code only while there is no `CLAUDE.md` — see *Existing `CLAUDE.md`* in Phase 2), and Claude Code passes it on to subagents.

### Tailor the seeded `docs/agents/LESSONS.md` example

The scaffold script copies `docs/agents/LESSONS.md` verbatim, and the seeded example uses `npx tsc --noEmit` as a placeholder typecheck command. After the script runs, edit the example so it matches this project's actual typecheck command:

- **TypeScript** → leave `npx tsc --noEmit` (or substitute the exact script from `package.json`, e.g. `pnpm typecheck`)
- **Python (mypy)** → swap to `mypy .` (or the project's exact invocation)
- **Python (pyright)** → swap to `pyright`
- **Go** → swap to `go vet ./...`
- **Rust** → swap to `cargo check` or `cargo clippy`
- **No static typing** → replace the example entirely with a stack-appropriate verification step (e.g. for a JS project: "Run the project's lint command and confirm exit 0 before any 'done' claim."; for Python without mypy/pyright: "Run `make test` (or the test command) and the linter, and confirm both exit 0")

Update the example's title, trigger, rule, and example block to match — the whole point is that an agent reading the seeded example sees a real, runnable command from *this* repo. A wrong-stack example is worse than no example.

---

## What makes a good output

**Specific, not generic.** If the repo uses Vitest, write "Vitest" — not "your test framework". If type checking is `npx tsc --noEmit`, write exactly that.

**Use the actual project name.** Refer to the project by the name you found in README, package.json, or go.mod — not a name you inferred or invented.

**Accurate commands.** Test, typecheck, dev server, build, and setup commands must be correct and copy-pasteable.

**Proportionate.** Don't add a "Database guidelines" section to a frontend-only repo. Don't add "TypeScript standards" to a Python project. Only include what applies. The templates are written with a web service in mind: for a library, CLI or job, reword "API contracts", "endpoints" and "routes" into what this repo actually exposes.

**Opinionated where it matters.** These rules are always included regardless of stack:
- TDD (red-green-refactor) is mandatory, driven by `/tdd`
- Plan mode for non-trivial tasks
- Verification before marking work done
- Self-improvement loop (lessons learned)
- Feature documentation contract

**Keep root AGENTS.md lean.** It is pushed into every agent's context, so it holds navigation pointers plus the most critical non-negotiable rules. Detail lives in the docs it points to; coding standards live in `CODING_STANDARDS.md`, which is read during review, not implementation.

---

## After generating

Tell the user:
1. Which files were created (full list with paths)
2. Which modules were listed in `AGENTS.md`, and whether a glossary was written
3. Which platform/tracker was used, and which labels were created
4. Any tech stack details you were uncertain about — be honest about gaps
5. What they should review and customize before committing

Then name what reads these files now — `/to-spec`, `/to-tickets`, `/triage`, `/wayfinder` and `/orchestrate-spec` use the tracker; `/grill-with-docs` and `/domain-modeling` grow the glossary and ADRs; `/code-review` checks against `CODING_STANDARDS.md` — and recommend the optional next steps:

> - **Review policies:** run `/review-policy-builder` to write module-scoped and machine-checkable review rules under `docs/agents/review/policies/`. Once they exist, `/code-review` reads them and `/agentic-review` runs one reviewer per module against them.
> - **Feature docs:** `docs/agents/features/` starts empty. The Mimas `find-features` and `document-features` skills (installed separately from https://github.com/Grade-AI-Labs/Mimas) fill it.

Ask the user to review the generated files before committing.
