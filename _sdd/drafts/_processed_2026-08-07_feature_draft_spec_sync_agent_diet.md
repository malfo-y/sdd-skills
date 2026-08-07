# Feature Draft: spec-sync agent single-home diet

> 규모 판정: 적격 — digest 계약 1개와 중복 규칙 3종이 네 동기화 표면에만 닫히며 task별 대응을 눈검산할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`spec-sync`의 implemented 분할 dispatch가 전달하는 digest를 고정 헤더와 필수 4필드(`Delta List`, `Classification Basis`, `Spec Version`, `Decision Title`)의 호출 계약으로 명시한다. agent 본문에서는 status routing, legacy fallback, `_processed_` 소유 규칙의 canonical home을 각각 하나로 줄여 같은 판단과 절차가 Acceptance Criteria·Hard Rules·Process에 반복되지 않게 한다.

## Scope
- **In**: Claude/Codex `spec-sync` wrapper의 digest producer 계약, Claude/Codex `spec-sync-agent`의 digest consumer 계약과 본문 중복 제거, 양 runtime 의미 parity 검증
- **Out**: status enum·evidence-driven 승격 의미 변경, 본문/기록 표면 분할 변경, dispatch lifecycle 변경, output report 필드 변경, 다른 skill·agent 수정
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | implemented sync digest consumer 계약 | `.claude/agents/spec-sync-agent.md`, `.codex/agents/spec-sync-agent.toml` | `rg -l '호출자 digest' .claude/agents/spec-sync-agent.md .codex/agents/spec-sync-agent.toml` → 두 agent 표면 | Task 1 |
| P2 | implemented sync digest producer 계약 | `.claude/skills/spec-sync/SKILL.md`, `.codex/skills/spec-sync/SKILL.md` | `rg -l 'delta 목록' .claude/skills/spec-sync/SKILL.md .codex/skills/spec-sync/SKILL.md` → 두 wrapper 표면 | Task 2 |
| P3 | status·legacy·processed single-home diet | `.claude/agents/spec-sync-agent.md`, `.codex/agents/spec-sync-agent.toml` | `rg -l 'Status 분류 \(Routing\)|legacy fallback|_processed_' .claude/agents/spec-sync-agent.md .codex/agents/spec-sync-agent.toml` → 두 agent 표면 | Task 1 |

# Part 2: Tasks

### Task 1: agent 계약과 판단 규칙을 단일 홈으로 정리한다
두 agent 미러에서 호출자 digest consumer 형식을 명시하고, 반복된 판정·fallback·소유 문장은 가장 가까운 소비 지점으로 모은다. Claude frontmatter와 Codex Agent Boundary 같은 runtime 고유 어댑터는 그대로 둔다.

**Contracts**: implemented 분할 호출의 `## Implemented Sync Digest`는 `- **Delta List**:`, `- **Classification Basis**:`, `- **Spec Version**:`, `- **Decision Title**:` 네 필수 필드를 이 순서로 정확히 한 번씩 받는다. 앞의 세 자유 서술값과 결정 제목은 비어 있지 않아야 하고 `Spec Version`은 SemVer다. status 4분류의 정의는 `Status 분류 (Routing)`, legacy input discovery는 `Input Sources`, `_processed_` rename의 본문/기록 묶음 소유권은 `호출자 표면 한정`이 각각 canonical home이다. 다른 절은 이 홈을 참조하되 판정 목록이나 소유 규칙을 재서술하지 않는다.

