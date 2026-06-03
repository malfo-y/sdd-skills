# Feature Draft: investigate를 orchestrator(skill) + 범용 Explore fan-out으로 재설계 + investigate-agent 제거

# Part 1: Temporary Spec Draft

## Change Summary

investigate를 thin wrapper(Mode B) → single `investigate-agent` dispatch 구조에서, **메인 루프 orchestrator skill**로 재설계한다. 이유: investigate는 탐색·가설 검증 단계에서 read-only sub-agent fan-out이 유익한데, 직전 wrapper화(spec v4.1.11)가 census 오분류("현재 agent 본문이 sub-agent를 안 깐다" → non-fan-out=wrapper)로 인해 investigate의 병렬 잠재력을 죽였다. 통합 규칙(`fan-out이 필요한 execution → orchestrator(skill) + leaf` / `non-fan-out → wrapper + single-source agent`, main.md L59/L90)에 비추면 investigate는 orchestrator여야 한다.

핵심 설계는 **투 트랙**이다:
- **탐색 트랙** (read-only 증거 수집·가설 검증): 넓고·모호할 때만 **범용 Explore agent를 병렬 fan-out**한다. Explore는 read-only(Edit/Write/Agent 도구 없음)이므로 탐색에만 적합하다.
- **인라인 트랙** (그 외 전 단계: 문제정의·근본원인 종합·Blast Radius·fix(write)·Fresh Verification): orchestrator가 메인 루프에서 직접 수행한다. fix는 write가 필요하므로 read-only Explore가 못 한다.

leaf는 implementation처럼 custom agent를 새로 만들지 않고 **런타임 빌트인 범용 read-only explore 역할을 재사용**한다 (claude `Explore`, codex `spawn_agent(agent_type="explorer")`). 따라서 `investigate-agent`(claude `.md` + codex `.toml`)는 제거하고 매니페스트 `agents` 목록에서도 뺀다.

## Scope Delta

**In-scope:**
- `.claude/skills/investigate/SKILL.md`를 wrapper → orchestrator로 재작성 (문제정의(대화 기반) → 조건부 Explore 병렬 fan-out → 근본원인 종합 → Blast Radius → fix·Fresh Verification 인라인, 3-Strike·Scope Lock 보존).
- `.codex/skills/investigate/SKILL.md`를 동일 orchestrator 구조로 재작성 (codex-native `spawn_agent(agent_type="explorer")` + `wait_agent` 병렬, 미가용 시 순차 인라인 graceful degrade).
- `.claude/agents/investigate-agent.md` 삭제.
- `.codex/agents/investigate-agent.toml` 삭제.
- `.claude-plugin/marketplace.json` `agents` 목록에서 `./.claude/agents/investigate-agent.md` 제외.

**Out-of-scope (guardrail):**
- spec 내 investigate 재분류(wrapper→orchestrator(Explore 재사용)) 갱신은 이 draft의 코드 범위 밖이며 후속 `spec-update-done` 대상이다 (Hard Rule 1: 이 작업은 spec 파일을 수정하지 않는다). **갱신 surface는 `_sdd/spec/components.md` L33(investigate를 "wrapper -> agent"로 분류한 유일 행) + `_sdd/spec/DECISION_LOG.md`(2026-06-03 entry의 "fan-out 없는 9종" 목록·Mode B 목록·Agent 도구 제거 목록 3곳)**. `main.md`는 일반 규칙(orchestrator vs wrapper)만 담고 investigate 문자열이 0건이므로 갱신 대상이 아니다.
- 다른 wrapped 스킬(review 3종, planner) 재분류 — 토론에서 investigate가 유일 오분류로 확정.
- 새 custom explore leaf agent 신설 — 런타임 빌트인 범용 역할 재사용으로 대체(custom leaf 만들지 않음).
- investigate의 디버깅 방법론 자체(근본원인 우선, Blast Radius, Fresh Verification 정의) 변경 — 소유 위치만 agent→orchestrator로 이동하고 의미는 보존.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | investigate entrypoint를 wrapper(single-agent dispatch) → orchestrator(메인 루프 skill)로 재정의. 전체 디버깅 계약(문제정의·근본원인·Blast Radius·fix·Fresh Verification·Investigation Report)을 skill이 인라인 소유 | fan-out은 메인 루프에서만 가능(nesting 1단계). investigate는 fan-out 유익 스킬이므로 orchestrator여야 함 (main.md L59/L90 통합 규칙) |
| C2 | Add | 탐색 트랙은 넓고·모호할 때(경쟁 가설/출처 불분명/대규모) 범용 read-only explore 역할을 병렬 fan-out한다. claude `Explore`, codex `spawn_agent(agent_type="explorer")`+`wait_agent` | 옛 Agent A/B 교차검증 의도(anti-anchoring)를 부활. read-only 병렬은 증거 수집·가설 검증을 가속 |
| C3 | Add | fan-out 트리거 = 기본 인라인 순차, 넓고·모호할 때만 병렬. 단순 단일파일 버그는 순차 인라인 | YAGNI. 디버깅 대부분은 단순 버그 — fan-out 오버헤드 회피. implementation "확신 없으면 순차" 철학과 정합 |
| C4 | Add | fix(write)·Fresh Verification·근본원인 종합·Blast Radius Gate·3-Strike·Scope Lock은 orchestrator 인라인 소유 (Explore는 read-only라 write 불가) | read/write 분리가 투 트랙의 칼선. 단일 스레드 fix loop |
| C5 | Modify | codex investigate는 동등 read-only explore 역할이 있으면 `spawn_agent(agent_type="explorer")`로 병렬, 없으면 순차 인라인 graceful degrade. (census 결과: codex README L60-62가 `explorer` 역할을 read-only investigation 표준으로 문서화 → 병렬 경로 우선) | 정확성은 양 플랫폼 동일, 병렬만 런타임 역량 조건부 |
| C6 | Remove | `investigate-agent`(claude `.md` + codex `.toml`) 제거 및 매니페스트 `agents` 목록에서 제외 | leaf=범용 Explore 재사용이라 custom investigate agent 불필요. 참조자=자기파일+wrapper+매니페스트뿐(autopilot·타 스킬 미참조)이라 제거 격리(저위험) |
| I1 | Preserve | investigate의 4대 불변식(근본원인 우선, Scope Lock, Blast Radius Gate, Fresh Verification=이전 결과 재사용 금지·env 미존재 시 UNTESTED 표기)은 소유 위치가 agent→orchestrator로 이동해도 보존된다 | 재설계는 fan-out 추가일 뿐, 디버깅 안전성 계약은 불변 |
| I2 | Preserve | investigate trigger와 Investigation Report 출력 계약(Problem/Root Cause/Fix(파일:라인)/Blast Radius/Verification PASS·FAIL·UNTESTED/Out-of-Scope Findings)은 보존된다 | 사용자·downstream 진입점/산출물 안정성 |
| I3 | Add | investigate-agent 제거 후에도 어떤 caller(autopilot·타 스킬)도 깨지지 않는다 (제거 전 grep 재확인으로 보장) | 제거 격리 불변식. 토론 grep 사실을 draft에서 재검증 |

