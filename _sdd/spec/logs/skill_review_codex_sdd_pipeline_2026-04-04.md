# Skill Review: Codex SDD Pipeline

**Review Date**: 2026-04-04
**Scope**: `.codex/skills/` 전체 SDD 체인 사용자 관점 리뷰
**Reviewer**: Codex (사용자 요청에 의한 비판적 리뷰)
**Context**: thin global spec model 정렬 이후, Codex skill set이 실제로 원하는 SDD를 잘 실현하고 좋은 품질의 코드/문서를 만들 수 있는지 점검

---

## 요약

큰 구조는 강하다. `sdd-autopilot`의 gate, `feature-draft -> implementation-plan -> implementation -> implementation-review -> spec-update-*`의 artifact contract, thin global spec과 temporary spec의 분리는 현재 방향과 잘 맞는다.

이후 patch를 적용하면서, 초기 리뷰 5개와 Claude Code 교차 검토로 추가된 5개 중 대부분을 Codex skill/agent surface에 반영했다. manual sync 운영 자체는 유지됐고, runtime smoke test는 아직 남아 있지만, 문서 계약 관점의 주요 갭은 한 차례 정리된 상태다.

- path contract와 실제 `_sdd/` 파일 구조의 불일치
- `sdd-autopilot`의 top-level entrypoint 한계
- best-effort default가 강해 생기는 plausible artifact 위험
- `implementation-review`의 한국어 강제
- skill/agent mirror 유지가 수동 복제 전제라는 점
- thin global spec 이후 `feature-draft`의 code exploration gate 부재
- `feature-draft` Part 2와 `implementation-plan`의 경계 불명확
- 소규모 작업에도 동일 강도로 요구되는 CIV ceremony
- `feature-draft`와 `implementation` 사이의 Target Files semantics 불일치
- `truly repo-wide` 판단 기준의 추상성

즉, 설계 방향은 맞고, 이번 patch로 top-level contract도 한 단계 정리됐다. 남은 과제는 운영 내구성 자체보다 patch가 실제 실행 흐름에서 기대대로 작동하는지 smoke check하는 일에 가깝다.

---

## Strengths

### 1. SDD 핵심 구조는 잘 잡혀 있다

- global spec을 장기 SoT, temporary spec을 실행 청사진으로 분리하는 모델이 skill 전반에 반영되어 있다.
- `feature-draft`는 temporary spec 7섹션과 implementation input을 한 번에 만들도록 설계되어 있다.
- `implementation-plan`과 `implementation`은 `Target Files`, dependency, validation linkage를 중심으로 연결된다.

### 2. 검증 강도가 약하지 않다

- `sdd-autopilot`은 Execute -> Verify, review-fix loop, explicit approval, pre-flight check를 강하게 요구한다.
- `implementation`과 `implementation-review`는 fresh verification을 강제하고, "should work" 류의 종료를 허용하지 않는다.

### 3. thin global model은 대체로 일관되게 반영됐다

- `spec-create`, `spec-summary`, `spec-review`, `spec-update-*`가 global spec을 `개념 + 경계 + 결정` 중심으로 다루도록 정리되어 있다.
- 이전처럼 global spec을 feature-level usage/reference/inventory로 되돌리려는 압력은 줄어들었다.

---

## Findings

### 1. [High] Path contract가 실제 워크스페이스와 어긋난다

**심각도**: High  
**영향**: portability / reproducibility / case-sensitive 환경 안정성

여러 skill이 `_sdd/spec/decision_log.md`, `_sdd/implementation/implementation_plan.md` 같은 lowercase 경로를 canonical처럼 사용한다. 하지만 현재 실제 파일 구조는 `DECISION_LOG.md`, `IMPLEMENTATION_PLAN.md`를 포함한다.

예시:
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/spec-update-todo/SKILL.md`
- `.codex/skills/spec-update-done/SKILL.md`
- `.codex/skills/spec-snapshot/SKILL.md`

실제 파일:
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/implementation/IMPLEMENTATION_PLAN.md`

