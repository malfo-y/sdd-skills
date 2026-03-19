# Feature Draft: Codex Full Skills AC-First 정제

**Date**: 2026-03-19
**Author**: Codex
**선행 작업**: Codex custom agent 8개 self-contained 정제 + wrapper contract 정리 완료
**요청 배경**: Codex 쪽에서 wrapper-backed agent entrypoint를 제외한 remaining full skill 10개를, 문서 중심 SDD 스킬의 성격을 유지한 채 AC-first 원칙으로 concise하게 정제한다.

---

<!-- spec-update-todo-input-start -->

# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 직접 복사-붙여넣기하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

## Spec Update Input

**Date**: 2026-03-19
**Author**: Codex
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: SHOULD update

## Improvement Changes

### Improvement: Codex full skill 10개를 SDD 철학 기반 AC-first 구조로 정제

**Priority**: Medium
**Current State**:
Codex 핵심 파이프라인 래퍼 스킬은 이미 concise wrapper + self-contained custom agent 구조로 정리되었지만, remaining full skill 10개는 여전히 장문 workflow, 반복 섹션, explanation-heavy boilerplate가 남아 있다. 이 중 다수는 스펙 작성, 스펙 재작성, 가이드 생성, PR 문서 작성처럼 문서 산출물을 직접 다루는 스킬이며, reference template과 example이 실제 품질에 중요한 역할을 한다. 현재 대상 10개 SKILL.md의 총합은 4,906줄이며, 특히 `sdd-autopilot`, `spec-summary`, `pr-spec-patch`, `pr-review`가 전체의 대부분을 차지한다.

**Proposed**:
Codex full skill 10개를 SDD 철학에 맞는 AC-first 구조로 정리한다. 각 `SKILL.md`는 먼저 해당 스킬의 목표에 맞는 Acceptance Criteria를 정의하고, 그 기준을 만족하도록 hard rules, 핵심 process, output contract 중심으로 본문을 압축한다. `references/`와 `examples/`는 삭제하지 않고, 문서 중심 스킬의 template/example 자산으로 유지한다.

**Reason**:
SDD의 핵심은 스펙과 문서 산출물을 중심으로 요구사항, 구현, 검증을 연결하는 것이다. 따라서 full skill 정제는 reference/template/example을 제거하는 방향이 아니라, 본문에서 스킬의 목표와 실행 계약을 더 선명하게 드러내고, supporting asset은 유지한 채 중복 설명만 덜어내는 방향이어야 한다. 이렇게 해야 플랫폼 전체 일관성, 유지보수성, 문서 품질, 회귀 검증성이 함께 올라간다.

#### 대상 Skill

| Skill | 현재 줄수 | 목표 줄수 | 감축률 | 비고 |
|-------|----------|----------|--------|------|
| sdd-autopilot | 957 | ~700 | 27% | 메타스킬, generated orchestrator contract 유지 필요 |
| spec-summary | 838 | ~600 | 28% | layered summary/output contract 유지 |
| pr-spec-patch | 522 | ~360 | 31% | spec-update-todo 호환 포맷 유지 |
| pr-review | 516 | ~360 | 30% | verdict logic 유지 |
| spec-create | 463 | ~340 | 27% | bootstrap + 2-phase generation 유지 |
| spec-upgrade | 409 | ~300 | 27% | whitepaper migration contract 유지 |
| spec-rewrite | 367 | ~270 | 26% | rewrite checklist/reference 유지 |
| discussion | 326 | ~240 | 26% | iterative discussion loop 유지 |
| guide-create | 320 | ~230 | 28% | guide section contract 유지 |
| spec-snapshot | 188 | ~145 | 23% | already concise, light cleanup only |
| **합계** | **4,906** | **~3,545** | **28%** | |

#### 정제 원칙

