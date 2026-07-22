# Feature Draft (Lite): full 전용 agent·스킬 삭제 + 등록 표면 정리 (F2)

> Lite 적격: 적격 — 삭제 대상(agent 4종 쌍·스킬 3종 쌍)과 등록·문서 표면이 전수 열거된 1:1 대응으로 눈검산 가능, 단일 세션 규모. 삭제 이름의 변형 참조가 흩어진 census형 신호는 마지막 검증 task(Task 5)로 대응. (분할 계획 원본: `_sdd/drafts/2026-07-22_feature_draft_lite_full_lane_removal.md`의 F2)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
full 레인 전용 실행 유닛을 삭제한다: agent 4종(feature-draft-agent·task-ordering-agent·test-author-agent·implementation-agent)과 스킬 3종(feature-draft·implementation·implementation-plan), claude·codex 쌍 전부. 등록 표면(marketplace.json skills/agents 배열, codex agents README)과 살아있는 문서(AGENTS.md SDD 흐름, 루트 README 목록)를 lite 체인 기준으로 정리한다.

- **트리거 흡수 (사용자 확정)**: 일반 구현 요청 트리거("implement the plan", "start implementation", "execute the plan", "구현해줘" 계열)를 `implementation-lite` description이 흡수한다 — lite가 유일 실행 경로이므로 일반 구현 요청은 lite로 라우팅된다. "병렬 구현" 계열 트리거는 폐기.
- 출제자·응시자 분리(test-author)의 대체 안전장치는 implementation-lite의 테스트 불변 규칙 + implementation-review Fresh Verification (slice 2 결정 기록 참조).

## Scope
- **In**: 위 삭제 대상 14파일 + 6디렉토리, marketplace.json, `.codex/agents/README.md`, `AGENTS.md`, `README.md`, implementation-lite description 쌍, 삭제 이름의 live dangling 참조 정리(simplicity-review-agent 쌍 등)
- **Out**: reviewer full 기계장치 트림(F3 — plan-review-agent 쌍의 full Tier·Orchestrator Review Mode 등), spec full 서술 트림과 잔재 폐기(F4), pr-review·spec 계열·ralph·discussion·guide-create 스킬
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: full 스킬 3종 쌍 삭제 + marketplace skills 배열 정리
각 디렉토리는 SKILL.md+skill.json뿐임을 실측 확인함.

**Acceptance Criteria**:
- [ ] AC1: 아래 [D] 디렉토리 6개가 부재한다 (`ls` 실패).
- [ ] AC2: marketplace.json skills 배열에 `feature-draft`·`implementation`·`implementation-plan` 항목이 없고(-lite·-review 항목은 유지), JSON이 유효하다.

**Target Files**:
- [D] `.claude/skills/feature-draft/` -- SKILL.md, skill.json
- [D] `.claude/skills/implementation/` -- 동일
- [D] `.claude/skills/implementation-plan/` -- 동일
- [D] `.codex/skills/feature-draft/` -- 동일
- [D] `.codex/skills/implementation/` -- 동일
- [D] `.codex/skills/implementation-plan/` -- 동일
- [M] `.claude-plugin/marketplace.json` -- skills 배열 3항목 제거

### Task 2: full agent 4종 쌍 삭제 + agents 등록 정리
**Acceptance Criteria**:
- [ ] AC1: 아래 [D] 파일 8개가 부재한다.
- [ ] AC2: marketplace.json agents 배열에 4개 agent 항목이 없고 JSON이 유효하다.
- [ ] AC3: `.codex/agents/README.md`에 삭제 agent 이름이 없다.

**Target Files**:
- [D] `.claude/agents/feature-draft-agent.md` / [D] `.claude/agents/task-ordering-agent.md` / [D] `.claude/agents/test-author-agent.md` / [D] `.claude/agents/implementation-agent.md`
- [D] `.codex/agents/feature-draft-agent.toml` / [D] `.codex/agents/task-ordering-agent.toml` / [D] `.codex/agents/test-author-agent.toml` / [D] `.codex/agents/implementation-agent.toml`
- [M] `.claude-plugin/marketplace.json` -- agents 배열 4항목 제거
- [M] `.codex/agents/README.md` -- 삭제 agent 목록 항목 제거

### Task 3: implementation-lite 트리거 흡수 (v1.2.0)
일반 구현 요청이 lite로 라우팅되도록 description을 확장한다. "병렬 구현" 계열은 넣지 않는다.

**Acceptance Criteria**:
- [ ] AC1: description(SKILL frontmatter + skill.json, 쌍 동일)에 "implement the plan"·"start implementation"·"execute the plan"·"구현해줘" 트리거가 있고 "병렬 구현"·"parallel implementation"이 없다.
- [ ] AC2: frontmatter=skill.json 버전 1.2.0 일치, codex 미러 identical.

**Target Files**:
- [M] `.claude/skills/implementation-lite/SKILL.md` -- frontmatter description
- [M] `.claude/skills/implementation-lite/skill.json` -- 동일
- [M] `.codex/skills/implementation-lite/SKILL.md` -- identical copy
- [M] `.codex/skills/implementation-lite/skill.json` -- 동일

