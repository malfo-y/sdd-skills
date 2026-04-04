---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a human-readable summary of the current specification for quick understanding.
version: 1.9.0
---

# spec-summary

## Goal

현재 스펙과 구현 상태를 읽어 `_sdd/spec/summary.md`에 사람이 빠르게 훑을 수 있는 layered summary를 만든다. 필요할 때만 `README.md`의 managed block을 갱신해, 짧은 스냅샷과 전체 요약 문서를 연결한다.

global summary는 현재 thinner global model을 반영해야 한다. 즉 글로벌 스펙은 `개념 + 경계 + 결정` 중심으로, temporary spec은 `change delta + touchpoints + implementation/validation + risks` 중심으로 요약한다.

## Acceptance Criteria

- [ ] `_sdd/spec/summary.md`를 생성하거나 안전하게 갱신했다.
- [ ] 대상 문서가 global spec인지 temporary spec인지 먼저 판별했다.
- [ ] global spec이면 concept, scope/non-goals/guardrails, key decisions를 왜곡 없이 요약했다.
- [ ] temporary spec이면 change summary, scope delta, contract/invariant delta, touchpoints, implementation/validation, risks를 왜곡 없이 요약했다.
- [ ] split spec과 구현 진행 문서가 있으면 이를 반영해 현재 상태를 요약했다.
- [ ] README 갱신은 사용자가 명시적으로 요청한 경우에만 수행했다.

## SDD Lens

- summary는 spec의 대체물이 아니라, `_sdd/spec/`를 빠르게 이해하기 위한 안내 문서다.
- global spec summary는 "이 프로젝트를 어떤 개념과 경계와 결정으로 읽어야 하는가"를 빠르게 잡아줘야 한다.
- temporary spec summary는 "이번 변경이 무엇을 바꾸고 어떻게 검증되는가"를 빠르게 잡아줘야 한다.
- global summary는 delegated-out information이 무엇인지도 짧게 알려줄 수 있지만, usage/CIV snapshot을 기본 shape로 강제하지 않는다.

## Companion Assets

- `references/summary-template.md`: summary 구조 템플릿
- `examples/summary-output.md`: 완성 예시

## Hard Rules

1. `_sdd/spec/*.md`는 읽기 전용이다. 단, `summary.md`는 생성/갱신할 수 있다.
2. README 갱신은 사용자가 명시적으로 요청한 경우에만 수행한다.
3. 기존 `summary.md`가 있으면 `prev/prev_summary_<timestamp>.md`로 백업 후 갱신한다.
4. README는 전체를 덮어쓰지 않는다. `spec-summary` marker block만 갱신하거나 없으면 안전하게 추가한다.
5. 문서 언어는 기존 스펙/문서를 따른다. 기존 스펙이 없으면 한국어를 기본으로 한다.
6. summary가 길거나 구조적으로 복잡하면 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
7. split spec 또는 컴포넌트 수가 많으면 병렬 추출 후 부모가 최종 summary를 통합한다.

## Input Sources

우선순위:

1. 사용자 지정 spec 경로
2. `_sdd/spec/main.md` 또는 프로젝트 index spec
3. index spec이 가리키는 sub-spec 파일
4. `_sdd/implementation/implementation_progress*.md`
5. `_sdd/implementation/implementation_review.md`
6. `README.md` (README sync 요청 시만)
7. `_sdd/env.md` (로컬 검증이 필요할 때만)

## Process

### Step 1: Locate the Spec Set

먼저 index/main spec을 찾고, 필요하면 sub-spec 집합을 결정한다.

### Step 2: Determine Spec Kind

판별 기준:

- global spec 신호: `배경`, `Scope / Non-goals / Guardrails`, `핵심 설계와 주요 결정`
- temporary spec 신호: canonical temporary 7섹션

혼합 문서라면 dominant purpose를 기준으로 정하고, 나머지는 notes로 정리한다.

### Step 3: Extract the Facts

global spec이면 아래를 추출한다.

- 프로젝트 이름, 버전, 최근 변경 시점
- 문제와 high-level concept
- scope / non-goals / guardrails
- 핵심 설계와 주요 결정
- 필요 시 repo-wide invariant note
- delegated-out information note

temporary spec이면 아래를 추출한다.

- change summary
- scope delta
- contract/invariant delta
- touchpoints
- implementation plan highlights
- validation linkage
- risks / open questions

구현 문서가 있으면 현재 상태, blocker, next step을 함께 추출한다.

### Step 4: Compute Status

상태 마커와 구현 문서를 바탕으로 현재 상태를 계산한다.

- `완료`
- `진행중`
- `계획됨`
- `보류`

### Step 5: Build the Summary Shape

global spec summary 기본 순서:

1. Executive Summary
2. Problem / High-Level Concept
3. Scope / Non-goals Snapshot
4. Key Decisions / Guardrails
5. Delegated-Out Information Note
6. Status / Issues / Next Steps

temporary spec summary 기본 순서:

1. Executive Summary
2. Change Summary
3. Scope Delta
4. Contract / Invariant Delta Snapshot
5. Touchpoints
6. Implementation / Validation Snapshot
7. Risks / Open Questions

### Step 6: Write `summary.md`

`references/summary-template.md`를 기반으로 내용을 채우고 `_sdd/spec/summary.md`를 작성한다.

### Step 7: Optional README Sync

사용자가 명시적으로 요청한 경우에만 수행한다.

### Step 8: Final Check

- summary가 스펙 kind에 맞는 shape를 가졌는가
- 핵심 신호를 놓치지 않았는가
- 진행 상태와 이슈가 최신 문서와 충돌하지 않는가
- README를 요청하지 않았는데 수정하지 않았는가

## Output Contract

기본 산출물:

- `_sdd/spec/summary.md`

조건부 산출물:

- `README.md`의 `spec-summary` managed block

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `$spec-create` 먼저 권장 |
| split spec 범위 불명확 | 후보를 제시하고 사용자 확인 |
| 구현 문서 없음 | spec만 기준으로 요약하고 상태 신뢰도 낮음을 명시 |
| global/temporary 판별 모호 | dominant purpose를 기준으로 판단하고 notes에 기록 |
| README 요청이 없는데 README 관련 문서만 있음 | README는 수정하지 않음 |
| 문서가 너무 큼 | caller가 skeleton을 먼저 저장한 뒤 같은 흐름에서 fill 또는 bounded fan-out |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
