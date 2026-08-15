# 토론 요약: sdd-autopilot을 goal-init의 SDD instance로 재정의

**날짜**: 2026-08-10
**라운드 수**: 34
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: 큰 기능에서는 `sdd-autopilot`보다 `goal-init`으로 native goal을 설정하는 패턴을 더 자주 쓰며, goal이 rolling feature와 여러 SDD pipeline path를 목표 달성까지 반복하므로 사실상 상위호환인지 검토하고자 했다.
- **토론을 시작한 배경**: 기존 autopilot은 한 번의 SDD 체인을 끝내는 데 최적화되어 있지만 실제 사용은 outcome 중심의 장기 수렴·재계획을 요구한다. 최근 rolling goal bridge 작업을 계기로 두 진입점의 중복과 제어권을 재설계할 필요가 생겼다.
- **현재 상태**: `sdd-autopilot`은 `feature-draft → implementation → 조건부 spec-sync` 순서를 명시하는 독립 메타스킬이다. `goal-init` generic mode는 native goal의 조건과 4-file harness를 만들지만 SDD 체인을 필수 계약으로 직접 소유하지 않는다. 각 feature의 plan/review gate는 이미 `feature-draft`와 `implementation` producer 내부에 있다. PR #54는 rolling child 1 선작성 모델이지만 이번 결론의 설계 전제로 사용하지 않기로 했다.
- **범위와 제외 범위**: `sdd-autopilot`의 향후 역할, goal-init 재사용 경계, SDD Loop Protocol, activation 소유권을 다뤘다. formal `SDD Goal Contract` schema와 별도 goal-level gate는 상세 검토 후 과설계로 판정해 철회했다. generic goal의 explicit migration 기능과 구현 세부는 별도 작업으로 남겼다.
- **수집한 근거**: `.codex/skills/sdd-autopilot/SKILL.md`, `.codex/skills/goal-init/SKILL.md`, `.claude/skills/goal-init/SKILL.md`, goal harness template, `_sdd/spec/{main,components,usage-guide}.md`, `docs/SDD_WORKFLOW.md`, PR #54 branch diff.

