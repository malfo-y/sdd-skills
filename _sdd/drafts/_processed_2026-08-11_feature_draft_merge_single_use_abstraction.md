# Feature Draft: Single-use Abstraction smell/차원 통합

> 규모 판정: 적격 (변경 요소 4개 — smell 통합·차원 통합·개수 리터럴 전파·차원명 열거 전파 — 가 task에 대응, 파일 12개 전수 열거로 눈검산 가능. census형 신호 있음 → Part 2 마지막 read-only 검증 task 포함)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

사용자 코멘트 반영: plan-review의 `Single-use Abstraction` smell은 `DRY Risk`의 "작은 중복에 과한 추상화" 절과 조기 추상화 영역을 나눠 갖는 부분 중복이라 통합한다. reviewer 짝 대칭 유지를 위해 simplicity-review의 `단일 사용처 추상화` 차원도 `중복 코드` 차원과 통합한다(사용자 결정 — 짝으로 묶어 진행).

**바뀌는 contract** (기존 계약 개정, 신규 없음):
- plan-review rubric: 6 smell → **5 smell** — `DRY Risk`가 단일 사용처 추상화 검사를 흡수(Check 문면 확장, Principle Link에 YAGNI 추가). 판단 렌즈 소유 = 나머지 4 smell.
- simplicity-review 차원: 5개 → **4개** — 1번 차원이 `중복 코드·단일 사용처 추상화 (Duplication & Single-use Abstraction)`로 통합. 참조 묶음 = 통합 차원 + 죽은 코드(2개), 국소 묶음 불변(2개), 합집합 = 정확히 4개.
- 차원 한정 없는 호출(pr-review 경로)은 전체 4차원 1회로 후방 호환 유지.

## Scope
- **In**: `.claude`/`.codex`의 agent 3종 짝(plan-review·simplicity·pr-review — pr-review는 경계 절 열거만) + 개수 리터럴·차원명 열거를 가진 wrapper/orchestrator/example 6파일, 변형형 전수 census 검증.
- **Out**: spec surface(main.md·components.md — spec-sync 소관), decision_log 과거 기록(append-only), 렌즈/묶음 dispatch 구조(분할 축 불변), severity 체계, Feature "리뷰 읽기 다이어트" 계열(별건).
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | smell 6→5 개수 리터럴 (claude 측 wrapper) | `.claude/skills/plan-review/SKILL.md` | `grep -rn "6-smell\|6 smell\|6개 전부\|6 Plan Smells" .claude/` → Task 1·3 완료 후 0건 | Task 3 |
| P2 | 차원 5→4 개수 리터럴 (claude 측 orchestrator·example) | `.claude/skills/implementation-review/SKILL.md`, `.claude/skills/pr-review/SKILL.md`, `.claude/skills/pr-review/examples/sample-review.md` | `grep -rn "5개 차원\|5차원\|5 차원" .claude/` → Task 2·3 완료 후 0건 | Task 3 |
| P3 | 위 전부의 codex 미러 반영 | `.codex/agents/plan-review-agent.toml`, `.codex/agents/simplicity-review-agent.toml`, `.codex/skills/plan-review/SKILL.md`, `.codex/skills/implementation-review/SKILL.md`, `.codex/skills/pr-review/SKILL.md`, `.codex/skills/pr-review/examples/sample-review.md` | 같은 두 grep을 `.codex/`에 실행 → Task 4 완료 후 0건 | Task 4 |
| P4 | 차원명 명시 열거 문면 (5차원 나열 → 통합 4차원 나열) — 개수 리터럴 grep에 안 걸리는 표면 | `.claude/agents/pr-review-agent.md`(:36 경계 절), `.claude/skills/pr-review/SKILL.md`(:12), `.claude/skills/implementation-review/SKILL.md`(:12) — claude 측은 Task 3, codex 짝 3파일은 Task 4 | `grep -rn "죽은 코드·단일 사용처" .claude .codex` → 현재 6건(위 3파일 + codex 짝), 완료 후 0건 | Task 3 |

# Part 2: Tasks

### Task 1: plan-review-agent 6→5 smell 통합 (claude)

`Single-use Abstraction` 행을 삭제하고 `DRY Risk`가 그 검사를 흡수한다 — 두 smell이 조기 추상화 영역을 나눠 갖던 부분 중복 해소.

