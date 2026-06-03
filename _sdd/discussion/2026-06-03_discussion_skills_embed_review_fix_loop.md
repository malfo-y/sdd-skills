# 토론 요약: 세 스킬에 producer→review→fix loop 내장 (+ feature-draft/implementation-plan orchestrator 승격)

**날짜**: 2026-06-03
**라운드 수**: 5 (context gathering 1 + analysis 4)
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: autopilot에는 구현 시 implementation → review → fix loop가 자동으로 들어가 있다. 이 패턴을 (1) `implementation` 스킬 자체에도 넣고, (2) `feature-draft`에는 feature-draft → plan-review → fix loop, (3) `implementation-plan`에는 plan → plan-review → fix loop로 각각 내장하고 싶다.
- **토론을 시작한 배경**: 직전 세션들에서 `implementation`을 orchestrator(skill)+leaf(agent)로 분리, mirror 스킬 9종을 thin wrapper로 전환, `investigate`를 wrapper→orchestrator로 승격하는 작업을 마쳤다. 그 연장선에서, 각 스킬이 자기 산출물의 품질 gate를 **자체 소유**하도록 만들려는 것. 후속으로 feature-draft/implementation-plan을 orchestrator로 승격하는 결정과 직접 연결된다.
- **현재 상태** (Explore 3-lane 조사로 확인):
  - **autopilot review-fix 계약** (`references/orchestrator-contract.md`): 순서 `review→fix→re-review`, exit `critical=0 AND high=0 AND medium=0`, agent 매핑 review=`implementation-review-agent`(opus)/fix=`implementation-agent`(sonnet), fix는 **finding 하나씩 순차** dispatch, scope `global`/`per-group`, MAX 도달 시 critical/high 잔존→중단·medium만→로그 후 진행, final integration review(adaptive).
  - **implementation 스킬**: 외부 review-agent를 **부르지 않음**. Step 6 Phase Review에서 orchestrator가 *인라인* 경량 품질체크 → Critical만 leaf 재dispatch, Quality는 문서화만.
  - **feature-draft / implementation-plan**: thin wrapper → agent. producer/reviewer 3개 agent 모두 **Agent 도구 미보유**(sub-agent spawn 불가).
  - **plan-review-agent**: 입력으로 feature draft Part 2 **또는** implementation plan 수용, 출력 Blocker Status `BLOCKED/CLEAR`, **native 정책 = Critical/High만 blocker·Medium/Low advisory**, 리포트 `_sdd/implementation/<date>_plan_review_<slug>.md`.
  - 산출물 경로: feature-draft `_sdd/drafts/<date>_feature_draft_<slug>.md`(Part 1 temp spec + Part 2 plan), implementation-plan `_sdd/implementation/<date>_implementation_plan_<slug>.md`.
- **범위와 제외 범위**:
  - **In**: `implementation`/`feature-draft`/`implementation-plan` 세 스킬에 review-fix loop 내장, feature-draft·implementation-plan의 wrapper→orchestrator 승격, 양 플랫폼(claude/codex).
  - **Out**: **autopilot은 건드리지 않음** — autopilot이 만드는 오케스트레이터는 스킬을 호출하지 않고 `*-agent` leaf를 **직접 dispatch**하므로, 스킬 내장 loop와 실행 경로가 겹치지 않는다(개념적 유사 ≠ 이중 실행).
- **수집한 근거**: `.claude/skills/sdd-autopilot/SKILL.md`, `references/orchestrator-contract.md`(§2/§Review-Fix Loop/Model Routing), `.claude/skills/implementation/SKILL.md`(Step 5/6/7), `.claude/agents/{feature-draft-agent,implementation-plan-agent,plan-review-agent}.md`, 세 wrapper SKILL.

## 핵심 논점 (Key Discussion Points)

1. **autopilot 이중화 우려 해소**: 처음엔 implementation 스킬 loop와 autopilot review-fix gate의 책임 중복을 우려했으나, 사용자가 "autopilot의 오케스트레이터는 스킬이 아니라 agent를 직접 부른다 → 실행이 겹치지 않는다"고 지적. autopilot을 범위에서 제외.
2. **fix 수행 주체**: producer-agent 재dispatch vs orchestrator 인라인.
3. **loop exit condition**: reviewer native 정책(plan-review=High까지) vs 통일.
4. **MAX iteration 가드**: Medium까지 fix 시 수렴 위험 → MAX 도달 시 처리 정책.
5. **① implementation 형태**: 기존 인라인 Step 6 self-review와 외부 review-agent loop의 결합 방식.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | **범위 = 세 스킬만, autopilot 제외** | autopilot은 `*-agent` leaf 직접 dispatch → 스킬 내장 loop와 실행 경로 분리, 충돌·이중실행 없음 | 1 |
| 2 | **feature-draft / implementation-plan을 wrapper→orchestrator로 승격** | loop를 돌리려면 메인 루프(스킬)가 reviewer agent를 dispatch해야 함(leaf agent는 sub-agent spawn 불가). 검증된 동형 선례는 `implementation` 스킬(orchestrator가 loop 소유 + fix=leaf 재dispatch). (investigate도 wrapper→orchestrator로 갔으나 fix=인라인 write·read-only Explore fan-out이라 본 review-fix/producer-재dispatch 메커니즘의 선례는 아님) | 1 |
| 3 | **fix = producer-agent 재dispatch (fix mode)** | feature-draft-agent/implementation-plan-agent가 review finding을 입력받아 자기 산출물 수정. implementation의 `fix=leaf 재dispatch`와 동형, 산출물 단일 작성자(agent) 유지 | 2 |
| 4 | **exit = `critical=high=medium=0` (세 loop 통일)** | 가장 엄격·일관. 세 loop가 동일 정책 | 3 |
| 5 | **MAX 처리 = autopilot과 동일** | MAX iteration(기본 3) 도달 시 critical/high 잔존→중단·사용자 보고, medium만 잔존→로그 후 진행(산출물 사용). medium은 fix '시도'하되 막히면 advisory로 graceful degrade → 무한루프 방지 | 4 |
| 6 | **① = 인라인 Step 6를 외부 `implementation-review-agent` loop로 교체** | phase(또는 실행분) 완료 후 review-agent 외부 호출→fix(implementation-agent leaf 재dispatch, finding 순차)→re-review. autopilot review-fix와 동형, review 단일 소유 | 5 |
| 7 | **feature-draft Mode B 유지** | 승격 후에도 orchestrator가 대화 맥락 digest를 수집해 producer-agent에 전달(생성·fix 라운드 모두). 입력이 대화에서 태어나는 특성 보존 | 확인사항 |
| 8 | **codex parity** | 양 플랫폼(.claude/.codex) 동시 구현 | 확인사항 |
| 9 | **re-review scope = 범위 전체 재리뷰** | 변경분만 아니라 loop 범위 전체 재리뷰(autopilot 동형) | 확인사항 |
| 10 | **producer-agent fix mode 입력 = review 리포트 경로 + 기존 산출물 경로** | producer-agent에 "fix mode" 입력 계약 추가(finding 반영 수정) | 확인사항 |

