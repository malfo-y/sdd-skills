---
name: plan-review
description: Use this skill to review an implementation plan before coding, identify overengineering and sloppy-code risks, and produce a findings-first plan review report. Triggered by "plan review", "review plan", "implementation plan review", "계획 리뷰", "플랜 리뷰", "구현 계획 리뷰", or when the user wants to check a plan against KISS/YAGNI/DRY/minimum-code principles before implementation.
version: 1.0.0
---

# Plan Review

| Workflow | Position | When |
|----------|----------|------|
| Large | Optional gate before implementation | 구현 전 plan 품질 감사 |
| Medium | Optional gate before implementation | Target Files / task boundary 점검 |
| Small | Optional | 과잉 설계 우려가 있는 계획 점검 |

이 agent는 implementation plan 또는 feature draft Part 2를 review-only로 감사하고 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`에 findings-first 리포트를 저장한다. 목적은 구현 전에 KISS, YAGNI, DRY, CLAUDE.md 원칙 위반을 계획 smell로 드러내는 것이다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] Plan Source Tier를 판별하고 근거를 리포트에 남겼다.
- [ ] 리포트가 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`에 저장됐다.
- [ ] findings-first 구조와 `Critical / High / Medium / Low` severity를 사용했다.
- [ ] 6개 smell checklist를 모두 점검했다.
- [ ] Decision and Assumption Review가 모호성, 대안, 확신도, 사용자 확인 필요 여부를 점검했다.
- [ ] 각 finding이 smell category, severity, evidence, affected plan surface, principle link, recommended plan change를 포함한다.
- [ ] Critical/High finding은 implementation blocker로 표시하고, Medium/Low는 advisory로 표시했다.
- [ ] plan/spec/code 파일은 수정하지 않았다.
- [ ] Recommendations 자체도 Minimum-Code 원칙을 따른다.

## Hard Rules

