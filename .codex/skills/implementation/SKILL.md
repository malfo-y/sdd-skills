---
name: implementation
description: Use this skill when the user wants to execute an implementation plan, start implementing tasks from a plan, work through a development roadmap, says "implement the plan", "start implementation", "execute the plan", "work on the tasks", or explicitly asks for "implement parallel", "parallel implementation", "병렬 구현", "병렬로 구현". Uses conflict-aware parallel execution when Target Files are available.
version: 3.1.0
---

# Implementation Orchestrator (Parallel TDD)

이 스킬은 **orchestrator**다. 메인 루프에서 실행되어 fan-out이 가능하다. task-set을 확보하고(plan 파싱 또는 plan 없으면 경량 분해), dependency 기반으로 병렬 그룹을 파생해 **`implementation_agent` leaf를 task당 spawn**하며, 통합·회귀·phase review·report를 소유한다. 각 task의 TDD(RED→GREEN→REFACTOR)는 leaf가 수행한다. 병렬화는 최적화 토글일 뿐 — 불가하면 동일 흐름으로 순차 실행한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: task-set을 확보한다 — plan 파싱(있을 때) 또는 plan 없으면 요청을 task로 경량 분해
- [ ] AC2: dependency 기반 병렬 그룹 파생("같은 phase + dependency edge 없음 + Target Files disjoint → 병렬") + file-disjoint 가드레일 + 순차 fallback
- [ ] AC3: 그룹 내 task마다 `implementation_agent` leaf를 spawn하고 leaf 입력 4종(task 필드 + Target Files + 환경/테스트 + 선행 보장)을 전달
- [ ] AC4: post-group 통합·회귀·phase review를 orchestrator가 수행하고 leaf 출력(UNPLANNED_DEPENDENCY 등)을 처리
- [ ] AC5: `_sdd/implementation/<YYYY-MM-DD>_implementation_report_<slug>.md` 및 progress artifact를 canonical 경로·필드로 생성(orchestrator 소유)
- [ ] AC6: leaf 출력이 AC 외 추가 코드(옵션·설정·추상화·에러 처리)를 포함하지 않으며, 발견 시 Phase Review에서 Quality 또는 Critical로 분류 (Minimum-Code Mandate)
- [ ] AC7: 시작 전 Plan Assumptions와 Phase별 Surprises가 사용자에게 노출됐다 (해당 항목이 없으면 생략 가능)

## Hard Rules

1. **Spec 파일 불가침**: `_sdd/spec/` 하위 파일을 생성/수정/삭제하지 않는다. Spec drift 발견 시 리포트에 기록하고 `spec-update-todo` 사용을 안내한다.
2. **TDD는 leaf가 수행**: 각 task의 RED→GREEN→REFACTOR는 leaf(`implementation_agent`)가 담당한다. orchestrator는 per-task TDD 절차를 복제하지 않는다.
3. **파일 경계 준수**: leaf는 할당된 Target Files만 생성/수정/삭제한다. 그 외 파일은 읽기 전용이며, leaf가 `UNPLANNED_DEPENDENCY`로 보고하면 orchestrator가 유효성을 판단해 처리한다.
4. **Verification Gate**: "should work" 금지. post-group 검증에서 테스트를 실제 재실행하고 출력을 근거로 제시한다. 이전 실행 결과 재사용 금지. `_sdd/env.md` 미존재 시 코드 분석 기반 검증을 허용하되, 리포트에 `UNTESTED` 표기.
5. **Regression Iron Rule**: 기존 테스트 실패 시 (1) 테스트 업데이트 + (2) 회귀 방지 테스트 추가를 사용자 확인 없이 자동 수행한다.
6. **Artifact Naming Transition**: 결과 파일은 lowercase canonical 경로에 저장하고, transition 기간에는 plan/progress/report의 legacy uppercase 경로를 입력 fallback으로 허용한다.
7. **Minimum-Code Mandate**: leaf와 후속 검증은 AC가 요구하는 동작만 구현·검증한다. 요청되지 않은 옵션·설정·추상화·에러 처리 추가 금지. 사변적 형용사("future-proof / extensible / configurable")는 task의 Technical Notes에 근거가 명시될 때만 허용. **REFACTOR 단계도 단일 사용처 추상화 도입은 금지한다.**

### Target Files 규격

- 모든 태스크에 `**Target Files**:` 필드 필수
- 마커: `[C]` 생성, `[M]` 수정, `[D]` 삭제
- 읽기 전용 참조는 Target Files에 포함하지 않음

### 그룹 파생과 file-disjoint 가드레일

