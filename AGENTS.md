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
- Execute → Verify 필수 (review-only로 닫지 않고 fix/re-review 또는 잔여 이슈 보고로 마무리). 작업을 닫기 전 그 단위를 `_sdd/work_log`에 기록한다(§5, 예외 없이).
- 커밋/PR: Conventional Commits(`/git` 스킬) · 코드/스킬이 global spec과 어긋나면 코드보다 spec을 먼저 갱신
- ⚠️ `_sdd/env.md`는 커밋되는 파일이다 — 비밀값(API 키·토큰·비밀번호)을 적지 말 것(환경변수/secret manager로 관리).

## 3. SDD 워크플로우
이 repo는 SDD를 따른다. 단계 순서:
discussion → feature-draft / temporary spec → (spec-sync) → implementation → review-fix → verify → spec-sync
괄호 단계(`spec-sync`)는 **대규모 구현용 optional**이다 — 소규모 변경은 생략 가능. `spec-sync`는 단일 스킬로, 구현 전(planned 반영, 조건부)과 구현 후(동기화)에 같은 진입점이 evidence 차이로 동작을 적응하며 최대 2회 호출된다. 각 단계의 구체 스킬은 **설치된 SDD 스킬**을 사용한다. ⚠️ 화살표의 각 단계 이름(discussion·feature-draft·implementation·spec-sync 등)은 **동명의 SDD 스킬**이다. 해당 단계 진입 시 그 스킬을 **호출**하고, 로직을 직접 재구현하지 않는다 — 스킬이 단일 소스다. 스킬 미설치 환경에서만 SDD 개념으로 수동 수행한다. (스킬 카탈로그를 여기 복사하지 않는다 — 최신 스킬셋이 단일 소스다.)

## 4. 판단 기준이 필요할 때 (가리키기, 복사 금지)
- scope / 경계 → `_sdd/spec/main.md` §2. Scope / Non-goals / Guardrails
- 핵심 결정의 '왜' → `_sdd/spec/main.md` §3. 핵심 설계와 주요 결정
- ⚠️ repo-specific 주의·불변 규칙(이 모듈 read-only 등)은 **여기 말고 spec Guardrails가 단일 소스**다. 이 파일에 적지 말 것.

## 5. 작업 기록 (work log)
- 각 작업 단위 종료 시 예외 없이 `_sdd/work_log/<yyyy-mm-dd>.md`에 항목을 append 한다(그날 파일이 없으면 생성). 작업 단위 = SDD 단계(논의·계획·구현·리뷰) 종료, 또는 그 밖의 독립 커밋. *작성*은 항상, 과거 로그 *읽기*만 on-demand(포렌식, §1 읽기 대상 아님).
- 항목: `## <순번/HH:MM> <제목>` 아래 `무엇/왜` · `결과` · `포인터`(관련 커밋·문서·decision log 링크) · `요약`(따로 남은 게 없을 때만 인라인).
- 포인터로 충분하면 `요약` 생략(중복 금지). `_sdd/pipeline/log_*.md`(autopilot 전용)와 별개 트랙 — 수동 작업도 포함.
<!-- SDD-HARNESS:END -->