## Touchpoints

> `Strategic Code Map`/components.md를 출발점으로 삼되 아래는 현재 코드 탐색으로 재확인했다.

| 지점 | 현재 상태 (재확인) | 변경 이유 |
|------|-------------------|----------|
| `.claude/skills/investigate/SKILL.md` | v3.0.0 thin wrapper. L19에서 `Agent(subagent_type="sdd-skills:investigate-agent", ...)` dispatch. 본문 30줄 | orchestrator 본문(문제정의→조건부 Explore 병렬→종합→Blast Radius→fix·검증 인라인)으로 재작성. wrapper↔agent pointer 제거 |
| `.codex/skills/investigate/SKILL.md` | v3.0.0 thin wrapper. L19에서 `spawn_agent(agent_type="investigate_agent", ...)`+`wait_agent` | claude와 동일 orchestrator 구조. 탐색 fan-out은 `spawn_agent(agent_type="explorer")`+`wait_agent`, 미가용 시 순차 degrade |
| `.claude/agents/investigate-agent.md` | 86줄. tools=[Read,Write,Edit,Glob,Grep,Bash]. Agent 도구 미보유(dispatch되면 fan-out 불가). 전체 디버깅 계약 단일 소스 | 삭제. 계약은 orchestrator skill로 이전 |
| `.codex/agents/investigate-agent.toml` | `name="investigate_agent"`. developer_instructions에 동일 계약. Step 3에 "Agent A/B 병렬 dispatch" 사문화된 문구 존재 | 삭제 |
| `.claude-plugin/marketplace.json` | L51에 `./.claude/agents/investigate-agent.md` 등록. skills L38 investigate는 유지 | `agents` 배열에서 L51 항목 제거. skills 항목은 유지(orchestrator도 skill) |
| codex 런타임 explore 역량 (census) | `.codex/agents/README.md` L60 `spawn_agent(agent_type="explorer")` for read-only investigation 명시 — claude `Explore` 동등 역할 존재 | C5의 병렬 경로가 codex에서 실제 가용함을 확정. 순차 degrade는 fallback으로만 명시 |
| autopilot 참조 (격리 재확인) | `.claude/skills/sdd-autopilot` 내 investigate 참조 0건 (grep 확인). investigate-agent 참조자=자기파일+wrapper 2종+매니페스트뿐 | I3 제거 격리 근거 — caller breakage 없음 |

## Implementation Plan

1. **investigate-agent 제거 격리 재확인** — `investigate-agent`/`investigate_agent` 참조를 전수 grep해 caller가 wrapper+매니페스트뿐임을 재검증(I3). 외부 dispatch 발견 시 중단·보고.
2. **claude orchestrator 재작성** — `.claude/skills/investigate/SKILL.md`를 orchestrator 본문으로 재작성. 문제정의(대화 기반 forwarding 유지) → 조건부 Explore 병렬 fan-out(가설-lane/영역-lane 예시) → 근본원인 종합 → Blast Radius → fix·Fresh Verification 인라인. 3-Strike·Scope Lock 보존. Investigation Report 계약 보존(I2).
3. **codex orchestrator 재작성** — `.codex/skills/investigate/SKILL.md`를 동일 구조로. 탐색 fan-out=`spawn_agent(agent_type="explorer")`+`wait_agent`, 미가용 시 순차 인라인 graceful degrade.
4. **agent 파일 삭제** — `.claude/agents/investigate-agent.md`, `.codex/agents/investigate-agent.toml` 삭제.
5. **매니페스트 정리** — `marketplace.json` `agents` 목록에서 `investigate-agent.md` 제외.
6. **정적 게이트 검증** — grep/diff로 orchestrator 구조·Explore dispatch 존재·agent/매니페스트 제거 확인. 런타임 smoke(단순 버그=인라인 / 넓은 버그=Explore 병렬 dispatch).

