<!-- 이 파일은 SDD 작업 하네스(AGENTS.md) 정본 템플릿이다.
     정본 = .claude/skills/spec-create/references/; 나머지 3곳(.codex/spec-create, .claude/spec-upgrade, .codex/spec-upgrade references)은 미러다. 수정 시 4곳을 동기화한다.
     아래 SDD-HARNESS 마커 블록이 소비 repo의 AGENTS.md로 들어가는 본문이며, `<…>`는 spec-create/spec-upgrade가 repo 맥락으로 채우는 변수 슬롯이다. 이 관리 주석 자체는 AGENTS.md로 복사하지 않는다. -->
<!-- SDD-HARNESS:START -->
# AGENTS.md — <repo-name> 작업 하네스

> 작업 규약(how). repo의 이해(what/why)·scope·guardrail은 여기 말고 `_sdd/spec/`.

## 0. 작업 원칙 (모든 작업에 우선)

- **Think Before Coding**: Don't assume. Don't hide confusion. Surface tradeoffs.
- **Simplicity First**: Minimum code that solves the problem. Nothing speculative.
- **Surgical Changes**: Touch only what you must. Clean up only your own mess.
- **Goal-Driven Execution**: Define success criteria. Loop until verified.

## 1. 작업 시작 시 읽는 순서

1. 이 파일 → 2. `_sdd/spec/main.md` → 3. `_sdd/env.md` → 4. 진행 중인 변경이면 관련 `_sdd/drafts/`·`_sdd/implementation/` temporary spec

## 2. 작업 규약 / 검증 표준

- 테스트: `<test command>` · 린트/타입체크: `<lint command>` (repo 변수, 없으면 줄 삭제)
- Execute → Verify 필수 (문서/스킬 변경은 diff·grep·review가 유효한 검증)
- 브랜치: 기능 추가/변경 시작 시 `<브랜치 규칙, 예: main에서 feature/fix/exp/... 브랜치>` 생성 후 작업
- 커밋/PR: `<커밋·PR 규칙>` · 코드가 global spec과 어긋나면 코드보다 spec을 먼저 갱신

## 3. SDD 워크플로우

이 repo는 SDD를 따른다. 단계 순서:
discussion → feature-draft / temporary spec → (spec-sync) → (implementation-plan) → implementation → review-fix → verify → spec-sync.
괄호 단계(`spec-sync`·`implementation-plan`)는 **대규모 구현용 optional**이다 — 소규모 변경은 생략 가능. `spec-sync`는 단일 스킬로, 구현 전(planned 반영, 조건부)과 구현 후(동기화)에 같은 진입점이 evidence 차이로 동작을 적응하며 최대 2회 호출된다. 각 단계의 구체 스킬은 **설치된 SDD 스킬**을 사용한다. (스킬 카탈로그를 여기 복사하지 않는다 — 최신 스킬셋이 단일 소스다.)

## 4. 판단 기준이 필요할 때 (가리키기, 복사 금지)

- scope / 경계 → `_sdd/spec/main.md` §`<scope 섹션>`
- 핵심 결정의 '왜' → `_sdd/spec/main.md` §`<decisions 섹션>`
- ⚠️ repo-specific 주의·불변 규칙(이 모듈 read-only 등)은 **여기 말고 spec Guardrails가 단일 소스**다. 이 파일에 적지 말 것.
<!-- SDD-HARNESS:END -->
