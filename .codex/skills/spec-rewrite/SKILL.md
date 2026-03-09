---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", or equivalent phrases indicating they want to reorganize an overly long/complex spec by pruning noise, splitting into hierarchical files, and explicitly listing ambiguities/problems.
version: 1.0.0
---

# Spec Rewrite - Restructure Long or Complex Specs

Rewrite long or complex specs into a clearer structure by pruning unnecessary content (delete or move to appendix), splitting into hierarchical files, and explicitly documenting ambiguities and quality issues.

## Overview

This skill treats `_sdd/spec/` as a documentation refactoring target, not a feature-expansion task.

Primary goals:
1. Remove low-value content or move it to appendices
2. Split content into multiple files with a clear hierarchy
3. Explicitly report ambiguities, conflicts, and missing decisions

## When to Use This Skill

- The spec is too long to scan and maintain effectively
- Core sections are mixed with logs, verbose historical notes, or repeated details
- Topic-based separation is needed, but the current file layout is flat or unclear
- Spec quality needs cleanup before implementation planning starts

## Hard Rules

1. **Always backup**: 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
2. **Preserve decision context**: 삭제하는 섹션에 중요한 "why" 컨텍스트가 있으면 `DECISION_LOG.md`에 보존한다.
3. **자동 검증 우선**: 대규모 구조 변경(파일 분할, 대량 이동) 전에 반드시 자동 검증을 받는다.
4. **한국어 작성**: 추가/수정 내용은 한국어로 작성한다 (기존 언어 유지).
5. **최소 산출물**: `DECISION_LOG.md` 외 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.

## Input Sources

### Primary
- `_sdd/spec/main.md` or `_sdd/spec/<project>.md`

### Secondary
- Sub-spec files linked from the main spec
- `_sdd/implementation/` outputs (plan/progress/review) for ambiguity validation
- `_sdd/spec/DECISION_LOG.md` (if present, for preserving rationale context)

## Rewrite Process

### Step 1: Diagnose Document Quality

**Tools**: `Read`, `Glob`

First identify structural quality issues in the current spec.

- Section length imbalance (single section dominates document size)
- Duplicated explanations, tables, or checklists
- Out-of-scope content (ops logs, temporary notes, long historical narratives)
- Broken links, inconsistent filenames, missing references
- Ambiguous wording ("as needed", "fast", "appropriately")
- Missing acceptance or completion criteria

**Decision Gate 1→2**:
```
quality_issues_identified = 구조적 품질 이슈 식별 완료
scope_clear = 리라이트 범위 명확

IF quality_issues_identified AND scope_clear → Step 2 진행
ELSE IF NOT quality_issues_identified → 추가 진단 수행
ELSE → deterministic defaults (non-interactive): 리라이트 범위 확인
```

### Step 2: Propose Rewrite Plan First

**Tools**: `deterministic defaults (non-interactive)`

Present a rewrite plan before making changes.

```markdown
## Spec Rewrite Plan

**Target**: `_sdd/spec/<project>.md`

### 1) Keep in Main
- [Core goal/scope/architecture summary]

### 2) Move to Appendix
- [Sections to move and rationale]

### 3) Split Map (복잡도에 따라 선택)

**중규모** (500–1500줄):
- `_sdd/spec/main.md` (인덱스)
- `_sdd/spec/<component>.md` (컴포넌트별 파일)

**대규모** (1500줄+):
- `_sdd/spec/main.md` (인덱스)
- `_sdd/spec/<component>/overview.md` (컴포넌트 서브디렉토리)

### 4) Ambiguities / Risks to Resolve
- [Ambiguous/conflicting/missing items]
```

For large structural changes (file splits and bulk moves), run automatic safety checks first.

**Decision Gate 2→3**:
```
plan_presented = 리라이트 계획을 작업 로그로 제시 완료
plan_validated = 자동 일관성/안전성 검증 통과

IF plan_presented AND plan_validated → Step 3 진행
ELSE IF NOT plan_presented → Step 2 재실행
ELSE → 자동 보정 후 계획 수정 (최대 2라운드)
```

### Step 3: Create Safety Backups

**Tools**: `Bash (mkdir -p, cp)`, `Write`

For every existing file you modify, create a backup under `_sdd/spec/prev/` using `prev/PREV_<filename>_<timestamp>.md` (create `_sdd/spec/prev/` first if missing).

### Step 4: Prune and Appendix Migration

**Tools**: `Edit`, `Write`, `Read`

Rules:
- Keep only decision-driving and execution-critical content in the main document
- Move long examples, verbose logs, and reference-only material to appendix (`appendix.md` or `<project>_APPENDIX.md`)
- Keep one canonical version of repeated content and replace duplicates with links
- Do not drop important "why" context silently; preserve it in `_sdd/spec/DECISION_LOG.md` when needed

### Step 4.5: Preserve Decision Context

**Tools**: `Read`, `Edit`

If rewriting removes narrative sections that contain meaningful rationale:
- Add a concise entry to `_sdd/spec/DECISION_LOG.md`
- Keep the rewritten main spec concise, and keep detailed rationale in the decision log
- Do not create additional side documents by default; keep rationale tracking in `DECISION_LOG.md`

### Step 5: Hierarchical Split

**Tools**: `Write`, `Bash (mkdir -p)`, `Glob`

프로젝트 복잡도에 따라 적절한 구조를 선택한다:

| 규모 | 구조 | 기준 |
|------|------|------|
| 소규모 | `main.md` 단일 파일 | 스펙 500줄 이하 |
| 중규모 | `main.md` (인덱스) + `<component>.md` | 스펙 500–1500줄 |
| 대규모 | `main.md` (인덱스) + `<component>/` 서브디렉토리 | 스펙 1500줄 초과 |

**중규모** — main.md + 컴포넌트 파일:
```
_sdd/spec/
├── main.md              # 인덱스 (목표, 아키텍처 요약, 컴포넌트 링크)
├── api.md
├── database.md
└── frontend.md
```

**대규모** — main.md + 컴포넌트 서브디렉토리:
```
_sdd/spec/
├── main.md              # 인덱스
├── api/
│   ├── overview.md
│   └── endpoints.md
├── database/
│   ├── overview.md
│   └── schema.md
└── frontend/
    ├── overview.md
    └── components.md
```

Rules:
- `main.md`는 항상 인덱스 역할 (목표, 아키텍처 요약, 컴포넌트 링크)
- 각 컴포넌트 파일/디렉토리는 단일 주제 책임
- 상대 링크 표준화 및 깨진 링크 수정
- 파일명은 컴포넌트 이름 그대로 사용 (번호 접두사 불필요)

### Step 6: Ambiguity and Problem Reporting

**Tools**: `Write`

Always call out these issue types explicitly.

- **Ambiguous Requirement**: requirement has multiple valid interpretations
- **Missing Acceptance Criteria**: no clear done condition
- **Conflicting Statements**: contradictory rules inside the spec
- **Undefined Ownership**: no clear owner/team/component responsibility
- **Outdated Claim**: statement no longer matches code or recent decisions

If needed, add `## Open Questions` to the index and keep detailed items in the report file.

## Output Format

### 1) Rewritten Spec Files

- List of rewritten files
- List of newly created sub-files
- List of sections moved to appendix

### 2) Rewrite Report

Create or update `_sdd/spec/REWRITE_REPORT.md` with:

```markdown
## Rewrite Summary
- Target document:
- Execution timestamp:
- Key changes:

## What Was Pruned or Moved
- [item] -> [appendix/file]

## File Split Map
- [index + sub-file tree]

## Ambiguities and Issues
- [Priority] [Type] description
- Suggested resolution

## Decision Log Additions
- [Entry title] (if any)
- Why this was recorded
```

## Quality Checklist

- Can a reader understand goal/scope/acceptance criteria quickly from the index?
- Are detailed sections separated by topic into dedicated files?
- Are links and paths valid?
- Are ambiguities/conflicts/missing items explicitly documented?
- Is unnecessary duplication removed?
- Is essential rationale preserved (in spec or `_sdd/spec/DECISION_LOG.md`)?

## Best Practices

### Writing Quality

- **Be Specific**: 모호한 표현("적절히", "필요에 따라") 제거, 구체적 기준으로 대체
- **Use Examples**: 코드 스니펫과 사용 예시 포함
- **Stay Current**: 코드와 맞지 않는 내용 발견 시 수정
- **Link to Code**: 파일 경로와 라인 번호 참조

### Organization

- **Logical Flow**: 개요 → 상세 순서 유지
- **Consistent Format**: 컴포넌트 간 동일한 구조 사용
- **Table of Contents**: 500줄 이상 문서에 목차 포함

### Completeness

- **All Components**: 모든 주요 컴포넌트 문서화
- **Error Cases**: 에러 처리와 엣지 케이스 문서화
- **Dependencies**: 모든 외부 의존성 기재
- **Configuration**: 모든 설정 옵션 문서화

### Decision Traceability

- **Record Why**: 비자명한 결정은 `_sdd/spec/DECISION_LOG.md`에 기록
- **Keep It Minimal**: 짧은 근거 항목으로 충분; 장문 서술 지양
- **Update on Change**: 방향/가정 변경 시 새 항목 추가
- **Artifact Scope**: 기본은 `DECISION_LOG.md`만; 추가 거버넌스 문서는 사용자 요청 시에만

## Language Preference

- Keep the existing spec language by default
- For mixed-language specs, follow the index document language
- If requested by the user, normalize output to a single language

## Context Management

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `rg`/`Glob`/`Read`/`Bash`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `rg`/`Glob`/`Read`/`Bash` 위주 → 최소한의 `Read` |

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 백업 디렉토리 미존재 | `mkdir -p _sdd/spec/prev/` 자동 생성 |
| 스펙이 이미 잘 구조화됨 | 불필요한 리라이트 지양, 작업 로그에 보고 |
| 분할 후 링크 깨짐 | Glob으로 경로 검증, 자동 수정 |
| DECISION_LOG.md 미존재 | 필요 시 새로 생성 |
| 계획 검증 실패 | 자동 보정 후 수정안 생성 (최대 2라운드) |
| 대형 스펙 (1000줄+) | 인덱스 기반 점진적 읽기, 섹션별 처리 |

## Additional Resources

### Reference Files
- `references/rewrite-checklist.md` - diagnosis/splitting/report checklist

### Example Files
- `examples/rewrite-report.md` - sample rewrite result report

## Integration with Other Skills

- **spec-update-done**: validate against code-level reality
- **spec-summary**: regenerate summary after rewrite
- **implementation-plan**: plan implementation from cleaned spec
