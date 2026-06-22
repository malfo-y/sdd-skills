# Feature Draft: goal-init 스킬 (`/goal` 조건 + 실행 하네스 생성기)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

신규 대화형 단일 스킬 `goal-init`을 추가한다. Claude Code / Codex의 네이티브 `/goal` 기능(조건 충족까지 매 턴 자동 반복하는 평가자 기반 루프)에 걸 **좋은 goal 조건 문자열**과 그 조건이 참조할 **4파일 실행 하네스**(`_sdd/goal/<YYYY-MM-DD>_<slug>/`)를 한 번의 대화로 셋업한다.

문제: `/goal`을 잘 쓰려면 (1) 평가자가 도구 없이 transcript만으로 판정할 수 있는 자족적 완료조건, (2) 목표를 향한 다양한 가설을 발산·실험·검증하는 메커니즘, (3) 검증 흔적을 대화에 surface, (4) 종료 후 회고 — 네 가지가 모두 필요한데 사용자가 수동으로 갖추기 어렵다. `goal-init`은 이 네 페인을 셋업 시점(사용자와 1차 발산)과 루프 진행 시점(조건 내장 자동 발산 규칙)에 나눠 해소한다.

기존 가장 가까운 선례 `ralph-loop-init`은 외부 bash `while-true` 루프 + 컨테이너 격리 + exit-code 머신 판정 모델이라 `/goal`의 네이티브 턴 루프와 실행 모델이 근본적으로 다르다. `goal-init`은 ralph에서 append-only journal·conclusion-first report·적합성 hard gate 정신만 차용하고, bash 루프·`run.sh`·컨테이너 격리는 차용하지 않는다.

v1 스코프는 대화형 goal-helper 한정이다. ralph-loop 대체는 의도적으로 deferred한다 (Q1 참조).

## Scope Delta

