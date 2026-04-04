# SDD Global Spec Template (Full)

# <Project Name>

> One-line description

**Version**: X.Y.Z
**Last Updated**: YYYY-MM-DD
**Status**: Draft | In Review | Approved | Deprecated

## 1. 배경 및 high-level concept

<!-- 이 프로젝트가 해결하는 문제와 핵심 아이디어를 고정한다.
     "무엇을 왜 만드는가"에 답하되, 구현 방법은 적지 않는다. -->

### Problem
- ...

### Why This Matters
<!-- 이 문제를 지금 풀어야 하는 이유. 비즈니스/기술적 동기. -->
- ...

### High-Level Concept
- ...

### Alternatives Considered
<!-- 검토했지만 채택하지 않은 접근과 그 이유. 나중에 같은 대안을 다시 검토하는 것을 방지한다. -->
- ...

## 2. Scope / Non-goals / Guardrails

<!-- 책임 범위의 안쪽과 바깥쪽을 동시에 고정한다.
     Guardrails는 repo 전체가 지켜야 할 운영 규칙이다.
     feature별 제약은 여기가 아니라 temporary spec에서 다룬다. -->

### In Scope
- ...

### Non-goals
<!-- "하지 않기로 한 것"을 명시해야 scope creep을 막는다. -->
- ...

### Guardrails
<!-- 전체 repo에 적용되는 운영 원칙. 예: "직접 DB 접근 금지, 반드시 API 경유" -->
- ...

## 3. 핵심 설계와 주요 결정

<!-- 이 프로젝트의 장기 설계 판단과 그 이유를 적는다.
     구현 방법(how)이 아니라 설계 판단(why)을 고정하는 게 목적이다.
     대안 대비 왜 이 방식을 택했는지를 한 줄이라도 남겨야 나중에 재논의를 방지한다.
     feature-level 결정은 temporary spec에서 다룬다. -->

### Core Design
- ...

### Key Decisions
<!-- 형식: "결정 — 이유". 이유 없는 결정은 나중에 반드시 재논의된다. -->
- ...

## Optional Supporting Notes

<!-- 아래 섹션들은 정말 필요할 때만 추가한다. 없어도 defect가 아니다. -->

### Repo-wide Invariant Note
<!-- 모든 모듈/feature가 지켜야 하는 규칙이 있을 때만 적는다.
     한 컴포넌트의 내부 규칙은 여기가 아니다. -->
- only if truly global

### Feature-Level Guide
<!-- 특정 기능의 사용법, 구조, 리뷰 가이드가 필요하면 `/guide-create`로 생성할 수 있다. -->

### Supporting References
<!-- 관련 docs, README, guide, external resource 링크. -->
- ...

### Appendix-Level Code Map
<!-- entrypoint, invariant hotspot, extension point 등 navigation hint.
     구현 파일 전수 목록이 아니라, 코드를 처음 보는 사람이 어디서 시작할지 안내하는 용도. -->
- only if manual navigation hints are genuinely useful
