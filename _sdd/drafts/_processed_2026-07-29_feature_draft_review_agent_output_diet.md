# Feature Draft: review agent 반환 출력 다이어트 + plan-review 입력 상한

> 규모 판정: 적격 — 변경 요소 4개(Progress Overview 제거·판정행 PASS 접기 2건·입력 상한)와 task가 1:1로 대응하고, 미러 전파는 각 task의 Target Files로 눈검산된다. 변형 표기가 여러 파일에 흩어지는 census형 sweep이므로 마지막에 read-only 검증 task를 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

review agent의 체감 지연은 subagent 호출이 아니라 **리포트 작성(추론)** 이 지배한다. 계약·rubric·severity는 그대로 두고, 반환 형식에서 **정보를 더하지 않는 출력**만 걷어낸다. 별도 lite agent를 만들지 않으므로 계약은 계속 agent 하나가 단일 소스로 보유한다.

세 갈래 변경:

1. **소비자 없는 중복 섹션 제거** — `implementation-review-agent` 반환의 `Progress Overview`(task/AC 단위 상태)를 삭제한다. 같은 반환의 `Verification ledger`가 AC별 verdict+증거를 이미 보유해 task 상태는 그로부터 도출되며, `implementation-review` SKILL의 relay 목록(`AC verdict ledger, findings 요약, blocker`)도 이 섹션을 소비하지 않는다.
2. **무정보 판정행 접기** — `plan-review-agent`의 Smell 6행, `simplicity-review-agent`의 차원 5행에서 **문제가 없는 행(PASS / finding 0)은 개별 행으로 열거하지 않고 이름만 한 줄로 접는다.** 점검·스캔 수행 의무는 유지하고 출력 의무만 완화하며, 각 agent AC1을 "6개(5개) 전부가 개별 행 또는 PASS 한 줄 중 하나에 귀속된다"로 다시 써 누락 검출력을 보존한다.
3. **plan-review 입력 상한** — `plan-review-agent`의 재량 문구("필요한 범위만 읽는다")를 **도구 계단**으로 대체한다: 경로 존재는 `Glob`, AC가 지목한 content anchor는 `Grep`, `Read`는 Grep으로 판정이 닫히지 않는 파일에 한정, 그래도 부족하면 `UNKNOWN` + limitation. 규칙 소유는 Step 3 한 곳으로 모으고 Input 절·Error Handling 표는 포인터로 축약한다.

**새 contract/invariant**

- (신규 불변식) 판정 표를 가진 reviewer 반환은 **점검 대상 전량이 개별 행 또는 PASS 접기 한 줄 중 하나에 귀속**되어야 한다 — 어느 쪽에도 없는 항목은 점검 누락이다. `plan-review-agent`(6 smell)·`simplicity-review-agent`(5 차원)에 적용된다.
- (신규 불변식) `plan-review-agent`의 읽기는 `Glob` → `Grep` → `Read` → `UNKNOWN` 계단을 따른다 — 상위 단계로 판정이 닫히면 하위 단계로 내려가지 않으며, 읽기 규칙의 단일 소유자는 Step 3다.
- (기존 계약 유지 확인) `pr-review-agent` 반환의 `Correctness 신호`는 `pr-review` orchestrator가 통합 리포트 `Signals` 줄에서 소비하는 실사용 계약이므로 **제거하지 않는다**.

## Scope

- **In**: `plan-review-agent`·`implementation-review-agent`·`simplicity-review-agent`의 claude md + codex toml 반환 형식/AC 문구, `plan-review-agent`의 읽기 규칙(Step 3 + 이를 중복 서술하는 Input 절·Error Handling 행), 이 변경으로 부정확해지는 wrapper SKILL의 relay 문구(`smell 6행 판정`·`차원 5행 판정`) 4개 미러.
- **Out**:
  - Medium finding 포맷 강등 (4개 agent 모두 현행 블록 유지)
  - lite review agent 신설 — 별도 파일·계약 복제 없음
  - model/effort 티어 변경 — 사용자가 이미 시도했고 효과 없음이 확인됨
  - `implementation-review`·`pr-review`에 입력 상한 규칙 추가
  - `pr-review-agent` 본문 변경 — `Correctness 신호`는 소비자가 있어 유지되고, 이 agent에는 판정행 표가 없다
  - rubric·severity 기준·6 smell/5 차원 정의 자체의 변경
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: implementation-review-agent 반환에서 Progress Overview 제거

