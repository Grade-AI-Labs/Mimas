# Platform Adapters

Building blocks for platform-specific sections in generated files. Pick the adapters matching the detected (and user-confirmed) git platform and issue tracker. Same pattern as `tech-adapters.md` — combine and customize, don't copy blindly.

---

## Git Platforms

### GitHub

**Detection:** remote URL contains `github.com`

AGENT_WORKFLOW.md — Pull Requests section:
```
### Pull Requests

- Create a feature branch for every change: `<type>/<short-description>` (e.g. `feat/add-retry-logic`, `fix/null-pointer-webhook`)
- Open a PR via `gh pr create` — include a summary and test plan
- Link issues in the PR body with `Fixes #<number>` for auto-close or `Relates to #<number>` for reference
- Request review if the repo has CODEOWNERS configured
- After merge, delete the feature branch
```

AGENTS.md completion checklist additions:
```
- [ ] PR opened with summary and linked issues
- [ ] CI checks passing
```

ENGINEERING.md — CI/CD section:
```
## CI/CD

- CI runs via GitHub Actions — workflow files in `.github/workflows/`
- Check workflow status: `gh run list`, `gh run view <id>`
- All workflow checks must pass before merging PRs
```

### Azure DevOps

**Detection:** remote URL contains `dev.azure.com` or `visualstudio.com`

AGENT_WORKFLOW.md — Pull Requests section:
```
### Pull Requests

- Create a feature branch for every change: `<type>/<short-description>` (e.g. `feat/add-retry-logic`, `fix/null-pointer-webhook`)
- Open a PR in Azure DevOps — include a summary and test plan
- Link the work item as the linking section of `ENGINEERING.md` describes; `AB#<id>` only works from GitHub and does nothing in Azure Repos
- Ensure all build validation policies pass
- After merge, delete the feature branch
```

AGENTS.md completion checklist additions:
```
- [ ] PR opened with summary and the work item linked
- [ ] Build policies passing
```

ENGINEERING.md — CI/CD section:
```
## CI/CD

- CI runs via Azure Pipelines — config in `azure-pipelines.yml`
- Build validation policies enforce CI on PRs
- Check pipeline status in Azure DevOps
```

### GitLab

**Detection:** remote URL contains `gitlab.com` or self-hosted GitLab instance

AGENT_WORKFLOW.md — Merge Requests section:
```
### Merge Requests

- Create a feature branch for every change: `<type>/<short-description>`
- Open an MR — include a summary and test plan
- Reference issues with `Closes #<number>` for auto-close or `Relates to #<number>`
- Ensure all pipeline stages pass
- After merge, delete the feature branch
```

AGENTS.md completion checklist additions:
```
- [ ] MR opened with summary and linked issues
- [ ] Pipeline passing
```

ENGINEERING.md — CI/CD section:
```
## CI/CD

- CI runs via GitLab CI — config in `.gitlab-ci.yml`
- All pipeline stages must pass before merging MRs
- Check pipeline status in the merge request pipeline tab
```

### Bitbucket

**Detection:** remote URL contains `bitbucket.org`

AGENT_WORKFLOW.md — Pull Requests section:
```
### Pull Requests

- Create a feature branch for every change: `<type>/<short-description>`
- Open a PR — include a summary and test plan
- Reference Jira issues in the PR description if applicable
- Ensure all build checks pass
- After merge, delete the feature branch
```

AGENTS.md completion checklist additions:
```
- [ ] PR opened with summary
- [ ] Build checks passing
```

ENGINEERING.md — CI/CD section:
```
## CI/CD

- CI runs via Bitbucket Pipelines — config in `bitbucket-pipelines.yml`
- All pipeline steps must pass before merging PRs
```

---

## Issue / Work Trackers

### GitHub Issues

**Detection:** platform is GitHub and no external tracker configured

ENGINEERING.md — Issue linking section:
```
## Issue linking

- Reference issues in commits and PRs: `Fixes #123`, `Relates to #123`
- Use `Fixes` to auto-close on merge; use `Relates to` for cross-references
- Create issues via `gh issue create`
```

### Azure DevOps Work Items

**Detection:** platform is Azure DevOps, or commit messages contain `AB#` pattern

ENGINEERING.md — Work item linking section:
```
## Work item linking

- Azure Repos: start commit messages with `#<id>` to link the commit, and attach the work item to the PR (`az repos pr create --work-items <id>`, or the Work Items section in the UI)
- GitHub repos connected to Azure Boards: reference the work item as `AB#<id>` in commits and PRs; `AB#<id>` does nothing in Azure Repos
```

### Jira

**Detection:** commit messages contain `[A-Z]+-\d+` pattern (e.g. `PROJ-123`)

ENGINEERING.md — Issue linking section:
```
## Issue linking

- Put the Jira key in the branch name and at the start of commit messages and the PR title (`PROJECT-123 Add retry logic`); Jira's development integrations link each of them by the key in its own text
- Use smart commits for transitions where configured: `PROJECT-123 #done`
- Include issue keys in PR descriptions for traceability
```

### Linear

**Detection:** commit messages contain Linear-style identifiers, or `.linear` config present

ENGINEERING.md — Issue linking section:
```
## Issue linking

- Reference Linear issues in commits and PR descriptions: `TEAM-123`
- Linear auto-links issues when the identifier appears in commit messages or branch names
- Branch naming for auto-link: `team-123-short-description`
```

### No tracker / Local

```
## Task tracking

- No external issue tracker configured
- Track work in whatever lightweight format suits the session (TodoWrite, scratchpad, etc.) — no shared convention
```
