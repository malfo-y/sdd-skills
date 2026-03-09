---
name: spec-review
description: This skill should be used when the user asks to "review spec", "spec drift check", "verify spec accuracy", "audit spec quality", "review spec against code", "refresh spec review", "스펙 리뷰", "스펙 검토", "스펙 드리프트 점검", or wants a review-only analysis of spec quality and code-to-spec alignment without directly editing spec files.
version: 1.1.0
---

# Spec Review (Strict, Review-Only)

| Workflow | Position | When |
|----------|----------|------|
| Large | Optional (after spec-update-done) | 대규모 업데이트 후 보조 검증 |
| Any | On-demand | 이상 징후/모호함 발견 시 보조 검증 |

Review SDD spec quality and spec-to-code alignment in strict review-only mode.
This skill generates findings and recommendations, but does not edit `_sdd/spec/*.md` (including `DECISION_LOG.md`).

A good spec is not a copy of the code. It is a searchable map that helps people and LLMs:
- understand what the repository does
- find where a feature or responsibility lives
- decide where to edit safely
- remember non-obvious decisions and invariants

## Hard Rules

1. `_sdd/spec/` 아래 실제 스펙은 수정하지 않는다.
2. `DECISION_LOG.md`도 직접 수정하지 않는다. 필요하면 제안만 남긴다.
3. 산출물은 `_sdd/spec/SPEC_REVIEW_REPORT.md` 리뷰 리포트다.
4. High / Medium finding에는 가능한 한 `file:line`, 테스트, diff 같은 구체적 근거를 붙인다.
5. 불확실한 내용은 `Open Questions`에 남긴다.
6. `MUST` 섹션과 `OPT` 섹션을 구분해서 평가한다. 선택 섹션 누락만으로 약한 스펙이라고 단정하지 않는다.
7. 리뷰 자체도 token-efficient 해야 하며, 없는 선택 섹션을 억지로 보완 요구하지 않는다.

## Overview: SDD 4 Review Dimensions

This skill evaluates four dimensions:

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
- Cross-Cutting Invariants 또는 불변 조건이 명시되어 있는가
- 비자명한 설계 결정이 `DECISION_LOG.md` 또는 스펙 본문에 기록되어 있는가
- `Open Questions`에 실질적 미결 사항이 정리되어 있는가
- "깨지면 안 되는 가정"을 스펙만 읽고 파악할 수 있는가

## When to Use This Skill

- Before implementation planning to validate spec quality
- After implementation/review cycles to detect drift
- During periodic documentation governance
- When a team wants findings first, and spec edits only after approval

## Inputs

### Primary
- `_sdd/spec/<project>.md` or `_sdd/spec/main.md`
- Linked sub-spec files (if split spec structure exists)

### Secondary
- `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
- `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- `_sdd/spec/DECISION_LOG.md` (if present)
- Recent code changes (`git diff`, `git log`, current workspace state)
- Test artifacts (when available)
- `_sdd/env.md` (when local runtime/test verification is needed)

## Review Process

### Step 1: Scope and Source Selection

**Tools**: `Glob`, `Read`

1. Identify main spec index file.
2. Enumerate linked sub-spec files.
3. Exclude generated/backup files (`SUMMARY.md`, `prev/PREV_*.md`) from primary analysis.
4. Load `_sdd/spec/DECISION_LOG.md` if present.
4.5. Capture code state: `git rev-parse --short HEAD` + uncommitted changes count (`git status --porcelain | wc -l`)
5. Define review scope:
   - Spec-only
   - Spec + code alignment (default)
6. If local commands/tests will be run for evidence, read `_sdd/env.md` and apply required setup first.

### Step 2: Audit the spec as a navigation surface

**Tools**: `Read`

Assess the spec as a searchable map for people and LLMs. Focus on:

- **Project Snapshot / Goal**: 프로젝트 목적이 빠르게 파악되는가
- **System Boundary**: 시스템 경계와 외부 의존이 명확한가
- **Repository Map**: 디렉토리-역할 매핑이 있는가
- **Runtime Map**: 요청/이벤트/데이터 흐름이 보이는가
- **Component Index**: 컴포넌트별 책임/비책임/경로가 있는가
- **Common Change Paths**: 자주 변경되는 시나리오별 진입점이 있는가
- **Open Questions**: 미결 사항이 정리되어 있는가

`MUST` 섹션과 `OPT` 섹션을 구분한다. 선택 섹션 누락만으로 감점하지 않는다.

