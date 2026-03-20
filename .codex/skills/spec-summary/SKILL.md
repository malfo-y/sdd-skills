---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a human-readable summary of the current specification for quick understanding.
version: 1.7.0
---

# spec-summary

## Goal

현재 스펙과 구현 상태를 읽어 `_sdd/spec/SUMMARY.md`에 사람이 빠르게 훑을 수 있는 layered summary를 만든다. 필요할 때만 `README.md`의 managed block을 갱신해, 짧은 스냅샷과 전체 요약 문서를 연결한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: `_sdd/spec/SUMMARY.md`를 생성하거나 안전하게 갱신했다.
- [ ] AC2: summary에 프로젝트 목표, 핵심 기능, 구조, 진행 상태, 주요 이슈, 다음 단계가 포함된다.
- [ ] AC3: split spec과 구현 진행 문서가 있으면 이를 반영해 현재 상태를 왜곡 없이 요약했다.
- [ ] AC4: README 갱신은 사용자가 명시적으로 요청한 경우에만 수행했다.
- [ ] AC5: summary와 README는 기존 문서 언어를 따르며, README는 marker block만 갱신했다.
- [ ] AC6: 본문만 읽어도 실행 계약은 이해 가능하고, `references/summary-template.md`와 `examples/summary-output.md`는 품질 향상을 위한 companion asset으로 유지된다.

## SDD Lens

- summary는 스펙의 대체물이 아니라, `_sdd/spec/`를 빠르게 이해하기 위한 안내 문서다.
- summary는 spec, implementation progress, implementation review를 연결해 현재 상태를 설명해야 한다.
- 문서 작성은 간결해야 하지만, 상태/리스크/다음 단계 같은 운영 정보는 빠뜨리면 안 된다.

## Companion Assets

- `references/summary-template.md`: SUMMARY 구조 템플릿
- `examples/summary-output.md`: 완성 예시

긴 문서일수록 위 자산을 적극 활용하되, 본문 자체가 입력 소스와 출력 계약을 설명해야 한다.

## Hard Rules

1. `_sdd/spec/*.md`는 읽기 전용이다. 단, `SUMMARY.md`는 생성/갱신할 수 있다.
2. README 갱신은 사용자가 명시적으로 요청한 경우에만 수행한다.
3. 기존 `SUMMARY.md`가 있으면 `prev/PREV_SUMMARY_<timestamp>.md`로 백업 후 갱신한다.
4. README는 전체를 덮어쓰지 않는다. `spec-summary` marker block만 갱신하거나 없으면 안전하게 추가한다.
5. 문서 언어는 기존 스펙/문서를 따른다. 기존 스펙이 없으면 한국어를 기본으로 한다.
6. summary가 길거나 구조적으로 복잡하면 먼저 `write_skeleton` agent로 skeleton을 만든다. 반환값이 `SKELETON_ONLY`이면 이 skill이 `default` 또는 `worker` agent로 남은 섹션을 채운다.
7. split spec 또는 컴포넌트 수가 많으면 병렬 추출 후 부모가 최종 summary를 통합한다.

## Input Sources

우선순위:

1. `_sdd/spec/main.md` 또는 프로젝트 index spec
2. index spec이 가리키는 sub-spec 파일
3. `_sdd/implementation/IMPLEMENTATION_PROGRESS*.md`
4. `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
5. `README.md` (README sync 요청 시만)
6. `_sdd/env.md` (로컬 검증이 필요할 때만)

주의:

- `SUMMARY.md`와 `prev/PREV_*.md`는 입력 후보에서 제외한다.
- split spec인데 링크가 불명확하면 관련 spec 집합을 사용자에게 확인한다.

## Process

### Step 1: Locate the Spec Set

먼저 index/main spec을 찾고, 필요하면 sub-spec 집합을 결정한다.

- 후보: `_sdd/spec/main.md`, `_sdd/spec/<project>.md`
- split spec이면 index에서 링크된 파일을 우선 사용
- 링크가 불명확하면 `_sdd/spec/<project>_*.md`를 후보로 모아 확인
- implementation progress/review 파일 존재 여부도 함께 확인

스펙이 없으면 `/spec-create`를 먼저 권장하고 종료한다.

### Step 2: Extract the Facts

아래 항목을 스펙과 보조 문서에서 추출한다.

- 프로젝트 이름, 버전, 최근 변경 시점
- 목표와 해결하려는 문제
- 핵심 기능과 현재 상태
- 주요 아키텍처/컴포넌트
- 진행률과 blocker
- 구현 리뷰 결과와 주요 이슈
- 다음 단계 후보

whitepaper 섹션이 있으면 다음을 추가로 활용한다.

- §1 Background & Motivation → why
- §2 Core Design → 핵심 설계 요약
- §5 Usage Guide & Expected Results → 대표 사용 시나리오

### Step 3: Compute Status

상태 마커와 구현 문서를 바탕으로 현재 상태를 계산한다.

- `✅` 완료
- `🚧` 진행중
- `📋` 계획됨
- `⏸️` 보류

기본 completion 계산:

```text
completed / (completed + in-progress + planned)
```

필요하면 구현 progress/review 문서의 최근 상태로 보정한다.

### Step 4: Build the Summary Shape

`SUMMARY.md`는 아래 순서를 기본으로 한다.

1. Executive summary
2. Project motivation / goals
3. Core design highlights (있는 경우)
4. Key feature explanations
5. Architecture snapshot
6. Status dashboard
7. Issues and improvements
8. Recommended next steps

원칙:

- summary는 읽기 쉬운 narrative + 표를 섞는다
- 구현 세부사항은 압축하고, 상태와 의미를 더 강조한다
- 모르는 정보는 추측하지 않고 명시적으로 `Unknown` 또는 open question으로 남긴다

### Step 5: Write `SUMMARY.md`

`references/summary-template.md`를 기반으로 내용을 채우고 `_sdd/spec/SUMMARY.md`를 작성한다.

문서가 길거나 컴포넌트가 많으면:

- 섹션별 핵심 포인트 추출을 병렬 수행
- 부모가 completion, risk, next steps를 통합
- 먼저 `write_skeleton` agent로 `SUMMARY.md` skeleton을 저장
- 결과가 `SKELETON_ONLY`이면 `default` 또는 `worker` agent로 `Sections Remaining`을 채운다

### Step 6: Optional README Sync

사용자가 명시적으로 요청한 경우에만 수행한다.

- `README.md`에 `spec-summary` marker가 있으면 해당 블록만 갱신
- marker가 없으면 새 managed block을 안전하게 추가
- 전체 README는 보존
- README에는 짧은 snapshot만 두고, 자세한 내용은 `_sdd/spec/SUMMARY.md`로 연결

권장 README 블록 요소:

- 프로젝트 한 줄 요약
- 현재 상태
- 핵심 기능 3-5개
- 전체 summary 링크

### Step 7: Final Check

마지막으로 아래를 점검한다.

- summary가 스펙의 핵심을 왜곡 없이 요약하는가
- 진행 상태와 이슈가 최신 문서와 충돌하지 않는가
- README를 요청하지 않았는데 수정하지 않았는가
- backup/marker 규칙을 지켰는가

## Output Contract

기본 산출물:

- `_sdd/spec/SUMMARY.md`

조건부 산출물:

- `README.md`의 `spec-summary` managed block

`SUMMARY.md`에 포함할 핵심 섹션:

- Executive Summary
- Goals / Motivation
- Core Design Highlights (있으면)
- Key Feature Explanations
- Architecture Snapshot
- Status Dashboard
- Issues & Improvements
- Recommended Next Steps

README block 원칙:

- concise snapshot만 제공
- 전체 요약 문서 링크 포함
- unrelated README 내용은 보존

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| split spec 범위 불명확 | 후보를 제시하고 사용자 확인 |
| 구현 문서 없음 | spec만 기준으로 요약하고 상태 신뢰도 낮음을 명시 |
| README 요청이 없는데 README 관련 문서만 있음 | README는 수정하지 않음 |
| README marker 없음 | 새 managed block 추가 |
| 문서가 너무 큼 | `write_skeleton` + caller fill 또는 fan-out으로 분리 작성 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