orchestrator는 **dependency를 그룹화의 권위 있는 신호로 신뢰**한다. 의미적 충돌(모델 import, 동시 마이그레이션, 동일 config, API 생산-소비, 상수 충돌)은 planner(`feature-draft`/`implementation-plan`)가 task `Dependencies` edge로 인코딩하므로(무방향 mutex도 임의 방향 dep로 흡수), orchestrator는 이를 재검출하지 않는다.

병렬 판단 규칙:

- **같은 phase + dependency edge 없음 + Target Files disjoint → 병렬 그룹**. 그 외는 순차.
- **file-disjoint 가드레일**(상시): fan-out 직전 그룹 내 task들의 Target Files가 실제로 disjoint한지 set-intersection으로 검사한다. 동일 파일이 두 task에 등장하면(마커 무관) 그 그룹을 순차로 내린다. plan staleness/dependency 누락에 대한 싸구려 안전망.
- **확신 없으면 순차**: dependency 정보가 빈약·부재하면(구식 plan 등) 순차로 기본 fallback한다. 덜 병렬화될 뿐 오작동하지 않는다.

> 파일 충돌 매트릭스 — 동일 파일이 두 task의 Target Files에 등장하면 마커 무관하게 충돌(`[C]+[C]` 동시 생성, `[M]+[M]` 동시 수정, `[C]+[M]`·`[M]+[D]`·`[C]+[D]` 순서 의존, `[D]+[D]` 중복 삭제). file-disjoint 가드레일이 이 매트릭스를 적용한다.

## Process

### Step 1: Secure the Task-Set

**경로 A — plan 파싱** (plan이 있을 때). 탐색 순서:
1. 사용자 지정 경로
2. `_sdd/implementation/*_implementation_plan_*.md` (slug 기반 glob)
3. `_sdd/implementation/implementation_plan.md` (legacy 고정 경로)
4. `_sdd/implementation/implementation_plan_phase_<n>.md`
5. legacy uppercase fallback: `_sdd/implementation/IMPLEMENTATION_PLAN.md`, `_sdd/implementation/IMPLEMENTATION_PLAN_PHASE_<N>.md`
6. `_sdd/drafts/*_feature_draft_*.md` (slug 기반 glob, Part 2: 구현 계획)
7. `_sdd/drafts/feature_draft_<name>.md` (legacy 고정 경로)

복수 파일 존재 시 사용자에게 확인. plan에서 추출: Components, Phases, Tasks (Target Files·Dependencies 포함), Open Questions.

**경로 B — no-plan 경량 분해** (plan이 없을 때). plan 작성 스킬로 되돌리지 않고, 사용자 요청을 직접 task로 **경량 분해**한다(충돌분석 rigor 불필요 — 순차 실행이므로). 각 조각에 Target Files를 best-effort로 부여하고, 저확신이면 순차 실행한다. 분해 가정을 리포트에 기록한다.

> 두 경로 모두 동일한 후속 흐름(Step 2~7)을 탄다. 차이는 task-set의 출처뿐이며, plan 유무·병렬/순차와 무관하게 정확한 결과를 낸다(병렬은 최적화).

#### Surface Plan Assumptions

task-set 확보 직후, 사용자에게 다음을 채팅으로 알림한다 (질문 아님 — redirect는 사용자가 다음 turn에 지시):

- Plan `Open Questions` 중 Confidence=LOW 또는 User confirmation needed=Yes 항목 (4-필드 스키마를 따르지 않는 plan은 Open Q 항목을 보수적으로 모두 노출)
- 본 실행에 적용될 Autonomous Decision-Making 카테고리 예고 (해당 항목이 있는 경우)

항목당 1줄: `[Qn] <Decision taken 요약> (출처/근거)`. 해당 항목이 없으면 "사용자 확인이 필요한 항목 없음" 한 줄로 마친다.

### Step 2: Initialize Task Tracking

`_sdd/implementation/<YYYY-MM-DD>_implementation_progress_<slug>.md`에 tracking row를 만든다:
- task_id, title, phase, dependencies, status, owner/leaf, notes
- 초기 상태는 dependency 존재 시 `BLOCKED`, 없으면 `READY`

이 progress artifact는 orchestrator가 소유하며, 경로·필드는 downstream(`spec-update-done`·`spec-summary`)이 소비하므로 canonical 형식을 보존한다.

### Step 3: Derive Parallel Groups

#### 3.1 Target Files 가용성 판단

| 상황 | 처리 |
|------|------|
| 모든 태스크에 Target Files 있음 | 전체 그룹 파생 |
| 일부만 있음 | 있는 태스크만 병렬 후보, 나머지 순차 |
| 없음 | 추론 시도 → 저확신 시 순차 fallback |

