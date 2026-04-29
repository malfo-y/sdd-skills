# 토론 요약: multi-phase implementation에서 review-fix gate를 phase 단위가 아닌 그룹 단위로 묶기

**날짜**: 2026-04-29
**라운드 수**: 8 (round 8: addendum — checkpoint 소유권 / multi-phase에서 implementation-plan 필수성)
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **현재 비효율의 root cause**: phase 단위가 너무 작아서 review의 가치/시간 대비 효용이 안 나온다. token 비용보다 (a) review depth 부족, (b) latency 누적, (c) "phase = review 단위 아님" 부적합성이 핵심.
2. **그룹 경계의 결정 주체**: plan-time annotation (implementation-plan이 phase 메타에 명시) vs runtime grouping (autopilot 휴리스틱) vs hybrid. → plan-time annotation으로 합의.
3. **그룹 내 phase의 검증**: 그룹 끝까지 아무 검증 없이 진행 vs phase별 light validation 유지. → 후자(phase별 light validation 유지, opus review-fix만 그룹 끝으로 모음).
4. **schema 형태**: phase별 `checkpoint: true/false` boolean flag. checkpoint=true 위치에서 group이 닫힘.
5. **default 값**: 미명시 phase의 default를 true(현 동작 보존)로 할지 false(batch)로 할지. → false로 합의 (단독 gate 필요한 phase만 explicit true).
6. **마지막 phase 처리**: implicit `checkpoint=true`를 강제 — 안 그러면 그룹이 한 번도 안 닫히는 케이스 발생 가능.
7. **mid-group critical issue 처리**: phase별 light validation에서 critical 이슈 발견 시 즉시 group boundary forced early하여 review-fix gate 트리거 (escape hatch).
8. **final integration review와의 관계**: 그룹 1개일 때만 마지막 group gate가 final을 겸함. 2개+면 cross-group regression 검토를 위한 별도 1회 유지.
9. **safety net 여부**: hard limit / reactive fallback 등 system-level 안전망 도입 vs plan(opus)을 신뢰. → 후자. plan이 잘못해도 review-fix loop가 실제 안전망 역할.
10. **plan의 foundation 판단 heuristic**: hard rule로 박을지 hint로만 둘지. → 후자. primary 신호 2개(dependency closure, risk level)는 권장 hint로만 명시하고, plan이 자율 판단하되 **reasoning은 무조건 남기도록 강제**.
11. **Checkpoint 필드 소유권 / multi-phase 진입 경로 (addendum)**: 새 `checkpoint` 필드는 implementation-plan이 만드는 phase 메타에만 존재. 그런데 autopilot은 single-phase medium path에서 feature-draft → implementation 직행을 허용하므로, multi-phase 실행이 implementation-plan 없이 시작되면 checkpoint 정보가 없어 그룹 체계가 깨질 수 있음. 두 가지 해결안: (A) **multi-phase 실행 시 implementation-plan 필수화** (autopilot 규칙 강화), (B) feature-draft 메타에도 checkpoint 추가. → (A) 채택. 이유: feature-draft는 spec/design 단계, checkpoint는 execution-level metadata로 관심사 분리. feature-draft Part 2는 단일 실행 패키지(single-phase)지 phase 분해가 아니므로 checkpoint 도입 시 phase 정의가 두 곳으로 갈라져 drift 발생. single-phase 경로는 어차피 phase가 1개뿐이라 마지막 phase implicit `checkpoint=true`로 자연 처리되어 필드 자체가 불필요.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | implementation-plan이 phase 메타에 `checkpoint: true/false` 명시 (plan-time annotation) | plan은 이미 dependency closure / exit criteria를 결정하는 단계라 그룹 판단도 같은 시점이 자연스럽다. explicit하고 디버깅 가능. | 2 |
| 2 | `checkpoint` 미명시 default = **false** (batch에 포함) | 단독 gate 필요한 phase만 explicit `true`. plan의 표현이 깔끔. | 5 |
| 3 | 마지막 phase는 explicit 값과 무관하게 implicit `checkpoint=true` | gate가 한 번은 반드시 닫혀야 함. mechanical 보호. | 6 |
| 4 | 그룹 내 phase는 light validation(test/typecheck/exit criteria) 유지, opus review-fix만 그룹 끝에서 1회 | review가 비싼 거지 validation은 비싸지 않음. 조기 회귀 차단. rollback risk 최소화. | 3 |
| 5 | foundation/contract phase는 단독 gate (group of 1) — plan이 `checkpoint=true`로 명시 | 후속 phase들이 의존하는 contract는 조기 검증 필요. group size 1과 N의 혼합 구조. | 1, 2 |
| 6 | mid-group light validation에서 critical 이슈 잡으면 즉시 review-fix gate 트리거 (group boundary forced early) | plan을 신뢰하되 명백한 폭탄은 즉시 차단. escape hatch. | 7 |
| 7 | 그룹 수 1개면 마지막 group gate가 final integration review를 겸함. 2개+면 cross-group regression 전용으로 별도 1회 유지 | adaptive — redundant round 제거하면서 cross-group 검토는 분리해 focus 유지. | 8 |
| 8 | safety net 없음 — plan(opus) 신뢰. group review-fix loop 자체가 안전망. | 과도한 safeguard는 시스템 복잡도만 키움. review-fix `max_rounds`가 이미 회복 메커니즘. | 9 |
| 9 | foundation 판단 heuristic은 hint만 명시 (primary 2개: dependency closure, risk level). plan이 자율 판단하되 phase별 reasoning 한 줄 의무 | rigid heuristic은 fragile. opus의 종합 판단이 더 신뢰. trace는 사용자 검증과 후속 디버깅에 필요. | 10 |
| 10 | **multi-phase 실행은 implementation-plan을 반드시 거치도록 autopilot 규칙 강화**. feature-draft → implementation 직행은 single-phase 경로에 한정. feature-draft 메타에 checkpoint 도입하지 않음. | 관심사 분리(spec vs execution), phase 정의 단일 SoT 유지(drift 방지), single-phase는 `checkpoint` 무관하게 자연 처리. 이미 부분적으로 규칙이 있어서(`Execution Mode: phase-iterative` ⇔ `Phase Source = implementation-plan output`) 강화·verification 추가만 필요. | 11 |
| 11 | orchestrator-contract와 SKILL.md에 명시적 invariant 추가: `Execution Mode: phase-iterative` ⇔ `Phase Source = implementation-plan output` (feature-draft 산출물을 Phase Source로 못 쓰게 명시) | 위 결정의 enforcement. 현재는 암묵적. invariant로 박아야 verification 가능. | 11 |
| 12 | Step 5 verification에 가드 추가: phase-iterative path인데 Phase Source가 implementation-plan output이 아니면 reject. 가능하면 self-correction(implementation-plan step 자동 삽입)까지 | invariant를 사후 검증으로 닫음. 사용자 개입 없이 autopilot이 회복 가능. | 11 |

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | 기존 plan들 (phase에 checkpoint 필드 없는 것)의 migration 방침 — 자동 변환할 것인가, 재작성 요구할 것인가 | deferred-deliberately | 실제 구현 시점에 결정. 새 plan은 explicit, 기존 plan은 그대로 동작하도록 하는 가장 단순한 길이 보임. |
| 2 | dependency closure 측정 단위 (file/module vs symbol-level) tuning | deferred-deliberately | 현재는 plan(opus)에 자율 위임. 운영 중 false positive/negative 패턴 보고 후속 tuning 가능. |
| 3 | implementation agent가 그룹 인식을 해야 하는가 (그룹 마지막 phase 끝나면 산출물 정리하라는 hint) | deferred-deliberately | 현재 가설: autopilot이 group boundary를 관리하고 implementation은 phase 단위로만 동작. 운영해보고 필요 시 추가. |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `implementation-plan` 스킬에 `checkpoint` 필드 schema 추가 (phase metadata 5개 → 6개) + foundation 판단 hint 2개(dependency, risk) 명시 + reasoning 의무화 | High | implementation-plan agent |
| 2 | `sdd-autopilot` orchestrator-contract와 SKILL.md에 group-aware execution 규칙 추가: phase 메타에서 checkpoint 읽고 group boundary 결정, group 끝에서만 review-fix gate, mid-group critical → forced early gate | High | sdd-autopilot |
| 3 | `examples/sample-orchestrator.md` Example B(multi-phase)를 group-aware 형태로 갱신: per-phase gate 표기 → per-group gate 표기, mid-group emergency 규칙 명시 | High | sample-orchestrator |
| 4 | Step 5 verification에 "그룹 1개면 final 겸함, 2개+면 분리" 검증 항목 추가 | Medium | sdd-autopilot SKILL.md |
| 5 | `references/orchestrator-contract.md` Review-Fix Gate 섹션을 per-phase에서 per-group 체계로 재기술 (agent_mapping 모델 표기는 유지) | High | orchestrator-contract |
| 6 | `references/orchestrator-contract.md` + `SKILL.md`에 invariant 추가: `Execution Mode: phase-iterative` ⇔ `Phase Source = implementation-plan output`. feature-draft 산출물은 Phase Source로 사용 불가 | High | orchestrator-contract / SKILL.md |
| 7 | Step 5 verification에 phase-iterative path의 Phase Source 출처 검증 추가. 위반 시 reject 또는 implementation-plan step 자동 삽입(self-correction) | Medium | sdd-autopilot SKILL.md |
| 8 | Step 4 reasoning rule 보강: multi-phase로 판단되면 planning precedence가 자동으로 implementation-plan을 끼우도록 명시 (현재 "필요한 경우" 표현을 "multi-phase면 의무"로 강화) | Medium | sdd-autopilot SKILL.md |

