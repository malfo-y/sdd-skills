# Feature Draft: plan-review gather 병렬화

> 규모 판정: 적격 — 변경 요소 9개가 task 5개에 1:1 배정되어 coverage 눈검산 가능, 단일 컨텍스트 감당 범위

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
plan-review의 벽시계 병목(리뷰 agent의 직렬 Read/Grep 22~25회, 게이트당 9~10분 실측)을 제거한다. orchestrator(SKILL.md)가 draft의 Target Files를 그룹으로 묶어 **병렬 gatherer agent들**에게 컨텍스트 수집을 위임하고, gatherer는 발췌 digest를 `_sdd/pipeline/plan_review_gather/`에 파일로 남긴다. 단일 `plan-review-agent`가 digest 경로 목록을 받아 전역 시야로 판정한다(smell별/렌즈별 판정 분할은 하지 않는다 — 판정은 cross-task 전역이어야 하고, 읽기 병목은 gather가 제거하므로).

새 contract/invariant:
- **digest 파일 계약**: gatherer는 배정 파일들의 draft-관련 구간을 verbatim 발췌(파일당 상한 내)로 `_sdd/pipeline/plan_review_gather/<draft-slug>/` 아래 digest 파일에 기록하고, 반환은 경로 + 1줄 상태로 제한한다. 상한 초과분은 `경로:줄범위` 좌표 목록으로 남긴다. `_sdd/pipeline/`은 `.gitignore` 등재로 로컬 전용을 보장한다(현재 미등재 실측 → 본 feature에서 추가). 리뷰 종료 후 digest를 삭제하지 않는다 — 사후 검시(발췌 누락→false CLEAR 계측) 자산으로 남기고, 같은 draft-slug 재실행이 같은 디렉토리를 덮어써 draft당 최신 1벌만 유지된다.
- **digest 신뢰 한계**: digest는 판정의 출발점이다 — 리뷰어는 의심 구간을 원본 residual read로 확정해야 하며, digest 부재 시(직접 호출 등) 기존 자체-read 동작으로 동작한다(하위 호환).
- **orchestrator read 규칙 개정**: plan-review orchestrator는 gather shard 구성을 위한 **대상 draft 1회 read만** 허용한다. 코드 분석 read 금지는 유지된다.
- 신규 agent `plan-context-gatherer` (Read/Glob/Grep/Write) — marketplace agents 배열·codex 미러에 등록.

게이트 2 임계(고정 임계로 인한 사실상 자동 재게이트) 문제는 본 feature scope 밖 — 별도 feature로 다룬다.

## Scope
- **In**: plan-review Claude 스킬/agent 개편, 신규 gatherer agent 생성·등록, codex 미러 전파, 등록 표면 census 검증
- **Out**: 게이트 2 임계 조정, implementation-review 등 다른 리뷰 스킬로의 gather 패턴 확대, smell별/2-렌즈 판정 분할
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: plan-context-gatherer agent 생성 및 Claude 등록
읽기 병목을 넘겨받을 read-mostly 수집 agent를 정의하고 플러그인에 등록한다 (등록 누락이 파이프라인에서 안 잡히는 기왕 사례가 있어 생성과 등록을 한 task로 닫는다).

**Contracts**: gatherer 입력 = 대상 draft 경로 + 배정 파일 그룹(3~5개) + digest 출력 경로. 출력 = digest 파일 1개 — 배정 파일별로 「draft가 그 파일에 대해 주장/의존하는 것과 관련된 구간의 verbatim 발췌, 파일당 ~150줄 상한, 초과분은 `경로:줄범위` 좌표 목록」. 최종 응답은 digest 경로 + 1줄 상태만(발췌 본문을 응답으로 반환하지 않는다). 요약/의역으로 발췌를 대체하지 않는다. 파일 생성은 digest 출력 경로 1개만 허용.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `.claude/agents/plan-context-gatherer.md`가 존재하고 frontmatter `tools`가 정확히 `["Read", "Glob", "Grep", "Write"]`다. 평가: `grep -A1 '^tools:' .claude/agents/plan-context-gatherer.md` 출력이 위 4개 도구만 포함.
- [ ] AC2 (2등급): 본문이 Contracts의 입력/출력/발췌 상한/반환 제한/요약 금지를 모두 명시한다. 평가: reviewer가 각 항목의 근거 문장을 인용.
- [ ] AC3 (1등급): `.claude-plugin/marketplace.json` agents 배열에 `./.claude/agents/plan-context-gatherer.md` 항목이 있다. 평가: `grep 'plan-context-gatherer' .claude-plugin/marketplace.json` 1 hit.

