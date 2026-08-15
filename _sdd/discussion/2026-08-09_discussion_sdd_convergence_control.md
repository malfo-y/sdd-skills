# 토론 요약: SDD 수렴 제어 — bounded fix loop와 rolling goal 전환

**날짜**: 2026-08-09 ~ 2026-08-10
**라운드 수**: 12
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: (1) `feature-draft`와 `implementation`의 현행 review 1회 + fix 1회 정책을 최대 2회 fix loop로 늘릴지, (2) 큰 기능에서 여러 SDD pipeline을 반복할 때 native goal을 어떻게 자동 연결할지 논의하고자 했다. 후속 라운드에서 두 번째 문제는 “`feature-draft`가 rolling split을 판정하면 자동으로 `goal-init` SDD mode로 전환하고, 여러 child feature-draft를 완주할 goal harness를 만든다”로 구체화됐다.
- **토론을 시작한 배경**: 최근 큰 기능이 단일 `feature-draft → implementation` 체인으로 닫히지 않고 롤링 feature별로 SDD 체인을 여러 번 타는 사례가 생겼다. 이 과정에서 native goal이 전체 진행과 종료조건을 유지하는 데 실용적으로 쓰였으나, 현행 SDD에는 goal과의 명시적 연결 계약이 없다.
- **현재 상태**: bounded fix-loop는 v4.6.57에서 구현·동기화됐다. `feature-draft`와 `implementation`은 gate 1/fix 1을 항상 수행하고 과다-finding 임계값에서만 gate 2/fix 2를 수행하며 gate 3은 금지한다. rolling 쪽은 아직 한 draft의 Part 1에 전체 분할 목록, Part 2에 첫 feature task를 함께 두고 goal로 전환하지 않는다. `goal-init`은 standalone generic goal helper이며 가설 큐 중심 4-file harness를 만들고 goal을 직접 활성화하지 않는다. 최근 `_sdd/goal/2026-08-07_skill_authoring_norms_core_rollout/` 실행은 여러 feature chain을 `report.md` inventory와 journal로 추적해 완료한 실사용 근거다.
- **범위와 제외 범위**: 단일 producer 내부의 bounded retry 정책과 rolling split에서 goal-init으로 자동 전환하는 산출물·소유권 경계를 함께 다뤘다. 실제 SKILL/spec 구현과 native goal 자동 활성화는 수행하지 않았다. 자동 전환 후에도 사용자가 goal 조건을 검토하고 직접 활성화하는 안전 경계는 유지한다.
- **수집한 근거**: `.codex/skills/feature-draft/SKILL.md`, `.codex/skills/implementation/SKILL.md`, `.codex/skills/sdd-autopilot/SKILL.md`, `.codex/skills/goal-init/SKILL.md`, `_sdd/spec/main.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/decision_log.md`, `_sdd/goal/2026-08-07_skill_authoring_norms_core_rollout/{goal,journal,report}.md`, OpenAI Codex configuration reference의 `features.goals` 설명, 현재 세션의 goal tool schema.