반면 uppercase fallback을 명시적으로 다루는 것은 사실상 `implementation` 계열뿐이다. macOS 기본 파일시스템에서는 넘어갈 수 있지만, case-sensitive 환경이나 다른 머신에서는 실제 실패 지점이 된다.

**리스크**:
- skillchain 중 일부만 artifact를 찾는다
- 환경에 따라 동일 요청의 성공/실패가 달라진다
- "canonical path"라는 말이 surface마다 다르게 해석된다

**권장**:
1. `_sdd/` canonical path를 lowercase로 확정할지, uppercase legacy를 계속 허용할지 먼저 결정
2. 결정 후 전체 skillchain에서 같은 fallback 규칙을 적용
3. 경로 drift를 검사하는 lightweight audit을 추가

---

### 2. [High] `sdd-autopilot`은 아직 universal top-level entrypoint가 아니다

**심각도**: High  
**영향**: 사용자 기대와 실제 동작의 불일치

`sdd-autopilot`은 설명상 "요구사항 분석부터 스펙 동기화까지 end-to-end"를 약속한다. 하지만 Step 0에서 `_sdd/spec/*.md`가 없으면 `/spec-create`를 안내하고 종료한다.

이 말은 실제로는:
- spec이 이미 있는 repo에서는 강한 메타 진입점
- spec이 없는 repo에서는 진입점이 아니라 router

라는 뜻이다.

**리스크**:
- 사용자는 "일단 `/sdd-autopilot`부터"를 기대하는데 실제로는 중간에서 멈춘다
- greenfield / low-doc repo에서 가장 필요한 순간에 최상위 진입점이 비활성화된다

**권장**:
1. `sdd-autopilot`을 truly universal entrypoint로 만들고, spec 부재 시 내부적으로 `spec-create`를 선행 호출
2. 혹은 현재 동작을 유지하되 설명/acceptance criteria에서 "spec이 준비된 repo용"임을 명시

---

### 3. [Medium] best-effort default가 너무 강해서 plausible artifact를 만들 위험이 있다

**심각도**: Medium  
**영향**: temporary spec / plan / guide 품질

`feature-draft`, `implementation-plan`, `guide-create`는 공통적으로 정보가 모자라도 멈추지 않고 best-effort로 계속 진행하는 성향이 강하다.

이건 속도를 올리지만, SDD 관점에서는 역효과가 있다. SDD의 핵심은 "그럴듯한 문서"보다 "잘못된 판단을 굳히지 않는 것"이기 때문이다.

특히 아래 상황에서 위험하다.
- domain terminology가 모호한데 draft를 먼저 굳히는 경우
- touchpoint와 target file이 불확실한데 plan을 세우는 경우
- spec 근거가 약한데 guide를 만드는 경우

**리스크**:
- 잘못된 가정이 `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/guides/`에 구조화된 artifact로 고정된다
- 이후 단계가 그 artifact를 "이미 정리된 truth"처럼 소비한다

**권장**:
1. ambiguity threshold를 명시해, 특정 조건 이상이면 질문 1회 추가를 기본값으로 전환
2. low-confidence artifact에는 stronger marker를 남겨 후속 skill이 보수적으로 읽게 함
3. `best-effort`와 `safe-to-assume`를 분리해서 서술

---

### 4. [Medium] `implementation-review`의 한국어 강제가 전체 체인의 언어 정책과 충돌한다

**심각도**: Medium  
**영향**: mixed-language repo / English-first 팀 / 외부 공유

다른 skill들은 대체로 "기존 문서 언어를 따르거나 사용자 언어를 따른다"는 정책인데, `implementation-review`만 리포트와 커뮤니케이션을 한국어로 강제한다.

이건 현재 repo엔 편할 수 있지만, Codex skill set 자체의 재사용성과 일관성 관점에서는 어색하다.

**리스크**:
- 영문 프로젝트에서 review artifact만 별도 번역이 필요해진다
- 사용자 언어와 출력 언어가 어긋나 pipeline UX가 흔들린다

**권장**:
1. "사용자 언어 우선, 기존 리뷰 문서 언어 fallback"으로 정책을 통일
2. 최소한 hard rule에서 한국어 강제를 제거

---

