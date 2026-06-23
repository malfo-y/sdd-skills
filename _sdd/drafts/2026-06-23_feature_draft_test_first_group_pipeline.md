# Feature Draft: Test-First Group-Pipeline Orchestration (RED 게이트 + test-author/impl 분리)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`implementation` 스킬의 phase 내부 fan-out을 **단일 TDD leaf 호출**에서 **wave(group)별 2-stage 파이프라인 + orchestrator 소유 RED 게이트**로 개편한다. 현재 implementation 경로는 문서상 100% test-first(RED→GREEN→REFACTOR)를 지시하지만, 유일한 hard-gate인 Verification Gate가 "코드 변경 후 테스트 재실행+통과 출력"에만 걸려 있어 test-after로도 완벽히 통과된다. RED 단계의 실패 증거를 아무도 요구하지 않고, leaf의 TDD표는 자기보고라 구현 완료 후 backfill 가능하다. 결과적으로 test-first가 falsifiable 산출물로 못박혀 있지 않아 모델이 저항 최소 경로(구현→테스트→통과→TDD표 backfill)로 새어나간다.

개편은 test 작성과 구현을 **별도 agent로 분리**하고, 그 사이에 **orchestrator가 소유하는 RED 게이트**(실패 증거 캡처 + falsifiability 점검)를 강제로 끼워 test-first를 검증 가능한 실행 불변식으로 만든다. 신규 `test-author-agent`(테스트만 작성)와 RED-전용으로 재정의된 `implementation-agent`(고정 실패 테스트를 최소코드로 통과)가 같은 상류 계약(plan의 Contract/Invariant Delta·Validation Plan `V*`)을 실행한다.

## Scope Delta

### In-scope (delta)
- **`test-author-agent` 신규 도입**(leaf): AC + Validation Plan `V*` + Contract/Invariant Delta를 입력받아 **테스트만** 작성한다. 구현 파일 생성 금지. 테스트 파일 경로는 plan이 명시하지 않고 test-author가 기존 테스트 관습을 탐색해 자체 추론한다.
- **`implementation-agent` 재정의**(GREEN 전용): 입력에 고정 실패 테스트 + RED 증거가 추가되고, mandate가 "RED→GREEN→REFACTOR 자체 수행"에서 "이 고정 테스트를 최소코드로 통과시키고 REFACTOR, 테스트 수정 금지"로 변경된다. RED 단계는 test-author + orchestrator 게이트로 이관된다.
- **`implementation` 스킬 Step 4 개편**: wave별 2-stage 파이프라인 — Stage A(테스트 작성: task별 test-author 병렬 dispatch) → RED 게이트(orchestrator 소유) → Stage B(구현: task별 impl-agent 병렬 dispatch) → GREEN 게이트.
- **RED 게이트 신설**(orchestrator 소유): 새 테스트 실행→실패 확인→RED 증거 캡처 + falsifiability 점검(테스트가 AC 관찰동작을 검증하고 `V*`에 1:1 대응하는지, 단순 import/collection 에러로만 빨간 게 아닌지).
- **CONTRACT_MISMATCH 경로 신설**: impl-agent가 테스트의 가정 계약이 틀렸다/구현 불가라고 보면 테스트를 몰래 수정하지 않고 `CONTRACT_MISMATCH: {test} - {문제} - {제안 계약}`으로 보고하고, orchestrator가 test-author 재dispatch 여부를 판정한다(기존 UNPLANNED_DEPENDENCY와 동결).
- **Fix 루프 정책 명문화**: review-fix gate에서 correctness finding(동작 버그)만 test-first(실패 테스트 먼저→fix)로, simplicity/refactor finding은 직접 fix로 처리한다.
- **no-framework graceful degradation**: 테스트 프레임워크 부재 시 test-author가 grep/구조 점검 같은 검증 가능한 acceptance check를 RED artifact로 작성하고, RED 게이트가 현재 미충족을 확인, impl이 충족시킨다. 프레임워크/`_sdd/env.md` 부재 시 기존 `UNTESTED` 표기 경로를 유지한다.

### Out-of-scope (delta)
- **cross-wave 중첩 금지**: wave G의 impl과 wave H의 테스트 작성을 동시에 돌리는 cross-wave 파이프라인 중첩은 도입하지 않는다(prose orchestration에 스케줄러 복잡도만 키우는 speculative 최적화 — YAGNI로 명시 기각). wave 내부만 파이프라인, wave끼리는 기존처럼 순차.
- **별도 test-review agent 신설 안 함**: RED 게이트의 falsifiability 점검은 기존 orchestrator 게이트에 접는다(right-sizing — 신규 agent 미도입).
- **plan 포맷 무변경**: `implementation-plan`/`feature-draft` Part 2 산출물 포맷(Validation Plan, Contract/Invariant Delta, Target Files)은 바꾸지 않는다. test-author는 기존 산출물을 입력으로 받을 뿐이다.
- **모든 finding을 파이프라인 태우지 않음**: simplicity/refactor finding까지 test-first 파이프라인으로 강제하지 않는다.

### Guardrail delta
- **nesting 1단계 제한 유지**: `test-author-agent`와 재정의된 `implementation-agent`는 모두 leaf이며 sub-agent를 spawn하지 않는다. RED/GREEN 게이트·fan-out은 orchestrator(skill/autopilot) 소유.
- **단일 작성자 불변식 유지**: test-author는 테스트 파일만, impl-agent는 자기 Target Files만 쓴다. impl-agent는 고정된 테스트를 수정하지 않는다(CONTRACT_MISMATCH 보고 경로로만 이의 제기).
- **파일 경계 준수 유지**: 두 leaf 모두 할당된 Target Files만 쓰고 그 외는 read-only.
- **Regression Iron Rule·Minimum-Code Mandate 유지**: impl-agent의 REFACTOR(중복 제거·명확성 한정, 단일 사용처 추상화 금지, clarity over brevity)와 회귀 처리는 그대로 유지.

## Persistent Spec Implications

persistent spec(`_sdd/spec/main.md` Guardrails / 주요 결정)에 남아야 하는 계약:

- **test-first는 실행 불변식이다(자기보고 아님)**: implementation-scoped 구현은 테스트 작성과 구현을 분리하고, 그 사이에 orchestrator가 소유하는 RED 게이트(새 테스트 실패 증거 캡처 + falsifiability 점검)를 강제로 닫은 뒤에만 구현을 dispatch한다. RED 증거는 leaf 자기보고 TDD표가 아니라 orchestrator가 캡처한 외부 산출물이다.
- **상류 결정, 하류 실행 분리**: 설계 결정(Contract/Invariant Delta, Validation Plan `V*`)은 plan에서 상류로 확정되고, test-author와 impl-agent는 둘 다 같은 pinned 계약을 실행만 한다. test-author는 계약을 발명하지 않고 plan을 근거로 테스트를 쓴다.
- **테스트는 impl에 대해 고정된다**: impl-agent는 주어진 실패 테스트를 최소코드로 통과시키며 테스트를 수정하지 않는다. 테스트 가정 계약이 틀렸다고 보면 `CONTRACT_MISMATCH`로 보고하고 orchestrator가 test-author 재dispatch를 판정한다(impl이 테스트를 약화시켜 "통과시키고 만세"로 퇴화하는 것을 막는 안전장치).
- **RED 게이트 falsifiability 한정**: RED 게이트는 테스트가 AC 관찰동작을 검증하고 `V*`에 1:1 대응하는 경우에만 통과시킨다. 단순 import/collection 에러로 빨간 것은 유효한 RED가 아니다.
- **wave 내부 파이프라인, wave 간 순차**: 파이프라인 2-stage는 wave 내부에 한정하고 cross-wave 중첩은 도입하지 않는다.
- **graceful degradation**: 테스트 프레임워크 부재 자산(문서/스킬)은 검증 가능한 acceptance check(grep/구조 점검)를 RED artifact로 쓰고, 프레임워크/`_sdd/env.md` 부재 시 `UNTESTED` 표기 경로를 유지한다.
- **agent 등록 확장**: canonical agent set에 `test-author-agent`가 추가되고, `implementation-agent`는 더 이상 RED를 자체 수행하지 않는다(GREEN 전용)는 계약 변화가 autopilot orchestrator-contract에 반영된다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

