---
name: document-feature
description: Guided walkthrough to create or update a feature doc under docs/features/ using the project's feature template. Use when user wants to document a feature, create a feature doc, or says "document feature" or "add feature docs".
---

# Document Feature

Walk the user through creating or updating a `docs/features/<slug>.md` file, using the project's feature template as a starting point.

## Process

1. **Identify the feature.** Ask the user which feature area to document. If they're vague, explore the codebase to suggest candidates — look for route handlers, service modules, or domain logic that aren't yet documented under `docs/features/`.

2. **Read the template.** Read `docs/features/feature-template.md` to understand the expected structure.

3. **Read the existing doc** (if updating). If `docs/features/<slug>.md` already exists, read it first.

4. **Explore the implementation.** Use subagents to explore the codebase in parallel:
   - API endpoints / route definitions related to this feature
   - Service layer and business logic
   - Database models, migrations, or queries
   - Test files covering this feature
   - Configuration and environment variables
   - Error handling patterns

5. **Draft the doc.** Fill in every section of the template that applies to this feature. **Delete sections that don't apply** rather than leaving them empty. A frontend feature won't need "Rate Limiting"; a utility library won't need "API Endpoint".

6. **Review with the user.** Present the draft and ask:
   - Does this accurately describe the feature?
   - Anything missing or incorrect?
   - Any sections that should be expanded?

7. **Write the file.** Save to `docs/features/<slug>.md`.

8. **Update the index.** If this is a new feature area, add an entry to `docs/FEATURES.md` (alphabetical order).

## Rules

- Populate from the actual codebase — don't invent or assume behavior
- Use the project's naming conventions for paths and identifiers
- Keep the overview section concept-first, not code-first
- Include real request/response examples from the code, not hypothetical ones
- If you can't determine something from the code, flag it as "TODO: verify" rather than guessing
