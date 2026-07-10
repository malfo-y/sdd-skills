---
name: implementation
description: "Use this skill when the user wants to execute an implementation plan, start implementing tasks from a plan, work through a development roadmap, says \"implement the plan\", \"start implementation\", \"execute the plan\", \"work on the tasks\", or explicitly asks for \"implement parallel\", \"parallel implementation\", \"병렬 구현\", \"병렬로 구현\". Uses conflict-aware parallel execution when Target Files are available."
version: 3.6.0
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# Implementation Orchestrator (Parallel Test-First)

이 스킬은 **orchestrator**다. 메인 루프에서 실행되어 fan-out이 가능하다. task-set을 확보하고(plan 파싱 또는 plan 없으면 경량 분해), `task-ordering-agent`가 파생한 wave(병렬 그룹)를 소비해(실행 직전 file-disjoint 실측 검증 후) **wave별 2-stage 파이프라인**으로 leaf를 dispatch한다: (Stage A) `test-author-agent` leaf가 테스트만 작성 → (RED 게이트) orchestrator가 실패 증거를 캡처하고 falsifiability를 점검 → (Stage B) `implementation-agent` leaf가 고정 실패 테스트를 최소코드로 통과(GREEN→REFACTOR) → (GREEN 게이트). 통합·회귀·phase review·report를 소유한다. RED는 test-author leaf + orchestrator RED 게이트가 흡수하고, GREEN→REFACTOR만 impl leaf가 수행한다 — leaf는 RED를 자체 수행하지 않는다. 병렬화는 최적화 토글일 뿐 — 불가하면 동일 흐름으로 순차 실행한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: task-set을 확보한다 — plan 파싱(있을 때) 또는 plan 없으면 요청을 task로 경량 분해
- [ ] AC2: `task-ordering-agent`가 파생한 wave 소비(wave 정보 없는 구식 plan만 자체 파생 fallback) + file-disjoint 실측 가드레일 + 순차 강등
- [ ] AC3: wave별 2-stage로 leaf를 dispatch(claude는 `sdd-skills:` prefix 필수) — Stage A는 `sdd-skills:test-author-agent`에 입력(task AC + Validation Plan `V*` + Contract/Invariant Delta + 환경/테스트)을 전달하고, RED 게이트 통과 후 Stage B는 `sdd-skills:implementation-agent`에 입력(task 필드 + Target Files + 환경/테스트 + 선행 보장 + 고정 실패 테스트 + RED 증거)을 전달
- [ ] AC4: post-group 통합·회귀·phase review를 orchestrator가 수행하고 leaf 출력(UNPLANNED_DEPENDENCY 등)을 처리
- [ ] AC5: `_sdd/implementation/<YYYY-MM-DD>_implementation_report_<slug>.md` 및 progress artifact를 canonical 경로·필드로 생성(orchestrator 소유)
- [ ] AC6: leaf 출력이 AC 외 추가 코드(옵션·설정·추상화·에러 처리)를 포함하지 않으며, 발견 시 Phase Review에서 Quality 또는 Critical로 분류 (Minimum-Code Mandate)
- [ ] AC7: 시작 전 Plan Assumptions와 Phase별 Surprises가 사용자에게 노출됐다 (해당 항목이 없으면 생략 가능)

## Hard Rules

