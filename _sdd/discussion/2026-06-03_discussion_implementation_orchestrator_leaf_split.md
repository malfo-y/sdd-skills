# 토론 요약: implementation fan-out 재설계 — orchestrator/leaf 분리

**날짜**: 2026-06-03
**라운드 수**: 5 (analysis 중심)
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: 원래 "10개 mirror 스킬 → thin wrapper(agent dispatch)" 전환을 시도(DRY + 컨텍스트 절약). 그러나 pilot에서 **dispatch된 agent는 Agent 도구를 못 받아 sub-agent를 spawn할 수 없음**(플랫폼 nesting 1단계 제한)이 드러남 → fan-out 의존 스킬이 깨짐. 이후 graceful-degradation 검증으로 "정확성은 유지, 병렬성만 상실"임을 확인. 이 발견이 아키텍처 재설계 토론으로 이어짐.
- **토론을 시작한 배경**: 보류된 wrapper 작업의 후속. "대규모 구현일수록 병렬 이점이 크다 + 나는 직접 호출과 autopilot 둘 다 쓴다"는 사용자 요구에서, fan-out을 어디에 둘지 재설계 필요.
- **현재 상태 (코드 확인)**:
  - mirror 스킬 10종 중 **7종이 `Agent` 도구 선언**, 그러나 실제 fan-out은 **`implementation` 하나가 핵심**(impl-review는 large-scope 조건부). 나머지는 "병렬"이라 적혀도 자기 실행이 아니라 *산출 계획의 병렬성* 또는 미사용.
  - **codex agent = 단독 `.toml`**(본문이 `developer_instructions='''...'''`에 임베드) → 외부 reference 공유 불가. **codex skill = 디렉토리 + `references/`** 가능(단 스킬 간 공유는 불확실).
  - 이 repo는 **claude/codex 두 런타임을 항상 이중 유지** → DRY는 *제거*가 아니라 *최소화*가 한계.
  - autopilot은 이미 implementation-agent를 sub-agent로 dispatch(현재 순차 degrade regime).
- **범위와 제외 범위**: 이번 토론 = **implementation fan-out 재설계(Min scope)**. 제외(deferred): implementation-review 병렬화, non-fan-out 스킬의 wrapper 전환.
- **수집한 근거**: pilot V3 smoke(dispatch된 agent에 Agent 도구 없음), graceful-degradation 테스트(implementation-agent가 sub-agent 없이 직접 구현, `2 passed`), 파일 구조 점검(codex .toml 단독 / codex skill references/ 보유).

## 핵심 논점 (Key Discussion Points)

1. **fan-out 위치**: nesting 제약은 "agent가 또 agent를 까는" 한 단계만 막음. 따라서 fan-out은 **메인 루프 orchestrator**에 두고 **leaf agent는 단일 task**로 → 제약을 우회가 아니라 해소.
2. **공유 reference 불가**: planner가 agent(standalone)가 되면 `references/parallel_grouping.md` 공유 불가 → 해법은 "복제되는 알고리즘 덩어리 자체를 작게".
3. **그룹화=의존성 인코딩(B)**: 의미적 충돌 5패턴의 부피는 사실상 dependency. planner가 충돌을 **dependency edge로 기록**하면, 모두가 쓰는 그룹화 규칙이 "dep 없음 + Target Files disjoint → 한 그룹" 2~3줄로 축소.
4. **mutex vs dependency(B1)**: 무방향 상호배제(마이그레이션·config·상수)도 임의 방향 dep로 흡수. 실행 결과·readiness 게이팅 동일, 비용은 약한 문서 smell뿐.
5. **통합 규칙**: fan-out 스킬 → orchestrator 유지 + leaf agent / non-fan-out → wrapper→agent. 원래 wrapper 작업까지 한 규칙으로 정리.
6. **leaf 계약**: 기존 "Sub-Agent Prompt" 블록을 leaf agent 정식 계약으로 승격 + "leaf가 안 하는 것" 명시.
7. **autopilot 잔여 중복**: 두 orchestrator가 각자 fan-out 루프 보유하나, B로 그룹 파생이 trivial + 무거운 verify/review는 autopilot이 이미 보유 → 복제 최소.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | **leaf/orchestrator 분리**: `implementation-agent`=단일 task TDD leaf(+`Agent` 도구 제거), `implementation` skill·autopilot=fan-out orchestrator | nesting 제약 해소 + 직접/autopilot 양 경로 병렬 확보 | 1 |
| 2 | **통합 규칙**: fan-out→orchestrator+leaf / non-fan-out→wrapper→agent | 재설계와 원 wrapper 작업을 한 규칙으로 | 5 |
| 3 | **그룹화=B**: planner가 의미적 충돌을 dependency로 인코딩, orchestrator는 "dep 없음+Target Files disjoint" trivial 규칙으로 그룹 파생 | standalone 제약(공유 reference 불가) 하에서 복제 덩어리 최소화, 새 schema 불필요 | 2,3 |
| 4 | **B1**: dependency가 무방향 mutex 흡수(임의 방향) | 실행·readiness 결과 동일, 새 개념 0 | 4 |
| 5 | **orchestrator 가드레일**: fan-out 직전 그룹 내 Target Files disjoint 검사 → 위반 시 그 그룹만 순차 | plan staleness 방어 (full 알고리즘 아닌 set-intersection 한 줄) | 3 |
| 6 | **범위=Min**: implementation(orchestrator/leaf) + planner(feature-draft, impl-plan) dep-encoding + autopilot fan-out | 포커스 유지; impl-review·wrapper는 별도 | 6 |
| 7 | **leaf 계약 확정**: 입력(task 필드+Target Files+환경/테스트+선행 보장) / 규칙(TDD·파일 경계·Min-Code·Verification Gate·Spec 불가침) / 출력(결과·TDD표·파일·테스트·UNPLANNED_DEPENDENCY·발견) / **안 하는 것**(plan 파싱·그룹화·fan-out·post-group 회귀·phase review·progress·report 작성) | 기존 Sub-Agent Prompt 승격; orchestration은 전부 orchestrator로 | 6 |
| 8 | **환경/테스트 정보는 orchestrator가 전달** (leaf가 env.md 재탐색 안 함) | leaf context-minimal + N개 leaf의 중복 read 회피 | 7 |

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | implementation-review를 같은 orchestrator/leaf(병렬 레인)로 전환할지 | deferred-deliberately | Min scope 제외. read-only·조건부라 후순위 |
| 2 | non-fan-out 스킬 8종의 wrapper→agent 전환(원 작업) | deferred-deliberately | 통합 규칙(결정 2)으로 방향은 확정, 별도 트랙. graceful degrade로 de-risk됨 |

