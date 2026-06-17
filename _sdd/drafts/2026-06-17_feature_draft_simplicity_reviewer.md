# Feature Draft: Simplicity Reviewer (직교 렌즈 병렬 review 아키텍처)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

모든 implementation review-gate를 단일 reviewer(`implementation-review-agent`)에서 **직교 두 렌즈 reviewer 병렬 dispatch**로 확장한다. 신규 `simplicity-review-agent`(read-only leaf)가 correctness reviewer와 매 gate에서 함께 dispatch되어, correctness(AC/버그/보안/spec drift)와 직교하는 **동작-불변 형태 품질**(중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축)을 리뷰한다.

동기: 앤트로픽 pr-review-toolkit의 code-simplifier(코드를 직접 고치는 reviewer-editor)를 이 repo의 단일 작성자 불변식(reviewer는 자기 리포트만 쓰고 code/plan/spec을 수정하지 않는다)에 맞게 "리뷰만 하는" 형제 agent로 번역한다. 직접 고치는 대신 finding을 내고, 기존 fix 경로(`implementation-agent` 재dispatch)가 처리한다.

## Scope Delta

### In-scope (delta)
- `simplicity-review-agent` 도입: read-only leaf reviewer. correctness reviewer와 동등한 구조(AC/Hard Rules/Process/Output Format/Re-review Mode/findings-first severity)를 형제 agent로 따른다.
- review-gate dispatch 모델 변경: 단일 reviewer → **correctness ∥ simplicity 병렬 2-reviewer**. 적용 범위는 implementation-scoped review-gate(producer `implementation` 스킬의 phase/final gate, autopilot의 global/per-group/final-integration gate)다.
- gating exit 조건 변경: **두 report의 합집합** `critical=high=medium=0`.
- 표적 disjoint: `Speculative Code` 차원을 correctness reviewer에서 simplicity reviewer로 **이관**. correctness=정확성, simplicity=동작-불변 형태.

### Out-of-scope (delta)
- `spec-review` gate는 승급하지 않는다. simplicity 렌즈는 코드 형태 품질이라 spec 문서 품질에 부적합하다.
- fix 경로 자체는 변경하지 않는다. 기존 `implementation-agent` 순차 fix dispatch를 그대로 재사용한다(두 report finding을 합산해 순차 dispatch).
- simplicity 전용 wrapper skill은 도입하지 않는다. `implementation-review` 스킬을 2-reviewer orchestrator(review-only)로 승격하는 것으로 충분하다.

### Guardrail delta
- 단일 작성자 불변식 유지: simplicity reviewer도 자기 리포트만 쓰고 code/plan/spec을 수정하지 않는다(correctness reviewer와 동일 제약).
- nesting 1단계 제한 유지: simplicity reviewer는 read-only leaf이며 sub-agent를 spawn하지 않는다.
- 병렬 안전성: 두 reviewer 모두 read-only leaf라 동시 dispatch가 충돌 없이 안전하다. 벽시계는 max(둘)≈1 reviewer, 토큰 비용만 증가한다(사용자 명시 수용).

## Persistent Spec Implications

persistent spec(`_sdd/spec/main.md` Guardrails / 주요 결정)에 남아야 하는 계약:

- **직교 2-렌즈 review 계약**: implementation-scoped review-gate는 correctness reviewer와 simplicity reviewer를 병렬 dispatch한다. 두 reviewer는 read-only leaf이며 표적이 disjoint하다(correctness=정확성/AC/버그/보안/spec drift, simplicity=동작-불변 형태: 중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축). gating exit는 두 report 합집합 `critical=high=medium=0`.
- **falsifiable-only gating 불변식**: simplicity finding 중 객관적으로 반증 가능한 위반만 Medium 이상(gating)이고, 주관적 취향은 Low(advisory)다. 병렬화는 벽시계만 줄이고 수렴은 보장하지 않으므로, gating을 falsifiable finding으로 한정하는 규칙이 수렴성의 핵심이다.
- **fix 경로 단일성**: 두 reviewer의 finding은 합산되어 기존 단일 fix 경로(`implementation-agent` 순차 재dispatch)로 처리된다. simplicity reviewer는 코드를 직접 수정하지 않는다(단일 작성자 불변식).
- **simplicity는 implementation review 한정**: simplicity 렌즈는 `spec-review`로 확장하지 않는다.
- **autopilot agent 매핑 확장**: review-fix gate의 agent 매핑이 단일 reviewer 고정에서 "correctness + simplicity 2-reviewer 병렬" 고정으로 확장된다. canonical agent set에 `simplicity-review-agent`가 추가된다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

이 plan은 Part 1의 직교 2-렌즈 review 계약을 6개 surface에 일관되게 구현한다: 신규 `simplicity-review-agent`(claude+codex), correctness reviewer 경량화(Speculative Code 이관), `implementation-review` 스킬의 2-reviewer orchestrator(review-only) 승격, `implementation` 스킬의 gate 확장, autopilot single-reviewer 고정(`SKILL.md` 5곳: Hard Rule 5 / Step 4 / Step 7.2 / per-group gate / Step 7.3 + 결정적 게이트키퍼 `validate_orchestrator.py`) + contract §6 + sample-orchestrator 갱신, codex 미러 정합.

`validate_orchestrator.py`(claude+codex)는 **결정적 게이트키퍼**다: 이 스크립트의 `mapping_specs`가 단일 reviewer만 허용하면, 2-reviewer 매핑을 선언한 orchestrator를 autopilot Step 5.1에서 reject한다. 따라서 스크립트 수정이 다른 autopilot 매핑 갱신(Step 4/Step 7.3/Hard Rule 5/contract §6/sample)의 선행 dependency다.

## Scope

### In Scope
- `.claude/agents/simplicity-review-agent.md` 신규 생성, `.codex/agents/simplicity-review-agent.toml` 신규 생성
- `.claude/agents/implementation-review-agent.md` + `.codex/agents/implementation-review-agent.toml`: Speculative Code 차원 제거(이관)
- `.claude/skills/implementation-review/SKILL.md` + `.codex/skills/implementation-review/SKILL.md`: wrapper → 2-reviewer orchestrator(review-only)
- `.claude/skills/implementation/SKILL.md` + `.codex/skills/implementation/SKILL.md`: Step 6 phase gate / Step 7 final gate가 두 reviewer 병렬 dispatch + 합집합 exit
- `.claude/skills/sdd-autopilot/scripts/validate_orchestrator.py` + `.codex/...`: 2-reviewer 매핑 허용
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` + `.codex/...`: §6 + canonical agent set 갱신
- `.claude/skills/sdd-autopilot/SKILL.md` + `.codex/...`: Hard Rule 5 / Step 4 / Step 7.3 미러 갱신
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` + `.codex/...`: review-fix gate 예시 갱신
- `.codex/agents/README.md`: Agent Set + Inline Writing 목록에 `simplicity-review-agent` 추가