## 핵심 논점 (Key Discussion Points)
1. **상위호환의 실체**: `goal-init` 단독이 아니라 `goal-init + native goal runtime + SDD producer skills` 조합이 autopilot보다 상위의 outcome-convergence loop를 제공한다.
2. **독립 runner의 필요성**: 기존 autopilot의 즉시 단일 체인 실행 가치는 있으나, 장기 기능에서는 goal setup과 중복되고 rolling·재계획을 별도 계약으로 유지하게 된다.
3. **instance 모델**: autopilot을 삭제된 이름으로 만들기보다 SDD 계약이 채워진 `goal-init` instance로 재정의하면 의도 표현과 발견 가능성을 보존할 수 있다.
4. **초기 planning 경계**: harness setup 전에 feature draft를 만들지 않고 기존 goal-init의 condition·4파일만 준비한다. 상세 next feature는 native goal이 실행 중 선택한다.
5. **품질 경계**: goal 전체는 기존 goal-init condition self-check가, 각 feature는 `feature-draft`·`implementation` 내부 gate가 검증한다. 별도 goal-level review gate는 두지 않는다.
6. **실행·활성화 소유권**: autopilot instance는 harness 생성까지만 수행하고 native goal 활성화는 사용자가 조건을 검토한 뒤 직접 한다.
7. **active goal과 setup의 분리**: setup은 native goal을 활성화·흡수·교체하지 않으므로 현재 goal 상태를 조회하거나 harness 생성을 차단하지 않는다. 활성화 시점과 기존 goal 처리는 사용자가 소유한다.
8. **formal coverage 탐색과 철회**: scope ID·`covers`·status manifest·general-agent gate를 검토했으나, goal-init preset을 별도 workflow engine으로 만드는 과설계라 폐기했다.
9. **기존 실패 경계 재사용**: 별도 `BLOCKED_GOAL_CONTRACT`를 만들지 않고 goal-init의 기존 intake·condition self-check 실패 경로를 사용한다.
10. **복잡도 재검토**: formal contract·coverage mapping·manifest state machine·goal-level reviewer를 함께 도입하면 goal-init preset이 별도 workflow engine으로 변질된다. 실제 사용에서 잘 작동한 native goal의 자율 수렴을 보존하고 SDD HOW만 preset으로 제공해야 한다.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | `sdd-autopilot`을 독립 pipeline runner가 아니라 `goal-init`의 SDD 전용 instance/harness generator로 재정의한다. | goal이 multiple SDD paths와 rolling을 목표 완료까지 지속하는 실제 사용 패턴 (`사용자 판단`) | 1, 2, 3 |
| 2 | **PARTIALLY SUPERSEDED by #16/#19** — setup 단계에서 기본 feature-draft는 생성하지 않는다. 다만 formal Initial Feature Queue의 `SEED` rows도 만들지 않고 기존 goal-init 자산만 사용한다. | 선행 draft와 별도 queue schema 모두 native goal의 동적 재계획을 조기에 고정한다는 후속 판단 (`사용자 판단`) | 4, 10 |
| 3 | **SUPERSEDED by #16** — goal 설정 시 별도 Goal Contract Gate와 실행 중 Feature Plan Gate를 모두 둔다. | formal goal-level gate가 별도 orchestration framework를 재생산한다는 후속 복잡도 검토로 변경 (`사용자 판단`) | 5, 10 |
| 4 | **SUPERSEDED by #16** — Goal Contract Gate가 scope·proof·Initial Feature Queue를 검증한다. | goal-init의 기존 condition self-check와 native goal 자율 수렴으로 축소하기로 변경 (`사용자 판단`) | 4, 5, 10 |
| 5 | goal loop는 feature마다 `feature-draft`의 내부 plan-review gate, `implementation`의 내부 implementation-review gate, 조건부 `spec-sync`를 사용한다. | 품질 gate의 producer ownership은 현행 SDD 불변식이다 (`코드 확인`) | 5 |
| 6 | harness 생성 후 native goal은 자동 활성화하지 않고 사용자가 직접 활성화한다. | 조건·scope·완료 proof를 사용자가 검토하는 안전 경계를 보존한다 (`사용자 판단`) | 6 |
| 7 | SDD preset goal 안에서 `feature-draft`가 분할되더라도 nested goal-init을 만들지 않고 현재 goal loop가 가장 작은 다음 feature를 계속 선택한다. formal manifest row ID 계약은 두지 않는다. | active goal 안의 재귀 goal 생성을 막되 별도 state machine은 만들지 않는다 (`사용자 판단`) | 1, 4, 6, 10 |
| 8 | **SUPERSEDED by #20** — RUNNING 또는 PAUSED generic goal이 있으면 `ACTIVE_GOAL_CONFLICT`로 중단하고 파일·manifest·condition을 변경하지 않는다. | 후속 단순화에서 setup은 native goal을 변경하지 않는 inert harness 생성일 뿐이므로 충돌 전제가 없다고 재판단했다 (`사용자 판단`) | 7 |
| 9 | **SUPERSEDED by #16** — `SDD Goal Contract`·Initial Feature Queue·Goal Contract Gate 명칭 세트를 도입한다. | schema 자체를 폐기해 별도 사용자-facing 개념이 불필요해졌다 (`사용자 판단`) | 4, 5, 8, 10 |
| 10 | **SUPERSEDED by #16** — ID가 있는 scope·completion·stop·initial feature schema를 둔다. | 기계적 coverage가 실제 요구보다 복잡한 workflow engine을 만들었다 (`사용자 판단`) | 4, 8, 10 |
| 11 | **SUPERSEDED by #16** — `covers`와 8열 status manifest를 둔다. | native goal의 자율 재계획과 기존 4파일이면 충분하므로 별도 manifest를 제거했다 (`사용자 판단`) | 4, 8, 10 |
| 12 | **SUPERSEDED by #16** — transient Goal Contract Review Context와 general-agent review를 둔다. | 별도 goal-level review를 제거하고 기존 goal-init condition self-check와 producer gates를 신뢰한다 (`사용자 판단`) | 5, 8, 10 |
| 13 | **SUPERSEDED by #16** — Goal Contract Gate에 bounded gate 1/2를 적용한다. | goal-level gate 자체를 제거해 적용 대상이 사라졌다 (`사용자 판단`) | 5, 8, 10 |
| 14 | **SUPERSEDED by #16** — 4파일에 formal contract/current queue/gate history/mutation proposal 역할을 새로 부여한다. | 기존 goal-init 4파일과 역할을 그대로 재사용하고 별도 schema 투영을 하지 않는다 (`사용자 판단`) | 4, 8, 10 |
| 15 | **SUPERSEDED by #16** — `BLOCKED_GOAL_CONTRACT` fail-closed 상태를 추가한다. | goal-init의 기존 intake·condition gate 오류 처리만 사용하기로 했다 (`사용자 판단`) | 9, 10 |
| 16 | `sdd-autopilot`은 기존 `goal-init`의 5단계·4파일·condition self-check를 그대로 사용하고 SDD Loop Protocol만 preset으로 제공한다. 별도 Goal Contract schema·manifest·goal-level reviewer는 만들지 않는다. | 형님의 실제 goal-init 사용 경험에 비해 formal 설계가 과도하게 복잡해졌다는 재검토 (`사용자 판단`) | 1, 3, 10 |
| 17 | scope-to-feature 기계적 coverage 대신 native goal의 자율 재계획과 최종 DONE WHEN/integration proof를 신뢰한다. feature 정확성은 기존 producer-owned gates가 담당한다. | goal-init의 장점은 outcome을 향한 유연한 multiple SDD path 실행이며 이를 state machine으로 재구현하지 않기로 했다 (`사용자 판단`) | 1, 5, 10 |
| 18 | SDD preset은 다음 6단계다: 미충족 DONE WHEN에서 최소 next feature 선택 → draft 부재 시 `feature-draft`(분할이면 최소 next unit) → `implementation` → persistent 변경 시 `spec-sync` → evidence·완료 feature·남은 gap·next action 기록 → 모든 DONE WHEN과 integration proof 통과 시 종료. | SDD 순서와 종료 증거만 HOW로 고정하는 최소 계약 (`사용자 판단`) | 1, 5, 6, 10 |
| 19 | 기존 `experiments.md`·`journal.md`·`report.md` 형식을 유지하고, 별도 Initial Feature Queue schema나 status enum을 추가하지 않는다. | 기존 goal-init 자산을 그대로 재사용하는 것이 instance 설계의 목적에 부합한다 (`사용자 판단`) | 3, 4, 10 |
| 20 | setup에서 현재 native goal 상태를 조회하거나 `ACTIVE_GOAL_CONFLICT`로 차단하지 않는다. inert harness는 항상 생성할 수 있고, native goal 활성화와 기존 goal 처리는 사용자가 직접 결정한다. handoff에는 “goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다”는 불변식을 한 줄로 명시한다. | setup과 activation의 소유권이 분리돼 있으므로 기존 goal과 실제 상태 충돌이 없고, 상태 조회는 불필요한 결합만 만든다 (`사용자 판단`) | 6, 7, 10 |