1. **SDD philosophy first**: 스킬 본문은 “문서/스펙이 Single Source of Truth”라는 전제를 분명히 하고, 산출물 중심 handoff를 드러낸다.
2. **AC-first**: 각 full skill은 먼저 “이 스킬이 성공했다는 것은 무엇인가”를 Acceptance Criteria로 정의하고, 이후 모든 단계는 그 AC를 만족시키도록 작성한다.
3. **Core-preserving compression**: 줄 수 감축보다 스킬의 핵심 요소, 산출물 계약, 판단 규칙, 문서 품질 기준 보존을 우선한다.
4. **Reference/example retention**: `references/`, `examples/`는 유지한다. 특히 spec/guide/pr 문서형 스킬에서는 template과 example을 품질 자산으로 취급한다.
5. **Concise body**: `SKILL.md` 본문은 스킬의 목표, AC, hard rules, process, output contract에 집중하고, template 전문이나 긴 예시는 reference/example 파일로 남긴다.
6. **Codex 특화 계약 보존**: `spawn_agent`, `wait_agent`, generated orchestrator, graceful degradation 같은 Codex 고유 실행 모델은 삭제하지 않는다.

#### Recommended Decisions

- **Line budget**: hard cap이 아니라 soft budget으로 운영한다. contract와 품질 기준 보존이 줄 수보다 우선이다.
- **References / examples**: 유지한다. spec/guide/pr 문서형 스킬에서는 template과 example을 핵심 보조 자산으로 간주한다.
- **본문 역할**: `SKILL.md`는 “무엇을 만들고 어떤 기준으로 성공으로 볼지”를 짧고 선명하게 설명하고, detailed template/example은 companion asset으로 연결한다.
- **sdd-autopilot wording**: generated orchestrator와 custom agent spawn contract는 유지하되, 장문 예시와 반복 설명은 압축한다.
- **Validation 기준**: 각 skill 본문만 읽어도 목표, AC, 핵심 실행 흐름, 출력 계약을 이해할 수 있어야 하며, references/examples는 문서 품질을 높이는 companion asset으로 계속 활용 가능해야 한다.

#### Acceptance Criteria

- [ ] AC1: 대상 10개 full skill 모두 상단에 Acceptance Criteria 또는 동등한 self-check contract를 가진다.
- [ ] AC2: 대상 10개 SKILL.md 총합 줄 수가 4,906줄에서 3,700줄 이하로 감소한다.
- [ ] AC3: 각 skill이 자신의 목표에 맞는 Acceptance Criteria를 먼저 정의하고, 본문이 그 AC를 만족시키는 구조로 재작성된다.
- [ ] AC4: 각 skill의 핵심 contract와 문서 품질에 필요한 핵심 요소가 유지된다.
- [ ] AC5: `references/`, `examples/`, `skill.json`은 삭제하지 않고 유지된다.
- [ ] AC6: spec/guide/pr 문서형 스킬의 template/example 자산이 유지되고, 본문과의 역할 분리가 더 명확해진다.
- [ ] AC7: wrapper-backed agent entrypoint (`feature-draft`, `implementation*`, `spec-review`, `spec-update-*`, `ralph-loop-init`, `write-phased`)는 이번 작업 범위에 포함되지 않는다.
- [ ] AC8: full skill 본문이 핵심 계약을 잃지 않은 채 더 concise해진다.

#### Related Paths

- `.codex/skills/discussion/`
- `.codex/skills/guide-create/`
- `.codex/skills/pr-review/`
- `.codex/skills/pr-spec-patch/`
- `.codex/skills/sdd-autopilot/`
- `.codex/skills/spec-create/`
- `.codex/skills/spec-rewrite/`
- `.codex/skills/spec-snapshot/`
- `.codex/skills/spec-summary/`
- `.codex/skills/spec-upgrade/`
- `_sdd/spec/main.md`

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

| Item | Detail |
|------|--------|
| 대상 | `.codex/skills/` 하위 remaining full skill 10개 |
| 작업 유형 | AC-first 정제 + concise 본문 재구성 + reference/example asset 유지 |
| 총 태스크 | 10개 skill 정제 + 1개 spec sync follow-up |
| 예상 변경 규모 | 4,906줄 → ~3,545줄 |
| 제외 범위 | 이미 정리한 wrapper-backed agent entrypoint와 `.codex/agents/*.toml` |

## Scope

### In Scope

- `discussion`
- `guide-create`
- `pr-review`
- `pr-spec-patch`
- `sdd-autopilot`
- `spec-create`
- `spec-rewrite`
- `spec-snapshot`
- `spec-summary`
- `spec-upgrade`

### Out of Scope

- `feature-draft`
- `implementation-plan`
- `implementation`
- `implementation-review`
- `spec-review`
- `spec-update-done`
- `spec-update-todo`
- `ralph-loop-init`
- `write-phased`
- `.codex/agents/*.toml`
- Claude mirror 변경