- **Spec 파일 불가침**: `_sdd/spec/` 하위 파일을 생성/수정/삭제하지 않는다. Spec drift 발견 시 리포트에 기록하고 사용자에게 `spec-sync` 사용을 안내한다.
- **Test-first는 2-stage로 분리**: RED는 `test-author-agent` leaf(테스트 작성) + orchestrator 소유 RED 게이트(실패 증거 캡처 + falsifiability 점검)가 담당하고, GREEN→REFACTOR는 `implementation-agent` leaf가 고정 실패 테스트를 최소코드로 통과시켜 담당한다. impl leaf는 RED를 자체 수행하지 않으며 테스트를 수정하지 않는다(이의는 CONTRACT_MISMATCH로만). orchestrator는 per-task GREEN/REFACTOR 절차를 복제하지 않는다.
- **파일 경계 준수**: leaf는 할당된 Target Files만 생성/수정/삭제한다. 그 외 파일은 읽기 전용이며, leaf가 `UNPLANNED_DEPENDENCY`로 보고하면 orchestrator가 유효성을 판단해 처리한다.
- **Verification Gate**: "should work" 금지. post-group 검증에서 테스트를 실제 재실행하고 출력을 근거로 제시한다. 이전 실행 결과 재사용 금지. `_sdd/env.md` 미존재 시 코드 분석 기반 검증을 허용하되, 리포트에 `UNTESTED` 표기.
- **Regression Iron Rule**: 기존 테스트 실패 시 (1) 테스트 업데이트 + (2) 회귀 방지 테스트 추가를 사용자 확인 없이 자동 수행한다.
- **Artifact Naming Transition**: 결과 파일은 lowercase canonical 경로에 저장하고, transition 기간에는 plan/progress/report의 legacy uppercase 경로를 입력 fallback으로 허용한다.
- **Minimum-Code Mandate**: leaf와 후속 검증은 AC가 요구하는 동작만 구현·검증한다. 요청되지 않은 옵션·설정·추상화·에러 처리 추가 금지. 사변적 형용사("future-proof / extensible / configurable")는 task의 Technical Notes에 근거가 명시될 때만 허용. **REFACTOR 단계도 단일 사용처 추상화 도입은 금지한다.**
- **Subagent Model Override**: `$ARGUMENTS`에 `--model <name>`이 있으면 이 스킬의 모든 `Agent(...)` 호출(test-author·implementation·correctness/simplicity reviewer 포함)에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

### Target Files 규격

- 모든 태스크에 `**Target Files**:` 필드 필수
- 마커: `[C]` 생성, `[M]` 수정, `[D]` 삭제
- 형식: `- [마커] relative/path/to/file.ext`
- 읽기 전용 참조는 Target Files에 포함하지 않음

### 그룹 파생과 file-disjoint 가드레일

orchestrator는 **dependency를 그룹화의 권위 있는 신호로 신뢰**한다. 의미적 충돌은 `task-ordering-agent`(Step 1에서 dispatch)가 task `Dependencies` edge로 인코딩하므로(무방향 mutex도 임의 방향 dep로 흡수), orchestrator는 이를 재검출하지 않는다.

병렬 판단 규칙:

- **같은 phase + dependency edge 없음 + Target Files disjoint → 병렬 그룹**. 그 외는 순차.
- **file-disjoint 가드레일**(상시): fan-out 직전 그룹 내 task들의 Target Files가 실제로 disjoint한지 set-intersection으로 검사한다. 동일 파일이 두 task에 등장하면(마커 무관) 그 그룹을 순차로 내린다. plan staleness/dependency 누락에 대한 싸구려 안전망.
- **확신 없으면 순차**: dependency 정보가 빈약·부재하면(구식 plan 등) 순차로 기본 fallback한다. 덜 병렬화될 뿐 오작동하지 않는다.

> 파일 충돌 매트릭스 — 동일 파일이 두 task의 Target Files에 등장하면 마커 무관하게 충돌(`[C]+[C]` 동시 생성, `[M]+[M]` 동시 수정, `[C]+[M]`·`[M]+[D]`·`[C]+[D]` 순서 의존, `[D]+[D]` 중복 삭제). file-disjoint 가드레일이 이 매트릭스를 적용한다.

## Process

### Step 1: Secure the Ordered Task-Set

implementation은 상위 orchestrator가 없는 **사용자 직접 실행 전용** 진입점이다 — autopilot 등 상위 orchestrator는 implementation SKILL을 경유하지 않고 자체 dispatch-controller로 실행하며 ordering도 스스로 소유한다. 따라서 implementation은 Phase Source를 hand-off 받는 경로가 없고, task-set 확보 후 dependency·phase가 아직 없으면 **항상 `task-ordering-agent`를 dispatch해 ordering을 파생**한다(ordering은 정확히 1회).

**1a. 입력 확보.** 탐색 순서:
1. 사용자 지정 경로
2. `_sdd/implementation/*_implementation_plan_*.md` (이미 ordering된 plan — 재개/직접 제공, slug 기반 glob)
3. legacy fallback: `_sdd/implementation/implementation_plan.md`, `_sdd/implementation/implementation_plan_phase_<n>.md`, uppercase `IMPLEMENTATION_PLAN.md`·`IMPLEMENTATION_PLAN_PHASE_<N>.md`
4. `_sdd/drafts/*_feature_draft_*.md` (slug 기반 glob, Part 2: **flat task-set** — dependency·phase 없음)
5. `_sdd/drafts/feature_draft_<name>.md` (legacy 고정 경로)
6. 입력 없음 → 사용자 요청을 flat task-set으로 **경량 분해**(각 조각에 Target Files를 best-effort 부여)