### 5. [Medium] skill/agent mirror 유지 방식이 수동 복제 전제라 drift가 반복될 수 있다

**심각도**: Medium  
**영향**: contract drift / maintenance cost

여러 skill이 자기 본문이 agent `developer_instructions`의 복사본이라고 선언하고, 둘을 반드시 함께 수정하라고 말한다. 하지만 이번 세션에서도 실제로 4개 pair가 드리프트 상태였다가 수동으로 다시 맞췄다.

즉 현재 구조는:
- 설계상 mirror
- 운영상 manual sync

상태다.

**리스크**:
- 다음 canonical model 변경 때 다시 skill과 agent가 어긋난다
- 사용자는 skill을 읽고 기대한 계약과 runtime agent 계약이 달라질 수 있다

**권장**:
1. one-source generation으로 바꾸거나
2. 최소한 pair sync audit을 스크립트/체크리스트로 자동화하거나
3. mirror pair와 wrapper-only skill을 명확히 분리

Claude Code 리뷰에서 제기된 항목 중 아래 두 개는 Codex에 그대로 옮기지 않았다.

- mirror notice의 `.toml`/`.md` 경로 버그는 Claude-only 문제였다.
- `spec-create` template/example 빈약 문제는 Codex 쪽 companion asset이 더 보강되어 있어 동일 finding으로 채택하지 않았다.

---

### 6. [Medium] thin global spec 모델이 `feature-draft`의 code exploration을 hard requirement로 고정하지 않는다

**심각도**: Medium  
**영향**: temporary spec 정확도 / touchpoint 식별 / Target Files 품질

`spec-create`와 현재 global model은 global spec을 `개념 + 경계 + 결정` 중심의 얇은 기준 문서로 정의한다. 이 모델 자체는 맞다. 문제는 이후 `feature-draft`가 temporary spec의 `Touchpoints`와 Part 2의 `Target Files`를 만들 때, 실제 코드 탐색이 사실상 필수인데 그 요구가 hard gate로는 고정되어 있지 않다는 점이다.

현재 `feature-draft`는 Step 2에서 관련 코드/테스트/설정 파일을 읽도록 말하지만, 이것이 thin global model에서 반드시 수행해야 하는 필수 검증 단계인지, 아니면 권장 탐색인지가 모호하다.

**리스크**:
- global spec만 읽고도 draft를 계속 진행해 버릴 수 있다
- `Touchpoints`와 `Target Files`가 코드 현실보다 spec wording에 끌려갈 수 있다
- downstream `implementation`이 실제 실행 시점에 `UNPLANNED_DEPENDENCY`를 더 많이 만나게 된다

**권장**:
1. `feature-draft`에 "global spec이 thin core만 제공하면 Step 2 code exploration은 필수"라는 hard rule 또는 gate를 추가
2. code exploration이 충분히 끝나지 않았으면 `low confidence` marker를 남기도록 강화

---

### 7. [Medium] `feature-draft` Part 2와 `implementation-plan`의 역할 경계가 skill 로컬 계약에 없다

**심각도**: Medium  
**영향**: workflow 선택 일관성 / 중복 작업 / 사용자 혼란

`feature-draft`는 Part 2에서 이미 실행 가능한 구현 계획을 만든다. 동시에 `implementation-plan`은 같은 delta를 더 세분화하는 별도 skill로 남아 있다. `sdd-autopilot`의 reasoning reference에는 큰 흐름이 드러나지만, 정작 사용자가 직접 읽는 skill 로컬 계약에는 "언제 Part 2만으로 충분하고 언제 `implementation-plan`을 한 번 더 써야 하는가"가 분명하지 않다.

**리스크**:
- `/feature-draft` 뒤에 `/implementation-plan`을 항상 한 번 더 돌리는 습관이 생긴다
- 반대로 실제로는 plan이 더 필요한데 Part 2만 보고 곧바로 구현으로 들어갈 수 있다

**권장**:
1. `feature-draft` Integration 섹션에 후속 `implementation-plan` 필요 조건을 명시
2. `implementation-plan`에도 "이미 충분한 Part 2가 있으면 생략 가능" 규칙을 대칭적으로 명시