### 기각한 대안
- **autopilot을 bounded single-feature fast path로 유지**: 사용자는 독립 runner를 유지하기보다 goal 기반 단일 실행 모델로 통일하기를 선택했다.
- **autopilot 완전 삭제 후 goal-init이 암묵적으로 SDD를 선택**: SDD 순서가 모델의 자율 판단으로 약해지므로, 명명된 SDD instance와 명시 계약을 유지한다.
- **harness 생성 직후 native goal 자동 활성화**: 사용자 검토 경계를 없애므로 채택하지 않았다.
- **active generic goal에 자동 흡수 또는 자동 migration**: 기존 condition과 scope를 조용히 바꾸므로 기본 경로에서 제외했다. explicit migration은 별도 기능이다.
- **setup 단계의 active-goal status preflight와 차단**: setup은 native goal을 변경하지 않으므로 충돌을 예방하지 못하면서 불필요한 runtime 결합만 만든다.
- **formal `SDD Goal Contract` schema 전체**: Contract/Queue 경계, 4개 필드 묶음, outcome ID, proof coverage, planned proof 책임까지 검토했으나 goal-init preset을 별도 workflow engine으로 만드는 과설계라 최종 폐기했다.
- **scope-to-feature 기계적 coverage와 goal-level general-agent gate**: native goal의 자율 수렴과 producer gate를 신뢰하기로 해 제거했다.
- **formal Initial Feature Queue·dependency/status schema**: 다음 feature 선택은 native goal과 기존 `experiments.md` pending 항목에 맡기고 별도 queue 모델은 두지 않는다.

