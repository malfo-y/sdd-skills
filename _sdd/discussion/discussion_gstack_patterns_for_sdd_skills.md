# 토론 요약: gstack 패턴의 sdd-skills 적용

**날짜**: 2026-03-24
**라운드 수**: 10
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **Fix-First 패턴**: gstack `/review`의 발견→즉시수정 패턴을 sdd-skills `/pr-review`에 적용할 범위. 스펙 레이어와 코드 품질 레이어의 분리 필요성.
2. **Verification Gate**: gstack의 "코드 변경 후 재검증 필수" 철학을 implementation/implementation-review/autopilot에 적용.
3. **자동 결정 투명성**: gstack `/autoplan`의 6원칙 자동 결정 vs sdd-autopilot의 동적 생성 철학. 원칙 세트 도입이 유연성을 해칠 수 있는 위험.
4. **Test Coverage Diagram**: 구현 계획 단계에서 기존 테스트 커버리지를 먼저 매핑하는 기법.
5. **Failure Modes 분석**: feature-draft에서 실패 경로를 사전 식별. 스킬/문서 복잡도 증가 우려 vs 에러 처리 누락 방지 가치.
6. **Scope Drift Detection**: PR 리뷰 전 범위 이탈 사전 감지.
7. **Regression Iron Rule**: 기존 테스트 실패 시 자동 회귀 방지 테스트 추가.
8. **Independent Agent 교차 검증**: 앵커링 바이어스 방지를 위한 독립 Agent 검증.
9. **Retro 스킬 vs spec-review 지표 강화**: 별도 회고 스킬 대신 기존 스킬에 코드 분석 지표 추가.
10. **체계적 디버깅 스킬**: gstack `/investigate`의 근본원인 우선 철학을 별도 스킬로 도입.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | `/pr-review`에 Fix-First 계층 분리 적용. 스펙 레이어(APPROVE/REQUEST CHANGES/NEEDS DISCUSSION)는 유지, 코드 품질 레이어만 AUTO-FIX/목록 기록 | 스펙 준수 판단은 리포트로, 기계적 코드 이슈는 즉시 수정. AUTO-FIX 불가 항목은 AskUserQuestion 없이 목록 기록 | #1 |
| 2 | `/implementation`, `/implementation-review`, autopilot review-fix loop에 Verification Gate Iron Rule 도입 | "should work"는 증거가 아님. 테스트 출력을 근거로 제시해야 함. 코드 변경 후 이전 결과 재사용 금지 | #2 |
| 3 | `/sdd-autopilot`에 Audit Trail + Taste Decision 표면화 (원칙 세트 미도입) | 원칙 세트는 동적 생성 철학과 충돌. 대신 Phase 2의 판단 근거를 구조화된 로그로 기록하고, taste decision만 최종 리포트에 표면화 | #3 |
| 4 | `/implementation-plan`에 Test Coverage Diagram 조건부 도입 (Target Files [M] 마커가 있을 때만) | 기존 코드 수정 시 회귀 방지를 위해 현재 커버리지 현황 파악 필요. 신규 생성 전용 계획에서는 불필요 | #4 |
| 5 | `/feature-draft` Part 1에 경량 Failure Modes 테이블 항상 포함 (수정: 원래 HIGH만 → 항상으로 변경) | 실패 경로를 생각하는 것을 기본 체크리스트화. 간단한 기능도 "정말 실패 경로가 없는가?" 확인. 간단하면 N/A 또는 1-2행, 복잡하면 3-5행. Single Source of Truth를 위해 feature-draft에만 배치 (implementation-plan은 이를 읽고 AC에 반영) | #5 |
| 6 | `/pr-review`에 Scope Drift Detection pre-step 추가 | PR diff 변경 파일 vs 스펙 패치 초안의 범위 비교. CLEAN/DRIFT/MISSING 판정을 리뷰 리포트 상단에 표시 (informational) | #6 |
| 7 | `/implementation`에 Regression Iron Rule 도입 | 기존 테스트 실패 시 테스트 업데이트 + 회귀 방지 테스트 추가를 필수 단계로 강제. 사용자 확인 없이 자동 | #7 |
| 8 | `/investigate` 신규 스킬에 Independent Agent 교차 검증 포함 (implementation-review에서 제외) | 디버깅 시 앵커링 바이어스 방지가 더 중요. implementation-review는 conciseness 원칙 유지 | #8 |
| 9 | retro 스킬 불필요. 대신 `/spec-review`에 코드 분석 지표(핫스팟, Focus Score, Test Coverage) 추가 | 별도 회고 스킬보다 기존 spec-review에 우선순위 가이드를 데이터 기반으로 추가하는 것이 SDD 워크플로우에 자연스러움 | #9 |
| 10 | `/investigate` (또는 `/debug`) 별도 스킬 신규 생성 | SDD 메인 루프 밖의 범용 디버깅 도구. 근본원인 우선, 3-strike 에스컬레이션, scope lock, fresh verification, blast radius gate. ralph-loop-init과 차별화 (범용 vs 장시간 프로세스 전용) | #10 |

## 미결 질문 (Open Questions)

