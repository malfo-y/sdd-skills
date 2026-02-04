---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions ".sdd" directory, specification documents, or project documentation needs.
version: 1.0.0
---

# Spec Document Creation and Management

Create and manage Software Design Description (SDD) spec documents for projects. Spec documents provide comprehensive technical documentation including goals, architecture, components, and usage examples.
Use Korean (한국어) for the spec document.

## Overview

Spec documents are stored in the `.sdd/spec/` directory within the project root. They follow a standardized structure to ensure consistency and completeness across different projects.

## When to Use This Skill

- Creating new spec documents for projects
- Breaking down large projects into modular spec files
- Generating documentation from existing code

## Directory Structure

```
.sdd/
├── spec/
│   ├── main.md             # Main spec document (or <project-name>.md)
│   ├── <component>.md      # Component-specific specs (for large projects)
│   └── user_spec.md        # User requirements (if exists)
└── IMPLEMENTATION_PLAN.md  # Implementation plan (if exists)
```

## Spec Document Creation Process

### Step 1: Gather Information

Before creating a spec document, collect:

1. **From User Input**: Direct requirements and constraints
2. **From Existing Code**: Analyze codebase structure and patterns
3. **From Documentation**: Read existing README, comments, configs
4. **Clarification**: Use AskUserQuestion for ambiguous requirements

User input includes user conversation and user-specified files (defaults to `.sdd/spec/user_spec.md`).

### Step 2: Analyze the Project

Explore the codebase to understand:

- Project structure and file organization
- Main entry points and components
- Dependencies and external integrations
- Data flow and architecture patterns
- Known issues and limitations

### Step 3: Write the Spec Document

Follow the template structure below, adapting sections as needed:

```markdown
# <Project Name>

## Goal

Describe project goals in detail:
- Primary objective
- Key features
- Target users/use cases
- Success criteria

## Architecture Overview

Describe project architecture:
- High-level system design
- Component interactions
- Data flow diagrams (use text or ASCII art)
- Technology stack

## Component Details

### <Component Name>

For each major component, include:

| Aspect | Description |
|--------|-------------|
| **Purpose** | What this component does |
| **Input** | Expected inputs and formats |
| **Output** | Produced outputs and formats |
| **Dependencies** | Other components or external deps |

**Architecture Details:**
- Implementation approach
- Key classes/functions
- Design patterns used

**How to Use:**
- API/interface examples
- Configuration options

**Known Issues:**
- Current limitations
- Planned improvements

## Environment & Dependencies

### Directory Structure
```
project/
├── src/
├── tests/
└── ...
```

### Dependencies
- Runtime dependencies
- Development dependencies
- Environment requirements

### Configuration
- Environment variables
- Config files
- Required credentials

## Identified Issues & Improvements

### Critical Bugs
- [ ] Issue description and location

### Code Quality Issues
- [ ] Technical debt items

### Missing Features
- [ ] Feature gaps

### Robustness & Reliability
- [ ] Error handling improvements needed

## Usage Examples

### Running the Project
```bash
# Command to run
```

### Common Operations
- Example 1: Description
- Example 2: Description

### Output Interpretation
- How to interpret results
```

## Spec Management Operations

### Creating a New Spec

1. Create `.sdd/spec/` directory if not exists
2. Analyze project using explore agent or direct reading
3. Write spec following template structure
4. Save as `<project-name>.md` or `main.md`

### Modular Specs for Large Projects

For large projects, split into multiple files:

```
.sdd/spec/
├── main.md              # Overview and cross-references
├── api-spec.md          # API component spec
├── database-spec.md     # Database component spec
└── frontend-spec.md     # Frontend component spec
```

Reference sub-specs from main:
```markdown
## Component Details

See detailed specs:
- [API Specification](./api-spec.md)
- [Database Specification](./database-spec.md)
```

## Best Practices

### Writing Quality

- **Be Specific**: Avoid vague descriptions
- **Use Examples**: Include code snippets and usage examples
- **Stay Current**: Update spec when code changes significantly
- **Link to Code**: Reference file paths and line numbers when helpful

### Organization

- **Logical Flow**: Start with overview, then details
- **Consistent Format**: Use same structure across components
- **Table of Contents**: Include for documents over 500 lines

### Completeness

- **All Components**: Document every major component
- **Error Cases**: Document error handling and edge cases
- **Dependencies**: List all external dependencies
- **Configuration**: Document all config options

## Language Preference

Follow user's language preference for spec content:
- Default to the language used in existing project documentation
- If unclear, use AskUserQuestion to confirm preferred language

## Output Location

Save spec documents to:
- **Default**: `.sdd/spec/<project-name>.md` or `.sdd/spec/main.md`
- **User Specified**: Any path the user requests
- **Create directories**: Automatically create `.sdd/spec/` if needed

## Additional Resources

### Reference Files
- **`references/template-full.md`** - Complete template with all sections
- **`references/examples.md`** - Real-world spec examples

### Example Files
- **`examples/simple-project-spec.md`** - Minimal spec for small projects
- **`examples/complex-project-spec.md`** - Full spec for large projects

## Integration with Other Skills

This skill works well with:
- **implementation-plan**: Create implementation plan from spec
- **implementation**: Implement features based on spec
- **implementation-review**: Review implementation against spec
