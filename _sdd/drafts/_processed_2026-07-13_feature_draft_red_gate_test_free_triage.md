# Feature Draft: RED 게이트 3-way triage — non-falsifiable content의 test-free 예외

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`implementation` 스킬(및 `sdd-autopilot`의 동형 RED 게이트)의 test-first 파이프라인은 현재 모든 task를 무조건 2-stage(Stage A test-author → RED 게이트 → Stage B impl)로 태운다. 테스트 프레임워크 부재 자산의 graceful degradation(I4)도 면제가 아니라 형태 변경이라, 문서 산문·설명·주석 같은 non-falsifiable content 작업에도 "파일에 이 문구 있나" 수준의 동어반복(tautology) grep 체크를 RED artifact로 억지로 만들게 된다 — 검증 가치는 낮고 파이프라인만 무겁다.

이를 해소하기 위해 RED 게이트를 2분기에서 **3-way triage**로 확장한다:

- **(a) test**: 관찰 가능한 코드 동작 → 실제 실패 테스트로 RED 캡처 (기존)
- **(b) structural-check**: 실질 있는 구조/존재(함수·심볼·config 키 추가 등) → grep/구조 acceptance check로 RED 캡처 (기존 graceful degradation I4의 명명)
- **(c) test-free (신규)**: non-falsifiable content(산문·설명 문서·주석) → Stage A(test-author) 스킵, RED artifact 없음. Step 6 리뷰 게이트(correctness ∥ simplicity)가 유일한 품질 관문

판정 주체는 **RED 게이트 런타임 triage**다(이미 falsifiability를 판정하는 지점의 자연 확장). feature-draft task별 Verification 필드 안과 사용자 `--no-tdd` 플래그 안은 기각됐다(전자는 스키마 팽창+남발 위험, 후자는 원칙 부재). "간단한 구현이라서"는 (c) 자격이 아니다 — 간단 opt-out은 RED 게이트 존재 이유(`should work` 자기보고 차단)를 침식하므로 기각됐다.

## Scope Delta

### In Scope

- `implementation` 스킬 RED 게이트의 3-way triage 확장 (claude·codex SKILL.md 미러 짝) — canonical surface
- `test-author-agent` 미러 짝: non-falsifiable AC의 (c) 후보 신호 반환 참조
- `implementation-agent` 미러 짝: test-free dispatch 입력 변형 수용 (근거 없는 테스트 부재는 여전히 `BLOCKED`)
- `sdd-autopilot` 동형 RED 게이트 표면 (orchestrator-contract.md §2 + SKILL.md dispatch controller 서술 + orchestrator 생성 shape 참조 example `sample-orchestrator.md`, claude·codex 미러 짝)
- `_sdd/spec/main.md`의 test-first 불변식 서술·결정 테이블 행 갱신 (본 Part 1이 `spec-sync` 입력)

### Out of Scope

- feature-draft task 스키마 변경 (task별 Verification/triage 필드 추가 안 함 — 판정은 런타임)
- 사용자 노출 opt-out 플래그 (`--no-tdd` 류)
- Step 6/checkpoint 리뷰 게이트 구조·exit 정책 변경
- Minimum-Code Mandate, Regression Iron Rule, Verification Gate 등 기존 Hard Rule 변경
- (a)/(b) 경로의 기존 falsifiability 판정 규칙(assertion 단계 실패 인정, import/collection-only 배제, 구분 불가 시 리뷰 판정 강등) 변경

### Guardrail Delta

- **(b)/(c) 경계**: grep 체크가 실질 검증(함수·심볼·config 키 존재 등)이면 (b), 단순 문구/존재 확인 동어반복이면 (c). test/structural check가 기술적으로 가능하면 (a)/(b)로 간다 — (c)는 오직 falsifiable하게 검증할 관찰 대상이 실제로 없을 때. 문서 자산의 중간 사례(이 repo의 지배적 자산): 문서 내 토큰/문구가 실제 계약·구조를 강제하면(게이트 판정 라벨·계약 토큰 등) (b), 단순 문구 존재 확인이면 (c)
- **무근거 (c) 강등 금지**: (c) 분류는 RED 게이트가 명시 근거(왜 non-falsifiable인지)와 함께 기록해야 한다 — 기록 홈은 RED 증거와 동일한 orchestrator 소유 progress 기록 위치이며, checkpoint 리뷰 dispatch 입력에 그 근거를 전달한다
- **안전망 불변**: (c) task도 Step 6 리뷰 게이트는 반드시 돈다 — test만 면제, 품질 게이트는 불면제

