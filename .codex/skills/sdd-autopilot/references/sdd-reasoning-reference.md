# SDD Reasoning Reference

## Part 1: SDD 철학

### 1.1 핵심 원칙

1. **Spec is Source of Truth**: 코드는 결과물이고, global spec은 장기적 의도를 고정한다.
2. **Global spec과 temporary spec은 역할이 다르다**: global spec은 얇은 repo-wide 판단 기준이고, temporary spec은 실행 청사진이다.
3. **검증은 실행 surface에 더 가깝게 둔다**: feature-level contract와 validation은 temporary spec, code, review evidence에 가깝게 둔다.

운영 대원칙: **AI가 만든 spec도 사람 승인 없이는 확정하지 않는다.**

### 1.2 사람과 LLM이 spec에서 필요로 하는 것

- 사람은 high-level concept, scope, non-goals, guardrails, key decisions가 먼저 필요하다.
- LLM은 코드를 빠르게 탐색할 수 있으므로 code-obvious inventory보다 경계와 결정이 더 중요하다.
- 따라서 global spec은 두꺼운 구현 해설서가 아니라 얇은 decision memo여야 한다.
- 사람이 repo 전체를 빠르게 설명 가능하게 이해해야 할 때는 `spec-summary`가 `_sdd/spec/summary.md`에 문제, 동기, 설계, 코드 근거, 사용/기대 결과를 묶는 reader-facing whitepaper surface를 담당한다.
- 상세 implementation inventory와 feature-level execution detail은 코드, temporary spec, guide, supporting docs에 맡긴다.

### 1.3 핵심 용어

| 용어 | 의미 |
|------|------|
| **Global Spec** | 장기적 SoT. 문제 framing, scope/non-goals/guardrails, key decisions를 유지하는 문서 |
| **Temporary Spec** | 변경 하나를 실행하기 위한 청사진. delta, touchpoints, plan, validation을 담는 문서 |
| **Repo-wide Invariant** | 여러 feature에 공통으로 적용되고, 틀리면 repo-level 판단이 어긋나는 operating rule |
| **Guide** | 필요할 때 만드는 feature-level companion surface |
| **Supporting Reference** | README, 환경 문서, appendix, code map 같은 보조 정보 |

### 1.4 Global Spec Canonical Shape

global spec core는 아래 순서를 유지한다.

1. `배경 및 high-level concept`
2. `Scope / Non-goals / Guardrails`
3. `핵심 설계와 주요 결정`

선택 정보:

- supporting reference
- guide 링크
- appendix-level code map
- repo-wide invariant note

global spec 규칙:

- scope는 책임 범위와 out-of-scope를 함께 고정한다.
- repo-wide invariant가 필요하면 guardrails 또는 key decisions에 흡수한다.
- usage guide, expected result, feature-level contract/validation은 기본 global core가 아니다.
- architecture/component inventory를 본문 필수로 강제하지 않는다.

### 1.5 Feature Draft Canonical Shape

feature draft는 global spec의 축약 복사본이 아니다. 변경 작업을 위한 spec delta와 실행 청사진이다.

canonical shape:

1. `Part 1: Spec Delta`
2. `Part 2: Implementation and Validation Plan`
3. `Risks/Mitigations and Open Questions`

핵심 규칙:

- `Part 1: Spec Delta`는 `<!-- spec-update-todo-input-start -->` / `<!-- spec-update-todo-input-end -->` 마커를 포함하고, 필수 섹션은 `Change Summary`, `Scope Delta`, `Persistent Spec Implications`뿐이다.
- `Persistent Spec Implications`는 persistent spec에 남아야 하는 repo-wide contract/invariant/validation 의도 후보를 compact하게 적는다. feature-level table, 상세 ID linkage, task plan, validation execution detail은 Part 1에 요구하지 않는다.
- `Part 2: Implementation and Validation Plan`은 execution-facing 섹션을 둔다: `Contract/Invariant Delta and Coverage`, `Touchpoints`, `Implementation Phases`, `Task Details`, `Validation Plan`, `Parallel Execution Summary`.
- Part 2의 `Contract/Invariant Delta and Coverage`는 `C*`, `I*`, `V*` ID와 task/validation coverage를 보존한다.
- `Risks/Mitigations and Open Questions`는 top-level 섹션이며, `Risks and Mitigations`는 `Risk / Impact / Mitigation` 표를 따르고 `Open Questions`는 Decision / Alternatives / Confidence / User confirmation needed 스키마를 따른다.
- feature draft의 실행 정보는 global spec에 그대로 병합하지 않는다.

