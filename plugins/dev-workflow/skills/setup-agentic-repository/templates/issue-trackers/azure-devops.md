# Issue tracker: Azure DevOps

Issues and specs for this repo live as Azure Boards work items. Use the `az boards` CLI (the `azure-devops` extension of the Azure CLI) for all operations.

## Project settings

- **Organization / project**: `[https://dev.azure.com/<org>]` / `[<project>]`. Set them once with `az devops configure --defaults organization=<url> project=<project>`, so the commands below need no `--org` / `--project`.
- **Work item type for specs and tickets**: `[User Story]` (`Product Backlog Item` in Scrum, `Issue` in Basic).
- **Done state**: `[Closed]` (`Done` in Scrum and Basic).

## Conventions

- **Create a work item**: `az boards work-item create --type "<type>" --title "..." --description "..."`. The description is HTML: wrap paragraphs in `<p>`, lists in `<ul><li>`.
- **Read a work item**: `az boards work-item show --id <id> --expand relations`. Comments are not included; read them with `az devops invoke --area wit --resource comments --route-parameters project=<project> workItemId=<id> --api-version 7.1-preview` (write the version exactly like that: `7.1-preview.4` crashes the CLI). If `invoke` still fails, `show` gives the latest comment in `System.History`; say that older comments weren't read.
- **List work items**: `az boards query --wiql "SELECT [System.Id], [System.Title], [System.State], [System.Tags] FROM workitems WHERE [System.TeamProject] = '<project>' AND [System.State] <> '<done state>'"`, adding `AND [System.Tags] CONTAINS '<label>'` to filter by label. Write the project name out: `@project` silently returns nothing from the CLI.
- **Make a work item a child of a parent**: `az boards work-item relation add --id <child> --relation-type parent --target-id <parent>`.
- **Blocking**: a Predecessor link from the blocked item to its blocker: `az boards work-item relation add --id <blocked> --relation-type predecessor --target-id <blocker>`. A ticket is unblocked when every predecessor is in the done state.
- **Count open blockers**: read the item with `--expand relations`, take the targets of its `System.LinkTypes.Dependency-Reverse` (Predecessor) relations, and count those not in the done state (0 means startable).
- **Comment on a work item**: `az boards work-item update --id <id> --discussion "..."`.
- **Apply / remove labels**: labels are tags. `--fields "System.Tags=..."` replaces the whole set, so read the current tags first, then write them back with the label added or removed: `az boards work-item update --id <id> --fields "System.Tags=needs-triage; backend"`.
- **Close**: post the explanation with `--discussion`, then `az boards work-item update --id <id> --state "<done state>"`.

## Pull requests as a triage surface

**PRs as a request surface: no.** Azure Repos pull requests are not triaged as requests.

## When a skill says "publish to the issue tracker"

Create a work item of the type above.

## When a skill says "fetch the relevant ticket"

Read it as in **Read a work item** above, comments included.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single work item with **child** work items as tickets.

- **Map**: a work item tagged `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body.
- **Child ticket**: a work item linked to the map as its child (see **Make a work item a child of a parent**), tagged `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, it is assigned to the driving dev.
- **Blocking**: see **Blocking** under Conventions.
- **Frontier query**: read the map with `--expand relations`, take its open children, drop any with an open blocker (see **Count open blockers**) or an assignee; first in map order wins.
- **Claim**: `az boards work-item update --id <id> --assigned-to "<your email>"`, the session's first write.
- **Resolve**: post the answer with `--discussion`, move the item to the done state, then append a context pointer (gist + link) to the map's Decisions-so-far.