---

### 8. [Medium] 소규모 작업에 CIV ceremony가 과할 수 있다

**심각도**: Medium  
**영향**: small-task usability / drafting overhead / artifact proportionality

현재 `feature-draft`는 `Contract/Invariant Delta`와 `Validation Plan`의 ID linkage를 항상 요구하고, `implementation-plan`도 같은 linkage를 보존하도록 강제한다. 대규모 기능에서는 강점이지만, 작은 UI 변경이나 로컬 refactor 수준의 작업에도 동일한 형식을 그대로 적용하면 ceremony가 작업 규모를 앞지르기 쉽다.

**리스크**:
- 단순 작업에도 temporary spec이 불필요하게 장황해진다
- 사용자가 SDD 체인을 "사소한 변경에는 너무 무겁다"고 느낄 수 있다

**권장**:
1. small task용 CIV light mode를 정의
2. delta 수가 매우 적고 repo-wide contract 변화가 없을 때는 inline linkage를 허용
3. 다만 validation traceability 자체는 유지

---

### 9. [Medium] `feature-draft`와 `implementation` 사이의 Target Files 계약이 같은 깊이로 정렬되어 있지 않다

**심각도**: Medium  
**영향**: 병렬 계획 품질 / phase 설계 / runtime fallback 빈도

`implementation`은 `Target Files and Conflicts`에서 동일 파일 충돌뿐 아니라 모델/타입 import, DB migration, shared config, API contract 소비, 상수/타입 가정 같은 의미적 충돌까지 본다. 반면 `feature-draft`의 `Target Files Rules`는 파일 겹침이 많으면 phase를 나누라는 수준에 머문다.

즉 draft 단계에서는 병렬 가능해 보이던 plan이 실제 실행 단계에서야 의미적 충돌로 드러날 수 있다.

**리스크**:
- Part 2가 병렬 친화적으로 보이지만 실제로는 순차 fallback이 늘어난다
- phase와 dependency 품질이 execution skill의 conflict model보다 얕다

**권장**:
1. `feature-draft`와 `implementation-plan`에 최소한의 semantic conflict 패턴을 올린다
2. shared model/type, API contract producer-consumer, config coupling은 draft 단계부터 dependency로 명시하게 한다

---

### 10. [Low] `truly repo-wide` 판단 기준이 여전히 추상적이다

**심각도**: Low  
**영향**: global spec 두께 일관성 / skill 간 판단 편차

`spec-create`, `spec-update-todo`, `spec-update-done`은 모두 "repo-wide invariant가 정말 필요할 때만" 또는 "truly repo-wide invariant가 있을 때만" 같은 표현을 사용한다. 방향은 맞지만, 무엇이 여기에 해당하는지 예시와 판정 기준이 부족하다.

**리스크**:
- 어떤 실행에서는 feature-level contract가 global spec으로 올라가고, 어떤 실행에서는 빠진다
- thin global model이 시간이 지나면서 repo나 모델마다 다른 두께로 변형될 수 있다

**권장**:
1. positive example과 negative example을 skill 본문에 직접 추가
2. "코드를 봐도 복구되지 않고, 여러 기능에 공통이며, 틀리면 repo-level 판단이 어긋나는가" 같은 판정 문장을 공통 rule로 고정

---

## Decision Resolution

아래 결정은 review 이후 사용자와 함께 확정한 운영 방향이다. 이 섹션을 기준으로 이후 patch 방향을 정한다.

### 1. `_sdd/` path policy

**Decision**: `lowercase canonical`

- 앞으로 `_sdd/` artifact path는 lowercase를 canonical로 본다.
- 기존 uppercase artifact는 transition 대상으로 보고, 필요한 경우에만 fallback으로 읽는다.
- 즉 path mismatch 문제는 "dual canonical"이 아니라 "lowercase canonical + legacy fallback"으로 정리한다.

### 2. `sdd-autopilot` entrypoint policy

**Decision**: spec-less repo에서도 작동하는 `code-first fallback entrypoint`

