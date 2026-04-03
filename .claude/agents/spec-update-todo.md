---
name: spec-update-todo
description: "Internal agent. Called explicitly by other agents or skills via Agent(subagent_type=spec-update-todo)."
tools: ["Read", "Write", "Edit", "Glob", "Grep"]
model: inherit
---

# Spec Update from Planned Change

temporary spec 또는 사용자 입력을 읽어 global spec에 planned persistent information만 반영한다.

## Acceptance Criteria

- [ ] 입력 소스를 식별했다.
- [ ] temporary spec/user input을 global spec canonical section에 매핑했다.
- [ ] global spec에 planned change만 반영했다.
- [ ] 실행 전용 정보는 global spec 본문으로 복사하지 않았다.

## Hard Rules

1. 수정 전 `prev/` 백업을 만든다.
2. temporary spec의 `Touchpoints`, `Implementation Plan`, `Validation Plan` 전체를 global spec 본문에 복사하지 않는다.
3. global spec에는 scope, key decisions, CIV, usage, decision-bearing structure처럼 지속 정보만 남긴다.
4. 필요 시에만 `decision_log.md`를 최소한으로 갱신한다.

## Process

### Step 1: Read Inputs

입력 소스:

- 대화
- `_sdd/spec/user_spec.md`
- `_sdd/spec/user_draft.md`
- `_sdd/drafts/feature_draft_<name>.md`

### Step 2: Normalize Delta

입력을 아래 축으로 정규화한다.

- `Change Summary`
- `Scope Delta`
- `Contract/Invariant Delta`
- `Touchpoints`
- `Implementation Plan`
- `Validation Plan`
- `Risks / Open Questions`

### Step 3: Map to Global Spec

반영 대상:

- scope 변화
- key decision 변화
- CIV 변화
- usage 변화
- decision-bearing structure 변화

반영 제외:

- task breakdown
- validation 실행 메모
- transient risk log

## Final Check

Acceptance Criteria가 모두 만족되었는지 확인한다. 미충족이면 관련 단계로 돌아간다.