**Contracts**: 통합 후 `DRY Risk` Check = 기존 문면 + "한 곳에서만 쓰이는 helper, layer, config, interface를 만들도록 계획했는가?", Principle Link = `DRY, KISS, YAGNI`. smell 총수 리터럴은 **census 금지 패턴(`5개 전부`)과 충돌하지 않는 문면으로 고정한다**: heading `Review Rubric: 5 Plan Smells`, AC1 `한정이 없으면 5 smell 전부`, `전체(5 smell)`, 판단 렌즈 소유 `나머지 4 smell`. Severity Medium 행의 "단일 사용처 추상화" 예시 문구는 smell 이름이 아니므로 유지.

**Acceptance Criteria**:
- [ ] AC1: rubric 표에서 `Single-use Abstraction` 행이 사라지고 잔여 5개 smell 명이 각 1행씩 있다. 평가(1등급): `grep -n "| Single-use Abstraction |" .claude/agents/plan-review-agent.md` 0건 + `Scope Creep`·`New File Justification`·`Task Boundary Drift`·`DRY Risk`·`Verification Weakness` 행 grep 각 1건.
- [ ] AC2: `DRY Risk` Check에 단일 사용처 검사 문구가 있고 Principle Link에 YAGNI가 포함됐다. 평가(1등급): `grep -n "한 곳에서만 쓰이는" .claude/agents/plan-review-agent.md`가 DRY Risk 행에서 1건.
- [ ] AC3: 개수 리터럴이 갱신됐다 — `6 Plan Smells`·`6개 전부`·`전체(6 smell)` 0건, `5 Plan Smells`·`5 smell 전부`·`전체(5 smell)`·`나머지 4 smell` 각 1건. 평가(1등급): grep 출력.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- rubric 행 삭제·DRY Risk 확장·개수 리터럴 갱신

### Task 2: simplicity-review-agent 5→4 차원 통합 (claude)

`단일 사용처 추상화` 차원을 `중복 코드` 차원과 통합해 reviewer 짝 대칭을 유지한다.

**Contracts**: 통합 차원 1 = `중복 코드·단일 사용처 추상화 (Duplication & Single-use Abstraction)` — "같은 로직이 둘 이상 지점에 복제됨(한 곳으로 합쳐도 동작이 같다), 또는 한 곳에서만 쓰이는 wrapper·helper·indirection 레이어(호출처에 인라인해도 동작이 같다)". 차원 번호 재부여(1 통합, 2 죽은 코드, 3 도달 불가 에러 처리, 4 과잉압축). 참조 묶음 = 통합 차원 + 죽은 코드, 국소 묶음 불변, "합집합 = 정확히 4개". 개수 리터럴(AC1 `5개 전부`, `전체 5개 차원`, Severity `5개 차원의`, Integration `전체 5차원`) 전부 4로.

**Acceptance Criteria**:
- [ ] AC1: Review Dimensions가 4개 항목이고 1번이 통합 차원(Duplication & Single-use Abstraction)이다. 평가(1등급): 해당 절 grep — 번호 행 4개, 통합 차원명 1건.
- [ ] AC2: 참조 묶음 정의가 통합 차원 + 죽은 코드이고 국소 묶음이 불변이다. 평가(1등급): `호출자 차원 한정` 절 grep.
- [ ] AC3: 개수 리터럴 `5개 전부`·`전체 5개 차원`·`5개 차원의`·`전체 5차원` 0건. 평가(1등급): grep 출력 0건.

**Target Files**:
- [M] `.claude/agents/simplicity-review-agent.md` -- 차원 통합·묶음 재정의·개수 리터럴 갱신

### Task 3: claude 측 wrapper/orchestrator/example 개수 리터럴·차원명 열거 갱신

agent 밖에 남은 개수 리터럴과 **차원명 명시 열거 문면**(개수 grep에 안 걸리는 표면 — P4)을 새 계약(5 smell·4차원)에 맞춘다.

**Contracts**: 차원명 열거 갱신 문면 — 통합 4차원 나열은 구분자를 쉼표로 바꿔 통합 차원명 내부 `·`과 구별한다: `중복 코드·단일 사용처 추상화, 죽은 코드, 도달 불가 에러 처리, 과잉압축`. 그 외는 기존 포인터 서술의 수치만 갱신(묶음·렌즈 정의의 단일 소스는 agent 유지).