### Task 4: 살아있는 문서·참조를 lite 체인 기준으로 정리
plan-review H1·H2·M1 반영으로 표면 확장 — F1이 영어 가이드 미러를 escape한 사실 기록(후속 census에 en 미러 포함 습관화 근거).

**Acceptance Criteria**:
- [ ] AC1: AGENTS.md(:23-24)와 **하네스 템플릿 4미러**(spec-create·spec-upgrade의 `references/agents-harness-template.md` claude·codex 쌍)의 SDD 단계 흐름이 lite 체인(feature-draft-lite → plan-review → implementation-lite → implementation-review → spec-sync)으로 갱신됐다.
- [ ] AC2: README.md **Subagent Model Override 목록·예시**(L112-129 부근)에서 삭제 스킬 항목·`/implementation --model` 예시가 제거됐다 — lite 치환은 하지 않는다(implementation-lite는 작성 무dispatch라 override 비대상; 거짓 문서 방지).
- [ ] AC3: simplicity-review-agent 쌍의 "implementation-agent REFACTOR Hard Rule" dangling 참조가 제거/재서술됐다.
- [ ] AC4: `docs/en/AUTOPILOT_GUIDE.md`가 한국어 2.0.0 기준 영어 미러로 재작성됐다 (구세계 어휘 33건 잔존 해소 — F1 escape 교정).
- [ ] AC5: 기타 live 참조가 정리됐다 — discussion SKILL 쌍(:12 `Pre-feature-draft` 연계, :428 후속 스킬 목록) + `examples/sample-discussion-session.md:115`, spec-sync-agent 쌍(:221-222 consumer 목록), spec-summary example 쌍(:32 경로, :39 `/feature-draft`).

**Target Files**:
- [M] `AGENTS.md` -- SDD 흐름 서술
- [M] `.claude/skills/spec-create/references/agents-harness-template.md` / [M] `.codex/skills/spec-create/references/agents-harness-template.md` -- SDD 흐름 라인
- [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md` / [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- 동일
- [M] `README.md` -- Subagent Model Override 목록·예시
- [M] `.claude/agents/simplicity-review-agent.md` / [M] `.codex/agents/simplicity-review-agent.toml` -- 과잉압축 차원의 참조 1곳
- [M] `docs/en/AUTOPILOT_GUIDE.md` -- 영어 미러 재작성
- [M] `.claude/skills/discussion/SKILL.md` / [M] `.codex/skills/discussion/SKILL.md` -- 연계·후속 목록 lite 이름 치환
- [M] `.claude/skills/discussion/examples/sample-discussion-session.md` / [M] `.codex/skills/discussion/examples/sample-discussion-session.md` -- 동일 (:115)
- [M] `.claude/agents/spec-sync-agent.md` / [M] `.codex/agents/spec-sync-agent.toml` -- consumer 목록 lite 이름 치환
- [M] `.claude/skills/spec-summary/examples/summary-output.md` / [M] `.codex/skills/spec-summary/examples/summary-output.md` -- 경로·커맨드 치환

### Task 5: 잔존 검증 (read-only) — 삭제 이름 변형 census
Task 1~4 완료 후 실행. `-lite`·`-review` 접미 이름과의 substring 충돌을 구분하는 패턴으로 전수 grep한다.

**Acceptance Criteria**:
- [ ] AC1: live 표면(`.claude/`·`.codex/`·`.claude-plugin/`·`docs/`·`README.md`·`AGENTS.md`)에서 삭제 이름 참조 잔존 0 — 패턴: `feature-draft-agent`, `task-ordering`, `test-author`, `implementation-agent`, `feature_draft`류 underscore 변형(artifact glob `*_feature_draft_lite_*` 등은 제외), 그리고 `feature-draft`/`implementation`/`implementation-plan`의 스킬명 참조(뒤에 `-lite`/`-review`가 붙지 않는 형태 — `rg -P` lookahead 또는 매치 후 제외 2단 필터로 판정). 허용 예외: ① 기록물(`_sdd/`·`.sdd-workbench/exports/`) ② F3 소관 reviewer 표면 — plan-review-agent 쌍(full Tier 서술) + implementation-review-agent 쌍(:194 implementation-plan 기준 언급) ③ AUTOPILOT_GUIDE(ko·en)의 tag 복구 FAQ ④ `docs/SDD_SPEC_DEFINITION.md`(:165·172 "feature-draft Part 2" — 검증 rubric 닻 문서의 재서술은 F4 spec 트림 소관).
- [ ] AC2: grep 명령·결과가 마감 증거 테이블에 남았다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 트리거 흡수 범위: 사용자 확정("implementation-lite로 흡수") — "병렬 구현" 계열 폐기 포함. 확인 완료.
- implementation-review-agent 실측 완료(plan-review M2): kebab agent 언급 0건, `implementation-plan` :194 1곳뿐 — census 예외 ②에 확정 반영. 해소됨.
