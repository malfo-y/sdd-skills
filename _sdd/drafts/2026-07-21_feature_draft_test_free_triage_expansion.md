# Feature Draft: RED 게이트 (c) test-free 범위의 카테고리 기반 확대 — 전-2등급 rubric task + proxy-check 명시화

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`implementation` 스킬 RED 게이트(및 `sdd-autopilot`의 동형 게이트)의 3-way triage에서 **(c) test-free** 자격은 현재 "acceptance check가 단순 문구·존재 확인 동어반복(tautology)으로 귀결되는 task" 하나뿐이다. 2026-07-21 agent 구조 다이어트 토론에서 "test-author-agent를 없애고 implementation-agent에 test-first 규칙만 넣자"는 통합안은 기각됐고(테스트 출제자·응시자 분리는 막힐 때 자기 테스트를 약화시키지 않는 인센티브 구조), 비용 절감 레버로 **(c) 범위의 카테고리 기반 확대만** 진행하기로 확정됐다. 이에 (c) 자격을 2개 카테고리로 확대한다:

1. **전-2등급 rubric task**: task의 `Validation`(`V*`)이 **전부 2등급(정성 rubric 판정형)**이면 (c)다. rubric 판정은 Step 6 checkpoint review의 reviewer(`implementation-review-agent` ∥ `simplicity-review-agent`)에게 위임된다. 근거: 판정 주체가 이미 reviewer인 task에서 기계 check는 rubric을 대리하지 못하는 약한 proxy이므로, RED artifact가 형식적 중간물이 된다. 혼재·등급 미표기 plan 처리는 아래 Guardrail Delta "전-2등급 판정의 입력 조건"을 따른다.
2. **proxy-check 명시화**: check 통과가 AC 충족을 **함의하지 못하는** 순수 문구-proxy check는 기존 동어반복과 동급으로 (c) 자격이다 (기존 "단순 문구 존재 확인" 서술을 이 함의 기준으로 명확화).

확대는 반드시 **카테고리 기반**이다 — "테스트하기 어려움/구현 난이도" 기반 확대는 test-free를 reward-hacking 도피 밸브로 만들므로 금지(같은 토론의 핵심 가드레일 합의). 판정 기준의 단일 소스는 `implementation` SKILL RED 게이트 canonical surface로 유지하고, 참조 surface에는 기준을 복제하지 않는다.

## Scope Delta

### In Scope

- `implementation` SKILL RED 게이트의 (c) 자격 카테고리 확대 (claude·codex 미러 짝) — canonical surface
- Step 6 checkpoint review dispatch 입력: 전-2등급 (c) task의 `V*` rubric 전달 의무 (위임 실행 경로)
- `test-author-agent` 미러 짝: (c) 후보 신호 기준을 확대 카테고리와 정합 (참조만, 판정 상세 미복제)
- `sdd-autopilot` `references/orchestrator-contract.md` 미러 짝: 동형 게이트의 (c) 요약 문구 정합 + review dispatch 입력 rubric 전달
- `_sdd/spec/main.md` §2 Guardrails test-first 불변식 bullet·§3 결정 테이블 행 갱신 (본 Part 1이 `spec-sync` 입력)

### Out of Scope

- test-author-agent 제거·implementation-agent 통합 (토론에서 기각 — 인센티브 구조 보존)
- 기존 가드레일 완화: "간단한 구현이라서"는 여전히 (c) 자격 아님, (c) 근거 기록 의무·Step 5 회귀 스윕·Step 6 리뷰 게이트 불면제 유지
- (a)/(b) 경로의 falsifiability 판정 규칙(assertion 단계 실패 인정·import/collection-only 배제 등) 변경
- Step 6/checkpoint 리뷰 구조·exit 정책·reviewer agent 본문 변경 (rubric 판정은 기존 AC/`V*` ledger 계약으로 수행됨)
- feature-draft task 스키마 변경 (등급 표기는 기존 `Validation` 블록 형식 그대로)
- `sdd-autopilot` SKILL.md·sample-orchestrator·`implementation-agent` 미러 짝 (카테고리 중립 문면이라 무변경 — Part 2 Touchpoints census D)

### Guardrail Delta

