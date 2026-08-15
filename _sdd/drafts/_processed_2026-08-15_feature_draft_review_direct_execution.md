# Feature Draft: implementation-review·pr-review correctness 직접 실행 전환

> 규모 판정: 적격 — 변경 요소(스킬 재작성 2쌍·agent 삭제 4·등록 해제 3·잔존 참조 갱신)가 task 6개에 1:1 배정되어 coverage 눈검산 가능. rename/삭제 census형 신호가 있어 마지막에 read-only 검증 task 예약.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

plan-review 직접 실행 전환(v4.20.0)과 같은 근거("읽기 통제는 순종이 아니라 구조로")를 implementation-review·pr-review의 correctness 렌즈로 확장한다. 원격 실측에서 dispatch된 reviewer agent가 로드된 읽기 규칙을 무시하는 문제가 재현 위험으로 남아 있었고, dispatch 왕복(correctness 1+N shard)이 게이트 벽시계의 큰 성분이었다.

- **새 contract**: `implementation-review`·`pr-review`의 correctness 리뷰는 **메인 루프가 직접 수행**한다. simplicity 렌즈만 `simplicity-review-agent`로 dispatch하며, dispatch를 먼저 띄운 뒤 correctness를 병행 수행해 벽시계를 두 작업의 max로 만든다.
- **새 contract**: correctness 계약(리뷰 차원·severity·fresh verification·읽기 계단·ledger MET 접기·기준 문서 적응)의 단일 소스는 각 SKILL.md다 — `implementation-review-agent`·`pr-review-agent`(claude/codex 4파일)는 삭제되고 등록 해제된다.
- **소멸하는 contract**: correctness task별 shard 분할(1+N)과 그 연접 relay, correctness용 "대화에만 있는 맥락 digest"(메인 루프가 대화를 직접 보유하므로 불요 — simplicity dispatch message에만 잔존), `--model` override의 correctness 적용(simplicity dispatch에만 적용으로 축소).
- **유지**: simplicity-review-agent 계약 전체(2묶음 병렬 dispatch in implementation-review, 통짜 4차원 1회 in pr-review), pr-review의 verdict 합성·통합 리포트·PR Review Input(simplicity 전달용으로 잔존), 단일 작성자 불변식, slow-test 정책(UNTESTED 라우팅은 메인 루프 correctness가 계승).
- **셀프 리뷰 편향 감수**: implementation-review는 producer(메인 루프)가 자기 구현을 검증하게 된다 — plan-review 전환과 같은 논리로 감수한다(증거 결속·rubric이 탐지의 실체, 독립 시선은 simplicity agent와 `second-opinion`).
- 남는 등록 agent는 `simplicity-review-agent` 1종이다.

## Scope

- **In**: implementation-review·pr-review SKILL.md 재작성(claude/codex 4벌), correctness agent 4파일 삭제, marketplace.json·.codex/agents/README.md·README.md 등록 해제, simplicity-review-agent 2벌의 형제 참조 갱신, implementation SKILL 2벌의 gate 합산 문면, pr-review 예시 파일 갱신, 삭제 census.
- **Out**: simplicity-review-agent의 계약 변경(차원·묶음·severity 불변), plan-review·다른 스킬, gate 2 임계 비례화(별건 Planned), spec surface 갱신(spec-sync 소관).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: `.claude/skills/implementation-review/SKILL.md`를 직접 실행 + simplicity dispatch 하이브리드로 재작성한다

orchestrator·shard·digest 구조를 걷어내고, correctness 계약을 `implementation-review-agent.md`에서 흡수한 직접 실행 스킬로 다시 쓴다.

**Contracts**:
- 실행 순서: ① simplicity 2묶음(참조 ∥ 국소)을 **한 메시지에 병렬 dispatch**(각 dispatch는 전체 변경 대상, 묶음 정의는 agent `호출자 차원 한정` 절이 단일 소스) → ② agent가 도는 동안 **메인 루프가 correctness 리뷰를 직접 수행** → ③ 두 반환을 수거해 correctness 결과와 함께 합산 severity로 보고.
- correctness 절이 흡수하는 것(구 agent 계약): 기준 문서 적응(draft→spec→git 변경 범위 graceful degradation + stale 강등), 읽기 계단 3단(변경 파일 hunk 기본 + 승격 트리거 6종 + `hunk-scoped` 표기 / 인접 표면 Grep 우선 / 탐색적 읽기 금지 — AC 명시 증거만 예외), Fresh Verification(증거 없는 MET 금지, 30초 중단, slow는 checkpoint 한정 + `UNTESTED(slow — checkpoint 대기)`), findings 4단계 분류, 반환 형식(Status·Findings·Verification ledger MET 접기·Recommendations Min-Code·Assumptions).
- digest 규칙은 simplicity dispatch에만 잔존한다(agent는 대화를 못 읽으므로) — correctness용 digest·shard 분할표·연접 relay 문면은 제거.
- `--model <name>`은 simplicity dispatch에만 적용하고 그 사실을 스킬 문면에 명시한다. 읽기 배칭·Grep 선행은 plan-review SKILL과 같은 지침 문면으로 명시한다.

