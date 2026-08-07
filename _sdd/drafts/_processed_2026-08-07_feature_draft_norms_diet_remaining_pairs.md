# Feature Draft: SDD 핵심 스킬·agent 규범 다이어트 — 나머지 5쌍

> 규모 판정: 분할 필요 — 분할 계획 포함 (5개 독립 쌍 × 각 codex 미러 전파 = 단일 컨텍스트 초과, 쌍 단위로 눈검산 가능한 feature 5개로 롤링 분할)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
SKILL_AUTHORING_NORMS 전수 리뷰(2026-08-07, finding 60건)의 잔여 5쌍을 쌍 단위 feature로 다이어트한다. 공통 원칙: 지시 반복·판단 주체 복제 해소(단일 홈), 근거 없는 수치·방어 규칙의 기준화, 하드 게이트 존치 시 근거 1줄 병기, Final Check 1줄은 존치(d903052). 사용자 결정: Propagation Surfaces 계약은 feature-draft 소유로 **단일 홈화**.

분할 feature 목록 (각 1줄 의도 + scope):
1. **autopilot-simplicity-diet**: sdd-autopilot의 producer 로직 재서술·다이어그램 제거 + simplicity-review-agent 재천명 축약 — scope: `.claude/skills/sdd-autopilot/` + `.claude/agents/simplicity-review-agent.md` + codex 미러 2
2. **spec-sync-agent-diet**: Hard Rules↔Process/Status 이중 서술 해소, digest 4필드 계약화, legacy fallback·`_processed_` 소유 반복 제거 — scope: `.claude/agents/spec-sync-agent.md` + `.claude/skills/spec-sync/SKILL.md` + codex TOML
3. **pr-review-diet**: 반환 형식 재정의 삭제(agent 홈), 경계 선언·read-only 재천명 통합, UNTESTED verdict 경로 명시, dispatch 입력 필드화 — scope: `.claude/skills/pr-review/` + `.claude/agents/pr-review-agent.md` + codex 미러
4. **feature-draft-pair-diet**: Propagation Surfaces 계약 단일 홈화(사용자 결정), Minimum-Code 이중 서술 축약, verbatim 복사 지시화, 인터뷰·평가방법 2등급 갭 반영 — scope: `.claude/skills/feature-draft/` + `.claude/agents/plan-review-agent.md` + `.claude/skills/plan-review/` + codex 미러
5. **implementation-pair-diet**: fix-1회 홈 단일화, 롤링 분할 포인터화, no-file 재천명 통합, ledger 이탈 기록 필드 추가 — scope: `.claude/skills/implementation{,-review}/` + `.claude/agents/implementation-review-agent.md` + codex 미러

## Scope
- **In**: 위 5쌍의 claude 본문 + codex 미러(3-way merge)
- **Out**: discussion 쌍(완료, v4.6.42), Final Check 1줄 제거, 하네스 AGENTS.md 수정, 리뷰 finding 중 d903052 기각분
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | autopilot orchestration 다이어트 | `.claude/skills/sdd-autopilot/SKILL.md`<br>`.codex/skills/sdd-autopilot/SKILL.md` | `rg --files .claude/skills/sdd-autopilot .codex/skills/sdd-autopilot -g 'SKILL.md'` → 두 exact path | Task 1 |
| P2 | simplicity reviewer 다이어트 | `.claude/agents/simplicity-review-agent.md`<br>`.codex/agents/simplicity-review-agent.toml` | `rg --files .claude/agents .codex/agents -g 'simplicity-review-agent.*'` → 두 exact path | Task 2 |

# Part 2: Tasks (첫 feature — autopilot-simplicity-diet)

### Task 1: sdd-autopilot Claude/Codex 쌍 다이어트
producer 스킬이 단일 소스인 로직의 재서술을 양 플랫폼에서 제거하고, 오케스트레이션 고유 내용과 runtime delta만 남긴다.

