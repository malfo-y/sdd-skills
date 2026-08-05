# Feature Draft: Producer-Review Contract Alignment

> 규모 판정: 적격 — 중요 결정 기록과 propagation surface 계약을 producer 2미러·reviewer 2미러·정의 문서 2미러에 전파하는 3-task 변경이며, 변경 요소→task 대응을 아래 표로 눈검산할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

- `feature-draft` producer와 `plan-review` reviewer는 결과 방향을 바꿀 수 있는 중요 결정에 한해서만 가정·근거·기각 대안·확신도·사용자 확인 필요 여부를 같은 조건으로 요구한다.
- 동일 변경 요소가 둘 이상의 동기화 표면에 전파될 때 draft는 조건부 `Propagation Surfaces` 표를 만들고, 각 행을 정확히 하나의 owner task와 그 task의 Target Files·AC에 연결한다.
- 일반 다중파일 변경은 propagation 표의 대상이 아니며, 변형 표기 전수 제거가 필요한 경우에만 기존 census read-only verification task를 추가한다.

## Scope

- **In**: Claude/Codex `feature-draft` 산출 계약, Claude/Codex `plan-review-agent` 판정 계약, 한·영 draft 정의 문서, 미러·계약 census 검증.
- **Out**: Feature B implementation ledger, plan-review의 6-smell 수·severity·2-렌즈 구조, implementation-review dedup·재리뷰 정책, 실제 Opus 5 finding 감소율 측정, AUTOPILOT_GUIDE 사용자 개입 계약.
<!-- spec-update-todo-input-end -->

# Decisions and Assumptions

### D1: Feature A와 implementation ledger를 분리한다

- **Decision / Assumption**: 이번 draft는 producer-review 정렬과 propagation 표만 다루고 ledger는 후속 Feature B로 분리한다.
- **Evidence**: 두 변경은 실패 원인과 수정 표면이 다르며, 사용자가 2단계 분리를 선택했다.
- **Rejected alternatives**: 세 변경을 한 feature로 묶는 안 — 변경 원인과 검증 범위가 섞여 기각.
- **Confidence**: High.
- **User confirmation needed**: No — 토론에서 확인됨.

### D2: draft 구조 정의 문서 한·영 미러를 구현 표면에 포함한다

- **Decision / Assumption**: `docs/SDD_SPEC_DEFINITION.md`와 `docs/en/SDD_SPEC_DEFINITION.md`는 현행 draft 섹션을 정확히 열거하므로 producer 계약과 같은 task에서 갱신한다.
- **Evidence**: 두 문서가 `Part 1`, `Part 2`, `Open Questions`와 템플릿을 직접 정의한다.
- **Rejected alternatives**: spec-sync에만 맡기는 안 — spec-sync는 `_sdd/spec/`만 수정해 docs drift를 닫지 못하므로 기각.
- **Confidence**: High.
- **User confirmation needed**: No — 기존 미러 정합 guardrail의 직접 적용.

### D3: propagation 표는 동일 변경 요소의 둘 이상 동기화 표면에만 발동한다

- **Decision / Assumption**: 일반 다중파일 변경은 제외하고, 동일 change element가 둘 이상의 동기화 표면에 반영돼야 할 때만 표를 만들며 각 행은 단일 owner task가 소유한다.
- **Evidence**: 모든 다중파일 변경에 표를 강제하면 Target Files 복제본이 된다는 토론의 비판적 검토와 사용자 선택.
- **Rejected alternatives**: 모든 다중파일 변경에 표 적용 — 일반 구현까지 중복 ceremony가 생겨 기각.
- **Confidence**: High.
- **User confirmation needed**: No — 토론에서 확인됨.

### D4: propagation 검사는 기존 Verification Weakness가 소유한다

- **Decision / Assumption**: `plan-review`의 smell 수를 늘리지 않고, 표 누락·실측·owner 연접 오류를 기존 `Verification Weakness` 안에서 판정한다.
- **Evidence**: 새 계약은 계획의 검증 완전성 문제이며 기존 6-smell의 `Verification Weakness` 정의에 직접 들어간다.
- **Rejected alternatives**: 일곱 번째 smell 추가 — rubric·병합 계약까지 넓어져 YAGNI라 기각.
- **Confidence**: High.
- **User confirmation needed**: No — Feature A가 기존 6-smell 구조를 변경하지 않는 범위로 확인됨.