이 plan은 Part 1의 test-first group-pipeline 계약을 두 leaf agent(claude+codex 미러)와 `implementation` 스킬 orchestration 개편, 그리고 autopilot 계약 참조 정합에 일관되게 구현한다. 핵심 실행 순서: (1) `test-author-agent` 신규 도입(claude+codex)과 `implementation-agent` GREEN 전용 재정의(claude+codex)로 leaf 계약을 먼저 고정하고, (2) `implementation` 스킬(claude+codex)의 Step 4를 2-stage 파이프라인 + RED/GREEN 게이트로, Step 6/7 fix 루프를 correctness-only test-first 정책으로 개편하고, (3) autopilot generated-orchestrator 계약 참조(orchestrator-contract·SKILL·sample-orchestrator + codex 미러)에 "impl-agent는 RED 자체 수행 안 함 + test-author dispatch step 추가" 변화를 반영하고, (4) 신규 agent를 marketplace registry와 codex README에 등록한다.

신규 agent 등록(marketplace `agents` 배열 + `.codex/agents/README.md`)은 SDD 파이프라인이 자동으로 잡지 못하는 누락 지점이다 — 과거 `simplicity-review-agent` 도입 때 동일 census를 명시 task로 잡아야 했던 선례를 따라 registry 등록을 별도 task로 고정한다.

`_sdd/spec/*`(main.md·components.md·decision_log.md·logs/changelog.md) 동기화는 이 plan의 구현 task에 포함하지 않는다 — implementation leaf는 spec 파일 불가침이고, persistent spec 반영은 구현 완료 후 `spec-sync`가 Part 1을 입력으로 수행한다(Q4 참조).

## Scope

### In Scope
- `.claude/agents/test-author-agent.md` 신규 생성, `.codex/agents/test-author-agent.toml` 신규 생성
- `.claude/agents/implementation-agent.md` + `.codex/agents/implementation-agent.toml`: GREEN 전용 재정의(고정 실패 테스트 입력, 테스트 수정 금지, CONTRACT_MISMATCH 경로, RED 이관)
- `.claude/skills/implementation/SKILL.md` + `.codex/skills/implementation/SKILL.md`: Step 4 2-stage 파이프라인 + RED/GREEN 게이트, Step 5/6/7 정합(fix 루프 correctness-only test-first), AC·Hard Rules 갱신
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` + `.codex/...`: Implementation Dispatch Controller 계약에 test-author dispatch + RED 게이트 반영, canonical agent set에 `test-author-agent` 추가
- `.claude/skills/sdd-autopilot/SKILL.md` + `.codex/...`: impl-agent dispatch controller 서술과 canonical agent 호출 목록 갱신
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` + `.codex/...`: 구현 step 예시에 test-author + RED 게이트 반영
- `.claude-plugin/marketplace.json` `agents` 배열 + `.codex/agents/README.md`: `test-author-agent` 등록

### Out of Scope
- cross-wave 파이프라인 중첩(Part 1 out-of-scope)
- 별도 test-review agent 신설(RED 게이트에 falsifiability 점검 접음)
- `implementation-plan`/`feature-draft` 산출물 포맷 변경(plan 포맷 무변경)
- `_sdd/spec/*` 직접 수정(spec-sync 후속 — Q4)
- simplicity/refactor finding의 test-first 강제(correctness finding만 test-first)

## Contract/Invariant Delta and Coverage

| ID | Type | Change | Covered By | Validated By |
|----|------|--------|------------|--------------|
| C1 | Add | `test-author-agent`(read+write 테스트만, leaf)가 AC + `V*` + Contract/Invariant Delta 입력으로 테스트만 작성하고, 테스트 경로를 기존 관습 탐색으로 자체 추론하며, 가정한 인터페이스 계약을 출력에 명시한다 | T1, T2 | V1 |
| C2 | Modify | `implementation-agent`가 GREEN 전용으로 재정의된다 — 입력에 고정 실패 테스트 + RED 증거가 추가되고 mandate가 "고정 테스트를 최소코드로 통과 + REFACTOR, 테스트 수정 금지"로 변경된다. RED는 자체 수행하지 않는다 | T3, T4 | V2 |
| C3 | Add | impl-agent가 테스트의 가정 계약이 틀렸다고 보면 테스트를 수정하지 않고 `CONTRACT_MISMATCH: {test} - {문제} - {제안 계약}`으로 보고하고, orchestrator가 test-author 재dispatch 여부를 판정한다 | T3, T4, T5 | V3 |
| C4 | Add | `implementation` 스킬 Step 4가 wave별 2-stage 파이프라인(Stage A test-author 병렬 → RED 게이트 → Stage B impl 병렬 → GREEN 게이트)이고, wave 간은 순차(cross-wave 중첩 없음)다 | T5, T6 | V4 |
| C5 | Add | RED 게이트(orchestrator 소유)가 새 테스트 실행→실패 확인→RED 증거 캡처 + falsifiability 점검(AC 관찰동작 검증 & `V*` 1:1 & import/collection-only 실패 배제)을 수행하고, 통과 전에는 Stage B를 dispatch하지 않는다 | T5, T6 | V5 |
| C6 | Modify | review-fix gate에서 correctness finding은 test-first(실패 테스트 먼저→fix), simplicity/refactor finding은 직접 fix로 처리한다 | T5, T6 | V6 |
| C7 | Modify | autopilot Implementation Dispatch Controller 계약이 "impl-agent가 RED 자체 수행"에서 "test-author dispatch + orchestrator RED 게이트 + GREEN-전용 impl dispatch"로 갱신되고, canonical agent set에 `test-author-agent`가 추가된다 | T7, T8, T9 | V7 |
| C8 | Add | `test-author-agent`가 marketplace `agents` 배열과 `.codex/agents/README.md` Agent Set에 등록된다 | T10 | V8 |
| I1 | Add | RED 증거는 orchestrator가 캡처한 외부 산출물이며 leaf 자기보고 TDD표로 대체되지 않는다(falsifiable test-first 불변식) | T5, T6 | V5 |
| I2 | Invariant | 테스트는 impl에 대해 고정된다 — impl-agent는 주어진 테스트를 수정하지 않고 CONTRACT_MISMATCH로만 이의 제기한다(약한 테스트 통과로 퇴화 방지) | T3, T4 | V2, V3 |
| I3 | Invariant | nesting 1단계 + 단일 작성자 유지 — test-author/impl 둘 다 leaf(sub-agent 미spawn), test-author는 테스트 파일만·impl은 자기 Target Files만 write | T1, T3 | V1, V2 |
| I4 | Invariant | graceful degradation — 프레임워크 부재 자산은 grep/구조 점검을 RED artifact로 쓰고, 프레임워크/`_sdd/env.md` 부재 시 `UNTESTED` 표기 경로 유지. **분기 기준의 canonical surface는 `implementation` SKILL RED 게이트 서술(T5)**이며 다른 surface(T1 AC·R4)는 이를 참조한다(구현 시 한 곳만 갱신되는 drift 방지) | T1, T5 | V1, V5 |
| I5 | Invariant | claude/codex 미러 정합 — 6쌍 surface의 두 플랫폼 표현이 동일 계약을 담는다 | T2, T4, T6, T8, T9, T10 | V9 |

## Touchpoints

현재 코드 기준으로 재확인한 변경 지점:

- **`.claude/agents/implementation-agent.md`** (현재 leaf, RED→GREEN→REFACTOR 자체 수행) — frontmatter `description`("단일 task를 TDD로 구현"), Hard Rules "TDD 필수"(L35), Verification Gate(L37), Step 2 "TDD per Acceptance Criterion"의 RED bullet(L51-55), 입력 섹션(L22-31, 고정 테스트/RED 증거 미포함), 출력 TDD표(L72-73). RED를 test-author+게이트로 이관하고 GREEN 전용으로 재정의. CONTRACT_MISMATCH 출력 항목 신설.
- **`.codex/agents/implementation-agent.toml`** — claude 본문의 codex 미러(`developer_instructions`). 동일 RED 이관 + CONTRACT_MISMATCH 반영.
- **`.claude/agents/test-author-agent.md`** — 미존재. 신규 생성. `implementation-agent.md`의 leaf 구조(frontmatter `tools`, AC/Hard Rules/입력/Process/출력/Final Check/Role Pointer)를 형제로 따르되 렌즈를 "테스트 작성"으로 한정.
- **`.codex/agents/test-author-agent.toml`** — 미존재. 신규 생성. claude 본문 codex 미러.
- **`.claude/skills/implementation/SKILL.md`** (v3.3.0) — frontmatter title "Parallel TDD"(L7)와 도입부(L9, "각 task의 TDD를 leaf가 수행"), AC1-7(특히 AC3 leaf 입력 4종 L17, AC6 Min-Code), Hard Rules("TDD는 leaf가 수행" L26, Verification Gate L28), Step 4 Fan-out(L126-167, 현재 leaf 1회 dispatch + 입력 4종), Step 5 Integrate & Verify(L169-180), Step 6/7 review-fix gate(L181-221, fix=impl-agent 순차 dispatch). Step 4를 2-stage 파이프라인 + RED/GREEN 게이트로, leaf 입력에 test-author/impl 분기 추가, Step 6/7 fix를 correctness-only test-first로 갱신.
- **`.codex/skills/implementation/SKILL.md`** — claude 본문 codex 미러. 동일 개편.
- **`.claude/skills/sdd-autopilot/references/orchestrator-contract.md`** — 허용 `subagent_type` 목록(L47-55, test-author 없음), §2 Implementation Dispatch Controller(L71-79, "단일 task만 TDD로 수행" L75 — impl이 RED 자체 수행 전제), §6 `fix = sdd-skills:implementation-agent`(L133). canonical agent에 test-author 추가, dispatch controller에 test-author dispatch + RED 게이트 반영, fix step에 correctness-only test-first 정책 반영.
- **`.codex/skills/sdd-autopilot/references/orchestrator-contract.md`** — 동형 미러.
- **`.claude/skills/sdd-autopilot/SKILL.md`** — canonical 호출 예시(L66, L180, L258-259 dispatch controller 서술, L161). impl-agent dispatch controller 서술에 test-author + RED 게이트 단계 반영, canonical 호출 목록에 test-author 추가.
- **`.codex/skills/sdd-autopilot/SKILL.md`** — 동형 미러.
- **`.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`** — 구현 step 서술(L79 "Contract/Invariant Delta and Coverage와 Validation Plan을 기준으로 TDD 방식으로 진행"). 구현 step 예시에 test-author dispatch + RED 게이트 + GREEN-전용 impl 반영.
- **`.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`** — 동형 미러.
- **`.claude-plugin/marketplace.json`** — `plugins[0].agents` 배열(L41-51, test-author 없음). `test-author-agent.md` 추가.
- **`.codex/agents/README.md`** — `Agent Set`(L20-29)·`Inline Writing`(미해당 — test-author는 inline writing helper 아님). Agent Set에 `test-author-agent` 추가.

## Implementation Phases

### Phase 1: Leaf agents (신규 test-author + impl GREEN 재정의)
두 leaf 본문이 이후 모든 orchestration surface의 계약 기준이 되므로 먼저 고정한다.

| Task | 목적 | Dependencies |
|------|------|--------------|
| T1 | `test-author-agent.md`(claude) 신규 생성 | - |
| T2 | `test-author-agent.toml`(codex) 미러 생성 | T1 |
| T3 | `implementation-agent.md`(claude) GREEN 전용 재정의 + CONTRACT_MISMATCH | - |
| T4 | `implementation-agent.toml`(codex) 동일 재정의 미러 | T3 |

### Phase 2: implementation 스킬 orchestration 개편
leaf 계약을 소비하는 orchestrator 스킬을 2-stage 파이프라인 + RED/GREEN 게이트 + correctness-only fix로 개편한다.

| Task | 목적 | Dependencies |
|------|------|--------------|
| T5 | `implementation` SKILL(claude) Step 4 파이프라인 + RED/GREEN 게이트 + Step 6/7 fix 정책 | T1, T3 |
| T6 | `implementation` SKILL(codex) 동형 미러 | T2, T4, T5 |

### Phase 3: autopilot 계약 참조 정합 + registry 등록
generated-orchestrator 계약을 leaf/orchestrator 변화에 맞추고, 신규 agent를 registry에 등록한다.

| Task | 목적 | Dependencies |
|------|------|--------------|
| T7 | autopilot `orchestrator-contract.md`(claude) dispatch controller + canonical agent + fix 정책 갱신 | T1, T3, T5 |
| T8 | autopilot `orchestrator-contract.md`(codex) + `SKILL.md`(claude+codex) 갱신 | T7 |
| T9 | autopilot `sample-orchestrator.md`(claude+codex) 구현 step 예시 갱신 | T7 |
| T10 | `marketplace.json` `agents` 배열 + `.codex/agents/README.md` Agent Set 등록 | T1 |

## Task Details

### Task T1: test-author-agent (claude) 신규 생성
**Priority**: P0
**Type**: Feature

**Description**: `.claude/agents/test-author-agent.md`를 신규 생성한다. `implementation-agent.md`의 leaf 구조(frontmatter `tools`, `model: inherit`, AC / 입력(orchestrator dispatch 전달) / Hard Rules / Process / 출력(orchestrator로 반환) / 안 하는 것 / Final Check / Role Pointer)를 형제 agent로 따르되 렌즈를 **테스트 작성 전용**으로 한정한다. 입력은 task AC + Validation Plan `V*` + Contract/Invariant Delta(orchestrator가 dispatch 시 전달) + 환경/테스트 명령이다. 작업: 각 AC마다 그 AC의 관찰 동작을 검증하는 의미 있는 테스트 1개를 작성한다(구현 내부가 아니라 관찰 동작 검증, `V*`에 1:1 대응). 테스트 파일 경로는 plan이 명시하지 않으므로 기존 테스트 디렉토리/네이밍 관습을 Grep/Glob으로 탐색해 자체 추론한다. 구현 파일은 생성하지 않는다. 출력에 "테스트가 가정한 인터페이스 계약"(impl-agent가 받음 — 어떤 함수/시그니처/반환을 호출하는지)을 명시한다. 프레임워크 부재 자산(문서/스킬)이면 테스트를 검증 가능한 acceptance check(grep/구조 점검)로 대체해 RED artifact로 쓰고, 프레임워크/`_sdd/env.md` 부재 시 `UNTESTED` 사유를 기록한다(I4).

**Non-Goals**: 구현 코드를 작성하지 않는다(테스트만). RED 실행/실패 증거 캡처를 자체 수행하지 않는다 — 그것은 orchestrator RED 게이트 소관이다. 계약(C*/I*/V*)을 발명하지 않는다 — plan 입력을 근거로만 테스트를 쓴다.

**Acceptance Criteria**:
- [ ] frontmatter가 `name: test-author-agent`, `tools`(테스트 작성에 필요한 Read/Write/Edit/Bash/Glob/Grep), `model: inherit`를 갖는다 (grep 확인)
- [ ] 본문이 AC / 입력 / Hard Rules / Process / 출력 / 안 하는 것 / Final Check / Role Pointer 섹션을 포함한다 (impl-agent leaf와 동형 — 섹션 heading grep)
- [ ] 입력 계약이 task AC + Validation Plan `V*` + Contract/Invariant Delta + 환경/테스트 명령을 orchestrator가 전달함으로 명시된다
- [ ] Process가 "AC당 관찰 동작 검증 테스트 1개, `V*`에 1:1 대응"과 "테스트 경로는 기존 관습 탐색으로 자체 추론"을 명시한다
- [ ] 출력 계약이 "테스트가 가정한 인터페이스 계약"을 impl-agent에 전달하도록 명시한다
- [ ] Hard Rules가 "구현 파일 생성 금지"(테스트만)와 nesting 1단계(sub-agent 미spawn) + 단일 작성자(테스트 파일만 write)를 명시한다 (I3)
- [ ] graceful degradation(프레임워크 부재 → grep/구조 점검 acceptance check, `_sdd/env.md` 부재 → `UNTESTED`)이 명시된다 (I4)
- [ ] Role Pointer가 이 agent를 leaf로, fan-out/RED 게이트를 소유하는 orchestrator(`implementation` skill / autopilot)를 가리킨다

**Target Files**:
- [C] `.claude/agents/test-author-agent.md` -- 신규 leaf agent. test 작성과 구현은 별도 렌즈(상류 결정/하류 실행)이고 impl-agent와 입출력 계약이 다르므로 기존 파일 수정이 아닌 형제 파일 신규 생성(확정 설계 "신규 test-author-agent")

**Technical Notes**: Covers C1, I3, I4; validated by V1. `implementation-agent.md`를 구조 템플릿으로 삼되 GREEN/REFACTOR/Verification Gate 본문은 복제하지 않는다 — test-author는 테스트 작성 leaf라 구현 절차가 불필요(Min-Code: 요청되지 않은 구현 절차 미도입). 테스트 경로 자체 추론은 plan 포맷 무변경 결정의 직접 귀결이다(plan이 테스트 경로를 명시하지 않음).

**Dependencies**: -

---

### Task T2: test-author-agent (codex) 미러 생성
**Priority**: P0
**Type**: Feature