`Verification ledger`가 AC별 verdict+증거를 보유하므로 task/AC 상태 요약은 도출 가능한 중복이고, relay 소비자도 없다. 반환 항목 하나를 통째로 없애 생성량을 줄인다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/agents/implementation-review-agent.md`의 Step 6 Return 목록에서 `Progress Overview` 불릿이 삭제됐다 — 파일 전체에 `Progress Overview` 문자열이 0회 등장한다.
- [ ] AC2: 같은 삭제가 `.codex/agents/implementation-review-agent.toml`에도 반영됐고, 해당 파일에 `Progress Overview` 문자열이 0회 등장한다.
- [ ] AC3: Step 6의 나머지 반환 항목(`Status`·`Findings`·`Verification ledger`·`Recommendations`·`Assumptions`)이 두 파일 모두에 그대로 남아 있다 — 항목 수가 5개다.

**Target Files**:
- [M] `.claude/agents/implementation-review-agent.md` -- Step 6 Return의 Progress Overview 불릿 삭제
- [M] `.codex/agents/implementation-review-agent.toml` -- codex 미러에 동일 삭제 (3-way merge: codex 적응 delta 보존)

---

### Task 2: plan-review-agent Smell 판정행 PASS 접기 + AC1 재작성

6개 smell 전부를 한 행씩 출력하는 대신 문제 있는 것만 행으로 내고 PASS는 이름만 한 줄로 접는다. 누락 검출력을 잃지 않도록 AC1을 "전량 귀속" 기준으로 다시 쓴다.

**Contracts**: 반환의 smell 판정은 (a) `WARN`/`FAIL`/`UNKNOWN` smell의 개별 행과 (b) `PASS: <이름 나열>` 한 줄로 구성되고, **6개 smell 전부가 둘 중 정확히 하나에 귀속**된다. 어느 쪽에도 없는 smell은 점검 누락으로 판정된다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/agents/plan-review-agent.md` Step 6 Return의 smell 판정 항목이 위 Contracts대로 재작성됐다 — WARN/FAIL/UNKNOWN만 개별 행으로 내고 `나머지는 PASS: <이름 나열> 한 줄로 접는다`는 지시가 문면에 있다. **완전성 불변식(6개 전량 귀속)은 여기 재서술하지 않는다** — 소유자는 AC1 절 한 곳이고, `나머지는`이 분할을 이미 완결한다.
- [ ] AC2: 같은 파일 AC1 문구가 "6개 smell 각각 점검" 의무는 유지한 채, 출력 요구를 "개별 행 또는 PASS 한 줄 중 정확히 하나에 6개 전부가 귀속"으로 바뀌었다 — `Smell 6행`이라는 표현이 파일에 남아 있지 않다. 같은 명제의 부정형 대우("어느 쪽에도 없는 smell은 점검 누락이다")는 positive와 중복이므로 두지 않는다.
- [ ] AC3: finding으로 기록된 항목의 재진술 금지 규칙이 재작성 후에도 보존됐다.
- [ ] AC4: AC1~AC3의 변경이 `.codex/agents/plan-review-agent.toml`에 동일 의미로 반영됐고, 그 파일에도 `Smell 6행` 표현이 남아 있지 않다.
- [ ] AC5: 6개 smell 정의(Review Rubric 표)와 Severity 표는 변경되지 않았다 — 두 파일에서 해당 표의 행 수가 각각 6, 4로 유지된다.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- AC1 문구 + Step 6 Return의 smell 판정 항목
- [M] `.codex/agents/plan-review-agent.toml` -- codex 미러에 동일 변경 (3-way merge)

---

### Task 3: plan-review-agent 읽기 규칙을 도구 계단으로 대체하고 소유를 Step 3으로 일원화

"필요한 범위만 읽는다"는 상한이 아니라 재량이라 read 비용이 무제한으로 열린다. 다만 Target File 본문 Read를 전면 금지하면 `Verification Weakness` smell(AC가 falsifiable한가·기존 구조와 충돌하는가)의 판정 근거가 사라지므로, 금지가 아니라 **더 싼 수단을 먼저 쓰게 하는 계단**으로 규칙을 세운다. 같은 규칙이 Input 절과 Error Handling 표에도 흩어져 있어 소유를 Step 3 한 곳으로 모은다.

