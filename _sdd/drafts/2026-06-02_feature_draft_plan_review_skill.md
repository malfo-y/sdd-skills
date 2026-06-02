# Feature Draft: plan-review 스킬 및 agent 추가

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

`plan-review`를 구현 전 계획 품질 게이트로 추가한다. 이 스킬/agent는 implementation plan 또는 feature draft Part 2를 읽고, 계획이 과잉 구현·불필요한 새 파일·단일 사용처 추상화·약한 검증 기준을 유도하는지 findings-first로 검토한다.

주요 근거:

- `_sdd/discussion/2026-06-02_discussion_plan_review_skill.md`에서 합의한 독립 review-only 설계, findings-first 출력, Critical/High 차단, 작업 표면 중심 루브릭, `_sdd/implementation` 저장 경로, 6개 smell 체크.
- `_sdd/spec/main.md`의 skill layer / agent layer 분리와 `.claude` / `.codex` dual bundle 유지 원칙.
- `_sdd/spec/components.md`의 wrapper -> agent 패턴과 Delivery & Review component 구조.
- 외부 `CLAUDE.md` 원칙: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution. 특히 “every changed line should trace directly to the user's request” 기준을 plan-review의 Scope Creep / New File Justification smell로 변환한다.

## Scope Delta

**In scope**:

- `.codex`에 `plan-review` skill wrapper와 custom agent를 추가한다.
- `.claude`에 `plan-review` skill wrapper와 agent를 추가한다.
- 양 플랫폼에서 `SKILL.md`와 agent 본문은 Mirror Notice를 제외하고 같은 실행 계약을 유지한다.
- `skill.json`은 각 플랫폼의 skill registry가 `plan-review`를 발견할 수 있게 생성한다.
- Codex agent registry README와 global supporting spec surface에 `plan-review`를 compact하게 추가한다.
- `plan-review` output contract는 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`로 둔다.

**Out of scope**:

- `sdd-autopilot`에 자동 plan-review gate를 즉시 삽입하지 않는다.
- `feature-draft` 또는 `implementation-plan` 생성 로직을 수정하지 않는다.
- 기존 `implementation-review` 동작을 변경하지 않는다.
- top-level `_sdd/logs` 디렉토리를 신설하지 않는다.
- plan-review가 plan을 직접 수정하거나 rewrite하지 않는다. 제안은 리포트에만 남긴다.

**Guardrail delta**:

- 새 스킬은 review-only다. `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/*_implementation_plan_*.md`를 직접 수정하지 않는다.
- Critical/High findings만 구현 전 blocker로 분류한다. Medium/Low는 권고로 둔다.
- recommendations도 Minimum-Code 원칙을 따라야 하며, 사변적 “future-proof / configurable / extensible” 권고를 금지한다.
- `.codex`와 `.claude`의 skill/agent mirror drift를 방지하기 위해 생성 task는 플랫폼별 파일이 아니라 mirror pair 단위로 묶는다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | `plan-review` skill/agent는 implementation plan 또는 feature draft Part 2를 review-only로 감사한다. | 구현 전 계획의 과잉 설계와 sloppy code 유도 요인을 구현 전에 드러내기 위함 |
| C2 | Add | `plan-review` 리포트는 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`에 findings-first로 저장한다. | implementation plan 검토 산출물이므로 기존 `_sdd/implementation` 흐름과 맞춘다 |
| C3 | Add | 리뷰 루브릭은 6개 smell 체크(Scope Creep, New File Justification, Single-use Abstraction, Task Boundary Drift, DRY Risk, Verification Weakness)를 사용한다. | KISS/YAGNI/DRY/CLAUDE.md 원칙을 실행 가능한 plan smell로 변환한다 |
| C4 | Add | severity는 Critical / High / Medium / Low이며, Critical/High만 implementation blocker로 명시한다. | plan-review 자체가 과잉 절차가 되지 않도록 게이트 강도를 보수적으로 유지한다 |
| C5 | Add | `plan-review`는 Plan Source Tier를 판별한다: Tier 1 plan 존재, Tier 2 feature draft Part 2 존재, Tier 3 spec/discussion 기반 제한 리뷰. | `implementation-review`의 graceful degradation 패턴을 계획 리뷰 도메인에 맞춘다 |
| C6 | Add | `.codex`와 `.claude`의 `plan-review` skill/agent pair는 Mirror Notice를 제외하고 동일 실행 계약을 공유한다. | direct invocation과 agent invocation 간 의미 drift를 방지한다 |
| C7 | Add | `plan-review` findings는 각 finding에 smell category, severity, evidence, affected plan surface, principle link, recommended plan change를 포함한다. | 구현자가 계획의 어느 부분을 어떻게 고칠지 바로 알 수 있게 한다 |
| I1 | Add | plan-review는 계획/스펙/코드를 읽을 수 있지만 plan/spec/code를 수정하지 않는다. | review-only 책임 경계 유지 |
| I2 | Add | New File Justification smell은 `[C]` Target File마다 “왜 기존 파일 수정이 아니라 새 파일인가” 근거를 요구한다. | 간단한 기능에도 새 설정/헬퍼/레이어를 만드는 agentic coding 실패를 줄인다 |
| I3 | Add | plan-review recommendations는 발견된 실제 smell 또는 측정된 위험에 직접 대응해야 한다. | 리뷰 권고 자체가 YAGNI 위반이 되는 것을 막는다 |

## Touchpoints

| 파일 | 변경 영역 | 이유 |
|------|----------|------|
| `.codex/skills/plan-review/SKILL.md` | 신규 skill wrapper / full contract | Codex 사용자가 직접 `plan-review`를 호출할 수 있게 한다 |
| `.codex/skills/plan-review/skill.json` | 신규 skill metadata | Codex skill discovery에 필요 |
| `.codex/agents/plan-review.toml` | 신규 custom agent | Codex orchestrator나 다른 skill이 `spawn_agent(agent_type="plan_review")`로 호출할 실행 단위 |
| `.codex/agents/README.md` | Agent Set / Inline Writing 목록 | 신규 Codex custom agent registry 반영 |
| `.claude/skills/plan-review/SKILL.md` | 신규 skill wrapper / full contract | Claude 사용자가 직접 `plan-review`를 호출할 수 있게 한다 |
| `.claude/skills/plan-review/skill.json` | 신규 skill metadata | Claude skill discovery에 필요 |
| `.claude/agents/plan-review.md` | 신규 agent | Claude agents/skills가 `Agent(subagent_type=plan-review)`로 호출할 실행 단위 |
| `_sdd/spec/components.md` | Delivery & Review table | `plan-review` component reference와 primary source 추가 |
| `_sdd/spec/usage-guide.md` | Scenario 2 수동 workflow | implementation 전에 선택적 plan-review를 넣는 expected result 추가 |
| `_sdd/spec/main.md` | Guardrails / key decisions compact note | implementation 전 계획 품질 게이트가 review-only로 추가됐음을 thin core에 반영 |

## Implementation Plan

1. Codex surface를 만든다: `.codex/skills/plan-review/`, `.codex/agents/plan-review.toml`, `.codex/agents/README.md` registry row.
2. Claude surface를 만든다: `.claude/skills/plan-review/`, `.claude/agents/plan-review.md`.
3. Supporting spec surface를 compact하게 갱신한다: `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/main.md`.
4. Mirror parity와 artifact contract를 검증한다: skill.json metadata, SKILL.md/agent mirror notices, output path, 6-smell rubric, blocker policy, review-only guardrails.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | review | plan-review Hard Rules에 review-only, no direct plan/spec/code mutation, input source tier가 명시돼 있는지 확인 |
| V2 | C2, C7 | review | Review Output template에 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`, findings-first, finding fields가 있는지 확인 |
| V3 | C3, I2 | review | 6개 smell rubric과 `[C]` Target File의 New File Justification 기준이 명시돼 있는지 확인 |
| V4 | C4, I3 | review | Critical/High blocker policy와 recommendations min-code rule이 명시돼 있는지 확인 |
| V5 | C5 | review | Tier 1/2/3 source selection과 stale/limited-review handling이 있는지 확인 |
| V6 | C6 | diff/review | `.codex` SKILL.md ↔ `.codex` agent instructions, `.claude` SKILL.md ↔ `.claude` agent body가 Mirror Notice/frontmatter 차이 외 같은 계약인지 확인 |
| V7 | C6 | review | `.codex/skills/plan-review/skill.json`, `.claude/skills/plan-review/skill.json`, `.codex/agents/README.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/main.md`가 새 surface를 가리키는지 확인 |

## Risks / Open Questions

### Q1. plan-review를 sdd-autopilot에 자동 게이트로 넣을지

- **Decision taken**: 이번 구현에서는 수동 호출 가능한 review-only skill/agent로만 추가한다.
- **Alternatives considered**:
  - autopilot Phase 2에서 feature-draft 또는 implementation-plan 직후 자동 실행. 기각: pipeline semantics, retry policy, blocker handling까지 바뀌어 변경 범위가 커진다.
  - implementation-plan의 내부 self-check로만 흡수. 기각: 독립 review surface가 없어 사용자가 계획만 따로 감사하기 어렵다.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. `_sdd/spec/main.md`까지 수정할지

- **Decision taken**: compact guardrail/key decision 한두 줄만 반영한다.
- **Alternatives considered**:
  - components/usage-guide만 수정. 기각: skill/agent layer에 review-only planning gate가 생긴 것은 repo-wide workflow guardrail에 해당한다.
  - main.md에 상세 루브릭까지 반영. 기각: thin global spec이 루브릭 inventory로 비대해진다.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q3. plan-review가 feature draft Part 1 temporary spec도 평가할지

- **Decision taken**: Part 1은 context로 읽되, 직접 리뷰 대상은 Part 2 implementation plan 또는 implementation plan artifact로 제한한다.
- **Alternatives considered**:
  - Part 1의 Contract/Invariant Delta까지 full spec-review처럼 감사. 기각: `spec-review`와 책임이 겹친다.
  - Part 1을 완전히 무시. 기각: Part 2의 scope/validation 근거를 확인하려면 C/I/V linkage context가 필요하다.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. severity blocker policy를 Medium까지 확장할지

- **Decision taken**: Critical/High만 blocker로 둔다. Medium/Low는 권고.
- **Alternatives considered**:
  - Medium까지 차단. 기각: 작은 작업에서 review 자체가 YAGNI 위반으로 부풀 수 있다.
  - blocker 없이 advisory only. 기각: 명백히 잘못된 Target Files나 검증 불가 계획을 구현 전에 멈출 수 없다.
- **Confidence**: HIGH
- **User confirmation needed**: No
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이 plan은 `_sdd/discussion/2026-06-02_discussion_plan_review_skill.md`의 합의를 실행 가능한 파일 작업으로 전개한다. `plan-review`는 implementation plan을 직접 수정하지 않는 review-only gate이며, 목표는 구현 전에 KISS / YAGNI / DRY / CLAUDE.md 원칙 위반을 계획 smell로 드러내는 것이다.

`plan-review`의 기본 입력은 `_sdd/implementation/<date>_implementation_plan_<slug>.md`다. 해당 파일이 없으면 `_sdd/drafts/<date>_feature_draft_<slug>.md`의 Part 2를 리뷰할 수 있고, 둘 다 없으면 spec/discussion 기반 제한 리뷰로 degrade한다. 이 Tier 개념은 `implementation-review`의 graceful degradation을 계획 리뷰 도메인에 맞춘 것이다.

## Scope

### In Scope

- Codex `plan-review` skill wrapper, skill metadata, custom agent 생성.
- Claude `plan-review` skill wrapper, skill metadata, agent 생성.
- Codex agent registry README와 global supporting spec surface에 새 component 추가.
- `plan-review` 실행 계약에 6-smell rubric, findings-first output, Critical/High blocker policy, review-only hard rules, mirror notice 포함.

### Out of Scope

- autopilot 자동 게이트 삽입.
- 기존 `feature-draft`, `implementation-plan`, `implementation-review` 본문 수정.
- plan-review가 plan을 자동 수정하는 기능.
- plan-review 전용 scoring dashboard나 별도 `_sdd/logs` 디렉토리.

## Components

| Component | Role | Primary Files |
|-----------|------|---------------|
| Codex plan-review skill | 사용자 직접 호출 entrypoint | `.codex/skills/plan-review/SKILL.md`, `.codex/skills/plan-review/skill.json` |
| Codex plan-review agent | orchestrator/spawn execution unit | `.codex/agents/plan-review.toml`, `.codex/agents/README.md` |
| Claude plan-review skill | 사용자 직접 호출 entrypoint | `.claude/skills/plan-review/SKILL.md`, `.claude/skills/plan-review/skill.json` |
| Claude plan-review agent | Claude Agent execution unit | `.claude/agents/plan-review.md` |
| Global supporting spec | component and usage navigation | `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md` |

## Contract/Invariant Delta Coverage

| Target | Planned Tasks | Validation Link |
|--------|---------------|-----------------|
| C1, C2, C3, C4, C5, C7, I1, I2, I3 | T1, T2 | V1, V2, V3, V4, V5 |
| C6 | T1, T2, T4 | V6, V7 |
| C2, C6 | T3 | V7 |

## Implementation Phases

### Phase 1: plan-review 실행 계약과 양 플랫폼 surface 생성

**Goal**: `plan-review`의 core contract를 작성하고 `.codex` / `.claude` 양쪽 skill+agent mirror를 생성한다.

**Tasks**: T1, T2

**Task Set / Dependency Closure**: T1과 T2는 서로 다른 플랫폼 파일을 생성하지만 동일 contract를 공유한다. T1에서 contract 문구를 먼저 확정하고 T2가 같은 contract를 Claude frontmatter/tool convention에 맞춰 반영한다. 두 task는 의미적으로 같은 계약을 공유하므로 병렬보다 순차 또는 같은 작업자가 처리하는 것이 mirror drift를 줄인다.

**Validation Focus**: V1, V2, V3, V4, V5, V6

**Exit Criteria**:

- [ ] Codex와 Claude의 `plan-review` skill/agent가 모두 존재한다.
- [ ] 양 플랫폼의 contract가 6-smell rubric, findings-first output, blocker policy, review-only rule을 모두 포함한다.
- [ ] Mirror Notice가 각 skill/agent에 들어 있고, 한쪽 수정 시 다른 쪽도 함께 수정해야 한다고 명시한다.

**Carry-over Policy**:

- Default: `None` (`critical/high/medium` block)
- Allowed Exception: 없음.

**Checkpoint**: false

### Phase 2: registry와 global supporting surface 반영

**Goal**: 새 `plan-review`가 repo navigation과 사용 흐름에서 발견 가능하도록 최소 supporting surface만 갱신한다.

**Tasks**: T3, T4

**Task Set / Dependency Closure**: T3은 Codex local registry 업데이트, T4는 global spec supporting surface 업데이트다. T4는 T1/T2에서 확정된 contract 명칭과 output path를 참조해야 하므로 Phase 1 이후 진행한다.

**Validation Focus**: V7

**Exit Criteria**:

- [ ] `.codex/agents/README.md`의 Agent Set 또는 Inline Writing 목록에 `plan_review`가 반영된다.
- [ ] `_sdd/spec/components.md`의 Delivery & Review table에 `plan-review`가 compact하게 추가된다.
- [ ] `_sdd/spec/usage-guide.md`가 implementation 전 선택적 `/plan-review` 흐름을 보여준다.
- [ ] `_sdd/spec/main.md`는 thin spec 원칙을 유지하고 세부 루브릭을 복사하지 않는다.

**Carry-over Policy**:

- Default: `None` (`critical/high/medium` block)
- Allowed Exception: 없음.

**Checkpoint**: true
**Checkpoint Reason**: Phase 2가 마지막 phase이며, registry/spec navigation까지 닫혀야 실제 사용자가 새 skill을 찾을 수 있다.

## Task Details

### Task T1: Codex plan-review skill과 custom agent 생성

**Component**: Codex plan-review surface
**Priority**: P0
**Type**: Feature

**Description**: Codex용 `plan-review` skill wrapper와 custom agent를 만든다. `SKILL.md`와 `.toml`의 `developer_instructions`는 같은 실행 계약을 공유해야 하며, Codex agent는 `spawn_agent(agent_type="plan_review")`로 호출 가능한 snake_case 이름을 사용한다.

**Non-Goals**: 기존 Codex skill/agent 본문을 수정하지 않는다. autopilot 호출 흐름도 변경하지 않는다.

**Acceptance Criteria**:

- [ ] `.codex/skills/plan-review/SKILL.md`가 생성되고 frontmatter `name: plan-review`, description, version을 포함한다.
- [ ] `.codex/skills/plan-review/skill.json`이 생성되고 `name`, `description`, `instruction_file`, `version`을 포함한다.
- [ ] `.codex/agents/plan-review.toml`이 생성되고 `name = "plan_review"`, spawn용 description, `developer_instructions`를 포함한다.
- [ ] `SKILL.md`와 `developer_instructions`는 Review Output, Hard Rules, Tier Selection, 6-smell rubric, severity/blocker policy, Process, Error Handling, Integration, Final Check를 포함한다.
- [ ] Output path는 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`로 명시한다.
- [ ] plan-review는 plan/spec/code를 직접 수정하지 않는 review-only agent임을 Hard Rules에 명시한다.
- [ ] Recommendations Min-Code rule이 포함된다.
- [ ] Mirror Notice가 `.codex/skills/plan-review/SKILL.md`와 `.codex/agents/plan-review.toml` 양쪽에 포함된다.

**Target Files**:

- [C] `.codex/skills/plan-review/SKILL.md` -- Codex 사용자 직접 호출용 skill contract. 기존 skill 수정으로 대체할 수 없는 새 entrypoint이므로 새 파일이 필요하다.
- [C] `.codex/skills/plan-review/skill.json` -- Codex skill discovery metadata. 새 skill directory의 필수 companion file이다.
- [C] `.codex/agents/plan-review.toml` -- Codex custom agent spawn target. 사용자-facing skill과 reusable agent를 분리하는 repo convention 때문에 새 agent 파일이 필요하다.

**Technical Notes**: Covers C1, C2, C3, C4, C5, C6, C7, I1, I2, I3. Validated by V1-V6. `plan_review` snake_case naming은 `.codex/agents/README.md`의 Codex agent naming rule에 따른다.

**Dependencies**: 없음.

### Task T2: Claude plan-review skill과 agent 생성

**Component**: Claude plan-review surface
**Priority**: P0
**Type**: Feature

**Description**: Claude용 `plan-review` skill wrapper와 agent를 만든다. T1에서 확정한 contract를 Claude frontmatter, tool list, agent invocation convention에 맞춰 반영하되 의미는 동일하게 유지한다.

**Non-Goals**: Claude 전용 추가 기능을 넣지 않는다. `second-opinion` 같은 Claude-only skill과 통합하지 않는다.

**Acceptance Criteria**:

- [ ] `.claude/skills/plan-review/SKILL.md`가 생성되고 frontmatter `name: plan-review`, description, version을 포함한다.
- [ ] `.claude/skills/plan-review/skill.json`이 생성되고 `name`, `description`, `instruction_file`, `version`을 포함한다.
- [ ] `.claude/agents/plan-review.md`가 생성되고 frontmatter `name: plan-review`, internal agent description, tools, model을 포함한다.
- [ ] Claude SKILL.md와 agent body는 Codex contract와 의미상 동일하며, 플랫폼별 invocation wording만 다르다.
- [ ] Claude agent tool list는 review-only에 필요한 읽기/검색 중심 도구를 사용하고, plan/spec/code 수정 도구는 넣지 않는다.
- [ ] Mirror Notice가 `.claude/skills/plan-review/SKILL.md`와 `.claude/agents/plan-review.md` 양쪽에 포함된다.

**Target Files**:

- [C] `.claude/skills/plan-review/SKILL.md` -- Claude 사용자 직접 호출용 skill contract. 새 entrypoint라 새 파일이 필요하다.
- [C] `.claude/skills/plan-review/skill.json` -- Claude skill discovery metadata. 새 skill directory의 필수 companion file이다.
- [C] `.claude/agents/plan-review.md` -- Claude reusable agent. wrapper-backed skill/agent split convention 때문에 새 agent 파일이 필요하다.

**Technical Notes**: Covers C1, C2, C3, C4, C5, C6, C7, I1, I2, I3. Validated by V1-V6. Claude agent invocation wording은 existing `.claude/agents/implementation-review.md` 패턴을 따른다.

**Dependencies**: T1의 contract wording 확정 이후 진행하면 mirror drift가 줄어든다.

### Task T3: Codex agent registry 갱신

**Component**: Codex agent registry
**Priority**: P1
**Type**: Documentation

**Description**: `.codex/agents/README.md`에 `plan_review`를 추가해 Codex custom agent set과 inline writing 대상 여부를 반영한다. 이 파일은 Codex agent naming, ownership, invocation convention을 설명하는 local registry이므로 새 custom agent가 생기면 갱신되어야 한다.

**Acceptance Criteria**:

- [ ] Agent Set에 `plan_review`가 추가된다.
- [ ] Inline Writing 목록에 `plan_review`가 추가된다. plan-review는 findings-first 리포트를 생성하는 장문 review artifact이므로 `implementation_review`와 같은 producer-owned inline writing 패턴을 따른다.
- [ ] 기존 Codex invocation contract 문구는 변경하지 않는다.

**Target Files**:

- [M] `.codex/agents/README.md` -- 신규 Codex custom agent registry 반영.

**Technical Notes**: Covers C6. Validated by V7.

**Dependencies**: T1.

### Task T4: global supporting spec에 plan-review 추가

**Component**: global spec supporting surface
**Priority**: P1
**Type**: Documentation

**Description**: `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`에 `plan-review`를 compact하게 반영한다. 세부 루브릭은 새 SKILL.md에 두고, global spec에는 workflow에서의 위치와 review-only guardrail만 남긴다.

**Non-Goals**: `_sdd/spec/DECISION_LOG.md`와 `_sdd/spec/logs/changelog.md`는 본 feature draft 단계에서는 수정하지 않는다. 실제 구현 완료 후 `spec-update-done`에서 처리한다.

**Acceptance Criteria**:

- [ ] `_sdd/spec/components.md` Delivery & Review table에 `plan-review` row가 추가되고 primary source가 `.claude`/`.codex` skill+agent를 가리킨다.
- [ ] `_sdd/spec/usage-guide.md` Scenario 2 수동 workflow에 optional `/plan-review`가 implementation 전 위치로 추가된다.
- [ ] `_sdd/spec/main.md` Guardrails 또는 key decisions에 implementation 전 plan review-only gate를 compact하게 반영한다.
- [ ] global spec 본문에 6-smell rubric 전체를 복사하지 않는다.

**Target Files**:

- [M] `_sdd/spec/main.md` -- repo-wide workflow guardrail에 plan-review 추가를 compact하게 반영.
- [M] `_sdd/spec/components.md` -- component reference와 primary source 추가.
- [M] `_sdd/spec/usage-guide.md` -- manual workflow usage path 업데이트.

**Technical Notes**: Covers C6. Validated by V7. `_sdd/spec/main.md`는 thin global spec이므로 세부 smell table은 복사하지 않는다.

**Dependencies**: T1, T2.

## Parallel Execution Summary

- T1과 T2는 플랫폼별 파일이 다르지만 같은 contract를 공유하므로 완전 병렬보다 T1 contract 확정 후 T2 mirror 작성이 안전하다.
- T3은 T1 이후 바로 가능하다.
- T4는 T1/T2 이후 가능하다. spec surface가 primary source 경로를 정확히 가리켜야 하기 때문이다.
- 동일 파일 충돌은 없다. 의미적 충돌은 T1/T2 contract drift이며, dependency로 제어한다.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Codex/Claude contract drift | 같은 이름의 skill이 플랫폼별로 다른 판단을 내릴 수 있음 | T1 contract를 기준으로 T2를 mirror하고, Mirror Notice와 diff/review 검증을 수행 |
| plan-review 자체가 절차 과잉이 됨 | 작은 작업에서도 implementation이 지연됨 | Critical/High만 blocker, Medium/Low는 advisory로 제한 |
| global spec 비대화 | thin spec 원칙 훼손 | main/components/usage에는 위치와 목적만 쓰고 6-smell 세부는 SKILL.md에 둠 |
| review-only 경계 침해 | plan-review가 plan rewrite skill로 변질 | Hard Rules에 no mutation 명시, recommendations는 리포트에만 기록 |

## Open Questions

### Q1. plan-review를 autopilot 자동 게이트로 넣을지

- **Decision taken**: 이번 구현에서는 제외하고 수동 호출 가능한 skill/agent만 만든다.
- **Alternatives considered**: autopilot Phase 2 자동 실행은 pipeline semantics 변경이 커서 후속 feature로 분리한다.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. implementation-plan이 plan-review를 자체 후속으로 권장할지

- **Decision taken**: 이번 구현에서는 기존 implementation-plan 본문을 수정하지 않는다.
- **Alternatives considered**: implementation-plan Integration 섹션에 plan-review를 추가할 수 있으나, 기존 스킬 수정은 이번 Target Files를 늘리고 mirror 작업을 추가한다.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

## Self-Containment Check

- 검토 섹션 수: 10
- Pass 1 발견 갭 및 보완:
  - `Overview`: `plan-review` 입력 tier가 외부 discussion에만 의존해 보이는 갭이 있어, Tier 1/2/3 정의를 본문에 재진술했다.
  - `Task T3`: 왜 `.codex/agents/README.md`가 필요한지 bare path처럼 보이는 갭이 있어, “Codex custom agent set과 inline writing registry” 목적을 inline으로 설명했다.
  - `Task T4`: `_sdd/spec/main.md` 수정 근거가 과해 보이는 갭이 있어, thin global spec에는 compact guardrail만 반영하고 6-smell table은 복사하지 않는다고 명시했다.
- Pass 2 발견 갭 및 보완:
  - `Scope`: plan-review가 plan을 수정하는지 모호한 갭이 있어 Out of Scope와 Hard Rule delta에 “plan 직접 수정 금지”를 반복 명시했다.
  - `Parallel Execution Summary`: T1/T2를 병렬로 처리해도 되는지 애매한 갭이 있어, 파일은 disjoint지만 contract drift 위험 때문에 순차/동일 작업자 처리를 권장한다고 보완했다.
  - `Task T2`: Claude agent tool list가 왜 write/edit을 제외해야 하는지 빠져 있어 review-only 도구 구성을 AC에 추가했다.
- 보완 완료: Yes