### Out of Scope
- `spec-review` 스킬/에이전트 변경 (Part 1 out-of-scope)
- fix 경로(`implementation-agent`) 변경 — 단, REFACTOR Hard Rule의 "clarity over brevity" 한 줄은 이번 세션에 선행 완료(R5 참조)
- 신규 simplicity 전용 wrapper skill (불필요 — `implementation-review` orchestrator 승격으로 충족)

## Contract/Invariant Delta and Coverage

| ID | Type | Change | Covered By | Validated By |
|----|------|--------|------------|--------------|
| C1 | Add | `simplicity-review-agent`(read-only leaf, re-review mode 포함)가 correctness reviewer와 형제 구조(AC/Hard Rules/Process/Output/Re-review/findings-first)로 존재한다 | T1, T2 | V1 |
| C2 | Modify | correctness reviewer에서 `Speculative Code` 차원을 제거한다 (simplicity로 이관 — 표적 disjoint) | T3, T4 | V2 |
| C3 | Add | implementation-scoped review-gate는 correctness ∥ simplicity를 병렬 dispatch하고 exit는 두 report 합집합 `critical=high=medium=0` | T5, T6 | V3 |
| C4 | Add | `implementation-review` 스킬이 2-reviewer 병렬 dispatch + 두 report 경로/합산 요약 relay까지 수행하는 review-only orchestrator다 (fix loop 미소유) | T5, T6 | V4 |
| C5 | Modify | autopilot review-fix gate 매핑이 `review` 단일에서 correctness+simplicity 2-reviewer 병렬로 확장된다 (contract §6 + SKILL 5곳 + sample 일관) | T9, T10, T11 | V5, V6 |
| C6 | Modify | `validate_orchestrator.py`가 2-reviewer 매핑을 PASS로 통과시키고, canonical agent set에 `simplicity-review-agent`를 포함한다 | T8 | V6 |
| I1 | Add | falsifiable-only gating: 객관적 위반(중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축)=Medium=gating, 주관적 취향=Low=advisory | T1, T2 | V1, V7 |
| I2 | Invariant | 단일 작성자 불변식 유지 — simplicity reviewer는 자기 리포트만 쓰고 code/plan/spec을 수정하지 않으며 sub-agent를 spawn하지 않는다 | T1, T2 | V1 |
| I3 | Invariant | claude/codex 미러 정합 — 6개 surface의 두 플랫폼 표현이 동일 계약을 담는다 | T2, T4, T6, T8, T10, T11 | V8 |

## Touchpoints

현재 코드 기준으로 재확인한 변경 지점 (각 항목은 read로 검증함):

- **`.claude/agents/implementation-review-agent.md`** — AC6/AC7, Hard Rule 11(Recommendations Min-Code), Step 5 Assessment의 Tier 1/2/3 `Speculative Code` bullet, Step 6 Findings Classification의 "Speculative Code ... 기본 분류"와 escalation이 correctness reviewer에 Speculative Code를 묶고 있다. 이관 대상이다. (codex: 동일 본문이 `.toml`의 `developer_instructions`에 Hard Rule 번호만 다르게 미러됨 — claude=11, codex=10)
- **`.claude/skills/implementation-review/SKILL.md`** — 현재 v5.0.0 thin entrypoint wrapper. 단일 `implementation-review-agent`만 dispatch한다. 2-reviewer 병렬 dispatch + relay로 승격 대상. (codex: `Codex Runtime Adapter` + `spawn_agent`/`wait_agent`/`close_agent` 호출 표현)
- **`.claude/skills/implementation/SKILL.md`** — Step 6 "Phase Review-Fix Gate (외부 reviewer loop)"의 `review`/`re-review`가 단일 `implementation-review-agent` 호출이다(L197-201). Step 7 "Final Cross-Phase Review-Fix Gate"도 동일(L216-221). 둘 다 2-reviewer 병렬 + 합집합 exit로 확장. Step 6 끝 "Speculative Code ... reviewer가 finding으로 분류"(L202)는 simplicity reviewer 소관으로 갱신.
- **`.claude/skills/sdd-autopilot/scripts/validate_orchestrator.py`** — `ALLOWED_BASE_AGENTS`(L19-29)에 `simplicity-review-agent` 없음. `mapping_specs`(L116-120)가 `review`/`fix`/`re-review`를 정확히 하나의 agent에 1:1로 강제하고, `role_match`가 `re.search`로 첫 매칭만 본다. 2-reviewer를 표현하려면 매핑 모델 확장 필요. **결정적 게이트키퍼** — 미수정 시 autopilot Step 5.1 reject.
- **`.claude/skills/sdd-autopilot/references/orchestrator-contract.md`** — §2 허용 `subagent_type` 목록(L47-55), §6 agent mapping(L128), Planning Producer Review Gate. canonical agent set + §6 매핑 확장.
- **`.claude/skills/sdd-autopilot/SKILL.md`** — `implementation-review-agent` 단일 reviewer 고정이 5곳에 있다: Hard Rule 5(L57), Step 4 reasoning(L180), Step 7.2 dispatch controller 서술(L258), per-group review-fix gate 본문(L265), Step 7.3 매핑(L273). 5곳 모두 2-reviewer 병렬로 갱신. 이 5곳에 더해 결정적 게이트키퍼인 validate 스크립트(T8)가 고정 surface다.
- **`.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`** — Example A `agent_mapping`/`execution_sequence`(L90-91), Example B `agent_mapping`/`execution_sequence_per_group`/`final integration review`(L268-289). 2-reviewer 병렬 표현으로 갱신.
- **`.codex/agents/README.md`** — `Agent Set`(L21-29), `Inline Writing`(L35-39) 목록에 `simplicity-review-agent` 추가.

## Implementation Phases

### Phase 1: Reviewer agents (신규 + 경량화)
신규 simplicity reviewer를 만들고 correctness reviewer에서 Speculative Code를 이관한다. 두 reviewer 본문이 이후 모든 orchestration surface의 계약 기준이 되므로 먼저 고정한다.

| Task | 목적 | Dependencies |
|------|------|--------------|
| T1 | `simplicity-review-agent.md`(claude) 신규 생성 | - |
| T2 | `simplicity-review-agent.toml`(codex) 미러 생성 | T1 |
| T3 | `implementation-review-agent.md`(claude) Speculative Code 이관 | - |
| T4 | `implementation-review-agent.toml`(codex) Speculative Code 이관 미러 | T3 |

