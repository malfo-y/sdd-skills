---
name: goal-init
description: This skill should be used when the user asks to set up a "/goal", "goal 조건", "goal init", "goal-init", "set up goal", "goal helper", "goal 설정", "goal 목표", wants to craft a good `/goal` completion condition, or to scaffold the 4-file goal harness for a native `/goal` loop. Conversational helper that crafts the condition string and harness; it does not invoke `/goal` itself.
version: 1.0.0
---

# goal-init - `/goal` 조건 + 실행 하네스 셋업

| Workflow | Position | When |
|----------|----------|------|
| Any | Standalone | `/goal`에 걸 좋은 완료조건 문자열과 4파일 실행 하네스를 한 번의 대화로 셋업 |

네이티브 `/goal`(조건 충족까지 매 턴 자동 반복하는 평가자 기반 루프)에 걸 **자족적 완료조건 문자열**과 그 조건이 참조할 **4파일 실행 하네스**(`_sdd/goal/<YYYY-MM-DD>_<slug>/`)를 대화형으로 함께 만든다. discussion식 대화형 단일 스킬이다 — 신규 agent를 위임하지 않고, `AskUserQuestion` 기반 단일 대화 루프로 진행하며, 파일 생성은 Harness Setup 단계에서만 한다. **스킬은 `/goal`을 직접 발동하지 않는다** — 사용자가 조건을 검토한 뒤 직접 발동한다.

## Goal

사용자의 멀티턴 목표를, (1) 평가자가 도구 없이 transcript만으로 판정 가능한 자족적 완료조건 문자열과 (2) 그 조건이 참조하는 4파일 실행 하네스로 전환해, 사용자가 검토 후 직접 `/goal`에 걸 수 있는 상태로 핸드오프한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 목표가 `/goal` 적합성 gate(verifiable end state가 있는 멀티턴 작업)를 통과했다.
- [ ] AC2: 목표 달성 접근/가설 2개 이상이 발산되어 `experiments.md` 백로그에 수집되었다.
- [ ] AC3: 완료조건 문자열이 평가자 적합성 self-check(도구 없이 판정·evidence 매 턴 surface·4,000자 이하)를 통과했다.
- [ ] AC4: `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 4파일(`goal.md`/`experiments.md`/`journal.md`/`report.md`)이 생성되었다.
- [ ] AC5: 조건 문자열 + Claude `/goal` 실행법을 핸드오프로 제시했고, 스킬이 `/goal`을 직접 발동하지 않았다.

## Hard Rules

1. **비발동 (I2)**: 스킬은 `/goal`을 직접 발동하지 않는다. Handoff는 조건 문자열 + 실행법 제시까지이며, 발동은 사용자가 검토 후 직접 한다.
2. **평가자 자족성 / 4,000자 (I1)**: 완료조건(`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 도구 없이 transcript만으로 판정 가능해야 하고 4,000자 이하여야 한다. 이 두 조건을 통과하지 못하면 Handoff하지 않는다.
3. **적합성 gate (I3)**: Goal Intake의 적합성 gate를 통과하지 못한 목표로는 Divergence를 진행하지 않는다.
4. **ralph 불간섭**: `ralph-loop-init` 스킬/agent를 건드리지 않는다. bash `while-true` 루프·`run.sh`·컨테이너 격리를 차용하지 않는다.
5. **산출 경로**: 4파일은 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에만 생성한다. 그 외 경로에 산출물을 만들지 않는다.

## Key Principles

Process의 모든 단계에 횡단 적용되는 판단 지침. Hard Rules가 강제 금지라면, Key Principles는 판단 지침이다.