> 경량 분해는 **소규모·순차 실행**용 fallback이다(순차라 얕은 task 정의도 안전 — file 충돌이 없으므로). 대규모거나 병렬 최적화가 중요한 요청이면 경량 분해로 강행하지 말고 `feature-draft`(제대로 된 flat task-set 생성) 또는 `sdd-autopilot`(feature-draft→task-ordering→implementation 전체 조율)을 사용하도록 안내한다.

복수 파일 존재 시 사용자에게 확인.

**1b. Ordering (항상 경유).**
- 입력이 **flat task-set**(feature-draft Part 2 또는 경량 분해 결과 — dependency·phase 미포함)이면 `Agent(subagent_type="sdd-skills:task-ordering-agent", prompt=<flat task-set 경로 + 요청>)`를 dispatch해 ordered plan(`_sdd/implementation/<YYYY-MM-DD>_implementation_plan_<slug>.md`: dependency edge·phase·Checkpoint 포함)을 받는다.
- 입력이 이미 **ordered plan**(dependency·phase를 담은 implementation_plan — 재개/직접 제공)이면 task-ordering을 생략하고 그대로 파싱한다.
- `task-ordering-agent`가 `BLOCKED`를 반환하면(task 정의만으로 dependency 복원 불가) 사용자에게 보고하고 중단한다.

ordered plan에서 추출: Phases, Tasks (Target Files·Dependencies 포함), top-level Open Questions. feature draft 유래 task-set에서는 `Components`를 요구하지 않는다. Open Questions는 최선의 판단으로 해결하고, 판단 불가 항목은 리포트에 기록.

> 구 "경로 B — no-plan 경량 분해"는 1a-6 + 1b(task-ordering dispatch)로 정식 승격됐다 — 분해 결과도 task-ordering을 거쳐 dependency·phase를 갖춘다. 모든 경로가 ordered plan을 거쳐 동일한 후속 흐름(Step 2~7)을 탄다.

#### Surface Plan Assumptions

task-set 확보 직후, 사용자에게 다음을 채팅으로 알림한다 (질문 아님 — redirect는 사용자가 다음 turn에 지시):

- Plan top-level `Open Questions` 또는 `Risks/Mitigations and Open Questions` 중 Confidence=LOW 또는 User confirmation needed=Yes 항목 (4-필드 스키마를 따르지 않는 plan은 Open Q 항목을 보수적으로 모두 노출)
- 본 실행에 적용될 Autonomous Decision-Making 카테고리 예고 (해당 항목이 있는 경우)

항목당 1줄: `[Qn] <Decision taken 요약> (출처/근거)`. 해당 항목이 없으면 "사용자 확인이 필요한 항목 없음" 한 줄로 마친다.

### Step 2: Initialize Task Tracking

각 태스크를 TaskCreate로 등록하고, blockedBy 관계를 TaskUpdate로 설정한다.
동시에 `_sdd/implementation/<YYYY-MM-DD>_implementation_progress_<slug>.md`에 tracking row를 기록한다:
- task_id, title, phase, dependencies, status, owner/leaf, notes
- 초기 상태는 dependency 존재 시 `BLOCKED`, 없으면 `READY`

Plan ID → System Task ID 매핑과 progress row 매핑을 함께 유지한다. 이 progress artifact는 orchestrator가 소유하며, 경로·필드는 downstream(`spec-sync`·`spec-summary`)이 소비하므로 canonical 형식을 보존한다.

### Step 3: Derive Parallel Groups

#### 3.1 Target Files 가용성 판단

| 상황 | 처리 |
|------|------|
| 모든 태스크에 Target Files 있음 | 전체 그룹 파생 |
| 일부만 있음 | 있는 태스크만 병렬 후보, 나머지 순차 |
| 없음 | 추론 시도 → 저확신 시 순차 fallback |

#### 3.2 wave 소비 (+ fallback)

