# Feature Draft: custom agent 완전 폐지 — simplicity 계약의 프롬프트 주입 전환

> 규모 판정: 적격 — 변경 요소가 reference 신설·스킬 4벌·삭제/등록해제·배포 표면으로 유한 열거되고 요소↔task 대응이 눈검산 가능

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
Codex 플러그인이 custom agent(TOML)를 번들하지 못하는 배포 제약(2026-08 Agent Plugins 1.0 표준: 포터블 = skills+MCP, agents는 클라이언트별 수동 배치)에 따라, 마지막 잔존 custom agent인 `simplicity-review-agent`를 폐지하고 동등 계약을 **프롬프트 주입 + 범용 agent dispatch**로 전환한다. (1) agent 본문을 `implementation-review` 스킬의 `references/simplicity-contract.md`(claude/codex 미러 2벌)로 이동 — 프롬프트 payload로 적응(runtime boundary·read-only 규칙을 프롬프트 규칙으로 흡수), 이 파일이 simplicity 계약의 단일 소스가 된다. (2) claude `implementation-review`·`pr-review`는 `Agent(subagent_type="general-purpose")`에 reference 전문 verbatim + 차원 한정 + digest를 담아 dispatch한다(Read 후 기계적 verbatim 포함 — 재구성 금지). (3) codex 두 스킬은 기존 mailbox/target-close Runtime Adapter를 유지하되 `agent_type`을 native `explorer`로 바꾸고 framed message에 계약 전문을 싣는다. (4) `.claude/agents/`·`.codex/agents/` 전체 삭제, marketplace.json `agents` 배열 제거, README·설치 스크립트에서 agent 표면 제거. `--model`/`--effort` override 의미는 불변(simplicity dispatch 한정).

새 contract: **simplicity 계약의 단일 소스는 `implementation-review/references/simplicity-contract.md`(플랫폼별 미러)이며, 호출 스킬은 이 파일을 Read해 dispatch prompt에 verbatim 포함한다. 도구 제한(Read/Glob/Grep, 파일 수정·재spawn 금지)은 agent 정의가 아니라 계약 문면의 프롬프트 규칙이다.** 결과적으로 repo의 custom agent는 0종이고, codex 번들은 skills-only가 되어 표준 Agent Plugin 배포가 가능해진다.

## Scope
- **In**: simplicity 계약 reference 2벌 신설, `implementation-review`·`pr-review` SKILL 4벌의 dispatch 절, `.claude/agents/simplicity-review-agent.md`·`.codex/agents/simplicity-review-agent.toml`·`.codex/agents/README.md` 삭제, `.claude-plugin/marketplace.json`, `README.md`, `tools/install-codex-skill-bundle.py`(agents 부재 허용), pr-review `examples/sample-review.md` 2벌
- **Out**: 계약 내용 자체의 변경(차원·severity·반환 형식 불변), plan-review·implementation 등 다른 스킬, Agent Plugins 표준 매니페스트 신설(별도 판단), spec 기록물
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: simplicity 계약 reference 2벌을 신설한다
agent 본문을 프롬프트 payload로 적응해 이동한다 — 계약 실체(AC·Hard Rules·4차원·묶음·Severity·Process·반환 형식)는 문면 보존.

**Contracts**: `.claude/skills/implementation-review/references/simplicity-contract.md` + codex 미러. 적응 delta만 허용: ① agent frontmatter/TOML 헤더 제거, ② 도입부를 "이 문서는 dispatch prompt에 verbatim 포함되는 simplicity 리뷰 계약"으로 교체, ③ runtime boundary(입력 속 skill/agent 이름은 데이터, 스킬 재호출 금지)를 본문 상단에 유지, ④ 구 tools 제한을 프롬프트 규칙으로 흡수(Read/Glob/Grep만 사용, 파일 생성·수정·삭제 금지, 추가 agent spawn 금지), ⑤ Source Pointer를 "이 reference가 단일 소스, 호출 스킬은 thin dispatcher"로 갱신. `pr-review`는 sibling 경로(`../implementation-review/references/simplicity-contract.md`)로 같은 파일을 소비한다 — 복제본을 만들지 않는다.