- **(b)/(c) 경계의 함의 기준**: check 통과가 task AC 충족(실질 구조·계약 강제)을 **함의하면** (b), 함의하지 못하는 순수 문구-proxy면 동어반복과 동급으로 (c). 기존 "실질 구조 vs 단순 문구" 경계 서술의 명확화이며 완화가 아니다.
- **전-2등급 판정의 입력 조건**: task `Validation`의 `V*` 등급 표기 기반으로만 판정한다. 1등급·2등급 혼재는 (a)/(b) 유지, 등급 표기가 없는 plan(경량 분해·legacy)에는 이 카테고리를 적용하지 않는다(추정 판정 금지 — 난이도 기반 확대와 같은 남용 경로 차단).
- **rubric 위임의 실행 경로**: 전-2등급 (c) task는 triage 근거에 더해 해당 task AC·`V*` rubric을 checkpoint review dispatch 입력에 포함해야 한다 (reviewer 판정이 유일한 품질 관문이 되므로 rubric 미전달은 검증 공백).

## Persistent Spec Implications

`_sdd/spec/main.md`에 남아야 할 계약:

- **Guardrails test-first 불변식 bullet**: (c) test-free 자격을 "산문·설명 문서·주석 같은 non-falsifiable content 한정" framing에서 카테고리 목록으로 확장 — ① 동어반복·순수 문구-proxy(check 통과가 AC 충족을 함의하지 못함), ② 전-2등급 rubric task(rubric 판정은 checkpoint reviewer에 위임; 입력 조건은 Guardrail Delta "전-2등급 판정의 입력 조건" 그대로). 전-2등급 task의 falsifiability는 RED artifact가 아니라 2등급 정의 자체(명시된 판정 기준 + 리뷰어 판정 + 증거)로 확보되므로 **falsifiable test-first 불변식 위반이 아니라 판정 주체 이동**이다 — 기존 "non-falsifiable content" 단독 framing과의 충돌은 이 문장으로 해소한다. (c) 근거 기록·리뷰 게이트 불면제·"간단한 구현" 무자격·(a)/(b) falsifiable 집행 성격은 불변.
- **결정 테이블 "implementation test-first" 행**: (c) 자격 카테고리 확대와 유지 이유(reviewer가 이미 판정 주체인 task에서 기계 check는 약한 proxy; 확대는 카테고리 기반만) 반영.
- **canonical surface 계약 유지**: 3-way triage(확대 카테고리 포함) 기준의 canonical은 `implementation` 스킬 RED 게이트 서술이며 다른 surface는 참조만 한다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

Part 1의 (c) 자격 확대 delta를 3개 변경 표면군(canonical `implementation` SKILL, `test-author-agent`, autopilot `orchestrator-contract` — 각 claude·codex 미러 짝)에 전개하고, 카테고리 중립 표면은 무변경으로 판정해 sweep으로 고정한다. 이 repo는 테스트 프레임워크 없는 문서/스킬 repo이므로 검증은 grep(1등급)과 리뷰어 rubric 판정(2등급)으로 수행한다. reviewer agent 본문은 무변경이다 — `implementation-review-agent`는 이미 "각 AC를 plan이 지정한 `V*`로 검증하고 verdict를 증거에 묶는" ledger 계약(§3 Verification Summary)을 보유하므로, 위임은 dispatch 입력에 rubric을 넣는 것으로 성립한다.

## Scope

Part 1 `Scope Delta`와 동일 범위. Part 2는 그중 스킬/agent 문서 표면만 task로 전개하며, `_sdd/spec/main.md`는 `spec-sync` 소관이라 어느 task의 Target Files에도 포함하지 않는다 (Spec 파일 불가침).

## Contract/Invariant Delta and Coverage

