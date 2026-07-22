# Feature Draft: 스탠드얼론 reviewer/generator agent를 직접 실행 skill로 흡수 (spec-review, ralph-loop-init)

> 규모 판정: 적격 — 성격 동일한 2개 대칭 전환 + 등록 정리 + census 1개. 변경 요소와 task 대응이 1:1 눈검산 가능. 단, agent 식별자 변형 전파(kebab/underscore/.md/.toml/subagent_type/agent_type, claude+codex 짝)가 census형 신호라 Part 2 마지막에 read-only 검증 task를 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`spec-review`와 `ralph-loop-init`을 "thin wrapper skill → agent(계약 보유)" 2홉 구조에서 **직접 실행 skill**(메인 루프가 본문을 직접 수행)로 흡수한다. 두 agent(`.claude/agents/*.md` + `.codex/agents/*.toml`)를 삭제하고, 계약 본문을 각 wrapper skill로 이관한다.

근거: 두 agent는 (a) 자기 wrapper skill만 dispatch하는 스탠드얼론 entrypoint라 프로그래밍적 재사용 대상이 없고, (b) 자동 SDD 체인 소속이 아니라 보호할 host 컨텍스트가 없어 subagent 격리 이득이 0이다. 추가로 ralph-loop-init은 대화형 사용자 확인 게이트(Step 2 검증 방법 확정)를 갖는데 subagent는 실행 중 사용자와 대화할 수 없어 현재 구조가 능력 불일치 상태다 — skill 전환이 이 게이트를 비로소 작동시킨다.

**대비(변경 없음, 경계 기록)**: `spec-sync`는 이 전환에서 제외한다. autopilot·체인이 프로그래밍적으로 dispatch하는 체인 종결 mutator라 spec 편집 추론을 오케스트레이터 컨텍스트에서 격리하는 이득이 load-bearing이다 (plan-review·implementation-review agent를 유지하는 근거와 동일).

**계약 변화**:
- `spec-review`, `ralph-loop-init` = 직접 실행 skill (더 이상 wrapper→agent 2홉 아님). 계약·프로세스·출력 형식의 단일 소스는 각 SKILL.md.
- 등록된 sdd-skills agent set: 7 → 5 (`plan-review-agent`, `implementation-review-agent`, `simplicity-review-agent`, `pr-review-agent`, `spec-sync-agent`).
- skill trigger·산출물 경로 계약(`_sdd/spec/logs/spec_review_report.md`, `ralph/` 산출물)은 불변.

## Scope
- **In**: `spec-review`·`ralph-loop-init`의 claude+codex SKILL.md 본문 흡수, 두 agent의 claude `.md`·codex `.toml` 삭제, 등록 surface(marketplace agents 배열, codex agents README) 정리, agent 식별자 변형 census 검증.
- **Out**: `spec-sync` 및 다른 agent 일체(유지). skill trigger/description 문구 변경(불필요). agent가 보유하던 리뷰 rubric·상태 머신·run.sh 템플릿 등 **계약 내용 자체의 수정**(이관만 하고 내용은 보존). components.md 등 spec surface 갱신(spec-sync 단계 소관).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: spec-review를 직접 실행 skill로 흡수
`spec-review-agent`의 리뷰 계약 본문을 `spec-review` SKILL.md(claude+codex)로 이관하고, 메인 루프가 dispatch 없이 직접 리뷰를 수행하도록 만든다. 두 agent 파일을 삭제한다.

**Contracts**: `spec-review` skill = 직접 실행 read-only reviewer. 리뷰 프로세스·global/temporary rubric·severity·리포트 형식(`_sdd/spec/logs/spec_review_report.md`)·review-only 불변식(spec 파일 미수정)의 단일 소스는 SKILL.md 본문. wrapper→agent dispatch 계약은 소멸.