#### Context Management (Step 1 후 적용)

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `Grep`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `Grep`/`Glob` 위주 → 최소한의 `Read` |

### Step 3: Audit changeability

**Tools**: `Read`, `Grep`

Evaluate whether someone (person or LLM) can find where to start editing for a feature change:

- `Common Change Paths` 또는 동등 정보가 있는가
- 변경 시나리오에서 관련 테스트/로그/디버깅 포인트를 찾을 수 있는가
- 컴포넌트 책임과 비책임이 구분되어 있어 안전한 편집 범위를 판단할 수 있는가
- 변경 영향 범위(blast radius)를 스펙만으로 추정할 수 있는가

### Step 4: Audit code-linked drift

**Tools**: `Grep`, `Glob`, `Read`, `Bash (git diff, git log)`

Compare spec claims to implementation evidence:

- **Architecture drift**: undocumented/new/removed components
- **Feature drift**: planned vs implemented vs documented behavior
- **API drift**: endpoint/method/schema changes
- **Config drift**: env vars/defaults/dependency versions
- **Issue drift**: resolved issues still open in spec, or new issues undocumented
- **Decision-log drift**: implemented behavior/constraints diverge from recorded rationale

#### Navigation Drift (Step 4 하위 범주)

- 새 컴포넌트가 구현에만 존재하고 Component Index에 없음
- 런타임 흐름이 바뀌었는데 Runtime Map이 낡음
- 소유 경로가 달라졌는데 Component Index가 낡음
- 운영/디버깅 경로가 바뀌었는데 Common Change Paths가 없음
- 이미 해결된 질문이 Open Questions에 남아 있거나, 새 질문이 문서에 없음

Require concrete evidence wherever possible:
- `path:line` references
- test names/status
- commit or diff references

When local runtime/test execution is used to collect evidence, follow `_sdd/env.md`.
If `_sdd/env.md` is missing/incomplete, ask the user for environment details instead of guessing.

### Step 4.5: Drift 발견 요약

Drift 발견 요약 테이블을 사용자에게 제시한 후 바로 Step 5로 진행한다 (사용자 확인을 기다리지 않는다):

```
| 카테고리 | High | Medium | Low |
|----------|------|--------|-----|
| Architecture drift | N | N | N |
| Feature drift | N | N | N |
| API drift | N | N | N |
| Config drift | N | N | N |
| Issue drift | N | N | N |
| Decision-log drift | N | N | N |
| Navigation drift | N | N | N |
```

### Step 5: Severity and Decision

**Tools**: — (분석/분류, 도구 불필요)

Classify findings:
- `High`: architecture breaks, security/reliability risks, contradictory spec claims
- `Medium`: behavior mismatch, missing acceptance criteria, important doc gaps
- `Low`: style/organization/non-blocking documentation quality issues

#### Drift Type → Default Severity Mapping

| Drift Type | Default Severity |
|------------|-----------------|
| Architecture | High |
| Feature | Medium |
| API | High |
| Config | Low |
| Issue | Low |
| Decision-log | Medium |
| Navigation | Medium |

#### Dimension별 판정

각 dimension을 PASS / WEAK / FAIL로 판정하고 결과 테이블을 제시한다:

| Dimension | Probe | 판정 | 근거 |
|-----------|-------|------|------|
| Entry Point Quality | "이 저장소는 무엇을 하는가?" | PASS | (구체적 근거) |
| Navigation Quality | "X 기능은 어디에?" | PASS | (구체적 근거) |
| Changeability | "Y를 변경하려면?" | PASS | (구체적 근거) |
| Drift | "스펙과 코드가 일치하는가?" | PASS | (구체적 근거) |
| Decision & Invariant Memory | "왜 Z를 선택? 깨지면 안 되는 가정은?" | PASS | (구체적 근거) |

Assign one overall decision:
- `SPEC_OK`: no material drift or quality blockers
- `SYNC_REQUIRED`: spec updates are needed before next planning/release step
- `NEEDS_DISCUSSION`: key ambiguities/trade-offs require product/architecture decisions

### Step 6: Report and Handoff

**Tools**: `Write`, `Bash (mkdir -p)`, `AskUserQuestion`

