# Advanced Implementation Planning Patterns

## Complex Project Patterns

### Microservices Architecture

When planning microservices:

1. **Service Boundaries First**: Define clear service responsibilities before tasks
2. **API Contracts Early**: Design inter-service communication in Phase 1
3. **Shared Infrastructure**: Plan common components (auth, logging, config)
4. **Independent Deployability**: Each service should have its own CI/CD tasks

Example component breakdown:
```
- API Gateway (routing, rate limiting)
- Auth Service (authentication, authorization)
- User Service (profiles, preferences)
- Core Service (business logic)
- Notification Service (email, push, SMS)
- Shared Libraries (common utilities, types)
```

### Monolith to Microservices Migration

1. **Strangler Pattern Tasks**: Identify features to extract incrementally
2. **Data Migration Strategy**: Plan database splitting carefully
3. **Dual-Write Period**: Tasks for maintaining consistency during transition
4. **Feature Flags**: Enable gradual rollout and rollback

### Legacy System Modernization

1. **Discovery Phase**: Tasks for understanding existing system
2. **Test Coverage First**: Add tests before refactoring
3. **Incremental Changes**: Small, reversible modifications
4. **Parallel Running**: Validate new implementation against old

## Task Decomposition Strategies

### Vertical Slicing

Break features into end-to-end slices:
```
Feature: User Authentication
├── Slice 1: Basic login (email/password)
│   ├── Backend: Login endpoint
│   ├── Frontend: Login form
│   ├── Database: User credentials schema
│   └── Tests: E2E login flow
├── Slice 2: OAuth integration
│   ├── Backend: OAuth callbacks
│   ├── Frontend: OAuth buttons
│   └── Tests: OAuth flow
└── Slice 3: MFA
    ├── Backend: TOTP validation
    ├── Frontend: MFA setup/verify
    └── Tests: MFA scenarios
```

### Horizontal Slicing (Use Sparingly)

Layer-by-layer when infrastructure requires:
```
Infrastructure Setup
├── Database: Schema, migrations, indexes
├── API Layer: Routes, middleware, validation
├── Service Layer: Business logic, repositories
└── Frontend: Components, state, API integration
```

## Risk-Based Planning

### Risk Assessment Matrix

| Probability | Low Impact | Medium Impact | High Impact |
|-------------|------------|---------------|-------------|
| High        | P2         | P1            | P0          |
| Medium      | P3         | P2            | P1          |
| Low         | P3         | P3            | P2          |

### Common Risk Categories

1. **Technical Risks**
   - New/unfamiliar technology
   - Complex integrations
   - Performance requirements
   - Security requirements

2. **Schedule Risks**
   - External dependencies
   - Resource availability
   - Scope creep potential

3. **Quality Risks**
   - Insufficient testing
   - Missing documentation
   - Technical debt accumulation

### Mitigation Strategies

- **Spike Tasks**: Research/prototype before committing
- **Buffer Tasks**: Explicit time for unknowns
- **Checkpoint Reviews**: Plan review points between phases
- **Fallback Options**: Document alternative approaches

## Dependency Management

### Dependency Types

1. **Hard Dependencies**: Must complete before starting
   - Database schema before data access code
   - Auth service before protected endpoints

2. **Soft Dependencies**: Beneficial but not blocking
   - UI components before final integration
   - Logging before full feature implementation

3. **External Dependencies**: Outside team control
   - Third-party API access
   - Security reviews
   - Infrastructure provisioning

### Critical Path Analysis

Identify the longest chain of dependent tasks:

```
[Schema Design] → [API Endpoints] → [Frontend Integration] → [E2E Tests]
     2 days          3 days              2 days              1 day
                                                         Total: 8 days

Parallel work possible:
- [Unit Tests] during [API Endpoints]
- [Component Development] during [API Endpoints]
```

## Phase Planning Strategies

### MVP-First Approach

```
Phase 0: Foundation (required for all features)
Phase 1: MVP (minimum viable product)
Phase 2: Core Features (essential but not launch-blocking)
Phase 3: Nice-to-Have (enhancements, optimizations)
Phase 4: Future (documented but not planned in detail)
```

### Risk-First Approach

```
Phase 1: Highest-risk items (validate assumptions early)
Phase 2: Core functionality
Phase 3: Lower-risk enhancements
```

### Dependency-Driven Approach

```
Phase 1: Foundation (no dependencies)
Phase 2: Core services (depends on Phase 1)
Phase 3: Integration (depends on Phase 2)
Phase 4: Polish (depends on Phase 3)
```

## Integration with Project Tools

### GitHub Issues

Map tasks to issue templates:
```yaml
Task → Issue
Component → Label
Priority → Label (priority/P0, priority/P1)
Phase → Milestone
Dependencies → Issue links
```

### Jira

Map tasks to Jira structure:
```yaml
Component → Epic
Task → Story/Task
Subtask → Subtask
Phase → Sprint/Version
Dependencies → Issue links
```

### Linear

Map tasks to Linear:
```yaml
Component → Project
Task → Issue
Phase → Cycle
Priority → Priority field
Dependencies → Relations
```

## Estimation Guidelines

While avoiding time estimates in conversation, plans may include relative sizing:

### T-Shirt Sizing
- **XS**: Trivial change, well-understood
- **S**: Small feature, clear requirements
- **M**: Medium feature, some unknowns
- **L**: Large feature, significant complexity
- **XL**: Epic-level, should be broken down

### Story Points (Fibonacci)
- **1**: Trivial
- **2**: Small
- **3**: Medium
- **5**: Large
- **8**: Very large (consider splitting)
- **13+**: Too large, must split

## Quality Gates

Define checkpoints between phases:

### Phase Exit Criteria

```markdown
## Phase 1 → Phase 2 Gate
- [ ] All P0 tasks complete
- [ ] Core API endpoints functional
- [ ] Basic auth working
- [ ] Database migrations applied
- [ ] CI/CD pipeline operational
- [ ] Code review completed
- [ ] No critical bugs open
```

### Definition of Done (per task)

```markdown
- [ ] Code complete and reviewed
- [ ] Unit tests passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Performance acceptable
- [ ] Security review (if applicable)
```