**Acceptance Criteria**:
- [ ] AC1 (흡수 완전성, positive): `.claude/skills/spec-review/SKILL.md` 본문에 이관 대상 핵심 섹션이 모두 존재한다 — Acceptance Criteria, Hard Rules(review-only), Review Dimensions(Global Spec Quality / Temporary Spec Quality / Code-Linked Drift), Process(Step 1~5 + Code Analysis Metrics), Output Format, Error Handling. 각 섹션 heading을 grep으로 확인(존재 = positive 증거).
- [ ] AC2 (wrapper 잔재 제거): `.claude/skills/spec-review/SKILL.md`에서 "entrypoint wrapper"·"위임"·`Agent(subagent_type`·`Source: ... agent가 단일 소스` 문구가 grep 0.
- [ ] AC3 (codex adapter 제거): `.codex/skills/spec-review/SKILL.md`가 직접 실행 본문을 보유하고 `Codex Runtime Adapter`·`spawn_agent`·`wait_agent`·`close_agent`·`Agent Message Boundary`가 grep 0. 트리거·리포트 경로 계약은 보존.
- [ ] AC4 (claude↔codex parity): codex SKILL.md 본문이 claude SKILL.md 본문과 동일하다 — 이 skill은 flag delta가 없으므로 frontmatter(version 제외) 아래 본문 diff가 0이어야 한다.
- [ ] AC5 (version lockstep): 4개 version 필드(claude skill.json, claude SKILL.md frontmatter, codex skill.json, codex SKILL.md frontmatter)가 모두 동일 목표값 `4.0.0`이다 — 기존 json↔md drift(2.3.1 vs 3.0.0)를 해소하며 상향.
- [ ] AC6: `.claude/agents/spec-review-agent.md`와 `.codex/agents/spec-review-agent.toml`이 삭제됨 (파일 부재).

**Target Files**:
- [M] `.claude/skills/spec-review/SKILL.md` -- agent 계약 본문 흡수, wrapper 문구 제거, frontmatter version
- [M] `.codex/skills/spec-review/SKILL.md` -- 직접 실행 본문 흡수, Codex adapter/spawn 제거, frontmatter version
- [M] `.claude/skills/spec-review/skill.json` -- version 4.0.0
- [M] `.codex/skills/spec-review/skill.json` -- version 4.0.0
- [D] `.claude/agents/spec-review-agent.md` -- skill로 흡수, 삭제
- [D] `.codex/agents/spec-review-agent.toml` -- skill로 흡수, 삭제

### Task 2: ralph-loop-init을 직접 실행 skill로 흡수
`ralph-loop-init-agent`의 계약 본문(discovery·상태 머신·파일 생성·run.sh 템플릿·CHECKS 검증)을 `ralph-loop-init` SKILL.md(claude+codex)로 이관하고, 메인 루프가 직접 수행하도록 만든다. Step 2 대화형 확인 게이트가 메인 루프에서 작동하도록 본문에 살린다. 두 agent 파일을 삭제한다.

**Contracts**: `ralph-loop-init` skill = 직접 실행 generator. discovery·상태 머신·5파일 생성·run.sh 템플릿·CHECKS 자체검증·출력 형식의 단일 소스는 SKILL.md 본문. Step 2 "Present Findings and Confirm" 사용자 확인 게이트는 메인 루프에서 직접 수행(더 이상 subagent 격리로 무력화되지 않음). codex의 Security Notice는 CLI별 flag delta(`--dangerously-bypass-approvals-and-sandbox`)를 보존.