| ID | Type | Change (1줄) | Covered By |
|----|------|--------------|------------|
| C1 | Modify | (c) 자격에 전-2등급 rubric 카테고리 추가 (혼재 (a)/(b) 유지·등급 미표기 plan 미적용 포함) | T1 |
| C2 | Modify | (b)/(c) 경계를 "check 통과 → AC 충족 함의" 기준으로 명확화 (순수 문구-proxy = (c)) | T1 |
| C3 | Add | 전-2등급 (c) task의 review/re-review dispatch 입력에 task AC·`V*` rubric 포함 (rubric 위임 실행 경로) | T1, T3 |
| C4 | Modify | test-author의 (c) 후보 신호 기준을 확대 카테고리와 정합 (canonical 참조 유지) | T2 |
| C5 | Modify | autopilot 동형 게이트의 (c) 요약을 확대 카테고리와 모순 없게 갱신 | T3 |
| I1 | Preserve | 기존 가드레일 불변 — 난이도 무자격·(c) 근거 기록 의무·Step 5/6 불면제·(a)/(b) falsifiability 판정 규칙 | T1, verified: T4 |
| I2 | Preserve | canonical 단일 소스 — 참조 표면에 카테고리 판정 상세 복제 금지 | T2–T3, verified: T4 |
| I3 | Preserve | claude·codex 미러 parity(판정 토큰 동치) + 카테고리 중립 표면 무변경 | T1–T3, verified: T4 |

## Touchpoints

`test-free` 언급 표면 전 grep census를 현재 코드로 실측 재검증했다 (2026-07-21 기준, line number는 이 census에만 기록).

**Census A — canonical `implementation` SKILL 미러 짝 (T1·T4 참조)**

- `.claude/skills/implementation/SKILL.md`: (c) 정의 bullet (L174), (b)/(c) 경계 문단 (L176), Hard Rule "Test-first는 2-stage로 분리"의 (c) 예외 요약 문장 (L27 — "acceptance check가 동어반복이라"로 tautology 단독 한정, 확대 후 stale), Step 6 review dispatch의 triage 근거 전달 문장 (L258). 잔존 확인 anchor: canonical 자기선언 (L186), falsifiability 판정 규칙 (L182-185). AC3 (L18)·Stage B (c) 서술 (L217)·GREEN 게이트 (L223)는 카테고리 중립 — 무변경.
- `.codex/skills/implementation/SKILL.md`: 동형 — (c) 정의 (L202), 경계 문단 (L204), Hard Rule 2 (L58), Step 6 review spawn 문장 (L285), 자기선언 (L214). AC3 (L49)·(L244)·(L250) 중립 무변경. spawn/close_agent 어휘만 다름.

**Census B — `test-author-agent` 미러 짝 (T2·T4 참조)**

- `.claude/agents/test-author-agent.md`: Step 3 "test-free 분기" 문단 (L63) — 후보 기준 요약이 "동어반복적 존재 확인" + "AC가 non-falsifiable content뿐"으로 현행 canonical만 반영, canonical 참조·미복제 문장은 같은 문단에 존재. AC4 (L19)·RED 근거 출력 (L87)·"안 하는 것" (L101)·Role Pointer (L118)는 후보 신호 언급만 있는 중립 문면 — 무변경.
- `.codex/agents/test-author-agent.toml`: 동일 anchor (L63; L19·L87·L101·L118 중립).

**Census C — autopilot `orchestrator-contract` 미러 짝 (T3·T4 참조)**

- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`: Stage B bullet의 (c) 요약 "acceptance check가 단순 문구·동어반복으로 귀결돼 falsifiable RED artifact를 만들 수 없는 task" (L86 — 확대 후 모순 문면, canonical 참조 문장은 동일 bullet에 잔존), review-fix gate invocation contract의 triage 근거 전달 bullet (L165). 초기 구현 step (b)/(c) 서술 (L93-94)은 중립 — 무변경.
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`: 동일 anchor (L106, L185; L113-114 중립).

**Census D — 카테고리 중립 판정으로 무변경인 표면 (T4 diff 확인 대상)**

- `sdd-autopilot` SKILL 미러 짝: claude L180-181 / codex L204-205 — "경계 기준은 implementation SKILL RED 게이트 canonical surface 참조"로 기준 미복제, 카테고리 중립.
- `sample-orchestrator` 미러 짝: claude L93·L95·L256 / codex L92·L94·L254 — "(c) test-free로 triage된 task는 triage 근거를 입력으로" 수신 서술만.
- `implementation-agent` 미러 짝: claude `.md` L12·L35·L51·L111 / codex `.toml` 동형 — "test-free 분류 + triage 근거" 수신 계약만 (자격 카테고리 무관, 직전 확대 draft가 이미 연 예외 경로 그대로).
- 2등급 정의 원천: `feature-draft-agent` 미러 짝 (claude L149-150 "2등급 (정성 rubric 판정형)") — read-only 참조, 무변경.

