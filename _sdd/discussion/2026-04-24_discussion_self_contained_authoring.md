# 토론 요약: Self-Contained Authoring 원칙 (feature-draft / implementation-plan)

**날짜**: 2026-04-24
**라운드 수**: 9
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **적용 범위 결정**: 원칙을 어떤 산출물까지 적용할지. implementation 산출물(implementation-plan.md + feature-draft Part2)만으로 좁힘. Part1 temp spec은 canonical spec에 머지되므로 scope 제외.
2. **원칙의 목적 재정의**: 처음엔 "subagent fresh-context 대비"로 프레임했으나, 사용자가 "reader autonomy — 다른 문서 없이도 읽히는 문서"로 재정의. subagent 케이스는 하위 사례일 뿐.
3. **두 갈래 실패 양상**: (a) 대화 context 유실(결정의 *이유*가 대화에만 남고 문서엔 미기재), (b) 외부 참조 암묵(문서가 다른 spec/코드 상태를 암묵 전제). 둘 다 같은 무게로 심각.
4. **Rule 1 재정의**: "근거 누락"이 아니라 **결정 자체 누락**이 더 큰 실패. 대화/외부 문서에서 내려진 결정이 draft에 *명시조차 안 되는* 문제가 1차. 근거 부재는 그 다음 문제.
5. **구조 추가 vs 작성 규율**: 현재 스킬은 이미 충분한 구조(Overview, Components, Task Details 등)를 갖고 있음. 실패 원인은 "구조 안에 채우는 글이 암묵적"이라는 것. 따라서 새 필드 신설보다 **작성 규율(negative rule)** 성격이 적합.
6. **AC teeth**: 단순 self-judgment("갭 없음")으로 통과되는 것 방지. 기계적 체크(Pass 1)와 구조화된 fresh-reader readthrough(Pass 2) 이중 장치 + 절차 흔적 기록.
7. **Thinness 축과의 관계**: Thinness(복사 금지, delta만)와 이 원칙(grounding 요구)은 층위 다름. grounding은 패러프레이즈·재진술이지 복사가 아니므로 상보적 관계.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 원칙 이름: **Self-Contained Authoring** (한국어: 자기완결 작성) | 사용자가 처음 쓴 용어 "self-contained" 계승, 작성 방식 규정이라는 내용과 맞닿음 | 1, 2 |
| 2 | 적용 범위: `implementation-plan.md` 전체 + `feature-draft` Part2 (implementation plan). Part1 temp spec은 제외 | Part1은 canonical spec으로 머지돼 별도 경로를 탐. 실패가 가장 크게 발현되는 곳은 implementation 산출물 | 1 |
| 3 | **Rule 1 (Decision & Assumption Surfacing)**: 이 문서의 실행에 필요한 모든 결정과 가정은 — 작성 대화/다른 문서/이전 토론 어디서 도출됐든 — 이 문서에 명시적으로 기록. "이미 결정됐으니" 생략 금지. 외부 결정이라도 (a) 결정 내용 재진술 + (b) 출처를 Rule 2 형식으로 grounding | 실패 1차 양상(결정 누락)을 정면으로 차단 | 4 |
| 4 | **Rule 2 (Reference Grounding)**: 외부 참조(spec 조항, 코드 경로, 결정 로그)는 bare path만 남기지 않음. 참조가 *이 문서의 어떤 판단·변경과 연결되는지*를 inline으로 서술. "the X를 수정" 류 대명사적 지시 금지 — 경로/ID 명시 | 실패 2차 양상(암묵 참조) 차단. "현재 상태 1줄 요약"이 공허화될 위험을 "판단과의 연결" 초점으로 해결 | 3 |
| 5 | **Rule 3 (Vocabulary Grounding)**: 프로젝트 고유 용어·개념은 최초 사용 시 1줄 정의 또는 Rule 2 준수 참조 동반 | Rule 1·2의 특수 사례지만 다른 메커니즘(공유 어휘 전제)이라 별도 rule화 | 3 |
| 6 | **AC (Self-Containment Check) — X1+X2 hybrid + 절차 흔적 기록**. Pass 1: 문서 내 모든 외부 path/ID 참조 enumerate, 각각 Rule 2 준수 확인. Pass 2: fresh-reader readthrough로 각 섹션 지시·결정·전제에 대해 "이 문장을 따르려면 뭘 알아야 하는가?" 질문해 갭 탐지. Pass 1·2 수행 결과(검토 섹션 수, 발견 갭 수, 보완 여부)를 Final Check 체크리스트로 기록 | 단순 self-judgment 회피. 기계적(Rule 2) + 구조적(Rule 1) 이중 teeth | 6 |
| 7 | **feature-draft Part2 ↔ Part1 carve-out**: 같은 파일 내 공존이므로 Part2가 Part1 결정·계약 참조 시 **ID + inline purpose**만 달면 Rule 2 준수로 인정 (예: "Contract C3 반영 — 세션 토큰 HMAC 검증"). Part1 전체를 Part2에 재진술할 필요 없음 | reader autonomy는 파일 수준에서 충족됨. 같은 파일 위로 스크롤만 해도 Part1 읽힘 | 1, 2 |
| 8 | **implementation-plan.md는 별도 파일**이므로 feature-draft 참조 시 full Rule 1+2 적용. 원 feature-draft의 결정 내용을 implementation-plan.md 자체에 surface | 별도 파일 reader는 feature-draft를 열지 않고도 이해 가능해야 함 | 2 |
| 9 | **배치**: Rules 1-3 → SKILL.md의 Hard Rules 섹션. AC → Acceptance Criteria에 한 줄 추가. Final Check 섹션에 Pass 1/2 체크리스트. 원칙 설명 → SKILL.md 상단 또는 Key Principles 짧게 | 기존 스킬 구조와 관행에 맞춤. 중복 기술(self-contained skill 관행) | - |
| 10 | **Thinness 축과 상보**: grounding은 복사가 아니므로 Thinness 위배 없음. Thinness = "쓰지 마라", 이 원칙 = "쓴다면 이렇게" | SDD_SPEC_DEFINITION 4축과의 정렬 명시 | 7 |

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| Q1 | X3 외부 fresh-reader 서브에이전트 검증을 도입할지 | deferred-deliberately | 1차 도입 후 효과 관찰하고 2차 결정. 비용·복잡도·재귀 context 문제 존재 |
| Q2 | X4 parent conversation log를 스킬 입력으로 전달하는 구조 변경 | deferred-deliberately | 현재 스킬 입력 구조 변경이 필요하므로 별도 설계 필요 |
| Q3 | 도입 후 효과 관찰 방법 (어떻게 측정할지) | deferred-deliberately | 별도 토론 주제로 이관. 본 원칙 1차 도입과 분리 |
| Q4 | `plugins/sdd-skills/` 경로 실존 및 반영 범위 | needs-data | MEMORY는 "플랫폼 parity" 기재, Explore는 `.claude/`만 발견. 실제 편집 작업 시 Glob으로 재확인 필요 |
| Q5 | spec-create, spec-update-todo 등 다른 SDD 산출물로 확대할지 | out-of-scope | 본 토론에서 명시적으로 implementation 산출물만으로 좁힘. 확대 여부는 별도 토론 |