### Phase 2: Producer orchestration (implementation-review + implementation 스킬)
reviewer 계약을 소비하는 producer 스킬을 2-reviewer 병렬로 확장한다.

| Task | 목적 | Dependencies |
|------|------|--------------|
| T5 | `implementation-review` SKILL(claude) 2-reviewer orchestrator 승격 | T1, T3 |
| T6 | `implementation-review` SKILL(codex) 미러 + `implementation` 스킬(claude+codex) gate 확장 | T2, T4, T5 |

### Phase 3: Autopilot SKILL(5곳) + validate 스크립트 + contract + example (validate 스크립트 선행)
autopilot의 결정적 게이트키퍼를 먼저 고치고, 나머지 매핑 surface를 일관 갱신한다.

| Task | 목적 | Dependencies |
|------|------|--------------|
| T8 | `validate_orchestrator.py`(claude+codex) 2-reviewer 매핑 허용 | T1 |
| T9 | autopilot `SKILL.md`(claude) Hard Rule 5 / Step 4 / Step 7.3 갱신 | T8 |
| T10 | autopilot contract §6 + canonical agent set(claude+codex) + `SKILL.md`(codex) 갱신 | T8, T9 |
| T11 | autopilot `sample-orchestrator.md`(claude+codex) + `.codex/agents/README.md` 갱신 | T8, T10 |

## Task Details

### Task T1: simplicity-review-agent (claude) 신규 생성
**Priority**: P0
**Type**: Feature

**Description**: `.claude/agents/simplicity-review-agent.md`를 신규 생성한다. `implementation-review-agent.md`의 구조(frontmatter `tools: [Read, Glob, Grep]`, `model: inherit`, AC / Hard Rules / Process / Output Format / Re-review Mode / findings-first severity / Final Check)를 형제 agent로 따르되, 렌즈를 correctness가 아닌 **동작-불변 형태 품질**로 한정한다. 리뷰 차원은 중복 코드, 죽은 코드, 단일 사용처 추상화, 도달 불가 에러 처리, 과잉압축(중첩 삼항·dense one-liner)이다. 리포트는 `_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md`에 findings-first로 저장한다. Re-review Mode는 correctness reviewer와 대칭으로, 기존 리포트 경로가 입력에 있으면 새 리포트를 만들지 않고 `Current Status` 갱신 + `Iteration History` append로 처리한다.

falsifiable-only gating(I1)을 severity 분류 규칙으로 명시한다: 객관적으로 반증 가능한 위반(위 5개 차원의 구체 사례)은 기본 Medium(gating), 주관적 취향(naming 호불호 등 반박 가능 증거를 댈 수 없는 것)은 Low(advisory). 반증 가능 형태의 판정 기준을 적는다 — "리뷰어가 동작 변화 없이 더 단순한 동등 형태를 구체적으로 제시하지 못하면 finding을 내지 않는다".

**Non-Goals**: correctness 차원(AC 충족·버그·보안·spec drift)은 리뷰하지 않는다 — 그것은 `implementation-review-agent` 소관이다(표적 disjoint). 코드를 직접 수정하지 않는다.

**Acceptance Criteria**:
- [ ] frontmatter가 `name: simplicity-review-agent`, `tools: ["Read", "Glob", "Grep"]`, `model: inherit`를 갖는다 (grep 확인 가능)
- [ ] 본문이 AC / Hard Rules / Process / Output Format / Re-review Mode / Final Check 섹션을 모두 포함한다 (correctness reviewer와 동형 — 섹션 heading grep)
- [ ] 리뷰 차원이 정확히 5개(중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축)로 명시되고, correctness 차원(AC/버그/보안/spec drift)을 리뷰 대상에서 명시적으로 제외한다
- [ ] severity 규칙이 falsifiable-only gating(I1)을 담는다: 객관적 위반=Medium 기본=gating, 주관적 취향=Low=advisory, 그리고 "더 단순한 동등 형태를 제시 못하면 finding 없음" 반증 기준이 적혀 있다
- [ ] Hard Rules가 단일 작성자 불변식(자기 리포트만 write, code/plan/spec 미수정)과 read-only leaf(sub-agent 미spawn)를 명시한다 (I2)
- [ ] Re-review Mode가 기존 리포트 경로 입력 시 새 리포트 미생성 + `Current Status` 갱신 + `Iteration History` append를 명시한다
- [ ] 리포트 저장 경로가 `_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md`로 명시된다 (correctness review 경로와 구분돼 병렬 dispatch 시 충돌 없음)
- [ ] Source Pointer가 이 agent를 단일 소스로, `implementation-review` 스킬을 dispatch wrapper/orchestrator로 가리킨다

**Target Files**:
- [C] `.claude/agents/simplicity-review-agent.md` -- 신규 reviewer agent. correctness reviewer와 표적이 disjoint한 별도 렌즈이므로 기존 파일 수정이 아닌 형제 파일 신규 생성(확정 설계 1번 "신규 별도 agent")

**Technical Notes**: Covers C1, I1, I2; validated by V1. `implementation-review-agent.md`를 구조 템플릿으로 삼되 Tier 시스템 전체를 복제하지 않는다 — simplicity는 동작-불변 형태 리뷰라 plan/spec Tier 분기가 불필요하다(Min-Code: 요청되지 않은 Tier 추상화 미도입). 과잉압축 금지의 근거는 선행 완료된 `implementation-agent.md` REFACTOR Hard Rule "clarity over brevity"(R5)와 짝을 이룬다 — 구현 측이 금지한 패턴을 review 측이 검출한다.

**Dependencies**: -

---

### Task T2: simplicity-review-agent (codex) 미러 생성
**Priority**: P0
**Type**: Feature

**Description**: `.codex/agents/simplicity-review-agent.toml`을 신규 생성해 T1의 claude agent 본문을 codex 표현으로 미러한다. `.codex/agents/implementation-review-agent.toml` 형식(`name`/`description`/`developer_instructions = '''...'''`)을 따른다. `description`은 `spawn_agent(agent_type="simplicity-review-agent")` 호출 안내를 담고, `developer_instructions`에 T1과 동일 계약(5개 차원, falsifiable-only gating, 단일 작성자 불변식, Re-review Mode, 리포트 경로)을 담는다. Source Pointer는 `.codex/skills/implementation-review/SKILL.md`를 wrapper/orchestrator로, 이 `.toml`의 `developer_instructions`를 단일 소스로 가리킨다.

