---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions "_sdd" directory, specification documents, or project documentation needs.
version: 1.7.0
---

# spec-create

## Goal

프로젝트의 요구사항, 코드베이스, 기존 문서를 바탕으로 `_sdd/spec/` 아래에 현재 SDD canonical model에 맞는 글로벌 스펙을 만든다. 필요하면 `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` 같은 최소 부트스트랩 파일도 함께 정리해 이후 스킬이 같은 기준으로 작업할 수 있게 한다.

글로벌 스펙은 구현 inventory 문서가 아니라 얇고 지속적인 기준 문서다. temporary spec은 이후 `feature-draft`, `implementation-plan`, `spec-update-todo` 계열에서 다루는 실행 청사진이다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: `_sdd/spec/` 아래에 canonical global spec 파일을 생성했다.
- [ ] AC2: 프로젝트 규모에 맞는 spec 구조를 선택했다. 단일 파일이면 `main.md` 또는 대표 spec, 분할 구조면 index + supporting spec 구성이 명확하다.
- [ ] AC3: 글로벌 스펙 본문이 `배경/개념`, `Scope / Non-goals / Guardrails`, `핵심 설계와 주요 결정`, `Contract / Invariants / Verifiability`, `사용 가이드 & 기대 결과`, `Decision-bearing structure`를 포함한다.
- [ ] AC4: 코드베이스가 있으면 스펙이 실제 코드 구조와 naming을 반영하고, strategic code map은 필요 시 manual curated appendix로만 포함한다.
- [ ] AC5: 참조형 정보(`데이터 모델`, `API`, `환경/의존성`)는 필요할 때만 추가되고, 구현 inventory를 본문 기본 구조로 강제하지 않는다.
- [ ] AC6: 필요한 경우에만 `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`를 최소 범위로 생성/보강했다.
- [ ] AC7: `references/`와 `examples/`는 유지되고, 본문은 실행 계약과 작성 기준을 self-contained하게 설명한다.

## SDD Lens

- 글로벌 스펙은 얇은 기준 문서다.
- temporary spec은 delta와 execution을 담는 별도 문서다.
- `Contract / Invariants / Verifiability`는 글로벌 스펙의 독립 필수 축이다.
- architecture/component 정보는 decision-bearing structure 또는 reference information으로 남긴다.
- strategic code map은 appendix-level hint이며, 기본 운영 방식은 manual curated다.

## Companion Assets

- `references/template-compact.md`: 기본 canonical global spec template
- `references/template-full.md`: richer global spec template
- `examples/simple-project-spec.md`, `examples/complex-project-spec.md`, `examples/additional-specs.md`: output examples

위 자산은 품질을 높이기 위한 companion asset이다. 하지만 본문만 읽어도 입력, 구조 선택, 출력 계약을 이해할 수 있어야 한다.

## Hard Rules

