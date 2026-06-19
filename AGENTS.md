<!-- SDD-HARNESS:START -->
# AGENTS.md — SDD Skills 작업 하네스

> 작업 규약(how). repo의 이해(what/why)·scope·guardrail은 여기 말고 `_sdd/spec/`.

## 0. 작업 원칙 (모든 작업에 우선)
- **Think Before Coding**: Don't assume. Don't hide confusion. Surface tradeoffs.
- **Simplicity First**: Minimum code that solves the problem. Nothing speculative.
- **Surgical Changes**: Touch only what you must. Clean up only your own mess.
- **Goal-Driven Execution**: Define success criteria. Loop until verified.

## 1. 작업 시작 시 읽는 순서
1. 이 파일 → 2. `_sdd/spec/main.md` → 3. `_sdd/env.md` → 4. 진행 중인 변경이면 관련 `_sdd/drafts/`·`_sdd/implementation/` temporary spec

## 2. 작업 규약 / 검증 표준
- 이 저장소는 전통적 테스트/빌드 프레임워크가 없다(마크다운·SKILL 자산 repo). 검증은 슬래시 커맨드 실제 호출 + 문서/스킬 변경은 `git diff --check`·diff·grep·review가 유효한 검증이다
- Execute → Verify 필수 (review-only로 닫지 않고 fix/re-review 또는 잔여 이슈 보고로 마무리)
- 커밋/PR: Conventional Commits(`/git` 스킬) · 코드/스킬이 global spec과 어긋나면 코드보다 spec을 먼저 갱신

## 3. SDD 워크플로우
이 repo는 SDD를 따른다. 단계 순서:
discussion → feature-draft / temporary spec → (spec-sync) → (implementation-plan) → implementation → review-fix → verify → spec-sync
괄호 단계(`spec-sync`·`implementation-plan`)는 **대규모 구현용 optional**이다 — 소규모 변경은 생략 가능. `spec-sync`는 단일 스킬로, 구현 전(planned 반영, 조건부)과 구현 후(동기화)에 같은 진입점이 evidence 차이로 동작을 적응하며 최대 2회 호출된다. 각 단계의 구체 스킬은 **설치된 SDD 스킬**을 사용한다. (스킬 카탈로그를 여기 복사하지 않는다 — 최신 스킬셋이 단일 소스다.)

## 4. 판단 기준이 필요할 때 (가리키기, 복사 금지)
- scope / 경계 → `_sdd/spec/main.md` §2. Scope / Non-goals / Guardrails
- 핵심 결정의 '왜' → `_sdd/spec/main.md` §3. 핵심 설계와 주요 결정
- ⚠️ repo-specific 주의·불변 규칙(이 모듈 read-only 등)은 **여기 말고 spec Guardrails가 단일 소스**다. 이 파일에 적지 말 것.
<!-- SDD-HARNESS:END -->
