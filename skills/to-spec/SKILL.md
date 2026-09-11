---
name: to-spec
description: "Turn the current conversation into a spec: no interview, just synthesis of what you've already discussed. Asks whether to publish it to an issue tracker; if the user declines or no tracker is available, falls back to a local markdown file in the OS temp directory."
disable-model-invocation: true
metadata:
  author: Olof Brogeby & Matt Pocock
  url: https://github.com/brogeby
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

## Output destination

Settle this **before** writing the spec. The spec always gets written somewhere; the only question is where.

### First, ask whether to publish

Ask first — never assume, and never publish to a tracker the user hasn't agreed to:

> Do you want this spec published to an issue tracker, or written as a local markdown file in your OS temp directory?

### If they want it published, find the tracker

Look in the agent instructions you were given — `AGENTS.md`, `CLAUDE.md`, or whichever instruction files this project uses — plus any tracker configuration they point to, for a named tracker and its triage label vocabulary. It counts as available only if you can both *name* it (GitHub, Linear, Jira, …) and *reach* it with the tools you have.

- **Available** → publish the spec as an issue there, applying the `ready-for-agent` triage label; no need for additional triage.
- **Not available** → say so plainly, naming where you looked, and fall back to the local file. Don't stall on it. If the user names a tracker or points you at its configuration on the spot, use that instead, and offer to record it in the project's agent instructions so the next session doesn't have to ask.

### If they decline, or no tracker is available

Write the spec to `<os-temp-dir>/<feature-slug>/spec.md` — in the OS temp directory, not in the workspace. Resolve `<os-temp-dir>` from the environment rather than hardcoding it (`$TMPDIR` on macOS, `$TMPDIR` or `/tmp` on Linux, `%TEMP%` on Windows). Report the absolute path you wrote, and warn the user that the OS may clear the temp directory, so anything worth keeping should be moved or pushed to a tracker.

This is the fallback in every case where publishing is either unwanted or impossible — never leave a finished spec unwritten.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Check with the user that these seams match their expectations.

3. Write the spec using the template below, then write it to the destination settled in **Output destination**. The spec content is the same either way.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
