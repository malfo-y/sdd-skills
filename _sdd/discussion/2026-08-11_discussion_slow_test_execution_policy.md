# 토론 요약: SDD TDD의 느린 테스트 실행 정책

**날짜**: 2026-08-11
**라운드 수**: 10
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: SDD 구현은 TDD와 리뷰 게이트 때문에 테스트를 반복 실행하는데, 실수로 만든 40분짜리 회귀 테스트가 반나절 동안 여러 번 실행되어 수시간이 낭비됐다. 30초 이상 걸리는 테스트는 fixture 등의 방법으로 분리하고 필요한 때만 실행하고자 했다.
- **토론을 시작한 배경**: 현재 안전 규율을 약화하지 않으면서 inner-loop 비용 폭증을 막을 repo-wide 실행 계약이 필요한지, 필요하다면 어느 단계가 fast/slow test를 소유할지 결정하기 위해 토론했다.
- **현재 상태**: `implementation`은 RED·GREEN, 삭제 후 재확인, 델타 테스트 변이 확인, 마감 회귀, gate fix 후 회귀를 수행할 수 있다. `implementation-review-agent`는 이전 결과를 재사용하지 않는 fresh verification을 요구하고, PR correctness reviewer는 CI evidence가 없으면 로컬 validation을 시도한다. 실행시간 예산·slow 분류·timeout·slow checkpoint 계약은 없다.
- **범위와 제외 범위**: implementation·implementation-review·PR review·checkpoint까지의 전체 테스트 실행 정책을 다뤘다. pytest/Jest/Gradle별 fixture API, 특정 CI vendor 설정, 구체 구현 파일 census는 후속 feature-draft 탐색 범위로 미뤘다.
- **수집한 근거**: `.codex/skills/implementation/SKILL.md`, `.codex/skills/implementation-review/SKILL.md`, `.codex/agents/implementation-review-agent.toml`, `.codex/agents/pr-review-agent.toml`, `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`의 현재 테스트·회귀·fresh verification 계약을 확인했다. 외부 자료는 사용하지 않았다.

## 핵심 논점 (Key Discussion Points)
1. **비용 증폭 구조**: 느린 테스트 한 번의 비용이 아니라 RED/GREEN·회귀·review freshness·fix 재검증 횟수의 곱이 실제 낭비를 만든다.
2. **안전성과 속도의 분리**: slow test를 평소 실행에서 제외하는 것만으로는 회귀 안전망이 사라지므로 반드시 실행되는 checkpoint를 함께 정의해야 한다.
3. **30초의 의미**: 프레임워크별 개별 test case가 아니라 agent가 실행하는 targeted inner-loop command의 wall-clock budget으로 삼아야 범용 계약이 된다.
4. **초과 테스트의 처리**: 30초 초과를 즉시 slow 등록하는 escape hatch로 쓰지 않고, 대상 축소·fixture/데이터 재사용·fake·fast contract와 slow integration 분리를 먼저 시도한다.
5. **리뷰 freshness 경계**: reviewer는 fast lane만 fresh 실행하고, slow 의존 AC는 checkpoint evidence 전까지 `UNTESTED`로 남겨 반복 비용과 근거 없는 `MET`를 동시에 막는다.
6. **repo별 설정**: `_sdd/env.md`가 fast/slow 명령, 예산, slow checkpoint를 소유하고, 공통 스킬은 기본 inner-loop budget만 제공한다.
7. **미설정 안전성**: checkpoint가 선언되지 않았을 때 자동 장시간 실행이나 조용한 skip 모두 금지하고 fail-closed한다.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | 정책 범위는 implementation만이 아니라 implementation-review·PR review·최종 checkpoint까지 포함한다. | 반복 실행 주체 전부를 닫지 않으면 비용이 다른 단계에서 재발한다 (`사용자 판단`) | 1 |
| 2 | 기본 구조는 hard cutoff 단일 규칙이 아니라 fast/slow lane을 둔 계층형 실행 정책으로 한다. | 합법적인 integration/e2e test를 보존하면서 inner-loop 반복만 줄인다 (`사용자 판단`) | 2 |
| 3 | slow lane 전체 실행은 merge CI로 고정하지 않고 repo가 선언한 지정 checkpoint에서 수행한다. | CI가 없는 소비 repo까지 포괄해야 한다 (`사용자 판단`) | 2, 6 |
| 4 | 기본 30초 예산은 개별 test case나 전체 suite가 아니라 targeted RED/GREEN command에 적용한다. | agent가 tool-agnostic하게 관측·제어 가능하고 큰 정상 suite의 오분류를 피한다 (`사용자 판단`) | 3 |
| 5 | 30초를 넘기면 반복 실행을 중단하고 비용 최적화를 먼저 수행하며, 본질적으로 느리다는 근거가 있을 때만 slow lane에 등록한다. | 즉시 slow 분류가 느린 테스트를 숨기는 escape hatch가 되는 것을 방지한다 (`사용자 판단`) | 4 |
| 6 | implementation-review는 fast lane만 fresh 실행하고 slow test를 재실행하지 않는다. slow 의존 AC는 checkpoint 전까지 `UNTESTED`로 유지한다. | 현재 fresh verification이 고비용 테스트를 중복 실행하지만, 이전 로컬 결과를 그대로 `MET`로 신뢰하는 것도 안전하지 않다 (`사용자 판단`) | 1, 5 |
| 7 | `_sdd/env.md`에 기본값 override, fast/slow validation command, 각 예산, slow checkpoint를 선언한다. | repo별 실행 환경을 매번 추측하지 않도록 persistent environment truth가 필요하다 (`사용자 판단`) | 6 |
| 8 | slow checkpoint 선언이 없으면 fail-closed한다. agent는 전체 slow suite를 임의 실행하지 않고 slow 의존 AC를 `UNTESTED`로 보고하며 current truth 승격을 막는다. | 자동 실행은 원래 시간 사고를 재현하고, 자동 skip은 검증 공백을 숨긴다 (`사용자 판단`) | 7 |

