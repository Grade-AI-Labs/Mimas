# Tech-Stack Adapters

Building blocks for `docs/ENGINEERING.md` and subdomain `AGENTS.md` files. Pick the adapters that match what you discovered in Phase 1. Combine and customize — don't copy blindly.

---

## Language / Type Checking

### TypeScript
```
## TypeScript standards

- Strict mode enabled
- Avoid `any` unless absolutely necessary (document why if used)
- Use path aliases defined in `tsconfig.json`
- `noUncheckedIndexedAccess` recommended

**Typecheck command:**
```bash
npx tsc --noEmit
```

AGENTS.md critical rule:
> ### TypeScript correctness (MANDATORY)
> Before completing any task: run `npx tsc --noEmit` and fix all errors. Do not consider work complete until it exits with code 0.
```

### JavaScript (no TypeScript)
```
## JavaScript standards

- Prefer ESM over CommonJS
- Avoid implicit globals
- Use JSDoc for public APIs if no type system is present
```

### Python
```
## Python standards

- Type hints required for function signatures
- Run `mypy .` (or project-specific mypy config) before completing work
- Use virtual environment (`venv` or `poetry`)
- Format with `black` / `ruff` if configured

**Typecheck command:**
```bash
mypy .
```

AGENTS.md critical rule:
> ### Type correctness (MANDATORY)
> Before completing any task: run `mypy .` and fix all type errors.
```

### Go
```
## Go standards

- Run `go vet ./...` before completing work
- Use standard `gofmt` formatting
- Follow standard Go project layout

**Vet command:**
```bash
go vet ./...
```

AGENTS.md critical rule:
> ### Go vet (MANDATORY)
> Before completing any task: run `go vet ./...` and fix all issues.
```

### C# / .NET
```
## C# standards

- Nullable reference types enabled
- Follow .NET naming conventions (PascalCase for public members)
- Use `dotnet build` to verify compilation

**Build command:**
```bash
dotnet build --no-restore
```

AGENTS.md critical rule:
> ### Build correctness (MANDATORY)
> Before completing any task: run `dotnet build` and fix all errors and warnings.
```

### Rust
```
## Rust standards

- Run `cargo clippy` for linting
- Run `cargo check` for fast type checking
- Follow Rust API guidelines

**Check command:**
```bash
cargo check
cargo clippy -- -D warnings
```

AGENTS.md critical rule:
> ### Rust correctness (MANDATORY)
> Before completing any task: run `cargo check` and `cargo clippy -- -D warnings`. Fix all errors and warnings.
```

---

## Test Frameworks

### Jest (TypeScript/JavaScript)
```
- **Framework**: Jest with ts-jest (or Babel)
- **Test suffix**: `*.spec.ts` or `*.test.ts`
- **Location**: colocated with source files
- **Run**: `npm test` or `npx jest`
- **Watch**: `npm test -- --watch`
- **Single file**: `npm test -- --testPathPattern=<path>`
- **Coverage**: `npm test -- --coverage`

Integration tests that require a database: use Testcontainers or a local DB in Docker Compose.
```

### Vitest
```
- **Framework**: Vitest
- **Test suffix**: `*.spec.ts` or `*.test.ts`
- **Location**: colocated with source files
- **Run**: `npx vitest run`
- **Watch**: `npx vitest`
- **Single file**: `npx vitest run <path>`
- **Coverage**: `npx vitest run --coverage`
```

### Pytest
```
- **Framework**: pytest
- **Test suffix**: `test_*.py` or `*_test.py`
- **Location**: `tests/` directory or colocated
- **Run**: `pytest`
- **Watch**: `pytest-watch` or `ptw`
- **Single file**: `pytest tests/path/to/test_file.py`
- **Coverage**: `pytest --cov`
```

### Go test
```
- **Framework**: Go standard `testing` package
- **Test suffix**: `*_test.go`
- **Location**: colocated with source files
- **Run**: `go test ./...`
- **Single package**: `go test ./path/to/pkg/...`
- **Coverage**: `go test -cover ./...`
- **Race detector**: `go test -race ./...`
```

### xUnit / NUnit (.NET)
```
- **Framework**: xUnit (or NUnit)
- **Test suffix**: `*Tests.cs`
- **Location**: separate test project(s)
- **Run**: `dotnet test`
- **Single project**: `dotnet test path/to/Tests.csproj`
- **Coverage**: `dotnet test --collect:"XPlat Code Coverage"`
```

