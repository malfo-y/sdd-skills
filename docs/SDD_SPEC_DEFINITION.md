# SDD 스펙의 정의

이 문서는 SDD에서 말하는 스펙이 무엇인지, global spec과 temporary spec이 각각 무엇을 담아야 하는지, 그리고 spec lifecycle 스킬들이 어떤 공통 기준선을 공유해야 하는지 정의하는 선언 문서다.

관련 문서:
- [SDD_CONCEPT.md](SDD_CONCEPT.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
- [SDD_QUICK_START.md](SDD_QUICK_START.md)
- [sdd.md](sdd.md)

---

## 1. 스펙이란 무엇인가

SDD에서 스펙은 코드와 사람과 에이전트가 같은 판단 기준을 공유하게 만드는 문서다.

스펙은 다음 질문에 답해야 한다.

- 이 프로젝트나 변경은 무엇을 해결하는가
- 어디까지를 책임지는가
- 무엇은 의도적으로 하지 않는가
- 어떤 판단은 이후에도 유지되어야 하는가

즉 스펙은 설명서의 총합이 아니라, 판단 기준을 고정하는 문서다.

## 2. Global Spec의 정의

global spec은 repo-wide Single Source of Truth다. 역할은 장기적으로 유지되어야 할 개념, 경계, 결정을 고정하는 것이다.

global spec의 mandatory core는 아래 세 가지다.

1. 배경 및 high-level concept
2. Scope / Non-goals / Guardrails
3. 핵심 설계와 주요 결정

### A. 배경 및 high-level concept

- 무엇을 해결하는가
- 왜 이 접근을 택하는가
- 이 repo를 어떤 관점으로 읽어야 하는가

### B. Scope / Non-goals / Guardrails

- 책임 범위
- 의도적으로 하지 않는 것
- repo-wide operating rule
- 여러 기능에 공통으로 적용되는 경계

### C. 핵심 설계와 주요 결정

- 유지해야 할 구조적 판단
- 바꾸면 repo-level drift가 생기는 결정
- extension 방향을 제한하는 선택

## 3. 공통 코어 체크리스트 4축

spec lifecycle 스킬은 모두 아래 4축을 공통 코어 checklist로 공유한다. 이 4축의 source-of-truth는 이 문서다.

1. `Thinness`
2. `Decision-bearing truth`
3. `Anti-duplication`
4. `Navigation + surface fit`

각 축의 의미는 아래와 같다.

### A. Thinness

- global spec은 repo-wide 판단에 필요한 최소 코어만 유지한다.
- temporary spec은 이번 변경 실행에 필요한 delta만 유지한다.
- 다른 surface에 있어야 할 detail로 본문을 불필요하게 두껍게 만들지 않는다.

### B. Decision-bearing truth

- 틀리면 repo-level 또는 change-level 판단이 달라지는 정보만 본문에 남긴다.
- code-obvious inventory나 단순 참고 정보는 판단을 바꾸지 않으면 본문 필수 진실이 아니다.
- 스펙 문장은 "왜 이 문장이 여기에 있어야 하는가"에 답할 수 있어야 한다.

### C. Anti-duplication

- 코드, README, guide, supporting docs, temporary spec과 중복되는 내용을 무의미하게 다시 싣지 않는다.
- 중복이 필요하다면 판단 기준을 고정하는 최소 요약만 남긴다.
- 같은 truth가 여러 surface에 퍼져 drift를 유발하지 않게 한다.

### D. Navigation + surface fit

- 정보는 가장 맞는 surface에 둔다.
- global spec, temporary spec, guide, summary, supporting docs, code/test 중 어디에 둘지 먼저 판단한다.
- reader와 agent가 다음 탐색 위치를 자연스럽게 찾을 수 있어야 한다.

## 4. Global Spec에 기본으로 넣지 않는 것

아래 항목은 존재할 수는 있지만 global mandatory core는 아니다.

- usage/expected-results section
- 참조 정보
- manual code-map appendix
- standalone contract/invariant/verification table
- feature-level contract, validation, expected result
- 코드에서 바로 복구 가능한 상세 inventory

이 정보는 성격에 맞는 surface로 내려야 한다.

- feature 변경 실행: temporary spec
- 구현/검토 보조: on-demand guide
- 설치법/참조 정보: README 또는 별도 docs
- 실제 동작/세부 구조: code + test + targeted review

## 5. Repo-wide invariant를 다루는 방식

repo-wide invariant가 정말 필요하면 global spec에 남긴다. 다만 별도 표 구조를 global 기본 형태로 강제하지 않는다.

권장 방식:

- guardrails 문장으로 흡수한다
- key decisions의 "what must stay true"로 남긴다
- 여러 feature에 공통이 아닌 invariant는 temporary spec 또는 guide로 내린다

판단 기준은 아래와 같다.

> 코드를 봐도 바로 복구되지 않고, 여러 기능에 공통으로 적용되며, 틀리면 repo-level 판단이 어긋나는 것만 global에 남긴다.

## 6. Temporary Spec의 정의

temporary spec은 global spec의 축약본이 아니라 변경 실행 청사진이다.

feature-level contract, validation, touchpoint, task sequencing은 여기에 둔다.

canonical 7섹션:

1. `Change Summary`
2. `Scope Delta`
3. `Contract/Invariant Delta`
4. `Touchpoints`
5. `Implementation Plan`
6. `Validation Plan`
7. `Risks / Open Questions`

temporary spec의 목적은 이번 변경이 무엇을 바꾸고, 어디를 건드리며, 무엇으로 검증할지를 직접 다루는 것이다.

## 7. 정보 배치 원칙

| 정보 유형 | 기본 위치 | 이유 |
|-----------|-----------|------|
| 프로젝트 문제와 framing | global spec | repo-wide 판단 기준 |
| scope / non-goals / guardrails | global spec | 공통 경계 고정 |
| 핵심 설계와 주요 결정 | global spec | 장기 의도 보존 |
| reader-facing 문제/동기/설계/사용 서사 | `spec-summary`가 만드는 `_sdd/spec/summary.md` | global spec과 코드를 바탕으로 사람이 읽는 whitepaper surface |
| feature-level contract / validation | temporary spec | 변경 청사진 |
| 사용 예시 / 기대 결과 | guide, README, temporary spec | feature 또는 user-facing 문맥 |
| 데이터 모델 / API / 환경 상세 | README 또는 참조 docs | 지원 정보 |
| code map / inventory | appendix 또는 code | on-demand 탐색 정보 |

## 8. AC / Final Check 매핑 규칙

공통 코어 4축은 spec lifecycle 스킬의 Acceptance Criteria와 Final Check에 흡수되어야 한다. 별도 `Shared Core Checklist` 블록을 재사용하도록 강제하지 않는다.

매핑 원칙:

- `Thinness`: 잘못된 surface inflation을 막는 검사 문구로 반영한다.
- `Decision-bearing truth`: 판단을 바꾸는 진술만 남기고, 약한 진술이나 code-obvious detail을 걸러내는 문구로 반영한다.
- `Anti-duplication`: code, guide, README, supporting docs, temporary spec과의 중복을 줄이는 문구로 반영한다.
- `Navigation + surface fit`: 정보를 맞는 surface로 보내고 링크/경로/배치를 점검하는 문구로 반영한다.

운용 원칙:

- 각 스킬은 위 4축을 자기 AC와 Final Check에서 self-contained하게 읽히도록 표현한다.
- 공통 코어 4축 외에 스킬별 1차 추가 축을 둘 수 있다.
- 1차 추가 축은 공통 코어를 대체하지 않고, 해당 스킬의 역할을 더 선명하게 만드는 용도로만 쓴다.

현재 1차 추가 축:

- `spec-create`: structure rationale + `single-file default`
- `spec-review`: rubric separation + evidence strictness
- `spec-rewrite`: rationale preservation + body/log placement
- `spec-upgrade`: rewrite boundary judgment

## 9. 권장 구조

### Global Spec

```markdown
# Project Global Spec

## 1. Background and High-Level Concept
## 2. Scope / Non-goals / Guardrails
## 3. Core Design and Key Decisions

## Optional Appendix or Supporting Docs
- reference notes
- code map
- guide links
```

### Temporary Spec

```markdown
# Feature Temporary Spec

## 1. Change Summary
## 2. Scope Delta
## 3. Contract/Invariant Delta
## 4. Touchpoints
## 5. Implementation Plan
## 6. Validation Plan
## 7. Risks / Open Questions
```

## 10. Skill에 주는 의미

- `spec-create`: 공통 코어 4축을 만족하는 얇은 global spec을 만든다. 기본값은 `_sdd/spec/main.md` 단일 파일이고, 분할은 navigation + surface fit 근거가 있을 때만 허용한다.
- `spec-review`: spec type에 맞는 rubric을 구분 적용한다. global spec의 feature-level 오염은 기본적으로 `Quality`이며, 문서 타입 혼동이나 잘못된 repo-wide truth처럼 판단을 직접 오도할 때만 `Critical`로 올린다. 모든 finding은 spec/code/doc evidence를 가져야 하고, 근거가 약하면 `UNTESTED`로 남긴다.
- `spec-summary`: `_sdd/spec/summary.md`를 reader-facing whitepaper로 작성한다. 문제, 배경/동기, 대안 대비 선택 이유, 핵심 설계, 코드 근거, 사용/기대 결과, 추가 읽을 surface를 함께 설명하며, status memo가 아니라 기술 whitepaper처럼 읽혀야 한다. 관련 draft/implementation signal이 있으면 appendix로 짧은 계획/진행 상태를 덧붙일 수 있다.
- `spec-rewrite`: 공통 코어 4축을 더 잘 드러내도록 구조를 재정리한다. pruning 과정에서 rationale, citation, code excerpt header를 잃지 않고, migration history나 실행 로그성 설명은 body 대신 `decision_log` 또는 rewrite report로 내린다.
- `spec-upgrade`: legacy spec을 current model로 마이그레이션한다. 다만 구조 재설계, 대규모 재분할, 역할 재배치가 핵심이면 upgrade로 덮지 않고 `spec-rewrite`로 분기한다.
- generator/planner/update 계열은 global spec을 더 두껍게 복구하지 않는다.
- guide는 authoritative spec이 아니라 필요 시 만드는 companion surface다.

## 11. 선언

SDD의 global spec은 repo-wide 판단 기준을 고정하는 선언 문서다.

SDD의 temporary spec은 변경 실행을 위한 구체적 청사진이다.

두 문서는 서로를 대체하지 않으며, 지원 정보는 코드, guide, README, reference docs로 분리한다.