## Common Editing Guide

### Required shape

각 대상 skill은 가능한 한 아래 구조를 따른다.

```markdown
---
frontmatter
---

# Skill Title

## Goal
[이 스킬이 만드는 문서/산출물과 성공 조건을 1-2문장으로 요약]

## Acceptance Criteria
- [ ] AC1: ...

## Hard Rules
1. ...

## Process
### Step 1: ...

## Output Contract
- Primary output: ...

## Error Handling / Edge Cases
- ...
```

### Common reduction targets

- `When to Use This Skill` 장문 설명은 frontmatter description과 trigger phrasing으로 충분하면 축소
- 반복되는 `Best Practices`, `Context Management`, `Language Handling` 장문은 hard rule 1-2줄로 흡수
- 예시가 본문 설명을 반복할 때는 예시를 `examples/`에 유지하고 본문은 contract 중심으로 축약
- reference template과 example은 유지하되, 본문이 그 존재를 전제로 핵심 계약 설명을 생략하는 구조는 금지
- 본문은 “무엇을 만들고 어떤 AC를 만족해야 하는가”를 설명하고, reference/example은 “어떻게 더 잘 쓸 것인가”를 보조한다

### Must preserve

- expected artifact path
- review/patch/verdict classification
- generated orchestrator / custom agent spawn contract
- graceful degradation or fallback rule
- 언어 규칙, 백업 규칙, read-only 규칙
- 문서형 스킬의 reference template / example 자산과 그 연결 지점

## Phases

### Phase 1: Pilot

pilot 2개를 먼저 정제해 compression rule과 review 기준을 고정한다.

| Task | Skill | 이유 |
|------|-------|------|
| 1 | `sdd-autopilot` | 가장 길고 Codex 고유 실행 계약이 많음 |
| 2 | `spec-summary` | long-form writing + artifact contract가 뚜렷함 |

### Phase 2: Core Spec / PR skills

| Task | Skill Group |
|------|-------------|
| 3 | `spec-create`, `spec-rewrite`, `spec-upgrade` |
| 4 | `pr-spec-patch`, `pr-review` |

### Phase 3: Supporting skills

| Task | Skill Group |
|------|-------------|
| 5 | `discussion`, `guide-create`, `spec-snapshot` |

### Phase 4: Verification and spec sync

| Task | Goal |
|------|------|
| 6 | line count, structure, contract, reference/example asset 보존 확인 |
| 7 | 필요 시 `_sdd/spec/main.md`에 concise full-skill policy 반영 |

## Task Details

### Task 1: `sdd-autopilot` AC-first 정제

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md`
- [R] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [R] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [R] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Acceptance Criteria**:
- [ ] Phase 1 / 1.5 / 2 구조가 보존된다.
- [ ] generated orchestrator와 custom agent spawn/wait contract가 보존된다.
- [ ] review-fix loop, execute→verify, log artifact contract가 유지된다.
- [ ] 반복 설명과 장문 use/do-not-use 섹션은 축소된다.

**Technical Notes**:
- Codex 고유 규칙은 남기되, 장문 narrative와 중복 설명만 줄인다.
- generated orchestrator 언급은 1개의 명확한 실행 contract 문단으로 수렴한다.

### Task 2: `spec-summary` AC-first 정제

**Target Files**:
- [M] `.codex/skills/spec-summary/SKILL.md`
- [R] `.codex/skills/spec-summary/references/summary-template.md`
- [R] `.codex/skills/spec-summary/examples/summary-output.md`

**Acceptance Criteria**:
- [ ] `_sdd/spec/SUMMARY.md` artifact contract가 보존된다.
- [ ] README sync는 explicit request only 규칙이 유지된다.
- [ ] long-form writing / fan-out contract는 concise wording으로 남는다.
- [ ] input source enumeration은 contract 중심으로 정리된다.
- [ ] summary template/example 자산은 유지되고, 본문과의 역할 분리가 선명해진다.

### Task 3: `spec-create`, `spec-rewrite`, `spec-upgrade` 정제

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md`
- [M] `.codex/skills/spec-rewrite/SKILL.md`
- [M] `.codex/skills/spec-upgrade/SKILL.md`