#### 3.2 그룹 파생 알고리즘

unblocked task에 대해 dependency 기반 규칙 + file-disjoint 가드레일을 적용한다:

```
function deriveGroups(unblockedTasks):   # 모두 같은 phase
    groups = []
    remaining = sort(unblockedTasks, by=[priority DESC, id ASC])
    while remaining not empty:
        group = []
        usedFiles = {}
        for task in remaining:
            # dependency edge 없음 (planner가 의미적 충돌을 dep로 인코딩)
            # AND Target Files disjoint (file-disjoint 가드레일)
            if no dependency edge between task and group
               AND task.targetFiles ∩ usedFiles == ∅:
                group.append(task); usedFiles ∪= task.targetFiles
        groups.append(group); remaining -= group
    return groups
```

> 대규모 Phase (10+ unblocked tasks): 그룹 크기를 최대 5로 제한.

#### 3.3 병렬 실행 계획 표시

실행 전 사용자에게 그룹 구성과 예상 효율을 보여준다.

### Step 4: Fan-out by Phase

```
For each phase:
  1. Unblocked 태스크에서 그룹 파생 (Step 3)
  2. For each group:
     a. 그룹 내 task마다 implementation_agent leaf를 spawn
     b. wait_agent로 전원 완료 수거
     c. Post-group 통합·검증 (Step 5)
     d. 실패/Unplanned Dependency 처리
  3. 전체 그룹 완료 → Phase Review (Step 6)
```

#### Leaf Dispatch

그룹 내 task마다 leaf를 dispatch한다:

- `spawn_agent(agent_type="implementation_agent", prompt=<leaf 입력>)`로 그룹 내 task를 동시 spawn하고, `wait_agent`로 결과를 수거한다.

leaf 입력(프롬프트)에 다음 4종을 전달한다 (leaf는 재탐색하지 않음):

```
## Task {id}: {title}
- Component / Priority / Description / Acceptance Criteria / Technical Notes

## Target Files (쓰기 허용 경계)
{target_files_list}

## 환경/테스트 (orchestrator가 로드해 전달)
{test_command}
{env_setup}     # _sdd/env.md에서 orchestrator가 1회 로드

## 선행 보장
이 task의 dependency는 완료됨. 그 산출물은 read-only 참조 가능.
```

leaf는 단일 task를 TDD로 구현하고 구조화된 결과(SUCCESS/PARTIAL/FAILED·TDD표·파일·테스트·UNPLANNED_DEPENDENCY·발견)를 반환한다.

#### Sequential Fallback

병렬 불가(파일 충돌·dependency·Target Files 부재·no-plan 저확신)면 동일 leaf를 하나씩 순차 spawn한다. 흐름은 동일하고 병렬성만 빠진다.

### Step 5: Integrate & Verify (Post-Group)

각 그룹 완료 후 orchestrator가 수행한다:

| 단계 | 내용 |
|------|------|
| 전체 테스트 | 새 테스트 + 기존 테스트 실행, 회귀 확인 |
| Unplanned Dependency | leaf 보고 수집 → 유효성 판단 → 해결 → 재검증 |
| leaf 실패 | 다른 leaf에 영향 없음. 실패 태스크는 순차 재시도, 2회 실패 시 사용자 보고 |
| 파일 경계 위반 | 미승인 변경 롤백 → 순차 재실행 |
| 태스크 상태 | 성공 → completed, 실패 → in_progress (재시도용), 부분 → 미완료 기준 기록 |

### Step 6: Phase Review-Fix Gate (외부 reviewer loop)

Phase 내 모든 태스크 완료 후, orchestrator는 **외부 `implementation_review_agent` review→fix→re-review loop**를 닫는다. 인라인 경량 self-review를 대체한다 — orchestrator가 직접 품질을 판정하지 않고 독립 reviewer agent를 spawn한다.

**loop scope**: **실행분(phase) 단위 1 gate**. 각 phase 완료 직후 1회 닫고 다음 phase로 진행한다. autopilot의 global/per-group·Checkpoint 메타 개념은 도입하지 않는다(직접 호출 경로엔 Checkpoint 신호를 줄 상위 오케스트레이터가 없음). multi-phase plan이면 phase마다 1회씩 닫힌다.

**공통 loop 정책** (autopilot `references/orchestrator-contract.md` §6 Review-Fix Contract 차용):