**In-scope (v1)**
- 신규 스킬 `goal-init` (Claude용 `.claude/skills/goal-init/`, Codex용 `.codex/skills/goal-init/` 각각 작성).
- discussion식 대화형 단일 스킬: 신규 agent 없음, 단일 대화 루프 + `AskUserQuestion`.
- Process 5단계: Goal Intake → Divergence → Condition Crafting → Harness Setup → Handoff.
- 4파일 하네스 생성: `goal.md` / `experiments.md` / `journal.md` / `report.md` (경로 `_sdd/goal/<YYYY-MM-DD>_<slug>/`).
- `/goal` 조건 문자열 = 분업형: 완료조건(`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 조건에 자족 인라인, 루프 행동(HOW)은 `goal.md`의 `Loop Protocol` 참조.
- 조건 본문은 런타임 독립, 실행법(활성화·라이프사이클 명령)만 각 스킬에 자기 런타임 것 기재.
- `marketplace.json` `plugins[0].skills` 배열에 두 경로 등록.

**Out-of-scope / deferred**
- ralph-loop 대체 (Q1, deferred-deliberately): `/goal` 턴 기반 한계 vs ralph bash 무한루프 격차 검토는 별도 장기 과제.
- 신규 agent 추가: `goal-init`은 대화형 단일 스킬이므로 `marketplace.json` `agents` 배열은 불변.
- 스킬이 `/goal`을 직접 발동하는 것: 사용자가 조건 검토 후 직접 발동 (잘못된 무인 루프 토큰 낭비 방지).
- bash `while-true` 루프 / `run.sh` / 컨테이너 격리: `/goal`은 네이티브 턴 루프라 불필요.
- README/docs 워크플로우 통합: v1에서 권고만 하고 본 delta 범위 밖 (Action Item Low, R-DOC 참조).

**Guardrail delta**
- 조건 문자열은 항상 4,000자 이하여야 한다 (Claude `/goal` 평가자 상한 — 런타임 독립 본문이 양쪽 모두 만족하도록 Claude 상한을 공통 기준으로 삼는다).
- 완료조건은 도구 없이 transcript만으로 판정 가능해야 한다 (평가자 적합성 self-check 통과 없이는 Handoff 불가).
- `ralph-loop-init` 스킬/agent는 건드리지 않는다 (v1 독립).

## Persistent Spec Implications

persistent spec(스킬 카탈로그/워크플로우 surface)에 남아야 하는 계약·불변식·검증 의도:

- **계약 — 스킬 존재·형태**: `goal-init`은 discussion식 대화형 단일 스킬(신규 agent 없음)로 카탈로그에 등재된다. Claude/Codex 두 디렉토리에 각각 존재하고 `marketplace.json` skills 배열에 등록된다.
- **계약 — 산출물 경로**: `goal-init` 실행 시 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 4파일(`goal.md`/`experiments.md`/`journal.md`/`report.md`)이 생성되고, 사용자가 검토 후 직접 `/goal`에 걸 조건 문자열이 제시된다.
- **불변식 — 평가자 자족성**: 생성되는 `/goal` 조건의 완료조건(`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 도구 없이 transcript만으로 판정 가능하고 4,000자 이하여야 한다. 루프 행동(HOW)은 조건이 아니라 `goal.md`의 `Loop Protocol`에 둔다 (조건 비대화·평가자 노이즈 방지).
- **불변식 — 비발동**: `goal-init`은 `/goal`을 직접 발동하지 않는다 (Handoff는 조건 + 실행법 제시까지).
- **불변식 — 런타임 분리**: 조건 본문은 런타임 독립, 실행법은 각 스킬이 자기 런타임 것만 기재한다 (실행법 미러 강제 없음, 스킬 구조까지만 미러).
- **불변식 — ralph 잔재 부재(v1 스코프)**: 4파일 하네스에 bash 루프/`run.sh`/state phase머신/컨테이너/별도 verification 파일이 없다 (`/goal` 네이티브 턴 루프이므로 ralph 실행 모델을 차용하지 않는다).
- **검증 의도**: Claude/Codex 양쪽에서 `goal-init` 호출 시 4파일이 규약 경로에 생성되고 조건 문자열이 평가자 적합성(자족 판정·evidence 매 턴 surface·4,000자 이하)을 만족하는지 확인한다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

`goal-init`을 Claude용·Codex용 두 스킬 디렉토리로 구현한다. 각 디렉토리는 `SKILL.md`(frontmatter → Goal → Acceptance Criteria → Hard Rules → Key Principles → Process 5단계 → Error Handling) + `skill.json` + `references/`(4파일 하네스 템플릿) + `examples/`(샘플 goal-init 세션)로 구성된다. 두 스킬의 SKILL.md 본문 구조와 Process는 미러이되, `/goal` 실행법(활성화·라이프사이클 명령) 섹션만 각 런타임 것으로 분리한다 (Part 1 "런타임 분리" 불변식 반영). 마지막으로 `marketplace.json` skills 배열에 두 경로를 등록한다.

이 draft는 `/goal` 동작 사실과 선례 패턴을 inline grounding하여 작성한다 (작성 대화·외부 `/goal` 문서를 reader가 다시 찾지 않아도 따라갈 수 있도록).

## Scope

Part 1 Scope Delta와 동일 범위. 구현 산출물은 8개 신규 파일(Claude 4 + Codex 4 — SKILL.md/skill.json/references 하네스 템플릿/examples 샘플) + `marketplace.json` 1개 수정. ralph-loop-init·기존 agent·README는 건드리지 않는다.

## Contract/Invariant Delta and Coverage

| ID | Type | Change | Covered By | Validated By |
|----|------|--------|------------|--------------|
| C1 | Add | `goal-init`은 discussion식 대화형 단일 스킬(신규 agent 없음)로 Claude/Codex 두 디렉토리에 존재한다 | T1, T2, T6 | V1 |
| C2 | Add | 실행 시 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 4파일(`goal.md`/`experiments.md`/`journal.md`/`report.md`)이 생성되고 조건 문자열이 사용자에게 제시된다 | T3, T4 | V2 |
| C3 | Add | `/goal` 조건 = 분업형: 완료조건(`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 조건에 자족 인라인, 루프 행동(HOW)은 `goal.md`의 `Loop Protocol` 참조 | T3, T4 | V3 |
| C4 | Add | 조건 본문은 런타임 독립, 실행법(활성화·라이프사이클 명령)만 각 스킬에 자기 런타임 것 기재 | T1, T2, T4 | V4 |
| C5 | Add | `marketplace.json` skills 배열에 두 경로 등록, agents 배열 불변 | T7 | V5 |
| I1 | Add | 생성되는 조건의 완료조건은 도구 없이 transcript만으로 판정 가능하고 4,000자 이하다 (Condition Crafting의 평가자 적합성 self-check가 강제) | T3 | V3 |
| I2 | Add | `goal-init`은 `/goal`을 직접 발동하지 않는다 (Step 5 Handoff는 조건+실행법 제시까지) | T3 | V6 |
| I3 | Add | Step 1 Goal Intake는 `/goal` 적합성 hard gate를 가진다 — verifiable end state 없는 단발성/모호 목표는 재정의 안내 후 진행 차단 | T3 | V6 |
| I4 | Add | Claude/Codex 두 SKILL.md는 본문 구조·Process가 미러이되 실행법 섹션만 분리된다 (구조 drift 금지) | T1, T2 | V4 |
| I5 | Add | 4파일 하네스에 bash 루프/`run.sh`/state phase머신/컨테이너/별도 verification 파일이 없다 (ralph 잔재 부재 — `/goal` 네이티브 턴 루프 스코프 불변식) | T0, T9 | V2 |

## Touchpoints

현재 코드 기준 재확인 결과 (Strategic Code Map은 본 repo에 없어 직접 탐색):

- `.claude/skills/discussion/` (SKILL.md / skill.json / references/ / examples/) — 대화형 단일 스킬의 권위 있는 구조 선례. `goal-init` SKILL.md 골격(frontmatter→AC→Hard Rules→Key Principles→Process(Step+Decision Gate)→Error Handling)과 `AskUserQuestion` 기반 단일 루프, "파일 생성은 마지막 단계에서만" 패턴을 차용한다. 읽기 참조 (Target Files 아님).
- `.claude/skills/ralph-loop-init/SKILL.md` + `.claude/agents/ralph-loop-init-agent.md` — append-only journal(decisions.md), conclusion-first report(final_report.md 구조: status PASS/FAIL/STUCK + Summary + Evidence + Risks + Next Actions), 적합성 hard gate 정신의 차용 원천. 단 entrypoint wrapper→agent 위임 구조와 bash 루프는 차용하지 않는다 (D5: agent 없는 단일 스킬). 읽기 참조.
- `.codex/skills/ralph-loop-init/SKILL.md` — Codex 스킬에 "Codex Runtime Adapter" 섹션이 있는 패턴 확인 (단, goal-init은 agent dispatch가 없으므로 이 adapter는 불필요). Codex 디렉토리는 references/examples 없이 SKILL.md+skill.json만으로도 운용되는 선례 확인 — 단 본 delta는 Claude와 동등하게 references/examples를 둔다 (C4 미러 구조).
- `.claude-plugin/marketplace.json` `plugins[0].skills` 배열 (line 17-39) — 등록 대상. agents 배열(line 40-50)은 불변.
- `.codex/skills/discussion/skill.json` 등 — Codex skill.json 포맷(name/description/instruction_file/version) 확인.

## Implementation Phases

**Phase 1 — 하네스 템플릿 확정 (선행)**: 4파일 템플릿(T3 본문에서 참조될 references)을 먼저 만든다. 조건 슬롯 구조(C3)·평가자 자족성(I1)·발산 메커니즘이 여기서 확정되어야 SKILL.md Process가 이를 가리킬 수 있다. → T3가 의존.

**Phase 2 — Claude 스킬 작성**: T1(Claude SKILL.md 골격) → T3(Process 5단계 + 적합성 gate + 조건 슬롯 규칙) → T5(skill.json) → T8(examples 샘플). T3는 Phase 1 템플릿 + T1 골격에 의존.

**Phase 3 — Codex 미러**: T2(Codex SKILL.md = T1/T3 미러 + Codex 실행법) → T6(skill.json). T1/T3 확정 후 진행 (구조 미러 — I4).

**Phase 4 — 등록**: T7(marketplace.json). 모든 디렉토리 경로 확정 후.

## Task Details

### Task T0: 4파일 하네스 references 템플릿 작성
**Priority**: P0
**Type**: Infrastructure

**Description**: SKILL.md Process가 참조할 4파일 하네스 템플릿을 `.claude/skills/goal-init/references/harness-templates.md`에 작성한다. 각 파일의 필드/포맷을 선례(ralph append-only decisions.md, conclusion-first final_report.md) 기반으로 확정한다. 4파일과 핵심 포맷:

- `goal.md`: (1) 목표 서술, (2) `/goal` 조건 문자열(분업형) — `DONE WHEN`(측정 가능 AC + 증명 명령/출력이 transcript에 PASS로 surface되는 형태를 인라인, 예: "`<cmd>` shows `<expected>` in transcript"), `CONSTRAINTS`(선택), `STOP`(턴 기준 기본), (3) `Loop Protocol` 섹션(루프 행동 HOW: "매 턴 `experiments.md`의 pending 가설 하나 시도 → 검증 명령 실행하고 출력을 대화에 표시 → `journal.md` append → 큐 비고 미완이면 새 가설 brainstorm해 append"), (4) 런타임별 실행법(각 스킬이 자기 런타임 것만 채움 — 본 템플릿엔 두 런타임 슬롯 표시).
- `experiments.md`: pending/done 두 섹션 가설 큐. 항목 필드 = 가설 한 줄 + 검증 방법(명령/판정조건) + 상태. 자동(루프)·사용자(수동) 공용.
- `journal.md`: append-only. 항목 = 타임스탬프/턴 + 시도한 가설 + 검증 명령·출력 요약 + 결과(통과/실패/부분) + 다음 결정. ralph decisions.md append-only 정신 차용.
- `report.md`: conclusion-first. 상단 status(PASS/FAIL/STUCK) + 요약 한 단락 + 시도한 가설 목록 + 근거(journal 참조) + 다음 단계 1-3개. ralph final_report.md 구조 차용.

**Non-Goals**: bash 루프·`run.sh`·state.md phase 상태머신·CHECKS.md·results/ 디렉토리는 만들지 않는다 (ralph 고유, `/goal` 네이티브 턴 루프엔 불필요). 별도 verification 파일을 두지 않는다 (검증은 대화 출력 + journal.md append).

**Acceptance Criteria**:
- [ ] `references/harness-templates.md`에 4개 파일(`goal.md`/`experiments.md`/`journal.md`/`report.md`) 템플릿이 각각 명확한 헤딩으로 존재한다.
- [ ] `goal.md` 템플릿이 `DONE WHEN`/`CONSTRAINTS`/`STOP` 슬롯과 별도 `Loop Protocol` 섹션을 가지며, `DONE WHEN` 예시가 "transcript에 surface되는 증명 형태"를 보인다 (별도 VERIFY 슬롯 없음).
- [ ] `experiments.md`가 pending/done 큐 구조를, `journal.md`가 append-only 항목 구조를, `report.md`가 conclusion-first(status 상단) 구조를 가진다.
- [ ] 4파일 어디에도 bash 루프/run.sh/컨테이너/state phase머신/별도 verification 파일이 등장하지 않는다.

**Target Files**:
- [C] `.claude/skills/goal-init/references/harness-templates.md` -- 4파일 하네스 템플릿 (신규: 기존 references 없음, SKILL.md Process가 참조할 단일 소스라 신규 파일로 분리)

**Technical Notes**: Covers C2, C3, I5, validated by V2, V3. Phase 1 산출물. Codex(T2)도 이 동일 템플릿을 references로 복사 사용한다 (T9 참조). 분업형 슬롯 근거 = D10(평가자가 도구 없이 transcript만 판정 + HOW 인라인 시 조건 비대·노이즈).
**Dependencies**: 없음 (선행 task)

### Task T1: Claude `goal-init` SKILL.md 골격 작성
**Priority**: P0
**Type**: Feature

**Description**: `.claude/skills/goal-init/SKILL.md`를 repo 스킬 규약 골격으로 작성한다. frontmatter(name: goal-init, description: "/goal", "goal 조건", "goal init", "goal-init", "set up goal", "goal helper" 등 트리거 문구 포함, version: 1.0.0) → Goal → Acceptance Criteria(AC1.. 체크박스) → Hard Rules → Key Principles → Process(5단계 placeholder, 상세는 T3) → Error Handling. discussion SKILL.md를 구조 선례로 따른다 (대화형 단일 스킬, `AskUserQuestion` 기반, 파일 생성은 Harness Setup 단계에서만).

Hard Rules에 반드시 포함: (1) 스킬은 `/goal`을 직접 발동하지 않는다 (I2), (2) 조건 완료부는 도구 없이 transcript만으로 판정 가능·4,000자 이하 (I1), (3) Goal Intake 적합성 gate 통과 없이 Divergence 진행 금지 (I3), (4) ralph-loop-init을 건드리지 않는다, (5) 4파일은 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에만 생성.

Error Handling 표: 목표가 단발성/모호(적합성 gate 실패) → 재정의 안내 또는 중단 / 검증 명령이 명령+판정조건으로 확정 안 됨 → 진행 차단(hard gate) / 조건이 4,000자 초과 → 응축 재시도 / Divergence에서 가설이 안 나옴 → 사용자에게 접근 후보 직접 요청.

**Non-Goals**: Process 5단계 본문 상세는 T3에서 채운다 (여기선 단계 이름·Decision Gate placeholder만). Codex 실행법은 T2에서.

**Acceptance Criteria**:
- [ ] frontmatter에 name/description/version이 있고 description에 `goal-init` 트리거 문구가 포함된다.
- [ ] SKILL.md가 Goal → Acceptance Criteria → Hard Rules → Key Principles → Process → Error Handling 순서를 가진다.
- [ ] Hard Rules에 비발동(I2)·평가자 자족성/4000자(I1)·적합성 gate(I3)·ralph 불간섭·산출 경로 5개 규칙이 명시된다.
- [ ] Process 섹션에 5단계(Goal Intake/Divergence/Condition Crafting/Harness Setup/Handoff) 이름과 Decision Gate placeholder가 있다.
- [ ] Error Handling 표에 적합성 gate 실패·검증 미확정·4000자 초과·가설 부재 4행 이상이 있다.

**Target Files**:
- [C] `.claude/skills/goal-init/SKILL.md` -- Claude 스킬 본문 (신규 스킬)

**Technical Notes**: Covers C1, C4, I2, I4, validated by V1, V4, V6. discussion SKILL.md(`.claude/skills/discussion/SKILL.md`)를 구조 선례로 참조. Phase 2 진입점. T3가 이 파일의 Process 본문을 채운다.
**Dependencies**: 없음 (선행). T3가 본 파일의 Process 본문을 이어서 채운다 (동일 파일 직렬 — T1 골격 먼저, 그 다음 T3).

### Task T3: Claude SKILL.md Process 5단계 본문 작성
**Priority**: P0
**Type**: Feature

**Description**: T1이 만든 Claude `SKILL.md`의 Process 섹션을 5단계 본문으로 채운다. 각 단계와 Decision Gate:

1. **Goal Intake** — 목표 수집 + `/goal` 적합성 hard gate. gate 기준: "verifiable end state가 있는 멀티턴 작업인가". "한 줄 수정"·"모호한 목표"면 재정의 안내 후, 재정의 불가 시 중단 (I3). Gate 1→2: 적합 목표 확정 시 진행.
2. **Divergence** — 목표 달성 접근/가설 2-3개를 AI가 능동 발산(discussion의 alternatives-initiation 차용: 권장안 먼저 + 트레이드오프) → `experiments.md` 초기 pending 백로그로 수집. Gate 2→3: 가설 2개 이상 확보.
3. **Condition Crafting** — 5요소(목표/측정 가능 AC/증명 방법/제약/종료 경계)를 조건 문자열로 응축 + **평가자 적합성 self-check**: (a) 도구 없이 대화만으로 판정 가능한가, (b) evidence가 매 턴 surface되나, (c) 4,000자 이하인가. self-check 실패 시 응축 재시도 (hard gate — I1). 조건은 분업형(C3, T0 템플릿 슬롯 사용). Gate 3→4: self-check 3항목 통과.
4. **Harness Setup** — `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 T0 템플릿으로 4파일 생성. `goal.md`에 확정 조건 문자열 + `Loop Protocol`(큐 소비·자동 발산·검증 출력·journal append 규칙) 기입. 실행법 슬롯엔 Claude 것만 채움(T4가 정의).
5. **Handoff** — 조건 문자열 + Claude 실행법 제시. **스킬은 `/goal`을 발동하지 않음**, 사용자가 검토 후 직접 발동 (I2).

**Non-Goals**: 요청되지 않은 단계·옵션·설정값을 추가하지 않는다 (5단계 고정). 발산 알고리즘을 추상 프레임워크로 일반화하지 않는다 (discussion alternatives-initiation 패턴 그대로).

**Acceptance Criteria**:
- [ ] Process에 5단계가 순서대로 본문과 함께 있고 각 단계 끝에 Decision Gate가 있다.
- [ ] Step 1에 적합성 gate 기준("verifiable end state 있는 멀티턴 작업")과 실패 시 재정의/중단 분기가 명시된다.
- [ ] Step 2가 AI 능동 발산(권장안 먼저 + 2-3개) → `experiments.md` pending 백로그 수집을 명시한다.
- [ ] Step 3에 평가자 적합성 self-check 3항목(도구 없이 판정·evidence 매 턴 surface·4000자 이하)이 hard gate로 명시되고, 조건이 분업형(`DONE WHEN`/`CONSTRAINTS`/`STOP` + `Loop Protocol` 분리)임이 명시된다.
- [ ] Step 4가 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 4파일 생성 + `Loop Protocol`(큐 소비·자동 발산·검증 출력·journal append) 기입을 명시한다.
- [ ] Step 5가 "스킬은 발동하지 않고 사용자가 직접 `/goal`"을 명시한다.

**Target Files**:
- [M] `.claude/skills/goal-init/SKILL.md` -- Process 섹션 본문 채우기

**Technical Notes**: Covers C2, C3, I1, I2, I3, validated by V2, V3, V6. T0 템플릿 슬롯과 1:1 대응. discussion 3.2.1 alternatives-initiation을 Divergence 출처로 inline grounding. T1과 동일 파일이므로 T1 이후 수행.
**Dependencies**: T1 (골격 먼저), T0 (템플릿 슬롯 참조)

### Task T5: Claude `goal-init` skill.json 작성
**Priority**: P1
**Type**: Infrastructure

**Description**: `.claude/skills/goal-init/skill.json`을 discussion skill.json 포맷(name/description/instruction_file/version)으로 작성한다. name=goal-init, description=SKILL.md frontmatter description과 동일 트리거 문구, instruction_file=SKILL.md, version=1.0.0.

**Acceptance Criteria**:
- [ ] `skill.json`에 name=goal-init, instruction_file=SKILL.md, version, description(트리거 문구 포함) 4필드가 있다.
- [ ] description이 SKILL.md frontmatter description과 일치한다.

**Target Files**:
- [C] `.claude/skills/goal-init/skill.json` -- 스킬 매니페스트 (신규 스킬 필수 파일)

**Technical Notes**: Covers C1, validated by V1. `.claude/skills/discussion/skill.json` 포맷 따름.
**Dependencies**: T1 (description 문구 일치)

### Task T8: Claude `goal-init` examples 샘플 세션 작성
**Priority**: P2
**Type**: Test

**Description**: `.claude/skills/goal-init/examples/sample-goal-init-session.md`에 goal-init 한 번의 대화 흐름 예시를 작성한다. 5단계가 어떻게 진행되어 4파일 + 분업형 조건 문자열이 나오는지 1개 구체 시나리오로 보인다. 조건 문자열 예시는 평가자 적합성 3항목(자족 판정·evidence surface·4000자 이하)을 만족하는 형태를 보인다.

**Acceptance Criteria**:
- [ ] `examples/sample-goal-init-session.md`에 5단계 진행 + 산출 4파일 경로 + 최종 분업형 조건 문자열 예시가 있다.
- [ ] 예시 조건 문자열의 `DONE WHEN`이 "transcript에 surface되는 증명" 형태이고 4,000자 이하다.

**Target Files**:
- [C] `.claude/skills/goal-init/examples/sample-goal-init-session.md` -- 샘플 세션 (신규 스킬 examples, discussion examples 선례 따름)

**Technical Notes**: Covers C2, C3, validated by V2, V3. `.claude/skills/discussion/examples/sample-discussion-session.md` 선례 따름.
**Dependencies**: T0, T3 (템플릿·Process 확정 후 예시 일관성)

### Task T2: Codex `goal-init` SKILL.md 작성 (구조 미러 + Codex 실행법)
**Priority**: P0
**Type**: Feature

**Description**: `.codex/skills/goal-init/SKILL.md`를 Claude SKILL.md(T1+T3)의 본문 구조·Process 5단계 미러로 작성한다. 차이는 단 하나 — 조건 본문은 런타임 독립으로 동일하되, **실행법 섹션만 Codex 것**으로 기재한다: (a) `features.goals` 활성화(`codex features enable goals` 또는 config), (b) 라이프사이클 = set/status/clear + pause/resume, (c) thread-scoped state·안전 경계(turn 종료/idle/no queued input) continuation 체크, (d) evidence-based completion 강조. Claude 전용 항목(workspace trust+hooks, disableAllHooks/allowManagedHooksOnly 제약, `--resume`/`--continue` 복원, `clear` 별칭 stop/off/reset 등)은 넣지 않는다.

`goal.md` 템플릿의 "런타임별 실행법" 슬롯 안내도 Codex 것만 채우도록 Process Step 4/5 실행법 서술을 Codex 명령으로 교체한다.

**Non-Goals**: Codex Runtime Adapter(agent dispatch) 섹션을 넣지 않는다 — goal-init은 agent 없는 단일 대화 스킬이라 sub-agent dispatch가 없다. 본문 구조·Process 단계·Decision Gate·Hard Rules를 Claude와 다르게 바꾸지 않는다 (실행법 외 drift 금지 — I4).

**Acceptance Criteria**:
- [ ] `.codex/skills/goal-init/SKILL.md`의 Goal/AC/Hard Rules/Key Principles/Process 5단계/Error Handling 구조가 Claude 버전과 미러(단계 이름·Gate·조건 슬롯 규칙 동일)다.
- [ ] 실행법 서술이 Codex 것(features.goals 활성화·pause/resume·thread-scoped·evidence-based)만 담고 Claude 전용 항목(trust+hooks·clear 별칭·resume 복원)을 담지 않는다.
- [ ] 조건 본문(`DONE WHEN`/`CONSTRAINTS`/`STOP` + `Loop Protocol` 분업형)이 Claude 버전과 동일하다.
- [ ] Codex Runtime Adapter(agent dispatch) 섹션이 없다.

**Target Files**:
- [C] `.codex/skills/goal-init/SKILL.md` -- Codex 스킬 본문 (신규)

**Technical Notes**: Covers C1, C4, I4, validated by V1, V4. Codex `/goal` 사실은 작성 입력에서 inline grounding(features.goals 활성화·pause/resume·thread-scoped continuation·evidence-based 6요소). T1/T3 확정 후 미러.
**Dependencies**: T1, T3 (미러 원본)

### Task T9: Codex `goal-init` references 하네스 템플릿 복사
**Priority**: P1
**Type**: Infrastructure

**Description**: T0이 만든 `.claude/skills/goal-init/references/harness-templates.md`를 `.codex/skills/goal-init/references/harness-templates.md`로 verbatim 복사한다. 단 `goal.md` 템플릿의 "런타임별 실행법" 슬롯 안내 문구를 Codex 실행법(features.goals·pause/resume)으로 맞추는 것만 허용한다 (조건 본문·4파일 구조·슬롯은 동일).

**Acceptance Criteria**:
- [ ] `.codex/skills/goal-init/references/harness-templates.md`가 존재하고 4파일 템플릿 구조가 Claude 버전과 동일하다.
- [ ] 실행법 슬롯 안내만 Codex 것이고, 조건 슬롯·journal/report/experiments 포맷은 Claude 버전과 동일하다.

**Target Files**:
- [C] `.codex/skills/goal-init/references/harness-templates.md` -- Codex 하네스 템플릿 (T0 복사, 실행법 슬롯만 조정)

**Technical Notes**: Covers C2, C4, I5, validated by V2, V4. verbatim 복사 + 실행법 슬롯 치환 (재구성 금지 — 템플릿 drift 방지).
**Dependencies**: T0 (복사 원본)

### Task T10: Codex `goal-init` examples 샘플 복사
**Priority**: P2
**Type**: Test

**Description**: T8의 `sample-goal-init-session.md`를 `.codex/skills/goal-init/examples/sample-goal-init-session.md`로 복사하되 실행법(Step 5 Handoff) 부분만 Codex 명령으로 맞춘다.

**Acceptance Criteria**:
- [ ] `.codex/skills/goal-init/examples/sample-goal-init-session.md`가 존재하고 5단계 흐름·4파일·분업형 조건이 Claude 예시와 동일 구조다.
- [ ] Handoff 실행법만 Codex(`/goal` + features.goals) 것이다.

**Target Files**:
- [C] `.codex/skills/goal-init/examples/sample-goal-init-session.md` -- Codex 샘플 (T8 복사, 실행법만 조정)

**Technical Notes**: Covers C2, validated by V2. T8 복사 + 실행법 치환.
**Dependencies**: T8 (복사 원본)

### Task T6: Codex `goal-init` skill.json 작성
**Priority**: P1
**Type**: Infrastructure

**Description**: `.codex/skills/goal-init/skill.json`을 Codex skill.json 포맷으로 작성한다 (name/description/instruction_file/version). 내용은 Claude skill.json(T5)과 동일.

**Acceptance Criteria**:
- [ ] `.codex/skills/goal-init/skill.json`에 name=goal-init, instruction_file=SKILL.md, version, description 4필드가 있다.

**Target Files**:
- [C] `.codex/skills/goal-init/skill.json` -- Codex 매니페스트 (신규)

**Technical Notes**: Covers C1, validated by V1. `.codex/skills/discussion/skill.json` 포맷 따름.
**Dependencies**: T2 (description 문구 일치)

### Task T7: `marketplace.json`에 goal-init 등록
**Priority**: P1
**Type**: Infrastructure

**Description**: `.claude-plugin/marketplace.json`의 `plugins[0].skills` 배열에 `"./.claude/skills/goal-init"`를 알파벳/논리 순서에 맞게 추가한다. `agents` 배열은 신규 agent가 없으므로 변경하지 않는다.

**Non-Goals**: agents 배열·다른 skills 항목·metadata를 건드리지 않는다.

**Acceptance Criteria**:
- [ ] `skills` 배열에 `./.claude/skills/goal-init` 항목이 추가된다.
- [ ] `agents` 배열은 변경되지 않는다 (diff에서 agents 영역 무변경).

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- skills 배열에 goal-init 경로 추가

**Technical Notes**: Covers C5, validated by V5. Codex 스킬은 `.codex/skills/` 디렉토리에 별도 존재하며 이 배열엔 Claude 경로만 등록(기존 패턴 — discussion 등도 `.claude/skills/` 경로만 등재).
**Dependencies**: T1 (디렉토리 경로 존재 확정)

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1 | 2등급 (rubric 판정) | 리뷰어가 `.claude/skills/goal-init/`와 `.codex/skills/goal-init/`에 SKILL.md+skill.json이 존재하고 둘 다 대화형 단일 스킬(agent 위임/신규 agent 없음)임을 확인. 위반 사례(누락 파일·agent 위임 서술·marketplace agents 배열 변경)를 지목하지 못하면 충족. 증거 = 파일 트리 + 두 SKILL.md 인용 |
| V2 | C2, I5 | 2등급 (rubric 판정) + 1등급 sub | (2등급) 리뷰어가 SKILL.md Step 4 + examples 샘플에서 4파일이 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 생성되고 조건 문자열이 사용자에게 제시됨을 확인. 4파일 중 누락·잘못된 경로·조건 미제시를 지목하지 못하면 충족. 증거 = Step 4 본문 + harness-templates.md 4헤딩 인용. (1등급 sub — I5 ralph 잔재 부재) `harness-templates.md`(및 Codex 복사본)에 `run.sh`/`while true`/`state.md`/state phase머신/컨테이너 토큰이 grep으로 0건. 증거 = `grep -iE 'run\.sh|while[ -]?true|state\.md|state machine|container' harness-templates.md` 출력 = 빈 결과(매치 0) |
| V3 | C3, I1 | 2등급 (rubric 판정) + 1등급 sub | (2등급) 리뷰어가 (a) 조건이 `DONE WHEN`/`CONSTRAINTS`/`STOP` + 별도 `Loop Protocol`로 분업되고, (b) `DONE WHEN`이 transcript-surface 증명 형태이며 별도 VERIFY 슬롯이 없고, (c) Step 3 self-check가 도구없이판정·evidence매턴surface·4000자이하를 hard gate로 강제함을 확인. 세 조건 중 위반을 지목하지 못하면 충족. 증거 = Step 3 본문 + goal.md 템플릿 슬롯 인용. (1등급 sub — I1 4000자 상한) T8 examples 샘플의 조건 문자열 문자 수 ≤ 4000. 증거 = 샘플 조건 문자열 구간을 잘라 `wc -m`(또는 동등 카운트) 출력 ≤ 4000 |
| V4 | C4, I4 | 2등급 (rubric 판정) | 리뷰어가 Claude/Codex 두 SKILL.md를 대조해 (a) Goal/AC/Hard Rules/Process 5단계/Gate가 미러이고, (b) 실행법 섹션만 각 런타임 것(Claude=trust+hooks/clear, Codex=features.goals/pause-resume)으로 분리됨을 확인. 구조 drift(실행법 외 차이)나 실행법 교차오염(Claude에 Codex 명령 등)을 지목하지 못하면 충족. 증거 = 두 SKILL.md 섹션 diff |
| V5 | C5 | 1등급 (정량) | `marketplace.json` 파싱 후 `skills` 배열에 `./.claude/skills/goal-init` 포함 = true AND `agents` 배열 길이/내용이 변경 전과 동일 = true. 증거 = 파싱 출력(grep/jq 결과 또는 diff에서 agents 영역 0 line 변경) |
| V6 | I2, I3 | 2등급 (rubric 판정) | 리뷰어가 (a) SKILL.md 어디에도 스킬이 `/goal`을 직접 발동하는 서술이 없고 Step 5가 "사용자가 직접 발동"임을, (b) Step 1에 verifiable end state 적합성 hard gate + 실패 시 재정의/중단 분기가 있음을 확인. 발동 서술이나 gate 부재를 지목하지 못하면 충족. 증거 = Step 1·Step 5 본문 + Hard Rules 인용 |

모든 task AC는 위 `V*`에 1:1 대응한다 (T0→V2·V3, T1→V1·V4·V6, T2→V1·V4, T3→V2·V3·V6, T5→V1, T6→V1, T7→V5, T8→V2·V3, T9→V2·V4, T10→V2). I5(ralph 잔재 부재)는 V2 1등급 sub-evidence로, I1 4000자 상한은 V3 1등급 sub-evidence로 측정 검증된다. AC 없는 `V*`·`V*` 없는 AC는 없다.

## Parallel Execution Summary

- **선행 단일**: T0(하네스 템플릿)은 의존 없는 선행 task. 가장 먼저 단독 실행.
- **Phase 2 직렬**: T1 → T3은 동일 파일(`.claude/skills/goal-init/SKILL.md`)이라 직렬 (파일 겹침 — 골격 후 본문). T5(skill.json)는 T1 description 확정 후 병렬 가능, T8(examples)은 T0+T3 후.
- **Phase 3 미러**: T2는 T1/T3 확정 후 (구조 미러 원본 의존 — 의미적 충돌: API contract 생산-소비 패턴, Claude SKILL.md가 Codex SKILL.md의 미러 원본). T9(references 복사)는 T0 후, T10(examples 복사)은 T8 후, T6(skill.json)은 T2 후. T2 확정 뒤 T9/T10/T6은 서로 다른 파일이라 상호 병렬 가능.
- **등록**: T7(marketplace.json)은 Claude 디렉토리 경로 확정(T1) 후 단독. 다른 파일과 겹치지 않으나 T1 경로 존재에 의존.
- **충돌 인코딩**: T1↔T3 파일 겹침은 T3→T1 dependency로, T2의 미러 원본 의존은 T2→{T1,T3} dependency로, 복사 task(T9/T10/T6)의 원본 의존은 dependency로 인코딩됨. Target Files disjoint + dependency 없음 조합(예: T2 확정 후 T9/T10/T6)만 동시 실행 그룹.

# Risks/Mitigations and Open Questions

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| R-EVAL: 생성 조건이 도구 없이 판정 불가능한 형태(예: "테스트 통과"인데 출력이 transcript에 안 드러남)로 나옴 | `/goal` 평가자가 영원히 미충족 판정 → 무인 루프 토큰 낭비 | Step 3 평가자 적합성 self-check를 hard gate로 두고(I1), `DONE WHEN`에 "`<cmd>` shows `<expected>` in transcript" 형태를 강제 (T0 템플릿 예시) |
| R-DRIFT: Claude/Codex 두 SKILL.md가 시간이 지나며 구조가 갈라짐 | 런타임 간 동작 불일치, 유지보수 부담 | I4 미러 불변식 + V4 대조 검증. 미러는 본문 구조까지, 실행법만 분리 (D7) |
| R-4000: 복잡한 목표에서 조건이 4,000자를 넘김 | Claude `/goal` 평가자 상한 초과로 조건 거부 | Loop Protocol(HOW)을 조건이 아닌 `goal.md`로 분리(C3·D10)해 조건 본문을 완료조건만으로 슬림 유지. self-check 4000자 항목으로 검출 후 응축 |
| R-SCOPE: 구현 중 ralph 대체·bash 루프 유혹으로 v1 스코프 팽창 | D2 위반, 산출물 비대 | Out-of-scope 명시 + T0 Non-Goals(bash/run.sh/state머신 금지). 핸드오프 중단 조건(D2/D8 모순 시 보고) 준수 |
| R-DOC: README/워크플로우 미통합으로 사용자가 goal-init 존재를 모름 | 발견성 저하 (기능 자체엔 무해) | v1 out-of-scope(Action Item Low). marketplace.json 등록(C5)으로 최소 발견성 확보, docs 통합은 후속 |

## Open Questions

### Q1. ralph-loop를 `/goal` 기반으로 대체할 수 있는가 / 해야 하는가
- **Decision taken**: v1에서 deferred. goal-init은 대화형 goal-helper로만 한정하고 ralph 대체를 시도하지 않는다.
- **Alternatives considered**: (a) v1에 ralph 대체 결합 → `/goal`은 턴 기반·평가자 도구 미사용이라 컨테이너 장시간 비대화형 머신검증 작업을 메커니즘상 대체하기 어렵고 v1 스코프가 비대해져 기각. (b) goal-init이 ralph로 핸드오프하는 브리지 → v1 범위 밖, 근거 부족으로 보류.
- **Confidence**: HIGH
- **User confirmation needed**: No (discussion D2에서 사용자 확정)

### Q2. 4파일 각각의 구체 포맷·필드 (goal.md 조건 슬롯은 D10으로 해소됨)
- **Decision taken**: 선례(ralph append-only decisions.md, conclusion-first final_report.md, discussion 요약 포맷) 기반으로 T0에서 초안 확정 — `experiments.md`(pending/done 큐 + 가설·검증방법·상태), `journal.md`(append-only 시도·검증결과·결정), `report.md`(conclusion-first status+요약+가설+근거+다음단계). YAGNI 적용(별도 verification 파일 없음).
- **Alternatives considered**: (a) 5파일(verification 분리) → 검증을 대화+journal로 surface하면 충분, 과설계로 기각. (b) 3파일 미니멀 → 큐와 로그가 한 파일에 섞여 가독성·append 충돌, 기각.
- **Confidence**: MEDIUM (포맷 세부는 구현 후 review-fix로 조정될 수 있음)
- **User confirmation needed**: No (Q2가 deferred-deliberately로 "구현 단계 초안 후 확정" 합의됨 — review-fix 루프가 수렴 담당)