**Acceptance Criteria**:
- [ ] AC1: `rtk grep -c "메인 루프가" .claude/skills/implementation-review/SKILL.md` ≥ 1이고, `rtk grep -n -e "shard" -e "digest" -e "implementation-review-agent" .claude/skills/implementation-review/SKILL.md`에서 correctness dispatch 배관 잔존이 0행이다(simplicity 관련 digest 문면은 "simplicity" 동반 행만 허용 — grep 출력을 인용해 판정).
- [ ] AC2 (rubric): 재작성된 스킬이 Contracts의 실행 순서(simplicity 먼저 dispatch → correctness 병행)와 흡수 항목(기준 문서 적응·읽기 계단·Fresh Verification·ledger MET 접기)을 모두 보유한다 — reviewer가 구 agent 문면과 대조 인용으로 판정.

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md` -- 재작성

### Task 2: `.claude/skills/pr-review/SKILL.md`의 correctness를 직접 실행으로 전환한다

Step 3의 2-agent 병렬 dispatch를 "simplicity 1 dispatch + 메인 루프 correctness 직접 수행"으로 바꾼다. verdict 합성·통합 리포트·Step 0~2 수집은 유지한다.

**Contracts**:
- 실행 순서: simplicity dispatch(통짜 4차원 1회, PR Review Input 전달)를 먼저 띄우고, 메인 루프가 correctness(Review Dimensions Code-only 항상 + Spec-based 조건부, 정확성-중복 잔존·형태-중복은 simplicity 소관, Fresh Verification CI→local→`UNTESTED`, findings 분류, AC ledger MET 접기)를 직접 수행한 뒤 반환을 수거해 Step 4 verdict로 간다.
- 흡수 소스는 `pr-review-agent.md`의 Review Dimensions·Hard Rules(표적 disjoint 경계·from-branch 기준·Fresh Verification·Min-Code)·Findings Classification·ledger 형식이다. verdict 미판정 규칙(구 Hard Rule 3)은 소멸한다 — correctness 수행자와 verdict 합성자가 같은 메인 루프다.
- AC3·AC6 등 dispatch 전제 AC를 새 구조로 고쳐 쓴다(`--model`은 simplicity dispatch에만 적용). PR Review Input은 simplicity 전달용 계약으로 잔존한다.

**Acceptance Criteria**:
- [ ] AC1: `rtk grep -n "pr-review-agent" .claude/skills/pr-review/SKILL.md` 0행이고, `rtk grep -c "simplicity-review-agent" .claude/skills/pr-review/SKILL.md` ≥ 1이다.
- [ ] AC2 (rubric): correctness 절이 Review Dimensions(Code-only/Spec-based)·정확성-중복 경계·Fresh Verification 사다리·ledger MET 접기를 보유하고, verdict 표·합류 규칙·Output Format·단일 작성자 불변식이 유지됐다 — 구 문면 대조 인용으로 판정.

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md` -- correctness 직접 실행 전환

### Task 3: correctness agent 4파일을 삭제하고 등록을 해제한다

**Acceptance Criteria**:
- [ ] AC1: `ls` 확인으로 `.claude/agents/implementation-review-agent.md`·`.claude/agents/pr-review-agent.md`·`.codex/agents/implementation-review-agent.toml`·`.codex/agents/pr-review-agent.toml`이 존재하지 않는다.
- [ ] AC2: `.claude-plugin/marketplace.json` agents 배열과 `.codex/agents/README.md` Agent Set이 `simplicity-review-agent` 1항목이다 (grep/Read 인용).

**Target Files**:
- [D] `.claude/agents/implementation-review-agent.md` -- correctness 직접 실행 전환
- [D] `.claude/agents/pr-review-agent.md` -- 동일
- [D] `.codex/agents/implementation-review-agent.toml` -- 동일
- [D] `.codex/agents/pr-review-agent.toml` -- 동일
- [M] `.claude-plugin/marketplace.json` -- agents 배열 축소
- [M] `.codex/agents/README.md` -- Agent Set 축소

### Task 4: 잔존 참조를 새 구조에 정합화한다