**Description**: `.codex/agents/test-author-agent.toml`을 신규 생성해 T1의 claude agent 본문을 codex 표현으로 미러한다. `.codex/agents/implementation-agent.toml` 형식(`name`/`description`/`developer_instructions = '''...'''`)을 따른다. `description`은 `spawn_agent(agent_type="test-author-agent")` 호출 안내를 담고, `developer_instructions`에 T1과 동일 계약(테스트만 작성, AC당 1테스트 `V*` 1:1, 경로 자체 추론, 가정 인터페이스 계약 출력, graceful degradation, leaf/단일 작성자)을 담는다. Role Pointer는 codex orchestrator(autopilot/generated orchestrator)를 가리킨다.

**Acceptance Criteria**:
- [ ] `.codex/agents/test-author-agent.toml`이 `name = "test-author-agent"`로 존재한다 (grep 확인)
- [ ] `developer_instructions`가 T1 claude 본문과 동일 계약(테스트만, AC당 1테스트 `V*` 1:1, 경로 자체 추론, 가정 인터페이스 계약 출력, graceful degradation)을 담는다 — 두 본문의 계약 항목이 1:1 대응한다 (I5)
- [ ] codex 호출 표현이 `spawn_agent`/`wait_agent`/`close_agent` 규약(`.codex/agents/README.md` Invocation Contract)과 정합한다

**Target Files**:
- [C] `.codex/agents/test-author-agent.toml` -- codex custom agent 신규 생성. codex agent는 `.toml` 단일 소스 형식이라 claude `.md`와 별개 파일이 필요(플랫폼 parity 수동 관리 — spec 운영 제약)

**Technical Notes**: Covers C1, I5; validated by V1, V9. claude `.md`와 codex `.toml`은 형식만 다르고 계약은 동일하다 — 미러 정합(I5)이 검증 대상.

**Dependencies**: T1

---

### Task T3: implementation-agent (claude) GREEN 전용 재정의
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/agents/implementation-agent.md`를 GREEN 전용 leaf로 재정의한다. 구체 변경:
1. frontmatter `description`을 "단일 task를 TDD로 구현"에서 "고정 실패 테스트를 최소코드로 통과시켜 단일 task를 구현(GREEN→REFACTOR)"으로 갱신.
2. 도입부와 Hard Rules "TDD 필수"(RED→GREEN→REFACTOR 자체 수행)를 "주어진 고정 실패 테스트를 최소코드로 통과시키고(GREEN) REFACTOR한다. RED는 자체 수행하지 않으며 테스트를 수정하지 않는다"로 갱신.
3. 입력 섹션에 "고정 실패 테스트(파일 경로 목록) + RED 증거(orchestrator가 캡처한 실패 출력)"를 추가한다.
4. Step 2를 "TDD per AC(RED→GREEN→REFACTOR)"에서 "고정 테스트를 GREEN시키고 REFACTOR(중복 제거·명확성 한정, 단일 사용처 추상화 금지, clarity over brevity)"로 갱신. RED bullet 제거.
5. `CONTRACT_MISMATCH` 출력 경로 신설: 테스트의 가정 계약이 틀렸다/구현 불가라고 판단하면 테스트를 수정하지 말고 `CONTRACT_MISMATCH: {test} - {문제} - {제안 계약}`으로 보고한다(기존 `UNPLANNED_DEPENDENCY`와 동결 구조). 두 신호의 경계를 본문에 1줄 명문화: **고정 테스트가 가정한 인터페이스 계약 자체가 틀림/구현 불가 → CONTRACT_MISMATCH**(해결책=test-author 재작성); **계약은 맞으나 Target Files 밖 파일 수정이 필요 → UNPLANNED_DEPENDENCY**(해결책=orchestrator가 경계 확장/추가 task). 둘 다 해당하면(밖 파일에 의존하는 계약 오류) **CONTRACT_MISMATCH 우선**으로 보고하고 의존 파일을 함께 적는다.
6. 본문 계약에 orchestrated-only 경계 1줄 추가: 이 leaf는 항상 고정 실패 테스트 + RED 증거를 입력으로 받는 orchestrated 경로(`implementation` 스킬/autopilot)에서만 호출된다. 입력에 고정 테스트/RED 증거가 **없으면 자체 RED(테스트) 작성을 금지하고** 입력 누락을 `BLOCKED`로 보고한다(테스트 없는 직접 호출은 지원 계약 밖 — test-after 재개방 방지). self-RED fallback 분기는 도입하지 않는다.
7. 출력 TDD표를 GREEN 전용 진행표(고정 테스트 → GREEN → REFACTOR 상태)로 갱신. Verification Gate(코드 변경 후 테스트 재실행+통과 출력)·Regression Iron Rule·Minimum-Code Mandate·파일 경계·Spec 불가침은 유지.

**Non-Goals**: REFACTOR 정책(중복 제거·명확성 한정, 단일 사용처 추상화 금지, clarity over brevity), Regression 처리, 파일 경계, Min-Code, Verification Gate는 의미를 바꾸지 않는다 — RED 자체 수행만 제거하고 입력에 고정 테스트를 추가한다. 테스트 작성 능력을 이 agent에 남기지 않는다(test-author 소관).

**Acceptance Criteria**:
- [ ] frontmatter `description`이 GREEN 전용("고정 실패 테스트를 최소코드로 통과")을 담는다 (grep)
- [ ] Hard Rules/도입부에 "RED 자체 수행 안 함" + "테스트 수정 금지"가 명시되고, RED→GREEN→REFACTOR를 leaf가 자체 수행한다는 표현이 0건이다 (grep `RED→GREEN→REFACTOR` 자체수행 문맥 → no match)
- [ ] 입력 섹션이 "고정 실패 테스트(경로) + RED 증거(orchestrator 캡처 실패 출력)"를 포함한다
- [ ] Step 2가 GREEN→REFACTOR로 갱신되고 RED 작성 bullet이 제거된다
- [ ] `CONTRACT_MISMATCH: {test} - {문제} - {제안 계약}` 출력 경로가 신설되고 "테스트를 직접 수정하지 않는다"가 명시된다 (I2)
- [ ] CONTRACT_MISMATCH ↔ UNPLANNED_DEPENDENCY 경계가 **판정 규칙**으로 명시된다: 가정 계약 오류=CONTRACT_MISMATCH(→test-author 재작성), Target Files 밖 구현 의존=UNPLANNED_DEPENDENCY(→경계 확장), 둘 다면 CONTRACT_MISMATCH 우선 + 의존 파일 병기 (C3, #M3)
- [ ] 입력에 고정 실패 테스트 + RED 증거가 **없을 때**의 행동이 명시된다: 자체 RED(테스트) 작성 금지 → 입력 누락을 `BLOCKED`로 보고. 본문 계약에 "이 leaf는 항상 고정 테스트 + RED 증거를 입력으로 받는 orchestrated 경로에서만 호출되며 테스트 없는 직접 호출은 지원 계약 밖"이 1줄로 박혀 있다 (I2, #M2 — test-after 재개방 방지)
- [ ] REFACTOR 정책(단일 사용처 추상화 금지, clarity over brevity) · Verification Gate · Regression Iron Rule · 파일 경계 · Spec 불가침이 잔존 확인된다 (해당 문구 grep)
- [ ] 출력 진행표가 GREEN 전용(고정 테스트→GREEN→REFACTOR)으로 갱신된다

**Target Files**:
- [M] `.claude/agents/implementation-agent.md` -- GREEN 전용 재정의 + CONTRACT_MISMATCH

**Technical Notes**: Covers C2, C3, I2; validated by V2, V3. RED 이관이지 삭제가 아니다 — RED 단계는 T1 test-author + orchestrator RED 게이트(T5)가 흡수한다. CONTRACT_MISMATCH는 impl이 테스트를 약화시켜 통과시키는 퇴화(약한 테스트 통과로 만세)를 막는 안전장치로, 기존 `UNPLANNED_DEPENDENCY` 보고 구조를 그대로 차용한다(새 보고 메커니즘 미도입).

**Dependencies**: -

---

### Task T4: implementation-agent (codex) GREEN 전용 재정의 미러
**Priority**: P0
**Type**: Refactor

**Description**: `.codex/agents/implementation-agent.toml`의 `developer_instructions`를 T3와 동일하게 GREEN 전용으로 재정의한다(고정 실패 테스트 입력, RED 자체 수행 제거, 테스트 수정 금지, CONTRACT_MISMATCH 경로, GREEN 전용 진행표). codex 본문의 cross-reference 번호 체계를 codex 쪽에 맞게 유지한다.

**Acceptance Criteria**:
- [ ] `developer_instructions`가 GREEN 전용 재정의(고정 테스트 입력, RED 자체 수행 제거, 테스트 수정 금지, CONTRACT_MISMATCH)를 담는다 — T3(claude)와 변경 항목 집합이 1:1 대응한다 (I5)
- [ ] CONTRACT_MISMATCH ↔ UNPLANNED_DEPENDENCY 경계 판정 규칙과 입력 누락 시 행동(자체 RED 작성 금지 → `BLOCKED`, orchestrated-only 경계)이 T3와 1:1 대응한다 (I5, #M2, #M3)
- [ ] codex 본문에 RED→GREEN→REFACTOR 자체 수행 표현이 0건이다 (grep → no match)
- [ ] codex 호출/cross-reference 표기가 codex 체계와 정합한다

**Target Files**:
- [M] `.codex/agents/implementation-agent.toml` -- GREEN 전용 재정의 미러

**Technical Notes**: Covers C2, C3, I5; validated by V2, V3, V9.

**Dependencies**: T3

---

### Task T5: implementation 스킬 (claude) Step 4 파이프라인 + RED/GREEN 게이트 + fix 정책
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/skills/implementation/SKILL.md` Step 4를 wave별 2-stage 파이프라인 + orchestrator 소유 RED/GREEN 게이트로 개편한다:
1. **Step 4 Fan-out**을 wave(group)별 2-stage로 재구성: (Stage A) wave 내 task마다 `test-author-agent` leaf를 병렬 dispatch(테스트만, 입력=task AC + `V*` + Contract/Invariant Delta + 환경/테스트) → (RED 게이트) → (Stage B) wave 내 task마다 `implementation-agent` leaf를 병렬 dispatch(입력=task 필드 + Target Files + 환경/테스트 + 선행 보장 + **고정 실패 테스트 + RED 증거**) → (GREEN 게이트). wave 간은 기존처럼 순차이며 cross-wave 중첩은 하지 않음을 명시(C4).
2. **RED 게이트(orchestrator 소유) 신설**: Stage A 완료 후 새 테스트를 실행→실패 확인→RED 증거(실패 출력) 캡처 + falsifiability 점검(테스트가 AC 관찰동작을 검증하고 `V*`에 1:1 대응하는지, 단순 import/collection 에러로만 빨간 게 아닌지). falsifiability를 **관찰 가능한 판정 규칙**으로 못박는다: 실패가 AC 관찰 동작에 대한 assertion/check 단계 실패(예: AssertionError 계열)여야 RED 통과로 인정하고, 순수 collection/import/syntax 단계 실패로만 빨간 테스트는 RED 미충족으로 분류해 test-author 재작성으로 돌린다. 어느 단계에서 실패했는지를 RED 증거에 기록한다(언어/프레임워크가 두 단계를 출력상 구분 못 하면 그 사실을 기록하고 리뷰 판정으로 강등). 통과 전에는 Stage B를 dispatch하지 않음(C5, I1). 프레임워크 부재 자산은 acceptance check의 현재 미충족을 명령 exit/diff로 RED 캡처하고, `_sdd/env.md` 부재 시 `UNTESTED` 경로 유지(I4).
3. **GREEN 게이트**: Stage B 완료 후 테스트 실행→통과 확인→GREEN 증거 캡처(기존 Step 5 post-group 통합·회귀 스윕은 유지).
4. **CONTRACT_MISMATCH 처리**: Stage B leaf가 CONTRACT_MISMATCH를 보고하면 orchestrator가 test-author 재dispatch 여부를 판정한다(기존 UNPLANNED_DEPENDENCY 처리와 동결).
5. **Step 6/7 review-fix gate 정책**: correctness finding(동작 버그)은 test-first(실패 테스트 먼저 작성→fix), simplicity/refactor finding은 직접 fix로 처리함을 명시(C6 — 모든 finding을 파이프라인 태우지 않음).
6. **AC/Hard Rules 정합**: AC3(leaf 입력)을 2-stage 입력(test-author 입력 + impl 입력에 고정 테스트/RED 증거)으로 갱신, Hard Rule "TDD는 leaf가 수행"을 "RED는 test-author+orchestrator 게이트, GREEN→REFACTOR는 impl leaf"로 갱신. frontmatter version bump.

