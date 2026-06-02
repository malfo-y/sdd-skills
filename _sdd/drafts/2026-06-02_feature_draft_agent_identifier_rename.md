# Feature Draft: agent 식별자·파일명에 `-agent` 접미사 도입

> 근거 토론: `_sdd/discussion/2026-06-02_discussion_agent_file_naming_convention.md` (범위 C, codex 포함, 분기 규칙, pilot-then-batch까지 합의됨)

# Part 1: Temporary Spec Draft

## Change Summary

agent의 canonical 식별자(`name` 필드)와 파일명에 `-agent`/`_agent` 접미사를 도입한다. 목적은 **skill과 agent가 같은 이름(`feature-draft`)을 공유해 생기는 호출 단계 모호함을 제거**하고, 파일명만으로 agent임이 드러나게 하는 것이다.

- claude: 전부 kebab — `name: feature-draft-agent`, 파일 `feature-draft-agent.md`, 호출 `subagent_type=feature-draft-agent`
- codex: 파일 kebab + 내부 snake — 파일 `feature-draft-agent.toml`, `name = "feature_draft_agent"`, 호출 `spawn_agent(agent_type="feature_draft_agent")`

핵심 제약(분기 규칙): **호출 식별자·파일 경로만** 바꾸고, **skill 이름·step 개념 산문·draft 산출물 파일명은 `feature-draft` 유지**한다. 이 칼선이 곧 skill↔agent 구분이라는 목적 자체다.

## Scope Delta

**In-scope (live 계약만):**
- `.claude/agents/*.md` 10개: 파일 rename + `name:` 필드 + 자기 `description`의 invocation 문자열
- `.codex/agents/*.toml` 10개: 파일 rename + `name =` 필드 + 자기 `description`의 invocation 문자열
- `.claude/skills/*/SKILL.md`의 agent 경로를 가리키는 Mirror/Sync Notice
- `.codex/skills/*/SKILL.md`의 agent 경로를 가리키는 Mirror Notice
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`: 허용 subagent_type 목록 + model 매핑 테이블 (호출값 행만)
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`: 허용 agent_type 목록 (호출값 행만)
- `.codex/skills/sdd-autopilot/references/execution-profile-policy.md`: agent_type 키 테이블
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`: `**Claude subagent_type**:` 예시 값
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`: `**Codex agent_type**:` 예시 값 + 프로파일 매핑 예시

**Out-of-scope (의도적 보존):**
- `.claude/skills/<slug>/`, `.codex/skills/<slug>/` **skill 폴더명**과 skill `name:` (변경 안 함 — 모호함 해소의 대상이 아니라 비교 기준)
- step/개념을 가리키는 산문 (`feature-draft는 temporary spec 7섹션을 만든다` 류)
- `_sdd/drafts/..._feature_draft_<slug>.md` 등 **산출물 파일명** 토큰
- `_sdd/pipeline/*` 과거 리포트·오케스트레이터 (날짜 박힌 스냅샷으로 보존)
- agent→skill 방향 Mirror Notice가 가리키는 **skill 경로**(`.claude/skills/feature-draft/SKILL.md`) — skill은 안 바뀌므로 경로 불변

**Guardrail delta:**
- blind 전역 치환 금지. 모든 치환은 컨텍스트 앵커(`subagent_type=`, `agent_type="`, `name:`/`name =`, agent 디렉토리 경로)에 한정하고, longest-match 우선(`implementation-review`/`implementation-plan`을 `implementation`보다 먼저)으로 처리한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | agent canonical 식별자 = `<slug>-agent`(claude) / `<slug>_agent`(codex) | skill 이름과 충돌하던 agent 식별자를 분리 |
| C2 | Modify | agent 파일명 = `<slug>-agent.md`(claude) / `<slug>-agent.toml`(codex) | flat-view에서 agent임이 파일명에 드러남 |
| I1 | Add | 모든 `subagent_type`/`agent_type` 호출값은 대응하는 agent `name`과 정확히 일치해야 한다 (dangling reference 0) | 누락 호출처 = 런타임 silent fail 방지 |
| I2 | Add | skill 폴더명·skill `name`·step 개념 산문·draft 산출물 파일명은 `<slug>`(접미사 없음)를 유지한다 | 분기 규칙 — skill↔agent 구분 경계 보존 |
| I3 | Add | claude↔codex Mirror는 **본문(developer_instructions) 계약** 동기이며, 식별자 문자열은 각 진영 컨벤션(kebab/snake)에 따라 의도적으로 다르다 | 한쪽만 바꿔도 본문 대칭은 유지된다는 사실 명문화 |