**Acceptance Criteria**:
- [ ] `.codex/agents/simplicity-review-agent.toml`이 `name = "simplicity-review-agent"`로 존재한다 (grep 확인)
- [ ] `developer_instructions`가 T1 claude 본문과 동일 계약(5개 차원, falsifiable-only gating, 단일 작성자 불변식, Re-review Mode, 리포트 경로)을 담는다 — 두 본문의 계약 항목이 1:1로 대응한다 (I3)
- [ ] codex 호출 표현이 `spawn_agent`/`wait_agent`/`close_agent` 규약(`.codex/agents/README.md` Invocation Contract)과 정합한다

**Target Files**:
- [C] `.codex/agents/simplicity-review-agent.toml` -- codex custom agent 신규 생성. codex agent는 `.toml` 단일 소스 형식이므로 claude `.md`와 별개 파일이 필요(플랫폼 parity 수동 관리 — spec 운영 제약)

**Technical Notes**: Covers C1, I3; validated by V1, V8. claude `.md`와 codex `.toml`은 형식만 다르고 계약은 동일하다 — 미러 정합(I3)이 검증 대상.

**Dependencies**: T1

---

### Task T3: implementation-review-agent (claude) Speculative Code 이관
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/agents/implementation-review-agent.md`에서 `Speculative Code` 차원을 제거한다(simplicity reviewer로 이관 — 표적 disjoint). 구체 제거 지점: AC6("Speculative Code 차원이 Step 5 Assessment에서 점검..."), Step 5 Assessment의 Tier 1/2/3 각 `Speculative Code` bullet, Step 6 Findings Classification의 Medium 항목 "**Speculative Code ... 기본 분류**"와 "Speculative Code escalation" 단락. correctness 표적(정확성/AC/버그/보안/spec drift)만 남긴다. AC 번호 재정렬은 최소화하되, 제거로 빈 AC 슬롯이 생기면 후속 AC를 당겨 일관성을 유지한다.

**Non-Goals**: Tier 시스템, Re-review Mode, findings-first 구조, Verification ledger는 건드리지 않는다 — Speculative Code 차원만 외과적 제거한다.

**Acceptance Criteria**:
- [ ] `Speculative Code` 문자열이 `.claude/agents/implementation-review-agent.md`에서 0건이다 (grep `Speculative Code` → no match)
- [ ] Step 5 Assessment의 Tier 1/2/3에 정확성/spec 정합 항목만 남고 사변적 코드 점검 항목이 없다
- [ ] Step 6 Findings Classification의 Medium 정의에서 Speculative Code 기본 분류 문구가 제거되고, escalation 단락이 제거된다
- [ ] AC 섹션이 일관된 번호 체계를 유지하며 Speculative Code 관련 AC가 없다
- [ ] correctness 표적(AC/버그/보안/spec drift) 리뷰 능력은 보존된다 (해당 Process/AC 항목 잔존 확인)

**Target Files**:
- [M] `.claude/agents/implementation-review-agent.md` -- Speculative Code 차원 제거(이관)

**Technical Notes**: Covers C2; validated by V2. 이관이지 삭제가 아니다 — 제거된 차원은 T1의 simplicity reviewer가 흡수한다. 두 reviewer 표적이 disjoint해야 중복 finding이 방지되고 correctness reviewer가 경량화된다(확정 2조건 ②).

**Dependencies**: -

---

### Task T4: implementation-review-agent (codex) Speculative Code 이관 미러
**Priority**: P0
**Type**: Refactor

**Description**: `.codex/agents/implementation-review-agent.toml`의 `developer_instructions`에서 T3와 동일하게 Speculative Code 차원을 제거한다. codex 본문은 Hard Rule 번호가 claude와 다르므로(codex Recommendations Min-Code=Hard Rule 10, claude=11) 본문 내 cross-reference를 codex 번호 체계에 맞게 유지한다.

**Acceptance Criteria**:
- [ ] `Speculative Code` 문자열이 `.codex/agents/implementation-review-agent.toml`에서 0건이다 (grep → no match)
- [ ] 제거 범위가 T3(claude)와 1:1 대응한다 — 두 본문에서 제거된 항목 집합이 같다 (I3)
- [ ] codex 본문의 Hard Rule cross-reference 번호가 codex 체계와 정합하다

**Target Files**:
- [M] `.codex/agents/implementation-review-agent.toml` -- Speculative Code 이관 미러

**Technical Notes**: Covers C2, I3; validated by V2, V8.

**Dependencies**: T3

---

### Task T5: implementation-review 스킬 (claude) 2-reviewer orchestrator 승격
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/skills/implementation-review/SKILL.md`를 thin entrypoint wrapper에서 **2-reviewer orchestrator(review-only)**로 승격한다. 동작: 사용자 요청 + 경로 + 대화 맥락 digest를 모아 `implementation-review-agent`와 `simplicity-review-agent`를 **병렬 dispatch**(한 메시지에서 동시 호출)하고, 두 report 경로와 합산 severity 요약을 사용자에게 relay한다. exit/합집합 판정·fix loop는 **가져오지 않는다**(review-only — fix loop는 `implementation` 스킬 gate 소유). 두 reviewer가 read-only leaf라 병렬 안전함과, simplicity 리포트가 별도 경로(`*_simplicity_review_*`)에 저장돼 충돌 없음을 명시한다.

**Non-Goals**: fix → re-review loop를 도입하지 않는다(그건 `implementation` 스킬 gate 소유). exit 조건 합집합 판정 같은 gating 의사결정을 이 스킬에서 내리지 않는다 — 두 report를 relay만 한다.

