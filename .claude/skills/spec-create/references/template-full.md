# Complete Spec Document Template

This is the full template with all possible sections. Adapt as needed for each project.

---

# <Project Name>

> One-line description of what this project does

**Version**: X.Y.Z
**Last Updated**: YYYY-MM-DD
**Status**: [Draft | In Review | Approved | Deprecated]

## Table of Contents

- [Background & Motivation](#background--motivation)
- [Core Design](#core-design)
- [Architecture Overview](#architecture-overview)
- [Component Details](#component-details)
- [Data Models](#data-models)
- [API Reference](#api-reference)
- [Environment & Dependencies](#environment--dependencies)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Performance Considerations](#performance-considerations)
- [Identified Issues & Improvements](#identified-issues--improvements)
- [Usage Guide & Expected Results](#usage-guide--expected-results)
- [Testing](#testing)
- [Deployment](#deployment)
- [Appendix: Code Reference Index](#appendix-code-reference-index)
- [Changelog](#changelog)

---

## Background & Motivation

### Problem Statement

[What problem does this project solve? What pain point or gap exists without it?]

### Why This Approach

[Why was this approach chosen over alternatives? Briefly compare with key alternatives considered.]

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| This project's approach | ... | ... | **Chosen** |
| Alternative A | ... | ... | Rejected: ... |

### Core Value Proposition

[What is the key value this project delivers? One paragraph summarizing the essential insight.]

### Primary Objective

[Clear statement of what the project aims to achieve]

### Key Features

1. **Feature 1**: Description
2. **Feature 2**: Description
3. **Feature 3**: Description

### Target Users / Use Cases

| User Type | Use Case | Priority |
|-----------|----------|----------|
| Developer | ... | High |
| Admin | ... | Medium |

### Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Non-Goals (Out of Scope)

- Item 1
- Item 2

---

## Core Design

### Key Idea

[Narrative explanation of the core design idea. What is the central insight or approach that drives this project's architecture? Write as a story — what problem was encountered, what solution was devised, and why it works.]

### Algorithm / Logic Flow

[Describe the main algorithm or processing flow. Include actual code excerpts for key functions.]

> **Code Excerpt Rule**: Functions ≤30 lines → include full body. Functions >30 lines → include signature + core logic only.

```python
# [src/core/processor.py:process_data]
def process_data(input: InputModel) -> OutputModel:
    """Core processing logic."""
    validated = validate(input)
    result = transform(validated)
    return OutputModel(result=result)
```

> **Inline Citation Format**: Reference code in prose as `[filepath:functionName]`.
> Example: "The validation step `[src/core/validator.py:validate]` ensures data integrity before the transform `[src/core/processor.py:transform]`."

### Design Rationale

[Why was this structure chosen? What constraints or goals drove the design decisions?]

| Design Choice | Rationale | Alternatives Considered |
|---------------|-----------|------------------------|
| Choice 1 | Why this was chosen | What else was considered |
| Choice 2 | Why this was chosen | What else was considered |

---

## Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Client Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │   Web    │  │  Mobile  │  │   CLI    │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
└───────┼─────────────┼─────────────┼─────────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
┌─────────────────────┼───────────────────────────────┐
│                     ▼                                │
│              ┌─────────────┐                         │
│              │  API Layer  │                         │
│              └──────┬──────┘                         │
│                     │                                │
│         ┌───────────┼───────────┐                   │
│         ▼           ▼           ▼                   │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│   │ Service  │ │ Service  │ │ Service  │           │
│   │    A     │ │    B     │ │    C     │           │
│   └────┬─────┘ └────┬─────┘ └────┬─────┘           │
└────────┼────────────┼────────────┼──────────────────┘
         │            │            │
         └────────────┼────────────┘
                      │
┌─────────────────────┼───────────────────────────────┐
│                     ▼                                │
│              ┌─────────────┐                         │
│              │  Database   │                         │
│              └─────────────┘                         │
└─────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Runtime | Python | 3.11+ | Primary language |
| Framework | FastAPI | 0.100+ | Web framework |
| Database | PostgreSQL | 15+ | Data storage |
| Cache | Redis | 7+ | Caching layer |

### Design Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| Use async | Performance for I/O-bound tasks | Sync (rejected: blocking) |
| PostgreSQL | ACID compliance, JSON support | MongoDB (rejected: consistency) |

Record significant decisions in `_sdd/spec/DECISION_LOG.md` as well, so rationale remains traceable when the main spec is later split or simplified.

---

## Component Details

### Component: <Name>

#### Overview

Brief description of what this component does.

#### Why

Why this component exists — what problem it solves, why it's a separate component rather than part of something else. Write as natural prose, NOT as a label pattern like "~의 이유: ..." (e.g., "Separated from X because Y to enable independent scaling").

#### Responsibility

- Primary: What it does
- Secondary: Supporting functions

#### Interface

**Input:**
```python
# Input type/schema
class InputModel:
    field1: str
    field2: int
```

**Output:**
```python
# Output type/schema
class OutputModel:
    result: str
    status: str
```

#### Implementation Details

**Key Files:**
- `src/components/name/main.py` - Entry point
- `src/components/name/utils.py` - Helper functions
- `src/components/name/models.py` - Data models

**Key Classes/Functions:**
- `ClassName.method()` - Description
- `function_name()` - Description

**Design Patterns Used:**
- Strategy pattern for...
- Factory pattern for...

<!-- Include Source field only when documenting an existing codebase -->
#### Source

| **Source** | `src/components/name/main.py`: ClassName.method(), entry_point() |
|            | `src/components/name/utils.py`: helper_function(), parse_input() |
|            | `src/components/name/models.py`: InputModel, OutputModel |

#### Dependencies

| Dependency | Type | Purpose | Why |
|------------|------|---------|-----|
| ComponentB | Internal | Data processing | Separated processing logic to allow independent scaling and testing |
| redis | External | Caching | In-memory store needed for sub-millisecond lookups; chosen over local cache for multi-instance consistency |

#### Error Handling

| Error | Cause | Handling |
|-------|-------|----------|
| ValidationError | Invalid input | Return 400 with details |
| TimeoutError | Slow downstream | Retry with backoff |

#### Known Issues

- **Issue 1**: Description (Workaround: ...)
- **Issue 2**: Description (Planned fix: ...)

---

## Data Models

### Model: <EntityName>

```python
class EntityName:
    id: UUID
    created_at: datetime
    updated_at: datetime

    # Core fields
    name: str
    status: Enum['active', 'inactive']

    # Relationships
    parent_id: Optional[UUID]
    children: List[EntityName]
```

**Constraints:**
- `name` must be unique within scope
- `status` defaults to 'active'

**Indexes:**
- Primary: `id`
- Unique: `(scope_id, name)`
- Index: `created_at`

---

## API Reference

### Endpoint: `GET /api/v1/resource`

**Description:** Retrieve list of resources

**Request:**
```
GET /api/v1/resource?page=1&limit=20
Authorization: Bearer <token>
```

**Response:**
```json
{
  "data": [
    {"id": "...", "name": "..."}
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

**Error Responses:**
| Status | Reason |
|--------|--------|
| 401 | Invalid token |
| 403 | Insufficient permissions |

---

## Environment & Dependencies

### Directory Structure

```
project/
├── src/
│   ├── __init__.py
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration management
│   ├── components/       # Core components
│   │   ├── __init__.py
│   │   └── component_a/
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   └── utils/            # Shared utilities
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
├── scripts/
├── .env.example
├── pyproject.toml
└── README.md
```

### Dependencies

**Runtime:**
```toml
[project.dependencies]
python = "^3.11"
fastapi = "^0.100.0"
pydantic = "^2.0"
```

**Development:**
```toml
[project.optional-dependencies]
dev = [
    "pytest",
    "black",
    "mypy",
]
```

### System Requirements

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- 2GB RAM minimum

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | - | PostgreSQL connection string |
| REDIS_URL | No | localhost:6379 | Redis connection |
| LOG_LEVEL | No | INFO | Logging verbosity |

### Configuration Files

**config.yaml:**
```yaml
server:
  host: 0.0.0.0
  port: 8000
  workers: 4

database:
  pool_size: 10
  max_overflow: 5
```

---

## Security Considerations

### Authentication

- JWT-based authentication
- Token expiry: 1 hour
- Refresh token: 7 days

### Authorization

| Role | Permissions |
|------|-------------|
| admin | All operations |
| user | Read, create own |
| viewer | Read only |

### Data Protection

- Passwords hashed with bcrypt
- Sensitive data encrypted at rest
- HTTPS enforced in production

---

## Performance Considerations

### Benchmarks

| Operation | Target | Current |
|-----------|--------|---------|
| List (100 items) | <100ms | 85ms |
| Create | <50ms | 42ms |
| Search | <200ms | 180ms |

### Optimization Strategies

- Database query optimization
- Redis caching for hot data
- Connection pooling

### Scaling Considerations

- Horizontal scaling via container orchestration
- Database read replicas for heavy read loads
- CDN for static assets

---

## Identified Issues & Improvements

### Critical Bugs

- [ ] **BUG-001**: Memory leak in long-running processes
  - Location: `src/services/processor.py:145`
  - Impact: High
  - Status: Investigating

### Code Quality Issues

- [ ] Missing type hints in legacy modules
- [ ] Inconsistent error handling patterns
- [ ] Duplicate code in utils

### Missing Features

- [ ] Batch operations API
- [ ] Export functionality
- [ ] Audit logging

### Technical Debt

- [ ] Migrate from deprecated library X
- [ ] Refactor monolithic service
- [ ] Add comprehensive test coverage

---

## Usage Guide & Expected Results

### Scenario 1: [Basic Usage]

**Setup:**
```bash
# Prerequisites and setup steps
```

**Action:**
```bash
# What the user does
```

**Expected Result:**
```
# What should happen — expected output, state changes, or observable effects
```

### Scenario 2: [Advanced Usage]

**Setup:** [Prerequisites]

**Action:** [Steps]

**Expected Result:** [Observable outcome with specific values/behaviors]

### Installation

```bash
# Clone repository
git clone https://github.com/org/project.git
cd project

# Install dependencies
pip install -e ".[dev]"

# Set up environment
cp .env.example .env
```

### Running Locally

```bash
# Start dependencies
docker-compose up -d db redis

# Run migrations
python scripts/migrate.py

# Start development server
python -m src.main
```

### Common Operations

**Creating a resource:**
```bash
curl -X POST http://localhost:8000/api/v1/resource \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "example"}'
```

**Querying resources:**
```bash
curl http://localhost:8000/api/v1/resource?status=active \
  -H "Authorization: Bearer $TOKEN"
```

---

## Testing

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# With coverage
pytest --cov=src --cov-report=html
```

### Test Coverage Goals

| Module | Target | Current |
|--------|--------|---------|
| Core | 90% | 85% |
| Services | 80% | 72% |
| Utils | 70% | 68% |

---

## Deployment

### Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL certificates installed
- [ ] Monitoring configured
- [ ] Backup strategy in place

### Deployment Commands

```bash
# Build container
docker build -t project:latest .

# Deploy
kubectl apply -f k8s/
```

---

## Appendix: Code Reference Index

All code references cited in this spec, organized by file.

| File | Functions / Classes | Referenced In |
|------|---------------------|---------------|
| `src/core/processor.py` | process_data(), transform() | Core Design, Component Details |
| `src/core/validator.py` | validate(), ValidationRule | Core Design |
| `src/api/handler.py` | APIHandler, handle_request() | Component Details |

---

## Changelog

### [Unreleased]
- Feature: ...
- Fix: ...

### [1.0.0] - YYYY-MM-DD
- Initial release
- Core functionality implemented