wave(병렬 그룹) 파생은 `task-ordering-agent`가 각 phase 내에서 이미 수행해 `Parallel Execution Summary`에 명시했다(`priority DESC, id ASC` 정렬 greedy, dependency 없음 + Target Files disjoint → 같은 wave, 대규모 phase는 크기 5 제한). orchestrator는 그 wave를 **그대로 소비**한다.

> wave 정보가 없는 구식 plan(재개 등)에서만 fallback으로 자체 파생한다: unblocked task를 `priority DESC, id ASC`로 정렬해 dependency 없음 + Target Files disjoint 기준으로 greedy하게 wave에 담는다.

#### 3.3 병렬 실행 계획 표시

실행 전 사용자에게 그룹 구성과 예상 효율을 보여준다.

### Step 4: Fan-out by Phase (wave별 2-stage 파이프라인)

각 phase의 wave(group)는 **2-stage 파이프라인**을 탄다: Stage A(test-author 병렬) → RED 게이트 → Stage B(impl 병렬) → GREEN 게이트. **wave 간은 순차**다 — wave G의 Stage B(impl)와 wave H의 Stage A(테스트 작성)를 동시에 돌리는 **cross-wave 중첩은 도입하지 않는다**(C4 — prose orchestration에 스케줄러 복잡도만 키우는 speculative 최적화, YAGNI). 파이프라인은 wave **내부**에만 적용하고, wave끼리는 한 wave가 GREEN 게이트를 닫은 뒤 다음 wave를 시작한다.

```
For each phase:
  1. Unblocked 태스크에서 wave(group) 파생 (Step 3)
  2. For each wave (순차 — 이전 wave의 GREEN 게이트 통과 후 다음 wave 시작):
     Stage A: wave 내 task마다 sdd-skills:test-author-agent leaf를 동시 dispatch (테스트만)
              → 전원 완료 대기
     RED 게이트 (orchestrator 소유): 새 테스트 실행→실패 확인→RED 증거 캡처 + falsifiability 점검
              → 미충족 task는 test-author 재dispatch (RED 게이트 통과 전 Stage B 미dispatch)
     Stage B: wave 내 task마다 sdd-skills:implementation-agent leaf를 동시 dispatch
              (입력에 고정 실패 테스트 + RED 증거 포함) → 전원 완료 대기
     GREEN 게이트: 테스트 실행→통과 확인→GREEN 증거 캡처 (Post-group 통합·회귀, Step 5)
              → CONTRACT_MISMATCH / Unplanned Dependency 처리
  3. 전체 wave 완료 → Phase Review (Step 6)
```

#### Stage A — test-author Dispatch (테스트만)

wave 내 task마다 test-author leaf를 dispatch한다 (병렬 시 한 메시지에서 동시 호출):

- **claude**: `Agent(subagent_type="sdd-skills:test-author-agent", prompt=<입력>)` — `sdd-skills:` prefix 필수(bare name 금지).
- **codex**: `spawn_agent(agent_type="test-author-agent", prompt=<입력>)` 후 `wait_agent`로 수거

test-author 입력(프롬프트)에 다음을 전달한다 (leaf는 재탐색하지 않음):

```
## Task {id}: {title}
- Acceptance Criteria  # 테스트가 검증할 관찰 동작의 원천

## Validation Plan (V*)
{validation_plan}      # 각 테스트가 1:1 대응

## Contract/Invariant Delta
{contract_invariant_delta}   # 테스트가 실행할 인터페이스 계약 (발명 금지)

## 환경/테스트 (orchestrator가 로드해 전달)
{test_command}
{env_setup}            # _sdd/env.md에서 orchestrator가 1회 로드

## Target Files (참조)
{target_files_list}    # 테스트가 호출할 인터페이스 추론용 (테스트 파일 경로는 leaf가 관습 탐색)
```

test-author는 각 AC의 관찰 동작을 검증하는 실패(RED) 테스트만 작성하고, 가정한 인터페이스 계약 + RED 근거를 반환한다.

#### RED 게이트 (orchestrator 소유)

Stage A 완료 후, orchestrator가 다음을 수행한다. **이 게이트가 falsifiable test-first 불변식(I1)의 집행 지점이다** — RED 증거는 leaf 자기보고 TDD표가 아니라 orchestrator가 캡처한 외부 산출물이다.

