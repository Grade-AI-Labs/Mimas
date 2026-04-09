# Improve Text

## Overview

The Improve Text feature improves text content based on specified goals, audience, tonality, and other parameters. The service uses AI to enhance text quality, clarity, engagement, and other aspects while allowing fine-grained control over the improvement process.

**Status**: In Progress - This endpoint is still in development and subject to change.

## API Endpoint

### Endpoint Details
- **Method**: POST
- **Path**: `/api/v1/generative/shared/improve-text`
- **Version**: v1
- **Authentication**: Required (JWT or API Key)
- **Rate Limiting**: Yes (product-specific)

### Request Schema

```json
{
  "data": {
    "type": "improve-text",
    "attributes": {
      "text": "We are looking for a software engineer. The candidate should have experience.",
      "improvement_goals": ["clarity", "engagement", "professionalism"],
      "audience": "technical professionals",
      "tonality": "professional",
      "change_level": "moderate",
      "length_adjustment": "same",
      "seo_keywords": ["software engineer", "developer"],
      "user_instructions": "Make it more compelling"
    }
  },
  "meta": {
    "account_id": 123,
    "product": "varbi",
    "user_id": 456,
    "prompts": {
      "improve-text": {
        "version": "latest"
      }
    }
  }
}
```

**Required Fields**:
- `data.attributes.text` (string, minLength: 1): Text to improve
- `data.attributes.improvement_goals` (array, minItems: 1): Goals for improving the text. Suggested goals include: clarity, conciseness, engagement, professionalism, friendliness, persuasion, grammar and spelling, SEO optimization, creativity, accessibility. Custom goals are also supported.
- `data.attributes.change_level` (string): Level of changes to apply. Must be one of: `"light_edit"`, `"moderate"`, `"rewrite"`

**Optional Fields**:
- `data.attributes.audience` (string): Target audience for the improved text. Defaults to "general" if not provided.
- `data.attributes.tonality` (string): Desired tonality for the improved text. Defaults to "neutral" if not provided.
- `data.attributes.length_adjustment` (string): Adjustment to the length of the text. Must be one of: `"shorter"`, `"longer"`, `"same"`. Defaults to "same" if not provided.
- `data.attributes.seo_keywords` (array): SEO keywords to incorporate into the text
- `data.attributes.user_instructions` (string): Additional user instructions for improving the text

**Headers**:
- `Accept-Language` (optional): Target language code (e.g., "sv", "en", "no", "da", "fi"). If not provided, language is automatically detected from the text. Must contain only one language (comma-separated values not supported).

### Response Schema

```json
{
  "data": {
    "type": "improve-text",
    "attributes": {
      "improved_text": "We are seeking an experienced software engineer to join our innovative team. The ideal candidate will possess strong technical expertise and a passion for building exceptional software solutions."
    }
  },
  "meta": {
    "trace_id": "langfuse-trace-id-123"
  }
}
```

### Error Responses

- **400 Bad Request**: Invalid input data, missing required fields, Accept-Language header contains multiple languages
- **401 Unauthorized**: Missing or invalid authentication
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Service error or AI model failure

## Business Logic

### Core Functionality

1. **Input Validation**: Validates request data structure and required fields
2. **Language Detection**: Extracts target language from `Accept-Language` header, or automatically detects language from text if header not provided
3. **Language Validation**: Ensures Accept-Language header contains only one language (rejects comma-separated values)
4. **Text Improvement**: Uses AI model with chain-based execution to improve text based on all specified parameters
5. **Usage Tracking**: Records feature usage and model consumption

### Improvement Goals

Supported improvement goals include:
- **clarity**: Improve clarity and readability
- **conciseness**: Make text more concise
- **engagement**: Increase engagement and interest
- **professionalism**: Enhance professional tone
- **friendliness**: Make text more friendly and approachable
- **persuasion**: Improve persuasive elements
- **grammar and spelling**: Fix grammar and spelling errors
- **SEO optimization**: Optimize for search engines
- **creativity**: Add creative elements
- **accessibility**: Improve accessibility

Custom goals are also supported.

### Change Levels

- **light_edit**: Minimal changes, preserve original structure
- **moderate**: Moderate changes, balance between original and improved
- **rewrite**: Extensive changes, significant restructuring