순서 근거: Step 1(격리 재확인)을 먼저 게이트로 둔다. Step 2~3은 파일 disjoint라 병렬 가능하나 동일 orchestrator 계약을 양 플랫폼에 인코딩하므로 의미적 정합(parity)이 필요하다. Step 4 삭제는 Step 2~3에서 wrapper의 agent dispatch가 제거된 뒤여야 dangling reference가 안 생긴다(생산-소비 순서). Step 5는 Step 4와 함께 제거 정합을 이룬다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C4, I1, I2 | static review (grep/diff) | claude SKILL.md가 orchestrator 본문을 가짐: 문제정의·근본원인 종합·Blast Radius·fix·Fresh Verification 인라인 단계 + 3-Strike·Scope Lock·Investigation Report 형식 존재. `Agent(subagent_type=...investigate-agent...)` dispatch 문구 부재 |
| V2 | C2, C3 | static review + 런타임 smoke | **정적**: SKILL.md에 `Explore` dispatch 지시 grep ≥1, "기본 인라인, 넓고·모호할 때만 병렬" 트리거 문자열 존재. **런타임(reload 후, 2케이스)**: (a) 단순 단일파일 버그 입력 → Explore dispatch **0회**(인라인 경로) 관찰; (b) 경쟁 가설/넓은 출처 버그 입력 → Explore **≥2 병렬 dispatch** 관찰. reload 불가 시 정적만 PASS + 런타임 DEFERRED 명시 |
| V3 | C5 | static review (codex) | `.codex/skills/investigate/SKILL.md`에 `spawn_agent(agent_type="explorer")`+`wait_agent` 병렬 경로 + 미가용 시 순차 인라인 degrade 명시. census 근거(README explorer 역할) 반영 |
| V4 | C6, I3 | grep/diff | `.claude/agents/investigate-agent.md`·`.codex/agents/investigate-agent.toml` 파일 부재(`test ! -f`). `marketplace.json` `agents` 배열에 investigate-agent 미등록. **잔존 코드 dispatch 0건**: `grep -rn 'investigate.agent'` 범위를 **코드 surface로 한정**(`.claude/skills .codex/skills .claude/agents .codex/agents .claude-plugin`)했을 때 0건(orchestrator skill엔 dispatch 없음). 제외 집합 = `_sdd/spec/*`·`_sdd/drafts/*`·`_sdd/discussion/*`·`_sdd/implementation/*`(문서 참조 — 후속 spec-update 대상, 코드 아님) |
| V5 | I1, I2 | static review (양 플랫폼 parity) | claude/codex 두 SKILL.md가 동일 orchestrator 계약(투 트랙·Report 형식·불변식)을 인코딩하고, dispatch 표현만 플랫폼별로 다름 |

## Risks / Open Questions

### Q1. codex 런타임에 claude `Explore` 동등의 범용 read-only explore 역할이 존재하는가 (census)
- **Decision taken**: 존재한다고 확정하고 codex 병렬 경로를 1차 경로로 둔다. `.codex/agents/README.md` L60-62가 `spawn_agent(agent_type="explorer")` for read-only investigation을 Codex-native 표준 역할로 명시하고, 동일 README가 `Agent(...)`/`subagent_type="general-purpose"` 대신 `explorer`/`worker`/`default` 역할 사용을 규정한다. 따라서 codex SKILL.md는 `spawn_agent(agent_type="explorer")`+`wait_agent` 병렬을 우선하고, 순차 인라인은 역할 미가용 시 graceful degrade fallback으로만 둔다.
- **Alternatives considered**: (a) codex는 순차만으로 두고 병렬 미지원 — 기각: README가 explorer 역할을 명시하므로 실제 역량을 죽이는 과보수. (b) codex 전용 explore leaf agent 신설 — 기각: 빌트인 `explorer` 역할 재사용이 가능하므로 custom leaf는 YAGNI(토론 결정 8과 정합).
- **Confidence**: HIGH (README 문서 직접 확인)
- **User confirmation needed**: No

### Q2. investigate-agent 제거가 caller를 깨뜨리지 않는가
- **Decision taken**: 안전 제거. 참조자는 자기 파일 2종(claude `.md`/codex `.toml`) + wrapper 2종 + 매니페스트 1곳뿐이고, autopilot·외부 스킬 dispatch는 0건임을 grep으로 재확인했다(I3). wrapper가 orchestrator로 재작성되며 dispatch가 사라지므로 dangling reference도 제거된다. 잔존하는 `_sdd/spec/*`·`_sdd/drafts/*` 내 문자열은 문서 참조이며 후속 spec-update 대상(코드 dispatch 아님).
- **Alternatives considered**: (a) agent 파일을 deprecated stub으로 남김 — 기각: 참조자가 없어 stub이 죽은 코드. (b) 제거를 후속 PR로 분리 — 기각: 동일 변경 단위로 묶는 것이 매니페스트/wrapper 정합을 한 번에 보장(토론 결정 1).
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. spec 재분류(wrapper→orchestrator(Explore 재사용))를 이 draft에서 함께 하지 않는 것
- **Decision taken**: spec 갱신은 out-of-scope로 두고 후속 `spec-update-done`에 위임한다 (Hard Rule 1: 이 작업은 `_sdd/spec/*`를 수정하지 않는다). investigate를 wrapper로 분류하는 surface는 **`components.md` L33 + `DECISION_LOG.md`(9종 목록·Mode B 목록·Agent 도구 제거 목록)** 이며(현재 코드 grep으로 확인), 이 코드 변경 머지 후 그 surface에 drift가 생긴다. `main.md`는 일반 규칙만 담고 investigate 문자열 0건이라 갱신 대상이 아니다. 정확한 surface를 Open Question에 명시해 인계한다.
- **Alternatives considered**: (a) 이 draft에서 spec도 함께 수정 — 기각: feature-draft agent의 Hard Rule 1 위반. (b) spec drift를 무시 — 기각: 분류 모순이 남아 추후 census 오분류를 재유발.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. lane 축(가설-lane vs 영역-lane)을 리지드 분기로 명세할지
- **Decision taken**: 리지드 machinery 없이 둘 다 예시로 제시하고 orchestrator가 케이스별 선택하도록 둔다. 경쟁 가설이면 가설-lane(anti-anchoring, 옛 Agent A/B 부활), 출처 불분명·넓으면 영역-lane(broad sweep). 강제 분기 알고리즘은 두지 않는다(YAGNI, 토론 결정 3).
- **Alternatives considered**: (a) lane 선택 결정 트리를 명세 — 기각: 디버깅 휴리스틱을 과하게 형식화, 유연성 저해. (b) 단일 lane만 지원 — 기각: 두 상황 모두 실제 발생.
- **Confidence**: MEDIUM (구현 시 표현 강도는 작성자 재량)
- **User confirmation needed**: No