## 미결 질문 (Open Questions)

없음. 기존 보류 2건은 후속 토론에서 한 차례 구체화됐고, formal schema 관련 결정은 복잡도 재검토를 거쳐 최종 결정 16~19로 supersede됐다.

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 새 정의를 구현 가능한 `feature-draft`로 작성한다. | High | 후속 SDD 작업 |
| 2 | `sdd-autopilot`의 직접 runner 로직을 `goal-init(preset=sdd)` thin entrypoint로 교체한다. | High | 후속 implementation |
| 3 | 기존 goal-init harness template에 6단계 SDD Loop Protocol preset을 추가한다. | High | 후속 implementation |
| 4 | active SDD goal 안의 feature split이 nested goal-init 없이 같은 loop의 다음 feature 선택으로 이어지는지 검증한다. | High | 후속 implementation |
| 5 | 사용자 활성화 경계와 기존 autopilot 문서·등록·spec surface를 전수 동기화한다. | Medium | 후속 implementation/spec-sync |
| 6 | RUNNING/PAUSED 여부를 조회하지 않고 harness setup이 성공하며, native goal 활성화와 기존 goal 상태 변경이 모두 0건인지 검증한다. | High | 후속 implementation |

### 후속 핸드오프 (Handoff)
- **목표**: `/sdd-autopilot`이 초기 feature draft나 코드를 만들지 않고 기존 `goal-init` 4-file harness에 6단계 SDD Loop Protocol을 적용하며, 사용자가 활성화한 native goal이 feature별 SDD chain을 반복해 모든 DONE WHEN과 integration proof를 닫게 한다.
- **변경 금지 제약**: generic `goal-init` 경로·기존 4파일 형식·condition self-check·producer-owned feature/implementation gate·사용자 직접 activation을 약화하지 않는다. setup에서 native goal 상태를 조회·변경하거나 active goal 때문에 차단하지 않는다. formal Goal Contract schema·scope ID·manifest state machine·goal-level reviewer를 재도입하지 않는다. PR #54의 reviewed-child-1 선행 모델을 새 설계의 전제로 복사하지 않는다.
- **검증**: single 규모·초기 oversized·실행 중 split 시나리오에서 activation 전 feature draft/implementation 0건, 6단계 preset 존재, feature별 producer gate, nested goal-init 0건, persistent 변경의 spec-sync, 실제 evidence surface, 최종 integration proof를 확인한다. RUNNING/PAUSED 여부와 무관하게 상태 조회 없이 harness setup이 성공하고 native goal 활성화·기존 goal 변경은 0건이어야 하며, handoff에 비활성 불변식 한 줄이 있어야 한다. Claude/Codex mirror와 docs/marketplace/spec 참조 census를 함께 검증한다.
- **중단 조건**: 기존 goal-init 4파일과 Loop Protocol만으로 SDD chain 반복·split continuation·evidence surface를 표현할 수 없다는 재현 가능한 반례가 나오면 구현을 멈추고 사용자에게 보고한다.

## 리서치 결과 요약 (Research Findings)
- 현재 autopilot의 고유 계약은 SDD chain order·무승인 실행·producer 결과 종합이며, gate 자체는 이미 producer가 소유한다.
- 현재 generic goal-init은 outcome condition과 실험 loop를 제공하지만 SDD chain을 필수로 명시하지 않으므로 autopilot 계약을 제거만 하면 SDD 실행 보장이 약해진다.
- Claude와 Codex goal-init 모두 native `/goal` lifecycle을 제공하므로 goal-backed instance는 dual-runtime 방향과 양립한다.
- PR #54는 rolling 시 goal로 넘기지만 single은 직접 실행하는 혼합 모델이다. 이번 결정은 이 혼합 모델 대신 처음부터 goal harness로 통일한다.
- active generic goal의 condition은 새 SDD scope와 proof를 포함하지 않으므로 자동 흡수는 조기 완료 위험이 있다. 다만 inert harness setup은 기존 goal을 변경하지 않으므로 충돌 대상이 아니며 상태 조회도 필요 없다.
- formal schema 탐색 당시 outcome ID·`covers`와 general-agent review를 함께 검토했으나, 결정 #16~19에서 schema와 goal-level reviewer를 모두 폐기했다.
- formal gate blocker의 파일 0건 경계도 함께 검토했으나, gate 자체와 active-goal setup blocker가 폐기되어 최종 설계에는 남지 않는다.
- formal schema가 복잡해진 근본 원인은 goal-init의 prompt-level 자율 loop를 coverage mapping·manifest state machine·별도 reviewer로 다시 구현하려 했기 때문이다.
- `goal-init + SDD Loop Protocol preset`은 기존 condition self-check와 producer-owned gates를 재사용하면서 SDD 순서만 명시해 중복 orchestration을 피한다.