### 기각한 대안
- **30초 hard cutoff로 모든 느린 테스트 금지**: 합법적인 integration/e2e test까지 부정하고 예외 관리가 경직된다.
- **30초 초과 즉시 slow lane 등록**: 최적화 없이 느린 테스트를 평소 실행에서 숨기는 우회로가 된다.
- **merge CI를 유일 checkpoint로 강제**: CI가 없거나 다른 release/nightly/manual checkpoint를 쓰는 repo를 포괄하지 못한다.
- **reviewer도 slow test fresh 재실행**: 현재의 비용 증폭 원인을 유지한다.
- **checkpoint 미설정 시 구현 마감에 slow suite 자동 실행**: 예측하지 못한 수십 분 실행을 다시 허용한다.
- **모든 validation command에 전역 30초 적용**: 개별 테스트는 빠르지만 suite 규모가 큰 정상 repo까지 slow로 오분류한다.

## 미결 질문 (Open Questions)
| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| — | 없음 | — | 토론 범위 안의 정책 결정은 모두 닫혔다. 프레임워크별 구현은 후속 feature-draft의 코드 탐색 대상이다. |

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 전체 전파면을 census한 feature draft를 작성한다: implementation, correctness reviewer, PR review, `_sdd/env.md` 생성·upgrade 표면, spec/docs mirror. | High | 후속 `feature-draft` |
| 2 | 30초 초과 시 무반복 중단, 최적화 우선, slow checkpoint 이관, 미설정 fail-closed를 각각 판별하는 시나리오 AC를 만든다. | High | 후속 `feature-draft` |
| 3 | 런타임별 timeout/cancel 능력 차이를 탐색하고 공통 계약과 adapter 예시를 분리한다. | Medium | 후속 구현 탐색 |
| 4 | 도입 후 실제 test command 시간과 반복 횟수를 관측해 30초 기본값과 regression budget의 적정성을 재평가한다. | Medium | 운영 관측 |

### 후속 핸드오프 (Handoff)
- **목표**: targeted RED/GREEN 명령이 기본 30초를 넘으면 같은 고비용 명령을 무심코 반복하지 않고 최적화 또는 slow lane으로 라우팅하며, slow 의존 AC는 지정 checkpoint evidence 전까지 `UNTESTED`로 유지되는 기능을 설계·구현한다.
- **변경 금지 제약**: RED 관찰 전 구현 금지, fast lane의 reviewer fresh verification, evidence 없는 `MET` 금지, repo별 checkpoint 선택 가능성은 유지한다. fixture를 유일한 해법으로 강제하거나 CI 존재를 전제하지 않는다.
- **검증**: Claude/Codex mirror census, structural check와 변이 확인, timeout 초과·checkpoint 존재/부재·review 재실행 방지 시나리오, spec version/parity 검증으로 확인한다.
- **중단 조건**: 지원 runtime에서 30초 시점의 cancel/interrupt를 신뢰성 있게 표현할 수 없거나, slow AC의 `UNTESTED` 상태가 기존 gate 완료 판정과 모순되면 구현을 강행하지 않고 계약을 다시 토론한다.