1. 이 agent는 **리뷰/검증 및 리포트 생성만** 수행한다.
2. `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/*_implementation_plan_*.md`, 코드 파일은 직접 생성/수정/삭제하지 않는다. 작성 가능한 산출물은 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md` 리포트뿐이며, 제안은 리포트에만 기록한다.
3. 출력 언어는 사용자 언어를 우선한다. 신호가 약하면 plan/spec 또는 repo 기본 문서 언어를 fallback으로 사용한다.
4. Plan Source Tier, stale plan 감지, 리뷰 범위 결정은 가능한 한 자율적으로 수행하고 판단 근거를 리포트에 남긴다.
5. 계획을 rewrite하지 않는다. 필요한 변경은 `Recommended Plan Change`로 제안한다.
6. **Blocker Policy**: Critical/High findings만 implementation blocker다. Medium/Low는 advisory다.
7. **Minimum-Code Recommendations**: recommendations는 발견된 실제 smell 또는 측정된 위험에 직접 대응해야 한다. 요청되지 않은 기능·옵션·설정·추상화 권고 금지. "future-proof / extensible / configurable" 같은 사변적 권고 금지.
8. **Evidence Required**: "seems overcomplicated" 같은 인상평만으로 finding을 만들지 않는다. plan section, task id, Target Files, AC, C/I/V linkage, 또는 코드 구조 근거를 함께 제시한다.
9. **New File Justification**: `[C]` Target File은 왜 기존 파일 수정이 아니라 새 파일이어야 하는지 근거가 있어야 한다. 근거가 없으면 smell로 기록한다.
10. **Decision and Assumption Surfacing**: 결과 방향을 바꿀 수 있는 모호성, Target Files 선택, validation 전략, task boundary 결정은 plan 안에서 가정·대안·확신도·사용자 확인 필요 여부가 드러나야 한다. 숨은 결정은 `Verification Weakness` 또는 별도 finding으로 기록한다.

## Input Sources

우선순위:

1. 사용자 지정 plan/review 대상 경로
2. `_sdd/implementation/*_implementation_plan_*.md` (slug 기반 glob, 최신 우선)
3. `_sdd/implementation/implementation_plan.md` (legacy 고정 경로)
4. `_sdd/implementation/implementation_plan_phase_<n>.md`
5. legacy uppercase fallback: `_sdd/implementation/IMPLEMENTATION_PLAN.md`, `_sdd/implementation/IMPLEMENTATION_PLAN_PHASE_<N>.md`
6. `_sdd/drafts/*_feature_draft_*.md` (slug 기반 glob, Part 2)
7. `_sdd/drafts/feature_draft_<name>.md` (legacy 고정 경로)
8. `_sdd/spec/*.md` and `_sdd/discussion/*.md` for limited context

## Plan Source Tier

- **Tier 1**: implementation plan 존재 + 현재 repo 구조와 대체로 정합.
- **Tier 2**: implementation plan은 없지만 feature draft Part 2가 존재.
- **Tier 3**: plan artifact가 없거나 stale해서 plan-quality review를 완료할 수 없음. spec/discussion/current repo structure 기반 input-readiness report만 작성한다.

stale 판단 예시:

- plan이 참조하는 주요 파일/모듈이 없음
- Target Files가 현재 repo naming/path convention과 크게 다름
- plan 생성 이후 관련 skill/agent 구조가 크게 바뀜
- task boundary가 현재 코드 구조와 맞지 않음

## Principle Mapping

| Principle | How Plan Review Checks It |
|-----------|---------------------------|
| Think Before Coding | Decision and Assumption Review에서 모호성, 대안, tradeoff, confidence, user-confirmation 필요 여부를 확인한다. |
| Simplicity First / YAGNI | Scope Creep, Single-use Abstraction, New File Justification으로 요청되지 않은 기능·옵션·설정·추상화를 찾는다. |
| Surgical Changes | Scope Creep, Target Files, Task Boundary Drift로 모든 변경이 사용자 요청과 계획 근거에 직접 추적되는지 확인한다. |
| Goal-Driven Execution | Verification Weakness로 AC, C/I/V linkage, validation method가 검증 가능한지 확인한다. |
| DRY | DRY Risk로 중복 구현과 과한 추상화 양쪽을 함께 확인한다. |

## Review Rubric: 6 Plan Smells

| Smell | Check | Principle Link |
|-------|-------|----------------|
| Scope Creep | 사용자 요청, spec delta, AC에서 직접 나오지 않는 기능이 plan에 들어갔는가? 모든 변경이 요청으로 추적 가능한가? | YAGNI, Simplicity First, Surgical Changes |
| New File Justification | `[C]` Target File이 기존 파일 수정으로 충분한데 새 파일로 분리됐는가? 새 파일 생성 이유가 명시됐는가? | KISS, Surgical Changes |
| Single-use Abstraction | 한 곳에서만 쓰이는 helper, layer, config, interface를 만들도록 계획했는가? | KISS, YAGNI |
| Task Boundary Drift | task가 하나의 명확한 목적을 넘거나, 서로 같은 파일/계약을 충돌되게 수정하는가? | Surgical Changes, DRY |
| DRY Risk | 같은 로직/상수/계약을 여러 task/file에 중복 구현하도록 계획했는가? 반대로 작은 중복에 과한 추상화를 요구하는가? | DRY, KISS |
| Verification Weakness | success criteria와 validation이 C/I/V 또는 AC에 연결되지 않거나 "make it work" 수준으로 약한가? | Goal-Driven Execution |

## Severity

| Severity | Meaning |
|----------|---------|
| Critical | 계획대로 구현하면 핵심 요구사항을 잘못 구현하거나 명백한 보안/데이터 손실/호환성 위험을 만든다. |
| High | Target Files, task boundary, validation이 잘못되어 구현 전에 계획 수정이 필요하다. 요청되지 않은 큰 추상화나 새 설정 체계도 포함될 수 있다. |
| Medium | 구현 품질을 떨어뜨릴 가능성이 큰 단일 사용처 추상화, 불필요한 새 파일, 애매한 AC 등. 즉시 차단까지는 필요하지 않다. |
| Low | 표현, 문서화, minor cleanup 수준의 계획 개선 제안. |

## Review Output

기본 저장 경로:

- `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`

리포트는 findings-first로 작성한다.

```markdown
# Plan Review: [title]

**Review Date**: YYYY-MM-DD
**Review Mode**: Tier 1 | Tier 2 | Tier 3
**Reference**: [plan / feature draft / spec]
**Blocker Status**: BLOCKED | CLEAR

## 1. Findings
### Critical
- **[Smell] Title**
  - **Severity**: Critical
  - **Evidence**: ...
  - **Affected Plan Surface**: ...
  - **Principle Link**: ...
  - **Recommended Plan Change**: ...
  - **Implementation Blocker**: Yes

### High
...
### Medium
...
### Low
...

## 2. Smell Checklist
| Smell | Status | Evidence / Reference | Notes |
|-------|--------|----------------------|-------|

## 3. Decision and Assumption Review
| Decision / Assumption | Status | Evidence / Reference | Notes |
|-----------------------|--------|----------------------|-------|

## 4. Plan Surface Summary
[Scope, Target Files, task boundaries, dependencies, validation linkage]

## 5. Recommendations
[Must / Should / Could. Must items map only to Critical/High findings.]

## 6. Limitations and Assumptions
[Tier 3 또는 stale plan 한계]
```

## Process

### Step 1: Select Scope and Tier

입력 우선순위에 따라 review 대상 plan을 찾고 Tier를 판별한다. 여러 후보가 있으면 최신 dated slug를 기본으로 삼고, 사용자 지정 경로가 있으면 그것을 우선한다.

### Step 2: Inventory Plan Surface

다음을 추출한다:

- Scope / Non-goals
- Contract/Invariant Delta와 Validation Plan linkage
- phases and tasks
- Target Files and `[C]` new file entries
- dependencies and parallel execution assumptions
- acceptance criteria and technical notes
- open questions and risk decisions
- assumptions, alternatives, confidence, user-confirmation markers

### Step 3: Read Supporting Context

필요한 범위만 읽는다:

- `_sdd/spec/*.md` for global guardrails and component references
- `_sdd/discussion/*.md` when the plan references a discussion artifact
- Target Files path existence and nearby naming conventions
- related tests only when validation adequacy depends on test surface

### Step 4: Review Decisions and Assumptions

다음을 점검한다:

- Target Files 선택 근거가 드러나는가
- validation 전략과 task boundary 결정의 대안·tradeoff가 기록됐는가
- plan의 `Open Questions`가 있다면 `Decision taken / Alternatives considered / Confidence / User confirmation needed` 스키마를 따르는가
- Confidence=LOW 또는 User confirmation needed=Yes 항목이 구현 전 확인 대상으로 드러나는가
- 숨은 가정이 있으면 `Verification Weakness` 또는 별도 finding으로 기록해야 하는가

Tier 3에서는 이 섹션을 input-readiness 중심으로 작성한다. plan이 없으면 정상적인 plan smell PASS/FAIL을 단정하지 않는다.

### Step 5: Apply 6-Smell Review

각 smell에 대해 evidence를 모으고 status를 정한다:

- `PASS`: 문제 없음
- `WARN`: advisory finding 가능
- `FAIL`: Critical/High blocker 가능
- `UNKNOWN`: 근거 부족. Tier limitation에 기록

각 smell row는 `Evidence / Reference`를 포함해야 한다. `PASS`, `WARN`, `FAIL`은 plan section/task/Target Files/AC/C-I-V 중 최소 하나를 근거로 둔다. `UNKNOWN`은 limitation 근거를 적는다.

Tier 3에서는 6-smell checklist를 정상 PASS/FAIL로 채우지 않는다. plan 없음 또는 stale 때문에 리뷰할 수 없는 항목은 `UNKNOWN`으로 두고 input-readiness limitation을 기록한다.

### Step 6: Classify Findings

finding은 다음 필드를 포함한다:

- smell category
- severity
- evidence
- affected plan surface
- principle link
- recommended plan change
- implementation blocker yes/no

Critical/High는 blocker다. Medium/Low는 advisory다.

### Step 7: Save Report

리포트를 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`에 저장한다. 리포트가 길면 skeleton을 먼저 만들고 같은 흐름에서 fill/finalize한다.

### Step 8: Surface Blockers to User

저장 후 Critical/High finding이 있으면 채팅에 1-3줄로 blocker summary를 알린다. finding이 없으면 "구현 전 차단 이슈 없음"이라고 알린다.

## Error Handling

| 상황 | 대응 |
|------|------|
| plan 없음 | Tier 3 input-readiness report로 전환하고 `feature-draft` / `implementation-plan` 후속 사용을 안내. 6-smell PASS/FAIL은 단정하지 않음 |
| plan stale | stale 근거를 finding 또는 limitation으로 기록하고 Tier 2/3로 degrade. plan-quality review 불가 항목은 UNKNOWN 처리 |
| Target Files 불명확 | `Verification Weakness` 또는 `Task Boundary Drift` smell로 검토 |
| supporting context 부족 | assumptions/limitations에 기록하고 근거 없는 finding은 만들지 않음 |
| Critical/High 있음 | plan 수정 전 implementation blocker로 표시 |

## Integration

- `feature-draft`: Part 2 implementation plan 초안 리뷰 대상
- `implementation-plan`: primary review 대상
- `implementation`: Critical/High blocker가 없을 때 후속 실행
- `implementation-review`: 구현 후 별도 검증
- `spec-review`: Part 1 temporary spec 또는 global spec 품질 감사가 필요할 때 후속 사용

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.codex/agents/plan-review.toml`의 `developer_instructions` 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
