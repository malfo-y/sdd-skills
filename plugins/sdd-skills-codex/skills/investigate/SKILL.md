---
name: investigate
description: "Use this skill when the user asks to \"investigate\", \"debug\", \"find root cause\", \"diagnose\", \"why is this failing\", \"track down bug\", \"근본원인 분석\", \"디버깅\", or wants systematic one-shot diagnosis or an explicitly authorized fix for a specific issue. For long-running iterative debugging processes, use ralph-loop-init instead."
---

# Investigate — Systematic Debugging (Orchestrator)

범용 체계적 디버깅 스킬. 증상이 아닌 근본원인을 증거로 확인하고, 사용자가 명시적으로 수정을 요청한 경우에만 fix와 검증까지 수행한다. **메인 루프 orchestrator**로 실행되어, 탐색이 넓고·모호할 때만 read-only `explorer` 역할을 병렬 spawn하고(증거 수집·가설 검증 가속), 문제정의·근본원인 종합·영향 범위 분석과 승인된 fix·검증은 인라인으로 직접 수행한다.

> ralph-loop-init과 차별화: investigate는 범용/단발 디버깅, ralph-loop-init은 장시간 반복 프로세스 전용.

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 Step 2의 조건부 `explorer` dispatch 범위에 대한 사용자 요청으로 처리한다. 단, AC5에 따라 탐색이 넓고·모호할 때만 fan-out한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

dispatch 전 active tool schema에서 lifecycle contract 하나를 선택한다. Mailbox(Desktop/current CLI: `task_name`/`fork_turns`가 필요하거나 wait에 `targets` 없음)는 invocation마다 짧은 lowercase `run_id`를 만들고 같은 parent tree의 재실행까지 고유한 `task_name`에 넣은 뒤, `fork_turns: "none"`, `message`로 spawn한다. target 없는 wait를 반복하며 완료 agent를 닫지 않는다. Target/close(legacy CLI schema: wait에 `targets` 지원 + `close_agent` 노출)는 `message` spawn, target wait, 완료 handle close를 사용한다. `agent_type`은 선택적 role selector다 — active schema가 `"explorer"` 값을 지원할 때만 spawn payload에 추가하고, 없으면 read-only 탐색 계약을 `message`에 직접 넣어 일반 sub-agent를 사용한다. 실행 surface 이름이 아니라 schema로 lifecycle을 선택한다. lifecycle contract가 불완전하거나 모호하면 fan-out하지 않고 인라인 순차 탐색으로 graceful degrade한다. `agent_type` 부재만으로는 degrade하지 않으며, 없는 lifecycle tool을 `tool_search`로 찾거나 두 contract를 혼용하지 않는다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

```text
Mailbox: spawn_agent({task_name: "investigate_r7f3a_error_path", fork_turns: "none", message: "<구체적 read-only 탐색 질문 + read-only 경계>"})  // r7f3a는 invocation마다 교체
Mailbox: wait_agent({timeout_ms: 600000})  // remaining이 빌 때까지 반복, close 없음
Target/close: spawn_agent({message: "<구체적 read-only 탐색 질문 + read-only 경계>"})
Target/close: wait_agent({targets: ["<agent_id>"], timeout_ms: 600000}) → final 기록 → close_agent({target: "<완료 agent_id>"})
```

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 근본원인이 증거와 함께 식별되었다 (근거 부족이면 `UNCONFIRMED`로 보고)
- [ ] AC2: diagnose-only mode에서는 제품·소스·spec fix와 회귀 테스트 추가가 0건이며, 상위 repo 규칙이 강제한 governance 기록이 있으면 보고에 공개했다
- [ ] AC3: fix mode에서는 수정 전 blast radius를 평가하고, 근본원인 수정 후 fresh verification을 실행했다
- [ ] AC4: 초기 범위를 벗어나는 분석·수정이 없다 (scope lock)
- [ ] AC5: 탐색 fan-out은 넓고·모호할 때만 사용했고, 단순 버그는 인라인 순차로 처리했다 (불필요한 fan-out 없음)

