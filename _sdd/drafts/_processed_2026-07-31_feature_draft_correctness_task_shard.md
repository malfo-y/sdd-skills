# Feature Draft: implementation-review correctness reviewer의 task 단위 분할 dispatch (1+N)

> 규모 판정: 적격 — 변경 파일 4개(orchestrator SKILL 미러 2벌 + docs 가이드 ko/en 각 1줄) + read-only census 1개, 변경 요소↔task 대응이 1:1로 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

implementation-review 게이트의 벽시계는 correctness reviewer 단독이 결정한다(오늘 5회차 실측 214~430s; simplicity 177~252s는 병렬 그늘 안). correctness의 시간 분해(transcript 실측)는 검증 루프(AC 단위 tool 턴) 65~80% + 최종 리포트 19~35%로, **둘 다 task 경계로 나뉜다** — 2분할 시 430s → ~220s(-45%) 예측. 분할 축이 task인 근거는 기존 불변식이다: feature-draft 규칙이 "task는 자기 AC만으로 완료 판정이 닫히는 실행 단위"를 보증하고 plan-review가 그 경계를 감시한다.

- **새 contract**: `implementation-review` orchestrator는 기준 draft의 Part 2 task가 **2개 이상이면 correctness를 task별 shard로 분할 dispatch**한다(1+N). shard k의 digest = 공통 digest + Task k의 AC·Target Files로 범위 한정. simplicity는 항상 통짜 1회. 전부 한 메시지에서 병렬 dispatch.
- **새 contract (relay)**: correctness AC ledger는 shard 반환의 연접이다(task별 AC 집합이 서로소이므로 누락 없이 합쳐진다). 합산 severity 요약은 N+1개 반환 전부를 합산한다. task들이 같은 파일을 만져 중복 finding이 나와도 orchestrator는 전부 relay하고 dedup하지 않는다 — dedup은 fix 주체(호출자)가 자연 흡수한다.
- **불변**: reviewer agent 본문 무변경 — shard 범위는 digest의 "호출자 지정" 경로로 기존 계약(기준 문서 적응 1번)에 이미 들어온다. review-only 경계·병렬 안전성 근거(read-only leaf)·비분할 경로(task 1개 또는 draft 없음 → 현행 1+1) 유지.
- **simplicity는 분할하지 않는다**: (1) 병렬 그늘 안이라 벽시계 이득 0, (2) 중복 탐지 렌즈는 두 지점을 같이 봐야 해서 task 분할이 렌즈 본질을 자른다.
- **분할 상한은 두지 않는다**: draft 분할 규칙이 task 수를 소수로 유지하고, simplicity(~177s)가 자연 바닥이라 상한 문면은 사변적이다(YAGNI).
- **spec 인계 표면**: `components.md`의 implementation-review 행과 `main.md`의 2-렌즈 서술(«직교 2-렌즈 review의 현재 적용 지점은 PR review» — implementation-review도 적용 지점이므로 stale 후보)은 spec-sync가 갱신한다. `docs/AUTOPILOT_GUIDE.md` ko/en의 "2-reviewer" 한 줄은 spec-sync 밖 표면이므로 이 feature가 직접 소유한다(Task 3).

## Scope

- **In**: `.claude/skills/implementation-review/SKILL.md` + `.codex/skills/implementation-review/SKILL.md`의 실행 절차 문면(분할 조건·shard digest·dispatch·relay) 변경. codex는 **3-way 적응**이다 — 두 미러는 byte-identical이 아니며(codex는 spawn_agent/wait_agent 어댑터 보유), 규칙 내용만 공통이고 표현은 런타임별이다. 추가로 `docs/AUTOPILOT_GUIDE.md`·`docs/en/AUTOPILOT_GUIDE.md`의 "2-reviewer" 서술 각 1줄(82행) 갱신.
- **Out**:
  - reviewer agent 본문(`.claude/agents/*.md`·`.codex/agents/*.toml`) 무변경.
  - `pr-review` SKILL 2벌 무변경 — 같은 "2-Reviewer Orchestrator" 패턴이지만 별도 스킬이고 이번 대상 아님.
  - `implementation` SKILL 무변경 — 마감 §3의 "implementation-review 스킬 1회" 문면은 orchestrator 내부 분할과 무충돌.
  - simplicity 분할·분할 수 상한·plan-review 2-렌즈 분할(별건 후보, 기대값 ~30%)은 넣지 않는다.
  - 행동 효과(벽시계 절감)의 스킬 문면 경유 검증은 범위 밖 — 단 이 feature의 구현 게이트에서 메인 루프가 수동 1+N dispatch로 파일럿 실측한다(Open Questions).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: claude orchestrator SKILL에 task 분할 dispatch 문면 반영