## 토론 흐름 (Discussion Flow)
Round 1: 논의 범위 → autopilot 폐기 가능성까지 검토.
Round 2: soft deprecation 대 완전 삭제 → 독립 runner 완전 삭제 선호.
Round 3: SDD 계약 공백 비판 → autopilot을 SDD 계약을 가진 goal-init instance로 재정의 제안.
Round 4: instance 형태 → 초기 feature-draft 없이 SDD goal harness generator로 정의.
Round 5: plan gate 소유 → goal 설정 시점과 각 feature 내부의 2단계 gate 선택.
Round 6: goal-level gate 깊이 → outcome·coarse decomposition만 검증.
Round 7: native goal 활성화 → 사용자 직접 활성화.
Round 8: 수렴 확인 → 현재 결론을 문서화하고 상세 schema는 후속으로 이관.
Round 9: active generic goal 기본 정책 → 자동 흡수·교체 없이 충돌 차단.
Round 10: paused 상태 → clear되지 않은 RUNNING/PAUSED 모두 충돌 대상.
Round 11: coarse SEED 용어 질문 → 상세 계획 전 초기 기능 큐로 설명.
Round 12: 초기 큐 필요성 → harness setup에서 Initial Feature Queue 생성.
Round 13: coverage 방식 → scope outcome ID와 feature `covers` 명시 매핑.
Round 14: exact schema → 최소 SDD Goal Contract와 8열 manifest 채택, dependency graph 제외.
Round 15: gate reviewer → transient Review Context를 받은 general agent review 선택.
Round 16: gate loop → 기존 bounded gate 1/조건부 gate 2 정책 재사용.
Round 17: canonical homes → goal/report/journal/experiments 4개 소유권 분리.
Round 18: 첫 수렴 확인 → `parent plan` 명칭 혼란을 재검토.
Round 19: 명칭 → `SDD Goal Contract`와 관련 용어 세트 채택.
Round 20: 두 번째 수렴 확인 → gate 실패 시나리오 추가 논의.
Round 21: blocker 출력 → fail closed·harness 파일 0건.
Round 22: 최종 수렴 → 기존 문서 갱신·마감.
Round 23: Contract와 Queue 경계 → stable contract와 mutable queue 분리를 임시 채택.
Round 24: Contract 필드 → goal/scope/completion/stop 4개 묶음을 임시 채택.
Round 25: scope granularity → 관찰 가능한 outcome 단위를 임시 채택.
Round 26: proof availability → schema field 대신 reviewer 문맥 판단 선택.
Round 27: planned proof → 특정 queue row의 명시적 책임을 임시 요구.
Round 28: STOP semantics 논의 중 복잡도 경고 → formal 설계 전체를 재검토.
Round 29: 단순화 방향 → Goal Contract schema를 버리고 SDD Loop preset만 유지.
Round 30: 보장 수준 → 기계적 coverage 대신 native goal의 자율 수렴 신뢰.
Round 31: exact preset → 6단계 SDD Loop Protocol 채택.
Round 32: 최종 수렴 → 기존 formal schema 결정을 supersede하고 문서 갱신.
Round 33: active-goal 차단 전제 재검토 → setup은 inert하므로 status 조회와 차단을 모두 제거.
Round 34: 혼동 가능성 비판 검토 → handoff에 비활성·기존 goal 무변경 불변식 한 줄 추가.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 역할 재정의, autopilot 폐기 검토, 현재 의견 정리 중 어디까지 논의할 것인가?
**Options**: 1) 역할 재정의 2) Autopilot 폐기 검토 3) 현재 의견만 정리
**A**: Autopilot 폐기 검토.
**Follow-up**: 현재 local contract와 PR branch를 비교했다.