---

# Part 2: Implementation Plan

## Overview

이 계획은 investigate를 메인 루프 orchestrator skill로 재작성하고, read-only fan-out leaf로 **런타임 빌트인 범용 explore 역할**(claude `Explore`, codex `explorer`)을 재사용하며, 더 이상 쓰이지 않는 `investigate-agent`(claude `.md` + codex `.toml`)와 그 매니페스트 등록을 제거한다. "investigate-agent"는 현재 investigate의 전체 디버깅 계약을 보유한 internal sub-agent(`.claude/agents/investigate-agent.md`, 86줄)를 가리키며, wrapper가 단일 dispatch하던 대상이다. "orchestrator"는 메인 루프에서 실행되어 sub-agent fan-out이 가능한 skill을 뜻한다(implementation skill과 같은 역할). "leaf"는 orchestrator가 fan-out하는 단일 실행 단위인데, 여기서는 custom agent가 아니라 read-only 빌트인 explore 역할을 재사용한다.

이 프로젝트에는 전통적 테스트 프레임워크가 없으므로(`_sdd/env.md` 기준 정적 문서 워크플로우) 검증은 **정적 게이트(grep/diff)** + **런타임 smoke**로 한다.

## Scope

**In-scope**: claude/codex investigate SKILL.md 2종을 orchestrator로 재작성, claude/codex investigate-agent 파일 2종 삭제, marketplace.json `agents` 목록 정리.

**Out-of-scope**: `_sdd/spec/*` investigate 재분류(후속 spec-update-done — Part 1 Q3), 새 custom explore leaf 신설(빌트인 역할 재사용), 다른 wrapped 스킬 재분류, 디버깅 방법론 자체 변경.

## Components

| Component | 역할 | 대상 파일 |
|-----------|------|----------|
| investigate-claude | claude orchestrator skill | `.claude/skills/investigate/SKILL.md` |
| investigate-codex | codex orchestrator skill | `.codex/skills/investigate/SKILL.md` |
| agent-removal | 폐기된 investigate-agent 정의 제거 | `.claude/agents/investigate-agent.md`, `.codex/agents/investigate-agent.toml` |
| manifest | 플러그인 매니페스트 agents 목록 | `.claude-plugin/marketplace.json` |

## Contract/Invariant Delta Coverage

| Delta ID | 커버하는 Task | Validation |
|----------|--------------|-----------|
| C1 (wrapper→orchestrator) | T2 (claude), T3 (codex) | V1 |
| C2 (조건부 Explore 병렬 fan-out) | T2, T3 | V2 |
| C3 (기본 인라인, 넓고·모호할 때만 병렬) | T2, T3 | V2 |
| C4 (fix·검증·종합·Blast Radius·3-Strike·Scope Lock 인라인 소유) | T2, T3 | V1 |
| C5 (codex explorer 병렬 / 미가용 순차 degrade) | T3 | V3 |
| C6 (investigate-agent + 매니페스트 제거) | T4 (삭제), T5 (매니페스트) | V4 |
| I1, I2 (불변식·Report 계약 보존) | T2, T3 | V1, V5 |
| I3 (제거 격리, caller 무손상) | T1 (재확인 게이트), T4, T5 | V4 |
| V1~V5 (검증 게이트) | T6 | — |

## Implementation Phases

| Phase | 목표 | Tasks | 병렬성 |
|-------|------|-------|--------|
| Phase 1: Isolation Gate | 제거 안전성 재확인 | T1 | 단독 (게이트) |
| Phase 2: Orchestrator Rewrite | claude/codex skill 재작성 | T2, T3 | 파일 disjoint → 병렬 가능. 단 동일 orchestrator 계약을 인코딩하므로 의미적 parity 확인 필요(T3는 T2의 계약 구조를 참조 소비) |
| Phase 3: Removal & Manifest | agent 삭제 + 매니페스트 정리 | T4, T5 | 병렬 가능(파일 disjoint). 단 Phase 2 완료 후(wrapper dispatch 제거 후) 실행해야 dangling reference 없음 |
| Phase 4: Verification Gate | V1~V5 실행 | T6 | 단독 게이트. T2~T5 완료 후 |

