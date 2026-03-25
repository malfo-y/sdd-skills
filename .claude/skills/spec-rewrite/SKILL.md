---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", "review spec quality", or equivalent phrases indicating they want to reorganize an overly long/complex spec by pruning noise, splitting into hierarchical files, and explicitly listing ambiguities/problems.
version: 1.3.0
---

# Spec Rewrite - Restructure Long or Complex Specs

Rewrite long or complex specs into a clearer structure by pruning unnecessary content (delete or move to appendix), splitting into hierarchical files, and explicitly documenting ambiguities and quality issues.

`_sdd/spec/`을 문서 리팩토링 대상으로 다룬다 (기능 확장이 아님).

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 리라이트 계획이 사용자에게 제시되고 승인을 받았다
- [ ] AC2: 수정 대상 파일이 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업되었다
- [ ] AC3: 스펙이 규모 기준(소/중/대)에 맞게 분할되었고, 인덱스(main.md)에서 모든 하위 파일로 링크가 유효하다
- [ ] AC4: `REWRITE_REPORT.md`가 Output Format에 따라 생성되었다
- [ ] AC5: 모호성(ambiguity), 충돌, 누락 항목이 보고서에 명시적으로 문서화되었다
- [ ] AC6: 기존 Source 필드, inline citation, whitepaper 섹션(§1,§2,§5)이 보존되었다
- [ ] AC7: 삭제된 섹션의 "why" 컨텍스트가 `DECISION_LOG.md`에 보존되었다

## Hard Rules

| # | 규칙 | 설명 |
|---|------|------|
| 1 | 백업 필수 | 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업 |
| 2 | 사용자 확인 우선 | 대규모 구조 변경(파일 분할, 대량 이동) 전 반드시 사용자 확인 |
| 3 | 언어 규칙 | 기존 스펙 언어 따름. 새 프로젝트는 한국어 기본. 사용자 지정 시 해당 언어 |
| 4 | 최소 산출물 | `DECISION_LOG.md` 외 추가 거버넌스 문서는 사용자 요청 시에만 생성 |
| 5 | 보존: Decision context | 삭제 섹션의 "why" 컨텍스트 → `DECISION_LOG.md`에 보존 |
| 6 | 보존: Source 필드 | 컴포넌트 테이블의 `Source` 필드, 섹션 이동 시에도 매핑 유지 |
| 7 | 보존: Inline citation | `[filepath:functionName]` 형식 코드 참조 및 Code Reference Index 유지 |
| 8 | 보존: Whitepaper 섹션 | §1 Background & Motivation, §2 Core Design, §5 Usage Guide는 prune/split/이동 금지 |
| 9 | 보존: Component Why | 컴포넌트의 Why 필드(존재 이유)는 해당 섹션에 유지 — DECISION_LOG로 이동 금지 |

## Input Sources

- **Primary**: `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`
- **Secondary**: 링크된 sub-spec 파일, `_sdd/implementation/` 산출물, `_sdd/spec/DECISION_LOG.md`

## Rewrite Process

### Step 1: Diagnose Document Quality

**Tools**: `Read`, `Glob`

> **먼저 `references/template-compact.md`를 Read로 읽는다.** §1-§8 섹션 구조, Writing Rules, Modular Spec Guide가 정의되어 있다.
> **그다음 `references/spec-format.md`를 Read로 읽는다.** 화이트페이퍼 스타일 스펙의 기대 섹션 구조와 보존 규칙이 정의되어 있다.

진단 항목:
- 섹션 길이 불균형 (단일 섹션이 문서 크기 지배)
- 중복된 설명, 테이블, 체크리스트
- 범위 외 콘텐츠 (운영 로그, 임시 메모, 장문 히스토리)
- 깨진 링크, 불일치 파일명, 누락 참조
- 모호한 표현 ("적절히", "빠르게", "필요에 따라")
- 누락된 완료 기준

**Gate 1→2**: 품질 이슈 식별 완료 AND 리라이트 범위 명확 → Step 2. 아니면 추가 진단 또는 사용자 확인.

### Step 2: Propose Rewrite Plan

**Tools**: `AskUserQuestion`

사용자에게 아래 구조의 리라이트 계획을 제시하고 승인을 받는다:

```markdown
## Spec Rewrite Plan
**Target**: `_sdd/spec/<project>.md`

### 1) Keep in Main
### 2) Move to Appendix
### 3) Split Map (규모별)
### 4) Ambiguities / Risks to Resolve
```

| 규모 | 구조 | 기준 |
|------|------|------|
| 소규모 | `main.md` 단일 파일 | 500줄 이하 |
| 중규모 | `main.md` (인덱스) + `<component>.md` | 500–1500줄 |
| 대규모 | `main.md` (인덱스) + `<component>/` 서브디렉토리 | 1500줄 초과 |

**Gate 2→3**: 사용자 승인 → Step 3. 피드백 시 수정안 제시 (최대 2라운드). 2라운드 후 거부 시 진단 결과를 REWRITE_REPORT.md에 저장하고 종료.

### Step 3: Create Safety Backups

**Tools**: `Bash (mkdir -p, cp)`, `Write`

수정 대상 파일을 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업. 디렉토리 미존재 시 `mkdir -p`.

