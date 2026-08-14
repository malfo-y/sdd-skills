<!-- 이 파일은 SDD 작업 하네스(AGENTS.md) 정본 템플릿이다.
     정본 = .claude/skills/spec-create/references/; 나머지 3곳(.codex/spec-create, .claude/spec-upgrade, .codex/spec-upgrade references)은 미러다. 수정 시 4곳을 동기화한다.
     아래 SDD-HARNESS 마커 블록이 소비 repo의 AGENTS.md로 들어가는 본문이며, `<…>`는 spec-create/spec-upgrade가 repo 맥락으로 채우는 변수 슬롯이다. 이 관리 주석 자체는 AGENTS.md로 복사하지 않는다. -->
<!-- SDD-HARNESS:START -->
# AGENTS.md — <repo-name> 작업 하네스

> 작업 규약(how). repo의 이해(what/why)·scope·guardrail은 여기 말고 `_sdd/spec/`.

## 0. Spec-Driven Development (SDD) 작업 원칙

- **Separate Truth by Lifetime**: Keep repo-wide decisions in the global spec and change-specific execution detail in temporary artifacts.
- **Evidence Before Promotion**: Promote outcomes to current truth only after goals and acceptance criteria are verified; otherwise keep them planned or unverified.
- **Persist Outcomes, Not Process**: Record concise decisions, results, evidence, and pointers needed for handoff, resumption, or audit; omit reproducible step-by-step narration.

## 1. 작업 시작 시 읽는 순서

1. 이 파일 → 2. `_sdd/spec/main.md` → 3. `_sdd/env.md` → 4. 진행 중인 변경이면 관련 `_sdd/drafts/`·`_sdd/implementation/` temporary spec

## 2. 작업 규약 / 검증 표준

- 테스트: `<test command>` · 린트/타입체크: `<lint command>` (repo 변수, 없으면 줄 삭제)
- 10초 이상 걸리는 테스트는 fixture를 붙여 분리하고, 꼭 필요한 경우에만 돌리도록 설계 및 구현한다.
- Execute → Verify 필수 (문서/스킬 변경은 diff·grep·review가 유효한 검증). 작업을 닫기 전 그 단위를 `_sdd/work_log`에 기록한다(§5).
- 브랜치: 기능 추가/변경 시작 시 `<브랜치 규칙, 예: main에서 feature/fix/exp/... 브랜치>` 생성 후 작업
- 커밋/PR: `<커밋·PR 규칙>` · 코드가 global spec과 어긋나면 코드보다 spec을 먼저 갱신
- ⚠️ `_sdd/env.md`는 커밋되는 파일이다 — 비밀값(API 키·토큰·비밀번호)을 적지 말 것(환경변수/secret manager로 관리). 작업 산출물 중 `_sdd/{discussion,implementation,pipeline,pr}/`는 `.gitignore`로 로컬 전용이고, 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`다(`drafts/`·`work_log/`는 구현 로그 자산).

## 3. SDD 워크플로우

SDD는 사용자의 직간접적 요청에 의해 적용된다 (discussion이나 feature-draft 등의 스킬 호출, "SDD로 구현/작업하자" 같은 사용자 요청 등). 사용자가 요청하지 않았지만 구현하는 기능이 크거나 복잡한 경우, 또는 스펙에 상당한 영향을 주는 작업인 경우에는 SDD 파이프라인을 적용할지 사용자에게 질문한다. 그 외의 경우에는 **비대상**으로 보고 SDD 없이 바로 명령을 수행한다.

SDD 적용 단계 순서: discussion → feature-draft → plan-review → implementation → implementation-review → spec-sync

- 각 단계의 구체 스킬은 **설치된 SDD 스킬**을 사용한다.
- ⚠️ 화살표의 각 단계 이름(discussion·feature-draft·implementation·spec-sync 등)은 **동명의 SDD 스킬**이다. 해당 단계 진입 시 그 스킬을 **호출**하고, 로직을 직접 재구현하지 않는다 — 스킬이 단일 소스다.
- `plan-review`·`implementation-review` 단계는 각각 `feature-draft`·`implementation` 스킬이 자기 품질 게이트로 내부 수행하므로 별도로 호출하지 않는다.
- 스킬 미설치 환경에서만 SDD 개념으로 수동 수행한다. (스킬 카탈로그를 여기 복사하지 않는다 — 최신 스킬셋이 단일 소스이고, 복사본은 스킬 추가·개명을 따라가지 못해 낡은 목록이 실행을 오도한다.)

SDD 파이프라인을 사용하지 않는 경우에도 섹션 2의 작업 규약과 검증 표준을 준수하며, 스펙에 변경이 있으면 `spec-sync`의 호출 여부를 사용자에게 확인받는다.

## 4. 판단 기준이 필요할 때 (가리키기, 복사 금지)

- scope / 경계 → `_sdd/spec/main.md` §`<scope 섹션>`
- 핵심 결정의 '왜' → `_sdd/spec/main.md` §`<decisions 섹션>`
- ⚠️ repo-specific 주의·불변 규칙(이 모듈 read-only 등)은 **여기 말고 spec Guardrails가 단일 소스**다. 이 파일에 적지 말 것 — 두 곳에 적히면 한쪽만 갱신돼 어긋난 규칙이 남는다.

## 5. 작업 기록 (work log)

- 각 작업 단위 종료 시 예외 없이 `_sdd/work_log/<yyyy-mm-dd>.md`에 항목을 append 한다(그날 파일이 없으면 생성). 작업 단위 = SDD 단계(논의·계획·구현·리뷰) 종료, 또는 그 밖의 독립 커밋. *작성*은 항상, 과거 로그 *읽기*만 on-demand(포렌식, §1 읽기 대상 아님).
- 항목: `## <순번/HH:MM> <제목> (<실행 모델명>)` 아래 `무엇/왜` · `결과` · `포인터`(관련 커밋·문서·decision log 링크) · `요약`(따로 남은 게 없을 때만 인라인).
- 모델명은 모든 항목 제목에 병기하고, 게이트를 다른 모델로 돌렸으면 그 수치 옆에도 적는다(예: `plan-review (opus-5): H2 M2`) — 모델별 finding 밀도 비교용.
- 포인터로 충분하면 `요약` 생략(중복 금지). 수동 작업도 포함.
- 이 규약은 커밋 게이트(`.claude/hooks/worklog-gate.sh`, PreToolUse 훅)로 강제된다 — 오늘 로그에 미커밋 변경이 없으면 **세션의 첫 `git commit`이 거부**된다(이후 분할 커밋은 통과). 로그가 불필요한 커밋은 `SDD_SKIP_WORKLOG=1 git commit ...` 로 우회한다.
<!-- SDD-HARNESS:END -->