## Persistent Spec Implications

`_sdd/spec/main.md`에 남아야 할 계약:

- **Guardrails의 test-first 불변식 bullet** ("implementation-scoped 구현의 test-first는 …" 및 graceful-degradation bullet): RED 게이트가 task AC 성격을 (a) test / (b) structural-check / (c) test-free 3-way로 triage하며, (c)는 non-falsifiable content 한정 + 명시 근거 기록 + Stage A/RED artifact 면제 + 리뷰 게이트 불면제. (a)/(b)의 falsifiable 집행 성격은 불변(test-after 새는 경로 차단)
- **결정 테이블 "implementation test-first" 행**: 3-way triage 예외와 그 유지 이유(동어반복 acceptance check 강제 제거, 판정 주체는 런타임 RED 게이트) 반영
- graceful-degradation 분기 기준의 canonical surface가 `implementation` 스킬 RED 게이트 서술이라는 기존 계약은 3-way triage 기준까지 포괄하도록 확장 유지
<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

Part 1의 3-way triage delta를 문서/스킬 repo의 6개 미러 짝 표면에 전개한다. canonical surface는 `implementation` SKILL의 RED 게이트 서술이며(자기선언 문장 보유), 나머지 표면은 참조 또는 동형 반영이다. 이 repo는 테스트 프레임워크 없는 문서 repo이므로 검증은 grep/구조 acceptance check(1등급)와 리뷰어 rubric 판정(2등급)으로 수행한다.

## Scope

Part 1 `Scope Delta`와 동일 범위. Part 2는 그중 코드(스킬/agent 문서) 표면만 task로 전개하며, `_sdd/spec/main.md`는 `spec-sync` 소관이라 어느 task의 Target Files에도 포함하지 않는다.

## Contract/Invariant Delta and Coverage

| ID | Type | Change | Covered By | Validated By |
|----|------|--------|------------|--------------|
| C1 | Modify | RED 게이트가 task AC 성격을 3-way triage((a) test / (b) structural-check / (c) test-free)로 판정한다. (c)는 Stage A 스킵 + RED artifact 없음 (implementation SKILL + autopilot 동형 게이트) | T1, T4 | V1, V4 |
| C2 | Add | (b)/(c) 경계 계약: grep 체크가 실질 구조/존재 검증이면 (b), 단순 문구 존재 동어반복이면 (c); 문서 내 토큰이 실제 계약·구조를 강제하면 (b) 귀속; "간단한 구현"은 (c) 자격 아님 | T1 | V1, V6 |
| C3 | Modify | implementation-agent 입력 계약: orchestrator가 test-free triage 분류 근거를 전달하면 고정 테스트/RED 증거 없이 AC 기준 최소 구현으로 진행. 근거 없는 테스트 부재는 여전히 `BLOCKED` | T3 | V3 |
| C4 | Modify | test-author-agent 계약: non-falsifiable AC는 테스트/acceptance check를 만들지 않고 (c) 후보 신호를 반환한다 (판정 canonical은 RED 게이트) | T2 | V2 |
| I1 | Preserve | (a)/(b) 경로에서 RED 게이트의 falsifiable 집행 성격 불변 — test-after 새는 경로 차단. impl-agent의 무근거 테스트 부재 `BLOCKED` 가드 잔존 | T1, T3 | V5, V3 |
| I2 | Add | (c) 분류는 명시 근거(왜 non-falsifiable인지)와 함께 RED 증거와 동일한 progress 캡처 홈에 기록되고 checkpoint 리뷰 dispatch 입력에 전달된다 — 무근거 (c) 강등 금지 | T1, T4 | V1, V4 |
| I3 | Add | (c) task도 Step 6 checkpoint 리뷰 게이트(correctness ∥ simplicity)를 반드시 통과한다 — test만 면제, 품질 게이트 불면제 | T1, T4 | V1, V4 |
| I4 | Add | 각 표면의 claude·codex 미러 짝은 판정 토큰 수준에서 동치다 (dispatch 어휘 `Agent`/`spawn_agent` 차이 제외) | T1, T2, T3, T4 | V1, V2, V3, V4 |

## Touchpoints

