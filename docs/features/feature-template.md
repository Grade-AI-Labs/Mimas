# [Feature Name]

## Overview

[One-paragraph description of what the feature does and its primary purpose.]

**Status**: [Stable | In Progress | Deprecated] - [Optional note if not Stable.]

## API Endpoint

### Endpoint Details
- **Method**: [GET | POST | PUT | PATCH | DELETE]
- **Path**: `/api/v1/generative/[product-or-shared]/[feature-name]`
- **Version**: v1
- **Authentication**: Required (JWT or API Key)
- **Rate Limiting**: Yes (product-specific)

### Request Schema

```json
{
  "data": {
    "type": "[feature-name]",
    "attributes": {
      "required_field": "value",
      "optional_field": "value"
    }
  },
  "meta": {
    "account_id": 123,
    "product": "varbi",
    "user_id": 456,
    "prompts": {
      "[feature-name]": {
        "version": "latest"
      }
    }
  }
}
```

**Required Fields**:
- `data.attributes.[field]` ([type], [constraints]): [Description]

**Optional Fields**:
- `data.attributes.[field]` ([type]): [Description]. Defaults to "[default]" if not provided.

**Headers**:
- `Accept-Language` (optional): Target language code (e.g., "sv", "en", "no", "da", "fi"). If not provided, language is automatically detected from the text. Must contain only one language (comma-separated values not supported).

### Response Schema

```json
{
  "data": {
    "type": "[feature-name]",
    "attributes": {
      "result_field": "value"
    }
  },
  "meta": {
    "trace_id": "langfuse-trace-id-123"
  }
}
```

### Error Responses

- **400 Bad Request**: [Specific causes, e.g., invalid input data, missing required fields]
- **401 Unauthorized**: Missing or invalid authentication
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Service error or AI model failure

## Business Logic

### Core Functionality

1. **Input Validation**: Validates request data structure and required fields
2. **Language Detection**: Extracts target language from `Accept-Language` header, or automatically detects language from text if header not provided
3. **[Step 3]**: [Description]
4. **[Step 4]**: [Description]
5. **Usage Tracking**: Records feature usage and model consumption

### [Domain-Specific Logic Section]

[Describe any enumerations, rules, or classifications central to this feature. For example, supported modes, types, or goal options.]

- **[option_1]**: [Description]
- **[option_2]**: [Description]

### Data Flow

```
Input Data
    ↓
Controller Validation
    ↓
Language Detection/Validation
    ├─ If Accept-Language provided: Use it (must be single language)
    └─ If not provided: Auto-detect from text
    ↓
[Intermediate Step]
    ↓
AI Model Generation ([Model Name])
    ↓
Response Formatting
    ↓
Usage Tracking (Database)
```

### Dependencies

- **Language Detection Service**: For automatic language detection (Azure)
- **Langfuse**: For prompt management and observability
- **LangChain**: For chain-based execution (createChain utility)
- **OpenAI API**: For AI generation ([Model Name])
- **PostgreSQL**: For usage tracking
- **GenerativeService**: Base service class

## Technical Implementation

### Service Layer

**Service Class**: `[FeatureName]Service extends GenerativeService`

**Location**: ` ``[start]:[end]:src/domains/generative/[scope]/[feature-name]/v1/[feature-name].service.ts` ``

**Key Methods**:
- `generate()`: Main generation method (inherited from GenerativeService)
- `generateOutput()`: Orchestrates the feature logic using createChain utility

**Key Components**:
- **Model**: [Model Name] with temperature: [value]
- **Prompt Key**: `[feature-name]`
- **Base Folder**: `[shared | product-name]`
- **Chain Type**: `[string | object | array]`
- **Chain Utility**: Uses `createChain` from `@src/domains/generative/utils/chains`

### Controller Layer

**Controller Function**: `[featureName]Controller`

**Location**: ` ``[start]:[end]:src/domains/generative/[scope]/[feature-name]/v1/[feature-name].controller.ts` ``

**Responsibilities**:
- Request validation
- Language validation (rejects multiple languages in Accept-Language header)
- Automatic language detection if header not provided
- Service instantiation
- Response formatting with trace_id
- Error handling

### Repository Layer

**Repository**: `GenerativeRepository`

**Operations**:
- Feature usage tracking
- Model usage recording
- Success/failure logging

**Database Tables**:
- `feature_usage`: Tracks feature usage
- `model_usage`: Tracks AI model consumption

### Models and Types

**Key Types**:
- `[FeatureName]Request`: Fastify request type with Accept-Language header
- `Extended[FeatureName]Input`: Input data structure with language
- `FeatureOutput`: Output data structure with result and trace_id
- `[EnumType]`: `'[value_1]' | '[value_2]' | '[value_3]'`

**Location**: ` ``[start]:[end]:src/domains/generative/[scope]/[feature-name]/v1/utils/[feature-name].types.ts` ``

## AI Model Configuration

### Model Used

- **Primary Model**: [Model Name]
- **Configuration**:
  - `temperature`: [value]
- **Model Selection**: Fixed model, no fallback

### Prompt Management

- **Prompt Template**: Managed in Langfuse
- **Prompt Key**: `[feature-name]`
- **Base Folder**: `[shared | product-name]`
- **Template Variables**:
  - `language`: Target language code
  - `[variable_1]`: [Description]
  - `[variable_2]`: [Description]
- **Version**: Uses version specified in `meta.prompts['[feature-name]']` or defaults to latest

## Usage Tracking

### Feature Registration