## 핵심 논점 (Key Discussion Points)
1. **두 번째 fix의 의미**: 재리뷰 없이 같은 finding을 다시 고치는 것이 아니라, 1차 fix 뒤 같은 gate를 한 번 더 실행해 새로 드러난 잔존 finding만 2차로 고치는 `review₁ → fix₁ → review₂ → fix₂`를 논의 대상으로 확정했다.
2. **추가 패스의 발동 범위**: 모든 작업에 2패스를 강제하면 finding이 적은 흔한 변경에도 reviewer 비용이 두 배 든다. 현행 과다-finding 임계값을 자동 2차 패스 trigger로 승격하면 위험 회차에만 비용을 지불하면서 새 판단 체계를 최소화할 수 있다.
3. **bounded loop의 종료 의미**: 2차 fix 뒤 3차 리뷰까지 허용하면 같은 문제가 재귀한다. 2차 finding별 표적 검증과 전체 회귀가 통과하면 완료하고, 3차 리뷰는 금지하는 bounded exit가 필요하다.
4. **gate 소유권**: 2차 패스도 caller나 goal이 아니라 producer가 소유해야 직접 호출·autopilot·goal 경로가 같은 품질 계약을 갖고, 현행 producer-owned gate 불변식을 보존한다.
5. **goal의 계층**: goal은 feature 설계나 review/fix 판단을 소유하기보다 여러 feature chain 위의 전체 종료조건·자동 continuation envelope가 되는 것이 자연스럽다. SDD는 per-feature 실행과 증거를, goal은 다음 미완료 feature 선택과 전체 완료 판정을 맡는 후보 구조를 검토했다.
6. **host 결합 위험**: 공식 공개 근거는 persisted goal과 automatic continuation을 확인해 주지만, 세부 lifecycle은 runtime/tool schema에 따라 달라질 수 있다. SDD core가 host 명령을 복제하기보다 manifest·completion evidence·next action의 runtime-independent handoff를 소유하는 편이 안전하다.
7. **자동 전환의 의미**: 사용자가 goal-init을 별도로 호출하는 권고형 연결이 아니라, `feature-draft`의 rolling split 판정이 `goal-init` SDD mode의 자동 진입 조건이 된다. goal-init은 원 요청·분할 사유·child 목록을 전달받아 generic intake/divergence를 반복하지 않는다.
8. **첫 child 경계**: 전환 전에 feature-draft가 child 1을 독립 정식 draft로 작성하고 plan-review/fix까지 닫는다. goal-init은 child를 만들지 않고 완성된 child 경로와 나머지 목록을 goal harness로 감싼다.
9. **rolling manifest**: 초기 child 개수는 고정 완료조건이 아니다. 후속 draft/implementation에서 발견된 근거에 따라 child를 추가·분할·병합할 수 있으며, 원래 상위 scope를 넓히지 않고 이유를 기록해야 한다.
10. **상태 단일 홈**: 안정적인 목표·종료조건은 `goal.md`, 현재 child inventory와 단계·next action은 `report.md`, 변경 이력은 `journal.md`, task별 상세 evidence는 child draft와 implementation ledger가 소유한다.
11. **재개 판단**: fix-loop feature는 완료됐고 rolling 전환 결정과 로컬 gap은 그대로다. handoff schema는 별도 토론으로 늘리지 않고 후속 feature draft의 Contracts·AC에서 반증 가능하게 구체화한다.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | 두 주제를 `SDD 수렴 제어`라는 하나의 범위로 함께 본다. | 단일 단계 retry budget과 여러 pipeline의 장기 종료조건은 각각 안쪽·바깥쪽 수렴 계층을 이룬다 (`사용자 판단`) | 1, 5 |
| 2 | “fix loop 2회”는 `review₁ → fix₁ → review₂ → fix₂`를 뜻한다. 재리뷰 없이 같은 finding을 한 번 더 처리하는 방식은 채택하지 않는다. | 새 finding과 잔존 위험은 post-fix review 없이는 관측할 수 없다 (`사용자 판단`) | 1 |
| 3 | 자동 2차 패스는 모든 회차가 아니라 현행 과다-finding 임계값(`Critical+High ≥ 3` 또는 `Medium ≥ 5`)을 만족한 회차에만 producer 내부에서 발동하는 방향을 기준안으로 삼는다. | 현행 advisory trigger를 재사용하면 보통 회차의 비용과 새 정책 표면을 줄이면서 무인 실행의 취약점을 보완할 수 있다 (`사용자 판단` + `코드 확인`) | 2, 4 |
| 4 | 2차 review finding을 fix한 뒤에는 finding별 표적 검증과 전체 회귀로 종료하며 3차 review는 수행하지 않는다. | 최대 2패스로 수렴을 보장하면서 마지막 fix의 판별력은 실행 evidence로 확보한다 (`사용자 판단`) | 3 |
| 5 | rolling split 판정 시 `feature-draft`가 `goal-init`의 SDD rolling mode로 자동 전환한다. 사용자는 goal-init을 별도로 호출하지 않지만 native goal 활성화는 직접 한다. | 큰 기능의 반복 SDD chain에 goal이 유용하다는 실사용과 명시적 사용자 의도를 결합하되, goal 자동 발동 금지 안전 경계는 보존한다 (`사용자 판단` + `코드 확인`) | 5, 7 |
| 6 | 전환 시 feature-draft가 첫 child의 독립 draft를 작성하고 plan-review/fix까지 완료한 뒤 goal-init에 인계한다. | 호출자가 실제 draft를 받고, 분할의 실행 가능성을 첫 slice로 검증하며, goal을 활성화하지 않아도 child 1을 독립 사용하게 한다 (`사용자 판단` + `코드 확인`) | 8 |
| 7 | child 목록은 고정 개수 대신 통제된 진화형 manifest로 관리한다. goal 완료조건은 `pending=0`, 전 child CLOSED evidence, 상위 AC 통합 PASS에 묶는다. | 후속 planning·implementation 발견이 초기 분할을 바꿀 수 있으므로 고정 개수는 조기 종료나 scope 압축을 유발한다 (`사용자 판단`) | 9 |
| 8 | 진화형 manifest의 canonical current-state 홈은 goal harness의 `report.md`, 변경 이력은 `journal.md`로 둔다. | 새 파일 없이 4-file harness를 유지하고 안정 계약과 변동 상태를 분리하며 최근 goal 실사용 패턴을 재사용한다 (`사용자 판단` + `코드 확인`) | 10 |
| 9 | 2026-08-10 재개 시 rolling 결정을 다시 열지 않고 곧바로 feature draft로 인계한다. | bounded fix-loop 완료와 rolling gap 존속을 최신 코드·spec에서 확인했고, 사용자가 바로 feature-draft 진행을 선택했다 (`코드 확인` + `사용자 판단`) | 11 |