## 미결 질문 (Open Questions)

없음 (in-scope 미결 0건). 세부 구현 결정(re-review 시점 세부, progress/report 소유, 승격 시 Mirror/Source Notice 처리 등)은 feature-draft Part 2에서 확정.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | feature-draft로 상세 설계 + 구현계획(Part 2) 작성 — 세 스킬 review-fix loop 내장 + ②③ orchestrator 승격 | High | 다음 단계 |
| 2 | producer-agent(feature-draft-agent/implementation-plan-agent)에 fix mode 입력 계약 추가 | High | 구현 |
| 3 | implementation 스킬 Step 6 인라인 self-review → 외부 review-agent loop 교체 | High | 구현 |
| 4 | 양 플랫폼(claude/codex) parity 유지 | High | 구현 |
| 5 | plan-review로 계획 감사 후 구현 | Medium | 후속 |

## 리서치 결과 요약 (Research Findings)

- **autopilot loop 계약**: review→fix→re-review / exit `critical=high=medium=0` / fix=finding 순차 dispatch / MAX 도달 분기(critical·high→중단, medium→로그 후 진행) / final integration review adaptive. → 세 스킬 loop의 참조 템플릿.
- **implementation 현 상태**: 외부 review-agent 미사용, orchestrator 인라인 Step 6 품질체크가 사실상 self-review-fix(Critical만 자동수정). → 외부 loop로 교체 대상.
- **3 agent 모두 Agent 도구 미보유**: 승격 시 loop orchestration은 반드시 메인 루프(스킬)가 소유해야 함을 확정.
- **plan-review 유연 입력**: feature draft Part 2와 implementation plan 둘 다 리뷰 → ②③ 공통 reviewer로 재사용 가능.

## 토론 흐름 (Discussion Flow)

Round 0 (context): Explore 3-lane 병렬 → autopilot loop 계약 / implementation 현 review 구조 / producer·reviewer agent 입출력 계약 수집
Round 1: autopilot 이중화 정합화 질문 → 사용자가 "agent 직접 호출이라 안 겹침" 정정 → autopilot 범위 제외
Round 2: fix 주체 → producer-agent 재dispatch (fix mode)
Round 3: exit condition → 세 loop 통일 (Medium까지)
Round 4: MAX 가드 (critical_review: Medium fix 수렴 위험 지적) → autopilot과 동일 처리
Round 5: ① 형태 → 인라인 Step 6를 외부 loop로 교체 → 수렴, feature-draft로

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: implementation 내장 loop와 autopilot review-fix gate 책임 중복을 어떻게 정리?
**A**: (clarify) "autopilot 오케스트레이터는 스킬이 아니라 agent를 직접 부르므로 실행이 겹치지 않는다."
**Follow-up**: 정정 수용 → autopilot 범위 제외, 세 스킬에만 집중.

### Round 2
**Q**: review가 이슈를 찾은 뒤 fix를 누가 수행?
**Options**: 1) producer-agent 재dispatch(권장) 2) orchestrator 인라인 fix
**A**: producer-agent 재dispatch.
**Follow-up**: producer-agent에 fix mode 입력 계약 추가 필요.

### Round 3
**Q**: loop exit condition (reviewer native 정책 상이)?
**Options**: 1) reviewer native 존중 2) 통일(Critical/High) 3) 통일(Medium까지)
**A**: 세 loop 통일 (Medium까지).
**Follow-up**: plan 단계 과잉 fix·수렴 위험 → MAX 가드 필요성 제기.

### Round 4
**Q**: MAX iteration 도달 시 처리?
**Options**: 1) autopilot과 동일(권장) 2) 엄격 중단 3) 느슨 진행
**A**: autopilot과 동일.
**Follow-up**: medium은 fix 시도하되 MAX에서 막히면 advisory degrade.

### Round 5
**Q**: ① implementation 형태(인라인 Step 6 vs 외부 loop)?
**Options**: 1) 인라인을 외부 loop로 교체(권장) 2) 인라인 유지+외부 추가(2단)
**A**: 인라인 Step 6를 외부 loop로 교체.
**Follow-up**: 수렴 → 정리 후 feature-draft.
