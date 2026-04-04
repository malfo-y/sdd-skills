# SDD Global Spec Template (Compact)

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

### High-Level Concept
- ...

## 2. Scope / Non-goals / Guardrails

<!-- 책임 범위의 안쪽과 바깥쪽을 동시에 고정한다.
     Guardrails는 repo 전체가 지켜야 할 운영 규칙이다.
     feature별 제약은 여기가 아니라 temporary spec에서 다룬다. -->

### In Scope
- ...

### Non-goals
- ...

### Guardrails
- ...

## 3. 핵심 설계와 주요 결정

<!-- 이 프로젝트의 장기 설계 판단과 그 이유를 적는다.
     구현 방법(how)이 아니라 설계 판단(why)을 고정하는 게 목적이다.
     대안 대비 왜 이 방식을 택했는지를 한 줄이라도 남겨야 나중에 재논의를 방지한다.
     feature-level 결정은 temporary spec에서 다룬다. -->

### Core Design
- ...

### Key Decisions
- ...

## Optional Supporting Notes

<!-- 아래 섹션들은 정말 필요할 때만 추가한다. 없어도 defect가 아니다. -->

### Repo-wide Invariant Note
<!-- 모든 모듈/feature가 지켜야 하는 규칙이 있을 때만 적는다.
     한 컴포넌트의 내부 규칙은 여기가 아니다. -->
- only if truly global

### Feature-Level Guide
- 특정 기능의 사용법, 구조, 리뷰 가이드가 필요하면 `/guide-create`로 생성할 수 있다.

### Reference Links
- ...