- **Evaluator-first**: 완료조건은 항상 "도구 없이 transcript만 보는 평가자가 판정할 수 있는가"를 기준으로 작성한다. 판정 불가능한 표현은 측정 가능한 형태로 바꾼다.
- **Condition vs HOW 분리**: 완료조건(WHAT/`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 조건 문자열에 자족 인라인하고, 루프 행동(HOW)은 `goal.md`의 `Loop Protocol`에 둔다 (조건 비대화·평가자 노이즈 방지).
- **AI-initiated divergence**: 가설은 사용자가 먼저 꺼낼 때까지 기다리지 않는다. AI가 권장안을 먼저 제시하고 2-3개 접근과 트레이드오프를 능동 발산한다 (discussion alternatives-initiation 패턴).
- **파일 생성은 Harness Setup에서만**: Goal Intake/Divergence/Condition Crafting 단계에서는 파일을 만들지 않는다. 4파일 생성은 Harness Setup에서만 수행한다.
- **YAGNI**: 5단계·4파일·분업형 조건 외의 옵션·설정·추상화를 추가하지 않는다.

## Process

> 5단계를 순서대로 진행하며, 각 단계 끝의 Decision Gate를 통과해야 다음 단계로 넘어간다. 단계 순서와 Gate 전이는 고정이다.

### Step 1: Goal Intake

사용자의 목표를 수집한 뒤, `/goal` 적합성 hard gate를 적용한다.

- **적합성 gate 기준**: "**verifiable end state가 있는 멀티턴 작업인가**" — (1) 달성 여부를 transcript에서 판정할 수 있는 종료 상태가 있고, (2) 한 번의 답변으로 끝나지 않는 반복 작업이어야 한다.
- **실패 분기**: "한 줄 수정"·"오타 고치기" 같은 단발성 작업이거나 종료 상태가 모호하면, 측정 가능한 종료 상태를 갖도록 **재정의를 안내**한다. 재정의가 불가능하면 `/goal` 대신 단발 작업임을 알리고 **중단한다 (I3)**.

**Decision Gate 1→2**: 적합성 gate를 통과한 목표가 확정되면 Step 2로 진행한다. ELSE 재정의 안내; 재정의 불가 시 중단한다.

### Step 2: Divergence

목표 달성 접근/가설을 **AI가 능동적으로 발산한다** (사용자가 먼저 꺼낼 때까지 기다리지 않는다 — discussion alternatives-initiation 패턴).

- **권장안 먼저**: 2-3개의 구별되는 접근/가설을 제시하되, 중립 나열만 하지 않고 **권장안을 먼저 말하고 이유와 트레이드오프를 붙인다**.
- **백로그 수집**: 발산한 가설들을 `experiments.md`의 초기 **pending 백로그**로 수집한다 (각 항목 = 가설 한 줄 + 검증 명령·판정조건). 단, 이 단계에서 파일을 만들지는 않는다 — 수집은 Harness Setup에서 기록한다.
- 가설이 안 나오면 사용자에게 접근 후보를 직접 요청해 백로그를 구성한다.

**Decision Gate 2→3**: pending 가설을 2개 이상 확보하면 Step 3으로 진행한다.

### Step 3: Condition Crafting

5요소(목표 / 측정 가능 AC / 증명 방법 / 제약 / 종료 경계)를 **분업형 조건 문자열**로 응축한다.

- **분업형 (C3, 템플릿 슬롯)**: 완료조건은 `DONE WHEN`(측정 가능 AC + 증명: 명령·기대 출력 인라인) / `CONSTRAINTS`(제약) / `STOP`(종료 경계 — N턴 무진척)로 작성하고, 루프 행동(HOW)은 조건 문자열에 넣지 않고 별도 `Loop Protocol`로 분리한다 (`references/harness-templates.md`의 `goal.md` 슬롯에 1:1 대응).
- **평가자 적합성 self-check (hard gate — I1)**: 응축한 조건 문자열에 대해 3항목을 확인한다.
  - (a) 도구 없이 대화(transcript)만으로 판정 가능한가
  - (b) evidence(검증 명령·기대 출력)가 매 턴 surface되는가
  - (c) 4,000자 이하인가
  - 하나라도 실패하면 **응축을 재시도한다** (3항목을 모두 통과할 때까지 통과시키지 않는다).

**Decision Gate 3→4**: self-check 3항목(도구 없이 판정 · evidence 매 턴 surface · 4,000자 이하)을 모두 통과하면 Step 4로 진행한다. ELSE 응축 재시도 (hard gate).

### Step 4: Harness Setup

`_sdd/goal/<YYYY-MM-DD>_<slug>/`에 `references/harness-templates.md` 템플릿으로 **4파일을 생성한다**: `goal.md` / `experiments.md` / `journal.md` / `report.md`.

- **`goal.md`**: 확정한 조건 문자열(`DONE WHEN`/`CONSTRAINTS`/`STOP`)을 `/goal` 조건 문자열 슬롯에 기입하고, `Loop Protocol`에 매 턴 행동 규칙(① `experiments.md` pending 큐 소비 · ② 큐가 비고 미완이면 새 가설 자동 발산해 pending에 append · ③ 검증 명령 출력을 대화에 surface · ④ 시도·결과를 `journal.md`에 append)을 기입한다.
- **`experiments.md`**: Step 2에서 발산한 가설들을 pending 백로그로 기입한다.
- **실행법 슬롯**: Claude Code 슬롯만 채운다 (Codex 슬롯은 Codex 스킬이 자기 슬롯을 채우므로 placeholder로 둔다).

**Decision Gate 4→5**: 4파일 생성이 완료되면 Step 5로 진행한다.

### Step 5: Handoff

확정한 **조건 문자열**과 **Claude `/goal` 실행법**을 사용자에게 제시한다.

- **Claude 실행법**: (a) workspace trust + hooks가 활성화되어 있어야 `/goal` 루프가 동작한다. (b) 라이프사이클은 `/goal set`(목표 설정)·`/goal status`(진행 확인)·`/goal clear`(종료)이며, `clear`는 별칭(`stop`·`off`·`reset` 등)으로도 호출할 수 있다. (c) 세션을 멈췄다 `--resume`/`--continue`로 이어가면 active goal이 복원되며 턴·타이머·토큰 카운터가 리셋된다. (d) 평가자는 조건 문자열을 4,000자 상한으로 읽으므로, 그 안에서 도구 없이 판정 가능한 evidence가 매 턴 surface되어야 한다.
- **스킬은 `/goal`을 직접 발동하지 않는다 (I2)**. 핸드오프는 조건 문자열 + 실행법 제시까지이며, 사용자가 조건을 검토한 뒤 **직접 발동한다**.

**Decision Gate (종료)**: 조건 문자열 + Claude 실행법 제시가 완료되면 종료한다.

## Error Handling

| 상황 | 대응 |
|------|------|
| 목표가 단발성/모호 (적합성 gate 실패) | 재정의 안내. 재정의 불가 시 중단하고 `/goal` 대신 단발 작업임을 알린다. |
| 검증 명령이 명령+판정조건으로 확정되지 않음 | 진행을 차단한다 (hard gate). 명령과 판정조건이 둘 다 확정될 때까지 Condition Crafting을 통과시키지 않는다. |
| 조건 문자열이 4,000자를 초과 | 응축 재시도. 4,000자 이하로 줄일 때까지 Handoff하지 않는다. |
| Divergence에서 가설이 안 나옴 | 사용자에게 접근 후보를 직접 요청하고, 받은 후보로 백로그를 구성한다. |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