1. **새 테스트 실행 → 실패 확인**: test-author가 작성한 테스트를 실제 실행해 현재 빨간지 확인한다.
2. **RED 증거 캡처**: 실패 출력(메시지·스택·실패 단계)을 캡처해 보존한다. 이 증거가 Stage B impl 입력으로 그대로 전달된다.
3. **falsifiability 점검** — 각 테스트가 (a) 해당 task AC의 **관찰 동작**을 검증하는지, (b) Validation Plan `V*`에 **1:1 대응**하는지, (c) **단순 import/collection 에러로만 빨간 게 아닌지**를 점검한다. 아래 판정 규칙으로 못박는다:
   - **관찰 가능한 판정 규칙**: 각 테스트의 실패가 **AC 관찰 동작에 대한 assertion/check 단계 실패**(예: `AssertionError` 계열 — 동작은 실행됐으나 기대값 불일치)여야 RED 통과로 인정한다. **순수 collection/import/syntax 단계 실패**(예: `ImportError`·`ModuleNotFoundError`·collection error·syntax error — 동작에 도달조차 못함)로만 빨간 테스트는 RED 미충족으로 분류해 **test-author 재작성으로 돌린다**(통과 전 Stage B 미dispatch).
   - **실패 단계 기록**: 각 테스트가 **어느 단계에서 실패했는지**(assertion 단계 vs collection/import/syntax 단계)를 RED 증거에 기록한다.
   - **구분 불가 시 강등**: 해당 언어/프레임워크가 collection 에러와 assertion 실패를 출력상 구분하지 못하면 그 사실을 RED 증거에 기록하고 falsifiability 점검을 **리뷰 판정으로 강등**한다(자동 판정 대신 orchestrator가 테스트 본문을 읽어 관찰 동작 검증 여부를 판단).
   - **graceful degradation (I4)**: 테스트 프레임워크 부재 자산(문서·스킬 등)은 grep/구조 점검 acceptance check를 RED artifact로 쓰고, 그 acceptance check의 **현재 미충족**을 **명령 exit code(비0) 또는 diff(기대 부재)**로 RED 캡처한다. 프레임워크/`_sdd/env.md` 부재로 실행 자체가 불가하면 코드/구조 분석 기반 점검을 허용하되 RED 증거에 `UNTESTED` + 사유를 표기한다. **이 RED 게이트 서술이 I4 graceful-degradation 분기 기준의 canonical surface다** — 다른 surface(test-author-agent AC 등)는 이를 참조한다.
4. **게이트 통과 전 Stage B 미dispatch**: RED 게이트(실패 확인 + falsifiability 통과)를 닫기 전에는 Stage B impl을 dispatch하지 않는다(C5, I1). 미충족 task는 test-author 재dispatch로 돌리고, 통과한 task만 Stage B로 넘긴다.

#### Stage B — impl Dispatch (GREEN→REFACTOR)

RED 게이트를 통과한 task마다 impl leaf를 dispatch한다 (병렬 시 한 메시지에서 동시 호출):

- **claude**: `Agent(subagent_type="sdd-skills:implementation-agent", prompt=<입력>)` — `sdd-skills:` prefix 필수(bare name 금지).
- **codex**: `spawn_agent(agent_type="implementation-agent", prompt=<입력>)` 후 `wait_agent`로 수거

impl 입력(프롬프트)에 다음을 전달한다 (leaf는 재탐색하지 않음):

```
## Task {id}: {title}
- Priority / Description / Acceptance Criteria / Technical Notes / Component(if present)

## Target Files (쓰기 허용 경계)
{target_files_list}

## 환경/테스트 (orchestrator가 로드해 전달)
{test_command}
{env_setup}

## 선행 보장
이 task의 dependency는 완료됨. 그 산출물은 read-only 참조 가능.

## 고정 실패 테스트 + RED 증거
{fixed_test_paths}     # Stage A가 작성한 실패 테스트 파일 경로 (impl에 대해 고정 — 수정 금지)
{red_evidence}         # RED 게이트가 캡처한 실패 출력
```

