# Feature Draft: plan-review 직접 실행 전환 — agent 완전 폐지 (판정 + 수집)

> 규모 판정: 적격 — 변경 요소 6개(SKILL 재작성·agent 4파일 삭제·등록 해제·codex 미러·README·census)가 task 4개에 1:1 배정, coverage 눈검산 가능

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
plan-review를 **agent 0개의 직접 실행 스킬로 전환**한다(판정·수집 모두 메인 루프). 근거 실측 사슬: v4.16.0 gather 도입 → 소비 repo에서 판정 agent가 digest를 두고 원본 전량 재독 → v4.19.0 문면 규칙으로 교정 → **로드된 규칙이 그대로 무시됨**(opus-5, 7분+ 전량 재독). 판정: 읽기 통제를 dispatch된 agent의 순종에 맡기는 층 자체가 실패했고, codex는 도구 박탈이 구조적으로 불가라 무도구 판정자도 반쪽이다. gatherer 존치안(수집만 agent)도 기각 — 병렬 읽기는 메인 루프의 tool call 배칭(독립 Read/Grep을 한 메시지에)으로 동일하게 달성되고, 컨텍스트 절약은 Grep 선행 + 선택적 구간 읽기로 상쇄되며, dispatch 고정비·agent 등록/미러 유지비가 사라진다. 메인 transcript에서 리뷰가 진행되어 사용자 실시간 관측이 가능한 것 자체가 불순종 재발 방지책이다.

**감수하는 트레이드오프**: producer(메인 루프)가 자기 draft를 자기 게이트로 리뷰하는 셀프 리뷰 편향(사용자 결정 — 검출력의 실적 원천이 rubric + evidence 의무였다는 판단, 독립 시선은 `second-opinion` 담당). 대형 draft에서 원본 구간이 메인 컨텍스트에 직접 적재되는 비용(선택적 읽기로 관리).

새 contract/invariant:
- **직접 실행 계약**: `plan-review` SKILL.md가 전체 계약의 단일 소스다 — 5-smell rubric·Severity·Blocker Policy·반환 형식(Blocker Status·Findings, 채팅 반환·리포트 파일 없음)·근거 부족 시 finding 금지·비열거(finding 아닌 확인 결과 미열거)·review-only(대상 draft·코드를 수정하지 않고 finding 반영은 producer 소관)를 SKILL 본문이 보유한다. wrapper↔agent 구조·gather phase·digest 파일(`_sdd/pipeline/plan_review_gather/`) 계약 소멸.
- **읽기 지침**: supporting context는 ① 서로 독립인 Read/Grep을 **한 메시지에 배칭** ② Grep으로 좌표를 먼저 잡고 관련 구간만 선택적 Read ③ spec surface는 draft가 명시 인용한 파일·섹션만, 기록물(`decision_log.md`·`logs/`·`prev/`) 금독 ④ 근거가 부족하면 읽기를 확장하지 않고 그 smell의 finding을 만들지 않는다 (v4.19.0 규칙의 직접 실행 계승).
- **agent 완전 폐지**: `plan-review-agent`·`plan-context-gatherer` claude `.md`·codex `.toml` 4파일 삭제, marketplace agents 배열·codex agents/README Agent Set에서 제거. `--model` override 계약 소멸(dispatch가 없음 — 인자로 오면 적용 대상 없음을 안내).

## Scope
- **In**: plan-review SKILL 2벌 직접 실행 재작성, agent 4파일 삭제·등록 해제, 삭제 census
- **Out**: implementation-review·pr-review의 직접 실행 전환(별도 관측 후), feature-draft의 게이트 호출 계약(스킬 이름 불변), `_sdd/pipeline` gitignore 라인(다른 스킬이 쓸 수 있는 일반 경로라 유지)
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: plan-review SKILL.md 직접 실행 재작성 (claude)
orchestrator+agent 2층을 단층으로 접는다 — agent 본문의 rubric·severity·반환 계약을 SKILL로 이관하고 판정·수집을 메인 루프가 수행한다.

**Contracts**: Part 1 「직접 실행 계약」+「읽기 지침」이 본문 구조의 단일 소스다. 이관 시 agent 본문의 5-smell rubric·Severity 표·Blocker Policy·근거 부족 규칙·비열거 규칙은 의미 보존 이관하고, agent 전용 장치(Codex Agent Boundary·frontmatter·AC 자체검증 절)와 gather phase·digest·`--model` override 절은 이관하지 않는다(인자로 받으면 적용 대상 없음 1줄 안내).