**Acceptance Criteria**:
- [ ] AC1 (흡수 완전성, positive): `.claude/skills/ralph-loop-init/SKILL.md` 본문에 이관 대상 핵심 섹션이 모두 존재한다 — Acceptance Criteria, Hard Rules, State Machine Reference, Process(Step 1~8, run.sh 템플릿 코드블록 포함), Error Handling. 각 섹션 heading + run.sh 템플릿의 핵심 앵커(`VALID_PHASES`, `run_llm_with_timeout`, `acquire_lock`)를 grep으로 확인(존재 = positive 증거).
- [ ] AC2 (확인 게이트 메인 루프화): Step 2 사용자 확인 게이트(검증 방법 = 명령어 + 판정 조건 확정, Hard gate)가 SKILL.md 본문에 메인 루프 수행 단계로 존재한다 — subagent 위임이 아니라 메인 루프가 사용자에게 확인받는 흐름임이 문면으로 드러난다.
- [ ] AC3 (wrapper 잔재 제거): `.claude/skills/ralph-loop-init/SKILL.md`에서 "entrypoint wrapper"·"위임"·`Agent(subagent_type`·`Source: ... agent가 단일 소스` 문구 grep 0.
- [ ] AC4 (codex adapter 제거 + flag delta 보존): `.codex/skills/ralph-loop-init/SKILL.md`가 직접 실행 본문을 보유하고 `Codex Runtime Adapter`·`spawn_agent`·`Agent Message Boundary`가 grep 0. Security Notice의 codex CLI flag `--dangerously-bypass-approvals-and-sandbox`는 보존(claude 본문의 `--dangerously-skip-permissions`와의 delta).
- [ ] AC5 (claude↔codex delta 보존, 정정됨): ralph는 identical copy가 아니라 codex 적응 delta를 보존하는 3-way다. codex SKILL.md는 claude SKILL.md와 **산문 계약 본문**(discovery·State Machine·CHECKS·출력 형식)은 동일하되, codex-CLI 적응 delta를 보존한다 — (a) Security Notice flag `--dangerously-bypass-approvals-and-sandbox`, (b) run.sh의 LLM 호출 블록이 `codex` CLI판(`command -v codex`, `codex exec --json --dangerously-bypass-approvals-and-sandbox -C ... -o LAST_MESSAGE_FILE`)이다. 검증: codex SKILL이 `codex exec`를 포함하고 `claude -p`/`--dangerously-skip-permissions`를 포함하지 않으며, 역으로 claude SKILL은 `claude -p`를 포함하고 `codex exec`를 포함하지 않는다. 구현 방법 = codex SKILL은 `.codex/agents/ralph-loop-init-agent.toml` 본문에서 빌드(delta 자동 보존).
- [ ] AC6 (version lockstep): 4개 version 필드(claude skill.json, claude SKILL.md frontmatter, codex skill.json, codex SKILL.md frontmatter)가 모두 동일 목표값 `4.0.0`이다 (현재 4곳 전부 3.1.0에서 상향).
- [ ] AC7: `.claude/agents/ralph-loop-init-agent.md`와 `.codex/agents/ralph-loop-init-agent.toml`이 삭제됨 (파일 부재).

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- agent 계약 본문 흡수, 확인 게이트 메인 루프화, frontmatter version
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 직접 실행 본문 흡수, Codex adapter/spawn 제거, Security flag delta 보존, frontmatter version
- [M] `.claude/skills/ralph-loop-init/skill.json` -- version 4.0.0
- [M] `.codex/skills/ralph-loop-init/skill.json` -- version 4.0.0
- [D] `.claude/agents/ralph-loop-init-agent.md` -- skill로 흡수, 삭제
- [D] `.codex/agents/ralph-loop-init-agent.toml` -- skill로 흡수, 삭제

### Task 3: 등록 surface·stale 문구에서 두 agent 제거
plugin marketplace agents 배열과 codex agents README의 agent 목록·포괄 단언 prose, 그리고 goal-init의 stale "/agent" 문구에서 삭제된 두 agent 흔적을 제거한다.

