---
name: pr-spec-patch
description: This skill should be used when the user asks to "create spec patch from PR", "PR spec patch", "compare PR with spec", "PR to spec", "PR 스펙 패치", "PR 리뷰 준비", "스펙 패치 생성", "PR 변경사항 스펙 반영", or wants to generate a spec patch document by comparing a pull request against the current specification.
version: 1.3.0
---

# pr-spec-patch

## Goal

PR 변경사항을 현재 스펙과 비교해 `_sdd/pr/spec_patch_draft.md`에 spec-update-todo 호환 패치 초안을 만든다. 이 스킬은 스펙을 직접 수정하지 않고, PR 변경을 문서 변경 후보로 구조화하는 데 집중한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: PR 메타데이터와 diff를 수집했다.
- [ ] AC2: baseline spec 또는 baseline 부재 상태를 명확히 기록했다.
- [ ] AC3: `_sdd/pr/spec_patch_draft.md`가 생성되거나 갱신되었다.
- [ ] AC4: patch content가 `spec-update-todo` 입력 형식과 호환된다.
- [ ] AC5: new feature / improvement / bug fix / component/config change / open question이 적절히 분류되었다.
- [ ] AC6: 기존 draft가 있으면 update mode로 갱신했고, 대화 기반 refinement를 반영했다.

## SDD Lens

- PR spec patch는 spec 자체가 아니라 “spec에 반영되어야 할 변경 목록”이다.
- 구현 evidence와 spec baseline 사이의 차이를 구조화해 후속 `pr-review`와 `spec-update-todo`의 입력으로 만든다.
- baseline spec이 없어도 진행할 수 있지만, 신뢰도는 더 낮다.

## Companion Assets

- `references/gh-commands.md`
- `examples/spec_patch_draft.md`

## Hard Rules

1. `_sdd/spec/` 아래 파일은 생성/수정/삭제하지 않는다.
2. 이 스킬의 기본 산출물은 `_sdd/pr/spec_patch_draft.md` 하나다.
3. 스펙 반영은 `/spec-update-todo`로만 수행한다.
4. 대형 patch 초안은 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
5. 대형 PR이나 split spec이면 evidence 수집과 분류를 분리하되, 최종 patch draft는 하나로 통합한다.

## Input Sources

1. `_sdd/spec/` 현재 스펙
2. `gh` CLI 기반 PR 데이터
3. 현재 대화와 사용자 피드백
4. 기존 `_sdd/pr/spec_patch_draft.md`

## Process

### Step 1: Prepare the Baseline

- `gh auth status` 확인
- `_sdd/pr/` 디렉토리 준비
- `_sdd/spec/` baseline 존재 여부 확인
- PR 번호를 명시 입력 또는 현재 브랜치에서 자동 감지

baseline spec가 없으면:

- warning을 남기고 계속 진행
- draft에 `no baseline` 성격을 명시

### Step 2: Collect PR Evidence

다음을 수집한다.

- PR title, body, author, branch, URL
- additions/deletions/changed files
- 주요 diff와 changed files
- 리뷰/코멘트에서 spec 반영이 필요한 포인트

대형 PR이면:

- PR metadata / baseline spec / diff loading을 병렬화
- change categorization을 lane별로 나눌 수 있다

### Step 3: Map PR Changes to Spec Changes

PR evidence를 아래 범주로 분류한다.

- New Features
- Improvements
- Bug Fixes
- Component Changes
- Configuration Changes
- Questions / Suggestions

각 항목에는 가능한 한 다음을 포함한다.

- priority 또는 severity
- target component / spec section
- acceptance criteria
- PR evidence (`file:line` 또는 equivalent)

### Step 4: Write or Update the Draft

초기 생성 모드:

- 새 `_sdd/pr/spec_patch_draft.md` 작성

기존 draft update 모드:

- 기존 draft 읽기
- 사용자 피드백을 `add / modify / remove / regenerate / finalize` 관점으로 반영
- conversation round와 상태를 갱신

초안이 길면 다음 순서를 따른다.

1. patch draft skeleton/섹션 헤더를 직접 작성
2. 같은 흐름에서 evidence와 patch 내용을 채움
3. TODO/placeholder를 제거하고 finalize
4. 의존 섹션은 `default`, 독립 섹션은 `worker`로 채운다

### Step 5: Finalize the Patch Draft

최종 draft가 아래 질문에 답하는지 확인한다.

- PR이 spec에 어떤 영향을 주는가
- 스펙에 반드시 반영해야 할 change는 무엇인가
- 확인이 필요한 ambiguity는 무엇인가
- baseline 또는 근거가 부족한 항목은 무엇인가

## Output Contract

기본 산출물:

- `_sdd/pr/spec_patch_draft.md`

기본 구조:

- PR Summary
- Spec Patch Content
- New Features
- Improvements
- Bug Fixes
- Component Changes
- Configuration Changes
- Notes / Context / Constraints
- Questions and Suggestions

patch content는 `spec-update-todo` 입력으로 재사용 가능해야 한다.

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` 인증 실패 | 인증 필요 사실을 보고하고 중단 |
| spec baseline 없음 | warning을 기록하고 low-confidence patch로 진행 |
| PR 번호 미확정 | 현재 브랜치 기준 자동 감지 시도, 실패 시 사용자 확인 |
| existing draft와 PR 불일치 | mismatch를 경고하고 update 대신 regenerate 권장 |
| diff가 너무 큼 | lane별 evidence 수집 후 최종 draft 통합 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