> in-scope 미결 0건. 위 2건은 의도적 보류.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `/feature-draft`로 Min scope 상세 계획(Target Files 포함) 작성 | High | 후속 |
| 2 | `implementation-agent` → leaf 축소(orchestration 제거, `Agent` 도구 제거, 계약 #7 반영) × claude/codex | High | 구현 |
| 3 | `implementation` skill → fan-out orchestrator(그룹 파생 #3 + 가드레일 #5 + leaf dispatch + post-group verify/회귀/phase review) × claude/codex | High | 구현 |
| 4 | planner(feature-draft, implementation-plan) → 의미적 충돌을 dependency로 인코딩(B/B1) × claude/codex (skill/agent 무관 content 변경) | High | 구현 |
| 5 | `sdd-autopilot` 구현 phase → "단일 agent dispatch"에서 "그룹별 leaf fan-out"으로 | High | 구현 |
| 6 | (deferred) impl-review 병렬화 / non-fan-out wrapper 트랙 | Low | 후속 |

## 리서치 결과 요약 (Research Findings)

- **nesting 제약**: dispatch된 agent는 `tools`에 `Agent`가 있어도 실제로는 못 받음 → 1단계 제한. 2회 독립 확인(forced smoke + 실제 task).
- **graceful degradation**: implementation-agent(항상 spawn 설계)조차 sub-agent 없이 직접 TDD로 완수(`2 passed`) → 정확성 유지, 병렬성만 상실.
- **codex 구조**: agent=단독 `.toml`(reference 불가), skill=디렉토리(`references/` 가능). claude/codex 항상 이중.
- **fan-out 실태**: mirror 스킬 중 실제 fan-out 핵심은 `implementation` 하나, impl-review가 large-scope 조건부. 나머지는 계획상 병렬성 또는 미사용.
- **병렬 이점 상한**: implementation 그룹 크기 상한 5 + phase 순차(review 게이트) → phase당 ~5배에서 saturate(선형 아님).

## 토론 흐름 (Discussion Flow)

- Round 1 (context): codex .toml standalone 제약 검증 → "공유 reference 불가" 확정, "복제 덩어리 최소화"로 문제 재정의.
- Round 2 (analysis): 그룹화 위치 A/B/C 제시 → **B(충돌=의존성)** 채택.
- Round 3 (critical review): 무방향 mutex vs 방향 dependency 약점 제기 → 실행 결과 동일 확인 → **B1(흡수)** 채택.
- Round 4 (priorities): 통합 규칙 도출 + **범위 Min** 확정.
- Round 5 (convergence): autopilot 잔여 중복 비판 → 수용 가능 확인 → **leaf 계약 구체화** + 환경 정보 출처(orchestrator 전달) 확정 → 수렴.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 그룹화 로직 위치 (standalone agent라 공유 reference 불가 전제)?
**Options**: B(충돌=의존성, 권장) / A(planner 명시적 그룹) / C(orchestrator 유지) / 종료
**A**: B.
**Follow-up**: 의미적 충돌 5패턴의 부피가 사실상 dependency라는 통찰 → 그룹화 규칙이 trivial로 축소.

### Round 2
**Q**: 무방향 mutex(마이그레이션·config·상수) 표현?
**Options**: B1(dependency 흡수, 권장) / B2(conflicts-with 추가) / 종료
**A**: B1.
**Follow-up**: 실행·readiness 결과가 방향 dep과 동일하므로 새 개념 없이 흡수.

### Round 3
**Q**: 작업 범위?
**Options**: Min(implementation 중심, 권장) / +impl-review / Full(wrapper까지) / 종료
**A**: Min.
**Follow-up**: 통합 규칙으로 wrapper 트랙은 별도 follow-up으로 분리.

### Round 4
**Q**: 수렴 확인 — 정리 vs 더 논의?
**A**: leaf agent 계약 구체화.
**Follow-up**: 기존 Sub-Agent Prompt를 leaf 정식 계약으로 승격 + 비책임 명시.

### Round 5
**Q**: leaf의 환경/테스트 정보 출처?
**Options**: orchestrator 전달(권장) / leaf가 env.md read / 정리
**A**: orchestrator 전달.
**Follow-up**: leaf context-minimal 유지, 수렴 → 정리.