## 리서치 결과 요약 (Research Findings)

- **현재 implementation-plan 메타 스키마**: phase는 `goal`, `task set / dependency closure`, `validation focus`, `exit criteria`, `carry-over policy` 5개 필드 보유. group annotation은 6번째 필드(`checkpoint`)로 자연 확장 가능.
- **현재 review-fix gate prompt 계약** (sample-orchestrator.md): per-phase scope를 명시적으로 강제. group 단위로 변경 시 prompt에 "현재 group 범위(phase X~Y)"로 scope 재정의 필요.
- **final integration review의 현재 prompt**: cross-phase regression 전용으로 명시되어 있어 "group 1개일 때 겸함" 판단 시 prompt 합치기 가능.
- **현재 autopilot의 multi-phase 진입 경로**: SKILL.md의 expanded path 규칙은 "expanded path면 downstream `implementation` step에 `Execution Mode: phase-iterative`와 `Phase Source`가 선언되었는가"로 검증을 요구. 즉 multi-phase는 이미 implementation-plan 출력을 Phase Source로 요구하는 구조이지만, "Phase Source는 implementation-plan output이어야 한다"는 invariant가 명시적으로 박혀 있지 않음. addendum 결정으로 이를 explicit invariant로 격상.
- **planning precedence 현재 표현**: "implementation-plan은 ... medium이라도 multi-phase execution gate가 필요한 경우에만 추가" — "필요한 경우"라는 약한 표현이라 누락 여지 존재. multi-phase로 판단되면 자동 의무화하는 표현으로 강화 필요.

