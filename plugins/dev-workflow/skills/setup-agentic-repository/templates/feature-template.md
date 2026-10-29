# [Feature Name]

> **Area:** [area-name]
> **Status:** Active | In Progress | Deprecated
> **Last updated:** YYYY-MM-DD

## Overview

One paragraph describing what this feature does and why it exists.

## Responsibilities

- What this feature is responsible for
- Its boundaries — what it does NOT own

## Key concepts

- **ConceptA**: short definition
- **ConceptB**: short definition

---

## API Endpoint

### Endpoint Details
- **Method**: [GET | POST | PUT | PATCH | DELETE]
- **Path**: `/api/v1/[feature-path]`
- **Authentication**: [Required | Optional | None]
- **Rate Limiting**: [Yes — describe | No]

### Request Schema

```json
{
  "field": "type — description"
}
```

**Required fields:**
- `field` (type, constraints): description

**Optional fields:**
- `field` (type): description. Defaults to "X" if not provided.

### Response Schema

```json
{
  "field": "type — description"
}
```

### Error Responses

- **400 Bad Request**: [specific causes]
- **401 Unauthorized**: missing or invalid authentication
- **404 Not Found**: [when this applies]
- **500 Internal Server Error**: [specific causes]

---

## Business Logic

### Core Functionality

1. **Step 1**: description
2. **Step 2**: description
3. **Step 3**: description

### Business Rules

- Rule 1
- Rule 2

### Data Flow

```
Input → Validation → [Processing Steps] → Response
```

### Dependencies

- **Service/Library**: what it's used for
- **External API**: what it's used for
- **Database**: what tables/collections are involved

---

## Technical Implementation

### Service Layer

- **Location**: `path/to/service`
- **Key methods**: `methodName()` — description

### Controller / Handler

- **Location**: `path/to/handler`
- **Responsibilities**: request validation, service invocation, response formatting

### Repository / Data Access

- **Location**: `path/to/repository`
- **Tables/Collections**: list the relevant database objects
- **Migrations**: reference the migration that created/modified the schema

### Key Types

- `TypeName`: description of what it represents

---

## Configuration

### Environment Variables

- `VAR_NAME`: description (required | optional, default: X)

### Feature Flags

- [List any feature flags, or "None"]

---

## Testing

### Unit Tests

- **Location**: `path/to/tests`
- **Key scenarios**: list the most important test cases

### Integration Tests

- **Location**: `path/to/integration/tests`
- **Setup**: describe any required infrastructure (database, external services, etc.)
- **Mocking**: what external services are mocked and how

---

## Error Handling & Edge Cases

### Common Errors

- **Error scenario**: how it's handled

### Edge Cases

- **Edge case**: expected behavior

---

## Security Considerations

- Authentication requirements
- Authorization / access control
- Input validation and sanitization
- Data privacy considerations

---

## Performance Considerations

- Expected response times
- Known bottlenecks
- Caching strategy (if any)

---

## Known Issues and Limitations

1. **Limitation**: description

---

## Related Features

- **[Related Feature]**: brief description of relationship

## Changelog

| Date | Change |
|------|--------|
| YYYY-MM-DD | Initial documentation |