**Census E — spec surface (Part 1 delta 대상, Part 2 task 없음)**

- `_sdd/spec/main.md`: §2 Guardrails test-first 불변식 bullet (L79 — "(c) test-free: 산문·설명 문서·주석 같은 non-falsifiable content…" framing 확장 필요), §3 결정 테이블 행 (L131). `_sdd/spec/decision_log.md` 2026-07-14 entry (L31-52)는 이번 확장의 직전 결정 — 신규 entry는 `spec-sync` 소관.

## Task Details

### Task T1: implementation SKILL RED 게이트의 (c) 자격을 2개 카테고리로 확대 (claude·codex 미러)
**Priority**: P0
**Type**: Feature

**Description**: canonical surface의 (c) 정의·경계·Hard Rule 요약·Step 6 dispatch 입력을 확대 카테고리와 일관되게 갱신한다. 확대를 canonical 한 곳에만 두는 근거: 참조 표면과 기준이 두 곳에 존재하면 drift가 두 런타임의 triage 판정을 가른다 (기존 canonical/참조 구조 유지 — Part 1 Change Summary의 확정 결정). Step 6 dispatch 입력에 rubric을 넣는 이유: 전-2등급 (c) task는 reviewer 판정이 유일한 품질 관문이라 rubric 미전달이 곧 검증 공백이며, reviewer agent는 기존 AC/`V*` ledger 계약으로 이를 소비하므로 본문 수정이 불필요하다. 수정 지점은 Touchpoints Census A 참조.

**Contracts**:
- C1 (Modify): (c) 자격 카테고리 — ① 동어반복·순수 문구-proxy(기존), ② **전-2등급 rubric**: task `Validation` 블록의 `V*`가 전부 2등급(정성 rubric 판정형 — feature-draft Validation 등급 체계)이면 (c)이며, rubric 판정은 Step 6 checkpoint review의 reviewer(`implementation-review-agent` ∥ `simplicity-review-agent`)에게 위임된다. 1등급·2등급 혼재 task는 (a)/(b) 유지. 등급 표기가 없는 plan(경량 분해·legacy)에는 이 카테고리를 적용하지 않는다. 근거 문장(reviewer가 이미 판정 주체인 task에서 기계 check는 rubric을 대리하지 못하는 약한 proxy)을 함께 명시한다.
- C2 (Modify): (b)/(c) 경계 — check 통과가 task AC 충족(실질 구조·계약 강제)을 **함의하면** (b), 함의하지 못하는 순수 문구-proxy check는 동어반복과 동급으로 (c). 기존 "단순 문구 존재만 확인하면 (c)" 서술을 이 함의 기준으로 명확화.
- C3 (Add): Step 6 review/re-review dispatch 입력 — 전-2등급 (c) task는 triage 근거에 더해 해당 task의 AC·`V*` rubric을 두 reviewer dispatch 입력(최초 review·review-fix 재리뷰 모두)에 포함한다.
- I1 (Preserve): "간단한 구현이라서" 무자격·(c) 근거 기록 의무·Step 5 회귀 스윕·Step 6 리뷰 불면제·(a)/(b) falsifiability 판정 규칙·canonical 자기선언 문장 잔존.

**Acceptance Criteria**:
- [ ] AC1: 두 미러의 (c) 정의에 확대 카테고리 2종이 존재한다 — 전-2등급 rubric 자격(전부 2등급 조건 + reviewer 위임처 명시 + 약한 proxy 근거)과 순수 문구-proxy의 함의 기준 문구
- [ ] AC2: 1등급·2등급 혼재 task의 (a)/(b) 유지 규칙과 등급 표기 부재 plan의 카테고리 미적용 규칙이 두 미러에 존재한다
- [ ] AC3: (b)/(c) 경계 문단이 함의 기준으로 갱신된다 — "check 통과가 AC 충족을 함의하면 (b), 함의하지 못하면 (c)" 취지 문장 존재
- [ ] AC4: Hard Rule "Test-first는 2-stage로 분리"의 (c) 예외 요약이 동어반복 단독 한정에서 확대 카테고리 포괄 서술로 갱신된다
- [ ] AC5: Step 6 dispatch 문장에 전-2등급 (c) task의 AC·`V*` rubric 포함 의무가 추가되고, 문구가 최초 review와 review-fix 재리뷰를 모두 포괄하는 "review/re-review dispatch 입력" 취지로 작성된다 — autopilot invocation contract의 triage 근거 전달 bullet(Census C)과 동형 (기존 triage 근거 전달 문장에 병치)
- [ ] AC6: 갱신된 (c)·경계 서술만 읽은 제3자가 사례를 오분류 없이 판정할 수 있다