**Acceptance Criteria**:
- [ ] AC1: 양 파일에서 `## Workflow Position` 섹션 전체가 삭제된다 — `rg -n '^## Workflow Position$|^User Request$|^\[sdd-autopilot\]|내부 품질 게이트' <두 파일>` 0건
- [ ] AC2: producer 내부 로직 재서술(`RED→GREEN|AC→증거|fix 1회|게이트당 fix`)은 양 파일에서 0건이고, `품질 게이트와 finding 반영은 producer 스킬이 소유한다`는 선언은 Step 2 규칙에 파일당 정확히 1건이다
- [ ] AC3: 질문 원칙은 `답이 설계나 범위를 바꾸는 핵심 분기만`·`한 번에 하나`·`최소 횟수` 기준으로 바뀌며 `2-3개|최대 5회`는 양 파일에서 0건이다
- [ ] AC4: AC1은 draft에 규모 판정 **근거가 존재**하는지만 요구하고 형식 리터럴 `` `> 규모 판정:` ``은 양 파일에서 0건이다
- [ ] AC5: 양 파일에서 `Draft`→`구현`→`Spec sync`→`최종 보고` 순서, `승인 게이트는 없다`, `_sdd/spec/` 직접 수정 금지와 spec-sync 위임 앵커가 각각 존재한다
- [ ] AC6: Claude 고유 `sdd-skills:` prefix·`Agent(...)` lifecycle 앵커와 Codex 고유 `framed payload`·`active schema`·`.codex/skills/<name>/SKILL.md` 앵커가 각각 1건 이상 보존된다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/SKILL.md`

### Task 2: simplicity-review-agent Claude/Codex 쌍 다이어트
공통 재천명과 방어 부연을 제거하되, Claude tools 제한과 Codex helper/runtime 경계의 차이는 보존한다.

**Acceptance Criteria**:
- [ ] AC1: correctness 배제는 양 파일의 `Hard Rules` `표적 disjoint` 1곳에만 남는다 — intro의 `correctness reviewer`, Severity의 `correctness 영향`, Step 2의 `correctness 신호`는 각각 0건
- [ ] AC2: Claude Hard Rule 1은 tools 배열과 중복되는 spawn·파일 mutation 금지를 제거하고 `단순성 리뷰만 수행한다. 제안은 반환에만 기록한다`로 축약한다. Codex Hard Rule 1은 파일 mutation 금지와 반환-only를 유지하고, `Codex Agent Boundary`의 `bounded helper(worker/explorer)` 허용을 보존한다
- [ ] AC3: 차원 한정 절은 `차원 한정이 없으면 전체 5개 차원을 수행한다`만 남기고 `이 절은 .*바꾸지 않는다`는 양 파일에서 0건이다
- [ ] AC4: 양 파일에서 차원 5종(`중복 코드|죽은 코드|단일 사용처 추상화|도달 불가 에러 처리|과잉압축`), severity 4종(`Critical|High|Medium|Low`), 반환 필드(`Findings|차원 판정|Assumptions`), `lowercase canonical`·`legacy uppercase` 앵커가 보존된다
- [ ] AC5: Codex TOML은 `python3 -c 'import tomllib; tomllib.load(open(".codex/agents/simplicity-review-agent.toml","rb")); print("TOML_OK")'`가 `TOML_OK`를 출력하고 `Codex Agent Boundary|spawn_agent\(agent_type=|bounded helper`가 각 1건 이상 남는다

**Target Files**:
- [M] `.claude/agents/simplicity-review-agent.md`
- [M] `.codex/agents/simplicity-review-agent.toml`

### Task 3: read-only census 검증
**Acceptance Criteria**:
- [ ] AC1: autopilot 두 파일에서 `^## Workflow Position$|^User Request$|^\[sdd-autopilot\]|내부 품질 게이트|RED→GREEN|AC→증거|fix 1회|게이트당 fix|2-3개|최대 5회|> 규모 판정:` census가 0건이다
- [ ] AC2: reviewer 두 파일에서 `correctness reviewer|correctness 영향|correctness 신호|이 절은 .*바꾸지 않는다` census가 0건이고, Claude 파일에서만 `sub-agent를 spawn하지 않고|어떤 파일도 생성/수정/삭제`가 0건이다
- [ ] AC3: Task 1 AC5~AC6과 Task 2 AC4~AC5의 보존 앵커 query를 재실행해 모두 기대 집합을 충족한다

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 경로 lowercase/legacy fallback 규칙의 파일 간 반복은 플러그인 이식성(각 스킬 자립 실행) 때문에 파일당 1회를 소비 지점 홈으로 판정 — 파일 간 단일화는 하지 않음. 사용자 확인 불요(리뷰어 유보 항목의 해소).