### 1.6 spec-sync의 역할

- `spec-sync`: 같은 진입점이 evidence 차이로 동작을 적응한다. 구현 전 호출(조건부)은 feature draft `Part 1: Spec Delta`나 user input을 읽고 global spec에 남아야 할 planned persistent information만 올린다. 구현 후 호출은 실제 구현과 validation evidence를 읽고 global spec에 남아야 할 implemented persistent information만 올린다. 따라서 동일 `spec-sync`가 구현 전/후 최대 2회 호출될 수 있다.

즉:

- temporary spec의 task breakdown, validation 실행 메모, transient risk log는 global spec 본문으로 가지 않는다.
- global spec으로 올라가는 것은 shared scope, guardrails, key decisions, repo-wide invariant note 같은 정보다.

### 1.7 파이프라인 구성 원칙

1. **Spec-optional**: global spec이 있으면 활용하고, 없으면 spec-less 모드로 진행한다. `spec-create`는 파이프라인 필수 선행이 아니라 사용자에게 추천하는 가이드 수준이다.
2. **Delta-first for non-trivial changes**: `feature-draft`는 기본 포함이다. 정말 간단한 디버깅 수준의 수정(typo fix, config 값 변경, 로그 한 줄 추가 등)이거나 해당 주제의 feature-draft artifact가 `_sdd/drafts/`에 이미 존재하는 경우에만 스킵할 수 있다.
3. **Review-fix 필수**: review만 하고 끝나지 않는다.
4. **Execute -> Verify**: 에이전트 호출 != 완료. evidence까지 확인해야 한다.
5. **파일 기반 handoff**: 상태 전달은 artifact 파일 경로 중심.
6. **Global spec 직접 수정 금지**: spec 변경은 `spec-sync`에 위임.

---

## Part 2: 스킬 카탈로그

### 2.1 스킬 의존성 그래프

```text
[Optional bootstrap]
(spec-create)

[Default planning path for non-trivial changes]
feature-draft
  -> plan-review [producer gate]
  -> (optional) spec-sync [planned]
  -> (required if multi-phase) implementation-plan
  -> plan-review [producer gate if implementation-plan ran]
  -> implementation

[Immediate gate after each implementation unit]
implementation
  -> implementation-review
  -> (if needed) implementation [fix]
  -> implementation-review [re-review]
  -> validation / phase validation

[Final gate before spec sync]
(if required by per-group final integration review adaptive policy) final integration review
  -> required validation/test closure
  -> spec-sync [post-implementation]

[Optional long-running validation]
validation / final integration review
  -> ralph-loop-init
```