**Validation** (AC와 1:1):
- AC1 → V1: 1등급 — 두 미러 grep: "전부 2등급"(또는 "전-2등급") 토큰, "함의" 기준 문구, reviewer 위임 문구(implementation-review-agent ∥ simplicity-review-agent 병기 또는 checkpoint review 위임 취지), "약한 proxy" 취지 근거 문구 각각 양 미러 ≥1 hit. 증거: grep 명령 + 파일별 hit 출력 (한쪽 0-hit이면 실패)
- AC2 → V2: 1등급 — "혼재…(a)/(b)" 취지 문구와 "등급 표기가 없는 plan…적용하지 않는다" 취지 문구 양 미러 hit. 증거: grep 출력
- AC3 → V3: 1등급 — 경계 문단 anchor("(b)와 (c)의 경계") 인접에 함의 기준 문구 hit. 증거: grep -A 컨텍스트 출력
- AC4 → V4: 1등급 — Hard Rule의 (c) 예외 문장에서 갱신된 카테고리 포괄 요약 문구 hit + 구 문면("acceptance check가 동어반복이라 falsifiable RED artifact를 만들 수 없는 task"의 단독 한정 형태) 소멸. 증거: grep hit/0-hit 출력
- AC5 → V5: 1등급 — Step 6 review dispatch 문장(claude "phase에 (c) test-free task가 있으면" / codex 동형)에 rubric 전달 토큰 hit + re-review 포괄 토큰("re-review" 또는 "재리뷰") hit. 증거: grep 출력 (둘 중 하나라도 0-hit이면 실패)
- AC6 → V6: 2등급 (정성 rubric 판정) — 작성 비참여 리뷰어가 갱신된 (c)·경계 서술만 읽고 4개 사례를 분류한다: (i) `V*` 전부 2등급 task → (c), (ii) 1등급·2등급 혼재 task → (a)/(b), (iii) "문서에 게이트 판정을 강제하는 계약 토큰 존재" check(통과가 AC 충족을 함의) → (b), (iv) AC 문구를 그대로 grep하는 check(통과해도 AC 충족 비함의) → (c). 오분류 0건이고 이중 해석되는 문장을 지목하지 못하면 충족. 증거: 리뷰어 판정 + 인용한 문서 지점

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- (c) 정의·경계 문단·Hard Rule 요약·Step 6 dispatch 문장 갱신 (anchor는 Census A)
- [M] `.codex/skills/implementation/SKILL.md` -- 동형 갱신 (spawn/close_agent 어휘 유지)

### Task T2: test-author-agent의 (c) 후보 신호 기준을 확대 카테고리와 정합 (claude·codex 미러)
**Priority**: P1
**Type**: Feature

**Description**: Step 3 "test-free 분기" 문단의 후보 기준 요약이 현행 canonical만 반영해, 확대 후에는 전-2등급 task나 순수 문구-proxy만 가능한 task에 대해 leaf가 억지 proxy check를 작성하는 경로가 남는다(전-2등급은 orchestrator triage가 dispatch 전에 잡는 것이 정상이나, triage가 놓친 경우의 사후 교정 경로가 stale해지면 안 됨). 후보 신호 요약 한 문장만 확장하고 판정 상세는 복제하지 않는다 — 기준이 두 곳에 존재하면 drift가 판정을 가르기 때문(canonical 참조 문장은 잔존). 수정 지점은 Touchpoints Census B 참조.

