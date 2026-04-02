---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", "review spec quality", or equivalent phrases indicating they want to reorganize an overly long/complex spec by pruning noise, splitting into hierarchical files, and explicitly listing ambiguities/problems.
version: 1.6.0
---

# Spec Rewrite - Restructure Long or Complex Specs

Rewrite long or complex specs into a clearer structure by pruning unnecessary content, splitting into hierarchical files, and explicitly documenting ambiguities and quality issues.

`_sdd/spec/`을 문서 리팩토링 대상으로 다루되, 재작성 전에 8개 핵심 품질 metric과 `docs/SDD_SPEC_DEFINITION.md` 기준으로 현재 스펙을 진단한다. `spec-rewrite`는 정리/재배치 도구이지, 누락된 whitepaper narrative를 자동 생성하는 스킬이 아니다.

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 리라이트 대상과 범위가 8개 핵심 metric으로 진단되고, 점수 또는 동등한 판단 근거가 남았다
- [ ] AC2: 리라이트 계획이 metric 기반 rationale, split map, ambiguity/risk와 함께 사용자에게 제시되었다
- [ ] AC3: 수정 대상 파일이 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업되었다
- [ ] AC4: 스펙이 더 명확한 구조를 가지며, 인덱스(main.md)에서 필요한 하위 파일/섹션으로 탐색 가능하다
- [ ] AC5: `REWRITE_REPORT.md`가 metric scorecard, whitepaper 적합성 평가, unresolved warning을 포함한다
- [ ] AC6: 기존 `Why`, `Source`, inline citation, whitepaper 핵심 narrative가 보존되었다
- [ ] AC7: 삭제된 섹션의 why-context가 `DECISION_LOG.md` 또는 rewrite report에 보존되었다

## Hard Rules

| # | 규칙 | 설명 |
|---|------|------|
| 1 | 백업 필수 | 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업 |
| 2 | 사용자 확인 우선 | 대규모 구조 변경(파일 분할, 대량 이동) 전 반드시 사용자 확인 |
| 3 | 언어 규칙 | 기존 스펙 언어 따름. 새 프로젝트는 한국어 기본. 사용자 지정 시 해당 언어 |
| 4 | 최소 산출물 | `DECISION_LOG.md` 외 추가 거버넌스 문서는 사용자 요청 시에만 생성 |
| 5 | 보존: Decision context | 삭제 섹션의 why-context → `DECISION_LOG.md` 또는 rewrite report에 보존 |
| 6 | 보존: Source / Why | 컴포넌트의 `Source`와 `Why`는 섹션 이동 후에도 inline으로 유지 |
| 7 | 보존: Inline citation | `[filepath:functionName]` 형식 코드 참조 및 Code Reference Index 유지 |
| 8 | 보존: Whitepaper narrative | §1 Background & Motivation, §2 Core Design, §5 Usage Guide가 존재하면 prune/split/appendix 이동으로 약화시키지 않음 |
| 9 | 자동 보강 금지 | 누락된 whitepaper 섹션은 경고할 수 있지만 자동 생성하지 않는다 |

## Input Sources

- **Primary**: `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`
- **Secondary**: 링크된 sub-spec 파일, `_sdd/implementation/` 산출물, `_sdd/spec/DECISION_LOG.md`
- **Definition Lens**: `docs/SDD_SPEC_DEFINITION.md`

## Rewrite Process

### Step 1: Diagnose Document Quality

**Tools**: `Read`, `Glob`

먼저 다음 reference를 읽는다.

- `references/template-compact.md`
- `references/spec-format.md`
- `references/rewrite-checklist.md`
- `docs/SDD_SPEC_DEFINITION.md`

진단은 아래 8개 핵심 metric을 기준으로 수행한다. 상세 질문형 rubric은 `references/rewrite-checklist.md`를 canonical source로 사용한다.

평점 기준:
- `0`: 거의 없음. 사용자가 이 정보로 판단/행동하기 어렵다
- `1`: 일부 존재하지만 불완전하거나 많이 흩어져 있다
- `2`: 대체로 충분하지만 핵심 공백이나 혼동 지점이 있다
- `3`: 명확하고 일관되며, 사용자가 쉽게 이해하고 활용할 수 있다

핵심 metric:
- `Component Separation` (`component 분리 적절성`): 각 주요 component가 대표 섹션/파일에 귀속되는가
- `Findability` (`탐색성`): 필요한 정보를 main 기준 2-hop 이내에 찾을 수 있는가
- `Repo Purpose Clarity` (`레포 목적 이해도`): main만 읽고 3문장 안에 레포 목적과 핵심 기능을 설명할 수 있는가
- `Architecture Clarity` (`아키텍처 이해도`): 핵심 흐름과 component 책임을 혼동 없이 설명할 수 있는가
- `Usage Completeness` (`사용법 완결성`): 신규 사용자가 대표 시나리오를 문서만 보고 실행할 수 있는가
- `Environment Reproducibility` (`환경 재현성`): 실행 조건, 의존성, 설정을 문서만으로 재현할 수 있는가
- `Ambiguity Control` (`모호성 수준`): 측정 불가능한 표현, 책임 불명확, 미정의 용어가 적절히 통제되는가
- `Why/Decision Preservation` (`Why/decision 보존도`): 중요한 설계 이유와 결정 배경이 삭제되거나 appendix로 밀려나지 않았는가