### Rust (cargo test)
```
- **Framework**: built-in `cargo test`
- **Test location**: `#[cfg(test)]` modules inline, or `tests/` for integration tests
- **Run**: `cargo test`
- **Single test**: `cargo test test_name`
- **Show output**: `cargo test -- --nocapture`
```

---

## Frameworks

### Fastify (Node.js)
```
Focus areas for subdomain AGENTS.md:
- API contracts and route definitions
- Plugin registration and lifecycle hooks
- Schema validation (Fastify JSON Schema or Zod)
- Error handling via `setErrorHandler`
- Security: rate limiting, CORS, helmet

Dev server: `npm run dev` (typically nodemon or tsx --watch)
```

### Express (Node.js)
```
Focus areas for subdomain AGENTS.md:
- Route definitions and middleware chain
- Request validation (zod, joi, or express-validator)
- Error handling middleware
- Security: helmet, cors, rate-limit

Dev server: `npm run dev`
```

### NestJS
```
Focus areas for subdomain AGENTS.md:
- Module, controller, service structure
- DTOs and class-validator decorators
- Guards and interceptors
- Exception filters

Dev server: `npm run start:dev`
```

### Next.js
```
Focus areas for subdomain AGENTS.md:
- App Router vs Pages Router (note which is used)
- Server components vs client components
- API routes (app/api/ or pages/api/)
- Data fetching patterns (server actions, fetch, SWR/React Query)

Dev server: `npm run dev`
Build check: `npm run build`
```

### React (Vite or CRA)
```
Focus areas for subdomain AGENTS.md:
- Component structure and prop contracts
- State management (Redux, Zustand, Context, etc.)
- Routing (React Router, TanStack Router)
- API integration layer

Dev server: `npm run dev`
```

### Django
```
Focus areas for subdomain AGENTS.md:
- URL routing and view definitions
- Serializers and model validation
- Middleware and authentication
- Database migrations (Django ORM)

Dev server: `python manage.py runserver`
```

### FastAPI
```
Focus areas for subdomain AGENTS.md:
- Endpoint definitions and Pydantic schemas
- Dependency injection
- Middleware and authentication
- Database sessions and Alembic migrations

Dev server: `uvicorn app.main:app --reload`
```

### ASP.NET
```
Focus areas for subdomain AGENTS.md:
- Controller/endpoint definitions
- Model binding and validation
- Middleware pipeline
- Dependency injection configuration
- Entity Framework migrations

Dev server: `dotnet run` or `dotnet watch`
```

---

## Databases

### Kysely (TypeScript)
```
## Database guidelines

- **Query builder**: Kysely (type-safe SQL)
- **Migrations**: in `{{migration_dir}}` — always write a migration for schema changes
- **Pattern**: Repositories own their DB access; no raw SQL outside repositories
- Run migration tests where appropriate
- Never mutate the database schema without a migration
```

### Prisma
```
## Database guidelines

- **ORM**: Prisma
- **Schema**: `prisma/schema.prisma`
- **Migrations**: `npx prisma migrate dev` for local, `npx prisma migrate deploy` for production
- **Client regeneration**: `npx prisma generate` after schema changes
- Do not edit migration files after they've been applied
```

### Drizzle
```
## Database guidelines

- **ORM**: Drizzle
- **Schema**: defined in `{{schema_location}}`
- **Migrations**: `npx drizzle-kit generate` → `npx drizzle-kit migrate`
- Keep schema definitions as the single source of truth
```

### SQLAlchemy (Python)
```
## Database guidelines

- **ORM**: SQLAlchemy
- **Migrations**: Alembic — always generate a migration for schema changes (`alembic revision --autogenerate`)
- **Session management**: use dependency injection; never share sessions across requests
```

### Entity Framework (.NET)
```
## Database guidelines

- **ORM**: Entity Framework Core
- **Migrations**: `dotnet ef migrations add <Name>` → `dotnet ef database update`
- **DbContext**: use dependency injection; never share across requests
- Always create a migration for schema changes — do not modify the database directly
```

### GORM (Go)
```
## Database guidelines

- **ORM**: GORM
- **Migrations**: use GORM auto-migrate or golang-migrate
- Always define models with explicit column names and types
```

### Diesel (Rust)
```
## Database guidelines

- **ORM**: Diesel
- **Migrations**: `diesel migration generate <name>` → `diesel migration run`
- **Schema**: auto-generated in `src/schema.rs` — do not edit manually
```

---

## Authentication

### JWT
```
## Authentication

- **Mechanism**: JWT (JSON Web Tokens)
- Tokens are verified on every request via middleware/plugin
- Never store secrets in code — use environment variables
- Token expiry must be enforced; refresh token rotation if applicable
- Auth logic lives in `{{auth_module_path}}`
```

### NextAuth / Auth.js
```
## Authentication