**Contracts**:
- C4 (Modify): (c) 후보 신호 기준 — 전달받은 `V*`가 전부 2등급이거나, 가능한 check가 AC 충족을 함의하지 못하는 순수 문구-proxy·동어반복뿐이면 억지 check로 메꾸지 말고 `(c) test-free 후보` 신호 + 사유를 반환한다. 최종 판정 canonical은 `implementation` SKILL RED 게이트 (기존 문장 유지).
- I2 (Preserve): 혼재 규칙·등급 미표기 plan 규칙 등 판정 상세는 이 agent 본문에 복제하지 않는다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러의 Step 3 분기 문단에 확대 후보 기준(전부 2등급 / 함의하지 못하는 순수 문구-proxy)이 존재하고 사유 반환·canonical 참조 문장이 잔존한다
- [ ] AC2: 이 파일 안에 카테고리 판정 상세(혼재 (a)/(b) 규칙·등급 미표기 plan 규칙)가 복제되지 않는다

**Validation** (AC와 1:1):
- AC1 → V1: 1등급 — 두 미러 grep: "전부 2등급"(또는 동치 표기) hit + "함의" 취지 문구 hit + "(c) test-free 후보" 및 canonical 참조 문장("복제하지 않는다" 취지) 잔존 hit. 증거: grep 출력
- AC2 → V2: 1등급 — 두 미러에서 "혼재" 규칙 문구·"등급 표기가 없는 plan" 문구 0-hit. 증거: grep 0-hit 출력

**Target Files**:
- [M] `.claude/agents/test-author-agent.md` -- Step 3 test-free 분기 문단 1곳 (Census B anchor)
- [M] `.codex/agents/test-author-agent.toml` -- 동형. codex 미러는 단순 복사가 아니라 codex 적응 delta(TOML 구조·codex 경로 표기) 보존 merge로 반영

### Task T3: autopilot orchestrator-contract 동형 게이트의 (c) 요약 정합 + rubric 전달 (claude·codex 미러)
**Priority**: P1
**Type**: Feature

**Description**: Stage B bullet의 (c) 한 줄 요약이 tautology 단독 한정이라 확대 후 canonical과 모순되는 문면이 된다 — 요약을 확대 카테고리 나열로 갱신하되 판정 상세는 넣지 않는다(canonical 참조 문장 잔존 — T2와 같은 drift 근거). review-fix gate invocation contract의 triage 근거 전달 bullet에는 전-2등급 (c) task의 rubric 전달을 병치한다(autopilot 생성 orchestrator도 동일한 위임 실행 경로를 갖도록). 수정 지점은 Touchpoints Census C 참조.

**Contracts**:
- C5 (Modify): Stage B bullet의 (c) 요약 — "동어반복·순수 문구-proxy(AC 충족 비함의)·전-2등급 rubric" 카테고리 나열 수준으로 갱신, 경계·판정 상세는 canonical 참조 유지.
- C3 (Add, 동형 반영): invocation contract의 review dispatch 입력에 전-2등급 (c) task의 AC·`V*` rubric 포함.
- I2 (Preserve): 혼재 규칙·등급 미표기 plan 규칙 등 판정 상세 미복제.

**Non-Goals**: `sdd-autopilot` SKILL.md·sample-orchestrator 미러 짝은 수정하지 않는다 — 카테고리 중립 문면(Census D)이라 확대 후에도 모순이 없다.

**Acceptance Criteria**:
- [ ] AC1: orchestrator-contract 미러 짝의 Stage B bullet (c) 요약이 확대 카테고리를 나열하고 canonical 참조 문장("복제하지 않음")이 잔존한다
- [ ] AC2: invocation contract의 triage 근거 전달 bullet에 전-2등급 (c) task의 AC·`V*` rubric 전달 문구가 추가된다

