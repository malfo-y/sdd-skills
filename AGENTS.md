<!-- SDD-HARNESS:START -->
# AGENTS.md — SDD Skills 작업 하네스

> 작업 규약(how). repo의 이해(what/why)·scope·guardrail은 여기 말고 `_sdd/spec/`.

## 0. 작업 원칙 (모든 작업에 우선)

- **Think Before Coding**: Don't assume. Don't hide confusion. Surface tradeoffs.
- **Simplicity First**: Minimum code that solves the problem. Nothing speculative.
- **Surgical Changes**: Touch only what you must. Clean up only your own mess.
- **Goal-Driven Execution**: Define success criteria. Loop until verified.

네 원칙은 리뷰 단계가 finding의 근거로 인용하는 이름이다(`plan-review`의 `Principle Link`). 이름을 바꾸면 그 인용이 끊긴다.

- 무인 실행(unattended) 중이라 물어볼 수 없으면 막히지 말고, 가장 합당한 해석을 골라 진행하되 그 가정을 기록한다.
- 더 나은 방법이 보이면 제안한다. 전술적 수정보다 오래 가는 개선을 우선한다.

## 1. 작업 시작 시 읽는 순서

1. 이 파일 → 2. `_sdd/spec/main.md` → 3. `_sdd/env.md` → 4. 진행 중인 변경이면 관련 `_sdd/drafts/`·`_sdd/implementation/` temporary spec

## 2. 작업 규약 / 검증 표준

- Execute → Verify 필수 (문서/스킬 변경은 diff·grep·review가 유효한 검증). 작업을 닫기 전 그 단위를 `_sdd/work_log`에 기록한다(§5, 예외 없이). 이 저장소는 전통적 테스트/빌드 프레임워크가 없다(마크다운·SKILL 자산 repo) — 검증은 슬래시 커맨드 실제 호출 + `git diff --check`·diff·grep·review이며, review-only로 닫지 않고 fix 또는 잔여 이슈 보고로 마무리한다.
- 브랜치: 기능 추가/변경 시작 시 main에서 `feat/`·`fix/`·`refactor/`·`docs/`·`chore/` 브랜치 생성 후 작업
- 커밋/PR: Conventional Commits(`/git` 스킬) · 코드가 global spec과 어긋나면 코드보다 spec을 먼저 갱신
- ⚠️ `_sdd/env.md`는 커밋되는 파일이다 — 비밀값(API 키·토큰·비밀번호)을 적지 말 것(환경변수/secret manager로 관리). 작업 산출물 중 `_sdd/{discussion,implementation,pipeline,pr}/`는 `.gitignore`로 로컬 전용이고, 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`다(`drafts/`·`work_log/`는 구현 로그 자산).

## 3. SDD 워크플로우

이 repo는 SDD를 따른다. 단계 순서:
discussion → feature-draft → plan-review → implementation → implementation-review → spec-sync
`spec-sync`는 단일 진입점으로, 분할 draft의 planned todo 고정(조건부)과 구현 후 동기화를 evidence 유무로 구분해 수행한다. 각 단계의 구체 스킬은 **설치된 SDD 스킬**을 사용한다. ⚠️ 화살표의 각 단계 이름(discussion·feature-draft·implementation·spec-sync 등)은 **동명의 SDD 스킬**이다. 해당 단계 진입 시 그 스킬을 **호출**하고, 로직을 직접 재구현하지 않는다 — 스킬이 단일 소스다. 단 `plan-review`·`implementation-review` 단계는 각각 `feature-draft`·`implementation` 스킬이 자기 품질 게이트로 내부 수행하므로 별도로 호출하지 않는다. 스킬 미설치 환경에서만 SDD 개념으로 수동 수행한다. (스킬 카탈로그를 여기 복사하지 않는다 — 최신 스킬셋이 단일 소스다.)

**경량 경로 (light path)**: 아래 셋에 **모두** 해당하는 소규모 변경은 풀 체인 대신 **직접 구현 → 검증 → spec-sync**로 처리해도 된다 — ① 새 contract/invariant가 없다 ② 신규 파일이 없다(work log 제외) ③ 전파 표면(미러·섹션 리터럴·등록 목록)이 전수 열거되고 각각 diff/grep로 검증된다. 하나라도 아니거나 판정이 애매하면 풀 체인이 기본값이다. 새 계약·agent 반환 형식·dispatch 구조 변경, rename/전파류(census 필요), 신규 skill/agent 추가는 항상 풀 체인이다. 경량 경로에서도 브랜치·Execute→Verify(§2)·spec-sync·work log(§5)는 생략하지 않으며, 채택 시 판정 근거 1줄을 work log 항목에 남긴다.

## 4. 판단 기준이 필요할 때 (가리키기, 복사 금지)

- scope / 경계 → `_sdd/spec/main.md` §2. Scope / Non-goals / Guardrails
- 핵심 결정의 '왜' → `_sdd/spec/main.md` §3. 핵심 설계와 주요 결정
- ⚠️ repo-specific 주의·불변 규칙(이 모듈 read-only 등)은 **여기 말고 spec Guardrails가 단일 소스**다. 이 파일에 적지 말 것.

## 5. 작업 기록 (work log)

- 각 작업 단위 종료 시 예외 없이 `_sdd/work_log/<yyyy-mm-dd>.md`에 항목을 append 한다(그날 파일이 없으면 생성). 작업 단위 = SDD 단계(논의·계획·구현·리뷰) 종료, 또는 그 밖의 독립 커밋. *작성*은 항상, 과거 로그 *읽기*만 on-demand(포렌식, §1 읽기 대상 아님).
- 항목: `## <순번/HH:MM> <제목>` 아래 `무엇/왜` · `결과` · `포인터`(관련 커밋·문서·decision log 링크) · `요약`(따로 남은 게 없을 때만 인라인).
- 포인터로 충분하면 `요약` 생략(중복 금지). 수동 작업도 포함.
- 이 규약은 커밋 게이트(`.claude/hooks/worklog-gate.sh`, PreToolUse 훅)로 강제된다 — 오늘 로그에 미커밋 변경이 없으면 **세션의 첫 `git commit`이 거부**된다(이후 분할 커밋은 통과). 로그가 불필요한 커밋은 `SDD_SKIP_WORKLOG=1 git commit ...` 로 우회한다.
<!-- SDD-HARNESS:END -->