기존 "두 reviewer 병렬 dispatch"를 "correctness shard N + simplicity 1, 한 메시지 병렬 dispatch"로 바꾼다.

**Contracts**:
- **분할 조건**: 기준 draft의 Part 2 task가 2개 이상이면 correctness를 task별로 나눈다. shard k의 digest는 공통 digest에 Task k의 AC·Target Files 범위 한정을 더한 것이다. task가 1개이거나 draft 없이(대화 digest 기반) 호출되면 현행(correctness 1 + simplicity 1) 그대로다.
- **simplicity 통짜 유지**: simplicity dispatch는 분할하지 않고 전체 변경을 본다 — 근거(중복 렌즈는 두 지점을 같이 봐야 한다)를 문면에 1줄 남긴다.
- **relay**: correctness AC ledger는 shard 반환의 연접(모든 task의 AC가 정확히 한 shard에 속한다), 합산 severity 요약은 모든 반환(N+1) 합산. 중복 finding dedup은 넣지 않는다 — fix 주체 소관을 명시.
- **보존**: "한 메시지에서" 병렬 dispatch, review-only 경계(«relay만 한다», «합산 요약은 relay이지 gating이 아니다»), 병렬 안전성 근거 섹션(read-only leaf — N개로 자연 확장), Model override(적용 대상 표현만 "두 reviewer 호출 모두" → 모든 reviewer 호출로 일반화, 동작 불변).
- **표기 정리**: reviewer 인스턴스 수를 고정하는 표현(`두 reviewer`·`두 개의 형제`·`2-Reviewer`)은 제거하고, 렌즈 서술은 2-렌즈(correctness/clarity)로 유지한다.

**Acceptance Criteria**:
- [ ] AC1: 분할 조건 앵커가 있다 — `task가 2개 이상`(조건) + `task별`(축) + shard digest 한정 앵커(`해당 task의 AC`와 `Target Files`)가 모두 존재.
- [ ] AC2: dispatch 단계에 `한 메시지`가 보존되고, correctness의 shard별 dispatch와 simplicity 1회(전체 변경 대상)가 모두 서술된다. simplicity 비분할 근거 1줄이 존재한다.
- [ ] AC3: 비분할 경로가 명시된다 — task 1개 또는 draft 없음이면 현행 dispatch라는 문장.
- [ ] AC4: relay 문면에 ledger 연접(모든 AC가 정확히 한 shard 소속)과 합산 severity의 대상이 모든 반환임이 있고, dedup을 fix 주체 소관으로 명시한다.
- [ ] AC5: 경계 앵커 보존 — `relay만 한다`·`합산 요약은 relay이지 gating이 아니다`·병렬 안전성 근거 섹션(`read-only leaf`)이 그대로 남는다.
- [ ] AC6: 고정 표기 잔존 0건 — `두 reviewer`·`두 개의 형제`·`2-Reviewer`가 이 파일에서 0건.

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md` -- orchestrator 실행 절차 변경

### Task 2: codex orchestrator SKILL에 동일 규칙 3-way 적응 반영

Task 1과 같은 규칙 내용을 codex 적응 delta(spawn_agent/wait_agent/close_agent, framed payload, Subagent model override)를 보존한 채 반영한다. 단순 복사 금지 — 기존 codex 고유 표면 위에 규칙만 얹는다.

**Contracts**: Task 1의 Contracts와 동일한 규칙 앵커가 존재하되, dispatch·수거 표현은 codex 문법이다 — correctness shard N개를 `spawn_agent`로 각각 spawn하고 `wait_agent` targets에 N+1개 id를 넣는다. codex 고유 섹션(Codex Runtime Adapter·Agent Message Boundary)은 무손실.

**Acceptance Criteria**:
- [ ] AC1: Task 1의 AC1~AC4와 동일한 규칙 앵커(분할 조건·shard digest 한정·비분할 경로·연접/합산/dedup 소관)가 이 파일에도 존재.
- [ ] AC2: codex 고유 앵커 보존 — `spawn_agent`·`wait_agent`·`close_agent`·`Runtime Boundary`·`Input Data`가 그대로 남고, `wait_agent`의 targets 서술이 shard 복수를 반영한다(고정 2개 id 열거가 아님).
- [ ] AC3: 고정 표기 잔존 0건 — `두 reviewer`·`두 개의 형제`·`2-Reviewer`가 이 파일에서 0건.
- [ ] AC4: 경계 앵커 보존 — `relay만 한다`·`합산 요약은 relay이지 gating이 아니다`·병렬 안전성 근거가 그대로 남는다.

**Target Files**:
- [M] `.codex/skills/implementation-review/SKILL.md` -- codex 미러 3-way 적응

### Task 3: docs 가이드 ko/en의 reviewer 구성 서술 갱신

`docs/AUTOPILOT_GUIDE.md`(ko)·`docs/en/AUTOPILOT_GUIDE.md`(en) 82행의 "correctness ∥ simplicity 2-reviewer" 서술이 구현 후 stale이 된다 — spec-sync 밖 표면이라 이 feature가 직접 갱신한다.

**Contracts**: 각 파일에서 해당 1줄만 수정한다 — reviewer 인스턴스 수 고정 표현을 shard 반영 표현(ko: `correctness shard N ∥ simplicity`, en: 대응 번역)으로 바꾸고, 그 줄의 나머지 서술(게이트 위치·경량 반환)은 보존한다.

**Acceptance Criteria**:
- [ ] AC1: 두 파일에서 `2-reviewer` 리터럴이 0건이고, 대체 서술에 shard 앵커(ko `shard`, en `shard`)와 `correctness`·`simplicity`가 모두 있다.
- [ ] AC2: 두 파일의 diff가 각 1줄 수정(-1/+1)뿐이다.

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md` -- 82행 reviewer 구성 서술 갱신
- [M] `docs/en/AUTOPILOT_GUIDE.md` -- 82행 동일 갱신 (en)