digest가 제공한 표면 목록을 현재 코드로 실측 재검증했다. line number는 이 census에만 기록한다 (2026-07-13 실측 기준).

**1. `implementation` SKILL 미러 짝 — canonical surface (T1)**

- `.claude/skills/implementation/SKILL.md`: AC3 "wave별 2-stage로 leaf를 dispatch" (L18), Hard Rule "Test-first는 2-stage로 분리" (L27), Step 4 heading·cross-wave 서술 (L118)과 파이프라인 의사코드 블록 (L120-133), RED 게이트 서술 (L164-175) 중 graceful degradation (I4) + "이 RED 게이트 서술이 I4 graceful-degradation 분기 기준의 canonical surface다" 자기선언 (L174), Stage B 입력 블록 "고정 실패 테스트 + RED 증거" (L200-203), GREEN 게이트 (L207-209), Sequential Fallback (L213)
- `.codex/skills/implementation/SKILL.md`: 동형 — AC3 (L49), Hard Rule 2 (L58), Step 4 의사코드 (L145-162), RED 게이트 (L192-203), Stage B 입력 (L205 이하). spawn/close_agent 어휘만 다름

**2. `test-author-agent` 미러 짝 (T2)**

- `.claude/agents/test-author-agent.md`: AC5 "프레임워크 부재 자산이면 grep/구조 점검 acceptance check" (L20), Step 3 프레임워크 부재 문단 (L65), Step 4 canonical 참조 (L70), "안 하는 것"의 RED 게이트 판정 소유 서술 (L104)
- `.codex/agents/test-author-agent.toml`: 동일 anchor (L20, L65, L70, L104) — codex는 canonical 경로를 `.codex/skills/implementation/SKILL.md`로 표기

**3. `implementation-agent` 미러 짝 (T3) — digest 표면 목록 밖 실측 발견 (Q1)**

- `.claude/agents/implementation-agent.md`: 서두 "입력에 고정 테스트/RED 증거가 없으면 … `BLOCKED`로 보고한다 (테스트 없는 직접 호출은 지원 계약 밖 — test-after 재개방 방지)" (L12), 입력 누락 처리 (L35), Step 1 중단 규칙 (L53), Autonomous Decision-Making의 BLOCKED 분기 (L111). 이 가드는 현재 문면 그대로면 (c) task의 Stage B dispatch를 `BLOCKED`로 차단한다 — test-free 경로가 성립하려면 반드시 수정해야 하는 표면
- `.codex/agents/implementation-agent.toml`: 동일 anchor (L12, L35, L53, L111)

**4. `sdd-autopilot` 동형 RED 게이트 표면 (T4)**

- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`: §2 Implementation Dispatch Controller — Stage B 정의 "orchestrator 소유 RED 게이트" (L86), (b) RED 게이트 서술 (L93), (c) impl 병렬 dispatch "RED 게이트를 통과한 task마다" (L94), cross-wave "한 wave가 GREEN 게이트를 닫은 뒤" 순차 문면 (L95)
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`: 동일 anchor (L106, L113, L114, L115)
- `.claude/skills/sdd-autopilot/SKILL.md`: Implementation Dispatch Controller bullet의 "(c) RED 통과 task에 `sdd-skills:implementation-agent` 병렬 dispatch" 문구 (L180) — test-free task를 배제하는 유일한 SKILL.md 문면. 인접 bullet L181과 L254·L259의 3단계 언급은 orchestrator-contract §2 pointer/구조 재진술이라 §2 갱신 후에도 모순 없음 → 수정 대상 아님
- `.codex/skills/sdd-autopilot/SKILL.md`: 동일 구조 — dispatch controller bullet (L204; L205·L279·L282는 위와 같은 이유로 수정 대상 아님)
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`: autopilot SKILL이 orchestrator 생성 shape 참조로 지정하는 example 표면 (리뷰 H1 실측 발견). Example A Step 4 프롬프트 "autopilot이 닫은 RED 게이트가 넘긴 고정 실패 테스트 + RED 증거를 입력으로 GREEN→REFACTOR만 수행하세요" (L93)가 전 task RED 증거를 전제하고, 양 example의 step-kind 서술 "test-author 병렬 dispatch → orchestrator RED gate → implementation 병렬 dispatch" (L95, L256)에 triage 분기가 없다 — 미갱신 시 생성된 orchestrator가 (c) test-free 경로를 배제하는 shape로 유도된다. Stage agents 라벨 행(L78, L244)은 (a)/(b) 경로의 agent 명명이라 무변경, review-fix gate의 correctness test-first fix prompt contract(L110, L118, L122, L283, L291, L295)는 T4 Technical Notes의 §6 무변경 근거와 동일하게 무변경
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`: 동일 anchor (Example A 프롬프트 L92, step-kind L94·L254) — spawn/close_agent 어휘만 다름