> 병렬 판단 근거: T2(claude SKILL)와 T3(codex SKILL)는 Target Files가 disjoint하나, 둘 다 같은 orchestrator 계약(투 트랙·Report 형식·불변식)을 표현해야 하는 API 생산-소비형 의미적 충돌이 있다. 따라서 T3는 T2를 dependency로 두어 계약 구조를 먼저 확정한 뒤 codex-native 표현으로 따른다. T4/T5는 Phase 2 완료를 dependency로 둔다(생산-소비 순서: wrapper가 agent dispatch를 버린 뒤 agent를 삭제해야 dangling 없음).

## Task Details

### Task T1: investigate-agent 제거 격리 재확인 (정적 게이트)
**Component**: agent-removal
**Priority**: P0
**Type**: Infrastructure

**Description**: 코드 변경 전, `investigate-agent`(claude)와 `investigate_agent`(codex) 식별자의 모든 참조를 전수 grep해 caller가 wrapper 2종(`.claude/skills/investigate/SKILL.md`, `.codex/skills/investigate/SKILL.md`) + 매니페스트(`.claude-plugin/marketplace.json`) + 자기 파일 2종뿐임을 재검증한다(I3 — 제거 후 어떤 caller도 깨지지 않는다는 불변식). `.claude/skills/sdd-autopilot/` 및 다른 skill/agent에서의 dispatch 참조가 0건임을 확인한다. `_sdd/spec/*`·`_sdd/drafts/*` 내 문자열은 문서 참조이므로(코드 dispatch 아님) 후속 spec-update 대상으로 기록만 한다.

**Acceptance Criteria**:
- [ ] `investigate-agent`/`investigate_agent` grep 결과에서 코드 dispatch caller가 wrapper 2종 + 매니페스트 외에 없음을 확인
- [ ] autopilot에 investigate 참조 0건 확인
- [ ] 예상 밖 외부 dispatch가 발견되면 작업을 중단하고 보고 (그 경우 제거는 격리되지 않음)

**Target Files**:
- (없음 — 읽기·검증 전용 게이트 task. 코드 변경 없음)

**Technical Notes**: Covers I3, validated by V4. 이 task는 게이트이며 코드를 수정하지 않으므로 Target Files가 없다(읽기 전용 검증). 후속 task의 안전 전제를 확정한다.
**Dependencies**: 없음