**Acceptance Criteria**:
- [ ] `spec-create`의 bootstrap + 2-phase generation contract가 유지된다.
- [ ] `spec-rewrite`의 rewrite checklist/reference 연결이 유지된다.
- [ ] `spec-upgrade`의 whitepaper migration / upgrade mapping contract가 유지된다.
- [ ] 각 skill의 backup/read-only/language rule이 hard rules로 남는다.
- [ ] template/example/reference가 유지되고, 본문은 그 사용 목적과 기준만 더 간결하게 설명한다.

**Technical Notes**:
- template/reference 파일은 유지하되, 본문에서 repeated section commentary는 줄인다.
- `spec-create`는 directory structure 설명을 표/짧은 bullet로 압축한다.

### Task 4: `pr-spec-patch`, `pr-review` 정제

**Target Files**:
- [M] `.codex/skills/pr-spec-patch/SKILL.md`
- [M] `.codex/skills/pr-review/SKILL.md`

**Acceptance Criteria**:
- [ ] `pr-spec-patch`의 initial/update mode와 spec-update-todo 호환 출력이 유지된다.
- [ ] `pr-review`의 verdict taxonomy와 evidence-first review contract가 유지된다.
- [ ] GitHub/PR inspection 관련 reference/example 자산은 유지된다.
- [ ] repetitive context-management prose는 제거된다.

### Task 5: `discussion`, `guide-create`, `spec-snapshot` 정제

**Target Files**:
- [M] `.codex/skills/discussion/SKILL.md`
- [M] `.codex/skills/guide-create/SKILL.md`
- [M] `.codex/skills/spec-snapshot/SKILL.md`

**Acceptance Criteria**:
- [ ] `discussion`의 iterative loop와 저장 artifact contract가 유지된다.
- [ ] `guide-create`의 required guide sections와 output structure가 유지된다.
- [ ] `spec-snapshot`의 번역/타임스탬프 규칙이 유지된다.
- [ ] supporting skill 3개 모두 20~30% 수준의 경량화가 이루어진다.
- [ ] `guide-create`의 template/example 자산은 유지되고, 본문은 guide 생성 기준을 더 선명하게 설명한다.

### Task 6: Verification

**Acceptance Criteria**:
- [ ] 각 skill이 AC / Hard Rules / Process / Output Contract를 갖추는지 확인한다.
- [ ] references/examples/skill.json이 보존되었는지 확인한다.
- [ ] wrapper-backed skill이 실수로 수정 범위에 포함되지 않았는지 확인한다.
- [ ] line count total이 목표 범위(3,700줄 이하)에 들어오는지 확인한다.
- [ ] 각 skill에 대해 “본문만 읽어도 목표/AC/핵심 계약을 이해할 수 있는지”를 smoke check 한다.
- [ ] 각 skill의 reference/example asset이 여전히 문서 품질 향상에 유효한지 확인한다.

### Task 7: Spec sync follow-up

**Target Files**:
- [M] `_sdd/spec/main.md`

**Acceptance Criteria**:
- [ ] 필요 시 `SKILL.md / Agent 정의 공통 구조`와 `Identified Issues & Improvements`에 Codex full-skill AC-first policy를 반영한다.
- [ ] wrapper-backed custom agent layer와 full skill layer의 역할 분리가 스펙에서 더 명확해진다.

## Parallelization Notes

- Phase 1 pilot 완료 전에는 전면 병렬 적용하지 않는다.
- Pilot에서 compression pattern이 안정화되면 아래 묶음은 병렬 가능하다.
  - `spec-create`, `spec-rewrite`, `spec-upgrade`
  - `pr-spec-patch`, `pr-review`
  - `discussion`, `guide-create`, `spec-snapshot`

## Risks

1. `sdd-autopilot`를 과도하게 줄이면 Codex 고유 실행 계약이 사라질 수 있다.
2. `spec-summary`와 `guide-create`는 long-form writing contract를 너무 많이 덜어내면 출력 품질이 흔들릴 수 있다.
3. references/examples를 유지하더라도, 본문이 목표와 AC를 충분히 설명하지 못하면 회귀가 발생할 수 있다.

## Next Steps

1. 이 draft를 검토하고 scope를 확정한다.
2. `/implementation`으로 Pilot 2개 (`sdd-autopilot`, `spec-summary`)부터 적용한다.
3. Pilot 검증 후 remaining full skill에 패턴을 확장한다.
4. 완료 후 필요하면 `/spec-update-done`으로 `_sdd/spec/main.md`를 동기화한다.
