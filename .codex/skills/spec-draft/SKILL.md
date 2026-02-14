---
name: spec-draft
description: This skill should be used when the user asks to "draft spec", "create spec draft", "write requirements", "collect requirements", "spec draft", "스펙 초안", "요구사항 수집", or wants to have a conversation to gather and document feature requests, improvements, or bug reports before updating the main spec.
---

# Spec Draft

> **Simplified Workflow Note**: This skill is part of the **legacy workflow**.
> In the simplified 4-step workflow (`spec -> feature-draft -> implementation -> spec-update-done`),
> this skill's functionality is included in **`feature-draft`**.
> Use `feature-draft` when possible; it combines `spec-draft` + `spec-update-todo` + `implementation-plan` in one step.

대화를 통해 요구사항을 수집하고 `_sdd/spec/user_draft.md` 초안을 작성한다.

## Purpose

- 구현 전 요구사항을 구조화된 문서로 고정한다.
- 이후 `spec-update-todo`가 바로 처리할 수 있는 입력 형식을 만든다.
- 중요한 의사결정은 필요 시 `DECISION_LOG.md` 후보로 분리한다.

## Inputs

- 사용자 대화(현재 세션)
- 기존 초안: `_sdd/spec/user_draft.md` (있으면 이어쓰기 여부 확인)
- 선택 입력: 사용자 제공 메모/문서/코드 단서
- 선택 컨텍스트: `_sdd/spec/DECISION_LOG.md`

## Output

- `_sdd/spec/user_draft.md`
- (선택) 결정 근거 초안: `_sdd/spec/DECISION_LOG.md`에 추가할 제안

## Hard Rules

- 이 스킬은 요구사항 초안 작성에 집중한다. 메인 스펙의 대규모 개편은 하지 않는다.
- 입력이 모호하면 추정하지 말고 사용자에게 직접 질문한다.
- 완료 기준(acceptance criteria) 없는 항목은 완료 처리하지 않는다.

## Workflow

### 1) Draft Context 확인

1. `_sdd/spec/` 디렉토리 및 `user_draft.md` 존재 여부 확인
2. 기존 초안이 있으면 `이어쓰기/정리 후 덮어쓰기` 중 사용자 의도 확인
3. 대상 스펙 파일(있다면) 이름을 기록

### 2) 요구사항 수집

요구사항 유형을 분류하며 수집한다:

- New Feature
- Improvement
- Bug Report
- Component/Config Change

각 항목에서 최소 필수 정보:

- 제목/이름
- 우선순위(또는 심각도)
- 설명(현재 상태와 목표 상태)
- 완료 기준(체크리스트)

### 3) 모호성 해소

아래 상황에서는 반드시 질문한다:

- 기능 범위가 넓거나 충돌 가능성이 있는 경우
- 우선순위가 비어 있는 경우
- 버그 재현 조건/기대 동작이 누락된 경우
- 특정 컴포넌트 영향 범위가 불명확한 경우

상세 질문 패턴은 `references/question-guide.md`를 사용한다.

### 4) Structured Draft 작성

`Spec Update Input` 호환 구조로 작성한다.

최소 섹션:

1. `## New Features`
2. `## Improvements`
3. `## Bug Reports`
4. `## Notes`

항목별 acceptance criteria는 체크리스트(`- [ ]`)로 작성한다.

### 5) 결정 근거 분리(선택)

대화 중 결정/트레이드오프가 확정되면:

- `DECISION_LOG.md` 후보 항목으로 정리
- Context / Decision / Rationale / Impact를 짧게 남김

### 6) 저장 및 마무리

- `user_draft.md` 저장
- 이번 라운드에서 추가/수정된 항목 요약
- 다음 단계로 `spec-update-todo` 실행 제안

## Quality Gates

완료 전 확인:

- 모든 주요 항목에 우선순위/심각도 존재
- 핵심 항목에 acceptance criteria 존재
- 모호한 표현(`빠르게`, `적절히`)이 구체화됨
- 다음 스킬이 바로 읽을 수 있는 구조 유지

## Error Handling

- `_sdd/spec/` 없음: 디렉토리 생성 후 계속 진행
- 기존 초안 충돌: 사용자 선택(병합/교체) 확인
- 정보 부족: 질문 후 임시 TODO 마커로 구분
- 사용자 중단: 현재까지 내용 저장 후 상태 요약

## Integration

권장 흐름:

`spec-draft` -> `spec-update-todo` -> `implementation-plan` -> `implementation`

## References

- `references/question-guide.md`: 유형별 질문 세트 및 인터뷰 순서
- `examples/user_draft.md`: 결과 초안 예시