**Contracts**: `plan-review-agent`의 supporting context 읽기는 다음 계단을 따르며, 상위 단계에서 판정이 닫히면 하위 단계로 내려가지 않는다 — (1) 경로 존재는 `Glob`, (2) AC가 지목한 content anchor(함수·심볼·문자열)는 `Grep`, (3) `Read`는 Grep으로 판정이 닫히지 않는 파일에 한정, (4) 그래도 근거가 부족하면 해당 smell을 `UNKNOWN`으로 두고 limitation 1줄을 기록하며 읽기를 확장하지 않는다. 이 규칙의 단일 소유자는 Step 3이고, 다른 절은 Step 3을 가리키는 포인터만 갖는다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/agents/plan-review-agent.md` Step 3이 위 계단 4단계를 순서대로 명시하고, 각 단계에 어떤 도구를 쓰는지가 문면에 있다 — `Glob`·`Grep`·`Read`·`UNKNOWN` 네 토큰이 모두 등장한다.
- [ ] AC2: 같은 Step 3에 "상위 단계로 판정이 닫히면 하위 단계로 내려가지 않는다"는 취지의 정지 규칙이 명시됐다 — Read가 무조건 수행되는 단계가 아님이 문면에서 읽힌다.
- [ ] AC3: Input 절(`:38` 부근)의 "판단에 필요한 범위만 읽는다" 문장이 Step 3 규칙을 가리키는 포인터로 축약되거나 삭제됐다 — 파일 전체에서 `필요한 범위만 읽는다` 문자열이 0회 등장한다.
- [ ] AC4: Error Handling 표의 "supporting context 부족" 행이 Step 3 계단 4단계를 가리키는 포인터 1줄로 축약됐다 — 같은 규칙의 완전 서술이 파일 내 2곳에 존재하지 않는다.
- [ ] AC5: AC1~AC4의 변경이 `.codex/agents/plan-review-agent.toml`에 동일 의미로 반영됐고, 그 파일에도 `필요한 범위만 읽는다`가 0회 등장한다.
- [ ] AC6: Step 3 외의 Process 단계(Step 1·2·4·5·6)와 tools frontmatter(`Read`,`Glob`,`Grep`)는 변경되지 않았다 — 단 Input 절과 Error Handling 표는 AC3·AC4의 변경 대상이므로 이 금지에서 제외된다.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- Step 3 재작성 + Input 절·Error Handling 행 포인터 축약
- [M] `.codex/agents/plan-review-agent.toml` -- codex 미러에 동일 변경 (3-way merge)

---

### Task 4: simplicity-review-agent 차원 판정행 PASS 접기 + AC1 재작성

Task 2와 같은 규칙을 5개 차원 판정에 적용한다.

**Contracts**: 반환의 차원 판정은 (a) finding이 있는 차원의 개별 행과 (b) `PASS: <차원 이름 나열>` 한 줄로 구성되고, **5개 차원 전부가 둘 중 정확히 하나에 귀속**된다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/agents/simplicity-review-agent.md` Step 4의 차원 판정 항목이 위 Contracts대로 재작성됐다 — finding 있는 차원만 행으로 내고 `나머지는 PASS: <이름 나열> 한 줄로 접는다`는 지시가 문면에 있다. **완전성 불변식(5개 전량 귀속)은 여기 재서술하지 않는다** (Task 2 AC1과 동일 규범 — 소유자는 AC1 절 한 곳).
- [ ] AC2: 같은 파일 AC1 문구가 "5개 차원 각각 능동 스캔" 의무는 유지한 채 출력 요구만 완화됐다 — `차원 5행`이라는 표현이 파일에 남아 있지 않다. 같은 명제의 부정형 대우는 두지 않는다.
- [ ] AC3: AC1~AC2의 변경이 `.codex/agents/simplicity-review-agent.toml`에 동일 의미로 반영됐고, 그 파일에도 `차원 5행` 표현이 남아 있지 않다.
- [ ] AC4: 5개 차원 정의(Review Dimensions)와 Severity Rules는 변경되지 않았다 — 두 파일에서 차원 항목이 5개로 유지된다.

**Target Files**:
- [M] `.claude/agents/simplicity-review-agent.md` -- AC1 문구 + Step 4 Classify+Return의 차원 판정 항목
- [M] `.codex/agents/simplicity-review-agent.toml` -- codex 미러에 동일 변경 (3-way merge)