- **Mechanism**: NextAuth (Auth.js)
- Configuration in `{{auth_config_path}}`
- Session strategy: database or JWT (note which)
- Protect routes via middleware (`middleware.ts`)
```

### OAuth / OpenID Connect
```
## Authentication

- **Mechanism**: OAuth 2.0 / OIDC via `{{auth_library}}`
- Authorization code flow — never use implicit flow
- Store tokens securely (httpOnly cookies or server-side session)
- Validate token signatures and expiry on every request
```

### API Key
```
## Authentication

- **Mechanism**: API key (header: `{{header_name}}`)
- Keys are validated server-side on every request
- Never log full API keys
- Key rotation must not require downtime
```

### ASP.NET Identity / IdentityServer
```
## Authentication

- **Mechanism**: ASP.NET Identity (or IdentityServer / Duende)
- Authentication middleware configured in `Program.cs`
- Use `[Authorize]` attributes on controllers/endpoints
- Never store secrets in code — use User Secrets or environment variables
```

---

## AI / LLM Libraries

### LangChain (JS/Python)
```
Focus note for subdomain AGENTS.md:
- LangChain chains, runnables, and prompts live in `{{ai_module_path}}`
- Prompt changes count as behavioral changes — update feature docs
- Langfuse (or equivalent) traces all LLM calls; check traces when debugging AI behavior
```

### Vercel AI SDK
```
Focus note for subdomain AGENTS.md:
- AI SDK `streamText`, `generateText`, `generateObject` calls live in `{{ai_module_path}}`
- Model config (model name, temperature, system prompt) counts as a contract — document changes
```

### OpenAI SDK (direct)
```
Focus note for subdomain AGENTS.md:
- OpenAI API calls in `{{ai_module_path}}`
- Prompt text and model name are behavioral contracts — update feature docs if changed
- Never hardcode API keys; use environment variables
```

### Anthropic SDK
```
Focus note for subdomain AGENTS.md:
- Anthropic API calls in `{{ai_module_path}}`
- System prompts and model parameters are behavioral contracts — update feature docs if changed
- Never hardcode API keys; use environment variables
```

### Semantic Kernel (.NET)
```
Focus note for subdomain AGENTS.md:
- Semantic Kernel plugins and functions in `{{ai_module_path}}`
- Prompt templates and function configurations are behavioral contracts
- Never hardcode API keys; use configuration/secrets
```

---

## Monorepo

### npm/pnpm workspaces
```
## Monorepo structure

This is a monorepo managed with {{pnpm/npm}} workspaces.

- Each `packages/<name>/` is a separate package with its own `package.json`
- Root scripts: `{{build_all_command}}`, `{{test_all_command}}`
- Run package-specific commands: `pnpm --filter <package-name> <command>`
- Shared packages are imported as workspace dependencies

When making cross-package changes, ensure all affected packages build and test cleanly.
```

### Turborepo
```
## Monorepo structure

This is a Turborepo monorepo.

- `turbo.json` defines the task pipeline
- Run tasks: `npx turbo run build`, `npx turbo run test`
- Turborepo caches task outputs — run with `--force` if results seem stale
- Each app/package has its own `package.json` and local config
```

### Nx
```
## Monorepo structure

This is an Nx monorepo.

- `nx.json` defines the workspace configuration
- Run tasks: `npx nx run <project>:<target>`, `npx nx run-many --target=test`
- Nx caches and only re-runs affected projects
- Each project has its own `project.json` or inferred config
```

---

## Naming Conventions (by language)

### TypeScript / JavaScript
```
- Files: `kebab-case.ts`
- Types / Interfaces / Classes: `PascalCase`
- Functions / variables: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE`
- React components: `PascalCase.tsx`
- Test files: `kebab-case.spec.ts` or `kebab-case.test.ts`
```

### Python
```
- Files / modules: `snake_case.py`
- Classes: `PascalCase`
- Functions / variables: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`
- Test files: `test_snake_case.py`
```

### Go
```
- Files: `snake_case.go`
- Exported identifiers: `PascalCase`
- Unexported identifiers: `camelCase`
- Packages: short, lowercase, no underscores
- Test files: `snake_case_test.go`
```

### C#
```
- Files: `PascalCase.cs`
- Classes / Interfaces / Enums: `PascalCase`
- Interfaces: `IPascalCase` (prefix with I)
- Methods / Properties: `PascalCase`
- Private fields: `_camelCase`
- Local variables / parameters: `camelCase`
- Constants: `PascalCase`
- Test files: `PascalCaseTests.cs`
```

### Rust
```
- Files / modules: `snake_case.rs`
- Types / Traits / Enums: `PascalCase`
- Functions / variables: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`
- Test files: inline `#[cfg(test)]` or `tests/snake_case.rs`
```