**Acceptance Criteria**:
- [ ] AC1: `.claude-plugin/marketplace.json`의 `agents` 배열에서 `ralph-loop-init-agent.md`·`spec-review-agent.md` 두 줄이 제거되어 5개(`plan-review-agent`, `implementation-review-agent`, `simplicity-review-agent`, `pr-review-agent`, `spec-sync-agent`)만 남는다. JSON 유효성 유지(trailing comma 없음).
- [ ] AC2: `.codex/agents/README.md`의 `Agent Set`에서 두 줄, `Inline Writing`에서 `spec-review-agent` 한 줄이 제거되어 5개 agent만 등록된다.
- [ ] AC3 (L1, 포괄 단언 prose 정합): `.codex/agents/README.md`의 intro·Ownership에 있는 "모든 `.codex/skills/*` = 얇은 wrapper, 실제 동작은 agent toml"류 포괄 단언이 전환 후에도 참이 되도록 수정된다 — spec-review·ralph는 직접 실행 skill이므로, 해당 서술을 "custom agent를 spawn하는 일부 skill" 범위로 한정하거나 예외를 명시한다.
- [ ] AC4 (L2, stale 문구): `.claude/skills/goal-init/SKILL.md:34`·`.codex/skills/goal-init/SKILL.md:34`의 "`ralph-loop-init` 스킬/agent를 건드리지 않는다"에서 삭제된 agent를 가리키는 "/agent"를 제거한다 (skill은 유지되므로 "`ralph-loop-init` 스킬을 건드리지 않는다"로).

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- agents 배열 2줄 제거
- [M] `.codex/agents/README.md` -- Agent Set 2줄 + Inline Writing 1줄 제거 + 포괄 단언 prose 한정
- [M] `.claude/skills/goal-init/SKILL.md` -- line 34 "/agent" stale 제거
- [M] `.codex/skills/goal-init/SKILL.md` -- line 34 "/agent" stale 제거

### Task 4: agent 식별자 변형 census 검증 (read-only)
삭제된 두 agent의 식별자가 활성 파일(스킬·플러그인·codex 등록 surface·설정)에 잔존하지 않는지 변형 표기 전수 grep으로 검증한다. skill 이름(`spec-review`, `ralph-loop-init`)은 **유지되므로** 오탐과 구분한다.

**Acceptance Criteria**:
- [ ] AC1: 고유 식별자 census(엄격 0) — `spec-review-agent`, `ralph-loop-init-agent`와 그 변형(`spec_review_agent`, `ralph_loop_init_agent`, `spec-review-agent.md`, `spec-review-agent.toml` 등, `.md`/`.toml`/`subagent_type=`/`agent_type:`/`spawn_agent` 문맥)이 활성 파일(`.claude/`, `.codex/`, `.claude-plugin/`)에서 0건. python 정규식으로 수행(BSD grep lookahead 함정 회피). 기록물(`_sdd/drafts/`, `_sdd/work_log/`, `_sdd/spec/logs/`, `.git/`)은 제외.
- [ ] AC2: 동음이의 확인 — skill 이름 `spec-review`·`ralph-loop-init`(agent suffix 없는 형)은 skill 디렉토리·skill.json·description·상호참조에 **정상 존재**함을 확인(잘못 삭제되지 않음). 즉 agent suffix 붙은 형만 0, skill 형은 살아있음.
- [ ] AC3: stale 문구 잔재 0 — "스킬/agent" 병기(goal-init) 등 삭제된 agent를 암시하는 문구가 활성 파일에 잔존하지 않는다 (L2 편집 확인).
- [ ] AC4: marketplace `agents` 배열 원소 5개, codex README Agent Set 5개로 실제 카운트 일치.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
[없음 — spec-sync 제외는 사용자 확정(주 용도 = 체인 종결). version 목표값은 두 skill 모두 `4.0.0`으로 확정(구조 전환 = major; spec-review는 기존 json 2.3.1↔md 3.0.0 drift를 4.0.0으로 해소, ralph는 4곳 3.1.0→4.0.0). plan-review H1/M1/M2/L1/L2 반영 완료.]
