# 토론 요약: task ordering을 feature-draft에서 분리해 구현 직전으로 late-binding

**날짜**: 2026-07-09
**라운드 수**: 7
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: "implementation-plan 스킬을 요새 거의 안 쓴다. feature-draft 다음에 바로 implementation으로 넘어가게 된다. 대규모 구현도 feature-draft에서 phase를 나눠주고, implementation에서 알아서 review phase가 들어간다." → 파이프라인에 죽은 단계가 껴 있는 것 아닌가.
- **토론을 시작한 배경**: 직전 세션에서 feature-draft/implementation-plan 두 producer의 검증 패스를 단일화하는 성능 작업(브랜치 `perf/feature-draft-single-pass-and-review-diet`)을 하며 두 agent가 near-duplicate임을 확인. 그 연장선에서 implementation-plan의 존재 이유를 재검토.
- **현재 상태 (코드 확인)**:
  - `implementation/SKILL.md` Step 1 task-set 탐색경로 **6번 = `_sdd/drafts/*_feature_draft_*.md` (Part 2: 구현 계획)** — implementation이 feature-draft Part 2를 plan으로 직접 파싱한다.
  - `implementation/SKILL.md` Step 6/7 — phase별·cross-phase review-fix gate를 implementation이 자체 소유한다(plan 출처와 무관하게 리뷰가 들어감).
  - `sdd-autopilot/SKILL.md` planning precedence(line 162) — "multi-phase면 `implementation-plan-agent` 필수, single-phase는 feature-draft → implementation 직행".
  - `orchestrator-contract.md` §8 — implementation-plan의 고유 계약은 phase별 `goal / task-set / dependency closure / validation focus / exit criteria / carry-over / Checkpoint`.
  - `feature-draft-agent` ↔ `implementation-plan-agent`는 near-duplicate producer(같은 Target Files 규격, 같은 Contract/Invariant Delta, 같은 `plan-review-agent` 리뷰어).
- **범위**: implementation-plan 단계의 재배치(무엇을 어디로 옮길지, 이름·하위호환 전략). **제외 범위**: 실제 구현 착수(별도 작업), deprecated mirror의 완전 제거 시점.

## 핵심 논점 (Key Discussion Points)

1. **왜 안 쓰이나 (진단)**: feature-draft Part 2가 dependency까지 인코딩해 implementation이 직행 가능 + implementation이 리뷰를 자체 소유 → implementation-plan은 손작업 경로에서 체감상 아무것도 더하지 않는다. 유일한 잔여 니치는 autopilot multi-phase per-group gate(Checkpoint 계약)와 spec-first 예외뿐.
2. **무엇을 옮길 것인가**: (초안) Part 2 전체를 implementation-plan으로 이동 → **사용자 정정**: Part 2는 feature-draft가 계속 소유하고, 그 안에서 **task 간 dependency 계산 + task ordering** 조각만 분리한다.
3. **late-binding의 근거**: ordering을 구현 직전으로 미루는 이득의 근원이 (1) 전체 조망(task를 다 정의해야 의존 그래프 전모가 보임) 인가 (2) 코드베이스 실측 인가 → **(1) 전체 조망이 핵심**으로 확정. 따라서 ordering 단계는 코드베이스 재훑기 없는 경량 계산.
4. **이름 충돌 & 하위호환**: skill 제거 + deprecated mirror 유지 결정 시, 같은 `implementation-plan` 이름 아래 agent(=ordering)와 skill(=feature-draft mirror)이 정반대 일을 하게 되는 충돌 발견 → 이름 분리(옵션 B)로 해소.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| D1 | task ordering(dependency edge 계산 + 순서 + phase 분할 + multi/single 판정)을 feature-draft에서 분리해 **구현 직전으로 late-binding**한다 | `사용자 판단` + `코드 확인`(implementation이 이미 dependency edge를 "신뢰하되 런타임 가드"로 소비 — file-disjoint 가드레일/RED 게이트/phase review) | 1, 3 |
| D2 | feature-draft Part 2는 **task 정의(AC·Target Files·Contract/Invariant Delta·Validation Plan)를 그대로 유지**하고, dependency edge·phase 그룹핑·multi/single 선언만 제거해 **dependency 없는 flat task-set**을 낸다. `plan-review-agent`는 task 정의를 계속 검증(살아있음) | `사용자 판단` | 2 |
| D3 | ordering 단계는 **review-fix loop 없이 self-check만** 수행하고, single/multi 무관하게 **항상 경유**한다 | `사용자 판단` + `코드 확인`(ordering은 확정된 task 정의에서 파생되는 결정론적 계산) | 3 |
| D4 | 신규 **`task-ordering-agent`** 도입 — feature-draft가 남긴 flat task-set만 입력받아 전체 조망 → dependency edge + ordering + phase 분할 + Checkpoint 배치 산출. 코드베이스 실측 없음 | `사용자 판단` | 3 |
| D5 | `implementation-plan` **skill + agent**를 통째로 **deprecated feature-draft mirror**로 전환(하위호환) — 기존 트리거 보존, 실동작은 새 feature-draft로 위임 | `사용자 판단` | 4 |
| D6 | 이름 충돌은 **옵션 B(이름 분리)**로 해소 — 새 역할엔 `task-ordering-agent` 새 이름, `implementation-plan` 네임스페이스는 하위호환 껍데기로 은퇴 | `사용자 판단` + `코드 확인`(repo의 핵심 가치 = legibility) | 4 |
| D7 | 배선: implementation은 Step 1(task-set 확보) 후 **항상 `task-ordering-agent`를 dispatch** → Step 3 wave 파생. autopilot은 `feature-draft → task-ordering → implementation`으로 재배선하고 "multi-phase면 필수/single 직행" precedence를 폐기 | `사용자 판단` | 2, 3 |
| D8 | `plan-review-agent`에서 dependency·parallelism·phase 관련 추출/리뷰 항목을 제거(ordering은 task-ordering 소관이므로 리뷰 대상 아님) | `사용자 판단`(D1의 파생) | 2 |