> 근거 유형: `코드 확인` / `외부 자료` / `사용자 판단` / `미검증 가정` 중 하나를 근거 뒤에 표기. `미검증 가정` 위에 선 결정은 후속 작업이 전제부터 재검증해야 한다. 재방문(3.3.1)으로 변경된 결정은 변경 이력 1줄을 함께 남긴다.

### 기각한 대안
- **항상 2패스**: finding 0~소수인 일반 변경에도 reviewer 시간과 비용을 항상 두 배 지불하므로 기각했다.
- **재리뷰 없는 동일 finding 2차 fix**: 1차 fix 이후의 실제 잔존·회귀·새 결함을 관측하지 못해 두 번째 fix의 입력이 불명확하므로 기각했다.
- **현행 advisory-only 유지**: 대규모 무인 goal 실행에서는 권고를 소비할 사용자가 중간에 없을 수 있어 위험 회차의 추가 검증이 실행되지 않는 문제가 남으므로 기준안에서 제외했다.
- **2차 fix 후 3차 review 허용**: 종료 상한이 다시 열리고 review-fix loop의 재귀 문제가 반복되므로 기각했다.
- **goal-init을 사용자가 별도 호출하도록 권고만 하기**: 형님이 원하는 것은 rolling 판정에서의 자연스러운 자동 전환이므로 연결 강도가 부족해 기각했다.
- **전용 `sdd-goal` entrypoint 신설**: 기존 `feature-draft` 진입점에서 규모 판정 결과로 자동 전환하는 편이 사용자 mental model과 기존 skill 책임에 더 직접적이어서 기각했다.
- **goal harness만 만들고 child 1은 goal 첫 턴에 작성**: `feature-draft` 호출이 실제 draft 없이 끝나고 이미 수행한 planning 맥락을 다음 턴에서 반복하므로 기각했다.
- **첫 child skeleton만 만들기**: 정식 draft와 manifest 사이에 반쯤 완성된 제3 상태·소비 계약을 추가하므로 기각했다.
- **초기 child 목록 고정**: 후속 discovery가 분할 경계를 바꾸는 rolling workflow와 충돌하므로 기각했다.
- **parent rolling draft를 live manifest로 유지**: spec-sync 처리·spec-less mode·상태 갱신 때문에 장기 current-state 홈으로 불안정해 기각했다.
- **`features.md` 신규 추가**: 의미는 선명하지만 SDD mode만 5-file harness가 되어 현 단계에서는 불필요한 output contract 확장으로 판단했다.