> 카테고리: 모두 사용자 확인 없이 자동 부여 — `(auto-labeled, please review)`. 사용자가 "제안 그대로 확정 → 요약 생성"을 명시 선택했으므로 그대로 기록.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `.claude/skills/feature-draft/SKILL.md` 편집: Rule 1/2/3 추가 (Part2 대상 명시), AC 추가, Final Check 체크리스트, Part1↔Part2 carve-out 조항 | High | (추후 결정) |
| 2 | `.claude/skills/implementation-plan/SKILL.md` 편집: Rule 1/2/3 추가 (문서 전체 대상), AC 추가, Final Check 체크리스트 | High | (추후 결정) |
| 3 | 대응 agent 파일(`.claude/agents/{feature-draft,implementation-plan}.md`)에 동등 guidance 반영 검토 | Medium | (추후 결정) |
| 4 | `plugins/sdd-skills/` 하위 동일 스킬 실존 여부 확인 후 병렬 적용 (Q4 해소 후) | Medium | (추후 결정) |
| 5 | 1차 도입 후 효과 관찰 방법 별도 토론 (Q1, Q3) | Low | (추후) |

## 리서치 결과 요약 (Research Findings)

Explore sub-agent가 수집한 주요 사실:
- 두 스킬 모두 `Agent(subagent_type=...)` 로 fresh context에서 spawn 가능한 internal agent로 선언됨
- 현재 두 스킬 어디에도 "self-contained" 하드 룰 없음. 다만 `2026-04-13_feature_draft_spec_update_shared_core_self_containment.md` 초안에서 shared-core 축에 대해 self-contained 요구 등장 (이번 토론과 다른 맥락)
- 참조 관행: 경로 기반 암묵 참조(Touchpoints, Target Files `[C]/[M]/[D]`)가 현재 표준. Inline 요약·quote 관행 없음
- `SDD_SPEC_DEFINITION.md` 4축(Thinness, Decision-bearing truth, Anti-duplication, Navigation+surface fit)에 self-containment 명시 없음. 본 원칙은 4축과 층위 다른 보완 관계
- Target Files의 `[TBD] <reason>` 패턴은 "미해결은 명시하라"는 취지라 본 원칙과 결이 같음