### 기각한 대안

- **Part 2 통째로 이동 + plan-review-agent 은퇴** (AI 초안): feature-draft에서 task 정의까지 전부 implementation-plan으로 옮기고 plan-review loop를 양쪽에서 제거하는 안. → **기각.** 사용자 의도는 task 정의를 feature-draft에 남기고 **ordering 조각만** 떼는 훨씬 좁은 변경. plan-review-agent는 task 정의 리뷰어로 그대로 유지.
- **현상 유지(안 쓰지만 놔둠)**: autopilot·spec-first 예외 보험으로 남기는 안. → 채택 안 함(중복 유지보수 부담).
- **옵션 A(이름 유지 + 충돌 감수)**: `implementation-plan-agent` 이름을 ordering에 재사용하고 skill만 deprecated mirror로. → 기각. skill이 자기 이름의 agent를 안 부르는 상태가 되어 legibility 훼손.

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| Q1 | `task-ordering-agent`가 feature-draft의 task 정의(Contract/Invariant Delta·Target Files)만으로 dependency edge를 신뢰성 있게 복원할 수 있는가 — "전체 조망"만으로 충분한지 | needs-data | 구현 후 실측으로 검증. 이 가정이 깨지면 D1의 전제(ordering=순수 파생)가 흔들림 → 후속 작업 중단 조건과 연결 |
| Q2 | 진행 방식: (가) 이 변경을 feature-draft에 태워 도그푸딩 vs (나) 직접 브랜치 구현 | deferred-deliberately | 설계 확정 후 별도 결정. AI 추천은 (가) 도그푸딩 |
| Q3 | deprecated `implementation-plan` mirror의 완전 제거(deprecation) 시점 | deferred-deliberately | 새 경로 안정화 확인 후 |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 진행 방식(Q2) 결정 후 이 설계로 구현 착수 | High | 사용자 + AI |
| 2 | 영향 표면 census 작성 및 적용 (아래 후속 핸드오프의 검증 항목) | High | AI |

### 후속 핸드오프 (Handoff)

- **목표**: task ordering을 feature-draft에서 분리해 신규 `task-ordering-agent`로 구현 직전 late-binding하고, `implementation-plan`은 deprecated feature-draft mirror로 은퇴시킨다. **관찰 가능한 완료 기준**: (a) feature-draft Part 2에 dependency edge·phase 그룹핑·multi/single 선언이 없다(flat task-set), (b) `task-ordering-agent`가 신규 등록되어 flat task-set → ordering을 산출한다, (c) implementation/autopilot이 구현 전 항상 ordering을 경유한다, (d) plan-review-agent에서 dependency/parallelism/phase 항목이 제거됐다, (e) 기존 `implementation-plan` 트리거가 새 feature-draft로 위임되어 깨지지 않는다.
- **변경 금지 제약**: feature-draft Part 2의 task 정의 계약(AC·Target Files·Contract/Invariant Delta·Validation Plan), plan-review의 task-정의 검증, implementation의 런타임 가드(file-disjoint 가드레일·RED 게이트·phase review-fix gate)는 건드리지 않는다. 기존 `implementation-plan` 사용자 트리거 문구를 보존한다.
- **검증**: 신규 agent 등록 갭 점검(`marketplace.json` agents 배열 + codex README), rename/deprecation census는 변형형(kebab/underscore/공백/글롭/slash)과 claude·codex 짝 모두 커버, 하네스 §섹션 propagation, claude/codex 미러 parity, 이 repo 자체의 spec surface(`_sdd/`) 갱신.
- **중단 조건**: `task-ordering-agent`가 task 정의만으로 dependency를 신뢰성 있게 복원하지 못한다고 판단되면(Q1의 "전체 조망" 가정이 깨지면) 중단하고 보고한다.