## Hard Rules

1. **근본원인 우선 (Iron Law)**: 증상 패치 금지. 근본원인을 증거로 확인한 뒤 diagnose-only report 또는 승인된 fix로 이어간다.
2. **3-Strike Escalation**: 같은 접근 3회 실패 시 전략을 변경한다 (다른 가설, 다른 도구, 다른 범위).
3. **Scope Lock**: 초기 범위(사용자가 지정한 문제)를 벗어나는 수정 금지. 발견한 추가 이슈는 리포트에 기록만 한다.
4. **Blast Radius Gate (fix mode)**: 수정 전 영향 범위를 평가한다. 변경 파일 수, 의존하는 모듈, 관련 테스트를 나열하고 수정을 진행한다.
5. **Fresh Verification (fix mode)**: 수정 후 반드시 테스트를 재실행한다. 이전 결과 재사용 금지. `_sdd/env.md` 미존재 시 코드 분석 기반 검증을 허용하되, 리포트에 `UNTESTED` 표기.
6. **Spec 파일 불가침**: `_sdd/spec/` 하위 파일을 생성/수정/삭제하지 않는다.
7. **Fix Authority**: 명시적 `fix`·`repair`·`patch`·`수정해줘`·`고쳐줘` 또는 후속 승인만 fix mode 권한이다. `investigate`·`debug`·`diagnose`처럼 불명확한 요청은 diagnose-only가 기본이며 권고만으로 write 권한을 추론하지 않는다.
8. **Diagnose-only Write Boundary**: 제품·소스·spec 파일 생성·수정·삭제와 회귀 테스트 추가를 금지한다. 상위 repo 규칙이 명시적으로 강제하는 work-log 같은 governance 기록만 예외이며 최종 보고에 공개한다. 예외 쓰기도 그 규칙의 최소 대상과 연산 의미를 그대로 지킨다(예: append 요구이면 기존 내용을 보존하고 append만 한다).
9. **fix는 인라인(write)**: fix mode의 write와 Fresh Verification은 orchestrator가 메인 루프에서 직접 수행한다. 탐색 fan-out의 `explorer` 역할은 항상 read-only다.

## Process

### Step 1: Problem Definition (인라인, 대화 기반)

1. 사용자 입력·대화에서 증상, 재현 조건, 기대 동작, 이미 시도한 가설을 추출한다. (이 입력은 대화에서 태어나므로 sub-agent가 못 읽는다 — orchestrator가 직접 정리한다.)
2. `_sdd/env.md` 존재 시 환경 설정을 적용한다.
3. 문제 범위를 확정하고 기록한다 (scope lock 기준).
4. intent를 기록한다.
   - 조사 대상 제품·소스의 fix·repair·patch·수정을 명시적으로 요청했으면 **fix mode**. 진단 보고서·분석 산출물을 파일로 작성해 달라는 요청은 제품 fix 권한이 아니다.
   - 그 외(`investigate`·`debug`·`diagnose`·원인 설명 포함)는 **diagnose-only mode**가 safe default다.
   - diagnose-only 진행 중 사용자가 후속으로 fix를 승인하면 기존 evidence를 유지한 채 fix mode로 전환한다. 승인 전에는 전환하지 않는다.

### Step 2: Evidence & Hypothesis (조건부 explorer 병렬 spawn)

기본은 **인라인 순차 증거 수집**이다: 에러 메시지·스택 트레이스·관련 코드 경로·최근 변경(`git log`/`git diff`)·관련 테스트를 수집하고 가설을 세운다.

**넓고·모호할 때만**(경쟁 가설이 여럿 / 출처가 불분명 / 탐색 범위가 큼) read-only explorer 역할을 **병렬 spawn**한다. 각 lane의 task/agent 식별자를 remaining set으로 관리하고, 선택한 Runtime Adapter가 final status를 반환한 explorer만 핵심 사실을 기록한 뒤 제거한다. timeout은 완료로 간주하지 않으며, remaining이 빌 때까지 더 기다리거나 controlled stop/blocked 상태를 기록한다. lane은 케이스에 맞게 선택한다 (리지드 분기 없음):