simplicity-review-agent 2벌의 형제 참조(Hard Rule 2 "implementation-review-agent 소관"·Integration 절·"두 reviewer의 Input Data" 등 수신자 문구 — 수신자는 simplicity 1종), implementation SKILL 2벌의 gate 문면("raw shard 합산" → 직접 correctness finding + simplicity 반환 합산), README.md(agent 3종→1종, model override 표), `.claude/skills/pr-review/examples/sample-review.md`의 dispatch 예시를 갱신한다.

**Acceptance Criteria**:
- [ ] AC1: `rtk grep -n "shard" .claude/skills/implementation/SKILL.md .codex/skills/implementation/SKILL.md` 0행이고, gate 합산 문면이 직접 correctness + simplicity 반환 합산으로 읽힌다(해당 행 인용).
- [ ] AC2: `.claude/agents/simplicity-review-agent.md`·`.codex/agents/simplicity-review-agent.toml`에서 `implementation-review-agent`·`pr-review-agent` 참조가 0행이고, correctness 소관 문면이 "호출 스킬의 메인 루프"로 대체됐다 (grep 인용).
- [ ] AC3: `README.md`와 `sample-review.md`에서 두 agent 이름 참조가 0행이다 (grep 인용).
- [ ] AC4 (rubric): README override 절(`README.md` "모델 override" 부근)이 `implementation-review`·`pr-review`의 `--model`이 simplicity dispatch에만 적용됨을 서술한다 — 해당 행 인용으로 판정.

**Target Files**:
- [M] `.claude/agents/simplicity-review-agent.md` -- 형제 참조 갱신
- [M] `.codex/agents/simplicity-review-agent.toml` -- 동일 (3-way 적응)
- [M] `.claude/skills/implementation/SKILL.md` -- gate 합산 문면
- [M] `.codex/skills/implementation/SKILL.md` -- 동일
- [M] `README.md` -- agent 목록·override 표
- [M] `.claude/skills/pr-review/examples/sample-review.md` -- dispatch 예시

### Task 5: codex 미러 2벌을 3-way 적응으로 재작성한다

Task 1·2 결과를 `.codex/skills/{implementation-review,pr-review}/SKILL.md`에 이식한다 — codex 적응 delta(custom agent 어휘, Codex Runtime Adapter는 **simplicity spawn 1종만** 남긴 축약본, Read/Grep 고유명사 대신 일반 어휘, `--model`/`--effort` schema 검증 문면)를 보존하고 새 본문을 재적용한다.

**Acceptance Criteria**:
- [ ] AC1: `rtk grep -n -e "implementation-review-agent" -e "pr-review-agent" .codex/skills/implementation-review/SKILL.md .codex/skills/pr-review/SKILL.md` 0행이고, 두 파일 모두 `simplicity-review-agent` spawn 문면을 보유한다.
- [ ] AC2 (rubric): claude 본문과 계약 등가(실행 순서·correctness 흡수 항목·잔존 Adapter가 simplicity spawn만 기술)임을 diff 대조로 판정.
- [ ] AC3: `.codex/skills/pr-review/examples/sample-review.md`에서 "두 렌즈 spawn" 서술 잔존이 0행이고 예시 흐름이 simplicity 단일 spawn + correctness 직접 수행으로 읽힌다 (grep + 해당 행 인용).

**Target Files**:
- [M] `.codex/skills/implementation-review/SKILL.md` -- 3-way 재작성
- [M] `.codex/skills/pr-review/SKILL.md` -- 3-way 재작성
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- 예시 흐름 갱신 (agent 이름 리터럴이 없어 census를 통과하므로 명시 배정)

### Task 6: 삭제 census (read-only 검증)

**Acceptance Criteria**:
- [ ] AC1: 변형형 포함 전수 grep — `implementation-review-agent`·`pr-review-agent`·`implementation_review_agent`·`pr_review_agent` 4패턴을 `.claude .codex .claude-plugin AGENTS.md CLAUDE.md README.md` 명시 경로에서 실행해 출력 0행이다 (`_sdd/spec`은 spec-sync 소관으로 제외).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- pr-review의 simplicity dispatch는 현행(차원 한정 없는 통짜 4차원 1회)을 유지하기로 결정 — 사용자가 "simplicity review는 충분히 빨라"라고 판단했고 경로 변경 요청이 없다. 확인 불요.
- implementation-review의 simplicity 2묶음 분할도 현행 유지로 결정 — 같은 근거. 확인 불요.
- 셀프 리뷰 편향 감수는 사전 대화에서 사용자가 인지한 상태로 진행 지시("진행하자")했으므로 확인 불요.