### Data Flow

```
Input Data (text + improvement parameters)
    ↓
Controller Validation
    ↓
Language Detection/Validation
    ├─ If Accept-Language provided: Use it (must be single language)
    └─ If not provided: Auto-detect from text
    ↓
Chain Creation (createChain utility)
    ↓
AI Model Generation (OpenAI GPT-4.1 Mini)
    ↓
Response Formatting
    ↓
Usage Tracking (Database)
```

### Dependencies

- **Language Detection Service**: For automatic language detection (Azure)
- **Langfuse**: For prompt management and observability
- **LangChain**: For chain-based execution (createChain utility)
- **OpenAI API**: For text improvement (GPT-4.1 Mini)
- **PostgreSQL**: For usage tracking
- **GenerativeService**: Base service class

## Technical Implementation

### Service Layer

**Service Class**: `GenerateImproveTextService extends GenerativeService`

**Location**: ```11:60:src/domains/generative/shared/improve-text/v1/improve-text.service.ts```

**Key Methods**:
- `generate()`: Main generation method (inherited from GenerativeService)
- `generateOutput()`: Orchestrates the text improvement using createChain utility

**Key Components**:
- **Model**: GPT-4.1 Mini with temperature: 0.7
- **Prompt Key**: `improve-text`
- **Base Folder**: `shared`
- **Chain Type**: `string`
- **Chain Utility**: Uses `createChain` from `@src/domains/generative/utils/chains`

### Controller Layer

**Controller Function**: `improveTextController`

**Location**: ```8:54:src/domains/generative/shared/improve-text/v1/improve-text.controller.ts```

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
- `ImproveTextRequest`: Fastify request type with Accept-Language header
- `ExtendedImproveTextInput`: Input data structure with language
- `FeatureOutput`: Output data structure with improved_text and trace_id
- `ChangeLevel`: `'light_edit' | 'moderate' | 'rewrite'`
- `LengthAdjustment`: `'shorter' | 'longer' | 'same'`

**Location**: ```1:44:src/domains/generative/shared/improve-text/v1/utils/improve-text.types.ts```

## AI Model Configuration

### Model Used

- **Primary Model**: GPT-4.1 Mini
- **Configuration**:
  - `temperature`: 0.7
- **Model Selection**: Fixed model, no fallback

### Prompt Management

- **Prompt Template**: Managed in Langfuse
- **Prompt Key**: `improve-text`
- **Base Folder**: `shared`
- **Template Variables**:
  - `language`: Target language code
  - `input_text`: Text to improve
  - `improvement_goals`: Comma-separated improvement goals
  - `audience`: Target audience (default: "general")
  - `tonality`: Desired tonality (default: "neutral")
  - `change_level`: Level of changes (light_edit, moderate, rewrite)
  - `length_adjustment`: Length adjustment (shorter, longer, same, default: "same")
  - `seo_keywords`: Comma-separated SEO keywords (optional)
  - `user_instructions`: Additional user instructions (optional)
- **Version**: Uses version specified in `meta.prompts['improve-text']` or defaults to latest

## Usage Tracking

### Feature Registration