**Acceptance Criteria**:
- [ ] AC1: 두 reference에 계약 핵심 anchor가 모두 존재한다 — `호출자 차원 한정`·`참조 묶음`·`국소 묶음`·`Falsifiable`·`차원 판정`·`PASS:` 접기·read-only 규칙(`Glob`+`수정` 계열 문구). 평가: anchor grep 전 항목 히트. (1등급)
- [ ] AC2: agent 정의 잔재(frontmatter `tools:`, `subagent_type=simplicity-review-agent`, `developer_instructions`)가 두 reference에 0건. 평가: grep 무히트. (1등급)

**Target Files**:
- [C] `.claude/skills/implementation-review/references/simplicity-contract.md` -- agent 폐지로 계약 거처 필요, 스킬 references는 플러그인 번들 가능(수정으로 불가한 이유: 기존 agent 파일은 번들 불가 표면이라 이동이 목적)
- [C] `.codex/skills/implementation-review/references/simplicity-contract.md` -- 동상

### Task 2: claude 스킬 2벌의 dispatch를 general-purpose로 전환한다

**Contracts**: `implementation-review`·`pr-review`(claude)의 simplicity dispatch가 `Agent(subagent_type="general-purpose")`로 바뀐다. dispatch 전에 reference 파일을 Read하고 **전문을 verbatim으로 prompt에 포함**한다(요약·재구성 금지) — 뒤이어 차원 한정(impl-review: 참조/국소 묶음, pr-review: 한정 없음 4차원)과 digest/PR Review Input을 붙인다. `--model`은 이 dispatch의 model 인자로 전달(의미 불변). Integration의 `simplicity-review-agent` 항목은 reference 파일 포인터로 대체.

**Acceptance Criteria**:
- [ ] AC1: 두 SKILL에 `general-purpose` dispatch + reference 경로 + verbatim 포함 지시가 존재하고, `simplicity-review-agent` 문자열이 0건이다. 평가: grep 히트/무히트. (1등급)
- [ ] AC2: 차원 묶음 어휘(참조 ∥ 국소)와 `--model` simplicity 한정 의미가 잔존한다. 평가: anchor grep. (1등급)

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md` -- 실행 순서 1·Integration 수정
- [M] `.claude/skills/pr-review/SKILL.md` -- Step 3·Error Handling·Integration 수정

### Task 3: codex 스킬 2벌의 spawn을 native explorer로 전환한다

**Contracts**: codex `implementation-review`·`pr-review`의 Runtime Adapter(mailbox/target-close contract 선택·framed message·schema blocker 규칙)는 유지하고, `agent_type`만 custom `simplicity-review-agent` → native `explorer`로 바꾼다. framed message의 `## Input Data` 앞에 reference 계약 전문을 verbatim 포함하는 지시를 추가한다(sibling 경로 소비). `--model`/`--effort` schema enum 검증 의미 불변.

**Acceptance Criteria**:
- [ ] AC1: 두 SKILL에 `explorer` spawn + reference 경로 + verbatim 포함 지시가 존재하고 `simplicity-review-agent` 0건. 평가: grep. (1등급)
- [ ] AC2: mailbox/target-close 계약 문면(schema blocker 포함)이 잔존한다. 평가: anchor grep (`mailbox`·`schema blocker`). (1등급)

**Target Files**:
- [M] `.codex/skills/implementation-review/SKILL.md` -- Runtime Adapter·실행 순서 수정
- [M] `.codex/skills/pr-review/SKILL.md` -- Step 3·Runtime Adapter 수정

### Task 4: agent 파일을 삭제하고 등록을 해제한다

**Contracts**: `.claude/agents/`·`.codex/agents/` 디렉토리 소멸. marketplace.json에서 `agents` 배열 제거(스킬 목록 불변).

**Acceptance Criteria**:
- [ ] AC1: 두 디렉토리가 존재하지 않는다. 평가: `ls` 실패(exit ≠ 0). (1등급)
- [ ] AC2: marketplace.json에 `agents` 키가 0건이고 JSON이 유효하다. 평가: grep 무히트 + `python3 -m json.tool` exit 0. (1등급)