impl leaf는 고정 실패 테스트를 최소코드로 통과(GREEN→REFACTOR)시키고 구조화된 결과(SUCCESS/PARTIAL/FAILED/BLOCKED·GREEN 진행표·파일·테스트·UNPLANNED_DEPENDENCY·CONTRACT_MISMATCH·발견)를 반환한다. **고정 테스트의 가정 계약이 틀렸다/구현 불가**라고 보면 테스트를 수정하지 않고 `CONTRACT_MISMATCH`로 보고하며, **orchestrator가 test-author 재dispatch 여부를 판정한다**(C3 — 기존 UNPLANNED_DEPENDENCY 처리와 동결: 계약 오류면 test-author 재dispatch, Target Files 밖 의존이면 경계 확장).

#### GREEN 게이트

Stage B 완료 후 테스트를 실제 실행해 **통과(GREEN)** 를 확인하고 GREEN 증거(통과 출력)를 캡처한다. 이어 Step 5 post-group 통합·회귀 스윕을 수행한다(기존 흐름 유지).

#### Sequential Fallback

병렬 불가(파일 충돌·dependency·Target Files 부재·no-plan 저확신)면 동일 2-stage 흐름을 task별로 하나씩 순차 dispatch한다(task당 test-author → RED 게이트 → impl → GREEN). 흐름은 동일하고 병렬성만 빠진다.

### Step 5: Integrate & Verify (Post-Group)

각 그룹 완료 후 orchestrator가 수행한다:

| 단계 | 내용 |
|------|------|
| 전체 테스트 | 새 테스트 + 기존 테스트 실행, 회귀 확인 (GREEN 게이트의 후속) |
| Unplanned Dependency | leaf 보고 수집 → 유효성 판단 → 해결 → 재검증 |
| CONTRACT_MISMATCH | Stage B impl 보고 수집 → 가정 계약 오류면 test-author 재dispatch(테스트 재작성 후 RED 게이트 재실행), Target Files 밖 의존이면 UNPLANNED_DEPENDENCY로 처리 |
| leaf 실패 | 다른 leaf에 영향 없음. 실패 태스크는 순차 재시도, 2회 실패 시 사용자 보고 |
| 파일 경계 위반 | 미승인 변경 롤백 → 순차 재실행 |
| 태스크 상태 | 성공 → completed, 실패 → in_progress (재시도용), 부분 → 미완료 기준 기록 |

### Step 6: Phase Review-Fix Gate (외부 reviewer loop)