## 리서치 결과 요약 (Research Findings)
- **구현 반복 지점**: 현재 `implementation` 계약은 task 하나에서도 RED, GREEN, 삭제 후 재확인, 변이 확인, 마감 회귀, fix 후 회귀로 같은 validation이 여러 번 실행될 수 있다.
- **review 반복 지점**: `implementation-review-agent`는 모든 test-dependent verdict에 fresh output을 요구하므로 producer 실행 evidence를 재사용하지 않는다.
- **PR 반복 지점**: PR correctness reviewer는 CI evidence가 없으면 `_sdd/env.md`의 local validation을 실행하므로 slow/fast 구분이 없으면 또 실행할 수 있다.
- **현재 공백**: 관련 canonical surface 어디에도 test command wall-clock budget, slow lane, checkpoint, timeout 초과 처리 규칙이 없다.
- **설정 위치**: `_sdd/env.md`는 이미 repo별 환경·실행 제약을 담는 committed canonical surface이므로 validation lane 선언 위치로 적합하다.

## 토론 흐름 (Discussion Flow)
Round 1: 적용 범위 → implementation·review·checkpoint 전체 정책 선택
Round 2: 실행 구조 → 계층형 fast/slow lane 선택
Round 3: slow 안전망 → merge CI 고정 대신 repo별 지정 checkpoint 선택
Round 4: 시간 예산 단위 → 개별 test가 아닌 command wall-clock 선택
Round 5: 초과 처리 → 즉시 slow 분류 대신 최적화 우선 선택
Round 6: reviewer 처리 → slow 재실행 대신 checkpoint 이관 선택
Round 7: checkpoint 미설정 → fail-closed 선택
Round 8: 설정 모델 → 기본 30초 + `_sdd/env.md` repo override 선택
Round 9: 30초 적용점 → targeted TDD inner loop로 한정
Round 10: 합의안 확인 → 문서 정리 승인

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 느린 테스트 제어를 구현 스킬만 다룰지 전체 테스트 정책으로 다룰지
**Options**: 1) 구현 스킬만 2) 전체 테스트 정책 3) 현재 의견 정리
**A**: 전체 테스트 정책
**Follow-up**: 현재 구현·review·PR 단계의 반복 실행 계약을 로컬 파일에서 확인했다.

### Round 2
**Q**: 계층형 정책과 hard cutoff 중 기본 구조
**Options**: 1) 계층형 정책 2) hard cutoff 3) 정리하고 종료
**A**: 계층형 정책
**Follow-up**: fast/slow 분리에는 slow lane 필수 실행 지점이 함께 있어야 함을 확인했다.

### Round 3
**Q**: slow lane 전체 실행 안전망
**Options**: 1) merge CI 필수 2) 지정 checkpoint 3) 정리하고 종료
**A**: 지정 checkpoint
**Follow-up**: CI 비의존 repo별 checkpoint 계약으로 범위를 정했다.

### Round 4
**Q**: 기본 30초 예산의 측정 단위
**Options**: 1) 명령 단위 30초 2) 테스트별 30초 3) 정리하고 종료
**A**: 명령 단위 30초
**Follow-up**: 범용 agent가 관측 가능한 wall-clock command budget으로 정의했다.

### Round 5
**Q**: 30초 초과 명령 처리
**Options**: 1) 최적화 우선 2) 즉시 slow 분류 3) 정리하고 종료
**A**: 최적화 우선
**Follow-up**: fixture는 여러 비용 축소 수단 중 하나이며 slow 등록의 자동 조건이 아님을 정했다.

### Round 6
**Q**: implementation-review의 slow test 처리
**Options**: 1) checkpoint로 이관 2) reviewer 재실행 3) 정리하고 종료
**A**: checkpoint로 이관
**Follow-up**: fast freshness는 유지하고 slow 의존 AC는 `UNTESTED`로 남긴다.

### Round 7
**Q**: slow checkpoint 미설정 기본 동작
**Options**: 1) fail-closed 2) 마감 1회 실행 3) 정리하고 종료
**A**: fail-closed
**Follow-up**: 임의 장시간 실행과 조용한 skip을 모두 금지했다.

### Round 8
**Q**: 시간 예산과 validation lane 설정 모델
**Options**: 1) 기본값 + repo 설정 2) 전역 30초 고정 3) 정리하고 종료
**A**: 기본값 + repo 설정
**Follow-up**: `_sdd/env.md`를 repo별 validation truth로 선택했다.

### Round 9
**Q**: 기본 30초를 모든 명령에 적용할지 inner loop에 한정할지
**Options**: 1) inner loop 한정 2) 모든 명령 적용 3) 정리하고 종료
**A**: inner loop 한정
**Follow-up**: fast regression과 slow checkpoint는 repo별 별도 예산을 갖게 했다.

### Round 10
**Q**: 합의안을 discussion 문서로 정리할지
**Options**: 1) 정리 2) 계속 논의
**A**: 정리해줘
**Follow-up**: in-scope 미결 없이 후속 feature-draft handoff를 작성했다.
