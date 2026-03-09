---
name: pr-spec-patch
description: This skill should be used when the user asks to "create spec patch from PR", "PR spec patch", "compare PR with spec", "PR to spec", "PR 스펙 패치", "PR 리뷰 준비", "스펙 패치 생성", "PR 변경사항 스펙 반영", or wants to generate a spec patch document by comparing a pull request against the current specification.
version: 1.3.0
---

# PR Spec Patch

PR 변경사항을 탐색형 스펙 기준으로 해석해 `_sdd/pr/spec_patch_draft.md` 초안을 만든다.

이 스킬의 목적은 "무엇이 바뀌었는가"만 적는 것이 아니라, 아래를 스펙 관점에서 정리하는 것이다.

- 어떤 섹션이 바뀌어야 하는가
- 어떤 컴포넌트와 경로가 영향받는가
- `Repository Map`, `Runtime Map`, `Component Index`, `Common Change Paths`가 갱신되어야 하는가
- `Component Details > Overview` 또는 why-context 설명이 갱신되어야 하는가
- 구현은 되었지만 아직 문서화되지 않은 리스크나 미확인 사항이 있는가

## Hard Rules

1. `_sdd/spec/` 아래 실제 스펙은 수정하지 않는다.
2. 이 스킬의 산출물은 `_sdd/pr/spec_patch_draft.md` 초안뿐이다.
3. 초안은 `spec-update-todo`가 소비할 수 있는 구조를 유지해야 한다.
4. 각 패치 항목에는 가능하면 `PR Evidence`(`file:line`)가 있어야 한다.
5. 대상 섹션이 불명확하면 억지로 단정하지 말고 `Target Section TBD`와 `Open Questions`로 남긴다.
6. 기본 언어는 한국어다.
7. 모든 PR이 스펙 업데이트를 요구하는 것은 아니다. 항목별로 `MUST update / CONSIDER / NO update`를 명시한다.
8. 빈 선택 섹션은 만들지 않는다. 초안은 token-efficient 해야 한다.

## Inputs

- 현재 스펙: `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`
- 링크된 컴포넌트 스펙
- 필요 시 `_sdd/spec/DECISION_LOG.md`
- PR 메타데이터와 diff (`gh`)
- 기존 `_sdd/pr/spec_patch_draft.md` (있으면 update mode)

## Spec Mapping Rules

PR 변경을 아래 축으로 먼저 분류한다.

| 변경 유형 | 기본 타겟 섹션 |
|----------|---------------|
| 사용자 가치/기능 추가 | `Goal` |
| 시스템 경계/구조 변화 | `Architecture Overview` |
| 경로/디렉터리/런타임 흐름 변화 | `Repository Map`, `Runtime Map` |
| 컴포넌트 책임/소유 경로 변화 | `Component Details`, 컴포넌트 스펙 |
| 컴포넌트 동작 방식/설계 의도 변화 | `Component Details > Overview` |
| 운영/디버깅/테스트 시작점 변화 | `Usage Examples` > `Common Change Paths` |
| 설정/필수 서비스 변화 | `Environment & Dependencies` |
| 미확정 설계/후속 검토 필요 | `Open Questions` |
| 중요한 이유/트레이드오프 변화 | `DECISION_LOG.md` 제안 |

## Process

### Step 1: Verify prerequisites

1. `gh auth status` 확인
2. `_sdd/pr/` 디렉터리 준비
3. PR 번호 자동 감지
4. 메인 스펙 존재 여부 확인

스펙이 없으면:
- 경고를 남기고 baseline 없이 진행
- 패치 초안에 `No baseline`을 명시
- `Open Questions`에 `/spec-create` 권장 메모 추가

### Step 2: Load baseline spec context

1. `_sdd/spec/main.md`를 우선 읽는다.
2. 없으면 `_sdd/spec/<project>.md`를 읽는다.
3. 메인 스펙 링크를 따라 관련 컴포넌트 스펙만 읽는다.
4. 생성물/백업 파일은 제외한다.
5. 필요한 경우 `DECISION_LOG.md`를 읽어 why-context를 확인한다.

핵심적으로 아래를 추출한다.

- `Goal`
- `Architecture Overview`
- `Repository Map`
- `Runtime Map`
- `Component Index`
- `Component Overview`
- `Common Change Paths`
- `Open Questions`

### Step 3: Collect PR evidence

기본 명령은 [`references/gh-commands.md`](references/gh-commands.md)를 따른다.

수집할 정보:

- PR 제목, 작성자, 브랜치, 상태
- changed files 목록
- 핵심 diff
- 테스트/CI 상태가 보이면 함께 기록

### Step 4: Map PR changes to spec impact

각 변경에 대해 아래를 정리한다.

- `Change Type`: Feature / Improvement / Bug Fix / Refactor / Infra
- `Spec Update Classification`: `MUST update` / `CONSIDER` / `NO update`
- `Target Section`
- `Target File`
- `Affected Components`
- `Related Paths / Symbols`
- `Current State`
- `Proposed Spec Update`
- `Risks / Invariants`
- `Test / Observability Notes`
- `PR Evidence`

특히 다음은 별도로 확인한다.

- 새 디렉터리/파일/엔트리포인트가 생겼는가
- 기존 흐름에 새 단계나 사용자 관점 설명 변화가 추가되었는가
- 컴포넌트 책임 경계가 달라졌는가
- 컴포넌트가 어떻게 동작하는지 또는 왜 이런 구조를 택했는지 설명이 달라졌는가
- 디버깅/운영 경로가 달라졌는가
- 기존 `Open Questions`를 해소하거나 새 질문을 만드는가

분류 기준:

- `MUST update`: 런타임 흐름, 시스템 경계, 컴포넌트 책임, 외부 계약, 변경 시작점이 달라짐
- `CONSIDER`: 디버깅 경로, 테스트/관측 포인트, why-context가 더 있으면 유용함
- `NO update`: 내부 리팩터링, 테스트 추가, 탐색성과 계약을 바꾸지 않는 변경

### Step 5: Write patch draft

초안은 아래 레이어를 가진다.

1. PR 요약
2. 탐색형 스펙 영향 요약
3. `Spec Update Input` 호환 패치 항목
4. `Open Questions`
5. `Next Recommended Actions`

모든 항목이 `NO update`라면, no-op 초안을 허용한다. 이 경우 왜 스펙 갱신이 불필요한지 근거를 남긴다.

### Step 6: Update mode

기존 초안이 있으면 아래 중 하나로 처리한다.

- refine: 항목 표현 수정
- add: 누락된 PR 영향 추가
- remove: 잘못된 항목 제거
- regenerate: PR 데이터를 다시 읽고 전체 재생성
- finalize: 현재 초안을 확정 상태로 정리

## Output Requirements

좋은 패치 초안은 아래를 만족한다.

- 섹션명만이 아니라 실제 파일/컴포넌트까지 연결된다.
- `Runtime Map`, `Component Index`, `Component Details > Overview` 반영 필요 여부가 드러난다.
- `Common Change Paths` 갱신 필요 여부가 보인다.
- 구현은 되었지만 스펙상 불명확한 부분이 `Open Questions`로 분리된다.
- evidence 없는 항목은 명시적으로 low-confidence 처리한다.
- `DECISION_LOG.md`로 보낼 가치가 있는 이유 변화는 `Decision-Log Candidates`로 분리한다.

## Example

예시는 [`examples/spec_patch_draft.md`](examples/spec_patch_draft.md)를 따른다.
