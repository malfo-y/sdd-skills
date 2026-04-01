# 토론 요약: Implementation 스킬에 TDD-Review Iteration 루프 추가

**날짜**: 2026-04-01
**라운드 수**: 5
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **기존 feature draft와의 관계**: inline orchestration feature draft가 이미 존재하지만, 이번 논의는 독립적으로 진행. 현재 implementation 스킬의 구조 내에서 review 루프를 추가하는 것에 집중.
2. **리뷰 수준 결정**: implementation-review의 전체 기능(Tier-based, 4-tier 이슈 분류, 상세 보고서) 중 Skeptical Evaluator 자세 + AC 검증만 선택적으로 가져옴.
3. **루프 단위와 범위**: Phase 단위가 아닌 전체 Plan 실행 후 Iteration 단위로 리뷰. 재실행 시에는 NOT_MET AC + Critical/High 관련 Task만 선택적으로 재실행.
4. **기존 Step 구조와의 통합**: Step 6(Phase Review)은 경량 체크로 유지하고, Step 7(Final Review)만 iteration 루프로 대체.
5. **implementation-review 스킬의 독립성**: 리뷰 로직이 implementation에 내장되더라도 impl-review는 독립 스킬로 유지 (PR 리뷰 전 수동 검증 등 별도 용도).

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | Feature draft와 독립적으로 논의 진행 | feature draft는 inline orchestration(가시성) 문제 해결 목적. 이번은 review 루프(품질 보장) 목적. 별개 관심사. | 1 |
| 2 | Skeptical Evaluator + AC 검증(MET/NOT_MET/UNTESTED)만 가져옴 | 4-tier 이슈 분류, 상세 보고서는 오버헤드. AC 검증 + Skeptical 자세가 핵심 가치. | 2 |
| 3 | 종료 조건: 모든 AC MET + Critical/High 0건 | AC 충족만으로는 부족(숨겨진 이슈 가능), Critical/High 0건 조건으로 안전망 추가. | 3 |
| 4 | Iteration 단위 루프 (전체 Plan 실행 후 리뷰) | Task/Phase 단위는 오버헤드 과다. Iteration 단위가 효율과 포괄성의 균형. | 3 |
| 5 | 2차 iteration부터 NOT_MET AC + Critical/High 관련 Task만 재실행 | 전체 재실행은 비효율. 선택적 재실행이 실용적. | 3 |
| 6 | 최대 5회 iteration | 3회는 복잡한 구현에 부족할 수 있음. 무제한은 위험. 5회가 적절한 여유. | 3 |
| 7 | Step 6(Phase Review) 유지, Step 7(Final Review)을 iteration 루프로 대체 | Phase 단위 경량 체크는 조기 문제 발견에 유용. Final Review가 iteration 루프의 자연스러운 대체 대상. | 4 |
| 8 | Orchestrator가 리뷰 직접 수행 (sub-agent 위임 X) | 가시성 확보. 사용자가 리뷰 과정을 실시간으로 볼 수 있음. | 4 |
| 9 | 5회 초과 시 보고서 생성 + 사용자에게 결정 위임 | 자동 판단의 한계. 미해결 항목을 명시하여 사용자가 수동 개입 가능하도록. | 3 |
| 10 | implementation-review 스킬 독립 유지 | 독립 리뷰가 필요한 용도(PR 전 검증, 수동 감사 등) 존재. 관심사 분리. | 5 |
| 11 | 리뷰 기록은 IMPLEMENTATION_REPORT.md에 통합 | iteration별 별도 파일은 관리 부담. 기존 보고서에 iteration 이력과 AC 상태를 통합하는 것이 간결. | 5 |

## 미결 질문 (Open Questions)

(없음 — 모든 핵심 질문이 해결됨)

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | implementation SKILL.md의 Step 7을 iteration 루프로 재작성 | High | 구현 담당 |
| 2 | Skeptical Evaluator AC 검증 로직을 Step 7 내에 인라인으로 정의 | High | 구현 담당 |
| 3 | iteration 상태 추적 구조 설계 (AC 상태 맵, iteration 이력) | High | 구현 담당 |
| 4 | IMPLEMENTATION_REPORT.md 형식에 iteration 이력 섹션 추가 | Medium | 구현 담당 |
| 5 | implementation agent.md에도 동일 변경 반영 (Mirror 동기화) | Medium | 구현 담당 |
| 6 | feature draft와의 향후 통합 방향 검토 (별도 후속 작업) | Low | 사용자 |

## 리서치 결과 요약 (Research Findings)