Phase 내 모든 태스크 완료 후, orchestrator는 **외부 2-reviewer review→fix→re-review loop**를 닫는다. 각 review/re-review 단계는 correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`)를 **병렬 dispatch**한다. 이 gate는 인라인 경량 self-review를 대체한다 — orchestrator가 직접 품질을 판정하지 않고 독립 reviewer agent를 호출한다.

**loop scope**: **실행분(phase) 단위 1 gate**. 각 phase 완료 직후 이 gate를 1회 닫고 다음 phase로 진행한다. autopilot의 global/per-group·Checkpoint 메타 개념은 도입하지 않는다(직접 호출 경로엔 Checkpoint 신호를 줄 상위 오케스트레이터가 없음). multi-phase plan이면 phase마다 이 gate가 1회씩 닫힌다.

**공통 loop 정책** (autopilot `references/orchestrator-contract.md` §6 Review-Fix Contract 차용):

- **exit 조건**: **두 report 합집합** `critical=0 AND high=0 AND medium=0` (= `critical=high=medium=0`). correctness·simplicity 두 리포트의 finding을 합산해 판정한다.
- **MAX**: 기본 3 iteration.
- **re-review scope**: loop 범위(이 phase) **전체 재리뷰** (변경분만 아님).
- **1 iteration 경계**: `review/re-review → finding>0이면 fix → 산출물 갱신`.
- **MAX 도달 분기**: critical/high 잔존 → 중단·사용자 보고. medium만 잔존 → 로그 후 진행(advisory degrade).

**단계**:

1. **review**: 한 메시지에서 두 reviewer를 **병렬 dispatch**한다 — `Agent(subagent_type="sdd-skills:implementation-review-agent")`(correctness)와 `Agent(subagent_type="sdd-skills:simplicity-review-agent")`(simplicity)에 각각 이 phase 범위의 변경 파일 전체 + 테스트 결과를 전달한다. 두 reviewer가 각자 severity별 finding을 반환한다.
2. **fix**: 두 report의 critical/high/medium finding을 **합산**해, finding이 있으면 **하나씩 순차** fix-task로 변환한다. finding 종류에 따라 경로가 갈린다(C6 — 모든 finding을 파이프라인 태우지 않음):
   - **correctness finding(동작 버그)**: test-first로 처리한다 — 먼저 그 버그를 노출하는 **실패 테스트**를 작성(`sdd-skills:test-author-agent` dispatch + RED 게이트로 실패 확인)한 뒤, 고정 실패 테스트 + RED 증거를 입력으로 `sdd-skills:implementation-agent` leaf를 재dispatch해 fix한다.
   - **simplicity/refactor finding**: 직접 fix한다 — 새 실패 테스트 없이 finding을 task로 받아 `sdd-skills:implementation-agent` leaf를 재dispatch한다(중복 제거·명확성·speculative code 제거는 새 동작이 아니라 새 테스트가 불필요).
   - finding 영향 파일 = 그 leaf의 Target Files. impl-agent는 fix mode 별도 계약 없이 finding을 task로 받아 기존 GREEN→REFACTOR 계약으로 순차 처리한다(I3 — leaf는 단일 task 실행자라 finding이 곧 task).
3. **re-review**: fix 후 loop 범위 전체를 두 reviewer(`implementation-review-agent` ∥ `simplicity-review-agent`)로 **병렬 재리뷰**한다. dispatch message에 각 reviewer의 **기존 리포트 경로**를 포함해 re-review mode로 진입시킨다 — 각 reviewer는 새 리포트를 만들지 않고 자기 기존 리포트의 `Current Status`를 갱신하고 `Iteration History`에 이번 회차(resolved/still-open/new)를 append한다.
4. exit 조건(두 report 합집합 `critical=high=medium=0`) 충족 또는 MAX 도달까지 1~3을 반복한다. MAX 도달 시 분기 정책 적용.

Speculative Code(AC 외 옵션·설정·추상화·도달 불가 에러 처리)는 simplicity reviewer(`simplicity-review-agent`)가 finding으로 분류하며, 실제 버그·보안 영향 시 correctness reviewer가 Critical로 escalate한다.

Phase 리포트는 필요 시 `_sdd/implementation/implementation_report_phase_<N>.md`로 저장한다(loop iteration·finding·해소 요약 포함).

#### Surface Phase Surprises

Phase Review 종료 시, 그 phase에서 발생한 다음 이벤트를 채팅으로 1-3줄 요약 (질문 아님). 발생 항목이 없으면 sub-step 자체 생략:

- UNPLANNED_DEPENDENCY 자동 해결 (어느 파일이 추가 수정됐는지)
- Regression Iron Rule 발동 (어느 기존 테스트가 자동 업데이트됐는지)
- leaf failure → 순차 fallback (어느 task가 재시도했는지)

### Step 7: Final Cross-Phase Review-Fix Gate & Report

모든 Phase 완료 후, orchestrator는 **cross-phase 범위로 외부 2-reviewer review→fix→re-review loop를 1회 닫는다**. Step 6과 동일하게 각 review/re-review 단계는 correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`)를 병렬 dispatch하며, orchestrator가 직접 품질을 판정하지 않고 독립 reviewer agent를 호출한다.

- **single-phase 가드**: phase가 1개뿐이면 Step 6 gate가 이미 전체 구현분을 동일 범위로 리뷰했으므로 이 gate를 **스킵하고 곧장 report 생성으로 진행**한다(중복 회피). multi-phase plan일 때만 이 gate를 닫는다.
- **loop scope**: 전체 구현분(all phases). phase별 gate에서 phase-local 품질은 이미 닫혔으므로, 이 gate는 **phase 경계를 넘는 이슈**(모듈 간 연동, 보안 경계, 전체 규모 성능, cross-phase 통합 일관성)에 초점을 둔다.
- **loop 정책**: Step 6의 공통 loop 정책을 그대로 재사용한다 (exit는 **두 report 합집합** `critical=high=medium=0`, MAX 3 iteration, re-review는 loop 범위 전체 재리뷰, MAX 도달 분기 동일).
- **단계**: Step 6의 review→fix→re-review와 동일. review는 `Agent(subagent_type="sdd-skills:implementation-review-agent")`(correctness) ∥ `Agent(subagent_type="sdd-skills:simplicity-review-agent")`(simplicity)를 병렬 dispatch해 전체 변경 파일 + cross-phase 통합 관점 + 최종 테스트 결과를 전달하고, 두 report finding을 합산해 finding은 하나씩 fix-task로 처리한다 — Step 6과 동일한 fix 정책(correctness finding=test-first[test-author + RED 게이트 → impl], simplicity/refactor finding=직접 fix)을 그대로 재사용한다.

