---
name: investigate
description: "Use this skill when the user asks to \"investigate\", \"debug\", \"find root cause\", \"diagnose\", \"why is this failing\", \"track down bug\", \"근본원인 분석\", \"디버깅\", or wants systematic one-shot debugging of a specific issue. For long-running iterative debugging processes, use ralph-loop-init instead."
version: 4.0.0
---

# Investigate — Systematic Debugging (Orchestrator)

범용 체계적 디버깅 스킬. 증상이 아닌 근본원인을 찾아 수정하고, 수정이 올바른지 검증한다. **메인 루프 orchestrator**로 실행되어, 탐색이 넓고·모호할 때만 read-only `explorer` 역할을 병렬 spawn해(증거 수집·가설 검증 가속), 나머지 전 단계(문제정의·근본원인 종합·Blast Radius·fix·검증)는 인라인으로 직접 수행한다.

> ralph-loop-init과 차별화: investigate는 범용/단발 디버깅, ralph-loop-init은 장시간 반복 프로세스 전용.

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 Step 2의 조건부 `explorer` dispatch 범위에 대한 사용자 요청으로 처리한다. 단, AC5에 따라 탐색이 넓고·모호할 때만 fan-out한다. dispatch 전에 `spawn_agent`, `wait_agent`, `close_agent`가 active tools에 없으면 `tool_search` query `spawn_agent wait_agent close_agent multi-agent sub-agent`로 multi-agent tools를 먼저 로드한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

```text
spawn_agent({agent_type: "explorer", message: "<구체적 read-only 탐색 질문>"})
wait_agent({targets: ["<agent_id>"], timeout_ms: 600000})
close_agent({target: "<agent_id>"})
```

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 근본원인이 식별되었다 (증상 패치가 아닌 원인 수정)
- [ ] AC2: 수정 후 테스트가 통과한다 (Fresh Verification)
- [ ] AC3: 수정 영향 범위(blast radius)가 사전 평가되었다
- [ ] AC4: 초기 범위를 벗어나는 수정이 없다 (scope lock)
- [ ] AC5: 탐색 fan-out은 넓고·모호할 때만 사용했고, 단순 버그는 인라인 순차로 처리했다 (불필요한 fan-out 없음)

## Hard Rules

1. **근본원인 우선 (Iron Law)**: 증상 패치 금지. 근본원인을 찾아 수정한다.
2. **3-Strike Escalation**: 같은 접근 3회 실패 시 전략을 변경한다 (다른 가설, 다른 도구, 다른 범위).
3. **Scope Lock**: 초기 범위(사용자가 지정한 문제)를 벗어나는 수정 금지. 발견한 추가 이슈는 리포트에 기록만 한다.
4. **Blast Radius Gate**: 수정 전 영향 범위를 평가한다. 변경 파일 수, 의존하는 모듈, 관련 테스트를 나열하고 수정을 진행한다.
5. **Fresh Verification**: 수정 후 반드시 테스트를 재실행한다. 이전 결과 재사용 금지. `_sdd/env.md` 미존재 시 코드 분석 기반 검증을 허용하되, 리포트에 `UNTESTED` 표기.
6. **Spec 파일 불가침**: `_sdd/spec/` 하위 파일을 생성/수정/삭제하지 않는다.
7. **fix는 인라인(write)**: 탐색 fan-out에 쓰는 `explorer` 역할은 read-only다. 근본원인 종합·Blast Radius·fix(write)·Fresh Verification은 orchestrator가 메인 루프에서 직접 수행한다.

## Process

### Step 1: Problem Definition (인라인, 대화 기반)

1. 사용자 입력·대화에서 증상, 재현 조건, 기대 동작, 이미 시도한 가설을 추출한다. (이 입력은 대화에서 태어나므로 sub-agent가 못 읽는다 — orchestrator가 직접 정리한다.)
2. `_sdd/env.md` 존재 시 환경 설정을 적용한다.
3. 문제 범위를 확정하고 기록한다 (scope lock 기준).

### Step 2: Evidence & Hypothesis (조건부 explorer 병렬 spawn)

기본은 **인라인 순차 증거 수집**이다: 에러 메시지·스택 트레이스·관련 코드 경로·최근 변경(`git log`/`git diff`)·관련 테스트를 수집하고 가설을 세운다.

**넓고·모호할 때만**(경쟁 가설이 여럿 / 출처가 불분명 / 탐색 범위가 큼) read-only explore 역할을 **병렬 spawn**한다: `spawn_agent({agent_type: "explorer", message: <구체적 read-only 탐색 질문>})`를 여러 개 띄우고 반환된 agent ids를 remaining set으로 관리한다. `wait_agent({targets: remaining, timeout_ms: 600000})`가 final status를 반환한 explorer만 핵심 사실을 기록한 뒤 `close_agent({target: <agent_id>})`로 닫고 remaining에서 제거한다. timeout은 완료로 간주하지 않으며, remaining이 빌 때까지 더 기다리거나 controlled stop/blocked 상태를 기록한다. lane은 케이스에 맞게 선택한다 (리지드 분기 없음):

- **가설-lane** (anti-anchoring): 경쟁 가설을 lane별로 분리해 각 explorer가 독립적으로 한 가설을 검증 + 가설 없는 독립 탐지 lane 1개를 둬 앵커링 바이어스를 막는다.
- **영역-lane** (broad sweep): 코드 영역·증거 출처(에러 경로 / 최근 변경 / 의존·설정 / 테스트)별로 explorer가 동시 sweep한다.

런타임에 `explorer` 역할이 미가용하면 **순차 인라인 증거 수집으로 graceful degrade**한다(정확성 동일, 병렬만 상실). **단순 단일파일 버그·명확한 에러는 fan-out 없이 인라인 순차**로 진행한다(불필요한 fan-out 회피).

### Step 3: Root Cause Synthesis (인라인)

인라인 증거와 (있다면) explorer lane 결과를 **교차 비교**해 근본원인을 종합한다. 가설 기반 결론과 독립 탐지 결론이 불일치하면 추가 증거를 수집한다. 같은 가설/접근이 3회 실패하면 즉시 전략을 변경한다(3-Strike).

### Step 4: Blast Radius Assessment (인라인)

수정 대상 파일과 영향 범위를 평가한다: 변경 파일 목록, 의존 모듈/함수(import/호출 검색), 관련 테스트.

### Step 5: Fix & Verify (인라인, write)

1. 근본원인을 수정한다 (orchestrator가 직접 — explorer는 read-only라 write 불가).
2. 테스트를 재실행해 수정을 검증한다 (Fresh Verification).
3. 기존 테스트가 실패하면 회귀 방지 테스트를 추가한다.

### Step 6: Report

```markdown
## Investigation Report

**Problem**: [1문장 요약]
**Root Cause**: [근본원인]
**Fix**: [수정 내용 + 파일:라인]
**Blast Radius**: [영향 범위]
**Verification**: PASS / FAIL / UNTESTED
**Out-of-Scope Findings**: [범위 밖 발견사항, 있는 경우]
```

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Role Pointer**: 이 스킬은 메인 루프 orchestrator다. 탐색 fan-out 단위는 빌트인 범용 read-only `explorer` 역할(`spawn_agent({agent_type: "explorer", message: ...})`)을 재사용하며 별도 custom leaf agent를 두지 않는다. (구 `investigate_agent`는 제거됨 — 전체 디버깅 계약을 이 skill이 인라인 소유한다.)