## 토론 흐름 (Discussion Flow)

- Round 1: 토픽·범위 확인 → 원칙을 implementation 산출물로 좁힘
- Round 2: 목적 재정의 → "reader autonomy" (subagent context 아님)
- Round 3: 초기 A/B/C 접근 제시 → 사용자 전면 재프레임 요구
- Round 4: 실패 양상 taxonomy 합의 → (a) 대화 유실 + (b) 참조 암묵, 둘 다 동일 심각
- Round 5: A+C hybrid 방향 합의 → 작성 규율 + self-check 조합
- Round 6: Rule 1 재정의 → "근거" 보다 "결정 자체 surfacing"이 주
- Round 7: AC teeth 방향 → X1+X2 hybrid + 절차 흔적 기록
- Round 8: 마무리 디테일 → 이름(Self-Contained Authoring), Part1 carve-out, 배치 확정
- Round 9: Wrap-up → 요약 생성 결정

## 부록: 대화 로그 (Conversation Log)

### Round 1 — Scope
**Q**: self-contained 원칙의 적용 범위를 어디까지로?
**Options**: Implementation 산출물만 / feature-draft 전체+implementation-plan / 모든 SDD 산출물
**A**: Implementation 산출물만
**Follow-up**: Part2 + implementation-plan.md만 대상. Part1 별도 경로.

### Round 2 — Purpose
**Q**: self-contained 원칙의 주된 목적?
**Options**: Reader autonomy / Subagent fresh context 안정성 / 시간 경과 대응 / 기타
**A**: Reader autonomy
**Follow-up**: 일반 기술 문서 자기완결성 원칙에 가까움. Subagent 케이스는 하위.

### Round 3 — Initial approach alternatives (재프레임됨)
**Q**: narrative self-containment / Context 섹션 / Rationale 필드 / 하이브리드
**A**: "아예 다르게 접근해 보자. 지금 문제는 작성되는 문서가 외부 문서나 대화 context를 암묵적으로 가정하고 작성되어서 나중에 다시 보면 외부 정보나 대화 context가 유실된 상태에서 내용을 이해할 수 없다는 거야."
**Follow-up**: 구조 제안 방식 폐기, 실패 양상 재분석으로 선회.

### Round 4 — Failure modes
**Q**: (a) 대화 context 유실 / (b) 외부 참조 암묵 중 어느 쪽이 주?
**A**: 둘 다 비슷하게 심각
**Follow-up**: 원칙 설계를 2-prong으로.

### Round 5 — A+C hybrid direction
**Q**: A+C 하이브리드 / B(구조 필드) / 정리해줘 / 기타
**A**: A+C 좋음, 디테일 뒤집자
**Follow-up**: 작성 규율 + AC self-check 조합으로 디테일.

### Round 6 — Rule 1 재정의
**Q**: Rule 1/AC 재작성본 어디 먼저 다듬을까
**A**: "Rule 1의 경우 '근거' 가 없는 것도 문제일 수 있지만 더 큰 문제는 다른 문서나 컨텍스트에서 이루어진 '암묵적 결정' 을 draft에 명시하지 않는 경우야."
**Follow-up**: Rule 1 무게중심을 "이유 붙이기"에서 "결정 자체 surfacing"으로 이동.

### Round 7 — Rule 1 fit check
**Q**: 재작성된 Rule 1 적절? 가정 포함 오버? 더 강해야?
**A**: 맞음. 다음 디테일로 넘어가자.

### Round 8 — AC teeth
**Q**: X1+X2 + 흔적 기록 / X3 추가 / X2만 / 기타
**A**: X1+X2 hybrid, 흔적 기록 포함
**Follow-up**: Pass 1(기계적) + Pass 2(구조적 readthrough) + 체크리스트.

### Round 9 — Wrap-up
**Q**: 이름/Part1 carve-out/배치 확정하고 정리로?
**A**: 제안 그대로 확정 → 요약 생성
**Follow-up**: Step 4 진입.