## 토론 흐름 (Discussion Flow)

- Round 1 (motivation): pain point 2~4(review depth 얕음 + latency + phase 단위 부적합) 모두 — root cause 합의
- Round 2 (constraint): 단독 gate 유지 phase = foundation/contract phase
- Round 3 (boundary owner): plan-time annotation (A) 채택
- Round 4 (intra-group validation): phase별 light validation 유지 + group end에 opus review-fix
- Round 5 (final review handling): adaptive (1 group=겸함, 2+groups=분리)
- Round 6 (safety net): 불필요 — plan 신뢰
- Round 7 (defaults): default=false (batch)로 뒤집기, mid-group escape는 유지
- Round 8 (heuristic granularity): hint만, plan 자율 + reasoning 의무
- Round 9 (addendum, checkpoint 소유권): feature-draft → implementation 직행 시 checkpoint 누락 risk 발견. (A) multi-phase에서 implementation-plan 의무화 vs (B) feature-draft에 checkpoint 추가. → (A) 채택. 관심사 분리, phase 정의 단일화, single-phase는 자연 처리. invariant로 격상 + Step 5 verification 가드 추가.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: phase마다 review-fix gate가 비효율적이라고 느낀 가장 큰 이유?
**Options**: 1) 토큰/비용 부담  2) review가 너무 얕음  3) 전체 시간/latency  4) phase 단위가 review 대상으로 부적합  + 토론 종료
**A**: 2-4 전부.
**Follow-up**: root cause 일치 — phase 단위가 너무 작아 review 가치 안 나옴. 해결 방향: 단위 키우기.