**Acceptance Criteria**:
- [ ] 스킬이 `implementation-review-agent`와 `simplicity-review-agent` 둘 다 병렬 dispatch함을 명시한다 (두 agent 이름 grep)
- [ ] 두 reviewer가 read-only leaf라 동시 dispatch가 안전하다는 근거가 적혀 있다
- [ ] 두 report 경로(`*_implementation_review_*`, `*_simplicity_review_*`)와 합산 severity 요약을 relay함이 명시된다
- [ ] review-only 경계가 명시된다 — fix/re-review loop를 이 스킬이 소유하지 않으며 그건 `implementation` 스킬 gate 소관이라는 문장이 있다 (Non-Goals 반영)
- [ ] 단일 reviewer만 호출하던 기존 표현이 남아 있지 않다 (단일 `implementation-review-agent` 전용 dispatch 문구 0건)

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md` -- 2-reviewer orchestrator(review-only) 승격

**Technical Notes**: Covers C3, C4; validated by V3, V4. simplicity 전용 wrapper를 신설하지 않는 이유: 이 스킬이 이미 implementation-review entrypoint이므로 여기에 2번째 reviewer를 병렬 추가하면 충분하다(확정 설계 "부품 절약"). version bump(5.0.0 → 6.0.0) 동반.

**Dependencies**: T1, T3

---

### Task T6: implementation-review(codex) 미러 + implementation 스킬(claude+codex) gate 확장
**Priority**: P0
**Type**: Refactor

**Description**: 세 갱신을 한 task로 묶는다(모두 "producer가 2-reviewer를 병렬 dispatch + 합집합 exit"라는 동일 계약을 각 surface에 적용하는 변경이라 단일 목적):
1. `.codex/skills/implementation-review/SKILL.md`를 T5와 동일하게 2-reviewer orchestrator로 승격(codex `spawn_agent` 병렬 표현).
2. `.claude/skills/implementation/SKILL.md` Step 6(Phase Review-Fix Gate)과 Step 7(Final Cross-Phase Gate)에서 `review`/`re-review` 단계를 correctness ∥ simplicity 병렬 dispatch로 확장하고, exit 조건을 두 report 합집합 `critical=high=medium=0`으로 갱신한다. Step 6 끝 "Speculative Code ... reviewer가 finding으로 분류" 문구를 simplicity reviewer 소관으로 갱신. fix는 두 report finding을 합산해 기존대로 순차 dispatch(변경 없음)임을 명시.
3. `.codex/skills/implementation/SKILL.md`에 동일 변경 미러.

**Acceptance Criteria**:
- [ ] `.codex/skills/implementation-review/SKILL.md`가 두 reviewer 병렬 dispatch + review-only 경계를 담고 T5와 계약 1:1 대응한다 (I3)
- [ ] `.claude/skills/implementation/SKILL.md` Step 6과 Step 7이 각각 correctness ∥ simplicity 병렬 dispatch를 명시한다 (두 agent 이름이 두 Step 모두에 등장)
- [ ] Step 6/Step 7의 exit 조건이 "두 report 합집합 `critical=high=medium=0`"으로 명시된다
- [ ] fix가 두 report finding 합산 → 기존 `implementation-agent` 순차 dispatch로 처리됨이 명시된다(fix 경로 무변경)
- [ ] Step 6의 Speculative Code 문구가 simplicity reviewer 소관으로 갱신된다
- [ ] `.codex/skills/implementation/SKILL.md`의 Step 6/Step 7 exit(두 report 합집합)·Speculative Code 문구(simplicity reviewer 소관 갱신)·2-reviewer(correctness+simplicity 두 agent) 등장이 claude 변경과 1:1 대응한다 (I3)

**Target Files**:
- [M] `.codex/skills/implementation-review/SKILL.md` -- 2-reviewer orchestrator 미러
- [M] `.claude/skills/implementation/SKILL.md` -- Step 6/Step 7 gate 2-reviewer 병렬 + 합집합 exit
- [M] `.codex/skills/implementation/SKILL.md` -- 동일 변경 미러

**Technical Notes**: Covers C3, C4, I3; validated by V3, V4, V8. 세 surface를 한 task로 묶은 이유: 동일 계약(2-reviewer 병렬 + 합집합 exit)을 producer 스킬 layer에 적용하는 단일 목적이고, codex 미러는 claude 변경에 종속이라 분리하면 인위적 dependency edge만 늘어난다. `implementation` 스킬은 gate dispatch 동작이 바뀌므로 frontmatter version bump를 동반한다; `implementation-review` codex SKILL은 T5(claude)와 동일 version 정책을 미러한다.

**Dependencies**: T2, T4, T5

---

### Task T8: validate_orchestrator.py (claude+codex) 2-reviewer 매핑 허용
**Priority**: P0
**Type**: Infrastructure

**Description**: `.claude/skills/sdd-autopilot/scripts/validate_orchestrator.py`와 `.codex/...` 동일 스크립트를 수정해 2-reviewer 매핑을 PASS시킨다. 두 지점:
1. `ALLOWED_BASE_AGENTS` set에 `"simplicity-review-agent"`를 추가한다 (canonical agent 이름 검증 통과).
2. `mapping_specs` 검증 로직을 확장한다. 현재 `review`/`re-review`가 각각 정확히 하나의 agent(`implementation-review-agent`)에 1:1 매핑되도록 `re.search` 첫 매칭만 강제한다. orchestrator가 `review = sdd-skills:implementation-review-agent + sdd-skills:simplicity-review-agent`(또는 합의된 2-reviewer 표기)를 선언할 수 있도록, `review`/`re-review` role이 correctness reviewer **와** simplicity reviewer **둘 다** 매핑돼 있는지 검증하는 형태로 바꾼다. `fix = implementation-agent` 단일 매핑은 그대로 유지한다(fix 경로 무변경).

두 플랫폼 스크립트는 `AGENT_FIELD`/`AGENT_PREFIX`만 다르고(claude=`sdd-skills:` prefix, codex=빈 prefix) 나머지 로직은 동일하므로, 변경을 양쪽에 동형 적용한다.

**Non-Goals**: 기존 검증 항목(필수 섹션, phase-iterative invariant, per-group 필드, `fix_targets`의 `low` 미포함)은 건드리지 않는다 — agent 매핑 검증만 확장한다.

**Acceptance Criteria**:
- [ ] 두 스크립트의 `ALLOWED_BASE_AGENTS`에 `simplicity-review-agent`가 포함된다 (grep)
- [ ] 2-reviewer 검출 파싱 방식(같은 라인 `+` 토큰 병기 vs `review`/`re-review` 두 라인 병기)을 **T8이 확정**하고, 그 표기 형식이 T9~T11 매핑 텍스트와 byte-identical하다 (T9~T11은 이 형식을 복사) — 현재 `role_match`의 `re.search` 첫 매칭 1개 검증을 두 reviewer 모두 매핑됐는지 검출하는 형태로 교체
- [ ] `review`/`re-review` role이 correctness + simplicity 2-reviewer로 선언된 orchestrator를 PASS시킨다 (2-reviewer 매핑 표기를 담은 샘플 orchestrator 텍스트로 스크립트 실행 → exit 0)
- [ ] `review`/`re-review`에 simplicity reviewer가 빠진 단일 reviewer 매핑은 FAIL시킨다 (단일 매핑 샘플 → exit 1, finding 출력) — 2-reviewer 고정이 강제됨
- [ ] `fix = implementation-agent` 단일 매핑 검증은 그대로 유지된다 (fix에 다른 agent 끼면 FAIL)
- [ ] claude/codex 두 스크립트의 변경이 `AGENT_PREFIX`/`AGENT_FIELD`를 제외하고 동형이다 (I3)

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/scripts/validate_orchestrator.py` -- 2-reviewer 매핑 허용 + canonical agent 추가
- [M] `.codex/skills/sdd-autopilot/scripts/validate_orchestrator.py` -- 동형 미러

