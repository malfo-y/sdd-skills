---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions "_sdd" directory, specification documents, or project documentation needs.
version: 1.6.0
---

# spec-create

## Goal

프로젝트의 요구사항, 코드베이스, 기존 문서를 바탕으로 `_sdd/spec/` 아래에 SDD 스펙을 만든다. 필요하면 `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` 같은 최소 부트스트랩 파일도 함께 정리해 이후 스킬이 같은 기준으로 작업할 수 있게 한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: `_sdd/spec/` 아래에 canonical spec 파일을 생성했다.
- [ ] AC2: 프로젝트 규모에 맞는 spec 구조를 선택했다. 단일 파일이면 `main.md` 또는 대표 spec, 분할 구조면 index + sub-spec 구성이 명확하다.
- [ ] AC3: 문서에 목표, 아키텍처, 컴포넌트, 사용 흐름, 환경/의존성, 주요 이슈가 포함된다.
- [ ] AC4: 코드베이스가 있으면 스펙이 실제 코드 구조와 naming을 반영하고, 코드베이스가 없으면 speculative 문서임을 명확히 드러낸다.
- [ ] AC5: 필요한 경우에만 `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`를 최소 범위로 생성/보강했다.
- [ ] AC6: `references/`와 `examples/`는 유지되고, 본문은 실행 계약과 작성 기준을 선명하게 설명한다.

## SDD Lens

- spec는 프로젝트의 Single Source of Truth다.
- 이후 `feature-draft`, `implementation-plan`, `spec-summary` 등이 읽을 수 있게 산출물 구조와 용어를 안정적으로 고정해야 한다.
- spec는 코드 설명서가 아니라 “무엇을 만들고 왜 그렇게 설계했는지”를 담는 문서다.

## Companion Assets

- `references/template-compact.md`: 기본 whitepaper 구조
- `references/template-full.md`: richer template
- `examples/simple-project-spec.md`, `examples/complex-project-spec.md`, `examples/additional-specs.md`: output examples

위 자산은 품질을 높이기 위한 companion asset이다. 하지만 본문만 읽어도 입력, 구조 선택, 출력 계약을 이해할 수 있어야 한다.

## Hard Rules

1. `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. 문서 언어는 기존 스펙/문서를 따른다. 기존 스펙이 없으면 한국어를 기본으로 한다.
3. 스펙 출력은 `_sdd/spec/`에만 저장한다.
4. 기존 스펙 파일을 덮어쓰기 전에는 `prev/PREV_<filename>_<timestamp>.md`로 백업한다.
5. `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`는 없을 때 생성하고, 이미 있으면 필수 안내 문구가 빠진 경우에만 최소 수정한다.
6. 거버넌스 문서는 기본적으로 `DECISION_LOG.md`까지만 사용한다. 추가 문서는 사용자 요청 시에만 만든다.
7. 장문 문서가 예상되면 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
8. 중대형 스펙은 canonical index를 먼저 확정한 뒤, 필요 시 하위 spec 작성을 병렬화한다.

## Structure Decision

규모에 따라 아래 중 하나를 선택한다.

- 소규모: `_sdd/spec/main.md` 단일 파일
- 중규모: `_sdd/spec/main.md` + `<component>.md`
- 대규모: `_sdd/spec/main.md` + `<component>/overview.md` 등 계층형 구조

선택 기준:

- 500줄 이하 예상: 단일 파일
- 500~1500줄 예상: index + component files
- 1500줄 초과 예상: index + component directories

코드베이스가 없으면 `Source` 필드는 생략할 수 있다. 코드베이스가 있으면 컴포넌트 설명과 실제 파일/심볼 naming을 최대한 맞춘다.

## Process

### Step 1: Gather Inputs

다음 입력을 우선순위대로 수집한다.

1. 현재 사용자 요청
2. `_sdd/spec/user_draft.md` 또는 사용자 지정 요구사항 파일
3. 기존 README / docs / config / comments
4. 기존 `_sdd/spec/DECISION_LOG.md`
5. 코드베이스 구조와 핵심 엔트리포인트

요구사항이 모호해서 스펙 방향이 크게 달라질 때만 `request_user_input`으로 짧게 보완한다.

### Step 2: Analyze the Project

다음을 파악한다.

- 프로젝트 목표와 해결하려는 문제
- 주요 컴포넌트와 관계
- 기술 스택과 외부 의존성
- 실행/테스트 환경 힌트
- 이미 존재하는 문서 구조와 naming

그 후 사용자에게 핵심 분석 결과를 짧은 표나 요약으로 보여주고 계속 진행한다. 다만 canonical 구조 선택이 매우 불안정할 때만 추가 확인을 요청한다.

### Step 3: Bootstrap Workspace Guidance

필요 시 아래 파일을 보강한다.

- `AGENTS.md`
- `CLAUDE.md`
- `_sdd/env.md`

기본 원칙:

- 없으면 생성
- 있으면 필요한 안내만 최소 추가
- `_sdd/env.md`는 TODO가 있는 최소 실행 가이드라도 남긴다

### Step 4: Write the Spec

`references/template-compact.md` 또는 `references/template-full.md`를 참고해 spec를 작성한다.

장문 spec이면 다음 순서를 따른다.

1. 대상 파일 skeleton/섹션 헤더를 직접 작성
2. 같은 흐름에서 각 섹션 내용을 채움
3. TODO/placeholder를 제거하고 finalize
4. 의존 섹션은 `default`, 독립 파일/섹션은 `worker`로 채운다

기본 포함 요소:

- Background & Motivation
- Core Design
- Architecture Overview
- Component Details
- Usage Guide / Expected Results
- Environment & Dependencies
- Issues & Improvements

중규모 이상이면:

- index 문서에 목표, 구조, 링크를 먼저 고정
- component 문서는 겹치지 않는 파일 경로로 나눠 작성
- 부모가 링크, 용어, 구조 일관성을 최종 검증

### Step 5: Validate and Save

마지막으로 아래를 점검한다.

- spec 구조가 프로젝트 규모에 맞는가
- 목표/아키텍처/컴포넌트/환경/이슈가 빠지지 않았는가
- 코드베이스와 naming/경로가 크게 어긋나지 않는가
- bootstrap 문서가 최소 기준을 충족하는가

## Output Contract

기본 산출물:

- `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`

조건부 산출물:

- `_sdd/spec/<component>.md`
- `_sdd/spec/<component>/...`
- `_sdd/spec/DECISION_LOG.md`
- `AGENTS.md`
- `CLAUDE.md`
- `_sdd/env.md`

spec에는 최소한 아래가 포함되어야 한다.

- 프로젝트 목표와 배경
- 핵심 설계와 구조
- 주요 컴포넌트 설명
- 사용 흐름 또는 기대 결과
- 환경/의존성
- 이슈/개선사항

## Error Handling

| 상황 | 대응 |
|------|------|
| 입력 정보 부족 | `request_user_input`으로 최소 보완 |
| 코드베이스 없음 | greenfield/spec-only 문서로 계속 진행하고 low confidence 영역을 표시 |
| 기존 스펙 존재 | 백업 후 갱신 |
| canonical 구조 불명확 | 후보를 비교하고 사용자 확인 |
| 환경 정보 부족 | `_sdd/env.md`에 TODO 기반 최소 가이드 생성 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