**Acceptance Criteria**:
- [ ] AC1: 두 agent에서 digest heading은 각 1건이고, 그 heading부터 다음 `## ` heading 전까지의 블록에 네 exact field prefix가 정해진 순서로 각 1건이다. 필수/비어 있지 않음·SemVer 조건과 기록 묶음의 소비 관계도 이 블록에 명시된다.
- [ ] AC2: 두 agent에서 네 status enum의 굵은 정의는 `Status 분류 (Routing)` 블록에 각 1건이고, 그 블록 밖에는 해당 굵은 enum token이 0건이다. Pipeline·Acceptance Criteria·Hard Rules·Process는 필요한 경우 canonical heading만 참조한다.
- [ ] AC3: legacy uppercase/fixed-name fallback 목록은 두 agent의 `Input Sources`에만 남고 Process와 Hard Rules에는 같은 fallback 목록이 없다. canonical lowercase 우선과 read-only fallback 의미는 보존된다.
- [ ] AC4: `_processed_` rename의 묶음별 소유권은 두 agent의 `호출자 표면 한정`에만 정의된다. Acceptance Criteria·Input Sources·Process·Final Check는 소유 규칙을 반복하지 않으며, unbounded 호출의 rename과 Output Format의 `Processed Input Files` 필드는 보존된다.
- [ ] AC5: 이번 scope에서 닿는 현행 Hard Rule 3(status), 5(legacy task-detail), 11(legacy decision input/기록 소유)은 각각 canonical home을 참조하는 문장으로 줄인다. 이 세 규칙에서 강제 표현을 남기면 그 표현이 막는 관측 실패를 한 줄로 설명하고, 나머지 Hard Rules는 변경하지 않는다.
- [ ] AC6: Claude/Codex agent에서 runtime 전용 서두를 제외한 계약·판정·프로세스 의미가 동일하고 TOML `developer_instructions`가 parse된다.

**Target Files**:
- [M] `.claude/agents/spec-sync-agent.md` -- digest consumer 계약과 single-home 본문 정리
- [M] `.codex/agents/spec-sync-agent.toml` -- 같은 의미의 Codex agent 미러 정리

### Task 2: wrapper가 고정 digest를 생성하도록 계약화한다
두 wrapper의 implemented 선고정 절을 자유 산문 필드 나열에서 agent가 소비하는 고정 형식으로 바꾼다. Claude `Agent(...)`와 Codex mailbox/legacy schema 어댑터는 유지한다.

**Contracts**: implemented 분할 dispatch 전에 wrapper가 `## Implemented Sync Digest` 아래 네 필수 필드를 채우며, 동일한 digest를 본문·기록 두 호출에 전달한다. `Spec Version`만 대화에서 미상이면 기존처럼 `main.md` 헤더 targeted grep 1회를 허용한다.

**Acceptance Criteria**:
- [ ] AC7: 두 wrapper에 agent와 동일한 `## Implemented Sync Digest` 4필드 형식 정의가 있고, implemented 본문·기록 두 dispatch가 같은 digest를 받는다고 명시한다.
- [ ] AC8: 기존 분기 수와 dispatch topology를 보존한다: planned는 1회, implemented는 본문/기록 2회 병렬이며 Claude는 `Agent(...)`, Codex는 active schema 기반 mailbox 또는 target/close contract를 사용한다.
- [ ] AC9: wrapper는 status 분류·spec 수정·`_processed_` rename을 수행하지 않고 agent에 위임하며, implemented 사후 검사는 기존의 version 일치와 history 삭제 줄 0 두 종류를 유지한다.
- [ ] AC10: 각 wrapper에서 digest heading은 1건이고 그 블록 내부의 네 exact field prefix는 정해진 순서로 각 1건이다. planned/implemented 분기와 사후 검사 섹션 밖에는 같은 계약 블록이 없다.

**Target Files**:
- [M] `.claude/skills/spec-sync/SKILL.md` -- Claude digest producer 형식 정의
- [M] `.codex/skills/spec-sync/SKILL.md` -- Codex digest producer 형식 정의

### Task 3: 전파와 잔존 중복을 read-only 검증한다
네 표면의 계약 전파 누락과 두 agent의 재서술 잔존을 구현과 분리해 검증한다.

**Acceptance Criteria**:
- [ ] AC11: section-aware 검사로 네 target 각각에서 digest heading 1건과 다음 `## ` 전까지 네 exact field prefix 각 1건·고정 순서를 assert한다. `rg -l '## Implemented Sync Digest' <네 target>`의 집합도 네 경로와 정확히 일치한다.
- [ ] AC12: agent별 section-aware 검사로 (a) 네 굵은 status enum이 `Status 분류 (Routing)` 안 각 1건/밖 0건, (b) legacy uppercase/fixed-name fallback 목록이 `Input Sources` 안에만 존재, (c) `표면 한정 시 기록 묶음 소유`·`본문 묶음은 rename하지 않는다`에 해당하는 소유 재서술이 `호출자 표면 한정` 밖 0건임을 assert한다. 이어 Claude/Codex 의미 대조, TOML parse, `git diff --check`가 모두 PASS다.

**Target Files**:
- 없음 (read-only 검증)
