# Issue tracker: Jira

Issues and specs for this repo live as Jira issues. Use the Atlassian (Jira) MCP tools when they are connected; if they are not, tell the user and ask them to connect them rather than guessing at another route.

## Project settings

- **Site / project key**: `[<site>.atlassian.net]` / `[PROJ]`.
- **Issue type for specs**: `[Story]`. **For tickets**: `[Story]`, or `[Sub-task]` when tickets should sit under the spec.
- **Done status**: `[Done]`.

## Conventions

- **Create an issue**: create it in the project above with a summary and description. Use Markdown in the description unless the tool asks for another format.
- **Read an issue**: fetch it with its description, labels, status, links and comments.
- **List issues**: search with JQL, for example `project = PROJ AND statusCategory != Done AND labels = ready-for-agent ORDER BY created`.
- **Make an issue a child of a parent**: set the child's `parent` field to the parent's key when creating it (a sub-task, or a child of an epic).
- **Blocking**: a `Blocks` issue link from the blocker to the blocked issue. A ticket is unblocked when every issue that blocks it is done.
- **Count open blockers**: read the issue's links and count the inward `is blocked by` links whose issue is not in the done status category (0 means startable).
- **Comment on an issue**: add a comment.
- **Apply / remove labels**: edit the issue's `labels` field. Jira labels cannot contain spaces.
- **Close**: post the explanation as a comment, then transition the issue to the done status. List its transitions first; the transition name is not always the status name.

## Pull requests as a triage surface

**PRs as a request surface: no.** Pull requests are not triaged as requests.

## When a skill says "publish to the issue tracker"

Create a Jira issue in the project above.

## When a skill says "fetch the relevant ticket"

Read it as in **Read an issue** above, comments included.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets.

- **Map**: an issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body.
- **Child ticket**: an issue whose `parent` is the map, labelled `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, it is assigned to the driving dev.
- **Blocking**: see **Blocking** under Conventions.
- **Frontier query**: JQL `parent = <map> AND statusCategory != Done AND assignee IS EMPTY`, then drop any with an open blocker (see **Count open blockers**); first in map order wins.
- **Claim**: assign the issue to yourself, the session's first write.
- **Resolve**: comment the answer, transition to done, then append a context pointer (gist + link) to the map's Decisions-so-far.