### Task 4: 변경 격리·잔존 census (read-only 검증)

이번 변경이 계획된 파일 밖으로 새지 않았고, 고정 표기가 변형형으로도 **repo-wide** 잔존하지 않음을 전수 확인한다. 범위를 변경 파일로 좁히면 이번 plan-review가 잡은 docs 누락 부류를 검증 task가 놓친다.

**Acceptance Criteria**:
- [ ] AC1: `git diff --name-only`가 정확히 계획된 4파일(SKILL 미러 2 + docs 2)과 프로세스 산출물(draft·work_log)만 보인다 — agent 10파일·pr-review 2벌·implementation SKILL 2벌은 diff 0.
- [ ] AC2: **repo-wide** 고정 표기 census — **git 추적 파일 대상**(gitignore된 로컬 전용 산출물은 커밋 표면이 아니므로 제외), `두 reviewer`·`두 개의 형제`·`2-Reviewer`·`two reviewer`(대소문자 무시)의 잔존이 정당 잔존 목록에만 있다: `pr-review` SKILL 2벌(별도 스킬)·`_sdd/spec/`(spec-sync 인계)·append-only 로그·`_sdd/drafts/`·`_sdd/work_log/`. 목록 밖 잔존 0건.
- [ ] AC3: spec 인계 표면이 라인 번호로 열거된다 — `_sdd/spec/` live 파일에서 implementation-review의 reviewer 구성 서술이 있는 위치(grep 출력)를 spec-sync 인계 목록으로 채팅에 노출.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **게이트 = 파일럿 (사용자 합의됨)**: 이 feature의 구현 게이트에서, 스킬 발효 전(plugin cache lag)이지만 메인 루프가 수동으로 correctness×2(task별 digest — Task 1+3/Task 2가 shard) + simplicity×1을 한 메시지 dispatch해 실측한다. 판정: shard 벽시계 ~220s대면 비례 분배 지지, ~350s+면 고정비 지배이므로 **머지 전 재고**. 중간 밴드(대략 250~350s)를 포함해 지지 밴드 밖이면 모두 사용자 보고 후 결정이다. 실측 수치를 마감 요약에 기록한다.
- **분할 상한 미도입**: simplicity(~177s)가 자연 바닥이고 draft 분할 규칙이 task 수를 소수로 유지하므로 상한 문면은 넣지 않는다(YAGNI). 사용자 확인 불요.
- **implementation SKILL 무변경**: 마감 §3 "implementation-review 스킬 1회"는 orchestrator 내부 분할과 무충돌 — 실측 확인함. 사용자 확인 불요.