**Technical Notes**: Covers C6, I3; validated by V6, V8. **결정적 게이트키퍼** — 이 스크립트가 단일 reviewer만 허용하면 2-reviewer orchestrator가 Step 5.1에서 reject되므로, autopilot 매핑 갱신(T9/T10/T11)의 선행 dependency다. T9~T11이 이 스크립트의 PASS 기준에 맞춰 매핑을 표기하려면 PASS 규칙이 먼저 확정돼야 한다.

**Dependencies**: T1

---

### Task T9: autopilot SKILL.md (claude) single-reviewer 5곳 2-reviewer 갱신
**Priority**: P1
**Type**: Refactor

**Description**: `.claude/skills/sdd-autopilot/SKILL.md`의 `implementation-review-agent` 단일 reviewer 고정 **5곳**을 2-reviewer 병렬로 갱신한다:
1. **Hard Rule 5**(L57): "review 포함 파이프라인에서 `implementation-review-agent` subagent로 review"를 "correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`) 2-reviewer 병렬 dispatch, exit는 두 report 합집합"으로 확장.
2. **Step 4 reasoning**(L180): review 포함 path에서 두 reviewer를 모두 subagent step으로 유지함을 명시.
3. **Step 7.2 dispatch controller 서술**(L258): "review 포함 path에서는 `implementation-review-agent`를 항상 subagent 호출로 실행"하는 서술을 correctness ∥ simplicity 2-reviewer 병렬 호출로 갱신.
4. **per-group review-fix gate 본문**(L265): group 범위로 `implementation-review-agent` subagent 실행하는 서술을 두 reviewer 병렬 실행 + 합집합 exit로 갱신.
5. **Step 7.3 매핑**(L273): agent 매핑 `review = sdd-skills:implementation-review-agent`를 2-reviewer 병렬 표기로 확장하고, exit가 두 report 합집합임을 명시. T8 스크립트가 PASS시키는 표기 형식과 정확히 일치시킨다(Q1 — T8이 형식 확정, T9가 복사).

**Acceptance Criteria**:
- [ ] Hard Rule 5(L57)가 correctness ∥ simplicity 2-reviewer 병렬 dispatch + 합집합 exit를 명시한다
- [ ] Step 4 reasoning(L180)이 두 reviewer를 subagent step으로 유지함을 명시한다
- [ ] Step 7.2 dispatch controller 서술(L258)이 두 reviewer 병렬 호출로 갱신된다
- [ ] per-group review-fix gate 본문(L265)이 두 reviewer 병렬 실행 + 합집합 exit로 갱신된다
- [ ] Step 7.3의 agent 매핑(L273)이 2-reviewer 병렬 표기로 확장되고 합집합 exit를 명시한다
- [ ] Step 7.3 매핑 표기 형식이 T8 스크립트 PASS 규칙과 일치한다 (이 SKILL의 매핑 예시 문자열을 스크립트가 PASS시킴)
- [ ] 이 파일 내 `implementation-review-agent` 단일 reviewer를 gating 주체로 서술하는 표현이 grep 0건이다 — 잔존 등장은 모두 2-reviewer/correctness-lens 문맥(correctness reviewer 지칭)으로만 존재한다
- [ ] `fix = sdd-skills:implementation-agent` 순차 매핑 표현은 무변경으로 유지된다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- single-reviewer 5곳(L57/L180/L258/L265/L273) 2-reviewer 갱신

**Technical Notes**: Covers C5; validated by V5. 이 파일이 autopilot single-reviewer 고정의 주 surface다(5곳). autopilot 매핑의 결정적 게이트키퍼인 validate 스크립트(T8)가 PASS 기준의 source of truth이므로 T8에 의존한다. version bump(frontmatter version 갱신)는 이번 범위 밖이다(매핑 표현 변경만, 스킬 인터페이스 무변경).

**Dependencies**: T8

---

### Task T10: autopilot contract §6 + canonical agent set(claude+codex) + SKILL.md(codex) 갱신
**Priority**: P1
**Type**: Refactor

**Description**: 매핑 계약의 canonical home과 codex 미러를 갱신한다:
1. `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`: §2 허용 `subagent_type` 목록에 `sdd-skills:simplicity-review-agent` 추가, §6 Review-Fix Contract의 agent mapping(`review = ...`, `re-review = ...`)을 correctness + simplicity 2-reviewer 병렬로 확장, Planning Producer Review Gate는 무변경(simplicity는 implementation review 한정).
2. `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`: 동일 변경 미러(codex `agent_type` 표기).
3. `.codex/skills/sdd-autopilot/SKILL.md`: T9의 claude 변경(Hard Rule 5 / Step 4 / Step 7.3 대응 지점)을 codex 표현으로 미러.