1. `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. 문서 언어는 기존 스펙/문서를 따른다. 기존 스펙이 없으면 한국어를 기본으로 한다.
3. 스펙 출력은 `_sdd/spec/`에만 저장한다.
4. 기존 스펙 파일을 덮어쓰기 전에는 `prev/prev_<filename>_<timestamp>.md`로 백업한다.
5. `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`는 없을 때 생성하고, 이미 있으면 필수 안내 문구가 빠진 경우에만 최소 수정한다.
6. 거버넌스 문서는 기본적으로 `decision_log.md`까지만 사용한다. 추가 문서는 사용자 요청 시에만 만든다.
7. 장문 문서가 예상되면 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
8. 중대형 스펙은 canonical index를 먼저 확정한 뒤, 필요 시 하위 spec 작성을 병렬화한다.
9. 코드 citation은 선택적으로 사용한다. 코드 전체를 문서로 복제하지 않는다.

## Structure Decision

규모에 따라 아래 중 하나를 선택한다.

- 소규모: `_sdd/spec/main.md` 단일 파일
- 중규모: `_sdd/spec/main.md` + supporting reference files
- 대규모: `_sdd/spec/main.md` + `<domain>.md` 또는 `<domain>/overview.md` 등 계층형 구조

선택 기준:

- 500줄 이하 예상: 단일 파일
- 500~1500줄 예상: index + supporting files
- 1500줄 초과 예상: index + domain directories

global spec core는 항상 유지한다.

- 1. 배경 및 high-level concept
- 2. Scope / Non-goals / Guardrails
- 3. 핵심 설계와 주요 결정
- 4. Contract / Invariants / Verifiability
- 5. 사용 가이드 & 기대 결과
- 6. Decision-bearing structure

필요 시에만 아래를 추가한다.

- 7. 참조 정보: 데이터 모델 / API / 환경 및 설정
- Appendix A. Strategic Code Map
- Appendix B. 관련 문서 및 코드 레퍼런스

## Process

### Step 1: Gather Inputs

다음 입력을 우선순위대로 수집한다.

1. 현재 사용자 요청
2. `_sdd/spec/user_draft.md` 또는 사용자 지정 요구사항 파일
3. 기존 README / docs / config / comments
4. 기존 `_sdd/spec/decision_log.md`
5. 코드베이스 구조와 핵심 엔트리포인트

요구사항이 모호해서 스펙 방향이 크게 달라질 때만 `request_user_input`으로 짧게 보완한다.

### Step 2: Analyze the Project

다음을 파악한다.

- 프로젝트 목표와 해결하려는 문제
- high-level concept와 핵심 가치
- 주요 경계와 scope / non-goals
- 유지해야 할 설계 결정
- contract/invariant 후보
- 참조형 정보 필요 여부
- strategic code map이 정말 필요한지 여부

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

`references/template-compact.md` 또는 `references/template-full.md`를 참고해 글로벌 스펙을 작성한다.

장문 spec이면 다음 순서를 따른다.

1. 대상 파일 skeleton/섹션 헤더를 직접 작성
2. 같은 흐름에서 각 섹션 내용을 채움
3. TODO/placeholder를 제거하고 finalize
4. 의존 섹션은 `default`, 독립 파일/섹션은 `worker`로 채운다

글로벌 스펙 본문 필수 요소:

- 배경 및 high-level concept
- Scope / Non-goals / Guardrails
- 핵심 설계와 주요 결정
- Contract / Invariants / Verifiability
- 사용 가이드 / 기대 결과
- Decision-bearing structure

조건부 요소:

- 데이터 모델 / API / 환경 및 설정
- Strategic Code Map appendix
- related docs / code references appendix

작성 원칙:

- scope는 기능 목록만이 아니라 책임 범위와 out-of-scope 경계를 같이 고정한다.
- architecture/component inventory는 본문 기본 구조로 강제하지 않는다.
- decision-bearing structure만 남기고, 단순 implementation detail inventory는 코드와 온디맨드 분석에 맡긴다.
- strategic code map은 entrypoint, invariant hotspot, extension point, change hotspot 같은 탐색 힌트만 담는다.

### Step 5: Validate and Save

마지막으로 아래를 점검한다.

- spec 구조가 프로젝트 규모에 맞는가
- 글로벌 스펙 core가 빠지지 않았는가
- CIV table 또는 동등한 구조가 실제 계약을 담고 있는가
- 코드베이스와 naming/경로가 크게 어긋나지 않는가
- strategic code map이 appendix-level hint로 유지되는가
- bootstrap 문서가 최소 기준을 충족하는가

## Output Contract

기본 산출물:

- `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`

조건부 산출물:

- `_sdd/spec/<domain>.md`
- `_sdd/spec/<domain>/...`
- `_sdd/spec/decision_log.md`
- `AGENTS.md`
- `CLAUDE.md`
- `_sdd/env.md`

global spec에는 최소한 아래가 포함되어야 한다.

- 프로젝트 문제와 high-level concept
- scope / non-goals / guardrails
- 핵심 설계와 주요 결정
- Contract / Invariants / Verifiability
- 사용 흐름 또는 기대 결과
- decision-bearing structure

참조 정보와 appendices는 필요할 때만 추가한다.

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
