# 토론 요약: spec 관련 스킬 open questions 후속 정리

**날짜**: 2026-04-13
**기준 문서**: `_sdd/discussion/2026-04-13_discussion_global_spec_role_balance.md`
**토론 범위**: `spec-summary` 구현 완료 이후 남은 spec 관련 스킬(`spec-review`, `spec-create`, `spec-rewrite`, `spec-upgrade`) 수정 방향의 open questions 정리

## 핵심 논점 (Key Discussion Points)
1. 공통 코어 checklist는 한 곳에 규범 기준선을 두되, 실제 운용은 각 스킬이 self-contained로 가져야 한다.
2. 스킬은 서로의 본문을 전제로 삼기 어렵기 때문에, 공통 코어를 별도 블록으로 두기보다 각 스킬 AC/Final Check에 흡수하는 편이 현실적이다.
3. 공통 코어 checklist를 AC에만 흡수하면 drift 위험이 커지므로, 상위 정의 문서에 매핑 규칙을 명시해야 한다.
4. `spec-review`의 핵심 추가 역할은 많은 항목을 더 보는 것이 아니라 global/temporary rubric을 잘못 섞어 오탐하지 않는 데 있다.
5. `spec-create`는 생성 단계의 구조 선택이 가장 중요하며, 초기 multi-file 과설계를 피해야 한다.
6. `spec-rewrite`는 문서를 얇게 만드는 것보다 중요한 rationale을 잃지 않는 구조 개선 도구여야 한다.
7. `spec-upgrade`는 legacy를 current model로 옮기는 도구이지, 대규모 구조 재편까지 흡수하는 도구가 아니다.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 |
|---|------|------|
| 1 | 공통 코어 checklist의 source-of-truth는 `docs/SDD_SPEC_DEFINITION.md`에 둔다 | 규범 기준은 상위 정의 문서에 있어야 하고, 특정 스킬 reference에 두면 전체 철학과 분리될 위험이 있다 |
| 2 | 각 spec 관련 스킬은 공통 코어를 self-contained하게 가져간다 | 스킬은 서로를 전제로 보기 어렵고, 실행 시 독립적으로 해석 가능해야 한다 |
| 3 | 공통 코어는 별도 `Shared Core Checklist` 블록이 아니라 각 스킬의 AC/Final Check 문구에 흡수한다 | self-contained를 유지하면서 문서 표면을 과도하게 늘리지 않기 위함이다 |
| 4 | `docs/SDD_SPEC_DEFINITION.md`에 공통 코어 4축과 AC 반영 매핑 규칙을 명시한다 | 별도 코어 블록 없이 AC에만 흡수할 때 발생하는 drift를 줄이기 위한 안전장치다 |
| 5 | 스킬별 추가 checklist 설계는 `spec-review`부터 시작한다 | review 기준이 먼저 잡혀야 나머지 생성/재구성 스킬의 목표선도 안정적으로 맞출 수 있다 |
| 6 | `spec-review`의 1차 추가 축은 `global/temporary rubric separation`이다 | 이 스킬의 핵심 가치는 더 많이 지적하는 것이 아니라, 틀린 rubric으로 오탐하지 않는 데 있다 |
| 7 | `spec-review`에서 global spec 오염은 기본적으로 `Quality`, 문서 타입 혼동을 일으킬 때만 `Critical`로 올린다 | 오염을 무조건 최상위 결함으로 다루면 false positive가 많아질 수 있다 |
| 8 | `spec-create`의 1차 추가 축은 `구조 선택 근거`다 | 초기 생성 단계에서 single-file/multi-file 판단이 흔들리면 뒤의 rewrite 비용이 커진다 |
| 9 | `spec-create`의 기본값은 `single-file`이며, 분할 필요가 증명될 때만 multi-file로 간다 | premature split을 막고 thin global default를 유지하기 위함이다 |
| 10 | `spec-rewrite`의 1차 추가 축은 `근거 보존`이다 | pruning 과정에서 중요한 `Why`와 결정 근거를 잃으면 구조는 좋아져도 판단 품질은 나빠질 수 있다 |
| 11 | `spec-rewrite`에서는 핵심 판단 이해에 필요한 최소 rationale만 본문에 남기고, 재배치/정리 메모는 `decision_log` 또는 `rewrite_report`로 보낸다 | 본문 비대화와 판단 근거 상실 사이의 균형점이다 |
| 12 | `spec-upgrade`의 1차 추가 축은 `rewrite 경계 판정`이다 | upgrade가 구조 재편까지 떠안으면 역할이 흐려지고 rewrite와 중복된다 |
| 13 | 대규모 분할, index/support 역할 재설계, 광범위한 section 재배열이 필요하면 `spec-upgrade`가 아니라 `spec-rewrite`로 분기한다 | upgrade는 in-place migration에 가깝고, 구조 재편은 rewrite의 책임이기 때문이다 |

## 남은 미결 질문 (Open Questions)
- [ ] 공통 코어 4축을 각 스킬 AC/Final Check 문구에 어떻게 문장 수준으로 매핑할지 최종 wording을 정할 필요가 있다.
- [ ] `spec-review`의 secondary 축으로 evidence strictness와 reporting/actionability 중 무엇을 더 강하게 올릴지 결정이 남아 있다.
- [ ] `spec-create`, `spec-rewrite`, `spec-upgrade` 각각의 secondary 추가 checklist 축을 어디까지 둘지 최종 압축이 필요하다.

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 |
|---|------|---------|
| 1 | `docs/SDD_SPEC_DEFINITION.md`에 공통 코어 checklist 4축과 AC 반영 매핑 규칙을 추가한다 | High |
| 2 | `spec-review` AC/Final Check에 `rubric separation`과 `조건부 Critical` severity 원칙을 반영한다 | High |
| 3 | `spec-create` AC/Final Check에 `구조 선택 근거`와 `single-file default` 원칙을 반영한다 | High |
| 4 | `spec-rewrite` AC/Final Check에 `근거 보존`과 `본문 vs 로그` rationale 배치 원칙을 반영한다 | High |
| 5 | `spec-upgrade` AC/Final Check에 `rewrite 경계 판정` 기준을 반영한다 | High |
| 6 | 위 반영 후 스킬별 secondary 축이 정말 필요한지 다시 점검해 checklist 비대화를 막는다 | Medium |

## 결론
이번 후속 논의의 핵심 결론은, 공통 코어 checklist는 상위 정의 문서에 규범 기준선으로 두되 실제 운용은 각 스킬이 self-contained한 AC/Final Check로 소화해야 한다는 점이다. 그 위에 각 스킬은 자기 역할이 가장 잘 드러나는 추가 축을 1개씩 우선 반영한다.