없음 — 모든 논점에서 결정이 이루어짐.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 적용 대상 |
|---|------|---------|----------|
| 1 | pr-review에 Fix-First 계층 분리 적용 (코드 품질 AUTO-FIX + 목록 기록) | High | `/pr-review` |
| 2 | Verification Gate Iron Rule 도입 (코드 변경 후 재검증 필수, "should work" 금지) | High | `/implementation`, `/implementation-review`, `/sdd-autopilot` |
| 3 | sdd-autopilot에 Audit Trail + Taste Decision 표면화 | High | `/sdd-autopilot` |
| 4 | implementation-plan에 Test Coverage Diagram 조건부 도입 ([M] 마커 있을 때만) | Medium | `/implementation-plan` |
| 5 | feature-draft Part 1에 경량 Failure Modes 테이블 항상 포함 | Medium | `/feature-draft` |
| 6 | pr-review에 Scope Drift Detection pre-step 추가 | Medium | `/pr-review` |
| 7 | implementation에 Regression Iron Rule 도입 | Medium | `/implementation` |
| 8 | `/investigate` 신규 스킬에 Independent Agent 교차 검증 포함 | Low | `/investigate` (신규) |
| 9 | spec-review에 코드 분석 지표 추가 (핫스팟, Focus Score, Test Coverage) | Low | `/spec-review` |
| 10 | `/investigate` 스킬 신규 생성 (범용 체계적 디버깅) | Low | 신규 스킬 |

## 리서치 결과 요약 (Research Findings)

- **gstack 전체 구조**: 28개 스킬, Markdown 기반, Garry Tan(YC CEO)이 만든 오픈소스. Think→Plan→Build→Review→Test→Ship→Reflect 스프린트 프로세스.
- **gstack 핵심 철학**: "Boil the Lake"(완전성 원칙), "Verification-Driven"(검증 주도), "Fix-First"(발견→즉시수정), "Completeness Score"(옵션마다 완전성 점수).
- **sdd-skills 현재 구조**: 20개 스킬 + 18개 에이전트, 스펙 = Single Source of Truth, 동적 오케스트레이터 생성.
- **철학적 차이**: gstack은 프로세스/배포 중심 (고정 파이프라인 자동화), sdd-skills는 스펙 라이프사이클 중심 (동적 파이프라인 생성). 적용 시 sdd-skills의 동적 생성 철학을 훼손하지 않도록 주의 필요.

## 토론 흐름 (Discussion Flow)

Round 1: Fix-First 패턴 → 계층 분리 적용 (스펙 레이어 유지 + 코드 품질 AUTO-FIX) 결정
Round 2: Verification Gate → Iron Rule 도입 결정
Round 3-4: Autopilot 자동 결정 → 원칙 세트 vs 유연성 충돌 논의 → Audit Trail + Taste 표면화 결정
Round 5: Test Coverage Diagram → 조건부 도입 결정
Round 6-7: Failure Modes → 배치 위치 논의 (feature-draft만 vs 둘 다) → feature-draft만, Single Source of Truth 근거로 결정
Round 8: Scope Drift + Regression + Independent Agent → 각각 결정
Round 9: Retro 스킬 → 불필요, spec-review 지표 강화로 대체 결정
Round 10: Investigate 스킬 → 별도 스킬 신규 생성 결정, Failure Modes 활성화 기준 수정 (HIGH→항상)

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: pr-review에 Fix-First 패턴을 어떤 범위로 적용하면 좋을까요?
**Options**: 1) 계층 분리 적용 2) 전면 적용 3) 리포트 전용 유지 4) 논의 더 필요
**A**: 계층 분리 적용 + autofix가 안 되는 것은 AskUserQuestion 없이 목록으로 기록. REQUEST CHANGES 및 NEEDS DISCUSSION 유지.

### Round 2
**Q**: Verification Gate를 sdd-skills에 어떻게 적용하면 좋을까요?
**Options**: 1) Iron Rule 도입 2) implementation-review에만 적용 3) 논의 더 필요
**A**: Iron Rule 도입 (Recommended)

### Round 3
**Q**: sdd-autopilot에 gstack의 자동 결정 패턴을 어떻게 도입할까요?
**Options**: 1) 원칙 + Audit Trail 2) Audit Trail만 3) 현재 방식 유지 4) 논의 더 필요
**A**: 논의 더 필요 — 원칙 세트의 깊이에 따라 template 기반이 될 수 있다는 우려.

### Round 4
**Q**: Audit Trail + Taste 표면화 방향이면 동적 생성 철학을 지키면서도 투명성을 높일 수 있는데, 어떻게 생각하세요?
**Options**: 1) Audit Trail + Taste 표면화 2) 최소한의 원칙도 추가 3) 현재 방식 유지 4) 논의 더 필요
**A**: Audit Trail + Taste 표면화 (Recommended)

### Round 5
**Q**: Test Coverage Diagram을 implementation-plan에 어떻게 도입할까요?
**Options**: 1) 조건부 도입 2) 항상 포함 3) 논의 더 필요
**A**: 조건부 도입 (Recommended)

### Round 6
**Q**: Failure Modes 분석을 feature-draft에 도입할까요?
**Options**: 1) 규모 기반 조건부 2) 항상 포함 3) implementation-plan에 배치 4) 논의 더 필요
**A**: 논의 더 필요 — 스킬/문서 복잡도 증가 우려.

### Round 7
**Q**: 경량 Failure Modes 테이블을 어디에 배치할까요?
**Options**: 1) feature-draft만 2) 점진적 구체화(둘 다) 3) 논의 더 필요
**A**: 논의 더 필요 — "둘 다"가 아닌 이유 질문. → Single Source of Truth + 데이터 흐름 방향 설명 후 feature-draft만 선택.

### Round 8
**Q**: pr-review Scope Drift / Regression Iron Rule / Independent Agent 교차 검증
**A**: 모두 채택 (Scope Drift 추가, Regression 도입, 교차 검증 선택적 도입)

### Round 9
**Q**: Retro / Investigate / Safety Guardrails 영감 수준 후보
**A**: Retro 불필요 → spec-review 지표 강화로 대체. Investigate 별도 논의 요청.

### Round 10
**Q**: Investigate 스타일 디버깅을 어떻게 도입할까요?
**A**: 별도 스킬로 도입. + Failure Modes 활성화 기준을 "항상"으로 수정.
