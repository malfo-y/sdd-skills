# SDD 스펙의 정의

이 문서는 SDD에서 말하는 스펙이 무엇인지, global spec과 temporary spec이 각각 무엇을 담아야 하는지 정의하는 선언 문서다.

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

## 3. Global Spec에 기본으로 넣지 않는 것

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

## 4. Repo-wide invariant를 다루는 방식

repo-wide invariant가 정말 필요하면 global spec에 남긴다. 다만 별도 표 구조를 global 기본 형태로 강제하지 않는다.

권장 방식:

- guardrails 문장으로 흡수한다
- key decisions의 "what must stay true"로 남긴다
- 여러 feature에 공통이 아닌 invariant는 temporary spec 또는 guide로 내린다

판단 기준은 아래와 같다.

> 코드를 봐도 바로 복구되지 않고, 여러 기능에 공통으로 적용되며, 틀리면 repo-level 판단이 어긋나는 것만 global에 남긴다.

## 5. Temporary Spec의 정의

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

## 6. 정보 배치 원칙

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

## 7. 권장 구조

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

## 8. Skill에 주는 의미

- `spec-review`: global spec에서는 최소 코어만 요구한다.
- `spec-summary`: `_sdd/spec/summary.md`를 reader-facing whitepaper로 작성한다. 문제, 배경/동기, 대안 대비 선택 이유, 핵심 설계, 코드 근거, 사용/기대 결과, 추가 읽을 surface를 함께 설명하며, status memo가 아니라 기술 whitepaper처럼 읽혀야 한다. 관련 draft/implementation signal이 있으면 appendix로 짧은 계획/진행 상태를 덧붙일 수 있다.
- `spec-rewrite`: line 수보다 feature-level 오염도를 우선 본다.
- generator/planner/update 계열은 global spec을 더 두껍게 복구하지 않는다.
- guide는 authoritative spec이 아니라 필요 시 만드는 companion surface다.

## 9. 선언

SDD의 global spec은 repo-wide 판단 기준을 고정하는 선언 문서다.

SDD의 temporary spec은 변경 실행을 위한 구체적 청사진이다.

두 문서는 서로를 대체하지 않으며, 지원 정보는 코드, guide, README, reference docs로 분리한다.