**Acceptance Criteria**:
- [ ] AC1: P1·P2 Discovery evidence의 두 grep이 `.claude/`에서 0건이다. 평가(1등급): grep 출력 0건.
- [ ] AC2: 갱신된 문면이 새 수치를 담는다 — `5-smell` 및 `4개 차원`(또는 `전체 4차원`)이 개수 리터럴 대상 4파일에 실재. 평가(1등급): 파일별 grep ≥ 1건.
- [ ] AC3: P4 claude 측 열거 3곳이 통합 4차원 나열로 갱신됐다 — `grep -rn "죽은 코드·단일 사용처" .claude/` 0건 + 쉼표 구분 나열 문면 3건. 평가(1등급): grep 출력.

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` -- 6-smell → 5-smell
- [M] `.claude/skills/implementation-review/SKILL.md` -- 5개 차원 → 4개 차원 + :12 열거 갱신
- [M] `.claude/skills/pr-review/SKILL.md` -- 5개 차원 → 4개 차원 + :12 열거 갱신
- [M] `.claude/skills/pr-review/examples/sample-review.md` -- 5개 차원 스캔 → 4개 차원 스캔
- [M] `.claude/agents/pr-review-agent.md` -- :36 경계 절의 5차원 열거 → 통합 4차원 나열

### Task 4: codex 미러 전파 (3-way merge)

Task 1~3 변경을 codex 적응 delta(Codex Agent Boundary·spawn_agent·Runtime Adapter 어휘)를 보존하며 미러 7파일에 재적용한다 — 단순 복사 금지.

**Acceptance Criteria**:
- [ ] AC1: P3 Discovery evidence의 두 grep과 P4 grep(`죽은 코드·단일 사용처`)이 `.codex/`에서 0건이다. 평가(1등급): grep 출력 0건.
- [ ] AC2: codex 고유 적응 보존 — `Codex Agent Boundary`가 세 agent toml에, `spawn_agent`가 orchestrator SKILL에 잔존. 평가(1등급): grep ≥ 각 1건.
- [ ] AC3: 통합 문면 동등성 — 통합 차원명·`나머지 4 smell`·`한 곳에서만 쓰이는`(DRY Risk 내)·쉼표 구분 4차원 나열이 codex 짝 파일에 실재. 평가(2등급): reviewer가 anchor 인용으로 판정.

**Target Files**:
- [M] `.codex/agents/plan-review-agent.toml` -- Task 1 미러
- [M] `.codex/agents/simplicity-review-agent.toml` -- Task 2 미러
- [M] `.codex/agents/pr-review-agent.toml` -- :36 경계 절 열거 갱신 (Task 3 미러)
- [M] `.codex/skills/plan-review/SKILL.md` -- Task 3 미러
- [M] `.codex/skills/implementation-review/SKILL.md` -- Task 3 미러 (:12 열거 포함)
- [M] `.codex/skills/pr-review/SKILL.md` -- Task 3 미러 (:12 열거 포함)
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- Task 3 미러

### Task 5: 변형형 전수 census 검증 (read-only)

rename census 함정 방지 — 개수·명칭 변형형을 전수 grep으로 확인한다.

**Acceptance Criteria**:
- [ ] AC1: 구 개수 변형형 전수 0건 — `.claude`·`.codex` 전체에서 `6-smell`·`6 smell`·`6개 전부`·`6 Plan Smells`·`5개 차원`·`5차원`·`5 차원`·`전체 5차원`·`5개 전부` 잔존 0 (glob·공백·하이픈 변형 포함 패턴으로). 평가(1등급): 통합 grep 출력 0건.
- [ ] AC2: `Single-use Abstraction`·`단일 사용처` 잔존이 전부 의도된 문맥(통합 차원명·DRY Risk Check·Severity Medium 예시·통합 차원 본문·P4 표면의 쉼표 구분 통합 나열 — pr-review-agent 짝 경계 절과 orchestrator 렌즈 설명 포함)에만 있다. 평가(2등급): reviewer가 전수 hit 목록을 문맥 분류해 판정.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- 통합 smell 이름: `DRY Risk` 유지로 결정(개명 시 census 표면이 커짐 — 흡수가 최소 변경). 확인 불필요.
- simplicity 통합 차원 이름: `중복 코드·단일 사용처 추상화 (Duplication & Single-use Abstraction)`로 결정 — 두 검사 모두 문면에 살아있어 검출 손실 없음. 확인 불필요.
- spec surface(main.md §81·82·86·150, components.md 27·29)의 구 수치는 이 feature에서 안 만진다 — 구현 후 spec-sync가 current truth 갱신 + decision entry로 처리. 확인 불필요.
