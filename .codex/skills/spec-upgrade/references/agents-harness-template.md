<!-- 이 파일은 SDD 작업 하네스(AGENTS.md) 정본 템플릿이다.
     정본 = .claude/skills/spec-create/references/; 나머지 3곳(.codex/spec-create, .claude/spec-upgrade, .codex/spec-upgrade references)은 미러다. 수정 시 4곳을 동기화한다.
     아래 SDD-HARNESS 마커 블록이 소비 repo의 AGENTS.md로 들어가는 본문이며, `<…>`는 spec-create/spec-upgrade가 repo 맥락으로 채우는 변수 슬롯이다. 이 관리 주석 자체는 AGENTS.md로 복사하지 않는다. -->
<!-- SDD-HARNESS:START -->
# AGENTS.md — <repo-name> 작업 하네스

> 작업 규약(how). repo의 이해(what/why)·scope·guardrail은 여기 말고 `_sdd/spec/`.

## 0. 작업 원칙 (모든 작업에 우선)

1. Ask, don't assume. If something is unclear, ask before writing a single line. Never make silent assumptions about intent, architecture, or requirements. When running unattended, pick the most reasonable interpretation, proceed, and record the assumption rather than blocking.

2. Implement the simplest solution for simple problems, better solutions for harder problems. Do not over-engineer or add flexibility that isn't needed yet.

3. Don't touch unrelated code but please do surface bad code or design smells you discover with me so we can address them as a separate issue.

4. Flag uncertainty explicitly. If you're unsure about something, see point 1 above. If it makes sense to do so, conduct a small, localised and low-risk experiment and bring the hypothesis and results to me to discuss. Confidence without certainty causes more damage than admitting a gap.

5. I'm always open to ideas on better ways to do things. Please don't hesitate to suggest a better way, or one that has long lasting impact over a tactical change. (as a few examples)

## 1. 작업 시작 시 읽는 순서

1. 이 파일 → 2. `_sdd/spec/main.md` → 3. `_sdd/env.md` → 4. 진행 중인 변경이면 관련 `_sdd/drafts/`·`_sdd/implementation/` temporary spec

## 2. 작업 규약 / 검증 표준

- 테스트: `<test command>` · 린트/타입체크: `<lint command>` (repo 변수, 없으면 줄 삭제)
- Execute → Verify 필수 (문서/스킬 변경은 diff·grep·review가 유효한 검증)
- 브랜치: 기능 추가/변경 시작 시 `<브랜치 규칙, 예: main에서 feature/fix/exp/... 브랜치>` 생성 후 작업
- 커밋/PR: `<커밋·PR 규칙>` · 코드가 global spec과 어긋나면 코드보다 spec을 먼저 갱신
- ⚠️ `_sdd/env.md`는 커밋되는 파일이다 — 비밀값(API 키·토큰·비밀번호)을 적지 말 것(환경변수/secret manager로 관리). 작업 산출물 중 `_sdd/{discussion,drafts,implementation,pipeline,pr,work_log}/`는 `.gitignore`로 로컬 전용이고, 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`다.

## 3. SDD 워크플로우

이 repo는 SDD를 따른다. 단계 순서:
discussion → feature-draft / temporary spec → (spec-sync) → (implementation-plan) → implementation → review-fix → verify → spec-sync.
괄호 단계(`spec-sync`·`implementation-plan`)는 **대규모 구현용 optional**이다 — 소규모 변경은 생략 가능. `spec-sync`는 단일 스킬로, 구현 전(planned 반영, 조건부)과 구현 후(동기화)에 같은 진입점이 evidence 차이로 동작을 적응하며 최대 2회 호출된다. 각 단계의 구체 스킬은 **설치된 SDD 스킬**을 사용한다. (스킬 카탈로그를 여기 복사하지 않는다 — 최신 스킬셋이 단일 소스다.)

## 4. 판단 기준이 필요할 때 (가리키기, 복사 금지)

- scope / 경계 → `_sdd/spec/main.md` §`<scope 섹션>`
- 핵심 결정의 '왜' → `_sdd/spec/main.md` §`<decisions 섹션>`
- ⚠️ repo-specific 주의·불변 규칙(이 모듈 read-only 등)은 **여기 말고 spec Guardrails가 단일 소스**다. 이 파일에 적지 말 것.

## 5. 작업 기록 (work log)

- 의미 있는 작업 단위를 끝낼 때 `_sdd/work_log/<yyyy-mm-dd>.md`에 항목을 append 한다(그날 파일이 없으면 생성). 포렌식 기록 — §1 읽기 대상 아님, 필요할 때만 on-demand.
- 항목: `## <순번/HH:MM> <제목>` 아래 `무엇/왜` · `결과` · `포인터`(관련 커밋·문서·decision log 링크) · `요약`(따로 남은 게 없을 때만 인라인).
- 포인터로 충분하면 `요약` 생략(중복 금지). `_sdd/pipeline/log_*.md`(autopilot 전용)와 별개 트랙 — 수동 작업도 포함.
<!-- SDD-HARNESS:END -->
