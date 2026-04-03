---
name: spec-review
description: This skill should be used when the user asks to "review spec", "spec drift check", "verify spec accuracy", "audit spec quality", "review spec against code", "refresh spec review", "스펙 리뷰", "스펙 검토", "스펙 드리프트 점검", or wants a review-only analysis of spec quality and code-to-spec alignment without directly editing spec files.
version: 2.1.0
---

# Spec Review

| Workflow | Position | When |
|----------|----------|------|
| Large | Optional audit | 구현 전/후 스펙 품질 점검 |
| Medium | Optional audit | spec drift 확인 |
| Any | Standalone | strict review-only 검토 |

이 agent는 global spec 또는 temporary spec의 품질과 코드-스펙 정합성을 **review-only**로 감사하고 `_sdd/spec/logs/spec_review_report.md`를 생성한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] spec type을 식별하고 global/temporary rubric을 구분 적용한다.
- [ ] spec-only quality review와 code-linked drift review를 모두 수행한다.
- [ ] findings를 severity 순으로 정리하고 next action을 제시한다.
- [ ] `_sdd/spec/*.md`와 `decision_log.md`는 수정하지 않는다.

## Hard Rules

1. 이 agent는 리뷰와 리포트 생성만 수행한다.
2. `_sdd/spec/*.md`와 `decision_log.md`는 생성/수정/삭제하지 않는다.
3. findings는 `Critical`, `Quality`, `Improvements` 순으로 정리한다.
4. 근거 없는 추정은 사실처럼 쓰지 않는다. 검증되지 않은 항목은 `UNTESTED`로 둔다.
5. 구현과 spec이 불일치하면 drift를 기록하고 후속 스킬만 제안한다.
6. 리포트는 lowercase canonical 경로에 저장한다. transition 기간에는 implementation artifact를 lowercase 우선, legacy uppercase fallback으로 읽는다.

## Review Dimensions

### Global Spec Quality

- `배경 및 high-level concept`가 문제와 framing을 분명히 고정하는가
- `Scope / Non-goals / Guardrails`가 책임 범위와 out-of-scope를 명시하는가
- `핵심 설계와 주요 결정`이 decision-bearing structure를 유지하는가
- `Contract / Invariants / Verifiability`가 명시적이며 추적 가능한가
- `Decision-bearing structure`가 시스템 경계, ownership, cross-component contract, extension point, invariant hotspot을 담는가
- `Strategic Code Map`이 appendix-level manual curated hint로 유지되는가

### Temporary Spec Quality

- `Change Summary`가 변경의 목적과 범위를 요약하는가
- `Scope Delta`가 global spec 대비 변경 경계를 분명히 하는가
- `Contract/Invariant Delta`가 `C*` / `I*` ID를 사용해 delta를 명시하는가
- `Touchpoints`가 실제 변경 지점을 전략적으로 식별하는가
- `Implementation Plan`이 delta를 실행 가능한 작업으로 연결하는가
- `Validation Plan`이 delta ID를 `V*` 검증 항목에 연결하는가
- `Risks / Open Questions`가 미해결 가정과 위험을 숨기지 않는가

### Code-Linked Drift

- 구현/테스트/실행 흐름이 spec과 맞는가
- implementation artifact와 spec의 계약이 맞는가
- outdated section, stale example, broken path/reference가 남아 있지 않은가
- global spec에는 지속 정보만, temporary spec에는 실행 정보가 남아 있는가

## Process

### Step 1: Scope and Spec Type Selection

다음 입력을 찾는다.

- 사용자 지정 경로
- `_sdd/spec/*.md`
- `_sdd/drafts/*.md`
- 관련 구현 파일 / 테스트 / `_sdd/implementation/*`

spec type 판별 규칙:

- global spec: canonical global 섹션(`Scope / Non-goals / Guardrails`, `Contract / Invariants / Verifiability`)이 중심
- temporary spec: canonical 7섹션(`Change Summary`, `Scope Delta`, `Contract/Invariant Delta`, `Touchpoints`, `Implementation Plan`, `Validation Plan`, `Risks / Open Questions`)이 중심
- 혼합/애매한 문서는 가장 지배적인 구조로 판정하고 근거를 리포트에 적는다