- `sdd-autopilot`은 `_sdd/spec/`가 없다고 중단하지 않는다.
- 필요 시 `_sdd/` workspace만 먼저 부트스트랩하고, 코드를 기준으로 draft/plan/implementation/review를 진행할 수 있다.
- 종료 시 또는 적절한 지점에 `spec-create`를 권고한다.
- 즉 `sdd-autopilot`은 spec-ready repo 전용이 아니라, spec-less repo에서도 동작하는 최상위 진입점으로 본다.

### 3. ambiguity policy

**Decision**: `One Extra Question`

- 결과 품질이나 방향을 실질적으로 바꾸는 ambiguity면 질문 1회를 추가한다.
- 그 외 ambiguity는 best-effort로 진행한다.
- 불확실성은 artifact에 남긴다.

### 4. review artifact language policy

**Decision**: `User Language First`

- review artifact는 현재 사용자 언어를 우선한다.
- 사용자 언어 신호가 약하면 기존 review 문서 언어를 fallback으로 사용한다.
- 따라서 `implementation-review`의 한국어 고정 정책은 완화 대상이다.

### 5. skill/agent mirror maintenance policy

**Decision**: `Manual Sync`

- skill/agent mirror는 생성 기반이나 자동 audit 기반으로 바꾸지 않는다.
- mirror pair는 사람이 함께 수정하는 운영 discipline으로 유지한다.
- 다만 이 결정은 drift 비용을 감수하는 선택이며, 이후 canonical model 재변경 시 다시 문제를 부를 수 있다.

---

## Status

| # | 이슈 | 심각도 | 결정 | 반영 상태 |
|---|------|--------|------|----------|
| 1 | `_sdd/` path contract 불일치 | High | lowercase canonical + legacy fallback | Patched on core chain |
| 2 | `sdd-autopilot` universal entrypoint 아님 | High | spec-less에서도 code-first fallback으로 동작 | Fixed |
| 3 | best-effort default 과강 | Medium | 핵심 ambiguity에는 질문 1회 추가 | Fixed |
| 4 | `implementation-review` 한국어 강제 | Medium | user language first | Fixed |
| 5 | skill/agent mirror 수동 유지 | Medium | manual sync 유지 | Decision Closed |
| 6 | thin spec 이후 `feature-draft` code exploration gate 부재 | Medium | code exploration hard gate | Fixed |
| 7 | `feature-draft` vs `implementation-plan` 역할 경계 불명확 | Medium | sufficiency heuristic in local contract | Fixed |
| 8 | 소규모 CIV ceremony 과잉 | Medium | compact CIV guidance | Fixed |
| 9 | `feature-draft` vs `implementation` Target Files semantics 불일치 | Medium | semantic conflict rules promoted upstream | Fixed |
| 10 | `truly repo-wide` 판단 기준 추상성 | Low | shared invariant rubric + examples | Fixed |

---

## 결론

지금 `.codex/skills/`는 "방향은 맞지만 운영 계약이 거칠다"는 초기 상태에서 한 번 더 정리됐다. core chain 기준으로는 path policy, spec-less autopilot, ambiguity rule, language policy, thin-spec handling, Target Files semantics, repo-wide invariant rubric이 문서 계약에 반영됐다.

즉 결론은:

> 방향은 맞고, 이번 patch로 contract layer의 큰 구멍은 대부분 막혔다. 다음 검증 포인트는 문서 내용이 아니라 실제 호출 흐름에서 이 규칙들이 기대대로 작동하는지다.

---

## Recommended Next Actions

1. `feature-draft -> implementation`과 `sdd-autopilot` spec-less mode를 실제로 한 번씩 smoke run 해서 문서 계약이 실행 결과와 맞는지 확인한다.
2. lowercase canonical path 정책이 secondary skill surface에도 충분히 반영됐는지 한 번 더 audit한다.
3. manual sync 유지 결정은 그대로 두되, 다음 skill 개편 때 mirror drift spot check를 다시 수행한다.

---

## Trace

이 review에 대한 후속 결정은 아래 discussion log에도 정리되어 있다.

- `_sdd/discussion/discussion_codex_skill_review_findings_resolution.md`
- `_sdd/spec/logs/skill_review_claude_code_pipeline_2026-04-04.md`
