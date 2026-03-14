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
- [Usage Guide & Expected Results](#usage-guide--expected-results)
- [Data Models](#data-models)
- [API Reference](#api-reference)
- [Environment & Dependencies](#environment--dependencies)
- [Appendix: Code Reference Index](#appendix-code-reference-index)

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
[ASCII diagram of system architecture]
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Runtime | Python | 3.11+ | Primary language |
| Framework | FastAPI | 0.100+ | Web framework |

### Design Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| ... | ... | ... |

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
```

**Output:**
```python
# Output type/schema
```

#### Implementation Details

**Key Files:**
- `src/components/name/main.py` - Entry point

**Key Classes/Functions:**
- `ClassName.method()` - Description

<!-- Include Source field only when documenting an existing codebase -->
#### Source

- `src/components/name/main.py`: ClassName.method(), entry_point()
- `src/components/name/utils.py`: helper_function(), parse_input()

#### Dependencies

| Dependency | Type | Purpose | Why |
|------------|------|---------|-----|
| ComponentB | Internal | Data processing | ... |

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

---

## Data Models

### Model: <EntityName>

```python
class EntityName:
    id: UUID
    name: str
    status: Enum['active', 'inactive']
```

**Constraints:**
- `name` must be unique within scope

**Indexes:**
- Primary: `id`

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
  "data": [{"id": "...", "name": "..."}],
  "pagination": {"page": 1, "limit": 20, "total": 100}
}
```

---

## Environment & Dependencies

### Directory Structure

```
project/
├── src/
├── tests/
└── ...
```

### Dependencies

**Runtime:**
```toml
[project.dependencies]
```

**Development:**
```toml
[project.optional-dependencies]
```

### Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| ... | ... | ... | ... |

---

## Appendix: Code Reference Index

All code references cited in this spec, organized by file.

| File | Functions / Classes | Referenced In |
|------|---------------------|---------------|
| `src/core/processor.py` | process_data(), transform() | Core Design, Component Details |
| `src/core/validator.py` | validate(), ValidationRule | Core Design |
