# Issue tracker: Linear

Issues and specs for this repo live as Linear issues. Use the Linear MCP tools when they are connected; if they are not, tell the user and ask them to connect them rather than guessing at another route.

## Project settings

- **Team key**: `[TEAM]`.
- **Done state**: `[Done]`.

## Conventions

- **Create an issue**: create it in the team above with a title and a Markdown description.
- **Read an issue**: fetch it with its description, labels, state, relations and comments.
- **List issues**: list the team's issues, filtered by state and label.
- **Make an issue a sub-issue of a parent**: set the child's parent to the parent issue.
- **Blocking**: a "blocks" relation from the blocker to the blocked issue. A ticket is unblocked when every issue blocking it is done.
- **Count open blockers**: read the issue's relations and count the issues blocking it that are not done (0 means startable).
- **Comment on an issue**: add a comment.
- **Apply / remove labels**: update the issue's labels.
- **Close**: post the explanation as a comment, then move the issue to the done state.

## Pull requests as a triage surface

**PRs as a request surface: no.** Pull requests are not triaged as requests.

## When a skill says "publish to the issue tracker"

Create a Linear issue in the team above.

## When a skill says "fetch the relevant ticket"

Read it as in **Read an issue** above, comments included.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **sub-issues** as tickets.

- **Map**: an issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body.
- **Child ticket**: a sub-issue of the map, labelled `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, it is assigned to the driving dev.
- **Blocking**: see **Blocking** under Conventions.
- **Frontier query**: list the map's open, unassigned sub-issues and drop any with an open blocker (see **Count open blockers**); first in map order wins.
- **Claim**: assign the issue to yourself, the session's first write.
- **Resolve**: comment the answer, move it to done, then append a context pointer (gist + link) to the map's Decisions-so-far.
