---
name: setup-mimas-template
description: Scaffold the Mimas agent instruction file tree for any repository — AGENTS.md at root, subdomain AGENTS.md files, and the full docs/ hierarchy. Every file is tailored to the repo's actual tech stack, git platform, and conventions. Use this skill whenever someone wants to set up agent instructions, onboard a repo for AI-assisted development, add AGENTS.md files, create engineering docs for agents, or mentions "mimas template". Even if they just say "set up this repo for agents" or "add agent docs", this is the skill to use.
metadata:
  author: Olof Brogeby
  url: https://github.com/brogeby
---

# setup-mimas-template

You are scaffolding a set of instruction files that AI agents read at the start of every session to understand how to work on a project. The output is a complete, project-specific instruction tree — not a generic template dump.

---

## Phase 1 — Automated Discovery

Explore before writing anything. **Launch three subagents in parallel** to maximize speed — each handles an independent research task. Collect their results before proceeding.

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

**Subagent C — Git platform, CI/CD, hooks & existing files.** Read `.git/config`, check for CI and hook config files, sample recent commits, and scan existing docs:

- Git platform from remote URL: `github.com` → GitHub, `dev.azure.com` / `visualstudio.com` → Azure DevOps, `gitlab.com` → GitLab, `bitbucket.org` → Bitbucket
- CI/CD: `.github/workflows/` → GitHub Actions, `azure-pipelines.yml` → Azure Pipelines, `.gitlab-ci.yml` → GitLab CI
- **Pre-commit hooks**: check for `.husky/`, `.pre-commit-config.yaml`, `lefthook.yml`/`lefthook.yaml`, `.git/hooks/` with non-sample files. If found, report which framework is in use and what each hook runs (open the config and summarize) — agents need to know these will block their commits, and the setup section must include the install step (`pnpm install` runs Husky's prepare script, `pre-commit install`, `lefthook install`, etc.).
- **Commit message conventions**: run `git log -n 100 --pretty=%s` and report patterns you observe:
  - Conventional Commits prefixes (`feat:`, `fix:`, `chore:`, scopes like `feat(api):`)
  - Ticket-key prefixes/suffixes (`AB#123`, `PROJ-456`, `#789`) — this confirms or overrides the platform-based tracker guess
  - Imperative vs. past tense, line-length norms, anything else consistent across 10+ commits
  - If commits are inconsistent or the repo has fewer than ~10 commits, say so — don't invent a convention
- Issue tracker hints from those same commit messages (`#123` → GitHub Issues, `AB#456` → Azure DevOps, `PROJ-789` → Jira/Linear)
- Whether `CLAUDE.md`, `AGENTS.md`, or `README.md` exist and have meaningful content (report a brief summary of what they contain)

### After subagents return

Combine the three reports into a unified picture. If any subagent couldn't determine something (e.g., no database found, no CI detected), that's fine — note it as "not detected" and move on.

For existing files:
- Pull project description from README into root `AGENTS.md` intro
- Incorporate documented conventions into `ENGINEERING.md`
- If an existing `AGENTS.md` or `CLAUDE.md` is empty or placeholder, replace it
- If there is a populated `CLAUDE.md`, keep it — it serves a different purpose

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
  Tracker:      [GitHub Issues | Azure DevOps | Jira | Linear | none detected]
  Commits:      [Conventional Commits | ticket-prefixed | freeform | none detected]
  Hooks:        [Husky | pre-commit | lefthook | none detected]
  Subdomains:   [list of discovered subdomains]
```

Then use `AskUserQuestion` to confirm and ask about work tracking in a single call. If the tracker was confidently detected, skip the tracker question. You can ask up to 4 questions per call — batch what makes sense.

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
        description: "Work items tracked in Azure DevOps, linked with AB#123."
      - label: "Jira"
        description: "Issues tracked in Jira, linked with PROJECT-123."
      - label: "Linear"
        description: "Issues tracked in Linear, linked with TEAM-123."
```

If the user picks "Needs corrections", wait for their corrections before continuing.

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
        description: "I'll paste a file path, URL, or content to weave into ENGINEERING.md."
```

If the user chooses to provide guidelines, wait for their input. Incorporate it into the relevant sections of `ENGINEERING.md` (coding standards, naming conventions, review practices, etc.). Don't dump it verbatim — integrate it naturally alongside the tech-stack-specific standards.

---

## Phase 3 — Scaffold verbatim files (script)

Run the scaffolding script to create all deterministic files — directories, universal templates, composed AGENT_WORKFLOW.md, and the CLAUDE.md bridge file. This saves tokens by avoiding LLM generation of verbatim content.

```bash
bash scripts/scaffold.sh --target <repo-root> --platform <platform>
```

The `--platform` flag determines which PR/MR workflow section is injected into `docs/AGENT_WORKFLOW.md`.

The script creates:

| File | How |
|---|---|
| `CLAUDE.md` | Created (or appended if exists) — points Claude to AGENTS.md |
| `docs/AGENT_WORKFLOW.md` | Composed from base template + platform PR/MR section |
| `docs/AGENTS_FEATURES.md` | Copied verbatim — universal feature doc contract |
| `docs/features/feature-template.md` | Copied verbatim — template for future feature docs |
| `docs/LESSONS.md` | Copied verbatim — lessons-file format and one seeded example, so agents have a populated file to append to (empty files get ignored) |

The script is idempotent — re-running skips existing files.

### Available scripts

- **`scripts/scaffold.sh`** — Scaffolds verbatim files and composes AGENT_WORKFLOW.md

---

## Phase 4 — Generate project-specific files (LLM)

These files require LLM reasoning and cannot be scripted. Read the reference files before writing:
- `references/file-templates.md` — base template for each file
- `references/tech-adapters.md` — tech-stack-specific sections
- `references/platform-adapters.md` — CI/CD and issue linking sections for ENGINEERING.md

Replace every `{{placeholder}}` with what you actually discovered. Every generated file should read as if a senior engineer on this project wrote it.

### Files to generate

| File | Purpose |
|---|---|
| `/AGENTS.md` | Entry point — links to docs, critical rules, completion checklist |
| `docs/ENGINEERING.md` | Engineering standards — testing, language, naming, DB, auth, CI/CD, commands |
| `docs/FEATURES.md` | Feature area index (start minimal or empty) |
| `<subdomain>/AGENTS.md` | One per discovered subdomain — scope and focus for that area |

### Subdomain AGENTS.md rules

Create one `AGENTS.md` at the **top level** of each subdomain — not deeper:

- `src/` → `src/AGENTS.md` (not `src/routes/AGENTS.md`)
- `internal/` → `internal/AGENTS.md` (not `internal/handlers/AGENTS.md`)
- `packages/auth/` → `packages/auth/AGENTS.md`
- `frontend/` → `frontend/AGENTS.md`

Each subdomain AGENTS.md covers everything within its subtree. Don't create them for utility folders, config dirs, or generated output.

### Feature index

`docs/FEATURES.md` should start minimal. Only add entries if you found feature domains with **meaningful implementation** — not just a route stub or empty handler. Even when you add entries, only add index entries — do not create the `docs/features/<area>.md` files themselves.

### Platform-specific content in AGENTS.md and ENGINEERING.md

Weave platform content from `references/platform-adapters.md` into the files you generate:

- **`AGENTS.md` completion checklist**: add platform-specific items (PR opened, CI passing, issues linked)
- **`docs/ENGINEERING.md`**: add CI/CD section and issue linking conventions

If no platform was detected and the user didn't specify one, omit platform-specific sections entirely — don't guess.

Note: `docs/AGENT_WORKFLOW.md` is already handled by the script with the correct platform section.

### Where Phase-1 signals land

The discovery phase captures a few signals beyond stack and platform — make sure each one shows up in the right file:

- **Formatter and linter** (Subagent A): list both as distinct commands in the `docs/ENGINEERING.md` commands section. If the project runs them as one script, say so; otherwise document each. Mention the formatter in the completion checklist alongside typecheck/tests.
- **Pre-commit hooks** (Subagent C): if hooks were found, document the framework and install step (`pre-commit install`, `lefthook install`, or "Husky installs automatically on `pnpm install`") in `docs/ENGINEERING.md` under setup, and add a short note in `AGENTS.md` so agents know commits will be gated. Name what each hook runs so agents understand why a commit was rejected.
- **Commit conventions** (Subagent C): if a clear pattern was detected, document it in `docs/ENGINEERING.md` (commit-message section) with one example matching the repo's actual style. If commits are inconsistent or too few to draw a pattern from, omit this section rather than imposing Conventional Commits by default.

### Tailor the seeded `docs/LESSONS.md` example

The scaffold script copies `docs/LESSONS.md` verbatim, and the seeded example uses `npx tsc --noEmit` as a placeholder typecheck command. After the script runs, edit the example so it matches this project's actual typecheck command:

- **TypeScript** → leave `npx tsc --noEmit` (or substitute the exact script from `package.json`, e.g. `pnpm typecheck`)
- **Python (mypy)** → swap to `mypy .` (or the project's exact invocation)
- **Python (pyright)** → swap to `pyright`
- **Go** → swap to `go vet ./...`
- **Rust** → swap to `cargo check` or `cargo clippy`
- **No static typing** → replace the example entirely with a stack-appropriate verification step (e.g. for a JS project: "Run the project's lint command and confirm exit 0 before any 'done' claim.")

Update the example's title, trigger, rule, and example block to match — the whole point is that an agent reading the seeded example sees a real, runnable command from *this* repo. A wrong-stack example is worse than no example.

---

## What makes a good output

**Specific, not generic.** If the repo uses Vitest, write "Vitest" — not "your test framework". If type checking is `npx tsc --noEmit`, write exactly that.

**Use the actual project name.** Refer to the project by the name you found in README, package.json, or go.mod — not a name you inferred or invented.

**Accurate commands.** Test, typecheck, dev server, build, and setup commands must be correct and copy-pasteable.

**Proportionate.** Don't add a "Database guidelines" section to a frontend-only repo. Don't add "TypeScript standards" to a Python project. Only include what applies.

**Opinionated where it matters.** These rules are always included regardless of stack:
- TDD (red-green-refactor) is mandatory
- Plan mode for non-trivial tasks
- Verification before marking work done
- Self-improvement loop (lessons learned)
- Feature documentation contract

**Keep root AGENTS.md lean.** It is an index plus the most critical non-negotiable rules. Detail lives in the docs it points to.

---

## After generating

Tell the user:
1. Which files were created (full list with paths)
2. Which subdomains were detected and got their own AGENTS.md
3. Which platform/tracker was used for platform-specific content
4. Any tech stack details you were uncertain about — be honest about gaps
5. What they should review and customize before committing

Then recommend the follow-up workflow that populates the empty `docs/features/` tree this scaffold creates:

> **Recommended next step: populate your feature docs.**
>
> The scaffold leaves `docs/features/` empty by design. The fastest way to fill it is two skills from the Mimas repo, run back-to-back in fresh sessions:
>
> 1. **`find-features`** — scans the codebase, identifies meaningful feature areas, and adds them to `docs/FEATURES.md`.
> 2. **`document-feature`** — guided walkthrough that turns each identified area into a populated `docs/features/<area>.md` from the template.
>
> Both skills (and others worth browsing) live at [https://github.com/Grade-AI-Labs/Mimas](https://github.com/Grade-AI-Labs/Mimas). Install them, run `find-features` first, then loop `document-feature` over what it found.
>
> Once that's done, review the generated files and commit.