### Step 2: Spec Quality Audit

스펙만 보고 품질을 평가한다.

- 용어 정의와 경계가 명확한가
- 필수 canonical section이 빠지지 않았는가
- CIV 또는 delta/validation linkage가 추적 가능한가
- 구조가 현재 canonical model과 맞는가
- 과도한 implementation inventory가 본문을 오염시키지 않는가

### Step 3: Code Drift Audit

코드/테스트/구현 문서와 대조한다.

- 실제 구현된 기능과 spec 주장 비교
- implementation 문서와의 정합성 비교
- delta ID와 validation evidence의 연결 확인
- strategic code map이나 reference path가 실제 코드와 맞는지 확인

상태 예시:

- `ALIGNED`
- `DRIFT`
- `MISSING`
- `UNTESTED`

### Step 3.5: Code Analysis Metrics

`Bash`, `Grep`, `Glob`으로 세 가지 지표를 수집한다.

| Metric | Method | Use |
|--------|--------|-----|
| Hotspots | `git log --format='' --name-only \| sort \| uniq -c \| sort -rn \| head -20` | 자주 변경되는 파일 식별 |
| Focus Score | 변경 파일 중 스펙 관련 컴포넌트 비율 | 변경 집중도 평가 |
| Test Coverage | 스펙 기능별 관련 테스트 파일 존재 여부 | 테스트 갭 식별 |

### Step 4: Severity and Decision

severity 규칙:

- `Critical`: 핵심 contract/invariant 오류, 심각한 drift, 잘못된 보안/동작 서술, global/temporary 구조 혼동
- `Quality`: 누락 설명, 약한 검증 링크, 구조 문제, 중간 수준 drift
- `Improvements`: 가독성, 정리, appendix 수준 개선

decision 예시:

- `SPEC_OK`
- `SYNC_REQUIRED`
- `NEEDS_DISCUSSION`

### Step 5: Report and Handoff

리포트를 `_sdd/spec/logs/spec_review_report.md`에 저장한다.

리포트에는 다음을 포함한다.

- findings
- spec type과 적용 rubric
- spec quality summary
- drift summary
- code analysis metrics
- next actions

후속 스킬 연결:

- 계획 변경 전 반영: `spec-update-todo`
- 구현 완료 후 동기화: `spec-update-done`
- 구현 검증: `implementation-review`

## Output Format

```markdown
# Spec Review Report

**Review Date**: YYYY-MM-DD
**Reviewed Spec**: ...
**Spec Type**: Global | Temporary | Mixed
**Decision**: SPEC_OK | SYNC_REQUIRED | NEEDS_DISCUSSION

## 1. Findings
### Critical
- ...

### Quality
- ...

### Improvements
- ...

## 2. Spec Quality Summary
...

## 3. Drift Summary
...

## 4. Code Analysis Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Top Hotspots | file1 (N), file2 (N) | 자주 변경되는 파일 |
| Focus Score | X% | 스펙 컴포넌트 집중도 |
| Test Coverage | X/Y features covered | 스펙 기능별 테스트 현황 |

## 5. Recommended Next Actions
...
```

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 파일이 적음/없음 | 존재하는 범위만 리뷰하고 한계를 리포트에 적는다 |
| 코드 범위가 너무 큼 | 핵심 모듈 위주로 drift를 점검한다 |
| 기준이 모호함 | `UNTESTED` 또는 `NEEDS_DISCUSSION`으로 남긴다 |
| spec 수정이 필요함 | 수정하지 말고 후속 스킬을 제안한다 |

## Integration

- `spec-update-todo`: 계획 요구사항 반영
- `spec-update-done`: 구현 후 스펙 동기화
- `implementation-review`: 구현 상태 검증과 교차 참조

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.claude/agents/spec-review.md`의 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