### Task T2: claude investigate를 orchestrator로 재작성
**Component**: investigate-claude
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/skills/investigate/SKILL.md`를 thin wrapper(`Agent(subagent_type="sdd-skills:investigate-agent", ...)` 단일 dispatch)에서 **메인 루프 orchestrator 본문**으로 재작성한다(Contract C1 — investigate entrypoint를 orchestrator로 재정의). 본문은 다음 투 트랙을 인코딩한다:

- **문제정의 (인라인, 대화 기반)**: 증상·재현 조건·기대 동작·이미 시도한 가설을 대화에서 추출(기존 Mode B context-forwarding 유지). `_sdd/env.md` 존재 시 환경 적용.
- **탐색 트랙 (조건부 Explore 병렬 fan-out)**: 기본은 인라인 순차 증거 수집이고, **넓고·모호할 때만**(경쟁 가설 / 출처 불분명 / 대규모) 범용 read-only `Explore` agent를 병렬 fan-out한다(Contract C2, C3). lane 축은 가설-lane(경쟁 가설을 lane별로 분리해 anti-anchoring) / 영역-lane(코드 영역·증거 출처별 broad sweep) 둘 다 예시로 두되 리지드 분기 없이 orchestrator가 케이스별 선택(Part 1 Q4). 단순 단일파일 버그는 fan-out 없이 인라인 순차.
- **인라인 트랙 (그 외 전 단계)**: 근본원인 종합(Explore 결과 교차 비교 포함) → Blast Radius Gate → fix(write) → Fresh Verification → Investigation Report. fix는 write가 필요하므로 read-only Explore가 못 하고 orchestrator가 직접 수행(Contract C4).

3-Strike Escalation, Scope Lock, 근본원인 우선(Iron Law), Fresh Verification(이전 결과 재사용 금지·`_sdd/env.md` 미존재 시 `UNTESTED` 표기)을 orchestrator 인라인 소유로 보존한다(Invariant I1). Investigation Report 출력 형식(Problem / Root Cause / Fix(파일:라인) / Blast Radius / Verification PASS·FAIL·UNTESTED / Out-of-Scope Findings)을 보존한다(Invariant I2). 기존 "Source: investigate-agent가 단일 소스" pointer와 wrapper↔agent 문구를 제거하고, implementation skill과 같은 orchestrator role pointer로 대체한다. frontmatter `version`을 major bump한다(현재 3.0.0 — wrapper→orchestrator는 breaking 구조 변경이므로 major). 정확한 숫자는 구현 시 현재 값 기준으로 산정.

**Non-Goals**: 새 custom explore agent를 만들지 않는다(빌트인 `Explore` 재사용). fix를 별도 leaf로 분리하지 않는다(read-only Explore가 write 불가이므로 orchestrator 인라인). `_sdd/spec/*` 분류를 수정하지 않는다(후속 spec-update).

**Acceptance Criteria**:
- [ ] SKILL.md 본문이 orchestrator 구조(문제정의→조건부 Explore 병렬 fan-out→근본원인 종합→Blast Radius→fix·Fresh Verification 인라인)를 담는다
- [ ] `Agent(subagent_type=...investigate-agent...)` 단일 dispatch 문구가 제거된다
- [ ] 탐색 트랙에 claude `Explore` agent를 조건부 병렬 dispatch하는 지시가 있다(가설-lane/영역-lane 예시 포함)
- [ ] "기본 인라인 순차, 넓고·모호할 때만 병렬" 트리거가 명시된다
- [ ] 3-Strike·Scope Lock·근본원인 우선·Fresh Verification(UNTESTED 표기 포함)이 보존된다
- [ ] Investigation Report 6필드 형식이 보존된다
- [ ] frontmatter `version`이 bump된다
- [ ] orchestrator role pointer로 wrapper↔agent pointer를 대체한다

**Target Files**:
- [M] `.claude/skills/investigate/SKILL.md` -- wrapper→orchestrator 재작성

**Technical Notes**: Covers C1, C2, C3, C4, I1, I2; validated by V1, V2. claude `Explore`는 빌트인 read-only agent로 별도 plugin 파일이 없다(`.claude/agents/explore*` 부재 확인). dispatch는 implementation orchestrator의 `Agent(subagent_type="sdd-skills:...", ...)` 패턴을 따르되 leaf가 빌트인 `Explore`인 점만 다르다.
**Dependencies**: T1 (제거 격리 확인 게이트)

### Task T3: codex investigate를 orchestrator로 재작성 (explorer 병렬 + 순차 degrade)
**Component**: investigate-codex
**Priority**: P0
**Type**: Refactor

**Description**: `.codex/skills/investigate/SKILL.md`를 T2와 동일한 orchestrator 계약(투 트랙·Report 형식·불변식)으로 재작성하되, dispatch 표현을 codex-native로 한다(Contract C1). 탐색 트랙의 병렬 fan-out은 `spawn_agent(agent_type="explorer")` + `wait_agent`로 표현한다 — census 확인 결과 `.codex/agents/README.md` L60-62가 `spawn_agent(agent_type="explorer")`를 read-only investigation 표준 역할로 명시하므로 이것이 1차 경로다(Contract C5). 동등 read-only explore 역할이 런타임에 미가용한 경우 순차 인라인 증거 수집으로 graceful degrade한다(정확성 동일, 병렬만 상실). 기존 `spawn_agent(agent_type="investigate_agent", ...)` 단일 dispatch와 wrapper↔agent pointer를 제거한다. frontmatter `version`을 T2와 동일하게 bump한다.

**Non-Goals**: codex 전용 explore leaf agent를 신설하지 않는다(빌트인 `explorer` 역할 재사용). claude와 본문 내용을 기계적으로 mirror하지 않되 동일 orchestrator 계약은 parity로 유지한다.

**Acceptance Criteria**:
- [ ] SKILL.md 본문이 T2와 동일한 orchestrator 구조·투 트랙·불변식을 codex-native 표현으로 담는다
- [ ] 탐색 fan-out이 `spawn_agent(agent_type="explorer")` + `wait_agent` 병렬로 표현된다
- [ ] explorer 역할 미가용 시 순차 인라인 graceful degrade가 명시된다
- [ ] `spawn_agent(agent_type="investigate_agent", ...)` 단일 dispatch 문구가 제거된다
- [ ] Investigation Report 6필드 형식·3-Strike·Scope Lock·Fresh Verification(UNTESTED 표기)이 보존된다
- [ ] frontmatter `version`이 T2와 동일하게 bump된다

**Target Files**:
- [M] `.codex/skills/investigate/SKILL.md` -- wrapper→orchestrator 재작성 (codex-native explorer fan-out)

**Technical Notes**: Covers C1, C2, C3, C4, C5, I1, I2; validated by V1, V2, V3, V5. codex census 근거: `.codex/agents/README.md` L60 `spawn_agent(agent_type="explorer")` for read-only investigation. codex implementation orchestrator(`spawn_agent(agent_type="implementation_agent")`+`wait_agent`) 패턴을 따르되 leaf가 빌트인 `explorer` 역할인 점만 다르다.
**Dependencies**: T2 (동일 orchestrator 계약 구조를 먼저 확정 — 의미적 parity 소비 관계)

### Task T4: investigate-agent 정의 파일 삭제 (claude + codex)
**Component**: agent-removal
**Priority**: P0
**Type**: Refactor

**Description**: 더 이상 dispatch되지 않는 investigate-agent 정의를 삭제한다(Contract C6). `.claude/agents/investigate-agent.md`(86줄)와 `.codex/agents/investigate-agent.toml`을 제거한다. 이 파일들이 보유하던 디버깅 계약은 T2/T3에서 orchestrator skill로 이전되었으므로 정보 손실이 없다. T2/T3에서 wrapper의 agent dispatch가 제거된 후 실행해야 dangling reference가 생기지 않는다.

**Acceptance Criteria**:
- [ ] `.claude/agents/investigate-agent.md` 파일이 삭제된다
- [ ] `.codex/agents/investigate-agent.toml` 파일이 삭제된다
- [ ] 삭제 후 두 SKILL.md(T2/T3 결과)에 이 파일들을 가리키는 dispatch·pointer가 남지 않는다

**Target Files**:
- [D] `.claude/agents/investigate-agent.md` -- 폐기된 agent 정의 삭제
- [D] `.codex/agents/investigate-agent.toml` -- 폐기된 codex agent 정의 삭제

**Technical Notes**: Covers C6, I3; validated by V4. 참조자 격리는 T1에서 재확인됨.
**Dependencies**: T2, T3 (wrapper dispatch 제거 완료 후 — 생산-소비 순서)

### Task T5: marketplace.json agents 목록에서 investigate-agent 제외
**Component**: manifest
**Priority**: P0
**Type**: Infrastructure

**Description**: `.claude-plugin/marketplace.json`의 `agents` 배열에서 `./.claude/agents/investigate-agent.md` 항목(L51)을 제거한다(Contract C6). `skills` 배열의 `./.claude/skills/investigate` 항목은 유지한다 — investigate는 orchestrator가 되어도 여전히 사용자 진입점 skill이다.

**Acceptance Criteria**:
- [ ] `agents` 배열에 `investigate-agent.md`가 없다
- [ ] `skills` 배열의 `./.claude/skills/investigate` 항목은 유지된다
- [ ] JSON이 유효하며 trailing comma 등 구문 오류가 없다

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- agents 목록에서 investigate-agent.md 제외

**Technical Notes**: Covers C6, I3; validated by V4. codex agent toml은 매니페스트에 등록되지 않으므로(codex는 `.codex/agents/` 디렉토리 기반) 이 task는 claude 매니페스트만 다룬다.
**Dependencies**: T4 (파일 삭제와 매니페스트 정리는 제거 정합을 함께 이룸 — 동일 제거 단위)

### Task T6: 검증 게이트 (V1~V5)
**Component**: (verification — 모든 컴포넌트 횡단)
**Priority**: P0
**Type**: Test

**Description**: Part 1 `Validation Plan`의 V1~V5를 실행한다(Part 1 Implementation Plan step 6의 Part 2 task home). 정적 게이트(grep/diff): orchestrator 구조·Explore/`explorer` dispatch 존재·`investigate-agent` 단일 dispatch 부재(V1)·트리거 문자열(V2 정적)·codex explorer 경로+degrade(V3)·agent 파일 삭제·매니페스트 미등록·코드 dispatch 잔존 0건(V4)·claude/codex parity(V5). 가능하면 런타임 smoke(V2): reload 후 단순 버그=Explore 0회 / 넓은 버그=Explore ≥2 병렬. 실패 항목은 해당 task로 복귀. reload 불가 시 런타임 DEFERRED 명시·사용자 보고.

**Acceptance Criteria**:
- [ ] V1~V5 정적 게이트 전부 PASS (각 V의 Evidence 기준 충족)
- [ ] V2 런타임 smoke 2케이스 PASS, 또는 reload 불가 시 DEFERRED 명시
- [ ] 실패 시 해당 task(T2~T5) 복귀 후 재검증

**Target Files**:
- [M] `_sdd/drafts/2026-06-03_feature_draft_investigate_orchestrator.md` -- 검증 결과 기록(검증 전용, 코드 변경 없음)

**Technical Notes**: Covers V1~V5(전체). 게이트 task — 통과 후 커밋.
**Dependencies**: T2, T3, T4, T5

## Parallel Execution Summary

| Phase | Tasks | 병렬 가능 | 근거 |
|-------|-------|----------|------|
| Phase 1 | T1 | 단독 | 게이트 task. 후속 전제 |
| Phase 2 | T2, T3 | 순차 (T3 deps T2) | 파일은 disjoint하나 동일 orchestrator 계약을 양 플랫폼에 인코딩하는 생산-소비 의미적 충돌 → T2가 계약 확정, T3가 codex-native 소비 |
| Phase 3 | T4, T5 | 병렬 가능 | Target Files disjoint(agent 파일 삭제 vs 매니페스트 수정), dependency edge 없음. 단 둘 다 Phase 2 완료 필요(dangling 방지) |
| Phase 4 | T6 | 단독 | 검증 게이트. T2~T5 완료 후 |

> 단순 변경 규모(5 task, 파일 5개)라 phase 분리는 의미적 충돌(생산-소비 순서, parity)만으로 결정했다. file-disjoint만으로는 T2/T3를 병렬화할 수 있으나 parity 정합을 위해 순차로 내렸다(확신 없으면 순차).

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| investigate-agent 제거가 미발견 caller를 깸 | T1 격리 게이트에서 전수 grep 재확인, 외부 dispatch 발견 시 중단 (Part 1 Q2, I3) |
| claude/codex orchestrator 계약 drift (parity 상실) | T3를 T2 dependency로 두어 동일 계약 구조 후 codex-native 표현. V5가 parity 검증 |
| codex explorer 역할이 일부 런타임에 미가용 | C5 graceful degrade — 순차 인라인 fallback. 정확성 동일, 병렬만 상실 (Part 1 Q1) |
| spec 분류 drift (components.md L33·DECISION_LOG.md가 investigate를 wrapper로 분류한 채 남음; main.md는 무관) | 후속 spec-update-done으로 인계, 정확한 surface(components.md L33 + DECISION_LOG.md)를 Open Question에 명시 (Part 1 Q3) |
| 단순 버그에 fan-out 오버헤드 | C3 "기본 인라인 순차, 넓고·모호할 때만 병렬" 트리거를 본문에 명시 |

## Open Questions

- **OQ1 (Part 1 Q3 인계)**: investigate 분류를 wrapper→orchestrator(Explore 재사용)로 갱신하는 작업은 이 draft 범위 밖이며 후속 `spec-update-done` 대상이다. **갱신 surface(grep 확인)**: `_sdd/spec/components.md` L33(investigate "wrapper -> agent" 분류 행), `_sdd/spec/DECISION_LOG.md`(2026-06-03 entry의 "fan-out 없는 9종" 목록·Mode B 목록·Agent 도구 제거 목록 3곳). `main.md`는 investigate 문자열 0건(일반 규칙만)이라 대상 아님. 머지 후 그 surface에 분류 drift가 존재함을 인지·인계한다.
- **OQ2 (Part 1 Q4)**: lane 축(가설-lane/영역-lane)의 본문 표현 강도는 작성자 재량. 리지드 결정 트리는 두지 않는다(YAGNI). Confidence MEDIUM.
- **plan-review 반영(`_sdd/implementation/2026-06-03_plan_review_investigate_orchestrator.md`, CLEAR)**: M1(spec 인계 surface 정정 — main.md 아님, components.md L33 + DECISION_LOG.md grep 확인) + M2(V2 런타임 smoke 2케이스·V4 grep 제외집합 조작화) + Low(검증 task T6 추가로 Part1 step6↔Part2 매핑 갭 해소, 버전 하드코딩 완화) 반영.

---

## Self-Containment Check (Hard Rule 11)

**Pass 1 — 외부 참조의 inline purpose 동반 확인** (검토 섹션: Overview, Components, Coverage table, Task T1~T5, Parallel Summary, Risks, Open Questions = 9개 섹션):
- Part 1↔Part 2 참조는 모두 `ID + inline purpose` 형식 충족 (예: "Contract C2 — 조건부 Explore 병렬 fan-out", "Invariant I2 — Report 계약 보존", "Part 1 Q3 인계"). bare ID 단독 참조 없음.
- 외부 파일 참조에 재진술 동반: `.claude/agents/investigate-agent.md`는 "현재 investigate 전체 디버깅 계약을 보유한 internal sub-agent(86줄)"로 재진술. `.codex/agents/README.md` L60-62는 "explorer를 read-only investigation 표준 역할로 명시"로 재진술. marketplace.json L51은 "agents 배열의 investigate-agent.md 등록 항목"으로 재진술.
- 고유 용어 inline 정의: "orchestrator"(메인 루프 fan-out 가능 skill), "leaf"(fan-out 단일 실행 단위, 여기선 빌트인 explore 재사용), "investigate-agent"(폐기 대상 internal agent), "투 트랙"(탐색 read-only fan-out / 그 외 인라인) 모두 Overview 또는 최초 사용 시 정의.
- **발견 갭**: 초안에서 T1의 Target Files가 비어 있어 reader가 "Target Files 누락"으로 오해할 소지 → Technical Notes에 "읽기 전용 검증 게이트라 코드 변경 없음"을 명시해 보완(Hard Rule 8은 코드 변경 task에 Target Files를 요구하며, 이 task는 의도적으로 변경 없음을 grounding). **보완 완료: Yes**.

**Pass 2 — 생초 독자 readthrough** (작성 대화·discussion 문서 미열람 가정):
- "census"가 무엇을 가리키는지: Overview·T3 Technical Notes·Part 1 C5에서 "codex 런타임에 explore 역할이 있는지 확인"으로 inline 설명됨 → 갭 없음.
- "graceful degrade"의 의미: C5·T3에서 "역할 미가용 시 순차 인라인 fallback, 정확성 동일·병렬만 상실"로 자립 설명 → 갭 없음.
- **발견 갭**: 초안 Parallel Summary에서 T2/T3를 왜 병렬 안 하는지(파일 disjoint인데)가 생초 독자에게 불명확 → "동일 orchestrator 계약을 양 플랫폼에 인코딩하는 생산-소비 의미적 충돌" 근거를 Parallel Summary 각주와 Phase 표에 추가해 보완. **보완 완료: Yes**.

**Minimum-Code self-check (Hard Rule 12)**: 모든 AC가 요청된 동작(orchestrator 재작성·Explore fan-out·agent 제거·매니페스트 정리)에서 직접 도출됨. 사변적 형용사("future-proof/extensible/configurable") 미사용. "graceful degrade"는 사변적 옵션이 아니라 C5의 런타임 역량 조건부 동작(근거: codex explorer 미가용 케이스)으로 근거가 task에 명시됨. 새 추상화·옵션·설정 가능성·도달 불가 에러 처리 미도입(빌트인 explore 재사용, custom leaf 미신설).

---

## 검증 결과 (T6, 2026-06-03 실행)

구현 방식: orchestrator(메인 루프) 직접 순차 편집 + 정적 게이트 (self-referential 리팩터).

| ID | 결과 | 근거 |
|----|------|------|
| V1 | **PASS** | claude SKILL이 orchestrator 구조(Problem Definition·Root Cause Synthesis·Blast Radius·Fix & Verify·Fresh Verification 인라인 + 3-Strike·Scope Lock·Investigation Report 6필드). `Agent(subagent_type=...investigate-agent...)` dispatch 0 |
| V2 | **PASS(정적)** / 런타임 DEFERRED | Explore 조건부 dispatch 1 + "넓고·모호할 때만" 트리거 3. 런타임 smoke(단순=Explore 0회 / 넓은=≥2 병렬)는 reload 의존이라 DEFERRED |
| V3 | **PASS** | codex `spawn_agent(agent_type="explorer")`+`wait_agent` 1, graceful degrade 명시, `investigate_agent` dispatch 0 |
| V4 | **PASS** | `.claude/agents/investigate-agent.md`·`.codex/agents/investigate-agent.toml` 삭제됨. 매니페스트 investigate-agent 0건. 코드 surface dispatch 0(잔존 2건은 Role Pointer의 "구 agent 제거됨" 이력 주석 — dispatch 아님) |
| V5 | **PASS** | 매니페스트 JSON 유효. claude/codex SKILL 83줄 parity, 동일 orchestrator 계약·dispatch만 플랫폼별 |

**게이트 종합**: 정적 V1~V5 전부 PASS. V6 런타임 smoke만 reload 의존으로 사용자 확인 대상. 구현은 계약 수준 완결. 후속: components.md L33 + DECISION_LOG.md를 spec-update-done으로 갱신(OQ1).