## Touchpoints

> 모두 현재 코드 census(2026-06-02)로 재확인함. agent별 독립 파일 vs 전 agent 공유 파일을 구분한다.

**A. agent별 독립 (agent마다 병렬 가능):**
- `.claude/agents/<slug>.md` — rename, `name:`, 자기 description의 `Agent(subagent_type=<slug>)`
- `.codex/agents/<slug>.toml` — rename, `name =`, 자기 description의 `spawn_agent(agent_type="<snake>")`
- `.claude/skills/<slug>/SKILL.md` — agent 경로 가리키는 Mirror/Sync Notice 1줄
- `.codex/skills/<slug>/SKILL.md` — agent 경로 가리키는 Mirror Notice 1줄

**A'. agent 파일 *내부*에 박힌 agent-파일 경로 참조 (제3 surface — 누락 주의):**
- `.claude/agents/spec-review.md` — 본문 Mirror Notice가 `.codex/agents/spec-review.toml`(rename 대상)을 참조. spec-review는 `claude agent ↔ claude skill ↔ codex agent` **3-way** 참조이므로 세 파일 모두에서 agent 경로를 갱신한다.
- `.claude/agents/implementation-plan.md` — Sync Notice가 자기 경로 `.claude/agents/implementation-plan.md`를 본문에 기재 → rename 시 함께 갱신.
- 이 surface는 호출값도 skill 파일 Notice도 아니어서 **반드시 경로-레벨 grep(V5)로 검증**한다.

**B. 전 agent 공유 (파일 단위 순차 편집, agent별 병렬 불가):**
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` — 허용목록(L41-48 중 호출값) + model 테이블(L65-72)
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` — 허용목록(L66-73)
- `.codex/skills/sdd-autopilot/references/execution-profile-policy.md` — agent_type 키 테이블(L12-20)
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` — `**Claude subagent_type**:` 값(L39,50,88,155,168,180,192,247)
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` — `**Codex agent_type**:` 값 + 프로파일 매핑(L30,41,49,60,100,129,158,169-173 등)

**C. 변경 금지 확인 지점 (negative touchpoints):**
- `.claude/skills/<slug>/`·`.codex/skills/<slug>/` 폴더명
- orchestrator-contract의 개념 산문(claude L88-89,176 / codex L91-92)
- agent 파일 내부의 skill 경로 참조(skill 미변경)

## Implementation Plan