- **Feature Name**: `[feature-name]`
- **Feature Version**: `1`
- **Tracking**: Records account_id, product_id, user_id, success status

### Model Usage

- **Token Tracking**: Input/output tokens recorded
- **Cost Tracking**: Model costs calculated and stored
- **Performance Metrics**: Response time and latency tracked
- **Trace ID**: Langfuse trace ID returned in response meta

## Examples

### Request Example

```json
{
  "data": {
    "type": "[feature-name]",
    "attributes": {
      "required_field": "example value",
      "optional_field": "example value"
    }
  },
  "meta": {
    "account_id": 100,
    "product": "varbi",
    "user_id": 200
  }
}
```

**Headers**:
```
Accept-Language: en
```

### Response Example

```json
{
  "data": {
    "type": "[feature-name]",
    "attributes": {
      "result_field": "example output"
    }
  },
  "meta": {
    "trace_id": "langfuse-trace-abc123"
  }
}
```

### Use Cases

1. **[Use Case 1]**: [Description]
2. **[Use Case 2]**: [Description]
3. **[Use Case 3]**: [Description]

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key (for [Model] via Azure)
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint
- `LANGFUSE_SECRET_KEY`: Langfuse secret key
- `AZURE_LANGUAGE_ENDPOINT`: Azure Language Detection endpoint
- `AZURE_LANGUAGE_API_KEY`: Azure Language Detection API key

### Feature Flags

- [List any feature flags, or "No specific feature flags for this feature"]

### Product-Specific Configuration

**Supported Products**: [All products (shared feature) | List specific products]
- `varbi`
- `onecruiter`
- [Others as applicable]

**Note**: [Any product-specific notes, e.g., "This is a shared feature available across all product areas."]

## Testing

### Unit Tests

**Test File**: `src/domains/generative/[scope]/[feature-name]/v1/[feature-name].spec.ts`

**Key Scenarios**:
- Missing API key validation
- Invalid API key validation
- Missing required fields validation
- Multiple languages in Accept-Language header (should fail)
- Automatic language detection
- Successful generation with various parameters
- Database usage tracking verification

**Mocking**:
- Langfuse client
- OpenAI API ([Model Name])
- Language Detection Service
- createChain utility
- Database repository

### Integration Tests

- End-to-end request flow
- Database usage tracking
- Error scenarios
- Rate limiting
- Language detection
- [Feature-specific scenario combinations]

## Error Handling

### Common Errors

- **Invalid Input**: Missing required fields
- **Multiple Languages**: Accept-Language header contains comma-separated values (not supported)
- **Model Error**: AI model generation failure
- **Language Detection Error**: Automatic language detection failure

### Edge Cases

- **Empty Input**: Minimum 1 character required
- **Very Long Input**: Handles large content
- **Missing Language Header**: Automatically detects language from text
- **Optional Parameters**: All optional parameters have sensible defaults

## Performance Considerations

### Response Times

- **Expected**: [X-Y seconds] for standard input
- **Complex Cases**: [X-Y seconds] for [describe complex scenario]
- **Bottlenecks**:
  - AI model generation (primary)
  - Language detection (if needed, secondary)

### Rate Limits

- **Product-Specific**: Different limits per product
- **Throttling**: Automatic throttling on limit exceeded
- **Priority**: Higher priority for premium products

## Security Considerations

### Authentication

- **Required**: JWT token or API key
- **Authorization**: Product-based access control
- **Validation**: Request signature validation

### Data Privacy

- **PII Protection**: [Yes — uses PII protection service | No — not applicable for this feature type]
- **Data Retention**: Usage data retained per product policy
- **Compliance**: GDPR-compliant data handling

## Monitoring and Observability

### Logging

- **Request Logging**: All requests logged with metadata
- **Error Logging**: Detailed error logs with stack traces
- **Performance Logging**: Response time and latency metrics

### Metrics

- **Success Rate**: Tracked per product
- **Response Time**: Average and p95/p99 percentiles
- **Token Usage**: Total tokens consumed
- **Error Rate**: Errors per product

### Tracing

- **Langfuse Traces**: Complete request/response tracing
- **Chain Tracing**: Chain execution traced
- **Prompt Versioning**: Track prompt versions used
- **Model Performance**: Model-specific performance metrics
- **Trace ID**: Returned in response meta for debugging

## Known Issues and Limitations

### Current Limitations

1. **[Limitation 1]**: [Description]
2. **Language Support**: Limited to languages supported by OpenAI and Azure Language Detection
3. **Multiple Languages**: Accept-Language header must contain only one language

### Future Improvements

1. **[Improvement 1]**: [Description]
2. **[Improvement 2]**: [Description]

## Related Features

- **[Related Feature 1]**: [Brief description of relationship]
- **[Related Feature 2]**: [Brief description of relationship]

## Changelog

### v1 (Current)
- Initial implementation
- [Notable capability 1]
- [Notable capability 2]
- Langfuse integration
- Multi-language support
- Multi-product support

## References

- **Code**: `src/domains/generative/[scope]/[feature-name]/`
- **Routes**: `src/routes/api/v1/generative/[scope]/[scope].route.ts`
- **Base Service**: ` ``23:196:src/domains/generative/generative.service.ts` ``
- **Chain Utility**: `src/domains/generative/utils/chains`
- **Language Detection**: `src/domains/azure-ai-services/language-detection`
- **Schema**: `src/domains/generative/[scope]/[feature-name]/v1/utils/[feature-name].schema.ts`
