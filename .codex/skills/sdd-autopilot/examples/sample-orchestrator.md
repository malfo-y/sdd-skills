# Sample Orchestrator - Codex Medium Pipeline Example

이 파일은 `sdd-autopilot`이 생성하는 orchestration skill의 완성도 기준 예시다.
사용자가 "Codex autopilot parity review와 restoration을 구현해줘"를 요청한 경우의 중규모 예시다.

## Generated Orchestrator Example

```markdown
# Orchestrator: Autopilot Parity Review

**generated**: 2026-03-17T23:00:00
**scale**: medium
**owner**: sdd-autopilot
**status**: active

## Goal

Claude `sdd-autopilot`과 Codex `sdd-autopilot`의 의미적 parity를 검토하고, 누락되거나 잘못 축약된 실행 계약을 복원한다.

### Clarified Requirements
- main skill body parity를 확인한다
- pipeline templates, scale assessment, sample orchestrator의 참조 계약을 맞춘다
- Codex custom agent spawn 모델을 유지한다
- 문서 드리프트와 실행 계약 누락을 바로 수정한다

### Constraints
- 기존 custom agent roster를 유지한다
- generated orchestrator는 custom agent 이름만 사용한다
- `_sdd/spec/`는 직접 수정하지 않는다

## Pipeline Steps

### Step 1: feature_draft

**agent**: `feature_draft`
**input**: (none)
**output**: `_sdd/drafts/feature_draft_autopilot_parity_review.md`

**prompt**:
Create a feature draft for the Codex/Claude autopilot parity review and restoration work.

Required focus:
- main skill body parity
- reference parity
- sample orchestrator parity
- Codex execution linkage sanity check

Keep the original user request and target files visible in the draft.

### Step 2: implementation_plan

**agent**: `implementation_plan`
**input**: `_sdd/drafts/feature_draft_autopilot_parity_review.md`
**output**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

**prompt**:
Turn the feature draft into an implementation plan.

Requirements:
- separate research, patching, and validation work
- keep Target Files explicit
- include documentation sync and validation steps

### Step 3: implementation

**agent**: `implementation`
**input**: `_sdd/drafts/feature_draft_autopilot_parity_review.md`
**output**:
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.codex/skills/sdd-autopilot/references/pipeline-templates.md`
- `.codex/skills/sdd-autopilot/references/scale-assessment.md`
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

**prompt**:
Implement the parity restoration plan.

TDD / verification expectations:
1. compare Codex and Claude documents
2. patch missing execution contracts
3. keep Codex-specific divergences explicit
4. run repository hygiene checks after edits

### Step 4: implementation_review

**agent**: `implementation_review`
**input**:
- `_sdd/drafts/feature_draft_autopilot_parity_review.md`
- modified Codex autopilot docs
**output**: review findings in text

**prompt**:
Review the updated Codex autopilot docs against the feature draft.

Focus:
- missing contracts
- incorrect translation
- doc drift
- execution linkage mismatch

### Step 5: spec_update_done

**agent**: `spec_update_done`
**input**: relevant spec docs if spec sync becomes necessary
**output**: optional

**prompt**:
Run only if implementation reveals spec drift that should be synchronized now.

## Artifact Handoff

- feature draft: `_sdd/drafts/feature_draft_autopilot_parity_review.md`
- implementation report: `_sdd/implementation/features/autopilot-parity-review/SYNC_20260317_230000_IMPLEMENTATION_REPORT.md`
- pipeline log: `_sdd/pipeline/log_autopilot_parity_review_20260317_230000.md`
- final report: `_sdd/pipeline/report_autopilot_parity_review_20260317_230000.md`

## Review-Fix Loop

- **max rounds**: 3
- **stop condition**: critical = 0 and high = 0
- **fix scope**: critical/high only

### Review Prompt

Review the Codex autopilot docs after the implementation step.

Check:
- When to Use / Do Not Use coverage
- pipeline lifecycle, review-fix, test, error handling coverage
- sample orchestrator detail density
- consistency with custom-agent execution model

### Fix Prompt

If critical/high issues remain, send only those issues back to `implementation`.
Do not broaden the scope beyond the identified parity gaps.

## Test Strategy

- **strategy**: inline verification
- **commands**:
  - `git diff --check`
  - targeted `rg` sanity checks for agent names, report path, and lifecycle wording
- **retry loop**: allowed when verification failures are local and quick to fix

## Error Handling

- **retry**: 3
- **critical steps**: `feature_draft`, `implementation_plan`, `implementation`, `implementation_review`
- **non-critical steps**: `spec_update_done`
- **fallback**: if review still fails after 3 rounds, leave active orchestrator in place and write a partial report
```

## Matching Pipeline Log Example

```markdown
# Pipeline Log: Autopilot Parity Review

## Meta
- **request**: "Codex autopilot 스킬을 Claude와 비교해서 빠진 걸 복원해줘"
- **orchestrator**: `.codex/skills/orchestrator_autopilot_parity_review/SKILL.md`
- **scale**: medium
- **started**: 2026-03-17T23:00:00
- **pipeline**: feature_draft -> implementation_plan -> implementation -> implementation_review

## Status
| Step | Agent | Status | Output |
|------|-------|--------|--------|
| 1 | feature_draft | completed | `_sdd/drafts/feature_draft_autopilot_parity_review.md` |
| 2 | implementation_plan | completed | `_sdd/implementation/IMPLEMENTATION_PLAN.md` |
| 3 | implementation | completed | 4 Codex autopilot docs updated |
| 4 | implementation_review | completed | no blocking findings |

## Execution Log

### feature_draft -- completed
- **time**: 23:00:00 ~ 23:05:00
- **output**: `_sdd/drafts/feature_draft_autopilot_parity_review.md`
- **key decisions**:
  - parity review 범위를 main skill + references + example + execution linkage로 확정
  - Codex divergence와 결함을 분리해 분류하기로 함
- **issues**: none

### implementation_plan -- completed
- **time**: 23:05:00 ~ 23:09:00
- **output**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **key decisions**:
  - research -> patch -> validation 순서
  - documentation sync를 구현 범위에 포함
- **issues**: none

### implementation -- completed
- **time**: 23:09:00 ~ 23:24:00
- **output**:
  - `.codex/skills/sdd-autopilot/SKILL.md`
  - `.codex/skills/sdd-autopilot/references/pipeline-templates.md`
  - `.codex/skills/sdd-autopilot/references/scale-assessment.md`
  - `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- **key decisions**:
  - When to Use / Do Not Use 복원
  - scale guide 경계 사례와 examples 복원
  - sample orchestrator에 review-fix, test, error handling, report path 추가
- **issues**: none

### implementation_review -- completed
- **time**: 23:24:00 ~ 23:28:00
- **result**: critical 0, high 0, medium 1, low 0
- **logged residual**:
  - actual Codex runtime dry-run remains manual
```

## Matching Final Report Example

```markdown
# Final Report: Autopilot Parity Review

## What Was Done

- compared Claude and Codex `sdd-autopilot` skill sets
- restored missing execution contracts in the Codex main skill
- expanded pipeline templates, scale guide, and sample orchestrator

## Results

- main skill body now includes use/do-not-use guidance, test strategy, retry/error handling, and richer orchestration requirements
- reference docs now preserve boundary rules and generated orchestrator contracts
- sample orchestrator now demonstrates artifact handoff, review-fix loop, test strategy, and final reporting

## Remaining Work

- actual Codex runtime dry-run is still required
- if runtime behavior diverges, validation guide and sample orchestrator may need a follow-up patch
```