### Round 2
**Q**: fast path 강등, 완전 삭제, 현재 정리 중 어느 방향인가?
**Options**: 1) Fast path로 강등 2) 완전 삭제 3) 여기까지 정리
**A**: 완전 삭제.
**Follow-up**: goal-init generic contract에는 SDD chain 보장이 없다는 숨은 전제를 지적했다.

### Round 3
**Q**: autopilot의 SDD 계약을 goal-init으로 이관할 것인가?
**Options**: 1) 최소 계약 이관 2) 자율 판단에 맡김 3) 결정 보류하고 정리
**A**: sdd-autopilot을 SDD 계약을 유지하는 goal-init의 instance로 변경하는 안을 제안했다.
**Follow-up**: 독립 runner가 아닌 명명된 SDD preset 모델로 재구성했다.

### Round 4
**Q**: 얇은 preset 유지, goal-init 완전 흡수, 현재 정리 중 어떤 형태인가?
**Options**: 1) 얇은 preset 유지 2) goal-init에 완전 흡수 3) 여기까지 정리
**A**: 초기 feature-draft 생성을 없애고, PR #54와 독립적인 SDD goal harness generator로 정의했다.
**Follow-up**: initial manifest를 SEED로 시작하고 실제 feature planning은 goal loop로 미뤘다.

### Round 5
**Q**: plan gate를 각 feature 내부 또는 goal 설정 시점 중 어디에 둘 것인가?
**Options**: 1) 각 feature 내부 2) Goal 설정 시점 3) 여기까지 정리
**A**: goal 설정 시점과 각 feature 내부 모두 필요하다고 판단했다.
**Follow-up**: 두 gate의 rubric 중복을 막기 위해 parent 대 feature 책임을 분리했다.

### Round 6
**Q**: parent-level gate의 깊이는 outcome·분해 또는 세부 계획 중 어디까지인가?
**Options**: 1) Outcome·분해만 검증 2) 세부 계획까지 검증 3) 여기까지 정리
**A**: Outcome·분해만 검증.
**Follow-up**: parent gate 최소 조건 네 가지를 합의했다.

### Round 7
**Q**: harness 생성 후 native goal을 사용자 또는 스킬 중 누가 활성화하는가?
**Options**: 1) 사용자가 직접 활성화 2) 자동 활성화 3) 여기까지 정리
**A**: 사용자가 직접 활성화.
**Follow-up**: goal-init의 기존 안전 경계를 유지했다.

### Round 8
**Q**: 지금 정리하거나 gate field·호환성을 더 논의할 것인가?
**Options**: 1) 지금 정리 2) Gate 필드 논의 3) 호환성 논의
**A**: 지금 정리.
**Follow-up**: exact schema와 active generic goal 충돌 정책을 의도적 후속 항목으로 분류했다.

### Round 9
**Q**: 활성 generic goal에 새 SDD 요청을 흡수할지 충돌로 차단할지?
**Options**: 1) 충돌로 차단 2) 확인 후 흡수 3) 이 항목 보류
**A**: 충돌로 차단.
**Follow-up**: 자동 migration은 별도 기능으로 분리했다.

### Round 10
**Q**: paused generic goal도 충돌 대상인가?
**Options**: 1) 미종료 전부 차단 2) RUNNING만 차단 3) 첫 항목 정리·종료
**A**: 미종료 전부 차단.
**Follow-up**: clear되지 않은 continuation state를 보호한다.

### Round 11
**Q**: scope ID와 `covers`를 가진 coarse SEED manifest를 사용할지?
**Options**: 1) Scope ID 매핑 2) 자유형 Scope만 3) 두 번째 항목 보류
**A**: coarse SEED manifest의 의미를 질문했다.
**Follow-up**: 상세 계획 전 goal이 소비할 초기 기능 후보 목록으로 풀어 설명했다.