**Non-Goals**: cross-wave 파이프라인 중첩을 도입하지 않는다. 별도 test-review agent를 신설하지 않는다(falsifiability 점검은 RED 게이트에 접음). 모든 finding을 test-first로 강제하지 않는다(correctness만). post-group 통합·회귀(Step 5)·Step 6/7 reviewer loop의 2-reviewer 구조·exit 조건은 바꾸지 않는다.

**Acceptance Criteria**:
- [ ] Step 4가 wave별 Stage A(test-author 병렬) → RED 게이트 → Stage B(impl 병렬) → GREEN 게이트 순서를 명시한다 (두 agent 이름 + 4단계 등장)
- [ ] wave 간은 순차이고 cross-wave 중첩이 없음이 명시된다 (C4 — "cross-wave 중첩 없음" 또는 동등 문구)
- [ ] RED 게이트가 orchestrator 소유로 (a) 새 테스트 실행→실패 확인, (b) RED 증거 캡처, (c) falsifiability 점검(AC 관찰동작 & `V*` 1:1 & import/collection-only 실패 배제), (d) 통과 전 Stage B 미dispatch를 명시한다 (C5, I1)
- [ ] RED 게이트의 import/collection-only 실패 배제가 **관찰 가능한 판정 규칙**으로 명시된다: 각 테스트의 실패가 **AC 관찰 동작에 대한 assertion/check 단계 실패**(예: AssertionError 계열)여야 RED 통과로 인정하고, **순수 collection/import/syntax 단계 실패**(예: ImportError·collection error)로만 빨간 테스트는 RED 미충족으로 분류해 test-author 재작성으로 돌린다. 판정 근거(어느 단계에서 실패했는지)를 RED 증거에 기록함이 적혀 있다. 해당 언어/프레임워크에서 collection 에러와 assertion 실패가 출력상 구분 불가하면 그 사실을 RED 증거에 기록하고 falsifiability 점검을 리뷰 판정으로 강등함을 1줄로 명시한다. graceful-degradation 경로(grep/구조 점검)에서는 "현재 미충족"을 어떤 명령 exit/diff로 캡처하는지 1줄 명시한다 (C5, I1, I4)
- [ ] Stage B impl 입력에 "고정 실패 테스트 + RED 증거"가 포함됨이 명시된다
- [ ] CONTRACT_MISMATCH 보고 시 orchestrator가 test-author 재dispatch 여부를 판정함이 명시된다 (C3)
- [ ] Step 6/7 fix 정책이 "correctness finding=test-first, simplicity/refactor finding=직접 fix"로 명시된다 (C6)
- [ ] graceful degradation(프레임워크 부재 자산 acceptance check RED, `_sdd/env.md` 부재 UNTESTED)이 RED 게이트 서술에 포함된다 (I4)
- [ ] AC3와 Hard Rule "TDD는 leaf가 수행"이 2-stage(RED=test-author+게이트, GREEN→REFACTOR=impl)로 갱신되고, impl leaf가 RED를 자체 수행한다는 표현이 0건이다 (grep)

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Step 4 2-stage 파이프라인 + RED/GREEN 게이트, Step 6/7 fix 정책, AC/Hard Rules 정합

**Technical Notes**: Covers C3, C4, C5, C6, I1, I4; validated by V3, V4, V5, V6. RED 게이트가 falsifiable test-first 불변식(I1)의 집행 지점이다 — leaf 자기보고 TDD표를 외부 캡처 RED 증거로 대체한다. Step 5 post-group 통합·회귀 스윕은 GREEN 게이트 뒤에 그대로 위치(재구현 없음). cross-wave 중첩 미도입은 prose orchestration 복잡도 회피(YAGNI)다.

**Dependencies**: T1, T3

---

### Task T6: implementation 스킬 (codex) 동형 미러
**Priority**: P0
**Type**: Refactor

**Description**: `.codex/skills/implementation/SKILL.md`에 T5와 동일한 개편을 codex 표현(`spawn_agent`/`wait_agent`/`close_agent`)으로 미러한다 — Step 4 2-stage 파이프라인 + RED/GREEN 게이트, CONTRACT_MISMATCH 처리, Step 6/7 correctness-only test-first fix 정책, AC/Hard Rules 정합.