**Target Files**:
- [C] `.claude/agents/plan-context-gatherer.md` -- 신규 agent 계약은 기존 4개 리뷰 agent 어디에도 속하지 않아 수정으로 닫히지 않음
- [M] `.claude-plugin/marketplace.json` -- agents 배열 등록

### Task 2: plan-review SKILL.md에 gather phase 도입
orchestrator가 읽기를 병렬 shard로 위임하고 판정 agent에는 경로만 중계하도록 실행 절을 개편한다.

**Contracts**: 실행 순서 = ① 대상 draft 1회 read → Target Files(+draft가 명시 참조하는 spec anchor) 추출 ② 디렉토리 근접 기준 3~5 파일/그룹(총량이 그보다 적으면 한 그룹), 최대 ~6그룹으로 묶어 gatherer들을 **한 메시지에서 병렬 dispatch** (digest 출력 경로 `_sdd/pipeline/plan_review_gather/<draft-slug>/` 지정) ③ 반환된 digest 경로 목록만 `plan-review-agent` prompt에 포함해 단일 dispatch. degrade 규칙: Target Files가 비었거나 gather dispatch가 전부 실패하면 gather를 생략하고 기존 단일 dispatch로 진행하고, 일부만 실패하면 성공한 digest만으로 진행한다. `--model` override는 gatherer dispatch에도 동일 적용.