### Round 12
**Q**: harness setup에서 초기 기능 큐를 만들지?
**Options**: 1) 초기 기능 큐 생성 2) Parent goal만 생성 3) 여기서 정리
**A**: 초기 기능 큐 생성.
**Follow-up**: 상세 feature plan이 아니라 제목·범위·상태만 갖게 했다.

### Round 13
**Q**: 초기 기능과 parent outcome을 ID로 연결할지?
**Options**: 1) ID로 연결 2) 자연어로 검토 3) Schema 논의 종료
**A**: ID로 연결.
**Follow-up**: 기계적 coverage와 판단형 decomposition review를 분리했다.

### Round 14
**Q**: 최소 Goal Contract schema와 8열 manifest를 채택할지?
**Options**: 1) 이대로 채택 2) Dependency 추가 3) Schema 논의 종료
**A**: 이대로 채택.
**Follow-up**: dependency graph 없이 row 순서를 사용하기로 했다.

### Round 15
**Q**: parent-level gate를 기존 plan-review mode 또는 내부 self-check로 실행할지?
**Options**: 1) plan-review 모드 추가 2) 내부 self-check만 3) Gate 방식 보류
**A**: 내부에서 적절한 리뷰 컨텍스트를 만든 뒤 general agent로 리뷰.
**Follow-up**: transient Goal Contract Review Context와 경량 반환을 정의했다.

### Round 16
**Q**: general-agent gate에 기존 bounded 정책을 적용할지?
**Options**: 1) 기존 정책 재사용 2) 항상 1회만 3) 여기서 정리
**A**: 기존 정책 재사용.
**Follow-up**: gate 1/조건부 gate 2/no gate 3를 정렬했다.

### Round 17
**Q**: contract와 evidence를 4개 canonical home으로 분리할지?
**Options**: 1) 4개 홈 분리 2) goal.md에 통합 3) 지금 정리
**A**: 4개 홈 분리.
**Follow-up**: Review Context는 transient로 유지했다.

### Round 18
**Q**: 두 미결을 문서화하고 마감할지?
**Options**: 1) 문서 갱신·마감 2) 실패 시나리오 논의 3) 호환성 논의
**A**: `parent plan`이라는 이름의 이유를 질문했다.
**Follow-up**: 실제 구조는 plan보다 scope·proof 실행 계약에 가깝다고 재평가했다.

### Round 19
**Q**: goal 설정 시 생성·리뷰하는 구조의 명칭은?
**Options**: 1) SDD Goal Contract 2) SDD Goal Blueprint 3) 이름 미정으로 정리
**A**: SDD Goal Contract.
**Follow-up**: Initial Feature Queue, Goal Contract Gate, Feature Plan Gate 용어를 함께 고정했다.

### Round 20
**Q**: 명칭까지 반영해 마감할지 실패 시나리오를 더 볼지?
**Options**: 1) 문서 갱신·마감 2) 실패 시나리오 논의 3) 추가 항목 논의
**A**: 실패 시나리오 논의.
**Follow-up**: 구조 오류, review blocker, high-density fixed 세 경로를 분리했다.

### Round 21
**Q**: Goal Contract Gate blocker에서 harness 파일을 만들지?
**Options**: 1) Fail closed·파일 없음 2) BLOCKED harness 생성 3) 실패 정책 보류
**A**: Fail closed·파일 없음.
**Follow-up**: `BLOCKED_GOAL_CONTRACT` transcript가 self-contained 재개 정보를 소유하게 했다.

### Round 22
**Q**: 전체 결정을 기존 discussion 문서에 반영하고 마감할지?
**Options**: 1) 문서 갱신·마감 2) 재개 UX 논의 3) 추가 항목 논의
**A**: 문서 갱신·마감.
**Follow-up**: 기존 open questions 2건을 결정 사항 8~15로 승격했다.

### Round 23
**Q**: SDD Goal Contract와 Initial Feature Queue를 분리할지?
**Options**: 1) Contract·Queue 분리 2) Contract에 Queue 포함 3) 설명만 정리
**A**: Contract·Queue 분리.
**Follow-up**: stable truth와 mutable state 중복을 제거하는 방향을 임시 채택했다.