## 리서치 결과 요약 (Research Findings)

- `코드 확인` — implementation Step 1 path 6이 feature-draft Part 2를 plan으로 직접 파싱. path B(no-plan 경량 분해)가 이 설계에서 정식 ordering 단계로 승격됨.
- `코드 확인` — implementation Step 6/7이 phase별·cross-phase review-fix gate를 자체 소유(plan 출처 무관).
- `코드 확인` — autopilot planning precedence(line 162) + orchestrator-contract §8이 implementation-plan을 multi-phase 전용 Checkpoint 계약 생산자로 규정. 이 계약이 D7 재배선의 개편 대상.
- `코드 확인` — feature-draft-agent ↔ implementation-plan-agent near-duplicate. D2+D4로 역할이 "task 정의 vs task 정렬"로 갈리며 이 중복 smell이 해소됨(부수 효과).

## 토론 흐름 (Discussion Flow)

- Round 1: "implementation-plan 안 씀" 문제 제기 → 코드 근거로 진단(path 6 직접 파싱 + 리뷰 자체 소유) → 3안 제시(통합/현상유지/축소 재정의).
- Round 2: 사용자 원안 제시(ordering을 implementation-plan-agent로, feature-draft에서 제거) → AI가 Part 2 통째 이동으로 오해, "plan-review-agent 은퇴" 파급까지 전개.
- Round 3: "아냐 그거 아냐" → AI 해석 철회, 어긋난 지점 확인.
- Round 4: "Part 2는 feature-draft가 소유, 그 중 dependency 계산해서 task ordering 하는 부분만 뺀다"로 정확화.
- Round 5: late-binding 근거를 전체 조망 vs 코드베이스 실측으로 분기 → "전체 조망이 핵심" 확정 → ordering=경량 계산 단계.
- Round 6: 항상 경유 확정 + skill 제거 + 하위호환 mirror 결정 → AI가 이름 충돌 지적 → 옵션 A(유지)/B(분리) 제시.
- Round 7: 옵션 B 확정. 이어 discussion 문서화 지시.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: implementation-plan 스킬 얘기해 보자. 요새 거의 안 쓴다. feature-draft → implementation 직행하게 된다.
**A**: 코드 확인 결과 안 쓰이는 게 아키텍처로 확증(path 6 + 리뷰 자체 소유). 유일 잔여 니치는 autopilot multi-phase Checkpoint + spec-first 예외. near-duplicate producer smell 지적. 3안(통합/현상유지/축소) 제시.
**Follow-up**: autopilot multi-phase 실제 사용 여부 질문.

### Round 2
**Q**: implementation-plan-agent에 feature-draft의 task planning을 주고, feature-draft에서 빼자. implementation/autopilot이 구현 직전 호출. 이유: (1) task planning은 plan-review loop 불필요 (2) feature-draft 빨라짐 (3) 규모 보고 multi/single 유연 결정.
**A**: (오해) Part 2 통째 이동으로 해석 → plan-review loop가 양쪽에서 빠져 plan-review-agent가 고아 됨을 전개. 대화 맥락 전달 리스크 제기.
**Follow-up**: plan-review-agent 은퇴 확정 여부 등 결정점 질문.

### Round 3
**Q**: 아냐 그거 아냐.
**A**: 해석 철회. 어디가 어긋났는지 확인 요청(feature-draft 잔여물 / plan-review loop 범위).

### Round 4
**Q**: Part 2는 feature-draft가 가져가되, 그 중 task들 dependency 계산해서 task ordering 하는 부분만 뺀다.
**A**: 정확히 재잡음. plan-review-agent 살아있음(고아 안 됨). ordering=결정론적 파생이라 loop 불필요. late-binding 근거가 (1)전체 조망 (2)코드베이스 실측 중 뭔지 질문.

### Round 5
**Q**: 1번 전체 조망이 핵심.
**A**: implementation-plan-agent=경량 ordering 계산기로 확정. near-duplicate smell 자동 해소. 결정점 정리(Part 2 잔여물 / 항상 경유 / Checkpoint 소유 / skill 운명).

### Round 6
**Q**: 항상 경유. skill 제거 맞지만 하위호환 위해 feature-draft mirror로 남기자.
**A**: 이름 충돌 지적(같은 implementation-plan 아래 agent=ordering, skill=mirror가 정반대). 옵션 A(유지+충돌 감수) / B(이름 분리, 새 역할=task-ordering-agent) 제시, B 추천.

### Round 7
**Q**: B로 가자. → 이어서: discussion 관례에 따라 문서 남기자.
**A**: 옵션 B 확정, 합의 설계 6항 정리. 진행 방식(도그푸딩 vs 직접) 질문 후 본 문서 작성.