**5. `_sdd/spec/main.md` — Part 1 delta 대상 (Part 2 task 없음)**

- Guardrails test-first 불변식 bullet (L76-79), 결정 테이블 "implementation test-first" 행 (L131). `spec-sync`가 Part 1을 머지하므로 어느 task의 Target Files에도 넣지 않는다 (Spec 파일 불가침)

## Task Details

### Task T1: implementation SKILL RED 게이트를 3-way triage로 확장 (claude·codex 미러)
**Priority**: P0
**Type**: Feature

**Description**: canonical surface인 RED 게이트 서술을 2분기에서 3-way triage로 확장해, non-falsifiable content task가 동어반복 acceptance check 없이 Stage B로 직행하게 한다. 판정을 이 게이트에 두는 근거: 이미 falsifiability를 판정하는 지점이라 자연 확장이며, plan 스키마 팽창(task별 Verification 필드)과 원칙 없는 opt-out(사용자 플래그)을 피한다 — Part 1 Change Summary의 확정 결정. triage 자체는 RED 게이트가 소유하되 실행 시점은 wave의 Stage A dispatch 직전이다((c) task에 불필요한 test-author dispatch를 만들지 않기 위함 — Q4). 수정 지점은 Touchpoints의 implementation SKILL census 참조.

**Acceptance Criteria**:
- [ ] 두 미러의 RED 게이트 서술에 (a) test / (b) structural-check / (c) test-free 3분기가 존재하고, canonical surface 자기선언 문장이 "I4 graceful-degradation 분기 기준"에 더해 3-way triage 기준까지 포괄한다고 갱신된다 (V1)
- [ ] (b)/(c) 경계 기준이 존재한다: 실질 구조/존재 검증(함수·심볼·config 키 등)이면 (b), 단순 문구/존재 확인 동어반복이면 (c); "간단한 구현이라서"는 (c) 자격이 아니며 test/structural check가 기술적으로 가능하면 (a)/(b)로 간다는 문장, 그리고 문서 자산 중간 사례 기준(문서 내 토큰이 실제 계약·구조를 강제하면 (b), 단순 문구 존재 확인이면 (c)) 포함 (V1, V6)
- [ ] (c) 분류 시 명시 근거(왜 non-falsifiable인지) 기록 의무 + Stage A 스킵 + RED artifact 없음 + Step 6 리뷰 게이트 불면제 문구가 존재하고, 근거의 기록 홈(RED 증거와 동일한 orchestrator 소유 progress 기록 위치)과 Step 6 checkpoint 리뷰 dispatch 입력에 (c) triage 근거를 포함할 의무가 명시된다 (V1)
- [ ] Hard Rule "Test-first는 2-stage로 분리"에 (c) 예외 문장이, AC3의 2-stage dispatch 강제 문구에 test-free 경로가 반영된다 (V1)
- [ ] Step 4 파이프라인 의사코드에 triage 수행(Stage A dispatch 전)과 (c) task의 Stage A 스킵 분기가 반영된다 (V1)
- [ ] Stage B 입력·GREEN 게이트 서술에 (c) task 경로가 반영된다: 고정 실패 테스트/RED 증거 대신 triage 분류 근거를 전달하고, (c) task는 GREEN 증거 면제(검증할 테스트 없음)하되 Step 5 post-group 회귀 스윕과 Step 6 리뷰 게이트는 유지 (V1)
- [ ] (a)/(b)의 기존 falsifiability 판정 규칙 문구(assertion 단계 실패 인정, 순수 import/collection/syntax 실패 배제, 구분 불가 시 리뷰 판정 강등, (b)의 exit code/diff RED 캡처)가 잔존한다 (V5)

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.codex/skills/implementation/SKILL.md`

**Technical Notes**: Covers C1, C2, I1, I2, I3, I4. Validated by V1, V5, V6. test-author가 (c) 후보 신호를 반환하는 사후 경로(T2)에서도 최종 판정·근거 기록은 이 게이트 소유임을 명시한다.

### Task T2: test-author-agent에 (c) 후보 신호 참조 추가 (claude·codex 미러)
**Priority**: P1
**Type**: Feature

**Description**: triage가 Stage A dispatch 전에 놓친 non-falsifiable AC를 test-author가 억지 동어반복 check로 메꾸지 않도록, 테스트 미작성 + (c) 후보 신호 반환 경로를 참조로 추가한다. 기존 canonical 참조 패턴(임계값 미복제)을 유지하는 이유: 경계 기준이 두 곳에 존재하면 drift가 두 모델 판정을 가른다. 수정 지점은 Touchpoints의 test-author-agent census 참조.

**Acceptance Criteria**:
- [ ] 두 미러에 "AC가 non-falsifiable content(산문·설명 문서·주석)뿐이면 테스트/acceptance check를 만들지 않고 결과에 (c) test-free 후보 신호 + 사유를 반환한다. 판정 canonical은 `implementation` SKILL RED 게이트"라는 취지의 문구가 존재한다 (V2)
- [ ] (b)/(c) 경계 기준·임계값 상세는 이 agent 본문에 복제되지 않고 canonical surface 참조로만 존재한다 (V2)

**Target Files**:
- [M] `.claude/agents/test-author-agent.md`
- [M] `.codex/agents/test-author-agent.toml`

**Technical Notes**: Covers C4, I4. Validated by V2. AC5·Step 3·Step 4의 기존 canonical 참조 문장에 인접 배치한다.

### Task T3: implementation-agent에 test-free dispatch 입력 변형 수용 (claude·codex 미러)
**Priority**: P0
**Type**: Feature

**Description**: Touchpoints의 implementation-agent census가 실측한 차단 가드에 (c) 경로 예외를 연다. orchestrator가 RED 게이트 triage 분류 근거를 입력에 담아 전달하는 경우만 예외로 열고, 그 외 테스트 부재는 여전히 `BLOCKED`로 남겨 test-after 재개방 방지 목적(가드 원문에 명시된 근거)을 보존한다.

**Acceptance Criteria**:
- [ ] 두 미러에서 입력에 "test-free 분류 + RED 게이트 triage 근거"가 있으면 고정 테스트/RED 증거 없이 task AC 기준 최소 구현으로 진행한다는 문구가 서두 계약·입력 누락 처리·Step 1·Autonomous Decision-Making의 BLOCKED 분기에 일관 반영된다 (V3)
- [ ] triage 근거 없는 고정 테스트/RED 증거 부재는 여전히 `BLOCKED`라는 문구와 "test-after 재개방 방지" 근거가 잔존한다 (V3)

**Target Files**:
- [M] `.claude/agents/implementation-agent.md`
- [M] `.codex/agents/implementation-agent.toml`

**Technical Notes**: Covers C3, I1(가드 보존 측), I4. Validated by V3. 이 표면은 digest 열거 밖 실측 발견 (경위·확장 근거는 Q1).

### Task T4: sdd-autopilot 동형 RED 게이트 표면에 3-way triage 반영 (claude·codex 미러)
**Priority**: P1
**Type**: Feature

**Description**: autopilot은 Stage B로 동형 RED 게이트를 소유하므로 orchestrator-contract §2와 SKILL.md dispatch controller 서술이 (c) task를 배제하지 않게 한다. orchestrator 생성 shape 참조인 sample-orchestrator example 미러 짝도 포함한다 — 미갱신 example이 생성된 orchestrator를 (c) 배제 형태로 유도하기 때문 (Touchpoints census의 example 실측 참조). 경계 기준 상세는 복제하지 않고 canonical surface(T1) 참조로 갈음한다 — T2와 같은 drift 근거. 수정 지점은 Touchpoints의 sdd-autopilot census 참조 (pointer성 재진술 지점은 수정 대상 아님).

**Acceptance Criteria**:
- [ ] orchestrator-contract 미러 짝의 §2 Stage B 서술에 3-way triage((c)는 Stage A/RED 스킵 + 명시 근거 기록 + 리뷰 게이트 불면제 + GREEN 증거 면제(Q3 결정의 동형 반영 — cross-wave GREEN 순차 문면 포함))와 `implementation` SKILL RED 게이트 canonical 참조가 존재한다 (V4)
- [ ] orchestrator-contract 미러 짝의 Stage C(impl dispatch) 서술이 "RED 게이트를 통과한 task"에 더해 "(c) test-free로 분류된 task(triage 근거 전달)" 경로를 포함한다 (V4)
- [ ] autopilot SKILL 미러 짝의 dispatch controller bullet에서 "(c) RED 통과 task에" 한정 문구가 test-free task 경로를 포함하도록 갱신된다 — Touchpoints census가 확정한 각 미러 1곳, 그 외 pointer성 재진술 지점 무변경 (V4)
- [ ] sample-orchestrator 미러 짝에서 Touchpoints census가 확정한 수정 지점(Example A Step 4 프롬프트 + 양 example step-kind 서술) 전체가 (c) test-free 경로를 배제하지 않게 갱신된다 — RED 증거 입력 전제는 (a)/(b) task 한정으로, step-kind 순서는 triage 분기 포함으로; census가 무변경 판정한 지점(Stage agents 라벨 행, fix prompt contract)은 diff 부재 (V4)

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.claude/skills/sdd-autopilot/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Technical Notes**: Covers C1(동형 게이트), I2, I3, I4. Validated by V4. §6 Review-Fix Contract의 correctness finding test-first 정책은 동작 버그 대상이라 무변경.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2, I2, I3, I4 (T1 AC) | 1등급 (정량 측정형): implementation SKILL 미러 짝 2개 파일에 대한 grep — (1) `test-free` 토큰, (2) 3분기 라벨 (a)/(b)/(c)와 `structural-check`, (3) 경계 문구(동어반복/tautology 취지), (4) "간단한 구현" 자격 부정 문구, (5) (c) 근거 기록 의무 문구, (6) 리뷰 게이트 불면제 문구, (7) 갱신된 canonical 자기선언 문장, (8) (c) 근거 기록 홈(progress 기록)·checkpoint 리뷰 dispatch 입력 전달 문구 — 각각 양 미러 모두 1회 이상 hit이면 통과 | grep 명령 + hit 출력 (파일별). 미러 한쪽이라도 0-hit이면 실패 |
| V2 | C4, I4 (T2 AC) | 1등급: test-author 미러 짝 grep — (c) 후보 신호 문구 + canonical surface 참조 문구 양 미러 hit, (b)/(c) 경계 임계값 문구는 0-hit(복제 금지) | grep 명령 + hit/0-hit 출력 |
| V3 | C3, I1, I4 (T3 AC) | 1등급: implementation-agent 미러 짝 grep — test-free triage 근거 수용 문구 양 미러 hit + `BLOCKED` 가드·"test-after 재개방 방지" 문구 잔존 hit | grep 명령 + hit 출력 |
| V4 | C1, I2, I3, I4 (T4 AC) | 1등급: orchestrator-contract·autopilot SKILL·sample-orchestrator 미러 짝 grep — §2 triage 문구·canonical 참조·(c) GREEN 증거 면제 문구·Stage C test-free 경로 문구 hit, autopilot SKILL bullet의 test-free 경로 문구 hit, sample-orchestrator의 Example A 프롬프트·양 example step-kind 서술에서 test-free/triage 분기 문구 hit, 무변경 대상(pointer 지점·Stage agents 라벨·fix prompt contract)은 diff 부재 | grep 명령 + hit 출력, git diff로 무변경 지점 확인 |
| V5 | I1 (T1 AC) | 1등급: implementation SKILL 미러 짝 grep — 기존 falsifiability 판정 토큰(assertion 단계 실패 인정 / import·collection·syntax 배제 / 구분 불가 시 강등 / exit code·diff RED 캡처) 잔존 hit | grep 명령 + hit 출력. 토큰 소실 시 실패 |
| V6 | C2 (T1 AC) | 2등급 (정성 rubric 판정형): 작성 비참여 리뷰어가 갱신된 (b)/(c) 경계 서술만 읽고 예시 3건 — "함수 X가 파일 Y에 존재" → (b), "SKILL 문서에 게이트 판정을 강제하는 계약 토큰이 존재" → (b) (문서 자산 중간 사례 — 실제 계약/구조를 강제하는 토큰), "이 문단에 이 문구가 있다" → (c) (단순 문구 존재 확인) — 을 오분류 없이 판정하고, 경계 서술에서 반박 가능한(이중 해석되는) 문장을 지목하지 못하면 충족 | 리뷰어 판정 + 인용한 문서 지점. 오분류 또는 이중 해석 지목 시 실패 |

# Risks/Mitigations and Open Questions

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| R1: (c) 문 남용 — 간단한 구현 task가 test-free로 강등돼 RED 게이트가 침식 | test-after `should work` 자기보고 재개방 | (b)/(c) 경계 기준(C2) + 무근거 강등 금지(I2) + 리뷰 게이트 불면제(I3)를 canonical surface에 falsifiable 문장으로 못박음 (V1, V6) |
| R2: claude·codex 미러 drift — 한쪽만 갱신되면 두 모델의 triage 판정이 갈림 | 동일 task가 런타임에 따라 test 강제/면제로 갈림 | 각 task가 미러 짝을 한 task로 묶고(T1-T4), 모든 V가 양 미러 동시 grep(I4) |
| R3: implementation-agent 가드 완화가 test-after 우회로로 확장 해석 | 테스트 없는 직접 호출 재개방 | 예외를 "orchestrator 전달 triage 근거 동반"으로만 한정하고 무근거 부재 `BLOCKED`와 방지 근거 문구 잔존을 V3로 검증 |
| R4: 경계 기준을 canonical 외 표면에 복제해 이중 소스화 | 기준 drift 시 표면 간 판정 불일치 | T2/T4는 참조만 두고 복제 0-hit을 V2로 검증 |

## Open Questions

### Q1. digest propagation 표면 목록에 없던 `implementation-agent` 미러 짝을 수정 범위에 추가
- **Decision taken**: T3로 포함. Touchpoints census 3이 실측한 차단 가드 문면상, 이 표면 없이는 test-free 경로가 leaf에서 붕괴한다.
- **Alternatives considered**: (1) orchestrator가 (c) task를 impl leaf 없이 직접 구현 — 기각: leaf 단일 작성자·파일 경계 계약 훼손. (2) impl-agent 무수정 + orchestrator가 형식상 RED 증거를 위조 전달 — 기각: 가드를 위장 우회해 test-after 방지 목적 자체를 훼손.
- **Confidence**: HIGH
- **User confirmation needed**: Yes (digest가 열거한 5개 표면 밖 확장이며, test-after 방지 가드를 건드리는 변경)

### Q2. autopilot SKILL.md 수정 범위 ("필요 시" 지시의 해석)
- **Decision taken**: dispatch controller bullet의 "(c) RED 통과 task에" 한정 문구가 있는 각 미러 1곳만 수정하고, orchestrator-contract §2를 pointer로 참조하는 재진술 지점은 무변경 (Touchpoints census 4 참조).
- **Alternatives considered**: 3단계 언급 전 지점 일괄 갱신 — 기각: pointer성 지점은 §2 갱신 후 모순이 없어 Minimum-Code Mandate 위반.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. (c) task의 GREEN 게이트 처리
- **Decision taken**: (c) task는 GREEN 증거 면제(검증할 테스트가 없음). Step 5 post-group 회귀 스윕(기존 테스트 재실행)과 Step 6 리뷰 게이트는 유지 — T1 AC와 T4 AC(autopilot 동형 표면)에 반영.
- **Alternatives considered**: (c) task에도 형식상 GREEN check 강제 — 기각: RED와 동일한 동어반복 문제를 GREEN 쪽에 재생산.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. triage 실행 시점 (RED 게이트 소유 vs Stage A 이후 판정)
- **Decision taken**: triage 판정은 RED 게이트 소유로 두되 실행 시점은 wave의 Stage A dispatch 직전 1회. test-author가 반환하는 (c) 후보 신호(T2)는 사전 triage가 놓친 경우의 사후 교정 경로이며, 최종 판정·근거 기록은 항상 RED 게이트가 한다.
- **Alternatives considered**: Stage A 완료 후 RED 게이트 시점에만 판정 — 기각: (c) task에 불필요한 test-author dispatch가 발생해 "Stage A 스킵" 확정 결정과 모순.
- **Confidence**: MEDIUM (digest는 "RED 게이트 런타임 triage"와 "Stage A 스킵"을 함께 확정했으나 실행 시점의 문면 배치는 명시하지 않음 — 두 결정을 모두 만족하는 유일 해석으로 판단)
- **User confirmation needed**: No
