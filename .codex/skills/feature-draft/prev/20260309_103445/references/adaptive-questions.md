# Adaptive Completion Guide (Non-Interactive)

Deterministic completion rules for handling incomplete feature input without mid-process user questions.

---

## Input Completeness Levels

### HIGH (Detailed Input)

All of these are present:
- Feature name or target is clear
- Description is concrete
- Acceptance criteria are present (or strongly inferable)
- Priority is explicit (or obvious from context)

**Action**:
- Proceed directly.
- Keep only a short assumptions note.

---

### MEDIUM (Partial Input)

Some information exists, but key fields are missing:
- Priority missing, or
- Acceptance criteria weak, or
- Technical constraints unclear

**Action (deterministic inference)**:
1. Infer priority from impact/risk terms and existing backlog style.
2. Infer acceptance criteria from similar implemented features and tests.
3. Infer constraints from stack conventions and existing architecture.
4. Record inferred values with confidence tags in `Open Questions` when confidence is low.

---

### LOW (Vague Input)

Input is idea-level and lacks concrete scope.

**Action (structured expansion)**:
1. Infer requirement type:
   - New Feature
   - Improvement
   - Bug
   - Component Change
   - Environment / Dependency Change
2. Expand into minimum executable draft fields.
3. Continue generation with conservative defaults.
4. Record unresolved assumptions in `Open Questions`.

---

## Required Completion Checklist

Use this checklist to complete missing fields non-interactively:

- Feature name and objective
- Requirement type
- Priority and risk level
- Acceptance criteria (target 3+, minimum 2 when evidence is limited)
- Target components
- Initial `Target Files` candidates
- Dependencies and constraints
- Open assumptions and confidence

---

## Type-Specific Completion Hints

### New Feature
- Define user value first.
- Add concrete success conditions and failure cases.

### Improvement
- Capture current behavior vs desired behavior.
- Include measurable delta (latency, reliability, maintainability, etc.).

### Bug
- Capture reproducible symptom and expected behavior.
- Include severity and blast radius.

### Component Change
- Clarify whether additive or breaking.
- Map affected interfaces and downstream consumers.

### Environment / Dependency Change
- Define whether it affects env vars, runtime, setup commands, or dependencies.
- Define default behavior and rollback behavior.

---

## Confidence and Recording Policy

Use three confidence bands:

- **High**: direct evidence from spec/code/tests
- **Medium**: strong pattern match, minor assumption
- **Low**: weak evidence, fallback inference

For **Medium/Low** items:
- Keep generated draft deterministic.
- Add explicit rationale and follow-up items to `Open Questions`.

---

## Avoiding Rework

- Do not re-derive fields already explicit in source inputs.
- Prefer project-local conventions over generic templates.
- Keep assumptions minimal and testable.
- Never block output waiting for additional user input.