1. **Census Lock**: replacement map(개념 → claude name/file, codex name/file)을 확정 표로 고정. implementation의 source of truth.
2. **Pilot (`feature-draft` 1개)**: A·B·C 모든 카테고리를 end-to-end로 적용 → 검증 게이트 통과 → 패턴 확정. 실패 시 이 지점에서 브랜치 롤백.
3. **Batch (나머지 9개)**: 검증된 패턴으로 (B1) agent별 독립 파일 일괄 + (B2) 공유 파일 라인 일괄.
4. **Final Verification**: 전역 검증 게이트 + negative 검증.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2 | test (grep) | `.claude/agents/`·`.codex/agents/`에 10개씩 `<slug>-agent.{md,toml}` 존재 + 각 `name`이 접미사 포함 |
| V2 | I1 | test (grep) | live 영역에서 접미사 없는 잔여 호출값(`subagent_type=<slug>` / `agent_type="<snake>"`) 0건 AND 모든 호출값에 대응 `name` 존재 (dangling 0) |
| V3 | I2 | review (grep) | skill 폴더명·draft 산출물 파일명·개념 산문에 `-agent`가 침범하지 않음 |
| V4 | C1, I1 | smoke (executable) | pilot 단계에서 `Agent(subagent_type=feature-draft-agent)`로 trivial 작업(예: "OK"만 반환)을 **실제 1회 dispatch**해 resolve 성공을 확인. 실패·dispatch 불가 시 batch 중단하고 사용자에게 보고 |
| V5 | I1 | test (grep) | live 영역에서 옛 agent 파일 경로(`agents/<slug>.md` / `agents/<slug>.toml` 중 `-agent` 없는 것) 참조 잔여 0건. agent 파일 내부 Mirror/Sync Notice(A')와 skill 파일 Notice를 함께 커버 |

## Risks / Open Questions

### Q1. autopilot `examples/`와 `sample-orchestrator.md`를 변경 범위에 포함할지 — RESOLVED
- **Decision taken**: 포함한다. 이 예시 값들은 생성될 orchestrator가 그대로 emit하는 호출값이므로, 갱신하지 않으면 생성물이 존재하지 않는 agent를 가리켜 무효가 된다. **(2026-06-02 사용자 확인 완료: "examples도 포함하는 게 맞아")**
- **Alternatives considered**: (a) examples 제외 → 생성된 orchestrator가 stale 호출값을 emit해 런타임 실패 위험. 기각. (b) examples에 "개념일 뿐" 주석만 추가 → 실제 호출값이라 부정확. 기각.
- **Confidence**: HIGH (사용자 확인으로 승격)
- **User confirmation needed**: No (resolved)

### Q2. model/profile 매핑 테이블의 key를 호출값으로 볼지 개념으로 볼지
- **Decision taken**: 호출값으로 본다(변경). 테이블 헤더가 `subagent_type`/`agent_type`이고 orchestrator가 이 key로 모델을 선택하므로 호출 식별자다. 같은 문서의 개념 산문은 유지.
- **Alternatives considered**: 테이블도 개념으로 간주해 유지 → 허용목록(변경)과 model 테이블(유지)이 어긋나 같은 agent를 두 이름으로 부르게 됨. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. 런타임 resolution이 파일명 무관·`name` 기반이라는 가정
- **Decision taken**: `name` 기반으로 가정하고 진행하되, pilot의 V4를 **실행 가능한 실제 dispatch**(`Agent(subagent_type=feature-draft-agent)` 1회)로 확정한 뒤 batch로 넘어간다. dispatch가 환경상 불가하면 가정을 "미검증"으로 격하하고 롤백 비용(파일 20개)을 사용자에게 보고한 뒤 진행 여부를 받는다.
- **Alternatives considered**: 가정 없이 batch 선실행 → 가정이 틀리면 20개 파일 롤백. pilot 게이트가 이 위험을 차단하므로 불필요.
- **Confidence**: MEDIUM (pilot V4 실제 dispatch 성공 시 HIGH로 승격)
- **User confirmation needed**: No (단, V4 dispatch 불가 시 Yes로 전환)

### Q4. stutter (`subagent_type=feature-draft-agent`에서 "agent" 삼중 등장)
- **Decision taken**: 수용(토론에서 확정). skill↔agent 모호함 해소라는 실익과 교환.
- **Alternatives considered**: 접미사 없는 다른 구분자 — 토론 Round 2에서 기각됨.
- **Confidence**: HIGH
- **User confirmation needed**: No

---

# Part 2: Implementation Plan

## Overview

agent 식별자/파일명 rename을 **census lock → pilot(feature-draft) → 검증 게이트 → batch(나머지 9) → 최종 검증** 순으로 수행한다. 모든 치환은 컨텍스트 앵커링(blind 전역 치환 금지)이며 `git mv`로 히스토리를 보존한다. 작업은 전용 브랜치에서 진행하고 검증 게이트 통과 시에만 커밋한다.

핵심 충돌 구조: agent별 독립 파일(카테고리 A)은 agent 간 병렬 가능하지만, autopilot 공유 파일(카테고리 B)은 모든 agent 항목이 한 파일에 모여 있어 **파일 단위 순차** 편집이어야 한다. 따라서 pilot과 batch는 공유 파일을 함께 건드리므로 **phase 간 병렬 불가, 엄격 순차**다.

## Scope

In/Out-of-scope는 Part 1 `Scope Delta`와 동일. 요약: live 계약(.claude/.codex의 agents·skills·autopilot references/examples)만 변경, skill 폴더명·개념 산문·draft 산출물 파일명·`_sdd/pipeline/*`은 보존.

## Components

| Component | 역할 |
|-----------|------|
| Census Map | 개념→claude(name/file)·codex(name/file) 확정 매핑. 모든 task의 입력 |
| claude agents | `.claude/agents/*.md` rename + name + self-description |
| codex agents | `.codex/agents/*.toml` rename + name + self-description |
| skill Mirror Notices | 각 SKILL.md의 agent 경로 참조 |
| autopilot shared docs | orchestrator-contract ×2, execution-profile-policy, sample-orchestrator ×2 |
| Verification Gate | grep 기반 V1~V3 + manual V4 |

### Census Map (확정, source of truth)

| 개념(slug) | claude `name`/파일 stem | codex `name` | codex 파일 stem |
|---|---|---|---|
| feature-draft | feature-draft-agent | feature_draft_agent | feature-draft-agent |
| implementation-plan | implementation-plan-agent | implementation_plan_agent | implementation-plan-agent |
| implementation-review | implementation-review-agent | implementation_review_agent | implementation-review-agent |
| implementation | implementation-agent | implementation_agent | implementation-agent |
| investigate | investigate-agent | investigate_agent | investigate-agent |
| plan-review | plan-review-agent | plan_review_agent | plan-review-agent |
| ralph-loop-init | ralph-loop-init-agent | ralph_loop_init_agent | ralph-loop-init-agent |
| spec-review | spec-review-agent | spec_review_agent | spec-review-agent |
| spec-update-done | spec-update-done-agent | spec_update_done_agent | spec-update-done-agent |
| spec-update-todo | spec-update-todo-agent | spec_update_todo_agent | spec-update-todo-agent |

> 앵커링 주의: `implementation`은 `implementation-plan`/`implementation-review`의 substring. 치환·검증 시 backtick/quote로 감싼 **완전 토큰**만 매칭하고 longest-match를 먼저 처리한다.

## Contract/Invariant Delta Coverage

| Task | Covers |
|------|--------|
| T0 | C1, C2 (정의 고정) |
| T1 | C1, C2, I1, I3 (pilot: 전 카테고리 1-agent) |
| T2 | V1~V5 (pilot 게이트, V4 실제 dispatch + V5 경로 grep) |
| T3 | C1, C2, I1 (batch: agent별 독립 파일 + A' 경로 참조) |
| T4 | C1, I1 (batch: 공유 파일 라인) |
| T5 | V1~V3, V5, I2 (최종 검증 + 경로-레벨 + negative) |

## Implementation Phases

| Phase | Tasks | 병렬성 | Checkpoint |
|-------|-------|--------|-----------|
| Phase 0 | T0 | 단독 | false |
| Phase 1 (Pilot) | T1 → T2 | 순차 (T2는 T1 검증) | **true** (게이트) |
| Phase 2 (Batch) | T3 ∥ T4 분리 가능하나 T4는 공유파일 단일 task | T3(agent별 병렬) / T4(파일 단위 순차) | false |
| Phase 3 | T5 | 단독 | **true** |

> Phase 1의 Checkpoint=true가 핵심 롤백 지점. T2 실패 시 batch로 진행하지 않고 브랜치 폐기.

## Task Details

### Task T0: Census Map 고정 및 앵커 규칙 확정
**Component**: Census Map
**Priority**: P0
**Type**: Infrastructure

**Description**: 위 Census Map 표를 구현 기준으로 확정하고, 치환 앵커 규칙(완전 토큰 매칭, longest-match 우선, 변경 금지 negative 패턴)을 implementation이 그대로 적용할 수 있게 명문화한다. 새 코드는 없고, 후속 task의 입력 계약을 고정하는 단계다.

**Acceptance Criteria**:
- [ ] 10개 개념 각각에 claude name/file·codex name/file이 1:1로 확정됨
- [ ] 앵커 패턴 목록 확정: `subagent_type=`, `subagent_type**: \``, `agent_type="`, `agent_type**: \``, `^name:`, `^name = "`, `agents/<slug>.{md,toml}` 경로
- [ ] negative 패턴 확정: `skills/<slug>/`, `_feature_draft_`/draft 산출물 토큰, 개념 산문 라인

**Target Files**:
- [M] `_sdd/drafts/2026-06-02_feature_draft_agent_identifier_rename.md` -- Census Map/앵커 규칙을 구현 입력으로 참조 (신규 산출물 없음)

**Technical Notes**: Covers C1, C2. 산출물은 문서가 아니라 "확정된 규칙"이며 T1·T3·T4가 이를 입력으로 받는다.
**Dependencies**: 없음

---

### Task T1: Pilot — `feature-draft` 전 카테고리 end-to-end 적용
**Component**: claude agents, codex agents, skill Mirror Notices, autopilot shared docs
**Priority**: P0
**Type**: Refactor

**Description**: `feature-draft` 하나에 대해 A(독립 파일)·B(공유 파일)·C(negative) 전 카테고리를 적용한다. claude는 `feature-draft-agent`, codex 내부 name은 `feature_draft_agent`(파일은 `feature-draft-agent.toml`). `git mv`로 파일을 옮기고, `name` 필드와 각 파일 자기 description의 invocation 문자열, skill Mirror Notice 경로, autopilot 공유 문서의 feature-draft 호출값 행(허용목록·model 테이블·profile 테이블·sample-orchestrator 예시 값)만 변경한다. 개념 산문(`feature-draft는 ...`)은 건드리지 않는다.

**Non-Goals**: 나머지 9개 agent는 이 task에서 건드리지 않는다. 개념 산문·skill 폴더명·draft 산출물 토큰 변경 금지.

**Acceptance Criteria**:
- [ ] `.claude/agents/feature-draft.md` → `feature-draft-agent.md` (git mv), `name: feature-draft-agent`, description의 `subagent_type=feature-draft-agent`
- [ ] `.codex/agents/feature-draft.toml` → `feature-draft-agent.toml` (git mv), `name = "feature_draft_agent"`, description의 `agent_type="feature_draft_agent"`
- [ ] `.claude/skills/feature-draft/SKILL.md`·`.codex/skills/feature-draft/SKILL.md`의 agent 경로 Mirror Notice가 새 파일명을 가리킴
- [ ] autopilot claude: 허용목록 L41·model 테이블 L65의 `feature-draft` → `feature-draft-agent`; sample-orchestrator의 `**Claude subagent_type**: feature-draft` 예시 값
- [ ] autopilot codex: 허용목록 L66·execution-profile-policy L12·sample-orchestrator의 `**Codex agent_type**: feature_draft` 예시 값/프로파일 매핑
- [ ] 개념 산문(claude L88 등 `feature-draft는...`)은 변경되지 않음

**Target Files**:
- [M] `.claude/agents/feature-draft.md` (→ rename `feature-draft-agent.md`)
- [M] `.codex/agents/feature-draft.toml` (→ rename `feature-draft-agent.toml`)
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/execution-profile-policy.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Technical Notes**: Covers C1, C2, I1, I3. 공유 autopilot 파일(B)을 여기서 처음 건드리므로 T4(batch 공유 파일)와 **같은 파일**을 편집한다 → T1과 T4는 순차여야 하며 절대 병렬 금지.
**Dependencies**: T0

---

### Task T2: Pilot 검증 게이트
**Component**: Verification Gate
**Priority**: P0
**Type**: Test

**Description**: feature-draft에 한정해 V1~V5를 실행한다. (V1) 새 파일 2개 존재 + name 확인, (V2) live 영역에 접미사 없는 `feature-draft` 호출값 잔여 0건 + 새 호출값에 대응 name 존재, (V3) skill 폴더명·draft 토큰·개념 산문 미침범, (V4) `Agent(subagent_type=feature-draft-agent)` 실제 1회 dispatch로 resolve 확인, (V5) 옛 파일 경로 참조 잔여 0건. 하나라도 실패하면 batch로 진행하지 않고 브랜치 폐기 후 T1로 복귀.

**Acceptance Criteria**:
- [ ] V1: `feature-draft-agent.md`/`.toml` 존재, `name`이 각각 `feature-draft-agent`/`feature_draft_agent`
- [ ] V2: `grep`으로 live 영역 접미사-없는 feature-draft 호출값(`subagent_type=feature-draft\b`, `agent_type="feature_draft"`) 0건; dangling 0
- [ ] V3: `.claude/skills/feature-draft/`·`.codex/skills/feature-draft/` 폴더명 불변, `_feature_draft_` draft 토큰 불변, 개념 산문 불변
- [ ] V4: `Agent(subagent_type=feature-draft-agent)`로 trivial 작업 1회 실제 dispatch → resolve 성공. dispatch 불가 시 가정 "미검증" 기록 + 사용자 보고 후 진행 여부 확인
- [ ] V5: live 영역에서 옛 경로 `agents/feature-draft.md`·`agents/feature-draft.toml` 참조 잔여 0건

**Target Files**:
- [M] `_sdd/drafts/2026-06-02_feature_draft_agent_identifier_rename.md` -- 게이트 결과 기록 (코드 변경 없음, 검증만)

**Technical Notes**: Covers V1~V4. Checkpoint gate. Q3의 가정을 여기서 HIGH로 승격.
**Dependencies**: T1

---

### Task T3: Batch — 나머지 9개 agent의 독립 파일 (카테고리 A)
**Component**: claude agents, codex agents, skill Mirror Notices
**Priority**: P0
**Type**: Refactor

**Description**: T2 통과 후, `feature-draft`를 제외한 9개 agent에 대해 카테고리 A(독립 파일)만 일괄 적용한다. 각 agent마다: claude `.md` rename+name+self-desc, codex `.toml` rename+name+self-desc, 양쪽 skill의 agent-경로 Mirror Notice. agent끼리는 파일이 겹치지 않아 병렬 가능하나, `implementation` 토큰은 longest-match(`implementation-plan`/`implementation-review` 먼저) 규칙을 반드시 지킨다.

**Non-Goals**: autopilot 공유 파일(B)은 이 task에서 건드리지 않는다(T4 담당). 개념 산문·skill 폴더명 변경 금지.

**Acceptance Criteria**:
- [ ] 9개 claude agent: `<slug>.md` → `<slug>-agent.md`, `name: <slug>-agent`, self-description invocation 갱신
- [ ] 9개 codex agent: `<slug>.toml` → `<slug>-agent.toml`, `name = "<snake>_agent"`, self-description invocation 갱신
- [ ] 9개 × 양쪽 skill의 agent-경로 Mirror/Sync Notice가 새 파일명을 가리킴
- [ ] **A' 경로 참조 갱신**: `.claude/agents/spec-review.md` 본문 Mirror Notice의 `.codex/agents/spec-review.toml` 경로 + 3-way 짝(`.claude/skills/spec-review/SKILL.md`, `.codex/skills/spec-review/SKILL.md`)의 양측 agent 경로; `.claude/agents/implementation-plan.md` Sync Notice의 self 경로
- [ ] `implementation` 치환이 `implementation-plan`/`implementation-review`를 오염시키지 않음 (완전 토큰 + longest-match)

**Target Files**:
- [M] `.claude/agents/{implementation-plan,implementation-review,implementation,investigate,plan-review,ralph-loop-init,spec-review,spec-update-done,spec-update-todo}.md` (각각 rename; spec-review·implementation-plan은 본문 경로 참조도 갱신)
- [M] `.codex/agents/{implementation-plan,implementation-review,implementation,investigate,plan-review,ralph-loop-init,spec-review,spec-update-done,spec-update-todo}.toml` (각각 rename)
- [M] `.claude/skills/{implementation-plan,implementation-review,implementation,investigate,plan-review,ralph-loop-init,spec-review,spec-update-done,spec-update-todo}/SKILL.md`
- [M] `.codex/skills/{implementation-plan,implementation-review,implementation,investigate,plan-review,ralph-loop-init,spec-review,spec-update-done,spec-update-todo}/SKILL.md`

**Technical Notes**: Covers C1, C2, I1. 카테고리 A·A'는 agent별 독립 → agent 단위 병렬 dispatch 가능. T4와는 파일이 겹치지 않으므로 T3∥T4 병렬 가능하나, 둘 다 T2 게이트 이후. spec-review의 3-way 경로는 한 agent task 안에서 함께 처리해 부분 갱신을 막는다.
**Dependencies**: T2

---

### Task T4: Batch — 나머지 9개 agent의 autopilot 공유 파일 (카테고리 B)
**Component**: autopilot shared docs
**Priority**: P0
**Type**: Refactor

**Description**: T2 통과 후, autopilot 공유 문서에서 호출값 행을 일괄 갱신한다. **공유 파일마다 등장하는 agent 집합이 다르므로 고정 개수가 아니라 "그 파일에 실제 존재하는 호출값"만** 갱신한다 — `investigate`/`plan-review`는 어느 공유 파일에도 없고, feature-draft 행은 T1에서 이미 처리됐다. 치환 대상은 backtick으로 감싼 완전 토큰이며 line number가 아닌 토큰 패턴으로 찾는다(파일이 T1 편집으로 밀렸을 수 있음).

**Non-Goals**: feature-draft 행 재변경 금지(T1 처리됨). 개념 산문(claude의 `feature-draft는...`/`spec-update-*만...` 류, codex 동일) 변경 금지.

**Acceptance Criteria (파일별 실제 멤버십 기준):**
- [ ] claude `orchestrator-contract.md` — 허용목록 + model 테이블에 등장하는 **7개**(feature-draft 제외): `spec-update-todo, implementation-plan, implementation, implementation-review, spec-update-done, spec-review, ralph-loop-init` → `-agent`
- [ ] codex `orchestrator-contract.md` — 허용목록의 동일 7개 snake(`spec_update_todo` 등) → `_agent`
- [ ] codex `execution-profile-policy.md` — distinct 7개. 단 `implementation_review`는 **2줄**(`구현 리뷰` + `final integration review`) 모두 갱신
- [ ] 양쪽 `sample-orchestrator.md` — `**Claude subagent_type**:`/`**Codex agent_type**:` 예시 값과 프로파일 매핑·retries·execution_sequence 라인 중 **호출값으로 쓰인 토큰만** 갱신(산문 설명은 제외)
- [ ] 개념 산문 라인 미변경 (V3로 재확인)

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/execution-profile-policy.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Technical Notes**: Covers C1, I1. 이 파일들은 T1에서 feature-draft 행만 건드렸으므로, T1 이후여야 하고(같은 파일) feature-draft 행 재변경 금지. 의미적 충돌(같은 파일·다른 행)이므로 T1과 순차.
**Dependencies**: T2 (그리고 같은 파일을 만진 T1 이후)

---

### Task T5: 최종 전역 검증 게이트 (V1~V3 + negative)
**Component**: Verification Gate
**Priority**: P0
**Type**: Test

**Description**: 전체 10개 agent에 대해 V1~V3 + V5를 실행하고 negative 검증을 더한다. live 영역에서 접미사 없는 잔여 호출값 0건, 옛 파일 경로 참조 0건, dangling reference 0건, skill 폴더명/개념 산문/draft 산출물 토큰 미침범. 실패 항목은 T3/T4로 복귀.

**Acceptance Criteria**:
- [ ] V1: `.claude/agents/`·`.codex/agents/` 각 10개 `<slug>-agent.{md,toml}` + name 확인
- [ ] V2: live 영역 `grep`에서 접미사 없는 호출값(완전 토큰) 0건; 모든 호출값↔name 대응(dangling 0)
- [ ] V5: live 영역 `grep`에서 옛 agent 파일 경로(`agents/<slug>.md`·`agents/<slug>.toml` 중 `-agent` 없는 것) 참조 0건 (A' surface 포함)
- [ ] V3(negative): `skills/<slug>/` 폴더 10개 불변, 개념 산문 불변, `_sdd/drafts` 산출물 토큰 불변, `_sdd/pipeline/*` 미변경
- [ ] 브랜치 커밋은 본 게이트 통과 후에만 수행

**Target Files**:
- [M] `_sdd/drafts/2026-06-02_feature_draft_agent_identifier_rename.md` -- 최종 검증 결과 기록 (검증만)

**Technical Notes**: Covers V1~V3, I2. Checkpoint gate. 통과 시 단일 또는 논리 단위 커밋.
**Dependencies**: T3, T4

## Parallel Execution Summary

- **Phase 0 (T0)**: 단독.
- **Phase 1 (T1→T2)**: 순차. T1이 공유 autopilot 파일을 처음 건드리는 지점, T2는 게이트.
- **Phase 2 (T3 ∥ T4)**: T3(agent별 독립 파일)와 T4(공유 파일)는 파일이 겹치지 않아 병렬 가능. T3 내부는 9개 agent가 서로 독립이라 agent 단위 추가 병렬 가능. 단 둘 다 T1이 만진 파일과의 관계상 T2 이후.
- **Phase 3 (T5)**: 단독, 최종 게이트.
- **충돌 메모**: autopilot 공유 5개 파일은 T1·T4가 공유 → 반드시 순차. `implementation` 토큰의 substring 충돌은 longest-match 규칙으로 회피.

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| 누락 호출처로 런타임 silent fail | V2 dangling-0 검증 + pilot 게이트 선행 |
| **agent 파일 내부 경로 참조(A') 누락으로 stale link** | V5 경로-레벨 grep + T3 AC에 spec-review 3-way·implementation-plan self 경로 명시 |
| `implementation` substring 오염 | 완전 토큰 매칭 + longest-match 우선(T0 앵커 규칙) |
| 개념 산문까지 잘못 치환(과잉) | V3 negative 검증 + Non-Goals 명시 |
| examples 누락 시 생성물 무효 | Q1 결정으로 examples 포함, T4 AC에 명시 |
| 런타임 resolution 가정 오류 | V4를 pilot에서 실제 dispatch로 확정, 실패 시 batch 차단·사용자 보고 |
| 공유 파일 멤버십 오해(없는 agent 탐색/중복 줄 누락) | T4 AC를 파일별 실제 7개 멤버십 + `implementation_review` 2줄로 명시 |

## Open Questions

- **Q1 (RESOLVED)**: autopilot `examples/sample-orchestrator.md` 변경 범위 포함 — 2026-06-02 사용자 확인 완료. 미결 아님.
- Q2~Q4는 Part 1에 결정 기록됨(확인 불요).
- **미결 0건**: 현재 모든 open question이 해소됨.

---

## Part 2 Self-Containment Check (Hard Rule 11)

- **검토 섹션 수**: 6개 task + Overview/Scope/Components/Phases/Parallel/Risks.
- **Pass 1 (외부 참조 inline purpose 확인)**:
  - 근거 토론 파일: 상단에 경로 + 합의 항목(범위 C/codex/분기 규칙/pilot-then-batch) 재진술 → bare path 아님. ✓
  - `C1~I3`, `V1~V4`: Part 1에 정의 후 Part 2 Coverage 표·Technical Notes에서 `ID + purpose`로 참조. ✓
  - 고유 용어(분기 규칙, 카테고리 A/B/C, longest-match, dangling, negative touchpoint): 최초 사용 지점에 1줄 정의. ✓
  - 라인 번호(L41 등): 2026-06-02 census 기준임을 Touchpoints 서두에 명시(구현 시 재확인 전제). ✓
- **Pass 2 (생초 독자 readthrough)**:
  - 발견 갭: 초기 draft에서 "공유 파일이 왜 병렬 불가인지"가 Task 레벨에만 있고 Overview에 없었음 → Overview에 충돌 구조 1문단 보완.
  - 발견 갭: `implementation` substring 위험이 T3에만 있고 전역 규칙으로 안 보였음 → T0 AC와 Census Map 주석에 앵커 규칙으로 승격.
- **보완 완료**: Yes
- **Plan-review 반영(2026-06-02, `_sdd/implementation/2026-06-02_plan_review_agent_identifier_rename.md`)**:
  - High: agent 파일 내부 경로 참조(A' surface) + 경로-레벨 게이트(V5) 추가 → Touchpoints A', T3 AC, V5, T2/T5 게이트 반영.
  - Medium: T4 "9개"를 파일별 실제 멤버십(7개 + `implementation_review` 2줄, investigate/plan-review 부재)으로 교정.
  - Medium: V4를 실제 dispatch로 구체화(+ dispatch 불가 시 사용자 보고 경로).
