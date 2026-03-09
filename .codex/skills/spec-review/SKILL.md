---
name: spec-review
description: This skill should be used when the user asks to "review spec", "spec drift check", "verify spec accuracy", "audit spec quality", "review spec against code", "refresh spec review", "스펙 리뷰", "스펙 검토", "스펙 드리프트 점검", or wants a review-only analysis of spec quality and code-to-spec alignment without directly editing spec files.
version: 1.2.0
---

# Spec Review

탐색형 스펙 기준으로 스펙 품질과 코드 정합성을 리뷰한다.

이 스킬은 스펙을 수정하지 않는다. 대신 아래를 판단한다.

- 이 스펙이 처음 보는 사람에게 5분 entry point 역할을 하는가
- 기능 변경 시 어디부터 봐야 하는지 알려주는가
- 실제 코드 경로와 컴포넌트 책임이 연결되어 있는가
- 코드와 문서가 drift 되었는가

## Hard Rules

1. `_sdd/spec/` 아래 실제 스펙은 수정하지 않는다.
2. `DECISION_LOG.md`도 직접 수정하지 않는다. 필요하면 제안만 남긴다.
3. 산출물은 `_sdd/spec/SPEC_REVIEW_REPORT.md` 리뷰 리포트다.
4. High / Medium finding에는 가능한 한 `file:line`, 테스트, diff 같은 구체적 근거를 붙인다.
5. 불확실한 내용은 `Open Questions`에 남긴다.
6. `MUST` 섹션과 `OPT` 섹션을 구분해서 평가한다. 선택 섹션 누락만으로 약한 스펙이라고 단정하지 않는다.
7. 리뷰 자체도 token-efficient 해야 하며, 없는 선택 섹션을 억지로 보완 요구하지 않는다.

## Review Dimensions

### 1. Entry Point Quality

- `Goal`이 프로젝트 목적을 빠르게 설명하는가
- `System Boundary`가 명확한가
- 메인 스펙이 너무 장황하지 않은가
- `MUST` 정보만으로도 5분 entry point 역할을 하는가

### 2. Navigation Quality

- `Repository Map`이 있는가
- `Runtime Map`이 있는가
- `Component Index`가 있는가
- 실제 경로와 심볼이 연결되는가

### 3. Changeability

- `Common Change Paths` 또는 동등 정보가 있는가
- 변경 시 같이 봐야 할 테스트/로그/디버깅 포인트가 보이는가
- 컴포넌트 책임과 비책임이 구분되는가

### 4. Drift

- 구현과 문서의 기능 설명이 맞는가
- 새 컴포넌트/경로/흐름이 문서에 빠져 있지 않은가
- 오래된 `Open Questions`가 그대로 남아 있지 않은가
- 결정 맥락이 달라졌는데 `DECISION_LOG.md` 제안이 필요한가

### 5. Decision & Invariant Memory

- Cross-Cutting Invariants 또는 동등한 불변 조건이 보이는가
- 비자명한 설계 결정이 스펙 본문이나 `DECISION_LOG.md`에 기록되어 있는가
- `Open Questions`에 실질적 미결 사항이 정리되어 있는가
- "깨지면 안 되는 가정"을 스펙만 읽고 파악할 수 있는가

## Inputs

- `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`
- 링크된 컴포넌트 스펙
- `_sdd/spec/DECISION_LOG.md` (있으면)
- `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- 최근 코드 상태 (`git diff`, 현재 워크트리)
- `_sdd/env.md` (로컬 검증 시)

## Process

### Step 1: Scope selection

1. 메인 스펙 식별
2. 링크된 컴포넌트 스펙 식별
3. 생성물/백업 파일 제외
4. 필요 시 `DECISION_LOG.md` 로드
5. review scope를 `Spec-only` 또는 `Spec+Code`로 명시

### Step 2: Audit the spec as a navigation surface

아래를 우선 본다.

- `Project Snapshot` 또는 동등 요약
- `System Boundary`
- `Repository Map`
- `Runtime Map`
- `Component Index`
- `Common Change Paths`
- `Open Questions`

판정 규칙:

- `Project Snapshot`, `System Boundary`, `Repository Map`, `Runtime Map`, `Component Index`, `Open Questions`는 핵심 축으로 본다.
- `Environment & Dependencies`, `Usage Examples`, `Identified Issues & Improvements`는 프로젝트 규모와 도메인에 따라 optional일 수 있다.
- optional 섹션이 비어 있거나 없더라도, 메인 탐색성과 변경 지원이 충분하면 finding으로 올리지 않는다.

### Step 3: Audit changeability

기능을 하나 바꾸려는 사람이 이 문서만 보고 시작점을 찾을 수 있는지 본다.

예시 질문:

- 새 API 필드 추가 시 어디를 먼저 봐야 하는가
- 권한 정책 변경 시 어디를 봐야 하는가
- 배치/이벤트 흐름 문제를 디버깅할 때 어디를 봐야 하는가

### Step 4: Audit code-linked drift

아래 drift를 찾는다.

- 새 컴포넌트가 구현에만 존재
- 런타임 흐름이 바뀌었는데 `Runtime Map`이 낡음
- 소유 경로가 달라졌는데 `Component Index`가 낡음
- 운영/디버깅 경로가 바뀌었는데 `Common Change Paths`가 없음
- 이미 해결된 질문이 `Open Questions`에 남아 있거나, 새 질문이 문서에 없음

### Step 5: Classify findings

| Severity | 의미 |
|----------|------|
| High | 잘못된 계약, 중요한 drift, 탐색 실패로 잘못 수정될 위험 |
| Medium | 누락/모호함, 자기검증 기준 부족으로 작업 효율이 떨어짐 |
| Low | 링크 위생, 표현 문제, 비핵심 개선 |

각 review dimension을 아래 probe로 `PASS` / `WEAK` / `FAIL` 판정한다.

| Dimension | Probe |
|-----------|-------|
| Entry Point Quality | "이 저장소는 무엇을 하는가?" |
| Navigation Quality | "기능 X는 어디에 있는가?" |
| Changeability | "변경 Y는 어디서 시작해야 하는가?" |
| Drift | "스펙과 코드가 현재도 일치하는가?" |
| Decision & Invariant Memory | "왜 Z를 선택했고 무엇을 깨면 안 되는가?" |

결론은 하나를 고른다.

- `SPEC_OK`
- `SYNC_REQUIRED`
- `NEEDS_DISCUSSION`

### Step 6: Write report

리포트에는 아래가 있어야 한다.

1. Executive Summary
2. Findings by Severity
3. Dimension Verdicts (`PASS` / `WEAK` / `FAIL` + 근거)
4. Entry Point / Navigation Notes
5. Changeability Notes
6. Spec-to-Code Drift Notes
7. Open Questions
8. Suggested Next Actions
9. `DECISION_LOG.md` proposal (필요 시)
10. LLM Efficiency Notes

`SYNC_REQUIRED`인 경우에는 바로 적용 가능한 spec update checklist를 함께 제시한다.

기존 리포트가 있으면 `_sdd/spec/prev/PREV_SPEC_REVIEW_REPORT_<timestamp>.md`로 백업한다.

## References

- 체크리스트: [`references/review-checklist.md`](references/review-checklist.md)
- 예시: [`examples/spec-review-report.md`](examples/spec-review-report.md)