**Acceptance Criteria**:
- [ ] claude contract §2 허용 목록에 `sdd-skills:simplicity-review-agent`가 포함된다
- [ ] claude contract §6 agent mapping의 `review`/`re-review`가 2-reviewer 병렬로 확장되고, `fix`는 `implementation-agent` 단일 유지, exit가 두 report 합집합임이 명시된다
- [ ] contract 내 §6 mapping(L128) 외 서술형 문장(L134/L139/L143)의 `implementation-review-agent` 잔존 표현이 모두 2-reviewer 문맥(correctness lens 지칭)으로 갱신됐고, 단일 reviewer를 gating 주체로 서술하는 문장이 grep 0건이다
- [ ] codex contract가 claude contract와 1:1 대응한다 (I3)
- [ ] codex `SKILL.md`가 T9 claude 변경과 1:1 대응한다 (I3)
- [ ] §15 계약 우선순위(contract가 canonical home)와 정합 — contract §6 표기와 SKILL 매핑 표기가 모순되지 않는다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` -- §2 + §6 매핑 확장
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- 동형 미러
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- T9 대응 미러

**Technical Notes**: Covers C5, I3; validated by V5, V8. contract가 매핑 규칙의 canonical home(autopilot SKILL §15)이므로 T9(claude SKILL)와 표기 일관이 필수다. T9의 claude SKILL 갱신 형식을 기준으로 contract와 codex SKILL을 맞춘다.

**Dependencies**: T8, T9

---

### Task T11: autopilot sample-orchestrator(claude+codex) + .codex/agents/README.md 갱신
**Priority**: P1
**Type**: Refactor

**Description**: 예시와 codex agent 목록을 갱신한다:
1. `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`: Example A의 `agent_mapping`/`execution_sequence`와 Example B의 `agent_mapping`/`execution_sequence_per_group`/`final integration review`를 2-reviewer 병렬 dispatch + 합집합 exit로 갱신. review 입력 설명에 두 reviewer 모두 호출됨을 반영.
2. `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`: 동일 변경 미러.
3. `.codex/agents/README.md`: `Agent Set`과 `Inline Writing` 목록에 `simplicity-review-agent` 추가.

**Acceptance Criteria**:
- [ ] claude sample-orchestrator Example A/B의 `agent_mapping`(L90-91)/`agent_mapping`(L268-271)/`execution_sequence_per_group`(L272)이 2-reviewer 병렬 + 합집합 exit를 표기하고, 그 표기가 T8 스크립트 PASS 규칙과 T10 contract §6와 일치한다
- [ ] claude sample-orchestrator의 review-fix gate 예시가 두 reviewer 동시 호출 + fix 순차(무변경)를 반영한다
- [ ] 이 파일 내 mapping/sequence 외 서술형 문장(L5/L92/L100-101/L273/L281/L286-287)의 `implementation-review-agent` 잔존 표현이 모두 2-reviewer 문맥(correctness lens 지칭)으로 갱신됐고, 단일 reviewer를 gating 주체로 서술하는 문장이 grep 0건이다 — final integration review 서술(L286-287)도 두 reviewer 병렬로 갱신된다
- [ ] codex sample-orchestrator가 claude와 1:1 대응한다 (I3)
- [ ] `.codex/agents/README.md`의 `Agent Set`과 `Inline Writing` 목록에 `simplicity-review-agent`가 추가된다
- [ ] sample-orchestrator 텍스트를 T8 스크립트로 검증 시 PASS한다 (예시가 게이트키퍼를 실제 통과)

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` -- Example A/B review-fix gate 갱신
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- 동형 미러
- [M] `.codex/agents/README.md` -- Agent Set + Inline Writing 목록 추가

**Technical Notes**: Covers C5, I3; validated by V5, V6, V8. sample-orchestrator는 autopilot이 생성하는 orchestrator의 품질 기준 예시이므로 T8 스크립트를 실제로 통과해야 한다(self-consistency). 표기는 T10 contract §6를 source로 따른다.

**Dependencies**: T8, T10

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1, I2 | review (2등급 정성) | `.claude/agents/simplicity-review-agent.md`를 리뷰어가 읽어 (a) AC/Hard Rules/Process/Output/Re-review/Final Check 6섹션 존재, (b) 리뷰 차원 정확히 5개 + correctness 차원 명시 제외, (c) falsifiable-only gating 규칙(Medium=gating/Low=advisory + 반증 기준), (d) 단일 작성자 불변식 + read-only leaf를 확인. 위반 사례(누락 섹션/차원/규칙)를 지목 못하면 MET. 증거=인용한 heading/문장 |
| V2 | C2 | test (1등급 정량) | `grep -c "Speculative Code" .claude/agents/implementation-review-agent.md` → 0, `grep -c "Speculative Code" .codex/agents/implementation-review-agent.toml` → 0. 증거=grep 출력. correctness 표적(AC/버그/보안/spec drift) Process/AC 항목 잔존은 리뷰 인용으로 보조 확인 |
| V3 | C3 | review (2등급 정성) | `.claude/skills/implementation/SKILL.md` Step 6/Step 7과 `implementation-review` SKILL을 리뷰어가 읽어 correctness ∥ simplicity 병렬 dispatch + exit 두 report 합집합이 명시됐는지 확인. 두 Step 모두에 두 agent 이름이 등장하고 합집합 exit 문구가 있으면 MET. 증거=인용한 dispatch/exit 문장 |
| V4 | C4 | review (2등급 정성) | `implementation-review` SKILL(claude+codex)을 리뷰어가 읽어 (a) 2-reviewer 병렬 dispatch, (b) 두 report 경로 + 합산 요약 relay, (c) review-only 경계(fix loop 미소유)가 명시됐는지 확인. fix loop를 이 스킬이 소유하는 표현이 남아 있으면 NOT MET. 증거=인용한 경계 문장 |
| V5 | C5 | review (2등급 정성) + test (1등급 정량 보조) | (정성) autopilot SKILL(L57/L180/L258/L265/L273, claude+codex), contract §2/§6(claude+codex), sample-orchestrator(claude+codex)를 리뷰어가 읽어 매핑이 SKILL 5곳+contract+example 전체에서 2-reviewer 병렬 + 합집합 exit로 일관 갱신됐는지 확인. 한 surface라도 단일 reviewer를 gating 주체로 서술하는 표현이 남으면 NOT MET. (정량 보조) `grep "implementation-review-agent" .claude/skills/sdd-autopilot/SKILL.md`의 모든 매칭이 2-reviewer/correctness-lens 문맥에서만 등장(단일 reviewer gating 서술 0건) — codex 미러도 동일. 증거=각 surface 인용 + grep 출력 |
| V6 | C5, C6 | test (1등급 정량) | (a) 2-reviewer 매핑을 표기한 sample-orchestrator를 `python3 validate_orchestrator.py <sample>` 실행 → exit 0(PASS). (b) simplicity reviewer가 빠진 단일 reviewer 매핑 fixture → exit 1(FAIL, finding 출력). (c) claude/codex 두 스크립트 모두 동일 판정. 증거=각 실행의 exit code + stdout |
| V7 | I1 | review (2등급 정성) | simplicity reviewer 본문의 severity 규칙을 리뷰어가 읽어 "객관적 위반=Medium=gating, 주관적 취향=Low=advisory, 더 단순한 동등 형태 제시 못하면 finding 없음"이 반박 가능한 형태로 적혔는지 확인. gating이 주관적 취향까지 끌어들이면(수렴성 훼손) NOT MET. 증거=인용한 severity 문장 |
| V8 | I3 | review (2등급 정성) | claude/codex 미러 쌍을 리뷰어가 대조해 계약 항목이 1:1 대응하는지 확인 — 각 쌍을 독립 항목으로 점검: (1) `simplicity-review-agent` 본문(.md ↔ .toml), (2) `implementation-review-agent` Speculative Code 이관(.md ↔ .toml), (3) `implementation-review` SKILL(claude ↔ codex), (4) `implementation` SKILL(claude ↔ codex), (5) `validate_orchestrator.py`(claude ↔ codex), (6) `orchestrator-contract.md`(claude ↔ codex), (7) autopilot `SKILL.md`(claude ↔ codex), (8) `sample-orchestrator.md`(claude ↔ codex) + `.codex/agents/README.md` 목록. 한 쌍이라도 계약 누락/불일치가 있으면 NOT MET. 증거=불일치 지목 또는 "대응 확인" 인용 |