- **exit 조건**: `critical=0 AND high=0 AND medium=0` (= `critical=high=medium=0`).
- **MAX**: 기본 3 iteration.
- **re-review scope**: loop 범위(이 phase) **전체 재리뷰** (변경분만 아님).
- **1 iteration 경계**: `review/re-review → finding>0이면 fix → 산출물 갱신`.
- **MAX 도달 분기**: critical/high 잔존 → 중단·사용자 보고. medium만 잔존 → 로그 후 진행(advisory degrade).

**단계**:

1. **review**: `spawn_agent(agent_type="implementation_review_agent", ...)`(model: opus)로 이 phase 범위의 변경 파일 전체 + 테스트 결과를 전달하고 `wait_agent`로 severity별 finding을 수거한다.
2. **fix**: critical/high/medium finding이 있으면, finding을 **하나씩 순차** fix-task로 변환해 `spawn_agent(agent_type="implementation_agent", ...)`(model: sonnet) leaf를 재spawn하고 `wait_agent`로 수거한다(finding 영향 파일 = Target Files). `implementation_agent`는 fix mode 별도 계약 없이 finding을 task로 받아 기존 TDD 계약으로 처리한다(I3 — leaf는 단일 task 실행자라 finding이 곧 task).
3. **re-review**: fix 후 loop 범위 전체를 `implementation_review_agent`로 재리뷰한다.
4. exit 조건 충족 또는 MAX 도달까지 1~3을 반복한다. MAX 도달 시 분기 정책 적용.

Speculative Code(AC 외 옵션·설정·추상화·도달 불가 에러 처리)는 reviewer가 finding으로 분류하며, 실제 버그·보안 영향 시 Critical로 escalate된다.

phase 리포트는 필요 시 `_sdd/implementation/implementation_report_phase_<N>.md`로 저장한다(loop iteration·finding·해소 요약 포함).

#### Surface Phase Surprises

Phase Review 종료 시, 그 phase에서 발생한 다음 이벤트를 채팅으로 1-3줄 요약한다 (질문 아님). 발생 항목이 없으면 sub-step 자체를 생략한다.

- `UNPLANNED_DEPENDENCY` 자동 해결 (어느 파일이 추가 수정됐는지)
- Regression Iron Rule 발동 (어느 기존 테스트가 자동 업데이트됐는지)
- leaf failure → 순차 fallback (어느 task가 재시도했는지)

### Step 7: Final Review & Report

모든 Phase 완료 후 orchestrator가 종합 리뷰를 수행한다.

- Cross-phase 통합 검증: 모듈 간 연동, 보안 경계, 전체 규모 성능
- Critical 이슈 발견 시 leaf 재spawn으로 TDD 수정

#### implementation_report 생성 (orchestrator 소유)

저장 경로: `_sdd/implementation/<YYYY-MM-DD>_implementation_report_<slug>.md`
- `slug`는 소문자 snake_case (영문 소문자, 숫자, `_`만 사용)
- progress·report 경로·필드는 `spec-update-done`·`spec-summary` 소비와 호환되도록 canonical 형식을 유지한다.

포함 내용: 완료/미완료 task, parallel execution stats(groups·parallel·sequential·leaf failures), 테스트 결과, unplanned dependency, critical/quality follow-up, conclusion(READY/NEEDS WORK/BLOCKED).

## Autonomous Decision-Making

다음 상황에서는 사용자에게 묻지 않고 최선의 판단으로 자율 진행:

- **Target Files 불명확**: 최선의 추론 후 진행, 저확신 시 순차 fallback
- **plan 부재**: 경량 분해(경로 B)로 순차 진행, 가정을 리포트에 기록
- **모호한 요구사항**: 합리적 해석으로 진행, 가정을 리포트에 명시
- **범위 결정**: 계획 범위 내에서만 작업, 범위 밖 발견사항은 리포트에 기록
- **기술 선택**: 기존 코드베이스 패턴 준수, 판단 근거를 리포트에 기록
- **블로커**: 외부 의존성은 mock 처리, 해결 불가 항목은 리포트에 기록

## Prerequisites

1. **task-set 확보** (Step 1: plan 파싱 또는 no-plan 경량 분해)
2. **환경 로드**: `_sdd/env.md` 존재 시 setup을 orchestrator가 1회 로드해 leaf dispatch 시 전달 (leaf는 재탐색 안 함)
3. **코드베이스 이해**: Grep/Glob으로 기존 패턴, 테스트 프레임워크, 테스트 파일 위치 파악

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Role Pointer**: 이 스킬은 orchestrator다. 단일 task TDD를 수행하는 leaf는 `.codex/agents/implementation-agent.toml`(agent_type `implementation_agent`)다. 더 이상 leaf와 동일 계약을 mirror하지 않는다 (orchestrator↔leaf 관계) — 변경 시 함께 수정할 동기화 의무 없음.