- **현재 implementation 구조**: 7-Step (Load → Init → Analyze → Execute → Integrate → Phase Review → Final Review). Step 4에서 sub-agent TDD 실행, Step 6에 경량 Phase Review 내장.
- **현재 implementation-review 구조**: 독립 스킬. Tier-based(Plan/Spec/Code) 리뷰, 4-tier 이슈 분류(Critical/High/Medium/Low), Skeptical Evaluator 자세, 상세 보고서 생성.
- **기존 feature draft**: `feature_draft_implementation_inline_orchestration.md` — ac-plan → tdd-execute → impl-review를 sub-agent 대신 inline Read로 실행하는 구조 제안. Re-anchor, State Externalization 패턴 포함.

## 토론 흐름 (Discussion Flow)

Round 1: [토픽 확인] → implementation에 review 루프 추가, feature draft와 독립 논의로 확정
Round 2: [리뷰 수준 + 루프 단위] → Skeptical + AC 검증, Iteration 단위
Round 3: [재실행 범위 + Max iterations] → NOT_MET AC + Critical/High Task, 5회
Round 4: [기존 Step 정리 + 실행 방식] → Step 6 유지 + Step 7 대체, Orchestrator 직접 실행
Round 5: [리뷰 기록 + 종료] → IMPLEMENTATION_REPORT 통합, 토론 종료

## 부록: 설계 스케치

```
implementation SKILL.md (개선안)

Step 1-3: 기존과 동일 (Load → Init → Analyze Parallelization)
Step 4-5: 기존과 동일 (Execute by Phase + Integrate & Verify)
Step 6: Phase Review (경량, 기존 유지)

Step 7: Iteration Review Loop (신규, 기존 Final Review 대체)
  ┌─────────────────────────────────────────────────┐
  │ iteration = 1, MAX_ITER = 5                     │
  │                                                 │
  │ WHILE iteration ≤ MAX_ITER:                     │
  │   7.1 Skeptical AC 검증                         │
  │       - 모든 AC에 대해 MET/NOT_MET/UNTESTED 판정│
  │       - Skeptical Evaluator: "증거 없으면 NOT_MET" │
  │       - Critical/High 이슈 식별                 │
  │                                                 │
  │   7.2 종료 판단                                 │
  │       IF 모든 AC == MET AND Critical/High == 0: │
  │         → PASS: Step 8로 진행                   │
  │       IF iteration == MAX_ITER:                 │
  │         → FAIL: 보고서 생성 + 사용자 위임       │
  │                                                 │
  │   7.3 수정 대상 선정                            │
  │       - NOT_MET AC 관련 Task 목록               │
  │       - Critical/High 이슈 관련 Task 목록       │
  │       - 합집합 → 재실행 대상                    │
  │                                                 │
  │   7.4 TDD 재실행                                │
  │       - 대상 Task만 Step 4-5와 동일 방식 실행   │
  │       - iteration += 1                          │
  │                                                 │
  │   → 7.1로 복귀                                  │
  └─────────────────────────────────────────────────┘

Step 8: Report (IMPLEMENTATION_REPORT.md 생성)
  - 기존 내용 + Iteration History 섹션
  - AC 최종 상태, iteration 횟수, 각 iteration 요약
```

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 기존 feature draft와의 관계는? (feature draft 기반 발전 / 대체 / 독립 논의)
**A**: feature draft 무관 (독립 논의)
**Follow-up**: 현재 implementation 스킬에 직접 review 루프를 추가하는 것에 집중하기로 함.

### Round 2
**Q1**: 리뷰 수준은? (Phase Review 강화 / impl-review 통합 / impl-review 연계)
**A1**: Phase Review 강화 — implementation 내부에서 완결
**Q2**: 루프 단위는? (Task / Phase / Iteration)
**A2**: Iteration 단위 — 전체 Plan 실행 후 리뷰
**Follow-up**: implementation 내부에서 Iteration 단위로 TDD → review 루프를 도는 구조.

### Round 3
**Q1**: 리뷰 요소는? (AC 검증 + 이슈 분류 / 전부 / Skeptical + AC만)
**A1**: Skeptical + AC 검증만
**Q2**: 종료 조건은? (Critical/High 0건 / 모든 AC MET / AC MET + Critical 0건)
**A2**: AC MET + Critical/High 0건 (사용자 노트)

### Round 4
**Q1**: 기존 Step 정리는? (6+7 대체 / 6 유지+7 대체 / 모두 유지+루프 추가)
**A1**: Step 6 유지 + Step 7 대체
**Q2**: 실행 방식은? (Orchestrator 직접 / Sub-agent / Hybrid)
**A2**: Orchestrator 직접 실행
**Follow-up**: Phase Review는 경량으로 유지, Final Review를 iteration 루프로 대체. 가시성을 위해 orchestrator가 직접 수행.

### Round 5
**Q1**: 리뷰 기록 형태는? (REPORT 통합 / iteration별 별도 / 최소한)
**A1**: IMPLEMENTATION_REPORT 통합
**Q2**: 토론 종료? (종료 / 추가 논의)
**A2**: 토론 종료