## Parallel Execution Summary

| Phase | Tasks | 병렬 가능 | 충돌/dependency 근거 |
|-------|-------|-----------|----------------------|
| Phase 1 | T1, T2, T3, T4 | T1 ∥ T3 (2그룹), 이어서 T2(T1 후) ∥ T4(T3 후) | T1/T3는 Target Files disjoint(신규 simplicity agent vs 기존 correctness agent)·dependency 없음 → 병렬. T2는 T1 본문에, T4는 T3 본문에 종속(미러). T2 ∥ T4는 Target Files disjoint |
| Phase 2 | T5, T6 | 순차 | T5(claude implementation-review 승격) → T6(codex 미러는 T5에 종속 + implementation 스킬 gate가 T5 reviewer 계약 소비). T6은 T2/T4/T5 모두에 종속 |
| Phase 3 | T8, T9, T10, T11 | 순차 (T8 → T9 → T10 → T11) | T8(validate 스크립트)이 PASS 규칙 source of truth라 선행. T9는 T8 PASS 형식에 매핑을 맞춤. T10은 T9 표기를 contract/codex로 전파. T11은 T8 스크립트 통과 + T10 contract 표기를 예시에 반영. 의미적 충돌: 모두 동일 매핑 표기를 가정하므로(④ contract 생산-소비 패턴) dependency edge로 직렬화 |

> Cross-phase: Phase 2는 Phase 1 reviewer 계약(T1/T3)을 소비하므로 Phase 1 후. Phase 3는 reviewer 존재(T1)만 필요해 Phase 2와 독립이지만, Phase 1 T1 완료가 공통 선행이다.

# Risks/Mitigations and Open Questions

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| R1: `validate_orchestrator.py` 매핑 모델 확장이 기존 단일 reviewer orchestrator(legacy)를 깨뜨려 resume 경로에서 reject | 기존 active orchestrator가 Step 5.1/resume 재검증에서 FAIL | T8에서 2-reviewer를 **강제**(단일 reviewer를 FAIL)하므로 의도된 동작 — 단일→2-reviewer 고정 확장이 목적(autopilot 4겹 고정의 확장). resume 시 legacy orchestrator는 contract 위반으로 regenerate 대상(Resume Contract 1번 재검증)이며, 이는 설계상 수용된 break |
| R2: 토큰 비용 증가 (매 gate마다 reviewer 2개 + 매 회차 simplicity 재참여) | gate당 토큰 ~2배, multi-phase에서 누적 | 사용자가 명시 수용(digest "토큰만 증가"). 벽시계는 병렬로 max(둘)≈1 reviewer 유지. mitigation 불필요 — 트레이드오프 자체가 채택안 |
| R3: 표적 disjoint가 불완전해 두 reviewer가 같은 finding을 중복 보고 | 합집합 gating에서 중복 finding이 fix를 2회 트리거 | T3/T4의 Speculative Code 완전 이관(grep 0건)으로 표적 경계 강제. V8 미러 대조 + V2 grep으로 검증. correctness=정확성/simplicity=형태 경계가 본문에 명시(C2) |
| R4: claude/codex 6쌍 미러 중 일부 누락으로 플랫폼 parity 깨짐 | codex 경로에서 simplicity reviewer 미작동 | I3를 V8 전용 검증으로 분리해 6쌍 전수 대조. spec 운영 제약상 parity는 수동 관리이므로 task마다 codex 미러를 명시적 AC로 고정 |
| R5: 선행 완료된 `implementation-agent.md` "clarity over brevity" 한 줄과 simplicity reviewer 과잉압축 차원의 용어 불일치 | 구현 측 금지와 review 측 검출이 어긋나 false positive/negative | T1에서 과잉압축 차원을 REFACTOR Hard Rule과 짝지어 정의(Technical Notes). 두 곳이 "중첩 삼항·dense one-liner" 같은 동일 구체 사례를 쓰도록 grounding |

## Open Questions

### Q1. validate_orchestrator.py에서 2-reviewer 매핑을 어떤 텍스트 형식으로 표기/검증할 것인가
- **Decision taken**: `review`/`re-review` role이 correctness reviewer **와** simplicity reviewer 둘 다 매핑된 경우에만 PASS시키는 형태로 `mapping_specs` 검증을 확장한다(예: `review = sdd-skills:implementation-review-agent + sdd-skills:simplicity-review-agent` 또는 두 role 라인 병기). **T8이 정확한 토큰 형식(라인 병기 vs `+` 토큰)을 확정하고**(기존 `re.search` 패턴과 충돌하지 않는 가장 단순한 표기), T9~T11은 그 확정된 형식을 byte-identical하게 복사한다. 즉 형식의 source of truth는 T8 스크립트이며 매핑 surface(T9~T11)는 소비자다.
- **Alternatives considered**: (a) `simplicity-review`를 별도 role 키로 추가 — 기존 `review`/`fix`/`re-review` 3-role 모델을 4-role로 키우지만, simplicity가 review와 항상 병렬이라 별도 키는 중복 개념. 기각. (b) 매핑 검증을 느슨하게 풀어 simplicity를 optional로 — 2-reviewer 고정(확정 설계 2번 "모든 gate에서 병렬")을 약화시켜 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: No (확정 설계가 2-reviewer 고정을 명시; 형식 세부는 구현 재량)

### Q2. 6개 surface 변경을 하나의 spec delta로 묶을 것인가
- **Decision taken**: 하나의 draft로 묶는다. 6개 surface는 모두 "직교 2-렌즈 병렬 review" 단일 계약의 다른 표현 지점이며, 부분 적용 시 autopilot single-reviewer 고정(SKILL 5곳 + validate 스크립트)이 깨져 게이트키퍼가 reject한다(원자적 변경).
- **Alternatives considered**: reviewer agent 도입(Phase 1~2)과 autopilot 매핑 확장(Phase 3)을 별도 draft로 분리 — Phase 3가 Phase 1 reviewer 존재에 의존하고, 분리 시 중간 상태에서 autopilot이 미존재 agent를 매핑해 validate FAIL. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. simplicity review 리포트를 correctness 리포트와 별도 경로/파일로 둘 것인가
- **Decision taken**: 별도 경로(`_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md`)로 둔다. 두 reviewer가 병렬 dispatch되므로 같은 파일에 쓰면 단일 작성자 불변식(각 reviewer는 자기 리포트만 write)과 충돌하고 동시 write race가 생긴다.
- **Alternatives considered**: 단일 통합 리포트에 두 섹션 — 병렬 write 충돌 + 단일 작성자 불변식 위반으로 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No