### Round 2
**Q**: 단독 gate 유지해야 하는 phase의 성격?
**Options**: 1) 더우 근간(foundation/contract)  2) 고위험/복잡도 높은 phase  3) 명시적 user/plan 표시 있을 때만  4) 우려 안 됨
**A**: 1 (foundation/contract).
**Follow-up**: group size 1과 N의 혼합 구조. foundation은 explicit single gate.

### Round 3
**Q**: 그룹 경계 결정 주체?
**Options**: A) plan-time annotation  B) runtime grouping by autopilot  C) hybrid  D) 더 논의 필요
**A**: A (plan-time annotation).
**Follow-up**: 비판적 짚음 — plan이 plan time에 foundation 판단 정확할지 의심. 일단 A로 가되 reasoning 의무화 필요.

### Round 4
**Q**: 그룹 내 phase의 validation?
**Options**: 1) phase별 light validation 유지 (추천)  2) 그룹 끝에서만 validation  3) 양쪽 둘 다
**A**: 1.
**Follow-up**: review가 비싸지 validation 안 비쌈. 조기 회귀 차단으로 rollback risk 감소.

### Round 5
**Q**: 마지막 그룹 gate와 final integration review 관계?
**Options**: 1) 마지막 group gate가 final 겸함  2) 별도 1회  3) 그룹 1개면 겸함, 2개+면 분리
**A**: 3 (adaptive).
**Follow-up**: redundant round 제거 + cross-group focus 유지의 균형.

### Round 6
**Q**: 그룹이 너무 커져 생기는 risk 처리?
**Options**: 1) hard limit  2) soft guideline  3) reactive fallback  4) safety net 불필요
**A**: 4.
**Follow-up**: review-fix loop 자체가 안전망. 과도한 safeguard 회피.

### Round 7
**Q**: backward compat default + mid-group escape OK?
**Options**: 1) 둘 다 OK  2) (2) 제거  3) (1) default=false (batch)  4) 더 논의
**A**: 3 — default=false로 뒤집기.
**Follow-up**: 단독 gate 필요 phase만 explicit true. 마지막 phase implicit true 추가 보호 필요.

### Round 8
**Q**: heuristic 세관도?
**Options**: 1) coarse + 보수적 default  2) fine-grained symbol-level  3) hint만, plan 자율
**A**: 3.
**Follow-up**: 일관된 철학 (plan 신뢰). reasoning 의무는 trace 보장.

### Round 9 (addendum)
**Q**: feature-draft → implementation 직행 경로에서 checkpoint가 누락되는 gap을 어떻게 닫을지. (A) multi-phase 실행은 무조건 implementation-plan을 거치게 강화 vs (B) feature-draft에도 checkpoint 추가.
**A**: (A) 채택.
**Follow-up**:
- feature-draft는 spec/design 단계, checkpoint는 execution-level metadata → 관심사 분리
- feature-draft Part 2는 single-phase 실행 패키지지 phase 분해가 아님 → 두 곳에 phase 구조 두면 drift
- single-phase는 phase 1개라 마지막 phase implicit `checkpoint=true`로 자연 처리, 필드 자체 불필요
- 현재 SKILL.md/orchestrator-contract에 multi-phase ↔ Phase Source 관계가 암묵적으로만 있음. 이번에 explicit invariant로 격상하고 Step 5 verification 가드 추가하기로 결정 (Action items 6-8).