**Acceptance Criteria**:
- [ ] codex Step 4가 Stage A(test-author 병렬) → RED 게이트 → Stage B(impl 병렬) → GREEN 게이트 + cross-wave 중첩 없음을 담고, T5(claude)와 단계/순서가 1:1 대응한다 (I5)
- [ ] codex RED 게이트 서술(실패 확인 + RED 증거 캡처 + falsifiability 점검 + 통과 전 Stage B 미dispatch)이 T5와 1:1 대응한다 (I5)
- [ ] codex RED 게이트의 관찰 가능한 판정 규칙(assertion/check 단계 실패만 RED 통과, collection/import/syntax-only 실패는 미충족→재작성, 실패 단계를 RED 증거에 기록, 구분 불가 시 리뷰 판정 강등)이 T5와 1:1 대응한다 (I5)
- [ ] codex Step 6/7 fix 정책(correctness=test-first, simplicity/refactor=직접 fix)이 T5와 1:1 대응한다 (I5)
- [ ] codex 호출 표현이 `spawn_agent`/`wait_agent`/`close_agent` 규약과 정합한다

**Target Files**:
- [M] `.codex/skills/implementation/SKILL.md` -- T5 동형 미러

**Technical Notes**: Covers C4, C5, C6, I5; validated by V4, V5, V6, V9. codex 미러는 claude 변경에 종속이라 분리하면 인위적 dependency만 늘어난다(T5 후).

**Dependencies**: T2, T4, T5

---

### Task T7: autopilot orchestrator-contract (claude) dispatch controller + canonical agent + fix 정책 갱신
**Priority**: P1
**Type**: Refactor

**Description**: `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`를 leaf/orchestrator 변화에 맞춘다:
1. 허용 `subagent_type` 목록에 `sdd-skills:test-author-agent` 추가.
2. §2 Implementation Dispatch Controller에서 "task-level `implementation-agent` leaf는 단일 task만 TDD로 수행"을 "초기 구현 step은 wave별로 (a) `test-author-agent` leaf 병렬 dispatch(테스트만) → (b) orchestrator 소유 RED 게이트(실패 증거 캡처 + falsifiability 점검) → (c) `implementation-agent` leaf 병렬 dispatch(고정 실패 테스트 + RED 증거 입력, GREEN→REFACTOR). impl-agent는 RED를 자체 수행하지 않는다"로 갱신. cross-wave 중첩 없음 명시.
3. §6 fix step 정책에 "correctness finding은 test-first(실패 테스트 먼저→fix), simplicity/refactor finding은 직접 fix" 한 줄 추가(기존 `fix = sdd-skills:implementation-agent` 순차 매핑은 유지).
4. CONTRACT_MISMATCH를 leaf 반환 항목으로 추가(기존 UNPLANNED_DEPENDENCY 옆).

**Non-Goals**: §6 review-fix loop의 2-reviewer 구조·exit 조건·Checkpoint group 모델은 바꾸지 않는다. Planning Producer Review Gate는 무관하므로 건드리지 않는다.

**Acceptance Criteria**:
- [ ] 허용 `subagent_type` 목록에 `sdd-skills:test-author-agent`가 포함된다 (grep)
- [ ] §2 Implementation Dispatch Controller가 wave별 (test-author 병렬 → RED 게이트 → impl 병렬) 3단계 + "impl-agent는 RED 자체 수행 안 함"을 명시하고, "단일 task만 TDD로 수행"(impl이 RED 자체 수행 전제) 표현이 갱신된다
- [ ] §6 fix 정책에 correctness-only test-first 분기가 추가되고 `fix = sdd-skills:implementation-agent` 순차 매핑은 유지된다
- [ ] leaf 반환 항목에 CONTRACT_MISMATCH가 추가된다
- [ ] cross-wave 중첩 없음이 명시된다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` -- dispatch controller + canonical agent + fix 정책 갱신

**Technical Notes**: Covers C7; validated by V7. orchestrator-contract가 generated-orchestrator 계약의 canonical home이므로 SKILL/sample(T8/T9)의 표기 기준이다 — T8/T9는 이 표기를 따른다. T5(implementation 스킬)에서 RED 게이트·2-stage 흐름을 먼저 고정한 뒤 계약 문서에 반영한다.

**Dependencies**: T1, T3, T5

---

### Task T8: autopilot orchestrator-contract (codex) + SKILL.md (claude+codex) 갱신
**Priority**: P1
**Type**: Refactor

**Description**: 세 surface를 T7 기준으로 갱신한다(모두 "generated-orchestrator가 test-author dispatch + RED 게이트 + GREEN-전용 impl을 안다"는 동일 계약을 각 표현에 반영하는 단일 목적):
1. `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`: T7과 동형 미러(codex `agent_type` 표기).
2. `.claude/skills/sdd-autopilot/SKILL.md`: impl-agent dispatch controller 서술(L258-259 등)에 test-author dispatch + RED 게이트 단계 반영, canonical 호출 목록/예시(L66 등)에 `sdd-skills:test-author-agent` 추가.
3. `.codex/skills/sdd-autopilot/SKILL.md`: claude SKILL 변경 동형 미러.

**Acceptance Criteria**:
- [ ] codex orchestrator-contract가 T7(claude) 변경과 1:1 대응한다 (test-author 허용 목록, dispatch controller 3단계, fix 정책, CONTRACT_MISMATCH) (I5)
- [ ] claude `SKILL.md` dispatch controller 서술이 test-author dispatch + RED 게이트 + GREEN-전용 impl을 반영하고, canonical 호출 목록에 `test-author-agent`가 추가된다
- [ ] codex `SKILL.md`가 claude `SKILL.md` 변경과 1:1 대응한다 (I5)
- [ ] 세 surface가 T7 orchestrator-contract 표기와 모순되지 않는다

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- T7 동형 미러
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- dispatch controller 서술 + canonical 호출 목록 갱신
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- claude SKILL 동형 미러

**Technical Notes**: Covers C7, I5; validated by V7, V9. orchestrator-contract가 canonical home이므로 SKILL 표기는 contract(T7)를 따른다. 세 surface를 한 task로 묶은 이유: 동일 계약을 autopilot 참조 layer에 반영하는 단일 목적이고 codex 미러는 claude에 종속.

**Dependencies**: T7

---

### Task T9: autopilot sample-orchestrator (claude+codex) 구현 step 예시 갱신
**Priority**: P1
**Type**: Refactor

**Description**: 예시 orchestrator의 구현 step 서술을 갱신한다:
1. `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`: 구현 step 서술(L79 "Validation Plan을 기준으로 TDD 방식으로 진행")을 wave별 test-author dispatch → orchestrator RED 게이트 → GREEN-전용 impl dispatch 흐름으로 갱신. review-fix gate 예시의 correctness-only test-first fix 반영.
2. `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`: 동형 미러.

**Acceptance Criteria**:
- [ ] claude sample-orchestrator 구현 step이 test-author dispatch → RED 게이트 → GREEN-전용 impl dispatch를 반영한다 (두 agent 이름 + RED 게이트 등장)
- [ ] sample-orchestrator의 fix 예시가 correctness=test-first / simplicity·refactor=직접 fix를 반영한다
- [ ] sample-orchestrator 표기가 T7 orchestrator-contract §2/§6와 일치한다
- [ ] codex sample-orchestrator가 claude와 1:1 대응한다 (I5)

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` -- 구현 step 예시 갱신
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- 동형 미러

**Technical Notes**: Covers C7, I5; validated by V7, V9. sample-orchestrator는 autopilot 생성물 품질 기준 예시이므로 T7 contract 표기를 source로 따른다.

**Dependencies**: T7

---

### Task T10: test-author-agent registry 등록 (marketplace.json + codex README)
**Priority**: P1
**Type**: Infrastructure

**Description**: 신규 agent를 registry 두 곳에 등록한다(SDD 파이프라인이 자동으로 잡지 못하는 누락 지점 — simplicity-review-agent 선례):
1. `.claude-plugin/marketplace.json`의 `plugins[0].agents` 배열에 `"./.claude/agents/test-author-agent.md"`를 추가한다.
2. `.codex/agents/README.md`의 `Agent Set` 목록에 `test-author-agent`를 추가한다. (test-author는 inline writing helper가 아니므로 `Inline Writing` 목록에는 추가하지 않는다.)

**Non-Goals**: 기존 agent 항목·순서·다른 registry 필드는 건드리지 않는다 — test-author 한 항목만 추가한다.

