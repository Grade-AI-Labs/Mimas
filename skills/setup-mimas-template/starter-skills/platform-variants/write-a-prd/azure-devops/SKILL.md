---
name: write-a-prd
description: Create a PRD through user interview, codebase exploration, and module design, then submit as an Azure DevOps Work Item. Use when user wants to write a PRD, create a product requirements document, or plan a new feature.
---

# Write a PRD

Create a product requirements document through structured interview, then submit it as an Azure DevOps User Story.

## Process

1. **Problem description.** Ask the user for a detailed description of the problem they want to solve and any ideas for solutions.

2. **Codebase exploration.** Explore the repo to verify their assertions and understand the current state.

3. **Interview.** Grill the user about every aspect of the plan until you reach shared understanding. Walk down each branch of the design tree, resolving dependencies one-by-one. Ask questions one at a time. If a question can be answered by exploring the codebase, explore instead of asking.

4. **Module design.** Sketch out the major modules to build or modify. Look for opportunities to extract deep modules — modules that encapsulate significant functionality behind a simple, testable interface. Check with the user that the modules match their expectations and which ones need tests.

5. **Write the PRD** using the template below.

6. **Submit as an Azure DevOps User Story.**

## PRD Template

```markdown
## Problem Statement

The problem from the user's perspective.

## Solution

The solution from the user's perspective.

## User Stories

1. As a <actor>, I want <feature>, so that <benefit>

(Extensive list covering all aspects of the feature.)

## Implementation Decisions

- Modules to build/modify and their interfaces
- Architectural decisions
- Schema changes
- API contracts

Do NOT include specific file paths or code snippets — they become outdated quickly.

## Testing Decisions

- What makes a good test (test external behavior, not implementation details)
- Which modules will be tested
- Prior art for tests in the codebase

## Out of Scope

What is explicitly not covered by this PRD.

## Further Notes

Any additional context.
```

## Submitting to Azure DevOps

After writing the PRD, submit it as a User Story using the Azure DevOps MCP tool (`mcp__azure-devops__wit_create_work_item`) or equivalent:

- **Work item type**: `User Story`
- **Title**: A concise description of the feature
- **State**: `Active`
- **Description**: The full PRD content formatted as HTML. Use `<h2>` for section headings and `<p>` / `<ul>` / `<ol>` for body content.
- **Area path**: Ask the user which board/area to file it under. If they don't have a preference, use the project root.
- Ask the user for the project name if you can't determine it from the repo context
