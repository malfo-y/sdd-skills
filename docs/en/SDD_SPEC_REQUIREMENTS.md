# SDD Spec Document Requirements

In SDD, a spec document is not just a description — it must be a navigable map that enables both humans and LLMs to quickly understand a codebase and make changes safely.

This document outlines the core purpose, mandatory requirements, recommended structure, and quality criteria we expect from spec documents.

---

## 1. Why We Write Spec Documents

### Core Purpose

1. **Rapid Understanding**
   - A person should be able to quickly understand what this codebase or spec is about.

2. **Navigation and Change Support**
   - When a person or LLM adds or modifies a feature, they should be able to find where things are and determine what needs to be changed.

3. **Preserving Decisions and Constraints**
   - Non-obvious structures, constraints, trade-offs, and invariants that are not apparent from code alone must be documented.

4. **Reducing Change Risk**
   - The spec should reveal how far a change propagates and what else needs to be verified, thereby reducing modification cost and regression risk.

### One-Line Definition

A good spec is not a copy of the code, but a searchable layer that compresses `intent + structure + contracts + change points + decision rationale`.

---

## 2. Documentation Philosophy

### What a Spec Should Be

- A spec should be a **navigable document**, not an encyclopedic code dump.
- A spec should prioritize answering "what does this repository do" and "what should be changed where."
- The main spec should serve as an **entry point** rather than a detailed manual.
- Component specs should emphasize **"where to look and what must not break"** more strongly than "what this component is."

### Relationship Between Spec and Code

- **Code is the source of truth for implementation.**
- **A spec is the operational interface for understanding and making changes.**
- A spec does not replace code.
- A spec should provide orientation before reading code and serve as a navigation starting point when modifying code.

### Do Not Hide What You Don't Know

- Do not assert unverified information as fact.
- Separate low-confidence information into `Open Questions`.
- Explicit uncertainty is better than false confidence.

### Consider How LLMs Consume Specs

