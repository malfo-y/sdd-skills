---
name: spec-review
description: "This skill should be used when the user asks to \"review spec\", \"spec drift check\", \"verify spec accuracy\", \"audit spec quality\", \"review spec against code\", \"refresh spec review\", \"스펙 리뷰\", \"스펙 검토\", \"스펙 드리프트 점검\", or wants a review-only analysis of spec quality and code-to-spec alignment without directly editing spec files."
version: 2.0.0
---

# Spec Review

스펙 품질과 코드-스펙 드리프트를 읽기 전용으로 감사하고, 리뷰 리포트를 생성한다. 스펙 파일은 절대 수정하지 않는다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 2차원 리뷰(spec quality + code drift) 수행 완료
- [ ] AC2: 모든 finding에 severity(High/Medium/Low) 분류 완료
- [ ] AC3: 전체 decision(SPEC_OK / SYNC_REQUIRED / NEEDS_DISCUSSION) 부여
- [ ] AC4: `_sdd/spec/SPEC_REVIEW_REPORT.md`에 리포트 저장
- [ ] AC5: spec 파일(`_sdd/spec/*.md`) 수정 없음 (리포트 파일 제외)

## Hard Rules

- `_sdd/spec/` 하위 파일을 생성·수정·삭제하지 않는다 (SPEC_REVIEW_REPORT.md 제외).
- `DECISION_LOG.md` 변경은 리포트 내 제안으로만 기록한다.
- 추정을 사실처럼 제시하지 않는다; 증거 없는 항목은 UNTESTED로 표시한다.
- 로컬 테스트 실행 시 반드시 `_sdd/env.md`를 따른다; 없으면 사용자에게 확인한다.

## Process

### Step 1: Scope 확정

1. `Glob`으로 `_sdd/spec/*.md` 스펙 파일 식별 (SUMMARY, prev/ 제외).
2. `DECISION_LOG.md` 존재 여부 확인.
3. 리뷰 범위 결정: Spec-only / Spec+Code(기본값).

### Step 2: Spec Quality 감사

`Read`로 스펙 파일을 읽고 아래 항목을 평가:
- Clarity / Completeness / Consistency / Testability / Structure / Ownership
- 각 컴포넌트에 _why_(설계 동기)가 있는지 확인; Purpose만 있으면 지적.

### Step 3: Code Drift 감사

`Grep`, `Glob`, `Read`로 스펙 주장과 구현을 비교:
- Architecture / Feature / API / Config / Issue / Decision-log / Source-field drift
- 증거는 `path:line`, 테스트명, commit/diff 참조로 뒷받침.
- Source field가 참조하는 파일·함수가 실존하는지 `Glob`/`Grep`으로 검증.

### Step 4: Severity 분류 및 Decision

Severity 기본 매핑:
| Drift Type | Default |
|------------|---------|
| Architecture / API | High |
| Feature / Decision-log | Medium |
| Config / Issue / Source-field | Low |

Decision 부여:
- **SPEC_OK**: material drift/quality blocker 없음
- **SYNC_REQUIRED**: 스펙 업데이트 필요 → `/spec-update-done` 권장
- **NEEDS_DISCUSSION**: 제품/아키텍처 의사결정 필요

### Step 5: 리포트 작성 및 저장

1. 기존 리포트가 있으면 `prev/PREV_SPEC_REVIEW_REPORT_<timestamp>.md`로 아카이브.
2. `write-skeleton` 서브에이전트에 위임한다. 반환값이 SKELETON_ONLY이면 Sections Remaining 목록을 보고 Edit으로 채운다.
   - 독립 섹션 2개+ → 병렬 Agent dispatch 가능
   - 의존 섹션 → 순서대로 Edit
   - 완료 후 TODO/Phase 마커 제거
   아래 Output Format으로 `_sdd/spec/SPEC_REVIEW_REPORT.md` 저장.
3. 사용자에게 severity 요약 테이블과 decision을 제시.

## Output Format

```markdown
# Spec Review Report

**Date**: YYYY-MM-DD | **Scope**: Spec-only | Spec+Code
**Decision**: SPEC_OK | SYNC_REQUIRED | NEEDS_DISCUSSION

## Summary
<1-paragraph overview>

## Findings

### High
1. <finding> — Evidence: `path:line` — Recommendation: ...

### Medium
...

### Low
...

## Open Questions
1. ...

## Suggested Next Actions
1. ...
```

SYNC_REQUIRED인 경우 `Handoff` 섹션을 추가하여 업데이트 우선순위(P1/P2/P3)를 기록한다.
Decision Log 제안이 있으면 `Decision Log Proposals` 섹션을 추가한다.

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 코드베이스 접근 불가 | Spec-only 모드로 전환 |
| git 이력 없음 | 현재 코드 상태만으로 drift 분석 |
| 다수 스펙 파일 존재 | 사용자에게 리뷰 범위 확인 |
| 기존 리뷰 리포트 존재 | `prev/`로 아카이브 후 신규 작성 |
| Decision Log 미존재 | Decision-log drift 분석 생략, 생성 제안 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

---

> **Mirror Notice**: 이 스킬의 본문은 `.claude/agents/spec-review.md`의 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