### D5: 완료 기준은 유한한 구조 assertion 검증으로 한정한다

- **Decision / Assumption**: 실제 Opus 5 finding 감소율은 측정하지 않고, producer/reviewer/docs의 유한 assertion matrix와 mutation 판별력만 완료 증거로 사용한다.
- **Evidence**: 사용자가 `구조검증만`을 선택했다.
- **Rejected alternatives**: 구조 검증 후 실제 3회 finding 관찰 — 효과 측정에는 유리하지만 이번 범위에서 기각.
- **Confidence**: High.
- **User confirmation needed**: No — 토론에서 확인됨.

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | producer의 중요 결정·조건부 propagation 산출 계약 | `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md`, `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` | live roots에서 ① `rg -l '^name: feature-draft$' .claude/skills .codex/skills --glob 'SKILL.md'` 기대 집합=producer 2경로, ② `rg -l 'canonical 구조.*feature-draft.*Required Output|Canonical structure.*feature-draft.*Required Output' docs --glob 'SDD_SPEC_DEFINITION.md'` 기대 집합=정의 문서 2경로. `_sdd/` history·process artifact는 제외 | Task 1 |
| P2 | reviewer의 중요 결정·propagation 검증 계약 | `.claude/agents/plan-review-agent.md`, `.codex/agents/plan-review-agent.toml` | live roots `.claude/agents`, `.codex/agents`에서 `rg -l 'Decision and Assumption Surfacing'` 기대 집합=reviewer 2경로. `_sdd/` history·process artifact는 제외 | Task 2 |

# Part 2: Tasks

### Task 1: Align the feature-draft producer contract and human definition

중요 결정과 propagation 정보를 producer가 reviewer 판정 전에 같은 형식으로 산출하도록 하고, 정확한 draft 구조를 정의하는 한·영 문서를 함께 맞춘다.

**Contracts**:

- 중요 결정은 결과 방향·Target Files 선택·task boundary 중 하나를 바꿀 수 있는 결정으로 한정하며, 해당 결정만 `Decision / Assumption`, `Evidence`, `Rejected alternatives`, `Confidence`, `User confirmation needed`를 기록한다. 해당 결정이 없으면 섹션을 생략한다.
- 동일한 change element가 둘 이상의 동기화 표면(미러·등록·템플릿·문서 등)에 반영돼야 할 때만 `Propagation Surfaces`를 만들고, 열은 `ID / Change element / Required surfaces / Discovery evidence / Owner task`로 고정한다. 각 행은 정확히 한 owner task를 가지며 그 task의 Target Files·AC가 required surface의 실행과 검증을 닫는다.
- 일반 다중파일 변경만으로는 propagation 표를 만들지 않는다. 변형 표기 전수 제거가 필요한 경우에만 기존 census verification task 규칙을 적용한다.

**Acceptance Criteria**:

- [ ] AC1: Claude/Codex `feature-draft` Required Output과 규칙에 중요 결정의 조건·5필드·조건부 섹션 생략이 모두 존재하고, 결과 방향을 바꾸지 않는 사소한 결정에는 기록을 강제하지 않는다고 명시돼 있다.
- [ ] AC2: Claude/Codex `feature-draft` Required Output과 규칙에 `Propagation Surfaces`의 발동 조건·5열·단일 owner task·Target Files/AC 연접·일반 다중파일 제외·census 별도 조건이 모두 존재한다.
- [ ] AC3: `Propagation Surfaces`는 `spec-update-todo-input` 마커 밖에 있으며, 기존 `Open Questions` 섹션과 사용자 확인 필요 항목만 채팅에 노출하는 surface 계약은 보존된다.
- [ ] AC4: 한·영 `SDD_SPEC_DEFINITION`의 draft 구조 목록과 템플릿이 assertion matrix `DOC1`(중요 결정 발동 조건+5필드+생략), `DOC2`(propagation 발동 조건+5열+단일 owner/Task 연접), `DOC3`(일반 다중파일 제외+census 분리)를 각각 충족한다.
- [ ] AC5: `.claude/skills/feature-draft/SKILL.md`와 `.codex/skills/feature-draft/SKILL.md`는 변경 후 byte-identical이다.

**Target Files**:

- [M] `.claude/skills/feature-draft/SKILL.md` -- Claude Code producer 산출 계약 추가
- [M] `.codex/skills/feature-draft/SKILL.md` -- Codex producer 미러 산출 계약 추가
- [M] `docs/SDD_SPEC_DEFINITION.md` -- 한국어 draft 구조 정의 동기화
- [M] `docs/en/SDD_SPEC_DEFINITION.md` -- 영어 draft 구조 정의 미러 동기화

### Task 2: Align the plan-review decision and propagation checks

reviewer가 producer와 같은 중요 결정 조건만 검사하고, 조건부 propagation 표의 누락·연접 오류를 기존 Verification Weakness smell 안에서 검출하게 한다.

**Contracts**:

- reviewer는 producer와 동일한 중요 결정 조건과 5필드를 사용한다. 중요 결정 신호가 없을 때 섹션 부재 자체를 finding으로 만들지 않는다.
- 동일 change element의 둘 이상 동기화 표면 신호가 있으면 `Propagation Surfaces` 존재 여부와 5열, required surface 실측, 단일 owner task, owner Target Files·AC 연접을 검증한다. 이 검사는 기존 `Verification Weakness` 소유이며 새 smell을 만들지 않는다.

**Acceptance Criteria**:

- [ ] AC1: Claude/Codex `plan-review-agent`의 Hard Rule·Inventory·Step 4가 중요 결정의 조건과 5필드를 producer 계약과 동일하게 사용하고, 중요 결정이 없을 때 조건부 섹션 생략을 허용한다.
- [ ] AC2: 두 reviewer가 propagation 발동 신호와 표의 5열·required surface·단일 owner·Target Files/AC 연접을 `Verification Weakness`로 검사하며, 6-smell 표와 severity 체계는 변경하지 않는다.
- [ ] AC3: Step 3 도구 계단이 propagation 표의 exact path/pattern과 discovery evidence를 기존 Glob→Grep→Read 순서 안에서 대조할 수 있게 명시돼 있다.
- [ ] AC4: Claude markdown agent와 Codex TOML agent가 assertion matrix `REV1`(중요 결정 조건+5필드+생략), `REV2`(propagation 5열·실측·단일 owner·Task 연접), `REV3`(`Verification Weakness` 소유), `REV4`(Glob→Grep→Read 계단)를 각각 충족한다. Codex 전용 `Codex Agent Boundary`와 runtime source pointer, Claude frontmatter는 비교 범위에서 제외한다.

**Target Files**:

- [M] `.claude/agents/plan-review-agent.md` -- Claude reviewer의 조건부 decision/propagation 판정 정렬
- [M] `.codex/agents/plan-review-agent.toml` -- Codex reviewer의 동일 계약 미러

### Task 3: Verify the contract propagation census

이번 변경 자체가 미러·정의 문서 전파형이므로 변형 표기와 누락 표면을 read-only census로 닫는다.

**Acceptance Criteria**:

- [ ] AC1: producer 2미러의 byte diff가 0이고, assertion `PROD1`(중요 결정 조건+5필드+생략), `PROD2`(propagation 조건+5열), `PROD3`(단일 owner+Target Files/AC 연접), `PROD4`(일반 다중파일 제외+census 분리), `PROD5`(마커 밖 배치+Open Questions 보존)가 양쪽에서 각각 검출된다.
- [ ] AC2: reviewer 2미러가 `REV1`~`REV4`를 각각 충족한다. 비교는 Task 2 AC4의 runtime 제외 경계를 적용하며, assertion별 필수 anchor의 양쪽 존재 여부로 판정한다.
- [ ] AC3: P1/P2 Discovery evidence의 live-root census 결과가 정렬된 기대 경로 집합과 정확히 일치하고 예상 밖·누락 경로가 있으면 실패한다. `docs/AUTOPILOT_GUIDE.md`와 `docs/en/AUTOPILOT_GUIDE.md`의 `Open Questions` 사용자 개입 anchor가 각각 남아 있고 두 파일의 git diff가 0이다.
- [ ] AC4: `PROD1`~`PROD5`, `DOC1`~`DOC3`, `REV1`~`REV4` assertion을 **저장소 밖 임시 복사본에서만** 하나씩 제거·변형하면 해당 assertion check가 실패하고, 정본 입력에서는 전부 통과한다. mutation 과정은 저장소 파일을 수정하지 않는다.

**Target Files**:

- 없음 (read-only 검증)
