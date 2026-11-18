# Spec Format Reference

`spec-upgrade`가 spec을 고치기 직전에 읽는다. 목표 구조, 구조를 고르는 기준, 예전 내용을 어디로 내리는지를 정한다.

## 목표 구조

global spec의 중심 절은 셋이고 모두 필수다.

| 순서 | 절 | 역할 |
|---|---|---|
| 1 | Background & High-Level Concept | 문제와 저장소를 보는 관점을 고정한다 |
| 2 | Scope / Non-goals / Guardrails | 책임 범위와 공통 경계를 고정한다 |
| 3 | Core Design & Key Decisions | 오래 유지할 판단을 고정한다 |

선택으로 둘 수 있는 것: 참조 정보, guide 링크(기능 가이드는 `guide-create` 스킬로 만든다), 짧은 `Strategic Code Map` 또는 보조 문서 링크. 저장소 전체 불변 규칙은 Guardrails나 Key Decisions 안에 쓴다.

## Skeleton

아래 둘 중 하나를 고르고, 고른 skeleton의 제목과 순서를 그대로 쓴다. 제목은 기존 spec의 언어에 맞춰 번역할 수 있다. 근거가 없는 선택 블록은 지운다.

**Compact** — 기본값.

```markdown
## 1. Background and High-Level Concept
## 2. Scope / Non-goals / Guardrails
## 3. Core Design and Key Decisions
```

**Full** — 원본에 프로젝트 동기나 검토한 대안의 근거가 적혀 있고, compact의 세 절 안에 그 근거를 뜻을 잃지 않고 둘 자리가 없을 때만 고른다.

```markdown
## 1. Background and High-Level Concept
### Problem
### Why This Matters
### High-Level Concept
### Alternatives

## 2. Scope / Non-goals / Guardrails
### In Scope
### Non-goals
### Guardrails

## 3. Core Design and Key Decisions
### Core Design
### Key Decisions

## Optional Supporting Notes
### Repo-wide Invariant Note
### Supporting References
### Feature-Level Guide
### Strategic Code Map (Appendix or Supporting Surface)
```

## 예전 내용을 어디로 내리는가

| 예전 내용 | 새 자리 | 규칙 |
|---|---|---|
| 문제 정의, 비전 | Background & High-Level Concept | global에 남긴다 |
| 범위, 비목표 | Scope / Non-goals / Guardrails | global에 남긴다 |
| 아키텍처 설명과 근거 | Core Design & Key Decisions | 판단을 바꾸는 부분만 남긴다 |
| 독립된 계약·불변식·검증 표 | Guardrails, Key Decisions, 또는 계획 파일 | 저장소 전체 규칙만 global에 남긴다 |
| 사용법 안내 | guide, README | global 본문에 두지 않는다 |
| 기대 결과 | guide, 테스트 | 실행이나 사용자 문맥 가까이에 둔다 |
| 참조 정보 | 보조 문서 | 본문에 두지 않는다 |
| code map | 짧은 appendix 또는 보조 문서 | 탐색에 꼭 필요한 것만 남긴다. 길거나 경로별 설명이 필요하면 보조 문서로 뺀다 |
| 전체 파일 목록, 컴포넌트 카탈로그 | 코드 또는 보조 문서 | global 본문에서 지운다 |
| 이행 이력, 정리한 이유, 실행 로그 | `decision_log.md` | 본문에 두지 않는다 |
| 기능 하나의 실행 상세(작업 분해, 바꾼 파일, 끝나는 조건) | `_sdd/drafts/`의 계획 파일 | global 본문에 두지 않는다 |