- **Feature Name**: `improve-text`
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
    "type": "improve-text",
    "attributes": {
      "text": "We need a developer. Must know React.",
      "improvement_goals": ["professionalism", "engagement", "clarity"],
      "audience": "software engineers",
      "tonality": "professional",
      "change_level": "moderate",
      "length_adjustment": "longer",
      "seo_keywords": ["React developer", "frontend engineer"],
      "user_instructions": "Make it sound more appealing to senior developers"
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
    "type": "improve-text",
    "attributes": {
      "improved_text": "We are seeking an experienced React developer to join our dynamic engineering team. The ideal candidate will possess deep expertise in React and modern frontend development practices, with a passion for building exceptional user experiences. This role offers the opportunity to work on cutting-edge projects and collaborate with talented engineers in a supportive, innovative environment."
    }
  },
  "meta": {
    "trace_id": "langfuse-trace-abc123"
  }
}
```

### Use Cases

1. **Content Enhancement**: Improve blog posts, articles, and marketing content
2. **Job Ad Refinement**: Enhance job advertisements for better appeal
3. **Email Improvement**: Improve professional emails and communications
4. **SEO Optimization**: Optimize content for search engines
5. **Tone Adjustment**: Adjust text tone for different audiences

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key (for GPT-4.1 Mini via Azure)
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint
- `LANGFUSE_SECRET_KEY`: Langfuse secret key
- `AZURE_LANGUAGE_ENDPOINT`: Azure Language Detection endpoint
- `AZURE_LANGUAGE_API_KEY`: Azure Language Detection API key

### Feature Flags

- No specific feature flags for this feature

### Product-Specific Configuration

**Supported Products**: All products (shared feature)
- `varbi`
- `onecruiter`
- `talentrekry`
- `talent`
- `learning`
- `refensa`
- `realcruit`
- And all other products

**Note**: This is a shared feature available across all product areas.

## Testing

### Unit Tests

**Test File**: `src/domains/generative/shared/improve-text/v1/improve-text.spec.ts`

**Key Scenarios**:
- Missing API key validation
- Invalid API key validation
- Missing required fields validation
- Multiple languages in Accept-Language header (should fail)
- Automatic language detection
- Successful text improvement with various parameters
- Database usage tracking verification

**Mocking**:
- Langfuse client
- OpenAI API (GPT-4.1 Mini)
- Language Detection Service
- createChain utility
- Database repository

### Integration Tests

- End-to-end request flow
- Database usage tracking
- Error scenarios
- Rate limiting
- Language detection
- Various improvement goal combinations

## Error Handling

### Common Errors

- **Invalid Input**: Missing required fields
- **Multiple Languages**: Accept-Language header contains comma-separated values (not supported)
- **Model Error**: AI model generation failure
- **Language Detection Error**: Automatic language detection failure

### Edge Cases

- **Empty Text**: Minimum 1 character required
- **Very Long Text**: Handles long text content
- **Missing Language Header**: Automatically detects language from text
- **Multiple Improvement Goals**: Handles multiple goals correctly
- **Optional Parameters**: All optional parameters have sensible defaults

## Performance Considerations

### Response Times

- **Expected**: 3-8 seconds for standard text
- **Complex Improvements**: 5-10 seconds for extensive rewrites
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

- **No PII Protection**: This feature does not use PII protection (text improvement)
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
- **Improvement Goal Distribution**: Usage of different improvement goals

### Tracing

- **Langfuse Traces**: Complete request/response tracing
- **Chain Tracing**: Chain execution traced
- **Prompt Versioning**: Track prompt versions used
- **Model Performance**: Model-specific performance metrics
- **Trace ID**: Returned in response meta for debugging

## Known Issues and Limitations

### Current Limitations

1. **Status**: Feature is marked as "In Progress" and subject to change
2. **Language Support**: Limited to languages supported by OpenAI and Azure Language Detection
3. **Multiple Languages**: Accept-Language header must contain only one language
4. **Improvement Quality**: Quality depends on input text and specified goals
5. **No PII Protection**: Does not use PII protection (may need for sensitive content)

### Future Improvements

1. **PII Protection**: Add optional PII protection for sensitive content
2. **Batch Processing**: Support for improving multiple texts
3. **Quality Metrics**: Metrics for improvement quality
4. **Custom Templates**: Pre-defined improvement templates
5. **Version Comparison**: Show before/after comparison

## Related Features

- **Summarize Text**: Summarizes text content (different use case)
- **Job Ad Generation**: Generates job ads (can use improve-text for refinement)

## Changelog

### v1 (Current)
- Initial implementation
- Multiple improvement goals support
- Automatic language detection
- Chain-based execution using createChain utility
- Langfuse integration
- Multi-language support
- Multi-product support

## References

- **Code**: `src/domains/generative/shared/improve-text/`
- **Routes**: `src/routes/api/v1/generative/shared/shared.route.ts`
- **Base Service**: ```23:196:src/domains/generative/generative.service.ts```
- **Chain Utility**: `src/domains/generative/utils/chains`
- **Language Detection**: `src/domains/azure-ai-services/language-detection`
- **Schema**: `src/domains/generative/shared/improve-text/v1/utils/improve-text.schema.ts`