## 미결 질문 (Open Questions)
| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| — | 현재 in-scope 미결 없음 | — | 기존 Q1은 `feature-draft rolling split → goal-init SDD mode 자동 전환`으로 해소됐다. handoff 필드의 정확한 schema는 후속 feature draft가 falsifiable AC로 구체화한다. |

> 카테고리: `out-of-scope` / `needs-data` / `deferred-deliberately` / `blocked-by:Q<n>` 중 하나. AI가 자동 부여한 항목은 `(auto-labeled, please review)` 표기.

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | ✅ 완료 — `feature-draft`와 `implementation`의 advisory trigger를 producer-owned conditional second review/fix로 바꿨다. | — | v4.6.57 |
| 2 | ✅ 완료 — 2차 fix의 표적 검증·회귀·최대 2패스 종료조건을 runtime mirror와 global spec에 동기화했다. | — | v4.6.57 |
| 3 | implementation-review shard 합산의 중복이 자동 trigger를 과도하게 발동시키는지 기존 실행 기록과 최초 적용 회차에서 관측한다. | Medium | 후속 검증 |
| 4 | `feature-draft`의 rolling 경로를 parent 한 파일 방식에서 `child 1 정식 draft → goal-init SDD handoff`로 바꾸는 feature draft를 작성한다. | High | 후속 `feature-draft` |
| 5 | `goal-init`에 SDD rolling 입력 mode를 추가해 generic divergence를 반복하지 않고 4-file harness를 만들며, `report.md` Feature Manifest와 `journal.md` 변경 이력 계약을 정의한다. | High | 후속 `feature-draft`·`implementation` |
| 6 | child 추가·분할·병합, pending 0, 전 child CLOSED, 상위 AC 통합 PASS를 구조 검증하고 goal 미활성화 시 child 1 독립 실행 경로도 검증한다. | High | 후속 검증 |
| 7 | `sdd-autopilot`, global spec, usage docs, Claude/Codex runtime mirror에 자동 전환과 사용자 활성화 안내를 전파한다. | Medium | 후속 `spec-sync` |

### 후속 핸드오프 (Handoff)
- **목표**: 남은 feature (B)를 닫는다. rolling split 시 child 1 정식 draft를 완성한 뒤 goal-init SDD mode가 진화형 `report.md` manifest를 가진 goal harness로 자동 전환한다.
- **변경 금지 제약**: producer-owned gate, caller의 gate 재호출 금지, scope 밖 finding 비수용, Low 정책, goal-init의 native goal 비발동, 4-file harness, child별 정식 feature-draft·implementation ledger 소유권을 보존한다. goal이 feature 설계·review 판단을 직접 소유하게 만들지 않는다.
- **검증**: 단일 규모는 기존 1-draft 경로, rolling 규모는 child 1 reviewed draft + 4-file goal harness, manifest mutation journal 기록, pending 0/전 child CLOSED/상위 AC PASS 종료, 미활성화 시 child 1 독립 실행, Claude/Codex mirror와 spec/docs census를 확인한다.
- **중단 조건**: 기존 threshold가 shard duplicate 때문에 자동 trigger로 부적합하거나, feature-draft가 goal-init을 호출할 때 interactive/lifecycle contract가 순환하거나, 4-file harness 안에서 current manifest와 append history의 단일 홈을 유지할 수 없으면 구현을 중단하고 해당 경계를 재논의한다.

