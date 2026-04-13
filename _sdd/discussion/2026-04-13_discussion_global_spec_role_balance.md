# 토론 요약: global spec의 존재의의와 균형점

**날짜**: 2026-04-13
**라운드 수**: 20
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)
1. global spec은 사람과 LLM 모두를 만족시키려는 만능 문서가 아니라, repo-wide 판단을 고정하는 계약 앵커여야 한다.
2. 사람이 global spec에서 얻는 가치는 "모든 상세 설명"보다 "무엇이 고정돼 있고 어디로 더 읽어야 하는지"를 빠르게 파악하는 데 있다.
3. 사람 친화성을 높인다고 해서 main body를 계속 키우면 supporting surface와 중복되고 drift가 커질 가능성이 높다.
4. 현재 저장소는 이미 thin global spec + supporting surface 분리를 채택하고 있으므로, 문제는 구조 자체보다 각 surface의 책임을 얼마나 명확히 운영하느냐에 가깝다.
5. human readability 문제는 global spec 본문 확장보다 summary/guide 같은 별도 surface 보강으로 해결하는 쪽이 현재 철학과 더 잘 맞는다.
6. 좋은 global spec의 기준은 "대부분을 설명했는가"가 아니라 "읽은 뒤 올바른 다음 판단으로 연결되는가"다.
7. 사람용 canonical overview는 `summary.md`, 기능별 상세 설명은 `guide`가 맡는 식으로 surface 책임을 분리하는 편이 적절하다.
8. review checklist는 개별 스킬마다 완전히 분리하기보다, 공통 코어 기준 위에 스킬별 추가 항목을 얹는 방식이 drift를 줄인다.
9. 공통 코어 checklist는 5축보다 4축이 더 실용적이며, 각 항목은 선언문보다 검사 질문형이 적절하다.
10. `navigation`과 `surface separation`은 통합 가능하지만, 최종 문항 안에서 두 요소가 모두 살아 있어야 한다.
11. `spec-summary`는 사람용 canonical overview 목적과 완전히 어긋나진 않지만, 현재 정의는 `status summary` 성격이 섞여 있어 목적 재정의가 필요하다.
12. `spec-summary`를 고칠 때는 template보다 `Goal/Acceptance Criteria`를 먼저 수정해야 회귀를 막을 수 있다.
13. `spec-summary`에서 `status / issues / next steps`는 핵심이 아니라 보조 섹션이어야 한다.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 이번 토론의 초점은 `global spec의 목적/독자 균형`으로 좁힌다 | 문제의 핵심이 문서량 자체보다 존재의의와 1차 역할 정의에 있음 | 1, 2 |
| 2 | global spec의 1차 역할은 `경계/결정 문서`다 | 사람과 LLM 모두에게 repo-wide 목적, 경계, 핵심 결정을 고정하는 것이 main 책임으로 더 적합함 | 1, 2 |
| 3 | 더 강하게 피할 실패는 `사람 가독성 붕괴`다 | thinness 자체보다, 사람이 판단 근거와 다음 경로를 못 얻는 상태를 더 문제로 봄 | 2, 5 |
| 4 | 선호 접근은 `thin core + reading map`이다 | main을 두껍게 키우지 않으면서도 사람의 탐색성과 판단 가능성을 높일 수 있음 | 3, 4 |
| 5 | 보완 수단은 `별도 summary surface`를 우선 고려한다 | human readability 문제를 main 확장이 아니라 별도 surface에서 해결하는 편이 drift 위험이 낮음 | 4, 5 |
| 6 | global spec은 계약 앵커로 두고, 사람 친화적 설명은 summary/guide가 맡아도 된다 | 문서 책임을 분리해야 main이 다시 코드 해설서가 되는 것을 막을 수 있음 | 1, 5 |
| 7 | global spec의 성공 기준은 `목적, 경계, 핵심 결정, 다음 읽을 surface`를 바로 말할 수 있느냐이다 | "많이 설명했는가"보다 "올바른 판단으로 연결되는가"가 더 적절한 평가 기준임 | 2, 6 |
| 8 | canonical human overview는 `summary.md`, 기능별 deep explanation은 `guide`가 맡는다 | 사람 친화성은 필요하지만 global main에 직접 싣기보다 별도 surface로 분리하는 편이 더 안정적임 | 5, 7 |
| 9 | reading map은 고정 형식보다 `중요하다고 판단되는 것은 자유롭게 허용` 원칙을 따른다 | 탐색성을 높이되 문서 형식 규칙이 다시 주객전도되는 것을 피하려는 판단 | 2, 7 |
| 10 | review checklist는 `spec-create`, `spec-rewrite`, `spec-upgrade`, `spec-review`에 있어야 한다 | global spec의 생성, 재구성, 업그레이드, 감사 단계 모두에서 같은 철학을 반복 검증해야 drift를 줄일 수 있음 | 4, 8 |
| 11 | checklist 구조는 `공통 코어 + 스킬별 추가`가 적절하다 | 핵심 철학은 공유하고, 각 스킬의 역할 차이는 추가 항목으로 분기하는 편이 일관성과 실용성의 균형이 좋음 | 8 |
| 12 | 공통 코어 checklist는 5축이 아니라 4축으로 압축한다 | checklist가 다시 비대해지지 않도록 유지비를 통제하면서도 핵심 판단은 남기기 위함 | 8, 9 |
| 13 | 공통 코어 checklist 항목은 `검사 질문형`으로 쓴다 | 생성/재작성/업그레이드/리뷰 단계 모두에서 자기점검과 감사 기준으로 재사용하기 쉽다 | 9 |
| 14 | 공통 코어 4문항 초안은 `Thinness / Decision-bearing truth / Anti-duplication / Navigation + surface fit`으로 확정한다 | 현재 철학을 가장 적은 수의 문항으로 충분히 포착하며, 사용자도 이 구조를 수용함 | 9, 10 |
| 15 | `spec-summary`는 폐기 대상이 아니라 `부분 적합, 목적 재정의 필요` 상태로 본다 | 이미 `_sdd/spec/summary.md`와 human-readable summary 역할을 갖고 있으나, status-heavy 해석 여지가 남아 있음 | 11 |
| 16 | `spec-summary` 수정의 최우선 순위는 `Goal/AC 재정의`다 | 상위 목적이 바뀌지 않으면 템플릿만 바꿔도 다시 상태 요약 중심으로 회귀할 가능성이 큼 | 11, 12 |
| 17 | `status / issues / next steps`는 `spec-summary`의 보조 섹션으로 축소한다 | canonical human overview의 주역은 목적/경계/결정/다음 읽을 surface여야 함 | 11, 13 |
| 18 | `spec-summary` 개편 패키지는 `목적 재정의 + AC 수정 + template 재배치 + global/temporary 서열 조정`으로 간다 | 스킬 분리 없이도 현재 철학에 맞게 정렬할 수 있는 가장 실용적인 수정 폭임 | 11, 12, 13 |

