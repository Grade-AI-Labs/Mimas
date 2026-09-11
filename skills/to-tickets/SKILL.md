---
name: to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges. Asks whether to publish to an issue tracker (native blocking links); if the user declines or no tracker is available, falls back to one local markdown file per ticket in the OS temp directory.
disable-model-invocation: true
metadata:
  author: Olof Brogeby & Matt Pocock
  url: https://github.com/brogeby
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

## Output destination

Settle this **before** drafting, so you know what shape the blocking edges take. Tickets always get written somewhere; the only question is where.

### First, ask whether to publish

Ask first — never assume, and never publish to a tracker the user hasn't agreed to:

> Do you want these tickets published to an issue tracker, or written as local markdown files in your OS temp directory?

### If they want them published, find the tracker

Look in the agent instructions you were given — `AGENTS.md`, `CLAUDE.md`, or whichever instruction files this project uses — plus any tracker configuration they point to, for a named tracker. It counts as available only if you can both *name* it (GitHub, Linear, Jira, …) and *reach* it with the tools you have.

- **Available** → the **real issue tracker** form in step 5.
- **Not available** → say so plainly, naming where you looked, and fall back to the **local files** form. Don't stall on it. If the user names a tracker or points you at its configuration on the spot, use that instead, and offer to record it in the project's agent instructions so the next session doesn't have to ask.

### If they decline, or no tracker is available

Use the **local files** form in step 5: one markdown file per ticket in the OS temp directory. This is the fallback in every case where publishing is either unwanted or impossible — never leave approved tickets unwritten.

Carry the answer through to step 5.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the tickets

Write the approved tickets to the destination settled in **Output destination**. The tickets are the same either way; only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under the OS temp directory, in `<os-temp-dir>/<feature-slug>/issues/<NN>-<slug>.md` — not in the workspace. Resolve `<os-temp-dir>` from the environment rather than hardcoding it (`$TMPDIR` on macOS, `$TMPDIR` or `/tmp` on Linux, `%TEMP%` on Windows). Number from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file. When done, list the absolute paths you wrote, and warn the user that the OS may clear the temp directory, so anything worth keeping should be moved or pushed to a tracker.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking / sub-issue relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. Apply whatever labelling convention the project's agent instructions document; if they document none, apply none.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None (can start immediately)".

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)".

</issue-template>

In either form, avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.