### Step 4: Prune and Appendix Migration

**Tools**: `Edit`, `Write`, `Read`

- 결정 구동(decision-driving) 및 실행 핵심(execution-critical) 콘텐츠만 메인에 유지
- 장문 예시, 로그, 참조 전용 자료 → appendix (`appendix.md` 또는 `<project>_APPENDIX.md`)
- 중복 콘텐츠: 정본 1개 유지, 나머지는 링크로 대체
- 삭제 시 "why" 컨텍스트 → `_sdd/spec/DECISION_LOG.md`에 보존

### Step 5: Hierarchical Split

**Tools**: `Write`, `Bash (mkdir -p)`, `Glob`

**멀티파일 구조 규칙:**

1. **main.md = 인덱스 + 공통 섹션**: §1 Background, §2 Core Design, §3 Architecture는 main.md에 인라인. §4 이하 컴포넌트는 링크로 분리.
2. **컴포넌트 파일명 = 컴포넌트명**: `auth.md`, `scheduler.md` 등 접두사 없이 직관적으로 명명.
3. **main.md 링크 형식**: §4 영역에 `See [Component Name](./component.md)` 형태로 링크. 모든 sub-spec 파일은 main.md에서 링크되어야 함.
4. **Cross-cutting 섹션**: §7 API, §8 Config 등 여러 컴포넌트에 걸치는 내용은 main.md에 유지하거나 별도 `api.md`, `config.md`로 분리 (규모에 따라 판단).

**중규모** 구조:
```
_sdd/spec/
├── main.md              # 인덱스 (§1-§3 인라인 + §4 컴포넌트 링크)
├── api.md
├── database.md
└── frontend.md
```

**대규모** 구조:
```
_sdd/spec/
├── main.md              # 인덱스
├── api/
│   ├── overview.md
│   └── endpoints.md
└── frontend/
    ├── overview.md
    └── components.md
```

추가 규칙:
- 각 파일/디렉토리는 단일 주제 책임
- 상대 링크 표준화 및 깨진 링크 수정

#### 파일 작성 위임

`sdd-skills:write-skeleton` 서브에이전트에 위임한다. 반환값이 SKELETON_ONLY이면 Sections Remaining 목록을 보고 Edit으로 채운다.
- 독립 섹션 2개+ → 병렬 Agent dispatch 가능
- 의존 섹션 → 순서대로 Edit
- 완료 후 TODO/Phase 마커 제거

서브에이전트 호출 시 Output Format 전체와 작성에 필요한 맥락을 프롬프트에 포함한다.

인덱스-먼저 패턴: (1) main.md 순차 작성 → (2) 컴포넌트 파일 병렬 작성. 독립 컴포넌트 2개 이상이면 병렬 디스패치. 소규모(500줄 이하)는 분할 불필요.

### Step 6: Ambiguity and Problem Reporting

**Tools**: `Write`

아래 이슈 유형을 명시적으로 보고한다:

| 유형 | 설명 |
|------|------|
| Ambiguous Requirement | 다수의 유효한 해석이 가능 |
| Missing Acceptance Criteria | 완료 조건 불명확 |
| Conflicting Statements | 스펙 내 모순 규칙 |
| Undefined Ownership | 담당 주체 불명 |
| Outdated Claim | 코드/최근 결정과 불일치 |

필요 시 인덱스에 `## Open Questions` 추가.

### Step 7: Validation

**Tools**: `Glob`, `Read`

> **`references/rewrite-checklist.md`를 Read로 읽고** 체크 항목을 검증한다.

Acceptance Criteria(AC1-AC7)를 자체 검증하고, 미충족 항목은 해당 단계로 돌아가 수정한다.

## Output Format

### 1) Rewritten Spec Files
- 재작성된 파일 목록 / 신규 생성 하위 파일 목록 / appendix 이동 섹션 목록

### 2) Rewrite Report (`_sdd/spec/logs/REWRITE_REPORT.md`)

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

## Whitepaper Section Status
- §1 Background & Motivation: [Present / Missing]
- §2 Core Design: [Present / Missing]
- §5 Usage Guide & Expected Results: [Present / Missing]
- Inline citations: [N found / None]
- Code Reference Index: [Present / Missing]

## Decision Log Additions
- [Entry title] (if any)
- Why this was recorded
```

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 백업 디렉토리 미존재 | `mkdir -p _sdd/spec/prev/` 자동 생성 |
| 스펙이 이미 잘 구조화됨 | 불필요한 리라이트 지양, 사용자에게 보고 |
| 분할 후 링크 깨짐 | Glob으로 경로 검증, 자동 수정 |
| DECISION_LOG.md 미존재 | 필요 시 새로 생성 |
| 사용자가 계획 거부 | 피드백 반영 후 수정안 제시 (최대 2라운드) |

## References

- `references/template-compact.md` — §1-§8 generation template (What/Why/How triad, Modular Spec Guide)
- `references/rewrite-checklist.md` — diagnosis/splitting/report checklist
- `references/spec-format.md` — whitepaper-style spec format and preservation rules
- `examples/rewrite-report.md` — sample rewrite report

**Related skills**: spec-update-done (코드 검증), spec-summary (요약 재생성), implementation-plan (구현 계획)

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