추가 whitepaper 평가 축:
- 배경 및 동기 설명 여부
- 핵심 설계 서사와 로직 흐름 설명 여부
- 구현 근거와 코드 매핑 존재 여부
- 사용 가이드와 기대 결과 존재 여부
- 참조형 보조 정보와 narrative 섹션의 균형

**Gate 1→2**: 품질 이슈 식별 완료 AND 리라이트 범위 명확 → Step 2. 아니면 추가 진단 또는 사용자 확인.

### Step 2: Propose Rewrite Plan

**Tools**: `AskUserQuestion`

사용자에게 아래 구조의 리라이트 계획을 제시하고 승인을 받는다:

```markdown
## Spec Rewrite Plan
**Target**: `_sdd/spec/<project>.md`

### 1) Keep in Main
### 2) Move to Appendix
### 3) Split Map
### 4) Metric-driven Rationale
### 5) Ambiguities / Risks / Whitepaper Warnings
```

계획에는 낮은 점수 metric을 어떻게 개선할지와, whitepaper 기준에서 자동 보강하지 않고 경고만 남길 항목을 함께 적는다.

**Gate 2→3**: 사용자 승인 → Step 3. 피드백 시 수정안 제시 (최대 2라운드). 2라운드 후 거부 시 진단 결과를 `REWRITE_REPORT.md`에 저장하고 종료.

### Step 3: Create Safety Backups

**Tools**: `Bash (mkdir -p, cp)`, `Write`

수정 대상 파일을 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업. 디렉토리 미존재 시 `mkdir -p`.

### Step 4: Rewrite the Spec

**Tools**: `Edit`, `Write`, `Read`

- 결정 구동(decision-driving) 및 실행 핵심(execution-critical) 콘텐츠만 main에 유지
- 장문 예시, 로그, 참조 전용 자료 → appendix
- 중복 콘텐츠: 정본 1개 유지, 나머지는 링크로 대체
- 삭제 시 why-context → `_sdd/spec/DECISION_LOG.md` 또는 rewrite report에 보존
- `Why`, `Source`, inline citation, code excerpt header는 유지
- missing whitepaper narrative는 새로 생성하지 않고 report에서 경고

### Step 5: Hierarchical Split

**Tools**: `Write`, `Bash (mkdir -p)`, `Glob`

멀티파일 구조 규칙:

1. `main.md = 인덱스 + 공통 섹션`: main에서 레포 목적, 핵심 흐름, 사용법 탐색이 더 쉬워져야 한다
2. 컴포넌트 파일명은 component/topic 책임 기준으로 직관적으로 명명한다
3. 모든 sub-spec 파일은 main에서 도달 가능해야 한다
4. split은 탐색성과 component 분리 적절성을 개선하는 방향이어야 한다

파일 작성 위임 규칙:
- 현재 콘텍스트에서 먼저 skeleton/섹션 헤더를 기록한 뒤 같은 흐름에서 Edit으로 내용을 채운다
- 독립 섹션 2개+이면 병렬 Agent dispatch 가능
- 의존 섹션은 순차 Edit
- 완료 후 TODO/Phase 마커 제거

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
| Whitepaper Gap | `docs/SDD_SPEC_DEFINITION.md` 기준 narrative/code mapping/usage guidance 부족 |

필요 시 인덱스에 `## Open Questions` 추가.

### Step 7: Validation

**Tools**: `Glob`, `Read`

`references/rewrite-checklist.md`를 읽고 체크 항목을 검증한다.

검증 항목:
- 링크/경로 유효성
- 8개 핵심 metric scorecard
- whitepaper 적합성 평가
- ambiguity / issue 기록 여부
- pruning / move / split 결과
- 자동 보강하지 않고 경고만 남긴 항목 정리 여부

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

## Metric Scorecard
- Component Separation: [0-3] - evidence / implication
- Findability: [0-3] - evidence / implication
- Repo Purpose Clarity: [0-3] - evidence / implication
- Architecture Clarity: [0-3] - evidence / implication
- Usage Completeness: [0-3] - evidence / implication
- Environment Reproducibility: [0-3] - evidence / implication
- Ambiguity Control: [0-3] - evidence / implication
- Why/Decision Preservation: [0-3] - evidence / implication

## Ambiguities and Issues
- [Priority] [Type] description
- Suggested resolution

## Whitepaper Fit Assessment
- Background & Motivation:
- Core Design Narrative:
- Code Grounding / Citation:
- Usage Guide & Expected Results:
- Reference Balance:

## Warnings Left Unresolved
- [warning]

## Decision Log Additions
- [Entry title] (if any)
- Why this was recorded
```

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 백업 디렉토리 미존재 | `mkdir -p _sdd/spec/prev/` 자동 생성 |
| 스펙이 이미 잘 구조화됨 | 불필요한 리라이트 지양, metric 기반 개선점만 보고 |
| 분할 후 링크 깨짐 | Glob으로 경로 검증, 자동 수정 |
| DECISION_LOG.md 미존재 | 필요 시 새로 생성 |
| whitepaper narrative 누락 | 자동 생성하지 말고 report에 경고 |
| 사용자가 계획 거부 | 피드백 반영 후 수정안 제시 (최대 2라운드) |

## References

- `references/template-compact.md` — compact rewrite target structure
- `references/rewrite-checklist.md` — question-style rubric and validation checklist
- `references/spec-format.md` — whitepaper evaluation / preservation reference
- `examples/rewrite-report.md` — sample rewrite report with metric scorecard
- `docs/SDD_SPEC_DEFINITION.md` — spec-as-whitepaper definition

**Related skills**: spec-update-done, spec-summary, spec-upgrade, implementation-plan

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