## 리서치 결과 요약 (Research Findings)
- **현행 gate 계약**: v4.6.57에서 producer-owned bounded conditional second gate/fix로 구현됐다. gate 1/fix 1은 항상, 임계값 경로만 gate 2/fix 2이며 gate 3은 없다.
- **현행 규모 초과 계약**: `feature-draft`는 첫 feature만 Part 2에 쓰고 나머지를 rolling list로 남긴다. `sdd-autopilot`은 목록을 spec planned todo로 고정하고 feature별 체인을 순차 반복한다.
- **goal 실사용 근거**: 2026-08-07 goal harness는 P0/P1/P2의 여러 feature chain과 commit boundary를 journal/report로 추적해 `DONE`으로 닫았다. goal이 multi-chain progress ledger와 종료조건 유지에 유용하다는 직접 로컬 근거다.
- **공식 Codex 근거**: OpenAI configuration reference는 `features.goals`를 persisted goals and automatic continuation 기능으로 설명한다. 검색에서 SDD 결합을 위한 더 구체적인 public goal orchestration 계약은 확인되지 않았다.
- **현재 세션 schema 근거**: callable goal surface는 objective 생성, 상태/예산 조회, complete/blocked 종료를 제공한다. 이 runtime 사실은 SDD의 portable contract가 아니라 adapter 판단 자료로 취급해야 한다.
- **현행 rolling과 첫 child**: 현재 feature-draft는 이미 전체 split list와 첫 feature task를 함께 작성한다. 첫 child까지 만드는 결정은 기존 사용자 결과를 보존하면서 parent manifest와 child draft의 파일 책임만 분리하는 변화다.
- **goal-init SDD mode gap**: 현재 goal-init은 generic intake→divergence→condition crafting과 `experiments.md` 가설 큐를 전제로 한다. 자동 SDD 경로는 이미 grounded된 split handoff를 소비해 중복 인터뷰를 생략하고, `report.md`를 child current-state manifest로 명시해야 한다.
- **report manifest 선례**: 최근 goal harness의 실제 `report.md`는 19개 component inventory와 disposition/evidence를 보유해 multi-feature current-state ledger로 이미 사용됐다.

## 토론 흐름 (Discussion Flow)
Round 1: 두 이슈의 범위 → `SDD 수렴 제어`로 함께 논의
Round 2: 두 번째 fix의 의미 → 재리뷰 뒤 2차 fix로 한정
Round 3: fix 정책 대안 → 현행 임계값을 이용한 조건부 2패스 선택
Round 4: 2차 pass 종료 → 표적 검증·회귀 후 종료, 3차 review 금지
Round 5: goal 결합 대안 → 얇은 브리지·전용 entrypoint·자동 활성화를 비교하고 선택은 보류
Round 6: 미결 분류 → goal 결합 수준을 `deferred-deliberately`로 기록
Round 7: 사용자 구체화·이해 확인 → rolling split이 goal-init SDD mode의 자동 진입 조건임을 확정
Round 8: 첫 산출물 대안 → child 1 정식 draft와 plan-review까지 전환 전에 완료
Round 9: 고정 목록 반례 검토 → child 추가·분할·병합을 허용하는 진화형 manifest 채택
Round 10: manifest 단일 홈 → current state는 `report.md`, 이력은 `journal.md`로 분리
Round 11: 수렴 확인 → in-scope 미결 없이 요약·후속 feature handoff로 종료
Round 12: 최신 상태 재확인 → fix-loop 완료·rolling gap 존속을 확인하고 feature draft로 즉시 인계

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 두 이슈를 하나의 `SDD 수렴 제어` 설계로 함께 다룰지, fix loop를 먼저 볼지?
**Options**: 1) 두 이슈 함께 2) Fix loop 먼저 3) 정리/종료
**A**: 두 이슈 함께.
**Follow-up**: 단일 단계 retry budget과 여러 pipeline의 장기 종료조건을 하나의 계층 설계로 분석했다.

### Round 2
**Q**: “fix loop 두 번”은 재리뷰 후 2차 fix인지, 같은 findings의 2차 fix인지?
**Options**: 1) 재리뷰 후 2차 fix 2) 같은 findings 2차 fix 3) 정리/종료
**A**: 재리뷰 후 2차 fix.
**Follow-up**: 논의 대상을 `review₁ → fix₁ → review₂ → fix₂`로 고정했다.