---

### Task 5: wrapper SKILL의 relay 문구 동기화

wrapper가 agent 반환을 `smell 6행 판정`·`차원 5행 판정`이라는 리터럴로 지칭하고 있어, Task 2·4 이후 실제 반환 형식과 어긋난다. 지칭만 고치고 wrapper의 역할·계약은 건드리지 않는다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/plan-review/SKILL.md`의 relay 목록에서 `smell 6행 판정`이 실제 반환을 가리키는 표현(예: `smell 판정`)으로 교체됐고, 나머지 relay 항목(Blocker Status·severity별 finding·규모 판정 검사 결과)은 그대로다.
- [ ] AC2: 같은 교체가 `.codex/skills/plan-review/SKILL.md`에도 반영됐다.
- [ ] AC3: `.claude/skills/pr-review/SKILL.md`와 `.codex/skills/pr-review/SKILL.md`의 `차원 5행 판정`이 같은 방식으로 교체됐다.
- [ ] AC4: `pr-review` SKILL의 `correctness 신호(AC 충족 현황·spec 위반·test pass rate)` 기대 문구와 Output Format의 `Signals` 줄은 **변경되지 않았다** — 이 계약은 유지 대상이다.
- [ ] AC5: `.claude/skills/implementation-review/SKILL.md`·`.codex/skills/implementation-review/SKILL.md`의 relay 목록에 `Progress Overview`가 없음을 확인했다(현재 없음 — 변경 불필요, 확인만).
- [ ] AC6: 같은 두 파일의 relay 문구 `simplicity: 5개 차원 판정`을 Task 4 이후 형식과 대조해 판정했다 — 의미가 유지되면 그대로 두고, 어긋나면 교체한다. 어느 쪽이든 판정 결과가 구현 기록에 1줄로 남는다.

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` -- relay 문구 `smell 6행 판정` 교체
- [M] `.codex/skills/plan-review/SKILL.md` -- 동일 교체
- [M] `.claude/skills/pr-review/SKILL.md` -- relay 문구 `차원 5행 판정` 교체
- [M] `.codex/skills/pr-review/SKILL.md` -- 동일 교체

---

### Task 6: 변형 표기 census 검증 (read-only)

`6행`·`5행`·`Progress Overview`는 claude/codex 짝과 agent/skill 양쪽에 흩어져 있어 단일 패턴 grep으로는 잔존이 재발한다. 전수 census로 잔존 0을 증명한다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/`·`.codex/` 하위(`*.md`,`*.toml`)에서 `6행`·`5행` 변형을 전수 grep한 결과가 **0건**이다. 변경 전 기준선은 12줄이며 전부 Task 2·4·5 범위다 — `agents/plan-review-agent.{md,toml}` 각 `:16,:96`, `agents/simplicity-review-agent.{md,toml}` 각 `:16,:68`, `skills/plan-review/SKILL.md`(claude `:17`, codex `:42`), `skills/pr-review/SKILL.md`(claude `:95`, codex `:130`).
- [ ] AC2: 같은 범위에서 `Progress Overview` 전수 grep 결과가 0건이다 (변경 전 기준선 2줄: `agents/implementation-review-agent.{md,toml}` 각 `:75`). `_sdd/implementation/`·`_sdd/spec/logs/`의 과거 리포트·이력 문서는 append-only 기록물이므로 census 대상에서 제외하고, 제외 사실을 결과에 명시한다.
- [ ] AC3: 같은 범위에서 `필요한 범위만 읽는다` 전수 grep 결과가 0건이다 (변경 전 기준선 2줄: `agents/plan-review-agent.{md,toml}` 각 `:38`).
- [ ] AC4: `git diff --check` 통과 및 변경 파일 목록이 Task 1~5의 Target Files 합집합과 정확히 일치한다 — 계획 밖 파일 변경이 0건이다.
- [ ] AC5: 변경된 3개 agent(claude md ↔ codex toml)의 짝 diff를 확인해, 이번 변경분이 양쪽에 동일 의미로 들어갔고 codex 적응 delta(runtime adapter·model 허용값 등)가 훼손되지 않았다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

없음 — 범위 결정(Medium 포맷 유지, 입력 상한은 plan-review 한정)은 사용자가 확정했고, `pr-review` Correctness 신호의 소비 여부는 `pr-review/SKILL.md:94,140` 실측으로 유지 확정됐다.