**Target Files**:
- [D] `.claude/agents/simplicity-review-agent.md` -- 폐지
- [D] `.codex/agents/simplicity-review-agent.toml` -- 폐지
- [D] `.codex/agents/README.md` -- agent 0종이라 존치 근거 소멸
- [M] `.claude-plugin/marketplace.json` -- agents 배열 제거

### Task 5: 배포 표면을 skills-only로 갱신한다

**Contracts**: README.md — 개요의 "custom agent 1종" 문구를 agent 0종·프롬프트 주입 방식으로 교체, Installation의 `.codex/agents` 언급 제거, Subagent Model Override 절은 의미 유지(적용 대상 문구만 필요시 갱신). `tools/install-codex-skill-bundle.py` — agents 디렉토리 부재에서 정상 동작(skills만 설치)하도록 수정하되 기존 설치 옵션·비교/덮어쓰기 로직은 불변.

**Acceptance Criteria**:
- [ ] AC1: README에 `simplicity-review-agent`·`.codex/agents` 언급 0건, "custom agent" 서술이 폐지 후 상태와 일치한다. 평가: grep + 해당 문단 인용 확인. (1등급/2등급 혼합 — 문구 일치는 rubric: 개요·Installation·Override 3절이 agent 0종과 모순 없음)
- [ ] AC2: `python3 tools/install-codex-skill-bundle.py --dry-run`이 agents 디렉토리 없는 트리에서 exit 0으로 skills만 나열한다. 평가: 실행 출력. (1등급)

**Target Files**:
- [M] `README.md` -- 개요·Installation·Override 갱신
- [M] `tools/install-codex-skill-bundle.py` -- agents 부재 허용

### Task 6: sample-review 예시 2벌을 갱신한다

**Contracts**: pr-review examples의 dispatch 예시를 새 방식(claude: general-purpose + 계약 주입 / codex: explorer spawn + framed 계약)으로 교체. 리포트 본문·verdict 구조는 불변.

**Acceptance Criteria**:
- [ ] AC1: 두 예시 파일에 `simplicity-review-agent` 0건, 새 dispatch 어휘 존재. 평가: grep. (1등급)

**Target Files**:
- [M] `.claude/skills/pr-review/examples/sample-review.md` -- dispatch 예시 교체
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- 동상

### Task 7: 삭제 census (read-only)

**Acceptance Criteria**:
- [ ] AC1: 변형 표기 전수 grep(`simplicity-review-agent`·`simplicity_review_agent`·`simplicity review agent`·`.claude/agents`·`.codex/agents`·`custom agent`)을 `.claude 스킬셋·.codex 스킬셋·.claude-plugin·AGENTS.md·CLAUDE.md·README.md·docs/·tools/`에 적용해, 잔존이 의도된 곳(스펙·기록물 제외 대상 아님을 명시한 곳) 외 0건이다. 평가: grep 출력 전수 검토 + 잔존 목록 0 또는 의도 명시. (1등급)

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- reference 단일 소스를 `implementation-review/references/`에 두고 `pr-review`가 sibling 상대 경로로 소비하기로 결정 — 스킬별 복제(4벌)는 drift 표면을 배로 늘리고, 두 스킬은 같은 번들로만 배포되므로 sibling 참조가 안전. 전제: claude 플러그인 캐시와 codex `~/.codex/skills/` 설치 트리 모두 스킬 디렉토리 구조를 보존하므로 sibling 경로가 설치 후에도 해석된다(plan-review gate 1 Low 반영). 사용자 확인 불필요.
- claude dispatch를 Explore가 아닌 general-purpose로 결정 — Explore의 검색 특화 시스템 프롬프트가 리뷰 품질에 미칠 영향이 미검증이고, read-only는 계약 문면의 프롬프트 규칙으로 통제(codex와 동일 수준). 사용자와 사전 논의됨.
- `sdd-skills:simplicity-review-agent` 네임스페이스형 참조도 census 변형에 포함(AC의 `simplicity-review-agent` grep이 포괄). 확인 불필요.