**Acceptance Criteria**:
- [ ] AC1 (1등급): SKILL.md에 5 smell 이름 전부(`Requirement Fit`·`Task Boundary Drift`·`Hidden Decision`·`Over-engineering`·`Verification Weakness`)와 `Severity`가 존재하고, `plan-review-agent`·`plan-context-gatherer`·`digest` 참조가 각 0건이다. 평가: grep.
- [ ] AC2 (1등급): 읽기 지침 anchor `한 메시지에 배칭`·`명시 인용한` 각 ≥ 1. 평가: grep.
- [ ] AC3 (2등급): 본문이 직접 실행 계약 전 요소(판정 주체=메인 루프, review-only, 반환 형식, 근거 부족·비열거 규칙, 읽기 지침 4항, --model 안내)를 담는다. 평가: reviewer 인용.

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` -- 직접 실행 재작성

### Task 2: agent 삭제 + 등록 해제 (claude)
**Acceptance Criteria**:
- [ ] AC1 (1등급): `.claude/agents/plan-review-agent.md`·`.claude/agents/plan-context-gatherer.md` 부재 + marketplace.json에 두 이름 각 0건 + JSON parse OK. 평가: `test -f` 실패 2건, grep 0, `json.load`.

**Target Files**:
- [D] `.claude/agents/plan-review-agent.md` -- 판정 주체 이관으로 소멸
- [D] `.claude/agents/plan-context-gatherer.md` -- 수집 주체 이관으로 소멸
- [M] `.claude-plugin/marketplace.json` -- agents 배열에서 2건 제거

### Task 3: codex 미러 전파
Task 1·2를 codex 적응 delta 보존으로 재적용한다 — agent dispatch가 사라지므로 Codex Runtime Adapter·framed payload 블록도 이 스킬에서 소멸한다(직접 실행 스킬 전례: `spec-review`·`ralph-loop-init`). codex판 override 안내는 `--model`뿐 아니라 `--effort`도 적용 대상 없음에 포함한다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `.codex/agents/plan-review-agent.toml`·`.codex/agents/plan-context-gatherer.toml` 부재 + `.codex/agents/README.md`에 두 이름 각 0건. 평가: `test -f` 실패 2건, grep 0.
- [ ] AC2 (2등급): `.codex/skills/plan-review/SKILL.md`가 Task 1과 의미 동일한 직접 실행 계약을 담고 `spawn_agent`·Runtime Adapter·gather 잔재 참조가 없다. 평가: reviewer 인용 + `grep -c -e 'spawn_agent' -e 'digest'` 0 (Task 1 AC1과 대칭).

**Target Files**:
- [D] `.codex/agents/plan-review-agent.toml` -- 동일 소멸
- [D] `.codex/agents/plan-context-gatherer.toml` -- 동일 소멸
- [M] `.codex/skills/plan-review/SKILL.md` -- 직접 실행 재작성
- [M] `.codex/agents/README.md` -- Agent Set에서 2건 제거

### Task 4: 삭제 census 검증
**Acceptance Criteria**:
- [ ] AC1 (1등급): live 스킬·에이전트·등록 표면에서 `plan-review-agent`·`plan_review_agent`·`plan-context-gatherer`·`plan_context_gatherer` 변형 grep 잔존이 0건이다. 평가: `grep -rn -e 'plan-review-agent' -e 'plan_review_agent' -e 'plan-context-gatherer' -e 'plan_context_gatherer' .claude .codex .claude-plugin AGENTS.md CLAUDE.md README.md` 출력 0행 — 명시 경로 한정 이진 판정. `docs/`는 별도 grep으로 hit 목록만 보고하고 AC 판정에서 제외한다(문서 기록물 갱신은 후속 docs 정비 소관).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 셀프 리뷰 편향 감수·gatherer까지 완전 폐지 — 사용자 결정(2026-08-15 대화: "수집을 agent로 안 하면 알아서 자체 병렬화 할 수 있는 거 아냐"). 확인 불필요.
- 기존 `_sdd/pipeline/plan_review_gather/` 산출물은 삭제하지 않는다(로컬 기록물, gitignored). `.gitignore`의 `_sdd/pipeline/` 라인도 유지. 확인 불필요.
