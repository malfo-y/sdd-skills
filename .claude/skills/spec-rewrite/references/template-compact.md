# Rewrite Target Template

## Global Spec Target Shape

```markdown
## 1. Background and High-Level Concept
## 2. Scope / Non-goals / Guardrails
## 3. Core Design and Key Decisions
```

Optional:

- reference notes
- appendix code map
- guide links
- repo-wide invariant note inside guardrails or key decisions
- feature-level guide 안내 (`/guide-create`로 생성 가능)

## Temporary Spec Target Shape

```markdown
# Feature Draft: [title]

> 규모 판정: [판정 근거 1줄 — 값은 "적격" 또는 "분할 필요 — 분할 계획 포함"]

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
[무엇이 왜 바뀌는가. **새 contract/invariant 약속이 생기면 여기 1줄씩 명시한다** — `spec-sync` 스킬이 이 마커 내부를 global spec 반영 입력으로 소비한다.]

## Scope
- **In**: ...
- **Out**: ...
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: [action-oriented title]
[의도 1줄 — 비자명한 근거가 있으면 함께.]

**Contracts** (있을 때만): 이 task가 만드는/바꾸는 약속(인터페이스·불변식)의 정밀 서술.

**Acceptance Criteria**:
- [ ] AC1: ...

**Target Files**:
- [M] `path/to/file` -- 변경 이유
- [C] `path/to/new_file` -- 생성 이유
- ...

# Open Questions
[없으면 섹션 생략. 항목당 1-2줄: 내린 결정 + 사용자 확인 필요 여부.]
```

For an oversized rolling split, Part 1 lists each current/planned feature with one-line intent and scope, while Part 2 details only the current feature.