**Acceptance Criteria**:
- [ ] AC1 (2등급): 실행 절이 Contracts의 ①~③ 순서·그룹 규칙·병렬 dispatch·경로만 중계를 명시한다. 평가: reviewer가 각 요소의 근거 문장 인용.
- [ ] AC2 (1등급): "orchestrator는 새 분석 read를 하지 않는다" 문장이 「대상 draft 1회 read만 허용, 코드 read 금지」 개정판으로 대체되었다. 평가: `grep -c '새 분석 read' .claude/skills/plan-review/SKILL.md` = 0 이고 draft 1회 read 허용 문장 존재.
- [ ] AC3 (2등급): degrade 규칙(빈 Target Files/gather 실패 → 기존 단일 dispatch) 문장이 존재한다. 평가: reviewer 인용.
- [ ] AC4 (1등급): `.gitignore`에 `_sdd/pipeline/` 라인이 있다 (digest 산출물이 untracked 오염물로 남지 않도록). 평가: `grep '_sdd/pipeline' .gitignore` ≥ 1 hit.

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` -- 실행 절 개편
- [M] `.gitignore` -- `_sdd/pipeline/` 무시 라인 추가 (현재 실측 부재 — AGENTS.md §2 서술과 달리 `implementation`·`pr`만 등재)

### Task 3: plan-review-agent에 digest 입력 모드 추가
판정 agent가 digest를 출발점으로 흡수하되 원본 확정 의무와 하위 호환을 갖게 한다.

**Contracts**: Input에 「호출자 제공 digest 경로 목록(optional)」 추가. digest 제공 시: 병렬 Read 배치로 일괄 흡수하고, 의심 구간·finding evidence로 쓸 구간은 원본 파일 residual read로 확정한다(digest 인용만으로 Critical/High evidence를 닫지 않는다). digest 미제공 시: 기존 Input 우선순위·자체 read 동작 그대로(하위 호환). Hard Rules·Severity·Step 4 반환 형식은 불변. 말미 Source Pointer의 "SKILL.md는 thin entrypoint wrapper" 서술은 gather orchestration 역할을 반영해 한 문장 갱신한다(codex 동문 갱신은 Task 4 소관).

**Acceptance Criteria**:
- [ ] AC1 (2등급): Input과 Process에 digest optional 입력·병렬 Read 배치·residual read 확정 의무·미제공 시 기존 동작이 모두 명시된다. 평가: reviewer가 근거 문장 인용.
- [ ] AC2 (1등급): Hard Rules 5개 항목·Severity 표·Step 4 반환 항목이 변경 전과 동일하다. 평가: `git diff` 해당 섹션 무변경(hunk 없음).

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- Input/Process에 digest 모드 추가

### Task 4: codex 미러 전파 (3-way merge)
Task 1~3의 변경을 codex 적응 delta(mailbox/target-close contract·framed payload·TOML 형식)를 보존하며 미러에 재적용한다. 단순 복사 금지.

**Contracts**: codex SKILL.md의 gather phase는 Runtime Adapter의 spawn 문법으로 표현한다 — gatherer N개를 각각 `spawn_agent`(고유 task_name)하고 mailbox/target wait로 전 final 수거 후 판정 agent를 단일 spawn. digest 경로·degrade 규칙·**orchestrator read 규칙 개정(대상 draft 1회 read만 허용, 코드 read 금지)**은 Task 2 Contracts와 의미 동일하게 반영한다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `.codex/agents/plan-context-gatherer.toml`이 존재하고 `.codex/agents/README.md` agent 목록에 등재된다. 평가: 두 파일 각각 `grep 'plan-context-gatherer'` ≥ 1 hit.
- [ ] AC2 (2등급): `.codex/skills/plan-review/SKILL.md`가 gather phase(병렬 spawn→wait 수거→단일 판정 spawn)·degrade 규칙·orchestrator read 규칙 개정 문장(기존 "새 분석 read를 하지 않는다" 대체)을 Runtime Adapter 문법으로 명시하고, 기존 codex 적응 delta(contract 선택·framed payload·model override 검증)가 보존된다. 평가: reviewer가 신규 요소(read 규칙 개정 포함)와 보존 요소 각각 인용.
- [ ] AC3 (2등급): `.codex/agents/plan-review-agent.toml`에 Task 3와 의미 동일한 digest 모드가 반영된다. 평가: reviewer 인용 대조.

**Target Files**:
- [C] `.codex/agents/plan-context-gatherer.toml` -- Task 1 agent의 codex 표현은 신규 파일로만 가능
- [M] `.codex/agents/plan-review-agent.toml` -- digest 모드 반영
- [M] `.codex/skills/plan-review/SKILL.md` -- gather phase 반영
- [M] `.codex/agents/README.md` -- agent 목록 등재

### Task 5: 등록·명명 표면 census 검증
신규 이름의 변형 표기가 모든 표면에 등재되고 잔존 누락이 없는지 read-only로 전수 확인한다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `plan-context-gatherer`·`plan_context_gatherer` 두 변형으로 repo 전체 grep 시 hit가 정확히 {`.claude/agents/*.md`, `.claude/skills/plan-review/SKILL.md`, `.claude-plugin/marketplace.json`, `.codex/agents/*.toml`, `.codex/skills/plan-review/SKILL.md`, `.codex/agents/README.md`, 본 draft} 집합 안에 있고, marketplace·codex README 등재 hit가 각각 ≥ 1이다. 평가: `grep -rn -e 'plan-context-gatherer' -e 'plan_context_gatherer' --exclude-dir=.git --exclude-dir=_sdd .` 출력 대조 + draft 등재는 `grep -l 'plan-context-gatherer' _sdd/drafts/2026-08-14_feature_draft_plan_review_parallel_gather.md` 별도 확인 (`_sdd/pipeline/` 로컬 digest 산출물이 위양성 hit를 만들지 않도록 `_sdd`는 통째로 제외).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- digest 저장 위치: 논의 시 scratchpad였으나 Claude 전용 경로라 codex 미러가 공유 불가 → **로컬 전용(gitignored) `_sdd/pipeline/plan_review_gather/<draft-slug>/`로 결정**. 사용자 확인 필요.
- gatherer 구현 방식: general-purpose agent + prompt 제약 대신 **등록 agent 신규 생성으로 결정** — codex spawn_agent가 등록 agent_type을 요구하고, 도구 제한(Write는 digest 출력만)을 frontmatter로 강제 가능. 확인 불필요(아키텍처 근거 명확).
- 게이트 2 임계 조정은 별도 feature로 분리 — 사용자와 기합의.