**Acceptance Criteria**:
- [ ] `marketplace.json` `plugins[0].agents` 배열에 `./.claude/agents/test-author-agent.md`가 포함되고 JSON이 유효하다 (`python3 -m json.tool` exit 0)
- [ ] `.codex/agents/README.md` `Agent Set` 목록에 `test-author-agent`가 포함된다 (grep)
- [ ] 기존 agent 항목이 모두 보존된다 (기존 9개 + test-author = 10개)

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- `agents` 배열에 test-author 등록
- [M] `.codex/agents/README.md` -- Agent Set에 test-author 등록

**Technical Notes**: Covers C8; validated by V8. T1(claude agent 파일 존재)에만 종속 — registry 등록은 파일 경로를 가리키므로 T1 완료 후 가능. autopilot 계약(T7~T9)과 독립.

**Dependencies**: T1

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I3, I4 | review (2등급 정성) | `.claude/agents/test-author-agent.md`(+ codex 미러)를 리뷰어가 읽어 (a) leaf 섹션 동형, (b) 입력=AC+`V*`+Contract/Invariant Delta, (c) AC당 관찰동작 테스트 1개 `V*` 1:1 + 경로 자체 추론, (d) 가정 인터페이스 계약 출력, (e) 구현 생성 금지 + leaf/단일 작성자, (f) graceful degradation 확인. 위반 사례(누락 섹션/계약)를 지목 못하면 MET. 증거=인용한 heading/문장 |
| V2 | C2, I2 | test (1등급 정량) + review (2등급 정성 보조) | (정량) `grep -c "RED→GREEN→REFACTOR" .claude/agents/implementation-agent.md`의 자체수행 문맥 매칭 → 0; `grep "고정 실패 테스트"` → 1+; `grep "테스트.*수정.*금지\|테스트를 수정하지" ` → 1+(테스트 고정 명시). codex 미러 동일. 증거=grep 출력. (정성 보조) GREEN 전용 재정의가 REFACTOR/Verification Gate/Regression/Min-Code를 보존했는지 리뷰 인용 |
| V3 | C3, I2 | review (2등급 정성) | impl-agent(claude+codex)와 `implementation` SKILL을 리뷰어가 읽어 (a) `CONTRACT_MISMATCH: {test} - {문제} - {제안 계약}` 출력 경로가 impl에 신설됐고 "테스트 직접 수정 안 함"이 명시됐는지, (b) SKILL이 CONTRACT_MISMATCH 시 orchestrator의 test-author 재dispatch 판정을 명시하는지, (c) **CONTRACT_MISMATCH↔UNPLANNED_DEPENDENCY 경계 판정 규칙**(가정 계약 오류=CONTRACT_MISMATCH / Target Files 밖 의존=UNPLANNED_DEPENDENCY / 겹치면 CONTRACT_MISMATCH 우선)이 AC로 박혔는지(#M3), (d) **입력에 고정 테스트/RED 증거가 없을 때** 자체 RED 작성 금지→`BLOCKED` 보고 + "orchestrated-only 경로" 비지원 명시(#M2)가 박혔는지 확인. 넷 중 하나라도 없으면 NOT MET. 두 신호가 같은 케이스에서 비결정적으로 선택될 여지가 남으면(#M3) 또는 입력 누락 시 자체 RED 작성이 허용되면(#M2) NOT MET. 증거=인용한 보고/처리/경계/누락처리 문장 |
| V4 | C4 | review (2등급 정성) | `implementation` SKILL(claude+codex) Step 4를 리뷰어가 읽어 wave별 Stage A(test-author 병렬)→RED 게이트→Stage B(impl 병렬)→GREEN 게이트 순서와 "wave 간 순차 + cross-wave 중첩 없음"이 명시됐는지 확인. 4단계 중 하나라도 누락이거나 cross-wave 중첩이 허용되면 NOT MET. 증거=인용한 Step 4 흐름 문장 |
| V5 | C5, I1, I4 | review (2등급 정성) | `implementation` SKILL Step 4 RED 게이트 서술을 리뷰어가 읽어 (a) orchestrator 소유, (b) 새 테스트 실행→실패 확인→RED 증거 캡처, (c) falsifiability 점검이 **관찰 가능한 판정 규칙**으로 적혔는지(#M1): assertion/check 단계 실패만 RED 통과로 인정, collection/import/syntax-only 실패는 RED 미충족→test-author 재작성, 실패 단계를 RED 증거에 기록, 구분 불가 시 그 사실 기록 + 리뷰 판정 강등, (d) 통과 전 Stage B 미dispatch, (e) graceful degradation(프레임워크 부재 자산은 "현재 미충족"을 명령 exit/diff로 RED 캡처 / `_sdd/env.md` 부재 UNTESTED)을 확인. falsifiability 점검이 "존재"만 적히고 import/collection-only 실패 배제가 관찰 가능한 규칙으로 못박히지 않았으면(#M1) NOT MET. RED 증거가 leaf 자기보고 TDD표로 대체 가능하게 적혔으면(I1 위반) NOT MET. codex 미러(T6)도 동일 규칙을 담는지 확인. 증거=인용한 RED 게이트 문장 |
| V6 | C6 | review (2등급 정성) | `implementation` SKILL(claude+codex) Step 6/7 fix 정책을 리뷰어가 읽어 "correctness finding=test-first(실패 테스트 먼저→fix), simplicity/refactor finding=직접 fix"가 명시됐는지 확인. 모든 finding을 test-first로 강제하거나 정책이 없으면 NOT MET. 증거=인용한 fix 정책 문장 |
| V7 | C7 | review (2등급 정성) | autopilot orchestrator-contract(claude+codex), `SKILL.md`(claude+codex), sample-orchestrator(claude+codex)를 리뷰어가 읽어 (a) canonical agent에 `test-author-agent` 추가, (b) dispatch controller가 wave별 test-author→RED 게이트→GREEN-전용 impl 반영(impl RED 자체 수행 안 함), (c) fix 정책 correctness-only test-first가 5 surface 전체에서 일관 갱신됐는지 확인. 한 surface라도 impl이 RED 자체 수행하는 옛 서술이 남으면 NOT MET. 증거=각 surface 인용 |
| V8 | C8 | test (1등급 정량) | `python3 -m json.tool .claude-plugin/marketplace.json`(exit 0) + `grep "test-author-agent.md" .claude-plugin/marketplace.json`(1+) + `grep "test-author-agent" .codex/agents/README.md`(1+). agents 배열 항목 수 = 10. 증거=명령 출력 |
| V9 | I5 | review (2등급 정성) + test (1등급 정량 보조) | (정성) claude/codex 미러 6쌍을 리뷰어가 대조: (1) `test-author-agent`(.md ↔ .toml), (2) `implementation-agent` GREEN 재정의(.md ↔ .toml), (3) `implementation` SKILL(claude ↔ codex), (4) orchestrator-contract(claude ↔ codex), (5) autopilot `SKILL.md`(claude ↔ codex), (6) sample-orchestrator(claude ↔ codex). 한 쌍이라도 계약 누락/불일치가 있으면 NOT MET. (정량 보조, #L2) 각 쌍의 핵심 계약 키워드(`CONTRACT_MISMATCH`, `RED 게이트`/`RED gate`, `test-author`, `BLOCKED`)가 .md/.toml(또는 claude/codex) 양쪽에 grep 1+ 존재 — 한쪽에만 있으면 미러 누락. 증거=불일치 지목 또는 "대응 확인" 인용 + grep 출력 |

## Parallel Execution Summary

| Phase | Tasks | 병렬 가능 | 충돌/dependency 근거 |
|-------|-------|-----------|----------------------|
| Phase 1 | T1, T2, T3, T4 | T1 ∥ T3 (2그룹), 이어서 T2(T1 후) ∥ T4(T3 후) | T1(신규 test-author)/T3(기존 impl-agent 수정)은 Target Files disjoint·dependency 없음 → 병렬. T2는 T1 본문에, T4는 T3 본문에 종속(codex 미러). T2 ∥ T4는 Target Files disjoint |
| Phase 2 | T5, T6 | 순차 | T5(claude implementation SKILL 개편)는 T1/T3 leaf 계약 소비. T6(codex 미러)은 T2/T4/T5에 종속 |
| Phase 3 | T7, T8, T9, T10 | T10은 T1 후 즉시(Phase 1/2와 독립 가능), T7→{T8 ∥ T9} | T7(orchestrator-contract claude)이 canonical home이라 선행. T8(contract codex + SKILL claude+codex)·T9(sample claude+codex)는 둘 다 T7 표기를 소비하고 Target Files disjoint → T7 후 병렬. T10(registry)은 T1만 필요하고 다른 Phase 3 task와 Target Files disjoint → 독립 |

> Cross-phase: Phase 2는 Phase 1 leaf 계약(T1/T3)을 소비하므로 Phase 1 후. Phase 3 autopilot 계약(T7~T9)은 implementation 스킬의 RED 게이트/2-stage 흐름(T5)을 계약 문서에 반영하므로 T5에 종속. T10(registry)은 T1 완료만 필요해 Phase 2와 독립적으로 진행 가능.

# Risks/Mitigations and Open Questions

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| R1: impl-agent가 CONTRACT_MISMATCH 대신 고정 테스트를 약화시켜 통과("약한 테스트 통과로 만세") | test-first가 형식만 남고 검증력 상실 | T3에서 "테스트 수정 금지" Hard Rule + CONTRACT_MISMATCH 전용 경로를 명시(I2). T5 RED 게이트 falsifiability 점검이 약한 테스트(import/collection-only 실패)를 사전 차단. V2 grep + V3 리뷰로 검증 |
| R2: test-author가 plan에 없는 계약을 발명해 impl이 통과 불가능한 테스트를 받음 | Stage B에서 CONTRACT_MISMATCH 빈발, wave 정체 | T1에서 "계약 발명 금지, plan(AC/`V*`/Contract Delta) 근거로만 작성"을 Hard Rule로 명시. test-author 출력의 "가정한 인터페이스 계약"을 impl이 받아 mismatch를 조기 표면화. orchestrator가 test-author 재dispatch로 수렴 |
| R3: 2-stage 파이프라인으로 wave당 dispatch가 2배(test-author + impl) → 토큰/벽시계 증가 | gate당 비용 증가, multi-wave에서 누적 | wave 내부는 각 stage 병렬 유지(벽시계는 max(병렬 leaf)). cross-wave 중첩을 도입하지 않아 스케줄러 복잡도는 억제(YAGNI). 트레이드오프는 test-first 검증력 확보를 위한 수용 비용 |
| R4: 프레임워크 없는 이 repo(마크다운/스킬)에서 RED 게이트가 항상 UNTESTED로 빠져 무력화 | test-first 강제가 메타 repo 자체엔 적용 안 됨 | I4 graceful degradation — test-author가 grep/구조 점검 acceptance check를 RED artifact로 쓰고 RED 게이트가 현재 미충족을 확인. `_sdd/env.md` 부재 시에만 UNTESTED 경로. V5 리뷰로 acceptance check RED 경로 존재 확인 |
| R5: claude/codex 6쌍 미러 중 일부 누락으로 플랫폼 parity 깨짐 | codex 경로에서 test-author/RED 게이트 미작동 | I5를 V9 전용 검증으로 분리해 6쌍 전수 대조. task마다 codex 미러를 명시 AC로 고정 |
| R6: autopilot orchestrator-contract의 "단일 task만 TDD로 수행"(impl RED 전제) 잔존 서술이 5 surface에 흩어져 일부만 갱신 | generated orchestrator가 옛 impl-RED 모델로 생성 | T7(contract canonical home) 선행 + T8/T9가 T7 표기 복사. V7이 5 surface 전체에서 "impl RED 자체 수행" 잔존 0건을 점검 |

## Open Questions

### Q1. test-author와 impl을 별도 agent로 분리할지, 단일 agent의 mode 분기로 둘지
- **Decision taken**: 별도 leaf agent로 분리한다(`test-author-agent` 신규 + `implementation-agent` GREEN 전용). 설계 결정(Contract/Invariant Delta·`V*`)이 plan에서 상류 확정되므로 두 leaf는 같은 pinned 계약을 실행만 하고 co-evolution 손실이 작다("상류 결정, 하류 실행"). 분리해야 orchestrator RED 게이트를 두 stage 사이에 강제로 끼울 수 있다.
- **Alternatives considered**: (a) impl-agent에 `mode=test|impl` 분기 — 단일 파일이지만 RED 게이트를 두 호출 사이에 끼우려면 결국 orchestrator가 2회 dispatch해야 해 분리와 실행 동형이고, 한 agent가 "테스트 작성"과 "테스트 수정 금지"를 동시에 보유해 계약 충돌. 기각. (b) orchestrator가 인라인으로 테스트 작성 — leaf 분리(nesting/단일 작성자) 모델 위반. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. RED 게이트 falsifiability 점검을 별도 test-review agent로 둘지, orchestrator 게이트에 접을지
- **Decision taken**: 기존 orchestrator RED 게이트에 접는다(별도 agent 미신설). falsifiability 점검(AC 관찰동작 검증 & `V*` 1:1 & import/collection-only 실패 배제)은 RED 증거 캡처와 같은 지점에서 수행되는 경량 판정이라 별도 agent의 dispatch/계약 오버헤드가 정당화되지 않는다(right-sizing).
- **Alternatives considered**: 신규 `test-review-agent` — 매 wave마다 reviewer dispatch 추가로 토큰/복잡도가 늘고, RED 게이트가 이미 테스트를 실행해 증거를 캡처하므로 같은 자리에서 점검 가능. YAGNI로 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. wave 간 파이프라인 중첩(wave G impl ∥ wave H 테스트 작성)을 허용할지
- **Decision taken**: 허용하지 않는다(wave 내부만 파이프라인, wave 간 순차). cross-wave 중첩은 prose 기반 orchestration에 스케줄러 상태(어느 wave가 어느 stage인지) 복잡도만 키우는 speculative 최적화다.
- **Alternatives considered**: cross-wave 중첩으로 벽시계 단축 — 실측 병목은 작성(추론)이지 dispatch 왕복이 아니므로(메모리 sdd-orchestration-speed) 중첩 이득이 작고 복잡도 비용이 크다. YAGNI로 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q4. `_sdd/spec/*` 동기화(main/components/decision_log/changelog)를 이 plan의 구현 task로 넣을지
- **Decision taken**: 구현 task에 넣지 않는다. implementation leaf는 spec 파일 불가침이고, persistent spec 반영은 구현 완료 후 `spec-sync`가 Part 1(spec-update-todo 마커 내부)을 입력으로 수행한다. 전파 census의 spec surface 4파일은 spec-sync의 대상이며 이 draft Target Files(=구현 leaf 쓰기 경계)에서는 제외한다.
- **Alternatives considered**: spec 4파일을 Target Files에 포함 — Hard Rule 1(spec 읽기 전용) + main.md Guardrails(implementation leaf spec 불가침) 위반. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q5. impl-agent에서 RED를 제거하면 impl을 스킬 미경유로 직접 호출하는 경로가 test-after로 퇴화하는지
- **Decision taken**: 직접 호출(스킬 미경유, 고정 테스트/RED 증거 입력 없음) 경로를 **계약상 비지원**으로 명시하고, 잔여 위험은 **집행으로 닫는다**. impl-agent 재정의(T3/T4)에 "이 leaf는 항상 고정 테스트 + RED 증거를 입력으로 받는 orchestrated 경로(`implementation` 스킬/autopilot)에서만 호출되며, 입력에 고정 테스트/RED 증거가 없으면 자체 RED(테스트) 작성을 금지하고 입력 누락을 `BLOCKED`로 보고한다"를 AC로 박았다(#M2). self-RED fallback 분기는 도입하지 않는다 — 이로써 직접 호출 경로에서도 test-after 재개방이 닫힌다. implementation 스킬은 항상 Stage A→RED 게이트→Stage B를 거치므로(T5) 정상 경로에서 입력 누락은 발생하지 않는다.
- **Alternatives considered**: (a) impl-agent에 RED fallback(테스트 없으면 자체 작성) 유지 — "테스트 수정 금지"·GREEN 전용 계약과 충돌하고 저항 최소 경로(impl 자기 테스트 작성=test-after)를 재개방해 개편 목적 무효화. 기각. (b) 결정을 미루고 구현 전 사용자 확인만 받음 — 집행(입력 누락→`BLOCKED`)이 framing과 무관하게 위험을 닫으므로 구현을 블록할 이유 없음. AC 집행으로 진행하되 "직접 호출 = 계약상 비지원" framing 자체는 사용자 확인 항목으로 남긴다.
- **Confidence**: HIGH (잔여 위험은 T3/T4 AC 집행으로 닫힘)
- **User confirmation needed**: Yes ("직접 호출 경로를 계약상 비지원으로 둔다"는 framing 확정 — 집행은 이미 plan에 박혀 구현 진행을 막지 않음)