#### implementation_report 생성 (orchestrator 소유)

저장 경로: `_sdd/implementation/<YYYY-MM-DD>_implementation_report_<slug>.md`
- `slug`는 소문자 snake_case (영문 소문자, 숫자, `_`만 사용)
- progress·report 경로·필드는 `spec-sync`·`spec-summary` 소비와 호환되도록 canonical 형식을 유지한다.

```markdown
## Implementation Report (Parallel Execution)

### Progress Summary
- Total Tasks: X | Completed: X | Tests Added: X | All Passing: Yes/No

### Parallel Execution Stats
- Groups Dispatched: X | Parallel Tasks: X | Sequential Fallbacks: X
- Leaf Failures: X (retried: Y, resolved: Z)

### Completed Tasks
- [x] Task 1: ... (N tests) [parallel: group 1]

### Review Gates
<!-- gate당 한 줄: iteration 수 + exit 충족(합집합 critical=high=medium=0) 또는 MAX 도달 + 두 reviewer 리포트 경로. cross-phase 이슈는 final gate 줄에 요약 -->
- Phase N gate: exit 충족 (iteration K) — reports: `<correctness>`, `<simplicity>`
- Final cross-phase gate: exit 충족 (iteration K) | 스킵 (single-phase — Step 6이 전체 범위 커버)

### Open Issues
<!-- review-fix loop 후 잔존분만: MAX 도달 잔존 medium, Low advisory, 범위 밖 발견. 항목당 reviewer 리포트 finding ID 참조 + 위치 포함 한 문장. 없으면 "없음." -->
- M2 (correctness report): `file:line` — <잔존 사유와 권고 한 문장>

### Recommendations
<!-- Open Issues 재진술 금지 — finding ID 참조로 갈음. finding에 대응되지 않는 신규 권고만 본문 1줄 (사변적 권고 금지) -->

### Conclusion
[READY / NEEDS WORK / BLOCKED] — <한 문장 근거>
```

## Autonomous Decision-Making

다음 상황에서는 사용자에게 묻지 않고 최선의 판단으로 자율 진행:

- **Target Files 불명확**: 최선의 추론 후 진행, 저확신 시 순차 fallback
- **plan 부재**: flat task-set으로 경량 분해 후 `task-ordering-agent`로 ordering 파생, 저확신 dependency는 순차 fallback, 가정을 리포트에 기록
- **모호한 요구사항**: 합리적 해석으로 진행, 가정을 리포트에 명시
- **범위 결정**: 계획 범위 내에서만 작업, 범위 밖 발견사항은 리포트에 기록
- **기술 선택**: 기존 코드베이스 패턴 준수, 판단 근거를 리포트에 기록
- **블로커**: 외부 의존성은 mock 처리, 해결 불가 항목은 리포트에 기록

## Prerequisites

1. **ordered task-set 확보** (Step 1: ordered plan 파싱, 또는 flat task-set → `task-ordering-agent` dispatch로 ordering 파생)
2. **환경 로드**: `_sdd/env.md` 존재 시 setup을 orchestrator가 1회 로드해 leaf dispatch 시 전달 (leaf는 재탐색 안 함)
3. **코드베이스 이해**: Grep/Glob으로 기존 패턴, 테스트 프레임워크, 테스트 파일 위치 파악

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Role Pointer**: 이 스킬은 orchestrator다. leaf는 둘이다 — `.claude/agents/test-author-agent.md`(테스트만 작성, RED)와 `.claude/agents/implementation-agent.md`(고정 실패 테스트를 GREEN→REFACTOR). RED 게이트(실패 증거 캡처 + falsifiability 점검)·fan-out·통합·report는 orchestrator가 소유한다. 더 이상 leaf와 동일 계약을 mirror하지 않는다 (orchestrator↔leaf 관계) — 변경 시 함께 수정할 동기화 의무 없음.