### Round 3
**Q**: 항상 2패스, 임계값부 2패스, 현행 유지 중 어느 정책을 기준안으로 검토할지?
**Options**: 1) 임계값부 2패스 2) 항상 2패스 3) 정리/종료
**A**: 임계값부 2패스.
**Follow-up**: 기존 과다-finding advisory 임계값을 producer 내부 자동 재리뷰 trigger로 승격하는 방향을 채택했다.

### Round 4
**Q**: 2차 리뷰 finding을 fix한 뒤 표적 검증으로 종료할지, 잔존 위험으로 중단할지?
**Options**: 1) 표적 검증 후 종료 2) 잔존 위험으로 중단 3) 정리/종료
**A**: 표적 검증 후 종료.
**Follow-up**: 3차 review 금지와 finding별 검증·전체 회귀를 bounded exit로 정했다.

### Round 5
**Q**: goal 결합은 얇은 브리지, 전용 `sdd-goal`, 또는 보류 중 어느 수준으로 잡을지?
**Options**: 1) 얇은 브리지 2) 전용 sdd-goal 3) 정리/종료
**A**: 정리/종료.
**Follow-up**: goal을 외부 envelope로 두는 후보 구조는 남기되 구체 결합 수준은 결정하지 않았다.

### Round 6
**Q**: goal–SDD 결합 수준 미결을 의도적 보류, 추가 데이터 필요, 범위 밖 중 어떻게 기록할지?
**Options**: 1) 의도적 보류 2) 추가 데이터 필요 3) 범위 밖
**A**: 의도적 보류.
**Follow-up**: Q1을 `deferred-deliberately`로 분류하고 토론을 종료했다.

### Round 7
**Q**: rolling split 시 feature-draft가 자동으로 goal-init SDD mode로 전환하고 사용자가 goal을 활성화한다는 이해가 맞는지?
**Options**: 1) 맞음, 경계 논의 2) 연결 방식이 다름 3) 정리/종료
**A**: 맞음, 경계 논의.
**Follow-up**: 권고형 연결이 아니라 split 판정 기반 자동 goal-init 전환으로 기존 Q1을 재개했다.

### Round 8
**Q**: 전환 시 첫 child 정식 draft까지 만들지, goal harness만 만들지?
**Options**: 1) 첫 child까지 작성 2) Goal만 작성 3) 정리/종료
**A**: 첫 child까지 작성.
**Follow-up**: feature-draft가 child 1과 plan-review/fix를 소유하고 goal-init은 그 결과를 외부 goal envelope로 감싸는 경계를 확정했다.

### Round 9
**Q**: goal의 child 목록을 초기 고정할지, 통제된 진화를 허용할지?
**Options**: 1) 진화형 manifest 2) 초기 목록 고정 3) 정리/종료
**A**: 진화형 manifest.
**Follow-up**: goal 완료조건을 고정 개수 대신 pending 0·전 child CLOSED·상위 AC 통합 PASS에 묶었다.

### Round 10
**Q**: 진화형 manifest의 canonical current-state 파일을 `report.md`로 할지 parent draft로 할지?
**Options**: 1) report.md 2) Parent draft 3) 정리/종료
**A**: report.md.
**Follow-up**: current state=`report.md`, history=`journal.md`, stable contract=`goal.md`, child detail=draft/ledger로 단일 홈을 분리했다.

### Round 11
**Q**: 토론을 정리할지, handoff 필드나 안내 UX를 더 논의할지?
**Options**: 1) 정리/종료 2) Handoff 필드 논의 3) 안내 UX 논의
**A**: 정리/종료.
**Follow-up**: 정확한 handoff schema와 안내 문면은 후속 feature draft의 AC로 넘기고 토론을 종료했다.

### Round 12
**Q**: rolling goal-init 전환을 바로 feature-draft로 구체화할지, handoff schema를 한 라운드 더 논의할지?
**Options**: 1) 바로 feature-draft 2) Handoff schema 논의 3) 정리/종료
**A**: 바로 feature-draft.
**Follow-up**: v4.6.57 fix-loop 완료와 현행 rolling·goal-init gap을 최신 코드에서 재확인했고, 기존 결정의 변경 없이 후속 feature draft로 인계했다.