- **가설-lane** (anti-anchoring): 경쟁 가설을 lane별로 분리해 각 explorer가 독립적으로 한 가설을 검증 + 가설 없는 독립 탐지 lane 1개를 둬 앵커링 바이어스를 막는다.
- **영역-lane** (broad sweep): 코드 영역·증거 출처(에러 경로 / 최근 변경 / 의존·설정 / 테스트)별로 explorer가 동시 sweep한다.

런타임에 `explorer` 역할이 미가용하면 **순차 인라인 증거 수집으로 graceful degrade**한다(정확성 동일, 병렬만 상실). **단순 단일파일 버그·명확한 에러는 fan-out 없이 인라인 순차**로 진행한다(불필요한 fan-out 회피).

### Step 3: Root Cause Synthesis (인라인)

인라인 증거와 (있다면) explorer lane 결과를 **교차 비교**해 근본원인을 종합한다. 가설 기반 결론과 독립 탐지 결론이 불일치하면 추가 증거를 수집한다. 같은 가설/접근이 3회 실패하면 즉시 전략을 변경한다(3-Strike).

### Step 4: Impact / Blast Radius Assessment (인라인)

영향 가능 범위를 평가한다: 관련 파일, 의존 모듈/함수(import/호출 검색), 관련 테스트와 위험 표면.

- **diagnose-only**: 영향 가능 범위와 권고만 기록하고 제품 변경 계획을 실행하지 않는다.
- **fix mode**: 실제 변경 대상 파일을 고정하고 Blast Radius Gate를 통과한 뒤 Step 5로 간다.

### Step 5: Fix & Verify (fix mode only, 인라인, write)

diagnose-only mode는 이 단계를 건너뛰고 Step 6으로 간다. fix mode에서만 다음을 수행한다.

1. 근본원인을 수정한다 (orchestrator가 직접 — explorer는 read-only라 write 불가).
2. 테스트를 재실행해 수정을 검증한다 (Fresh Verification).
3. 기존 테스트가 실패하면 회귀 방지 테스트를 추가한다.

### Step 6: Report

아래 field name을 그대로 사용하고 선택한 mode의 값 하나만 기록한다. field name을 번역·축약하거나 Markdown 강조를 제거하지 않는다.

```markdown
## Investigation Report

**Mode**: diagnose-only | fix
**Problem**: [1문장 요약]
**Root Cause**: [근본원인]
**Evidence**: [근본원인 근거]
**Fix**: [선택한 mode에 맞는 값]
**Impact / Blast Radius**: [영향 범위]
**Verification**: [선택한 mode에 맞는 값]
**Governance Writes**: None | [상위 repo 규칙이 강제한 기록]
**Out-of-Scope Findings**: [범위 밖 발견사항, 있는 경우]
```

| Mode | Fix | Verification |
| --- | --- | --- |
| diagnose-only | `Not applied (diagnose-only)` | `CONFIRMED` 또는 `UNCONFIRMED` |
| fix | 수정 내용 + 파일:라인 | `PASS`, `FAIL`, 또는 `UNTESTED` |

## Final Check

선택한 mode에 적용되는 Acceptance Criteria가 모두 만족되었나 검증한다. diagnose-only에서 AC3의 fix 조건은 적용하지 않고, fix mode에서 AC2의 no-fix 조건은 적용하지 않는다. 미충족 항목이 있으면 해당 단계로 돌아간다.

> **Role Pointer**: 이 스킬은 메인 루프 orchestrator다. 탐색 fan-out 단위는 빌트인 범용 read-only `explorer` 역할을 선택한 runtime contract로 재사용하며 별도 custom leaf agent를 두지 않는다. (구 `investigate_agent`는 제거됨 — 전체 디버깅 계약을 이 skill이 인라인 소유한다.)
