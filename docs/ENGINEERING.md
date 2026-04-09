# Engineering Standards & Workflows

This document defines shared engineering practices for the Hyperion backend.

---

## Root README.md policy

README.md exists to answer:
- what this repo is
- how to run it locally
- where to find canonical documentation

Agents should update README.md when:
- dev commands change
- ports or startup steps change
- links to docs move or are renamed

Agents should not:
- describe feature behavior
- list API endpoints
- include request/response schemas

Canonical documentation lives under `docs/` and `openspec/`.

## Testing standards

- **Framework**: Jest with ts-jest
- **Test suffix**: `*.spec.ts`
- **Location**: Tests live in `src/**/*.spec.ts`
- **Database**: Testcontainers for DB integration tests (Docker required locally)
- **Mocking**: Langfuse and external services are mocked in test environment
- **Path aliases**: Same path aliases (`@src/*`, `@domains/*`, etc.) work in tests as in application code

Example:
```ts
import { describe, it, expect } from '@jest/globals'
import { myService } from '../my-service'

describe('MyService', () => {
  it('returns expected result for valid input', async () => {
    const result = await myService.process({ input: 'test' })
    expect(result).toBeDefined()
  })
})
```

---

## TypeScript standards

- Strict mode enabled
- `noUncheckedIndexedAccess` enabled
- Avoid `any` unless absolutely necessary (document why)
- Use path aliases: `@src/*`, `@domains/*`, `@config/*`, `@routes/*`

---

## Naming conventions

- Files: `kebab-case.ts`
- Types / Classes: `PascalCase`
- Functions / variables: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE`

---

## Error handling

- Use typed errors
- Never swallow errors silently
- Log errors intentionally
- Centralized error handling where applicable

---

## Database guidelines

- **ORM**: Kysely (type-safe SQL query builder)
- **Migrations**: in `src/db/` (or project-specific migration directory)
- **Dual database**: PostgreSQL (primary) + pgvector (vector DB for embeddings)
- Write migration tests where appropriate

---

## Authentication (current model)

- **Mechanism**: JWT with Fastify
- **Security**: Rate limiting, input validation
- **Token domain**: Authentication and authorization under `src/domains/token/`

---

## Commands reference

```bash
npm test
npm test -- --watch
npx tsc --noEmit
npm run dev
```

---

## Completion checklist

Before marking work complete:

* [ ] Tests written before implementation
* [ ] All tests passing
* [ ] `npx tsc --noEmit` passes
* [ ] Naming conventions followed
* [ ] Errors handled
* [ ] Security considered
* [ ] Feature docs updated if contract/schema/invariant changed (see docs/AGENTS_FEATURES.md)