### Round 24
**Q**: Contract를 goal·scope·completion·stop 네 묶음으로 정규화할지?
**Options**: 1) 4개 묶음 채택 2) Flat field 유지 3) 필드 논의 종료
**A**: 4개 묶음 채택.
**Follow-up**: 기존 `parent_*` flat field를 폐기하는 안을 임시 채택했다.

### Round 25
**Q**: scope.in을 관찰 가능한 capability·invariant로 제한할지?
**Options**: 1) Outcome 단위 2) Component 단위 허용 3) Scope 논의 종료
**A**: Outcome 단위.
**Follow-up**: 구현 방법과 무관한 stable scope ID를 설계했다.

### Round 26
**Q**: proof command에 availability field를 둘지?
**Options**: 1) 상태 필드 추가 2) Reviewer가 문맥 판단 3) Completion 논의 종료
**A**: Reviewer가 문맥 판단.
**Follow-up**: schema 증가 대신 repository grounding으로 존재 여부를 보려 했다.

### Round 27
**Q**: planned proof는 특정 Initial Feature Queue row 책임이 있을 때만 허용할지?
**Options**: 1) 명시적 책임 필수 2) 산문상 가능하면 허용 3) Proof 논의 마감
**A**: 명시적 책임 필수.
**Follow-up**: phantom proof를 막는 review rule을 임시 채택했다.

### Round 28
**Q**: progress event를 profile 공통 규칙 또는 Contract별 정의로 둘지?
**Options**: 1) 공통 규칙 사용 2) Contract별 정의 3) STOP 논의 종료
**A**: 논의를 중단하고 goal-init보다 복잡해진 이유를 질문했다.
**Follow-up**: schema·coverage·state machine·review gate가 별도 workflow engine을 만들었다고 진단했다.

### Round 29
**Q**: formal schema를 버리고 goal-init에 SDD Loop Protocol preset만 추가할지?
**Options**: 1) Loop preset만 유지 2) 최소 기능 큐만 유지 3) 여기서 토론 종료
**A**: Loop preset만 유지.
**Follow-up**: 결정 9~15와 Round 23~27의 schema 상세를 재방문했다.

### Round 30
**Q**: scope-to-feature 기계적 coverage 없이 native goal의 자율 수렴을 신뢰할지?
**Options**: 1) 자율 수렴 신뢰 2) 최종 조건 리뷰만 3) 축소안만 정리
**A**: 자율 수렴 신뢰.
**Follow-up**: goal-init condition self-check와 producer gates만 품질 경계로 유지했다.

### Round 31
**Q**: 6단계 SDD Loop Protocol을 핵심 preset으로 채택할지?
**Options**: 1) 6단계 채택 2) 더 축약 3) 여기까지 정리
**A**: 6단계 채택.
**Follow-up**: SDD 순서·분할·evidence·종료 증거만 HOW로 고정했다.

### Round 32
**Q**: 기존 discussion 문서를 단순화 결론으로 갱신하고 마감할지?
**Options**: 1) 문서 갱신·마감 2) Loop 문구 다듬기 3) 추가 쟁점 논의
**A**: 문서 갱신·마감.
**Follow-up**: formal Goal Contract 결정에 supersede 이력을 남기고 후속 handoff를 축소했다.

### Round 33
**Q**: active goal 처리의 최종 계약을 status 검사 제거 또는 advisory 유지 중 어디에 둘지?
**Options**: 1) 검사 자체 제거 2) 경고만 유지 3) 여기까지 정리
**A**: 검사 자체 제거.
**Follow-up**: setup은 native goal을 변경하지 않는 inert harness 생성이므로 기존 goal과 충돌하지 않고, activation 책임은 사용자에게 있다고 재판단했다.

### Round 34
**Q**: status 조회 제거 후 새 harness를 active goal로 오해하지 않도록 handoff에 비활성 불변식을 명시할지?
**Options**: 1) 불변식 한 줄 추가 2) 기존 안내로 충분 3) 여기까지 정리
**A**: 불변식 한 줄 추가.
**Follow-up**: runtime 상태를 조회하지 않으면서도 “goal 미활성·기존 goal 무변경”을 항상 명시해 setup과 activation 경계를 분명히 하기로 했다.