- LLMs have a finite context window. An overly long spec can be harmful by pushing out key information.
- The main spec should be short enough for an LLM to read in one pass and grasp the big picture. Move details to component specs.
- LLMs parse **structured formats** (tables, lists, `key: value`) more accurately than natural language prose.
- Paths and symbols should be wrapped in code blocks (`` ` ``) to distinguish them from regular text.

---

## 3. Mandatory Requirements

| Requirement | Meaning | How It Should Appear in the Document |
|-------------|---------|--------------------------------------|
| Rapid First Understanding | A newcomer should grasp the big picture within 5 minutes | Project summary, system boundary, key flows |
| Searchability | Humans/LLMs should be able to find the relevant area immediately | Actual paths, component index, key symbols |
| Change Orientation | Should indicate where to start when modifying a feature | Change Guide, Change Recipes, impact scope notes |
| Clear Responsibility Boundaries | Each component's scope and non-scope should be visible | Responsibility, Owned Paths, Dependencies |
| Contract Visibility | External/internal interfaces and invariants should be visible | Inputs/Outputs, API/Event contracts, Invariants |
| Risk Exposure | Should reveal what can go wrong if changed incorrectly | Risks, Known Issues, regression points |
| Executability | There should be a starting point for local execution/testing/verification | Environment, Setup/Test Commands |
| Decision Traceability | The rationale behind structural choices should be preserved | `DECISION_LOG.md` or brief rationale |
| Scalability | Documentation should not collapse even in large codebases | main + component spec split structure |
| Freshness | Specs must be updated when code changes | Connected to spec-update flow |

---

## 4. Content That Must Be Included

### Main Spec

The main spec should be the first document a newcomer opens, and it must serve the following roles:

1. Explain the problem the project solves.
2. Describe the system boundary of the repository.
3. Provide a map of key directories/files/components.
4. Show major runtime flows.
5. Indicate starting points for feature changes.
6. Expose common invariants and important constraints.
7. Separately present remaining uncertainties.

### Component Spec

A component spec deeply describes a specific unit of responsibility and must serve the following roles:

1. Describe the responsibilities and non-responsibilities of this component.
2. Link actual owned paths to key symbols.
3. Organize inputs/outputs/external contracts.
4. Document upstream/downstream dependencies.
5. Provide starting points and verification checkpoints for each type of change.
6. Show related tests, logs, metrics, and debugging points.
7. Record invariants and risks specific to this component.

### Separate Documents

- `DECISION_LOG.md`
  - Used only to record non-obvious decisions, trade-offs, and structural constraints.
- `_sdd/env.md`
  - Manages environment information such as execution, testing, environment variables, and required services.

---

## 5. Recommended Document Structure

Sections are divided into **required (MUST)** and **optional (OPT)**. The required sections alone should produce a useful spec; optional sections are added based on project size and complexity.

### Recommended Main Spec Sections

| Type | Section | Description |
|------|---------|-------------|
| **MUST** | `Goal` | Project purpose and scope |
| | ↳ `Project Snapshot` | One-paragraph summary |
| | ↳ `Key Features` | List of core features |
| | ↳ `Non-Goals` | What the project does not do |
| **MUST** | `Architecture Overview` | System structure |
| | ↳ `System Boundary` | External boundaries and integrations |
| | ↳ `Repository Map` | Directory/file map |
| | ↳ `Runtime Map` | Major runtime flows |
| OPT | ↳ `Technology Stack` | Technology stack summary |
| OPT | ↳ `Cross-Cutting Invariants` | Global invariants |
| **MUST** | `Component Details` | Component summaries and links |
| | ↳ `Component Index` | Name, responsibility, path, spec link |
| OPT | `Environment & Dependencies` | Execution environment (can be separated into `env.md`) |
| OPT | ↳ Setup / Test Commands | Setup and test commands |
| OPT | ↳ Configuration / Secrets | Configuration and secrets |
| OPT | `Identified Issues & Improvements` | Risks, tech debt, gaps |
| OPT | `Usage Examples` | Execution, common tasks, change path examples |
| OPT | ↳ `Common Change Paths` | Starting points for frequent changes |
| **MUST** | `Open Questions` | Unverified/uncertain items |

> **Guideline**: For small projects (50 files or fewer), the MUST sections alone are sufficient. Start filling in OPT sections for projects with 5 or more components or complex external integrations.

### Recommended Component Spec Sections

| Type | Section | Description |
|------|---------|-------------|
| **MUST** | `Responsibility` | What this component does and does not do |
| **MUST** | `Owned Paths` | Owned files/directory paths |
| **MUST** | `Key Symbols / Entry Points` | Key functions, classes, entry points |
| **MUST** | `Interfaces / Contracts` | Inputs/outputs, API, event contracts |
| **MUST** | `Dependencies` | Upstream/downstream dependencies |
| **MUST** | `Change Recipes` | Starting points and verification checkpoints per change type |
| OPT | `Tests / Observability` | Tests, logs, metrics, debugging points |
| OPT | `Risks / Invariants` | Conditions that must not be broken, cautions |
| OPT | `Known Issues` | Known problems and workarounds |
| OPT | `Open Questions` | Unverified items |

---

## 6. Concrete Examples: Good Spec vs Bad Spec

Principles alone make it difficult to judge actual quality. This section compares good and bad examples across key areas.

### 6.1 Repository Map

**Bad example** — Vague description without paths:

```
The project consists of a service layer, data layer, and presentation layer.
The service layer handles business logic, and the data layer handles DB access.
```

**Good example** — Linking actual paths to roles:

```
src/
├── api/            # HTTP endpoints (Express routers)
│   ├── routes/     # Route definitions
│   └── middleware/  # Authentication, error handling
├── domain/         # Business logic (framework-agnostic)
│   ├── order/      # Order creation, state transitions
│   └── payment/    # Payment processing, refunds
├── infra/          # External integrations
│   ├── db/         # Prisma schema, migrations
│   └── external/   # Payment gateway API client
└── config/         # Environment-specific configuration
```

### 6.2 Change Recipes

**Bad example** — No indication of what to change:

```
To add a new API, modify the relevant files.
```

**Good example** — Provides specific steps, paths, and verification points:

```markdown
### Adding a New REST Endpoint

1. Add a route file in `src/api/routes/`
2. Write the business logic function in `src/domain/`
3. Register the route in `src/api/routes/index.ts`
4. Add an integration test in `tests/api/`

Verification: `npm test -- --grep "new endpoint"` passes
Caution: Must apply the permission check middleware in `src/api/middleware/auth.ts`
```

### 6.3 Interfaces / Contracts

**Bad example** — Copying the implementation as-is:

```typescript
// The OrderService class has the methods createOrder, cancelOrder, getOrderById,
// updateOrderStatus, listOrders, getOrderHistory, validateOrder,
// calculateTotal, applyDiscount, sendConfirmation.
// createOrder takes userId, items, shippingAddress and...
// (200+ lines of per-method descriptions follow)
```

**Good example** — Only the contracts that external consumers need to know, kept concise:

```
OrderService core contracts:
- createOrder(userId, items, address) → Order
  - Invariant: Rejects if items is empty
  - Invariant: Inventory deduction is handled within this function as a transaction
  - Side effect: Emits `order.created` event after order creation
- cancelOrder(orderId) → void
  - Invariant: Cannot cancel after SHIPPED status
  - Side effect: Restores inventory, emits `order.cancelled` event
```

### 6.4 Responsibility

**Bad example** — Responsibility only, no non-responsibilities:

```
PaymentService handles payments.
```

**Good example** — Clear boundaries:

```
PaymentService
- Responsibility: Payment gateway API calls, payment status tracking, refund processing
- Non-responsibility: Order status changes (OrderService), notification delivery (NotificationService)
- Note: Payment status and order status synchronization is event-driven. No direct calls.
```

### 6.5 Open Questions

**Bad example** — Describing uncertainties as facts:

```
This system can handle 10,000 requests per second.
```

**Good example** — Explicitly stating what is unknown:

```
## Open Questions
- No load testing has been performed. Actual throughput is unverified.
- Need to verify whether the Redis cache expiration policy aligns with business requirements.
- The rationale for the timeout setting in `external/pg-client.ts` is unclear (currently 30 seconds).
```

---

## 7. How to Use Specs in Large Codebases

### Step 1: Quick Onboarding

Open the main spec to first understand the project goals, system boundary, key components, and runtime flows.

The objective is to grasp "what this repository does" in a short time.

### Step 2: Finding the Starting Point for Changes

To modify a feature, look at the relevant component spec for:

- Which responsibility units are involved
- Which paths to actually look at
- Which contracts must not be broken
- Which tests and operational points to verify together

### Step 3: Assessing Impact Scope

A spec should reveal not only "where to change" but also "how far to look."

The following areas are particularly important for impact assessment:

- API contracts
- Event flows
- State transitions
- Configuration changes
- Batch jobs
- External service integrations

### Step 4: Review and Verification

Code reviews are line-level, but specs are used for system-level verification.

That is, check whether the implementation violates any of the following:

- Goal
- Architecture Overview
- Component contract
- Invariants

### Step 5: Post-Implementation Synchronization

If the architecture, contracts, operational methods, or change paths have changed, the spec must be updated accordingly.

Without updates, specs quickly become outdated wikis.

---

## 8. Spec Update Criteria

Not every code change requires a spec update. Use the following criteria to decide.

### Changes That Require Updates (MUST update)

| Change Type | Example |
|-------------|---------|
| Component added/removed/renamed | New service module added, existing module removed |
| External contract change | API endpoint added/changed, event schema changed |
| Architecture structure change | Directory structure reorganization, new external service integration added |
| Invariant change | State transition rule change, validation condition change |
| Runtime flow change | Sync-to-async conversion, new queue/worker added |
| Environment/dependency change | New environment variable, DB migration, major library replacement |

### Changes That Do Not Require Updates (NO update)

| Change Type | Example |
|-------------|---------|
| Internal implementation refactoring | Improving function internals, renaming variables |
| Bug fix (contract unchanged) | Fixing behavior that did not conform to the existing contract |
| Test addition | Adding tests for existing functionality |
| Performance optimization (interface unchanged) | Query optimization, adding cache (same external behavior) |
| Code style/formatting | Lint fixes, import cleanup |

### Changes That May Require Updates (CONSIDER)

| Change Type | Criteria |
|-------------|----------|
| New internal util/helper added | Update if shared across other components |
| Error handling policy change | Update if the exposed error format changes |
| Configuration value change | Update if behavior changes |
| Dependency library update | Update if it is a major version change |

---

## 9. Principles for Writing Good Specs

### 1. Path-First

Prefer actual file/directory paths, entry points, and symbols over vague descriptions.

### 2. Change-First

Explaining "how it works" is important, but "where to change it" matters more.

### 3. Index-First

The main spec should help find where things are quickly, rather than explain everything at length.

### 4. Split-Friendly

As documentation grows, it should be split into a `main + component specs` structure.

### 5. Decision Traceability

Non-obvious choices should be recorded, however briefly, in `DECISION_LOG.md`.

### 6. Explicit Unknowns

Do not hide what you don't know — write it in `Open Questions`.

### 7. Token-Efficient

When consumed in an LLM context, if the same information can be conveyed in fewer tokens, do so. Tables and lists are better than prose, and reference links are better than repeated explanations.

---

## 10. Anti-Patterns to Avoid

For each anti-pattern, we explain why it is problematic and how to fix it.

| Anti-Pattern | Why It Is a Problem | Alternative |
|--------------|---------------------|-------------|
| Documentation that is nearly a verbatim copy of code | Becomes inconsistent as soon as code changes. Provides no new information when read | Keep only contracts and intent; leave implementation details to the code |
| Documentation that starts with verbose implementation details | Readers give up before understanding the project's purpose | Place Goal/Project Snapshot at the top |
| Documentation without actual paths or symbols | No search starting point, forcing readers to dig through code | Include Owned Paths and Key Symbols for every component |
| Documentation without change points | Cannot answer "I understand, but where do I change things?" | Add a Change Recipes section |
| Documentation that unconditionally includes security/performance details for every project | Irrelevant information obscures what matters. Wastes tokens | Include only items that actually apply to the project |
| Documentation that states uncertain information as fact | Acting on incorrect information can lead to incidents | Separate into Open Questions |
| Documentation that crams everything into a single main document | Exceeds LLM context limits; humans also get lost | Split into main + component specs |
| Documentation not updated after code changes | Over time, creates more confusion than clarity | Synchronize according to the update criteria in Section 8 |

---

## 11. Quality Checklist

You should be able to answer "yes" to most of the following questions.

### Understanding

- Can a new contributor understand the project's purpose within 5 minutes from this document alone?
- Is the system boundary clear?
- Are the major flows presented briefly and clearly?

### Navigation

- Is each major component linked to actual paths or symbols?
- Can you find where to start when modifying a feature?
- Can you find related tests and debugging starting points?

### Stability

- Are important contracts and invariants visible?
- Are high-impact change points exposed?
- Are Known Issues / Risks not hidden?

### Maintainability

- Is the document structure scalable?
- Are uncertainties separated into `Open Questions`?
- Is it clear where to update after code changes?

### LLM Efficiency

- Is the main spec short enough to fit in a single LLM context window?
- Does it use structured formats (tables, lists)?
- Are paths and symbols distinguished with code blocks?
- Is there no redundant duplication of information?

---

## 12. Conclusion

An SDD spec document should not be a "code description" but rather an **operational interface for understanding and safely changing the codebase**.

A good spec must satisfy all of the following:

1. Humans can understand it quickly.
2. Humans and LLMs can locate change points.
3. Non-obvious decisions and constraints are preserved.
4. The impact scope and risk of changes are reduced.
5. It is continuously updated alongside the code.
6. It can be consumed efficiently within LLM context constraints.