## 미결 질문 (Open Questions)
- [ ] 공통 코어 checklist를 실제로 어느 문서/스킬에 source-of-truth로 둘 것인가: 개별 `SKILL.md` 반복, 별도 reference, 혹은 definition/workflow 문서?
- [ ] `spec-create`, `spec-rewrite`, `spec-upgrade`, `spec-review` 각각에 어떤 스킬별 추가 checklist 항목을 붙일 것인가?
- [ ] `spec-summary`의 Goal/AC에 넣을 canonical human overview 문구를 정확히 어떻게 쓸 것인가?
- [ ] `spec-summary` 템플릿에 `How to Read This Spec` 또는 `Where Details Live` 같은 navigation 섹션을 어떤 이름과 위치로 넣을 것인가?

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | global spec의 성공 기준을 `목적/경계/핵심 결정/다음 경로` 관점으로 한 줄 명문화한다 | High | 사용자/후속 spec 작업 |
| 2 | `summary.md`와 `guide`의 책임 경계를 spec surface 정책으로 정리한다 | High | 사용자/후속 spec 작업 |
| 3 | reading map은 자유 허용하되, `판단/탐색 가치가 있을 때만 넣는다`는 운영 원칙을 명문화한다 | Medium | 사용자/후속 spec 작업 |
| 4 | 공통 코어 checklist 4문항을 기준 문안으로 고정한다 | High | 사용자/후속 spec 작업 |
| 5 | `spec-create`, `spec-rewrite`, `spec-upgrade`, `spec-review`에 공통 코어 checklist + 스킬별 추가 구조를 설계한다 | High | 사용자/후속 spec 작업 |
| 6 | supporting surface가 global truth를 복제하지 않도록 review 기준을 정리한다 | Medium | 사용자/후속 spec 작업 |
| 7 | `spec-summary`의 Goal과 Acceptance Criteria를 `canonical human overview` 중심으로 재작성한다 | High | 사용자/후속 spec 작업 |
| 8 | `spec-summary` 템플릿에서 status 섹션을 보조로 내리고 navigation/reading-map 성격을 전면에 둔다 | High | 사용자/후속 spec 작업 |
| 9 | global summary와 temporary summary의 목적 차이를 스킬 문서에서 더 강하게 분리해 서술한다 | Medium | 사용자/후속 spec 작업 |