**Validation** (AC와 1:1):
- AC1 → V1: 1등급 — 두 미러 grep: Stage B bullet에서 "전-2등급"(또는 "전부 2등급") 토큰·"함의" 취지 토큰 hit + "canonical surface…참조" 문장 잔존 hit + 구 요약("단순 문구·동어반복으로 귀결돼"의 단독 한정 형태) 소멸. 증거: grep hit/0-hit 출력
- AC2 → V2: 1등급 — 두 미러 grep: triage 근거 전달 bullet 인접에 rubric 전달 토큰 hit. 증거: grep -C 컨텍스트 출력

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` -- Stage B bullet + invocation contract bullet 2곳 (Census C anchor)
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- 동형 (spawn 어휘·codex 적응 delta 보존 merge)

### Task T4: 미러 parity·가드 잔존·무변경 표면 sweep 검증
**Priority**: P1
**Type**: Test

**Description**: T1–T3 완료 후 전역 1회 read-only 검증으로 세 invariant를 고정한다. 개별 task의 per-file 검증으로 쪼개지 않는 이유: parity·복제 0-hit·무변경 diff는 표면군 전체를 한 번에 비교해야 잔존 누락(한쪽 미러만 갱신·의도 밖 파일 수정)이 드러난다. V3의 diff 기준: 이 repo는 전용 구현 branch가 보장되지 않아(main 직행 커밋 이력) "branch 범위" diff가 미정의이므로, 구현 시작 시점(T1 착수 전)의 HEAD를 baseline commit으로 progress artifact에 기록해 둔다.

**Contracts**:
- I1 (Preserve): canonical 미러 짝에 기존 가드 토큰 전부 잔존 — "간단한 구현이라서" 무자격 문구, (c) 근거 기록 의무, "불면제", canonical 자기선언 문장, (a)/(b) falsifiability 판정 토큰(assertion 단계 인정·import/collection 배제·구분 불가 시 강등·exit code/diff RED 캡처).
- I2 (Preserve): 카테고리 판정 상세(혼재 규칙 문구·등급 미표기 plan 문구)는 canonical 미러 짝 2파일 밖 전 repo에서 0-hit.
- I3 (Preserve): 변경 3 표면군의 claude·codex 짝은 신규 판정 토큰 존재가 동치이고(dispatch/spawn 어휘 차 제외), Census D 무변경 표면은 diff에 나타나지 않는다.

**Acceptance Criteria**:
- [ ] AC1: 변경 3 표면군 각 미러 짝에서 T1–T3의 신규 판정 토큰 존재가 짝 간 동치다
- [ ] AC2: canonical 미러 짝에 I1 가드 토큰이 전부 잔존한다
- [ ] AC3: Census D 무변경 표면(autopilot SKILL 짝·sample-orchestrator 짝·implementation-agent 짝·feature-draft-agent 짝)이 이번 변경 diff에 없다
- [ ] AC4: 판정 상세 문구가 canonical 미러 짝 밖에서 0-hit이다

**Validation** (AC와 1:1):
- AC1 → V1: 1등급 — T4 실행 시 T1–T3가 실제 기입한 신규 판정 문구에서 grep 토큰 목록을 확정하고(변형 표기 병행 열거 — 예: "전부 2등급"/"전-2등급", rubric 전달 문구의 실제 표기), 표면군별로 claude·codex 짝에 각각 실행해 hit 존재 여부 비교 — 짝 불일치 1건이라도 있으면 실패. 증거: 확정한 토큰 목록 + 짝별 grep 출력 대조표
- AC2 → V2: 1등급 — canonical 미러 짝 2파일 grep: I1 가드 토큰 목록 전부 hit — 1개라도 0-hit이면 실패. 증거: 토큰별 grep 출력
- AC3 → V3: 1등급 — `git diff --name-only <baseline>..HEAD`와 미커밋 working tree diff(`git diff --name-only` + `git diff --name-only --cached`)의 합집합에 Census D 파일 0건 (baseline = Description의 progress 기록 commit). 증거: baseline commit hash + 합집합 diff 파일 목록 출력
- AC4 → V4: 1등급 — T1이 canonical에 실제 기입한 혼재 (a)/(b) 규칙·등급 미표기 plan 규칙 문장에서 고정 토큰을 추출해(변형 표기 병행 열거) repo 전역 grep — hit가 canonical 미러 짝 2파일(및 본 draft·spec 문서)로 한정, 참조 표면(agent·orchestrator-contract) hit 0. 증거: 추출한 토큰 목록 + 경로별 grep hit 목록

**Target Files**:
- 없음 (read-only 검증)

# Risks/Mitigations and Open Questions

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| R1: 확대 오독 — "2등급으로 쓰기 쉬우니 rubric으로만 짜서 (c)로 빠지자"는 plan 측 reward-hacking (난이도 기반 확대의 우회 재현) | RED 게이트 침식, test-after 재개방 | 혼재 (a)/(b) 유지·등급 미표기 미적용·"간단한 구현" 무자격을 canonical에 falsifiable 문장으로 명시(T1 AC2 + T4 AC2), (c) 근거 기록·리뷰 불면제 유지. plan의 등급 남발 자체는 feature-draft 위계 규칙("1등급 우선, 품질 AC만 2등급")과 plan-review가 상류에서 견제 |
| R2: 전-2등급 (c) task의 rubric이 reviewer에 닿지 않으면 품질 관문이 실질 공백 | 위임만 선언되고 판정 미수행 | C3를 dispatch 입력 의무로 명문화 (T1 AC5, T3 AC2) — reviewer의 기존 AC/`V*` ledger 계약이 수신 측을 이미 보장 |
| R3: claude·codex 미러 drift — 한쪽만 갱신되면 두 런타임의 triage 판정이 갈림 | 동일 task가 런타임 따라 test 강제/면제로 갈림 | 각 task가 미러 짝을 한 task로 묶고(T1–T3), T4 sweep이 짝 동치를 전역 1회 검증 |
| R4: 참조 표면에 판정 상세가 복제돼 이중 소스화 | 기준 drift 시 표면 간 판정 불일치 | T2/T3는 요약·참조만 갱신, T4 AC4가 복제 0-hit을 전역 검증 |

## Open Questions

### Q1. Part 2 출력 포맷 — dispatch 지시 템플릿(전역 Validation Plan 표)과 repo canonical(v4.5.9 task-국소 Validation 블록)의 충돌
- **Decision taken**: repo canonical(v4.5.9) 형식 채택 — task별 `Contracts`·`Validation` 블록 + thin coverage index. downstream `implementation` SKILL이 task `Validation` 블록을 Stage A dispatch 입력으로 그대로 소비하고, `plan-review`가 전역 Validation Plan 표·역방향 coverage 기록을 plan smell로 감사하기 때문.
- **Alternatives considered**: dispatch 템플릿의 구 형식(전역 `## Validation Plan` 표 + Technical Notes "Covers…") 유지 — 기각: downstream 소비 계약·리뷰 게이트와 충돌해 review-fix loop에서 반려된다.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. 등급 표기가 없는 plan(경량 분해·legacy)에서의 전-2등급 판정
- **Decision taken**: 카테고리 미적용 — `V*` 등급 표기가 있는 plan에서만 전-2등급 (c)를 판정하고, 미표기 plan은 기존 기준(동어반복·proxy)만 적용한다.
- **Alternatives considered**: orchestrator가 `V*` 성격을 읽어 등급을 자체 추정 — 기각: 추정 판정은 "카테고리 기반만 확대" 가드레일이 막는 난이도/재량 기반 확대와 같은 남용 경로를 연다.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. rubric 위임의 실행 메커니즘 (dispatch 입력 vs reviewer agent 본문 수정)
- **Decision taken**: 위임 선언은 canonical (c) 정의에, 실행은 Step 6/invocation contract의 dispatch 입력에 task AC·`V*` rubric을 포함하는 것으로 성립시킨다 (C3). reviewer agent 본문은 무변경 — `implementation-review-agent`가 이미 "각 AC를 plan 지정 `V*`로 검증 + 2등급은 인용 근거로 verdict를 ledger에 기록"하는 계약을 보유한다.
- **Alternatives considered**: reviewer agent 본문에 전-2등급 (c) 전용 처리 신설 — 기각: 기존 ledger 계약과 중복되는 미요청 기능 추가 (Minimum-Code Mandate).
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. test-author-agent 수정(T2) 필요성 — 전-2등급은 dispatch 전에 결정론적으로 잡히는데도 고치는가
- **Decision taken**: 후보 신호 요약 한 문장만 정합 수정한다. 전-2등급 task는 정상 흐름에서 test-author에 닿지 않지만, triage가 놓친 경우의 사후 교정 경로(기존 계약)가 stale 요약("AC가 non-falsifiable content뿐")을 근거로 억지 proxy check를 작성하도록 유도하는 것을 막는다.
- **Alternatives considered**: 무변경 — 기각: 참조 표면의 stale 후보 기준이 canonical과 다른 leaf 행동을 유도해 canonical/참조 구조의 목적(판정 일관성)을 훼손한다.
- **Confidence**: HIGH
- **User confirmation needed**: No