1. Create/update strict review report.
2. Do not edit actual spec content.
3. If decision is `SYNC_REQUIRED`, include a ready-to-apply update checklist and recommend running `/spec-update-done`.
4. If needed, include proposed `DECISION_LOG.md` entries in the report (proposal only).
5. **Progressive Disclosure**:
   ```
   1. Severity별 요약 테이블 제시:
      | Severity | 건수 | 주요 항목 |
      |----------|------|----------|
      | High | N | ... |
      | Medium | N | ... |
      | Low | N | ... |
      | Decision | SPEC_OK / SYNC_REQUIRED / NEEDS_DISCUSSION |

   2. 전체 리포트를 출력하고 `_sdd/spec/SPEC_REVIEW_REPORT.md`로 저장한다 (사용자 확인을 기다리지 않는다).
   ```

## Output

### Report File

- Default path: `_sdd/spec/SPEC_REVIEW_REPORT.md`
- If the file already exists, archive it first:
  - `_sdd/spec/prev/PREV_SPEC_REVIEW_REPORT_<timestamp>.md` (create `_sdd/spec/prev/` if missing)

### Report Format

```markdown
# Spec Review Report (Strict)

**Date**: YYYY-MM-DD
**Reviewer**: Claude
**Scope**: Spec-only | Spec+Code
**Spec Files**: [list]
**Code State**: <commit hash or workspace summary>
**Decision**: SPEC_OK | SYNC_REQUIRED | NEEDS_DISCUSSION

## Executive Summary
- <one-paragraph summary>

## Findings by Severity

### High
1. <finding>
   - Evidence: `path:line`, tests, diff references
   - Impact:
   - Recommendation:

### Medium
...

### Low
...

## Entry Point / Navigation Notes
- Goal clarity:
- System Boundary:
- Repository Map:
- Runtime Map:
- Component Index:

## Changeability Notes
- Common Change Paths:
- Test/debug discoverability:
- Responsibility boundaries:

## Spec-to-Code Drift Notes
- Architecture:
- Features:
- API:
- Configuration:
- Issues/Technical debt:
- Navigation drift:

## LLM Efficiency Notes
- Token cost of entry (spec 읽기만으로 맥락 파악이 되는가):
- Navigation precision (경로/심볼이 정확해서 불필요한 탐색이 줄어드는가):
- 선택 섹션 과잉 여부 (불필요한 OPT 섹션이 토큰을 낭비하는가):

## Open Questions
1. <question requiring decision>

## Suggested Next Actions
1. <action>
2. <action>

## Decision Log Follow-ups (Proposal Only)
- Proposed entry: <title>
  - Context:
  - Decision:
  - Rationale:
  - Alternatives considered:
  - Impact / follow-up:

## Handoff for Spec Updates (if SYNC_REQUIRED)
- Recommended command: `/spec-update-done`
- Update priorities:
  - P1:
  - P2:
  - P3:
```

## Guardrails

- Do not present assumptions as facts; label unknowns clearly.
- Prefer evidence-backed findings over broad statements.
- Separate objective drift findings from subjective design suggestions.
- Keep recommendations actionable and ordered by risk/impact.
- Keep `DECISION_LOG.md` updates as recommendations only in this skill.
- Keep artifact recommendations minimal: default to `DECISION_LOG.md` only unless the user asks for more.
- Do not run local runtime/tests with inferred setup; use `_sdd/env.md` or user-confirmed environment details.
- `MUST` 섹션과 `OPT` 섹션을 구분해서 평가한다. 선택 섹션 누락만으로 약한 스펙이라고 단정하지 않는다.

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 코드베이스 접근 불가 | Spec-only 모드로 전환, 코드 drift 분석 생략 |
| `_sdd/env.md` 미존재 | 로컬 테스트 건너뛰고 코드 분석만 수행 |
| git 이력 없음 | 현재 코드 상태만으로 drift 분석 |
| 다수 스펙 파일 존재 | 사용자에게 리뷰 범위 확인 |
| Evidence 부족 | UNTESTED로 표시, 신뢰도 낮음 명시 |
| 기존 리뷰 리포트 존재 | `prev/PREV_SPEC_REVIEW_REPORT_<timestamp>.md`로 아카이브 |
| Decision Log 미존재 | Decision-log drift 분석 생략, 생성 제안 |

## Integration with Other Skills

- **spec-update-done**: apply approved spec updates and decision-log entries after this review
- **spec-update-todo**: add planned requirements before implementation
- **implementation-review**: verify plan/task completion against acceptance criteria
- **spec-summary**: regenerate summary after approved updates are applied

## Additional Resources

### Reference Files
- `references/review-checklist.md` - SDD 4-dimension review checklist and decision rules

### Example Files
- `examples/spec-review-report.md` - sample strict review report output with Navigation Drift and LLM Efficiency
