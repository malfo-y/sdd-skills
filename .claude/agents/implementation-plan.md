---
name: implementation-plan
description: "Internal agent. Called explicitly by other agents or skills via Agent(subagent_type=implementation-plan)."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Agent"]
model: inherit
---

# Implementation Plan Creation

temporary spec의 delta를 실행 가능한 implementation plan으로 세분화한다.

## Acceptance Criteria

- [ ] `implementation_plan.md`가 생성되었다.
- [ ] 모든 task에 `Target Files`가 있다.
- [ ] `Contract/Invariant Delta`와 `Validation Plan` linkage가 plan에 남아 있다.
- [ ] phase/dependency/risk/open question이 포함되었다.

## Hard Rules

- `_sdd/spec/` 파일은 읽기만 한다.
- 모든 task는 action-oriented title, AC, `Target Files`, dependencies를 가진다.
- delta/validation linkage를 plan에서 잃으면 안 된다.

## Process

### Step 1: Read Inputs

`Read`로 global spec, feature draft, temporary spec, 관련 코드/테스트를 읽는다.

### Step 2: Extract Delta

- `Contract/Invariant Delta`
- `Touchpoints`
- `Validation Plan`

을 추출하고 구현 컴포넌트로 분해한다.

### Step 3: Build Plan

아래 구조를 사용한다.

```markdown
# Implementation Plan
## Overview
## Scope
## Components
## Contract/Invariant Delta Coverage
## Implementation Phases
## Task Details
## Parallel Execution Summary
## Risks and Mitigations
## Open Questions
```

task의 `Technical Notes`에는 관련 `C*`, `I*`, `V*` 링크를 남긴다.

## Final Check

Acceptance Criteria가 모두 만족되었는지 확인한다. 미충족이면 관련 단계로 돌아간다.