- 그래프는 "항상 이 순서로 모두 지난다"는 뜻이 아니다. `optional` 표시는 조건부 삽입 단계다.
- `implementation-review`는 `implementation` 다음의 별도 downstream step이 아니라, 각 `implementation` 실행 단위 직후 즉시 닫는 gate다.
- `plan-review`는 planning producer output gate다. `feature-draft` output은 `spec-sync`, `implementation-plan`, `implementation` 어느 downstream step으로 소비되기 전에도 먼저 `plan-review`를 통과해야 한다.
- `implementation-plan`을 실행한 경우 그 output도 `implementation`이 소비하기 전에 `plan-review`를 통과해야 한다.
- producer gate가 fail이면 finding을 implementation fix task로 normalize하지 않는다. 해당 producer 산출물을 reject/regenerate한다.
- `spec-sync`의 post-implementation 호출은 review-fix gate, required validation/test, 필요한 경우 `final integration review`가 모두 끝난 뒤에만 온다.
- `ralph-loop-init`은 구현 본선 뒤에 무조건 붙는 단계가 아니라, 장시간 검증이 필요할 때 validation surface에 붙는 선택지다.
- Step 4 orchestrator generation은 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`만 materialize한다. `_sdd/drafts/*`, `_sdd/implementation/*`, `_sdd/pipeline/report_*`, 코드/테스트 출력은 future step의 planned output으로만 존재한다.
- review-fix loop에서 agent 역할은 고정이다: review는 correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`) 2-reviewer 병렬, fix는 `implementation-agent` 단일 재호출, re-review도 다시 correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`) 2-reviewer 병렬이다. gate exit는 두 report의 합집합 `critical=high=medium=0`이다. 이 loop는 파이프라인 끝의 후처리가 아니라 각 `implementation` 실행 단위 직후 즉시 닫는 completion gate다.
- review가 포함된 small/medium/large 모든 규모에서 `implementation-agent`와 review 2-reviewer(`implementation-review-agent` ∥ `simplicity-review-agent`)는 sub-agent mapping으로만 실행한다. 부모 autopilot이 local implementation/review로 대체하지 않는다.
`spec-review`는 파이프라인 끝이나 중간의 감사 단계로 선택적으로 추가한다.
`spec-sync`의 post-implementation 호출은 global spec이 없으면 수행하지 않는다.
`spec-summary`와 `spec-rewrite`는 비오케스트레이션 보조 스킬이다.

### 2.1.1 Planning precedence by scale

- **Small direct path**: 바로 `implementation`으로 간다. 정말 간단한 디버깅 수준의 수정(typo fix, config 값 변경, 로그 한 줄 추가 등)이거나 해당 주제의 feature-draft artifact가 `_sdd/drafts/`에 이미 존재하는 경우에만 `feature-draft`를 생략할 수 있다. review가 포함되면 규모와 무관하게 `implementation-agent -> (implementation-review-agent ∥ simplicity-review-agent) -> implementation-agent -> (implementation-review-agent ∥ simplicity-review-agent)` custom-agent mapping을 사용하고(review/re-review는 correctness ∥ simplicity 2-reviewer 병렬, exit는 두 report 합집합), 부모 autopilot이 로컬 구현/로컬 리뷰로 대체하지 않는다.
- **Single-phase medium path**: 기본 진입은 `feature-draft`다. Part 2가 task/dependency/validation 측면에서 충분히 명확하면 `implementation-plan` 없이 `implementation`으로 바로 연결한다. 이 경우에도 해당 `implementation` 직후 global review-fix gate를 즉시 닫아야 하며, 그 전에는 downstream step으로 진행할 수 없다. review가 있으면 실행 주체는 항상 `implementation-agent`/review 2-reviewer(`implementation-review-agent` ∥ `simplicity-review-agent`) custom-agent mapping이고, gate exit는 두 report의 합집합이다.
- **Multi-phase medium / large expanded path**: `feature-draft`로 slim Part 1과 execution-facing Part 2를 고정한 뒤, planned persistent global alignment가 필요할 때만 `spec-sync`(planned 호출)를 조건부로 추가하고, multi-phase 실행으로 판단되면 `implementation-plan`을 반드시 포함한다. feature-draft -> implementation 직행은 single-phase 경로에 한정한다. 이 path에서 downstream `implementation` step은 flat single-shot step이 아니라 `Execution Mode: phase-iterative`와 `Phase Source`를 선언하는 runtime control-flow unit이어야 하며, phase count와 boundary는 Step 4가 아니라 runtime에 plan output을 읽어 해석한다.
- **Group-gated execution rule**: medium 이상에서 multi-phase plan이 생성되면 `Review-Fix Loop.scope = per-group`을 기본값으로 본다. `Phase Source`의 `Checkpoint` 필드가 group boundary를 결정하며, Checkpoint phase 직후 같은 group 범위의 review-fix gate와 validation을 닫는다. 그룹 2개 이상이면 마지막 group gate 후 cross-group regression 전용 `final integration review`를 1회 더 수행한다.
- **Spec sync ordering rule**: `spec-sync`의 post-implementation 호출은 모든 required implementation-scoped review-fix gate, required validation/test, 필요한 경우 `final integration review`가 끝난 뒤 최종 단계에서만 수행한다.
- **Carry-over default**: `medium` 이슈도 기본적으로 phase exit blocker다. carry-over는 plan과 orchestrator에 정책과 근거가 명시된 경우에만 허용한다.
- **Standalone implementation-plan exception**: 기존 feature draft, temporary spec, 구현 재개용 plan artifact가 이미 있고 phase/task detail만 더 필요할 때만 허용한다.

### 2.2 오케스트레이션 대상 실행 유닛

#### feature-draft
- Role: temporary spec draft + implementation plan 통합 생성
- Reasoning note: non-trivial change의 기본 planning entry다. feature-level execution surface를 먼저 고정한다. global spec이 thin core면 관련 코드 탐색이 필수다. single-phase medium path에서 Part 2가 충분히 명확하면 별도 implementation-plan 없이도 implementation 입력으로 쓸 수 있다.

#### plan-review
- Role: planning producer output gate
- Reasoning note: `feature-draft`와 `implementation-plan` output을 downstream step이 소비하기 전에 검토한다. 실패하면 finding을 implementation fix task로 바꾸지 않고, 해당 producer output을 reject/regenerate 대상으로 돌린다.
- Reasoning note: 오케스트레이터 자체도 producer output이다. autopilot Step 5에서 Orchestrator Review Mode로 이 gate를 통과해야 Phase 2로 진행한다.

#### spec-sync
- Role: global spec 동기화 (planned 또는 implemented). 같은 진입점이 evidence 차이로 동작을 적응하므로 구현 전/후 최대 2회 호출될 수 있다.
- Reasoning note: 구현 전 planned 호출은 planned persistent global change만 반영하고, 구현 후 호출은 구현/검증 완료 후 persistent truth만 남긴다. temporary execution detail은 global에 올리지 않는다. planned 호출은 complex planned global alignment가 실제로 필요할 때만 조건부로 사용한다.

#### implementation-plan
- Role: feature draft Part 2를 phase/task 중심 계획으로 세분화
- Reasoning note: `feature-draft` 이후 phase/task/validation linkage를 강화하는 확장 단계다. `feature-draft` Part 2가 충분하지 않거나 multi-phase gate가 필요한 경우에 사용한다. multi-phase 실행으로 판단되면 반드시 포함하며, 각 phase에 `goal`, `task set / dependency closure`, `validation focus`, `exit criteria`, `carry-over policy`를 제공해야 한다. downstream `implementation` step은 이 output을 `Execution Mode: phase-iterative`와 `Phase Source`로 참조해야 한다.

#### implementation
- Role: actual code generation/modification 단계

#### implementation-review
- Role: 구현 결과를 계획/스펙 대비 리뷰

#### spec-review
- Role: global/temporary spec 품질 및 drift 감사
- Reasoning note: thin global model 기준으로 품질을 검증한다.

#### ralph-loop-init
- Role: 장시간 반복 검증 루프 생성 및 실행 지원

### 2.3 비오케스트레이션 스킬

| 스킬 | 용도 |
|------|------|
| spec-create | global spec 최초 생성 |
| discussion | 방향성과 개념 토론 |
| guide-create | 구현/리뷰 가이드 생성 |
| write-phased | inline phased writing helper |
| spec-summary | reader-facing whitepaper for `summary.md`; covers problem, motivation, core design, code grounding, usage/expected results, with appendix only for short planned/progress signals |
| spec-rewrite | canonical model에 맞춰 spec 구조 재정리 |
| spec-upgrade | 구형 spec을 current model로 변환 |