## 리서치 결과 요약 (Research Findings)
- `_sdd/spec/main.md`: 현재 스펙은 이미 `thin global spec`으로 정의되어 있으며, repo-wide `개념 + 경계 + 결정`만 고정한다고 명시한다.
- `_sdd/spec/components.md`: component별 상세 설명을 배제하고 `Purpose / Why / Source` 중심의 compact reference-only surface로 운영 중이다.
- `_sdd/spec/usage-guide.md`: usage/expected result detail은 main이 아니라 supporting surface에서 다루는 구조다.
- `_sdd/spec/DECISION_LOG.md`: 과거에 `main.md`와 `components.md`가 과도하게 두꺼워져 다시 압축한 이력이 있어, "main 비대화"는 이미 한 번 실제 문제로 경험된 상태다.
- `_sdd/env.md`: 이 저장소는 마크다운/스킬 문서 중심 저장소라서, 전통적인 테스트보다 문서 discipline과 review semantics가 운영 품질에 더 직접적이다.

## Sources
- `_sdd/spec/main.md`
- `_sdd/spec/components.md`
- `_sdd/spec/usage-guide.md`
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/env.md`

## 토론 흐름 (Discussion Flow)
Round 1: 토론 범위를 `목적/독자 균형`으로 좁힘
Round 2: global spec의 1차 역할을 `경계/결정 문서`로 설정
Round 3: 더 우선적으로 피할 실패를 `사람 가독성 붕괴`로 확인
Round 4: `thin core + reading map` / `human-rich main` / `two-layer main` 중 권장안을 비교하고 `thin core + reading map`을 선택
Round 5: 해당 접근의 약점을 보완할 안전장치로 `별도 summary surface`를 선호
Round 6: 사람 친화성은 global spec이 아니라 별도 surface가 맡아도 된다는 철학을 수용
Round 7: 토론이 수렴했으나, `성공 기준 한 줄`은 추가로 정하기로 결정
Round 8: 성공 기준을 `목적/경계/핵심 결정/다음 surface`를 말할 수 있느냐로 확정
Round 9: 토론 종료 대신 정식 요약 문서 생성을 선택
Round 10: 사람용 canonical overview를 `summary.md`, 기능별 상세 설명을 `guide`로 분리하고, reading map은 중요 판단 기준에 따라 자유 허용하기로 정리
Round 11: review checklist는 `spec-create`, `spec-rewrite`, `spec-upgrade`, `spec-review`에 두고, 구조는 `공통 코어 + 스킬별 추가`로 정리
Round 12: 공통 코어 checklist는 5축 균형형으로 시작
Round 13: `navigation`과 `surface separation`은 separate 유지 대신 하나로 합쳐 4축으로 압축
Round 14: 각 항목은 선언형보다 검사 질문형이 적합하다고 정리
Round 15: 공통 코어 4문항 초안을 제시하고, 이 구성이 충분한지 검토
Round 16: 4문항 초안을 그대로 채택하고 토론 문서 반영을 선택
Round 17: `spec-summary`는 사람용 canonical overview 목적에 부분 적합하지만 목적 재정의가 필요하다고 판정
Round 18: `spec-summary` 수정의 최우선 순위를 `Goal/AC 재정의`로 설정
Round 19: `status / issues / next steps`는 핵심이 아니라 보조 섹션으로 축소하기로 정리
Round 20: `목적 재정의 + AC 수정 + template 재배치 + global/temporary 서열 조정` 패키지로 개편 방향을 확정

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 이번 라운드에서는 global spec 문제를 어떤 축으로 먼저 좁혀서 논의할까요?
**Options**: 1) 목적/독자 균형 2) 문서 깊이 경계 3) 지금 정리/종료
**A**: 목적/독자 균형
**Follow-up**: 토론의 핵심을 "얼마나 많이 쓸 것인가"보다 "누구를 위해 무엇을 보장할 것인가"로 좁혔다.

### Round 2
**Q**: global spec이 가장 먼저 보장해야 할 1차 역할을 무엇으로 볼까요?
**Options**: 1) 경계/결정 문서 2) 사람 이해 우선 3) 지금 정리/종료
**A**: 경계/결정 문서
**Follow-up**: main body의 책임을 repo-wide 판단 고정에 두고, 세부 설명은 별도 surface로 분리하는 방향이 강화됐다.

### Round 3
**Q**: 이 방향에서 특히 더 강하게 피하고 싶은 실패는 어느 쪽인가요?
**Options**: 1) 스펙 비대화 2) 사람 가독성 붕괴 3) 지금 정리/종료
**A**: 사람 가독성 붕괴
**Follow-up**: thinness 자체보다, 사람이 읽고도 판단 근거를 못 얻는 상태를 더 큰 위험으로 본다는 우선순위가 드러났다.

### Round 4
**Q**: 세 가지 접근 중 가장 맞는 방향은 무엇인가요?
**Options**: 1) thin core + reading map 2) human-rich main 3) 지금 정리/종료
**A**: thin core + reading map
**Follow-up**: global spec 비대화를 피하면서도 인간의 탐색 경험을 보완하는 접근을 선호했다.

### Round 5
**Q**: `thin core + reading map`의 실패를 막기 위해 가장 먼저 고정해야 할 안전장치는 무엇일까요?
**Options**: 1) 고정 템플릿 2) 별도 summary 표면 3) 지금 정리/종료
**A**: 별도 summary 표면
**Follow-up**: 인간용 설명량은 main에 직접 싣기보다 별도 요약 surface로 분리하는 것이 더 낫다는 판단이 나왔다.

### Round 6
**Q**: global spec은 계약 앵커로 두고, 사람 친화적 설명은 summary/guide 같은 별도 surface가 맡아도 된다고 봐도 괜찮을까요?
**Options**: 1) 네, 받아들임 2) 아니요, main도 더 설명적이어야 함 3) 지금 정리/종료
**A**: 네, 받아들임
**Follow-up**: global spec의 존재의의를 "많이 설명하는 문서"가 아니라 "올바른 판단을 고정하는 문서"로 재정의했다.

### Round 7
**Q**: 지금 정리할지, 아니면 `global spec의 성공 기준 한 줄`까지 더 정할지?
**Options**: 1) 정리해줘 2) 성공 기준 1개 더 3) 토론 종료
**A**: 성공 기준 1개 더
**Follow-up**: 철학적 합의만으로 끝내지 않고, 실제 운영 기준까지 명시하려는 필요를 확인했다.

### Round 8
**Q**: global spec의 성공 기준으로 어느 한 줄이 가장 맞을까요?
**Options**: 1) 판단+다음 경로 기준 2) 대부분 이해 기준 3) 지금 정리/종료
**A**: 판단+다음 경로 기준
**Follow-up**: main은 모든 지식을 담는 문서가 아니라, 목적/경계/결정/다음 읽을 곳을 정확히 안내하는 문서여야 한다는 기준을 얻었다.

### Round 9
**Q**: 지금까지 결론을 토론 요약으로 정리할까요, 아니면 미결 1개를 더 논의할까요?
**Options**: 1) 정리해줘 2) 미결 1개 더 3) 토론 종료
**A**: 정리해줘
**Follow-up**: 현재 합의 수준이면 후속 spec 작업이 바로 이어질 수 있다고 보고 토론을 종료했다.

### Round 10
**Q**: 미결 질문에 대한 운영 방침은 어떻게 둘까요?
**Options**: 사용자 자유 응답 기반 후속 정리
**A**: canonical 형태는 `summary.md`, 기능별 설명은 `guide`; reading map은 중요하다고 판단되는 것은 자유롭게 허용
**Follow-up**: 사람용 overview와 기능별 deep explanation의 책임 분리가 명확해졌고, reading map은 형식 규칙보다 실질적 탐색 가치가 우선이라는 합의가 생겼다.

### Round 11
**Q**: checklist 구조는 어떤 쪽이 더 좋을까요?
**Options**: 1) 공통 코어 + 스킬별 추가 2) 각 스킬 완전 독립 3) 지금 정리/종료
**A**: 공통 코어 + 스킬별 추가
**Follow-up**: checklist는 `spec-create`, `spec-rewrite`, `spec-upgrade`, `spec-review`에 두되, 공통 철학을 반복 검증할 수 있도록 shared core를 두는 편이 적절하다는 결론에 도달했다.

### Round 12
**Q**: 공통 코어 checklist의 기본 축으로 어떤 묶음이 가장 적절한가?
**Options**: 1) 5축 균형형 2) 4축 압축형 3) 지금 정리/종료
**A**: 5축 균형형
**Follow-up**: 처음에는 thinness, decision truth, anti-duplication, navigation, surface separation의 5축으로 출발하는 것이 자연스럽다고 봤다.

### Round 13
**Q**: `Navigation quality`와 `Surface separation`은 별도 축으로 유지할지, 하나로 합칠지?
**Options**: 1) 별도 유지 2) 하나로 합치기 3) 지금 정리/종료
**A**: 하나로 합치기
**Follow-up**: checklist 자체가 비대해지는 것을 피하기 위해 5축을 4축으로 압축하되, 통합 항목 안에 읽기 길찾기와 surface 책임 분리를 모두 담기로 했다.

### Round 14
**Q**: 이 4축을 checklist에 넣을 때 각 항목은 어떤 스타일이 더 좋은가?
**Options**: 1) 검사 질문형 2) 원칙 선언형 3) 지금 정리/종료
**A**: 검사 질문형
**Follow-up**: checklist를 실제 review와 self-check에 바로 쓸 수 있도록 yes/no형 질문 스타일이 적합하다고 판단했다.

### Round 15
**Q**: 공통 코어 checklist 4문항 초안으로 이대로 갈지, 4번만 더 다듬을지?
**Options**: 1) 이대로 간다 2) 4번만 더 다듬기 3) 지금 정리/종료
**A**: 이대로 간다
**Follow-up**: `Thinness / Decision-bearing truth / Anti-duplication / Navigation + surface fit`의 4문항이면 현재 철학을 충분히 담는다고 보았다.

### Round 16
**Q**: 이 결론을 토론 문서에 반영해 마무리할지, 스킬별 추가 항목까지 더 논의할지?
**Options**: 1) 문서 반영 후 마무리 2) 스킬별 추가 항목 1라운드 더 3) 토론 종료
**A**: 문서 반영 후 마무리
**Follow-up**: 공통 코어 checklist는 확정하고, 스킬별 추가 항목은 별도 후속 논의로 남겨 두었다.

### Round 17
**Q**: `spec-summary`가 canonical human overview 목적에 맞는지 어떻게 판정할까?
**Options**: 1) 부분 적합, 목적 재정의 필요 2) 대체로 충분히 적합 3) 역할 분리 필요
**A**: 부분 적합, 목적 재정의 필요
**Follow-up**: 현재 스킬은 이미 human-readable summary를 지향하지만, `현재 스펙과 구현 상태 요약` 성격이 섞여 있어 canonical overview로는 다소 흐릿하다고 보았다.

### Round 18
**Q**: `spec-summary`를 고친다면 어떤 축을 먼저 고정하는 게 가장 중요한가?
**Options**: 1) Goal/AC 재정의 2) Template 재배치 3) Global/Temporary 분기 강화
**A**: Goal/AC 재정의
**Follow-up**: 상위 목적이 바뀌지 않으면 실제 산출물도 다시 status-heavy summary로 회귀하기 쉽다는 판단을 확인했다.

### Round 19
**Q**: canonical human overview 기준이라면, `status / issues / next steps`는 `spec-summary`에서 어느 정도 비중이 맞는가?
**Options**: 1) 보조 섹션으로 축소 2) 지금처럼 핵심 섹션 유지 3) 별도 산출물로 분리
**A**: 보조 섹션으로 축소
**Follow-up**: `summary.md`의 주역은 목적/경계/결정/다음 읽을 surface여야 하고, 상태 정보는 뒤에 짧게 붙는 수준이면 충분하다고 정리했다.

### Round 20
**Q**: `spec-summary` 수정 패키지로 `목적 재정의 + AC 수정 + template 재배치 + global/temporary 서열 조정` 방향이 맞는가?
**Options**: 1) 이 방향으로 맞음 2) 더 세게 바꿔야 함 3) 지금 정리/종료
**A**: 이 방향으로 맞음
**Follow-up**: 스킬을 둘로 찢지 않고도, canonical human overview 쪽으로 충분히 재정렬할 수 있다는 결론을 얻었다.

## 공통 코어 Checklist 초안
1. `Thinness`
   main/global spec이 repo-wide 기준 문서 수준을 넘어서 inventory, 구현 해설, 장문 usage 설명으로 비대해지지 않았는가?
2. `Decision-bearing truth`
   main/global spec에 repo-wide 목적, 경계, 핵심 결정처럼 지속적으로 유지해야 할 truth만 남아 있는가?
3. `Anti-duplication`
   summary, guide, component/reference, log surface가 main의 truth를 장문으로 반복 복제하지 않는가?
4. `Navigation + surface fit`
   독자가 이 문서를 읽고 다음에 봐야 할 surface를 바로 알 수 있으며, 동시에 각 surface가 자기 책임(main/summary/guide/log)에 맞는 내용만 담고 있는가?
